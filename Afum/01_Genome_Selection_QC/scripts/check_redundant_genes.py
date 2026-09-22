#!/usr/bin/env python3
"""
Verify that the genes on a `small-redundant` contig are genuinely already present
elsewhere in the same assembly — the check to run before dropping such a contig.

For each gene on the flagged contig(s):
  1. cut its genomic span out of the assembly           (samtools faidx)
  2. blastn it against the whole assembly               (blastn -subject)
  3. keep the best hit that is NOT on the gene's own contig
  4. see whether that hit lands on an annotated gene     (gff_originals GFF)

A gene is `duplicated` when its best off-contig hit is >= --min-id identity over
>= --min-cov of the gene's length AND overlaps an annotated gene there. A contig
is `DROP-OK` only when every one of its genes is `duplicated`.

    check_redundant_genes.py <project_dir> [label ...] [options]

With no labels it does every genome whose contig_redundancy/<label>.contigs.tsv
has a `small-redundant` row carrying genes.

Needs `samtools` and `blastn` on PATH. Per genome it writes to contig_redundancy/ :
  <label>.redundant_genes.tsv        one row per gene: descriptions + verdict
  <label>.redundant_genes.fa        the extracted gene spans (for manual BLAST / TE-aid)
  <label>.redundant_genes.blast.tsv the raw blastn hits
and prints a per-contig verdict (DROP-OK / REVIEW) with the unconfirmed genes.
"""
import argparse
import collections
import os
import subprocess
import sys
import tempfile
import urllib.parse


