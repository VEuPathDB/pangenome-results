#!/usr/bin/env python3
"""
Alternative to filter_final_annotation.py: instead of dropping any gene, tag every gene in
every strain's <genome>_final_annotation.gff with what its CDS overlaps, and pass everything
through unfiltered to the get_pangenes prep step. The idea: some overlaps are local artifacts
of one genome's Liftoff transfer (see the general README's overlap-rule notes) - deleting a
gene before get_pangenes has run risks a false gene-absence call for a real, panel-wide gene
that only misbehaves in one genome. Tagging instead defers that judgment to after get_pangenes,
where the pangene's real presence/absence pattern across the whole panel is known and is much
stronger evidence than anything computable from a single genome's GFF alone.

Adds one new attribute to every protein-coding gene line (not its children):
    intersect=NA                        no CDS-to-CDS overlap >= --min-overlap-bp with anything
    intersect=with_main                 overlaps the reference-derived "main" gene
    intersect=with_other_with_domain    overlaps a non-main gene that itself has a protein domain
    intersect=with_other_no_domain      overlaps a non-main gene with no protein domain either

If a gene overlaps more than one other gene (rare, but possible), the tag is the single most
informative of the above - priority with_main > with_other_with_domain > with_other_no_domain -
not a list of every partner (that detail is still in --out-dir/<genome>_intersect_pairs.tsv,
one row per overlapping pair, for anyone who wants to look closer).

Protein domain = the gene has an InterPro or Pfam hit in its own Dbxref attribute - same
detection as filter_final_annotation.py, see that script's docstring for the caveat on
genomes whose original annotation never recorded this field.

This script never removes a gene. It does, however, do the same two get_pangenes-readiness
things filter_final_annotation.py does, so either script's output is ready to hand straight to
get_pangenes without an extra prep pass:

- every protein-coding gene is relabeled to feature type "gene" (get_pangenes only clusters
  features literally typed that), and its "pseudogenic_transcript" child (if any) to
  "transcript" - non-coding RNA genes are left exactly as they are, feature type and source
  both, since they were already retyped away from "gene" back in step 3
  (prepare_for_liftoff.py) specifically so get_pangenes would never see them as candidates;
- every gene's ID is renumbered to "<id-prefix><strain-index>g<00001, 00002, ...>", same
  scheme and same reason as filter_final_annotation.py (the same source gene ID can otherwise
  appear unchanged in several genomes' GFFs, since this pipeline's Liftoff transfers preserve
  it - get_pangenes needs every ID unique across the whole panel). The original ID is kept in
  a new "original_ID=" attribute.

Usage:
    python3 tag_final_annotation.py \\
        --strains genome_order.txt \\
        --final-dir expanded_annotation \\
        --out-dir tagged_annotation
"""

import argparse
import os
import re
import sys
from collections import defaultdict

ID_RE = re.compile(r"ID=([^;]+)")
PARENT_RE = re.compile(r"Parent=([^;]+)")

TAG_PRIORITY = {"with_main": 3, "with_other_with_domain": 2, "with_other_no_domain": 1}

# Same set filter_final_annotation.py uses to recognize "a new gene-level block just started".
CHILD_FEATURE_TYPES = {
    "mRNA", "pseudogenic_transcript", "CDS", "exon", "five_prime_UTR", "three_prime_UTR",
    "ncRNA", "tRNA", "rRNA", "snRNA", "snoRNA",
}


def read_strains(value):
    if os.path.isfile(value):
        with open(value) as fh:
            return [l.strip() for l in fh if l.strip() and not l.startswith("#")]
    return [s.strip() for s in value.split(",") if s.strip()]


