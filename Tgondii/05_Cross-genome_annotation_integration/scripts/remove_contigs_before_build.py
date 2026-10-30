#!/usr/bin/env python3
"""Remove the listed contigs (redundant, apicoplast) from the inputs of step 05's build, so the build is redone
without them and Liftoff does not have to run again.

Tgondii-only. The contig screens were done after Liftoff; removing the contigs from the build's inputs gives the
same result as removing them before Liftoff: no gene on those contigs, no transfer of their genes, no transfer onto
them, and the places their transfers took are free again for the other genes during the build.
Nothing is overwritten: everything is written to new folders.

  1. The contig lists (any number, each with columns genome and contig) are joined; a contig in more than one list
     is removed once.
  2. Prepared GFFs (--gff-dir, <genome><--gff-suffix>): every line on a listed contig of that genome is dropped (gene,
     its children, the ##sequence-region line). The IDs of the genes removed are collected per genome.
  3. Liftoff outputs (--pairwise-dir, <source>_onto_<target><--pair-suffix>): dropped are every feature on a listed
     contig of the target, and every transfer of a gene removed from the source in step 2 (same ID, or the same ID
     with a copy suffix _<n>), with all its children. A file with nothing to drop is linked, not copied.
  4. With --genome-dir, every genome FASTA is written to --out-genome-dir without the listed contigs (for
     get_pangenes); a genome with nothing to remove is linked, not copied.

    remove_contigs_before_build.py --list 01_Genome_Selection_QC/redundant_contigs_removed.tsv \\
        --list 01_Genome_Selection_QC/apicoplast_screen/apicoplast_contigs.tsv \\
        --gff-dir gff_for_liftoff --gff-suffix .gff3 --out-gff-dir gff_for_liftoff_nonredundant \\
        --pairwise-dir liftoff_output/polished --pair-suffix _liftoff.gff3_polished \\
        --out-pairwise-dir liftoff_output/polished_nonredundant \\
        --genome-dir genomes --genome-suffix .fna --out-genome-dir genomes_nonredundant \\
        --report 05_Cross-genome_annotation_integration/contigs_removed_before_build.tsv

Standard library only.
"""
import argparse
import csv
import os
import re
import sys
from collections import defaultdict

ID_RE = re.compile(r"(?:^|;)ID=([^;]+)")
PARENT_RE = re.compile(r"(?:^|;)Parent=([^;]+)")


def read_lists(paths):
    out = defaultdict(set)
    for path in paths:
        with open(path, newline="") as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                out[r["genome"]].add(r["contig"])
    return out


def link(src, dst):
    if os.path.lexists(dst):
        os.remove(dst)
    os.symlink(os.path.abspath(src), dst)


