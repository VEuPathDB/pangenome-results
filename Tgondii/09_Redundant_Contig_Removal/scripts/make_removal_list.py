#!/usr/bin/env python3
"""List the contigs to remove after the redundancy check (Tgondii-only, step 09).

Reads <label>.contigs.tsv (from contig_redundancy_final.slurm.sh) and keeps every small contig that
carries at least one gene and is either
  flagged        class small-redundant (>= 90% duplicated in a longer contig), whatever the BLAST verdict
  just under the cut   not flagged, but duplicated between --near-min and 90% (default 75%)
Contigs with no gene are left out: with no gene in the final annotation they add nothing to the pangenome.
Large contigs (>= 1 Mb) are never listed.

    make_removal_list.py --red-dir <contig_redundancy_final> -o redundant_contigs_removed.tsv

Writes a tab-separated table: genome, contig, length, pct_duplicated, n_genes, reason. Standard library only.
"""
import argparse
import csv
import glob
import os


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--red-dir", required=True, help="folder with <label>.contigs.tsv")
    ap.add_argument("--near-min", type=float, default=75.0, help="lowest %% duplicated counted as just under the cut (default 75)")
    ap.add_argument("--dup-frac", type=float, default=90.0, help="the cut used by the screen (default 90)")
    ap.add_argument("-o", "--out", required=True)
    args = ap.parse_args()

    rows = []
    for path in sorted(glob.glob(os.path.join(args.red_dir, "*.contigs.tsv"))):
        genome = os.path.basename(path)[:-len(".contigs.tsv")]
        with open(path, newline="") as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                dup, n = float(r["pct_duplicated_in_longer_contig"]), int(r["n_genes"])
                if r["class"] == "large" or n == 0:
                    continue
                if r["class"] == "small-redundant":
                    reason = "flagged"
                elif args.near_min <= dup < args.dup_frac:
                    reason = "just under the cut"
                else:
                    continue
                rows.append((genome, r["contig"], int(r["length"]), dup, n, reason))
    with open(args.out, "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["genome", "contig", "length", "pct_duplicated", "n_genes", "reason"])
        for g, c, L, d, n, why in rows:
            w.writerow([g, c, L, f"{d:.1f}", n, why])
    for why in ("flagged", "just under the cut"):
        sel = [r for r in rows if r[5] == why]
        print(f"{why}: {len(sel)} contigs, {sum(r[4] for r in sel)} genes, {sum(r[2] for r in sel):,} bp")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