def parse_gff(path):
    genes = {}
    mrna_to_gene = {}
    cds_by_mrna = defaultdict(list)
    mrna_has_domain = defaultdict(bool)

    with open(path) as fh:
        raw_lines = fh.readlines()

    for line in raw_lines:
        if line.startswith("#") or not line.strip():
            continue
        fields = line.rstrip("\n").split("\t")
        if len(fields) < 9:
            continue
        seqname, source, feature, start, end, score, strand = fields[:7]
        attrs = fields[8]
        m = ID_RE.search(attrs)
        feat_id = m.group(1) if m else None

        if feature == "protein_coding_gene" and feat_id:
            genes[feat_id] = {
                "id": feat_id, "seqname": seqname, "source": source,
                "start": int(start), "end": int(end),
            }
        elif feature == "mRNA" and feat_id:
            parent = PARENT_RE.search(attrs)
            if parent:
                mrna_to_gene[feat_id] = parent.group(1)

    for line in raw_lines:
        if line.startswith("#") or not line.strip():
            continue
        fields = line.rstrip("\n").split("\t")
        if len(fields) < 9:
            continue
        feature, start, end, attrs = fields[2], fields[3], fields[4], fields[8]
        if feature != "CDS":
            continue
        parent = PARENT_RE.search(attrs)
        if not parent:
            continue
        mrna_id = parent.group(1)
        if mrna_to_gene.get(mrna_id) not in genes:
            continue
        cds_by_mrna[mrna_id].append((int(start), int(end)))
        if "InterPro:" in attrs or "PFAM:" in attrs or "Pfam:" in attrs:
            mrna_has_domain[mrna_id] = True

    for gene_id, gene in genes.items():
        gene_mrnas = [m for m, g in mrna_to_gene.items() if g == gene_id]
        best_mrna, best_bp = None, -1
        for mrna_id in gene_mrnas:
            segs = cds_by_mrna.get(mrna_id, [])
            bp = sum(e - s + 1 for s, e in segs)
            if bp > best_bp:
                best_bp, best_mrna = bp, mrna_id
        gene["cds_segments"] = cds_by_mrna.get(best_mrna, [])
        gene["has_domain"] = any(mrna_has_domain.get(m, False) for m in gene_mrnas)

    return genes


def segments_overlap_bp(segs1, segs2):
    total = 0
    for s1, e1 in segs1:
        for s2, e2 in segs2:
            lo, hi = max(s1, s2), min(e1, e2)
            if hi >= lo:
                total += hi - lo + 1
    return total


def find_cds_overlaps(genes, min_overlap_bp):
    by_seq = defaultdict(list)
    for gene in genes.values():
        by_seq[gene["seqname"]].append(gene)

    pairs = []
    for seqname, seq_genes in by_seq.items():
        seq_genes.sort(key=lambda g: g["start"])
        active = []
        for gene in seq_genes:
            active = [a for a in active if a["end"] >= gene["start"]]
            for other in active:
                ov_bp = segments_overlap_bp(other["cds_segments"], gene["cds_segments"])
                if ov_bp >= min_overlap_bp:
                    pairs.append((other["id"], gene["id"], ov_bp))
            active.append(gene)
    return pairs


def compute_tags(genes, overlap_pairs, ref_tag):
    """gene_id -> (tag, [(partner_id, overlap_bp), ...]) for every gene involved in >=1 pair."""
    best_tag = {}
    partners = defaultdict(list)

    def update(gid, tag, partner_id, ov_bp):
        partners[gid].append((partner_id, ov_bp))
        cur = best_tag.get(gid)
        if cur is None or TAG_PRIORITY[tag] > TAG_PRIORITY[cur]:
            best_tag[gid] = tag

    for g1_id, g2_id, ov_bp in overlap_pairs:
        g1, g2 = genes[g1_id], genes[g2_id]
        for gid, own, partner in [(g1_id, g1, g2), (g2_id, g2, g1)]:
            if partner["source"] == ref_tag:
                tag = "with_main"
            elif partner["has_domain"]:
                tag = "with_other_with_domain"
            else:
                tag = "with_other_no_domain"
            update(gid, tag, partner["id"], ov_bp)

    return best_tag, partners


def assign_new_ids(genes, strain_index, id_prefix):
    ordered = sorted(genes, key=lambda gid: (genes[gid]["seqname"], genes[gid]["start"]))
    width = max(5, len(str(len(ordered))))
    return {gid: f"{id_prefix}{strain_index}g{i:0{width}d}" for i, gid in enumerate(ordered, start=1)}


def add_original_id_attr(attrs, old_id):
    return attrs.rstrip(";") + f";original_ID={old_id}"


