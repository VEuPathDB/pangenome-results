#!/usr/bin/env python3
"""Explore pangenes that hold more than one gene in the same genome.

get_pangenes sometimes puts two (or more) genes of the SAME genome in one pangene. For every such
group this script lists each pair of genes (neighbours along the chromosome) and reports:
  - whether their CDSs overlap (the 7b `<genome>_intersect_pairs.tsv` report, >= --min-overlap-bp),
  - the gap between the two genes (negative = the gene spans overlap),
  - same or opposite strand,
  - each gene's source layer (main / good_<genome> / rescued_<genome> / own annotation), its
    `intersect=` tag, and whether it has a protein domain (InterPro/PFAM).

Inputs:
  --genes-matrix  pangene_matrix_genes.tr.tab from get_pangenes (cells = gene IDs, "-" = absent)
  --tagged-dir    step 05's 7b output: <genome>_final_annotation_tagged.gff and <genome>_intersect_pairs.tsv
Writes <out-prefix>_pairs.tsv (one row per gene pair) and prints a summary.

Standard library only.
"""
import argparse
import csv
import os
import re
import sys
from collections import Counter

ID_RE = re.compile(r"(?:^|;)ID=([^;]+)")
PARENT_RE = re.compile(r"(?:^|;)Parent=([^;]+)")
ORIG_RE = re.compile(r"(?:^|;)original_ID=([^;]+)")
INTERSECT_RE = re.compile(r"(?:^|;)intersect=([^;]+)")
DBXREF_RE = re.compile(r"(?:^|;)Dbxref=([^;]+)")


def parse_tagged_gff(path):
    """new gene ID -> dict(chrom, start, end, strand, source, tag, orig, domain)."""
    genes, mrna_gene = {}, {}
    with open(path) as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            f = line.rstrip("\n").split("\t")
            if len(f) < 9:
                continue
            attrs = f[8]
            if f[2] == "gene":
                i = ID_RE.search(attrs)
                if not i:
                    continue
                o, t = ORIG_RE.search(attrs), INTERSECT_RE.search(attrs)
                genes[i.group(1)] = {"chrom": f[0], "start": int(f[3]), "end": int(f[4]), "strand": f[6],
                                     "source": f[1], "tag": t.group(1) if t else "NA",
                                     "orig": o.group(1) if o else "", "domain": False}
            elif f[2] in ("mRNA", "transcript"):
                i, p = ID_RE.search(attrs), PARENT_RE.search(attrs)
                if i and p:
                    mrna_gene[i.group(1)] = p.group(1)
            elif f[2] == "CDS":
                p, d = PARENT_RE.search(attrs), DBXREF_RE.search(attrs)
                if p and d and any(t.startswith(("InterPro:", "PFAM:")) for t in d.group(1).split(",")):
                    g = genes.get(mrna_gene.get(p.group(1), p.group(1)))
                    if g:
                        g["domain"] = True
    return genes


def parse_pairs(path):
    """set of frozenset({original_ID_a, original_ID_b}) with a CDS overlap."""
    pairs = set()
    if os.path.exists(path):
        with open(path) as fh:
            next(fh, None)
            for line in fh:
                f = line.rstrip("\n").split("\t")
                if len(f) >= 3:
                    pairs.add(frozenset((f[0], f[2])))
    return pairs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--genes-matrix", required=True)
    ap.add_argument("--tagged-dir", required=True)
    ap.add_argument("--gff-suffix", default="_final_annotation_tagged.gff")
    ap.add_argument("--pairs-suffix", default="_intersect_pairs.tsv")
    ap.add_argument("-o", "--out-prefix", required=True)
    args = ap.parse_args()

    with open(args.genes_matrix, newline="") as fh:
        rows = list(csv.reader(fh, delimiter="\t"))
    cols = [(i, g.replace("_for_get_pangenes", "")) for i, g in enumerate(rows[0]) if i > 0 and g.strip()]

    genes, cds_pairs = {}, {}
    for _, genome in cols:
        gff = os.path.join(args.tagged_dir, genome + args.gff_suffix)
        if not os.path.exists(gff):
            sys.exit(f"ERROR: missing {gff}")
        genes[genome] = parse_tagged_gff(gff)
        cds_pairs[genome] = parse_pairs(os.path.join(args.tagged_dir, genome + args.pairs_suffix))
        print(f"{genome}: {len(genes[genome])} genes", file=sys.stderr)

    out_rows, multi_pangenes, missing = [], set(), 0
    for r in rows[1:]:
        if r[0].startswith("chr"):
            continue
        for i, genome in cols:
            cell = r[i] if i < len(r) else ""
            if cell in ("", "-", "NA") or "," not in cell:
                continue
            multi_pangenes.add(r[0])
            members = []
            for gid in cell.split(","):
                g = genes[genome].get(gid)
                if g is None:
                    missing += 1
                    continue
                members.append((gid, g))
            members.sort(key=lambda x: (x[1]["chrom"], x[1]["start"]))
            for (ida, a), (idb, b) in zip(members, members[1:]):
                same_chrom = a["chrom"] == b["chrom"]
                gap = (b["start"] - a["end"]) if same_chrom else ""
                out_rows.append([r[0], genome, len(members), ida, idb, a["chrom"], b["chrom"], a["start"], a["end"],
                                 b["start"], b["end"], "same" if a["strand"] == b["strand"] else "opposite", gap,
                                 "yes" if frozenset((a["orig"], b["orig"])) in cds_pairs[genome] else "no",
                                 a["source"], b["source"], a["tag"], b["tag"],
                                 "yes" if a["domain"] else "no", "yes" if b["domain"] else "no"])

    header = ["pangene", "genome", "genes_in_cell", "gene_a", "gene_b", "chrom_a", "chrom_b", "start_a", "end_a",
              "start_b", "end_b", "strand", "gap_bp", "cds_overlap", "source_a", "source_b", "tag_a", "tag_b",
              "domain_a", "domain_b"]
    with open(args.out_prefix + "_pairs.tsv", "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(header)
        w.writerows(out_rows)

    n = len(out_rows)
    print(f"\n{len(multi_pangenes)} pangenes with >1 gene in some genome; {n} neighbouring gene pairs"
          + (f"; {missing} gene IDs not found in the GFFs" if missing else ""))
    if n == 0:
        return

    def gapbin(row):
        gap = row[12]
        if gap == "":
            return "different chromosomes"
        if row[13] == "yes":
            return "CDS overlap"
        if gap < 0:
            return "gene spans overlap, no CDS overlap"
        if gap <= 1000:
            return "no overlap, gap <= 1 kb"
        if gap <= 5000:
            return "no overlap, gap 1-5 kb"
        return "no overlap, gap > 5 kb"

    print("\nHow the two genes of each pair sit relative to each other:")
    for k, v in sorted(Counter(gapbin(r) for r in out_rows).items(), key=lambda x: -x[1]):
        print(f"  {k:38s} {v:6d}  ({100 * v / n:.1f}%)")
    print("\nStrand:", dict(Counter(r[11] for r in out_rows)))
    print("Domain (gene_a, gene_b):", dict(Counter((r[18], r[19]) for r in out_rows)))
    print("Source of the pair:", dict(Counter(tuple(sorted((r[14].split("_")[0], r[15].split("_")[0]))) for r in out_rows).most_common(8)))
    cds = {r[0] for r in out_rows if r[13] == "yes"}
    print(f"\nPangenes where at least one pair has a CDS overlap: {len(cds)} of {len(multi_pangenes)}")


if __name__ == "__main__":
    main()