def filter_gff(src, dst, contigs, drop_ids=frozenset()):
    """Copy src to dst without the features on `contigs` and without the top-level features whose ID (or ID minus a
    copy suffix _<n>) is in drop_ids, with their children. Returns (IDs of top-level features removed on the
    contigs, number of transfers removed). Children must come after their parent (as in these GFFs)."""
    on_contig, removed, n_drop = set(), set(), 0
    with open(src) as fin, open(dst, "w") as fout:
        for line in fin:
            if line.startswith("##sequence-region"):
                parts = line.split()
                if len(parts) > 1 and parts[1] in contigs:
                    continue
            elif not line.startswith("#"):
                f = line.split("\t")
                if len(f) >= 9:
                    m, p = ID_RE.search(f[8]), PARENT_RE.search(f[8])
                    if f[0] in contigs:
                        if m and not p:
                            on_contig.add(m.group(1))
                        continue
                    if m and not p:
                        i = m.group(1)
                        b = re.match(r"^(.*)_\d+$", i)
                        if i in drop_ids or (b and b.group(1) in drop_ids):
                            removed.add(i); n_drop += 1
                            continue
                    if p and any(x in removed for x in p.group(1).split(",")):
                        if m:
                            removed.add(m.group(1))
                        continue
            fout.write(line)
    return on_contig, n_drop


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", action="append", required=True, help="contig table (genome, contig); can be given more than once")
    ap.add_argument("--gff-dir", required=True)
    ap.add_argument("--gff-suffix", required=True)
    ap.add_argument("--out-gff-dir", required=True)
    ap.add_argument("--pairwise-dir", required=True)
    ap.add_argument("--pair-suffix", required=True)
    ap.add_argument("--out-pairwise-dir", required=True)
    ap.add_argument("--genome-dir", default="")
    ap.add_argument("--genome-suffix", default=".fna")
    ap.add_argument("--out-genome-dir", default="")
    ap.add_argument("--report", required=True)
    args = ap.parse_args()

    contigs = read_lists(args.list)
    genomes = sorted(n[:-len(args.gff_suffix)] for n in os.listdir(args.gff_dir) if n.endswith(args.gff_suffix))
    for g in contigs:
        if g not in genomes:
            sys.exit(f"ERROR: {g} is in a contig list but {g}{args.gff_suffix} is not in {args.gff_dir}")

    # 1. prepared GFFs
    os.makedirs(args.out_gff_dir, exist_ok=True)
    origin = {}
    for g in genomes:
        src, dst = os.path.join(args.gff_dir, g + args.gff_suffix), os.path.join(args.out_gff_dir, g + args.gff_suffix)
        if not contigs.get(g):
            link(src, dst); origin[g] = set()
            continue
        origin[g], _ = filter_gff(src, dst, contigs[g])
        print(f"{g}: {len(contigs[g])} contigs, {len(origin[g])} genes removed from its own annotation")

    # 2. Liftoff outputs
    os.makedirs(args.out_pairwise_dir, exist_ok=True)
    onto = defaultdict(int); dropped = defaultdict(int); n_files = n_links = 0
    for name in sorted(os.listdir(args.pairwise_dir)):
        if not name.endswith(args.pair_suffix) or "_onto_" not in name:
            continue
        s, t = name[:-len(args.pair_suffix)].split("_onto_", 1)
        src, dst = os.path.join(args.pairwise_dir, name), os.path.join(args.out_pairwise_dir, name)
        if not contigs.get(t) and not origin.get(s):
            link(src, dst); n_links += 1
            continue
        on_ctg, n_drop = filter_gff(src, dst, contigs.get(t, set()), frozenset(origin.get(s, set())))
        onto[t] += len(on_ctg); dropped[s] += n_drop; n_files += 1
    print(f"Liftoff outputs: {n_files} filtered, {n_links} linked unchanged")

    # 3. genomes for get_pangenes
    if args.genome_dir:
        os.makedirs(args.out_genome_dir, exist_ok=True)
        for g in genomes:
            src, dst = os.path.join(args.genome_dir, g + args.genome_suffix), os.path.join(args.out_genome_dir, g + args.genome_suffix)
            if not os.path.exists(src):
                sys.exit(f"ERROR: missing {src}")
            cset = contigs.get(g, set())
            if not cset:
                link(src, dst)
                continue
            keep, n_out = True, 0
            with open(src) as fin, open(dst, "w") as fout:
                for line in fin:
                    if line.startswith(">"):
                        keep = line[1:].split()[0] not in cset
                        n_out += not keep
                    if keep:
                        fout.write(line)
            if n_out != len(cset):
                print(f"WARNING: {g}: {len(cset)} contigs listed, {n_out} found in {src}", file=sys.stderr)

    with open(args.report, "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["genome", "contigs_removed", "own_genes_removed", "transfers_onto_its_removed_contigs",
                    "transfers_of_its_removed_genes_into_other_genomes"])
        for g in genomes:
            w.writerow([g, len(contigs.get(g, ())), len(origin[g]), onto[g], dropped[g]])
    print(f"\n{sum(len(v) for v in contigs.values())} contigs in {len(contigs)} genomes; "
          f"{sum(len(v) for v in origin.values())} genes removed from the genomes' own annotations; "
          f"{sum(onto.values())} transfers onto removed contigs and {sum(dropped.values())} transfers of removed genes "
          f"dropped from the Liftoff outputs. Report: {args.report}")


if __name__ == "__main__":
    main()