def write_tagged_gff(gff_path, out_path, best_tag, id_mapping):
    with open(gff_path) as in_fh, open(out_path, "w") as out_fh:
        current_gene_id = None
        current_is_gene_block = False
        for line in in_fh:
            if line.startswith("#") or not line.strip():
                out_fh.write(line)
                continue
            fields = line.rstrip("\n").split("\t")
            if len(fields) < 9:
                out_fh.write(line)
                continue
            feature, attrs = fields[2], fields[8]

            if feature == "protein_coding_gene":
                m = ID_RE.search(attrs)
                gene_id = m.group(1) if m else None
                current_gene_id = gene_id
                current_is_gene_block = True
                new_id = id_mapping[gene_id]
                tag = best_tag.get(gene_id, "NA")
                attrs = add_original_id_attr(attrs, gene_id)
                attrs = attrs.replace(f"ID={gene_id}", f"ID={new_id}", 1)
                attrs = attrs.rstrip(";") + f";intersect={tag}"
                fields[2] = "gene"  # get_pangenes only clusters feature type "gene"
                fields[8] = attrs
                out_fh.write("\t".join(fields) + "\n")
                continue

            if feature not in CHILD_FEATURE_TYPES:
                current_is_gene_block = False
                current_gene_id = None
                out_fh.write(line)
                continue

            if current_is_gene_block:
                if feature == "pseudogenic_transcript":
                    fields[2] = "transcript"  # get_pangenes' expected child type
                if current_gene_id in id_mapping and feature in ("mRNA", "pseudogenic_transcript"):
                    attrs = attrs.replace(f"Parent={current_gene_id}", f"Parent={id_mapping[current_gene_id]}", 1)
                fields[8] = attrs
            out_fh.write("\t".join(fields) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--strains", required=True, help="Comma-separated genome names or a file with one per line - first one must be the reference, same as the rest of this pipeline's ORDER")
    parser.add_argument("--final-dir", required=True, help="Directory with <strain>_final_annotation.gff (this pipeline's raw output)")
    parser.add_argument("--out-dir", default="./tagged_annotation", help="Where to write the tagged GFFs + intersect-pair reports")
    parser.add_argument("--min-overlap-bp", type=int, default=20,
                         help="CDS-to-CDS overlaps under this many bp are ignored entirely - boundary-rounding noise, not treated as a real overlap (default: 20)")
    parser.add_argument("--reference-source-tag", default="main",
                         help="The source tag marking the reference-derived tier in this pipeline's output (default: 'main')")
    parser.add_argument("--id-prefix", default="Afu", help="Prefix for renamed gene IDs (default: 'Afu', this project's own convention - change for other species)")
    args = parser.parse_args()

    strains = read_strains(args.strains)
    os.makedirs(args.out_dir, exist_ok=True)

    summary_rows = []
    for i, s in enumerate(strains, start=1):
        gff_path = os.path.join(args.final_dir, f"{s}_final_annotation.gff")
        out_path = os.path.join(args.out_dir, f"{s}_final_annotation_tagged.gff")
        pairs_report_path = os.path.join(args.out_dir, f"{s}_intersect_pairs.tsv")

        print(f"=== Genome {i}/{len(strains)}: {s} ===", file=sys.stderr)
        genes = parse_gff(gff_path)
        overlap_pairs = find_cds_overlaps(genes, args.min_overlap_bp)
        best_tag, partners = compute_tags(genes, overlap_pairs, args.reference_source_tag)
        id_mapping = assign_new_ids(genes, i, args.id_prefix)
        write_tagged_gff(gff_path, out_path, best_tag, id_mapping)

        with open(pairs_report_path, "w") as fh:
            fh.write("gene_id\tintersect\tpartner_id\toverlap_bp\n")
            for gid, tag in best_tag.items():
                for partner_id, ov_bp in partners[gid]:
                    fh.write(f"{gid}\t{tag}\t{partner_id}\t{ov_bp}\n")

        n_total = len(genes)
        tag_counts = defaultdict(int)
        for gid in genes:
            tag_counts[best_tag.get(gid, "NA")] += 1
        print(f"  {n_total} protein-coding genes -> "
              f"NA={tag_counts['NA']}, with_main={tag_counts['with_main']}, "
              f"with_other_with_domain={tag_counts['with_other_with_domain']}, "
              f"with_other_no_domain={tag_counts['with_other_no_domain']} -> {out_path}", file=sys.stderr)
        summary_rows.append((s, n_total, tag_counts["NA"], tag_counts["with_main"],
                              tag_counts["with_other_with_domain"], tag_counts["with_other_no_domain"]))

    with open(os.path.join(args.out_dir, "tag_summary.tsv"), "w") as fh:
        fh.write("strain\tn_total\tn_NA\tn_with_main\tn_with_other_with_domain\tn_with_other_no_domain\n")
        for row in summary_rows:
            fh.write("\t".join(str(x) for x in row) + "\n")

    print(f"All genomes tagged (nothing removed). Outputs are in {args.out_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()
