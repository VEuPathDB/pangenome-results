#!/usr/bin/env python3
"""Remove the genes of the redundant contigs from the final GFFs and from the get_pangenes matrices.

Tgondii-only, step 09. Nothing is overwritten: the filtered GFFs and matrices are written to new folders.

  1. Every line on a listed contig is dropped from <genome><--gff-suffix> (gene and all its children, and the
     ##sequence-region line of the contig). The IDs of the top-level features removed are collected.
  2. pangene_matrix_genes.tr.tab: those IDs are taken out of every cell; a cell left empty becomes "-", a
     pangene left with no gene is dropped.
  3. pangene_matrix.tr.tab (counts) is rebuilt from the filtered genes matrix, same rows and columns.
     Other get_pangenes outputs (POCS.matrix.tab, ...) are NOT recomputed and are not copied.

The IDs in the matrices are the ones of the GFFs given to get_pangenes, so run it once per set (7a and 7b),
each with its own GFF folder and matrices. Neighbourhoods used by get_pangenes are not recomputed; rerun
get_pangenes on the new GFFs if an exact result is needed.

    remove_redundant_contig_genes.py --list redundant_contigs_removed.tsv \\
        --gff-dir tagged_annotation --gff-suffix _final_annotation_tagged.gff --out-gff-dir annotation_7b \\
        --matrix-dir for_get_pangenes_7b_pangenes --out-matrix-dir pangenes_7b --report report_7b.tsv

Standard library only.
"""
import argparse
import csv
import os
import re
import sys
from collections import defaultdict

ID_RE = re.compile(r"(?:^|;)ID=([^;]+)")
EMPTY = ("", "-", "NA")


def read_list(path):
    out = defaultdict(set)
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            out[r["genome"]].add(r["contig"])
    return out


def filter_gff(src, dst, contigs):
    removed_ids, n_lines = set(), 0
    with open(src) as fin, open(dst, "w") as fout:
        for line in fin:
            if line.startswith("##sequence-region"):
                parts = line.split()
                if len(parts) > 1 and parts[1] in contigs:
                    continue
            elif not line.startswith("#"):
                f = line.split("\t")
                if f[0] in contigs:
                    n_lines += 1
                    if len(f) >= 9 and "Parent=" not in f[8]:
                        m = ID_RE.search(f[8])
                        if m:
                            removed_ids.add(m.group(1))
                    continue
            fout.write(line)
    return removed_ids, n_lines


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", required=True, help="table from make_removal_list.py")
    ap.add_argument("--gff-dir", required=True)
    ap.add_argument("--gff-suffix", required=True)
    ap.add_argument("--out-gff-dir", required=True)
    ap.add_argument("--matrix-dir", required=True, help="folder with pangene_matrix.tr.tab and pangene_matrix_genes.tr.tab")
    ap.add_argument("--out-matrix-dir", required=True)
    ap.add_argument("--report", required=True)
    args = ap.parse_args()

    contigs = read_list(args.list)
    os.makedirs(args.out_gff_dir, exist_ok=True)
    os.makedirs(args.out_matrix_dir, exist_ok=True)

    removed, report = set(), []
    for genome in sorted(contigs):
        src = os.path.join(args.gff_dir, genome + args.gff_suffix)
        if not os.path.exists(src):
            sys.exit(f"ERROR: missing {src}")
    for name in sorted(os.listdir(args.gff_dir)):
        if not name.endswith(args.gff_suffix):
            continue
        genome = name[:-len(args.gff_suffix)]
        ids, n_lines = filter_gff(os.path.join(args.gff_dir, name), os.path.join(args.out_gff_dir, name),
                                  contigs.get(genome, set()))
        removed |= ids
        report.append([genome, len(contigs.get(genome, ())), len(ids), n_lines])
        if ids:
            print(f"{genome}: {len(contigs[genome])} contigs, {len(ids)} top-level features, {n_lines} lines removed")

    genes_in = os.path.join(args.matrix_dir, "pangene_matrix_genes.tr.tab")
    counts_in = os.path.join(args.matrix_dir, "pangene_matrix.tr.tab")
    with open(genes_in, newline="") as fh:
        genes_rows = list(csv.reader(fh, delimiter="\t"))
    with open(counts_in, newline="") as fh:
        counts_rows = list(csv.reader(fh, delimiter="\t"))
    counts_by_id = {r[0]: r for r in counts_rows[1:]}

    new_genes = [genes_rows[0]]
    new_counts = [counts_rows[0]] + [r for r in counts_rows[1:] if r[0].startswith("chr")]   # "unsorted" row, as it is
    n_pangenes = n_dropped = n_reduced = n_genes_removed = n_mismatch = 0
    dropped_occ, seen = [], set()
    for r in genes_rows[1:]:
        if r[0].startswith("chr") or r[0] not in counts_by_id:
            new_genes.append(r)
            continue
        n_pangenes += 1
        old_counts = counts_by_id[r[0]]
        row_g, row_c, before, after, occ_before = [r[0]], [r[0]], 0, 0, 0
        for i in range(1, len(r)):
            cell = r[i]
            if cell in EMPTY:
                row_g.append(cell)
                row_c.append("0")
                continue
            genes = cell.split(",")
            occ_before += 1
            kept = [g for g in genes if g not in removed]
            seen |= {g for g in genes if g in removed}
            n_genes_removed += len(genes) - len(kept)
            before += len(genes)
            after += len(kept)
            row_g.append(",".join(kept) if kept else "-")
            row_c.append(str(len(kept)))
            if i < len(old_counts) and old_counts[i] not in ("NA", "") and int(float(old_counts[i])) != len(genes):
                n_mismatch += 1
        # keep trailing empty cells (the files end each line with a tab)
        row_g += r[len(row_g):]
        row_c += old_counts[len(row_c):]
        if after == 0:
            n_dropped += 1
            dropped_occ.append(occ_before)
            continue
        if after < before:
            n_reduced += 1
        new_genes.append(row_g)
        new_counts.append(row_c)

    for path, rows in ((os.path.join(args.out_matrix_dir, "pangene_matrix_genes.tr.tab"), new_genes),
                       (os.path.join(args.out_matrix_dir, "pangene_matrix.tr.tab"), new_counts)):
        with open(path, "w", newline="") as fh:
            csv.writer(fh, delimiter="\t", lineterminator="\n").writerows(rows)

    with open(args.report, "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["genome", "contigs_removed", "features_removed", "gff_lines_removed"])
        w.writerows(report)
    print(f"\ngenes removed from the GFFs: {len(removed)}; found in the matrix: {len(seen)}; "
          f"not in the matrix: {len(removed) - len(seen)}")
    print(f"pangenes: {n_pangenes} -> {n_pangenes - n_dropped} ({n_dropped} removed, {n_reduced} lost some genes)")
    if dropped_occ:
        from collections import Counter
        print("removed pangenes by occupancy:", dict(sorted(Counter(dropped_occ).items())))
    if n_mismatch:
        print(f"WARNING: {n_mismatch} cells where the original count differs from the number of gene IDs", file=sys.stderr)
    print(f"Wrote {args.out_gff_dir}/, {args.out_matrix_dir}/ and {args.report}")


if __name__ == "__main__":
    main()