def sh(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def find_file(*paths):
    for p in paths:
        if os.path.exists(p):
            return p
    return None


def merged_len(iv):
    if not iv:
        return 0
    iv = sorted(iv)
    tot = 0
    cs, ce = iv[0]
    for s, e in iv[1:]:
        if s <= ce:
            ce = max(ce, e)
        else:
            tot += ce - cs
            cs, ce = s, e
    tot += ce - cs
    return tot


def _desc(attrs):
    """Best human-readable label from GFF attributes."""
    for k in ("product", "description", "Note", "Name", "gene"):
        v = attrs.get(k)
        if v:
            return urllib.parse.unquote(v)
    return ""


# Gene-level feature types (GFF3 column 3). NCBI GFFs use plain "gene" for
# everything; VEuPathDB/FungiDB GFFs (e.g. AF293, A1160, A1163 in this
# project) commonly use "protein_coding_gene" instead, with
# "pseudogene"/"tRNA_gene"/etc for the rest. A bare f[2] == "gene" check
# recognises none of those - read_gff_genes() would then fall back to the
# mRNA-derived list below for every gene on such a genome (still not silent,
# but a multi-isoform gene gets counted/spanned per-transcript instead of
# once), so the real gene-level feature types are matched directly here.
GENE_FEATURE_TYPES = {
    "gene", "protein_coding_gene", "pseudogene", "ncRNA_gene",
    "tRNA_gene", "rRNA_gene", "snoRNA_gene", "snRNA_gene", "miRNA_gene",
}


def read_gff_genes(gff):
    """[(seqid, start, end, gene_id, description)] for gene features (fallback: mRNA).

    `product` usually lives on the mRNA, not the gene, so it is pulled up to the
    parent gene when present.
    """
    span, gattr = {}, {}                 # gene_id -> (seqid,s,e) / attrs
    prod_by_parent = {}                  # gene_id -> product (from its mRNA)
    mrna = []                            # fallback if the GFF has no gene lines
    with open(gff) as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            f = line.rstrip("\n").split("\t")
            if len(f) < 9 or (f[2] not in GENE_FEATURE_TYPES and f[2] != "mRNA"):
                continue
            attrs = dict(kv.split("=", 1) for kv in f[8].split(";") if "=" in kv)
            if f[2] in GENE_FEATURE_TYPES:
                gid = attrs.get("ID") or attrs.get("gene_id") or attrs.get("Name") or f"{f[0]}:{f[3]}"
                span[gid] = (f[0], int(f[3]), int(f[4]))
                gattr[gid] = attrs
            else:
                par = attrs.get("Parent", "").split(",")[0]
                if par and attrs.get("product") and par not in prod_by_parent:
                    prod_by_parent[par] = urllib.parse.unquote(attrs["product"])
                gid = attrs.get("ID") or f"{f[0]}:{f[3]}"
                mrna.append((f[0], int(f[3]), int(f[4]), gid, _desc(attrs)))

    if span:
        return [(seqid, s, e, gid, prod_by_parent.get(gid) or _desc(gattr[gid]))
                for gid, (seqid, s, e) in span.items()]
    return mrna


def gene_index(gene_list):
    idx = collections.defaultdict(list)
    for seqid, s, e, gid, desc in gene_list:
        idx[seqid].append((s, e, gid, desc))
    for seqid in idx:
        idx[seqid].sort()
    return idx


def overlapping_genes(idx, seqid, s, e):
    """[(gene_id, description)] annotated genes overlapping [s, e] on seqid."""
    hits = []
    for gs, ge, gid, desc in idx.get(seqid, []):
        if gs <= e and ge >= s:
            hits.append((gid, desc))
        if gs > e:
            break
    return hits


def flagged_contigs(tsv, want_classes):
    """{contig: n_genes} for rows whose class is in want_classes."""
    out = {}
    with open(tsv) as fh:
        header = fh.readline().rstrip("\n").split("\t")
        ci = {name: i for i, name in enumerate(header)}
        for line in fh:
            f = line.rstrip("\n").split("\t")
            if f[ci["class"]] in want_classes:
                out[f[ci["contig"]]] = int(f[ci["n_genes"]])
    return out


def analyse(label, proj, a):
    genome = find_file(*[os.path.join(proj, "genomes", f"{label}.{e}")
                         for e in ("fna", "fasta", "fa")])
    gff = find_file(*[os.path.join(proj, "gff_originals", f"{label}.{e}")
                      for e in ("gff", "gff3")])
    tsv = os.path.join(proj, "contig_redundancy", f"{label}.contigs.tsv")
    for name, p in (("genome FASTA", genome), ("GFF", gff), ("contigs.tsv", tsv)):
        if not p or not os.path.exists(p):
            sys.stderr.write(f"  ! {label}: {name} not found — skipping\n")
            return None

    want = {"small-redundant"}
    if a.also_unplaced:
        want.add("small-unplaced")
    targets = flagged_contigs(tsv, want)
    if a.contigs:
        targets = {c: targets.get(c, -1) for c in a.contigs}
    targets = {c: n for c, n in targets.items() if n != 0}   # skip 0-gene contigs
    if not targets:
        sys.stderr.write(f"  - {label}: no flagged contigs carrying genes\n")
        return None

    all_genes = read_gff_genes(gff)
    idx = gene_index(all_genes)
    genes_on_targets = [g for g in all_genes if g[0] in targets]
    if not genes_on_targets:
        sys.stderr.write(f"  - {label}: GFF has no gene features on {sorted(targets)}\n")
        return None

    out_dir = os.path.join(proj, "contig_redundancy")
    workdir = tempfile.mkdtemp(prefix=f"redcheck_{label}_")
    regions = os.path.join(workdir, "regions.txt")
    with open(regions, "w") as fh:
        for seqid, s, e, gid, desc in genes_on_targets:
            fh.write(f"{seqid}:{s}-{e}\n")
    raw = sh(["samtools", "faidx", "-r", regions, genome])

    # extracted gene spans, kept for manual inspection:
    #   >gene_id  contig:start-end  description
    q_fa = os.path.join(out_dir, f"{label}.redundant_genes.fa")
    with open(q_fa, "w") as out:
        i = -1
        for line in raw.splitlines():
            if line.startswith(">"):
                i += 1
                sid, gs, ge, gid, desc = genes_on_targets[i]
                out.write(f">{gid} {sid}:{gs}-{ge} {desc}".rstrip() + "\n")
            else:
                out.write(line + "\n")

    fields = "qseqid sseqid pident length qlen qstart qend sstart send evalue bitscore"
    blast = sh([
        "blastn", "-query", q_fa, "-subject", genome,
        "-evalue", "1e-20", "-perc_identity", str(int(a.min_id)),
        "-outfmt", f"6 {fields}",
    ])
    blast_tsv = os.path.join(out_dir, f"{label}.redundant_genes.blast.tsv")
    with open(blast_tsv, "w") as fh:
        fh.write("\t".join(fields.split()) + "\n")
        fh.write(blast)

    own_contig = {gid: seqid for seqid, s, e, gid, desc in genes_on_targets}
    # per (gene, subject_contig): merged subject intervals + id-weighted length
    hsp = collections.defaultdict(lambda: {"iv": [], "idlen": 0.0, "len": 0,
                                           "qlen": 0, "smin": 10**12, "smax": 0})
    for line in blast.splitlines():
        if not line.strip():
            continue
        q, s, pid, ln, qlen, qs, qe, ss, se = line.split("\t")[:9]
        if s == own_contig.get(q):
            continue
        d = hsp[(q, s)]
        d["iv"].append((int(qs), int(qe)))
        d["idlen"] += float(pid) * int(ln)
        d["len"] += int(ln)
        d["qlen"] = int(qlen)
        lo, hi = sorted((int(ss), int(se)))
        d["smin"] = min(d["smin"], lo)
        d["smax"] = max(d["smax"], hi)

    best = {}   # gene -> (contig, cov%, id%, s_lo, s_hi)
    for (q, s), d in hsp.items():
        if not d["qlen"]:
            continue
        cov = 100.0 * merged_len(d["iv"]) / d["qlen"]
        idp = d["idlen"] / d["len"] if d["len"] else 0.0
        score = cov * idp
        if q not in best or score > best[q][5]:
            best[q] = (s, cov, idp, d["smin"], d["smax"], score)

    rows = []
    per_contig = collections.defaultdict(lambda: {"n": 0, "dup": 0})
    for seqid, gs, ge, gid, desc in genes_on_targets:
        per_contig[seqid]["n"] += 1
        b = best.get(gid)
        if b:
            hc, cov, idp, slo, shi, _ = b
            ann = overlapping_genes(idx, hc, slo, shi)
            is_dup = cov >= a.min_cov and idp >= a.min_id and bool(ann)
        else:
            hc, cov, idp, ann, is_dup = "-", 0.0, 0.0, [], False
        if is_dup:
            per_contig[seqid]["dup"] += 1
        hit_gene = ";".join(g for g, _ in ann[:3]) if ann else "-"
        hit_desc = " | ".join(sorted({d for _, d in ann if d})[:3]) if ann else ""
        rows.append(dict(contig=seqid, gene=gid, desc=desc or "",
                         hit_contig=hc, cov=cov, ident=idp,
                         hit_gene=hit_gene, hit_desc=hit_desc,
                         verdict="duplicated" if is_dup else "CHECK"))

    subprocess.run(["rm", "-rf", workdir])
    return dict(label=label, rows=rows, per_contig=dict(per_contig), targets=targets)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project_dir")
    ap.add_argument("labels", nargs="*", help="genome labels (default: auto-detect)")
    ap.add_argument("--contigs", nargs="*", default=None,
                    help="restrict to these contig IDs (one genome only)")
    ap.add_argument("--also-unplaced", action="store_true",
                    help="also check small-unplaced contigs, not just small-redundant")
    ap.add_argument("--min-id", type=float, default=98.0, help="%% identity for 'duplicated'")
    ap.add_argument("--min-cov", type=float, default=90.0, help="%% gene length covered")
    a = ap.parse_args()

    proj = os.path.abspath(a.project_dir)
    labels = a.labels
    if not labels:
        cr = os.path.join(proj, "contig_redundancy")
        for fn in sorted(os.listdir(cr)):
            if not fn.endswith(".contigs.tsv"):
                continue
            lab = fn[:-len(".contigs.tsv")]
            flagged = flagged_contigs(os.path.join(cr, fn), {"small-redundant"})
            if any(n != 0 for n in flagged.values()):
                labels.append(lab)
    if not labels:
        sys.exit("no genomes with gene-carrying small-redundant contigs found")

    print(f"{'genome':<16} {'contig':<24} {'genes':>5} {'duplicated':>10}  verdict")
    print("-" * 72)
    for lab in labels:
        res = analyse(lab, proj, a)
        if not res:
            continue
        out = os.path.join(proj, "contig_redundancy", f"{lab}.redundant_genes.tsv")
        with open(out, "w") as fh:
            fh.write("contig\tgene\tdescription\tbest_off_contig_hit\tpct_gene_covered\t"
                     "pct_identity\thit_gene\thit_gene_description\tverdict\n")
            for r in res["rows"]:
                fh.write(f"{r['contig']}\t{r['gene']}\t{r['desc']}\t{r['hit_contig']}\t"
                         f"{r['cov']:.1f}\t{r['ident']:.1f}\t{r['hit_gene']}\t{r['hit_desc']}\t"
                         f"{r['verdict']}\n")
        for c, d in sorted(res["per_contig"].items()):
            verdict = "DROP-OK" if d["dup"] == d["n"] else f"REVIEW ({d['n']-d['dup']} unconfirmed)"
            print(f"{res['label']:<16} {c:<24} {d['n']:>5} {d['dup']:>10}  {verdict}")
            if d["dup"] != d["n"]:
                for r in res["rows"]:
                    if r["contig"] == c and r["verdict"] == "CHECK":
                        why = (f"best hit {r['hit_contig']} {r['cov']:.0f}% cov / {r['ident']:.0f}% id"
                               if r["hit_contig"] != "-" else "no off-contig hit")
                        print(f"    ? {r['gene']}  {r['desc'] or '(no description)'}  [{why}]")
        sys.stderr.write(f"[{lab}: wrote .redundant_genes.tsv / .fa / .blast.tsv]\n")


if __name__ == "__main__":
    main()
