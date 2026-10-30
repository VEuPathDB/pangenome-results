#!/usr/bin/env python3
"""Find the apicoplast contigs of every genome from blastn hits of the reference apicoplast sequence.

Tgondii-only, step 01. Input: one <genome>.tsv per genome, blastn of the reference apicoplast (ME49 KE138841) against
the genome, -outfmt '6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen'.

For every contig with a hit, the share of the CONTIG covered by the hits is computed (not the share of the apicoplast
covered by the contig: assemblies that collapse the apicoplast inverted repeat give a ~24 kb contig that holds the
whole apicoplast but covers only ~71% of the 35 kb reference). A contig with at least --min-contig-cov of its length
covered is an apicoplast contig; smaller shares are apicoplast DNA inserted in nuclear contigs (NUPTs) and are kept.

Outputs:
  <out-dir>/apicoplast_hits.tsv    every contig with a hit: genome, contig, length, pct_of_contig, mean pident,
                                   n_genes (from --gff-dir, if given), apicoplast_contig yes/no
  <out-dir>/apicoplast_contigs.tsv the apicoplast contigs, in the column layout of redundant_contigs_removed.tsv
                                   (genome, contig, length, pct_duplicated=NA, n_genes, reason=apicoplast), to add to
                                   the contig list removed before step 05's build

Standard library only.
"""
import argparse
import glob
import os
from collections import defaultdict


def merged(iv):
    iv = sorted(iv)
    total, (cs, ce) = 0, iv[0]
    for s, e in iv[1:]:
        if s > ce:
            total += ce - cs + 1
            cs, ce = s, e
        else:
            ce = max(ce, e)
    return total + ce - cs + 1


def count_genes(path, contigs):
    n = defaultdict(int)
    if not os.path.exists(path):
        return n
    with open(path) as fh:
        for line in fh:
            f = line.split("\t")
            if len(f) > 8 and f[0] in contigs and f[2] == "gene" and "Parent=" not in f[8]:
                n[f[0]] += 1
    return n


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--blast-dir", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--min-contig-cov", type=float, default=0.9, help="share of the contig covered by hits to call it apicoplast (default 0.9)")
    ap.add_argument("--gff-dir", default="", help="final GFFs, to count the genes on each contig (optional)")
    ap.add_argument("--gff-suffix", default="_final_annotation_filtered.gff")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    hits, apico = [], []
    for path in sorted(glob.glob(os.path.join(args.blast_dir, "*.tsv"))):
        genome = os.path.basename(path)[:-4]
        iv, slen, pid = defaultdict(list), {}, defaultdict(list)
        with open(path) as fh:
            for line in fh:
                f = line.rstrip("\n").split("\t")
                if len(f) < 14:
                    continue
                s, e = sorted((int(f[8]), int(f[9])))
                iv[f[1]].append((s, e))
                slen[f[1]] = int(f[13])
                pid[f[1]].append(float(f[2]))
        genes = count_genes(os.path.join(args.gff_dir, genome + args.gff_suffix), set(iv)) if args.gff_dir else {}
        for c in iv:
            cov = merged(iv[c]) / slen[c]
            is_ap = cov >= args.min_contig_cov
            hits.append([genome, c, slen[c], f"{100 * cov:.1f}", f"{sum(pid[c]) / len(pid[c]):.1f}",
                         (str(genes.get(c, 0)) if args.gff_dir else ""), "yes" if is_ap else "no"])
            if is_ap:
                apico.append([genome, c, str(slen[c]), "NA", (str(genes.get(c, 0)) if args.gff_dir else ""), "apicoplast"])

    hits.sort(key=lambda r: (r[0], r[6] != "yes", -int(r[2])))
    with open(os.path.join(args.out_dir, "apicoplast_hits.tsv"), "w") as out:
        out.write("genome\tcontig\tlength\tpct_of_contig\tmean_pident\tn_genes\tapicoplast_contig\n")
        for r in hits:
            out.write("\t".join(map(str, r)) + "\n")
    with open(os.path.join(args.out_dir, "apicoplast_contigs.tsv"), "w") as out:
        out.write("genome\tcontig\tlength\tpct_duplicated\tn_genes\treason\n")
        for r in apico:
            out.write("\t".join(r) + "\n")
    with_ap = sorted({r[0] for r in apico})
    without = sorted({r[0] for r in hits} - set(with_ap))
    print(f"{len(apico)} apicoplast contig(s) in {len(with_ap)} genome(s); no apicoplast contig in: {', '.join(without) or '-'}")


if __name__ == "__main__":
    main()
