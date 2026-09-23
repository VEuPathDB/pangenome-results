#!/usr/bin/env python3
"""
Post-process every strain's <genome>_final_annotation.gff (this pipeline's output) with two
filters: dropping unsupported extra-copy genes, then resolving overlapping-gene pairs. Unlike
the rest of this pipeline's per-genome scripts, this one reads ALL genomes in --strains in one
run, because one of the overlap rules below (case 6) needs to know each gene's status
panel-wide, not just within its own genome.

1) Extra-copy genes (extra_copy_number > 0) are kept only if they have a valid ORF - dropped
   otherwise. No contig-size or domain check - a genuine extra copy (real tandem duplication,
   real gene family expansion, see the general README's own notes on this) can legitimately
   sit on a short contig or lack a domain hit on its own, so those aren't used as filters here
   any more; a broken ORF is the one thing that's unambiguous evidence of a bad transfer.

2) Every rescued_<strain> gene below --min-rescued-coverage (default 0.5) Liftoff coverage is
   dropped outright, whatever else is true about it. rescued_<strain> is this pipeline's
   lowest-confidence tier (round 2 of the build step - a strain's *entire* transfer, unfiltered,
   added only as a last resort) - it never had to clear a coverage/identity bar to get into the
   final annotation in the first place, unlike good_<strain>, so this is the one basic quality
   floor that tier gets.

3) Overlapping gene pairs (from a fresh CDS-to-CDS overlap scan of the genes that survived
   steps 1-2 - the same logic as check_overlapping_genes.py/plot_final_annotation_qc.py).
   Overlaps under --min-overlap-bp (default 20bp) are ignored entirely - boundary-rounding
   noise, not a real overlap (most of these are 1-2bp touches from Liftoff's coordinate
   polishing, checked against this project's own real data). Of what's left:
   - "minor" overlap (< 20% of the smaller gene's own CDS) **and** "flank" (only touches the
     bigger gene's outermost CDS segment, not an internal one): both genes kept, no action -
     the two gene models most likely just disagree at the boundary, both genes are probably
     real. A minor overlap that's "inside" (touches an internal CDS segment - i.e. the smaller
     gene mostly sits in what's actually an intron) or "single_exon" (bigger gene has only one
     CDS segment, flank/inside doesn't apply) does NOT get this automatic pass - it's still
     more likely a spurious call, so it falls through to the same resolution as a
     substantial/contained overlap below.
   - "substantial" or "contained" (>= 20%, sized against whichever gene is smaller - sizing
     against the bigger gene alone can make a real problem look tiny) **or** minor-but-not-flank
     from above:
       1) both sides are the reference-derived "main" gene: keep both (a real overlap
          transferred straight from the reference's own annotation - not this pipeline's
          call to resolve).
       2) exactly one side is "main": keep it; drop the other side UNLESS it also has a
          protein domain, in which case both are kept (uncertain - left for a human to
          look at, not auto-resolved).
       3) neither side is "main", exactly one has a domain -> keep that one, drop the other.
       4) neither side is "main", both have a domain -> keep both, uncertain, left for
          manual review.
       5) neither side is "main", neither has a domain -> no trusted anchor and no domain
          evidence on either side, so this falls back to how well-supported each gene is
          across the WHOLE panel, not just this one genome:
            - a gene present in only 1 genome of the whole --strains panel is dropped
              outright - a single occurrence with no domain and no reference backing is
              the weakest possible support (checked against this project's real data:
              this is also exactly the profile of most genuine strain-private gene calls,
              so this is a soft call, not a certainty - see the general README's overlap
              rule notes).
            - between two genes both present in >1 genome, keep whichever has more
              good_<strain>-sourced occurrences across the whole panel (high-confidence
              Liftoff transfers are stronger support than raw presence count, which also
              includes low-confidence rescued_<strain> copies); on a tie, keep the one
              with the longer CDS.

Protein domain = the gene has an InterPro or Pfam hit in its own Dbxref attribute (the
CDS-level Dbxref=InterPro:...,PFAM:... that NCBI-style annotations carry, which Liftoff
carries through on any gene transferred from a genome that had it - no external lookup
file needed, so this works for any species' annotation that uses this convention, not
just this project's specific strains).

Every removed gene is logged with why, in each genome's own --out-dir/<genome>_filter_report.tsv
- nothing is silently dropped.

4) Every kept protein-coding gene/pseudogene is relabeled to feature type "gene" (whatever
   it was called before), and its "pseudogenic_transcript" child (if any) to "transcript" -
   the one thing get_pangenes' own parser actually requires (it only clusters features
   literally typed "gene", see the general README's get_pangenes step). Non-coding RNA
   genes are left exactly as they are, feature type and source both - they were already
   retyped away from "gene" back in step 3 (prepare_for_liftoff.py), specifically so they'd
   never be mistaken for a protein-coding candidate here or by get_pangenes later; nothing
   left to do for them at this point.

5) Every kept gene's ID is renumbered to "<id-prefix><strain-index>g<00001, 00002, ...>"
   (default prefix "Afu", strain-index = the genome's 1-based position in --strains, same
   style as this pipeline's reference genome's own native gene IDs, just repurposing the
   number after the prefix as a strain index instead of a chromosome number). The original
   ID is kept in a new "original_ID=" attribute (not folded into description=, so it stays
   its own machine-readable field, consistent with this GFF's other pipeline-added
   attributes like copy_num_ID=/coverage=).

Known limitation - "protein domain" is only as good as the source annotation: see
analyze_final_annotation.py / plot_final_annotation_qc.py's own notes on this - a genome
whose ORIGINAL annotation never recorded InterPro/PFAM hits at all will have every gene
sourced from it test has_domain=False unconditionally, not because those genes lack real
domains, but because this annotation source never recorded them.

Usage:
    python3 filter_final_annotation.py \\
        --strains genome_order.txt \\
        --final-dir expanded_annotation \\
        --out-dir filtered_annotation
"""

import argparse
import os
import re
import sys
from collections import defaultdict

ID_RE = re.compile(r"ID=([^;]+)")
PARENT_RE = re.compile(r"Parent=([^;]+)")
# Feature types that only ever appear nested under a level-1 gene feature, never as an
# independent top-level entity - used to recognize "a new gene-level block just started"
# in the output-writing pass below, without having to enumerate every naming convention
# an annotation might use for its non-protein-coding gene types (NCBI's "gene", FungiDB's
# "ncRNA_gene", etc.) - anything not in this set is treated as a new top-level block.
CHILD_FEATURE_TYPES = {
    "mRNA", "CDS", "exon", "five_prime_UTR", "three_prime_UTR",
    "ncRNA", "tRNA", "rRNA", "snRNA", "snoRNA", "pseudogenic_transcript",
}


def read_strains(value):
    if os.path.isfile(value):
        with open(value) as fh:
            return [l.strip() for l in fh if l.strip() and not l.startswith("#")]
    return [s.strip() for s in value.split(",") if s.strip()]


def parse_gff(path):
    """Gene-level records, mRNA->gene links, and per-mRNA CDS segments/domain flags."""
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
                "start": int(start), "end": int(end), "strand": strand,
                "extra_copy_number": _int_attr(attrs, "extra_copy_number"),
                "valid_ORF": _valid_orf(attrs),
                "coverage": _float_attr(attrs, "coverage"),
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
        # sorted left-to-right by genomic position - needed by classify_minor_position below,
        # which walks segments outermost-to-innermost.
        gene["cds_segments"] = sorted(cds_by_mrna.get(best_mrna, []))
        gene["cds_bp"] = best_bp if best_bp > 0 else 0
        gene["has_domain"] = any(mrna_has_domain.get(m, False) for m in gene_mrnas)

    return genes


def parse_gene_sources_only(path):
    """Lightweight pass for the panel-wide stats: just gene_id -> source, no CDS/domain
    parsing - used across all --strains genomes before the real per-genome processing."""
    sources = {}
    with open(path) as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            fields = line.rstrip("\n").split("\t")
            if len(fields) < 9 or fields[2] != "protein_coding_gene":
                continue
            m = ID_RE.search(fields[8])
            if m:
                sources[m.group(1)] = fields[1]
    return sources


def _int_attr(attrs, key):
    m = re.search(rf"{key}=(\d+)", attrs)
    return int(m.group(1)) if m else None


def _float_attr(attrs, key):
    m = re.search(rf"{key}=([\d.]+)", attrs)
    return float(m.group(1)) if m else None


def _valid_orf(attrs):
    if "valid_ORF=True" in attrs:
        return True
    if "valid_ORF=False" in attrs:
        return False
    m = re.search(r"valid_ORFs=(\d+)", attrs)
    if m:
        return int(m.group(1)) >= 1
    return None


def segments_overlap_bp(segs1, segs2):
    total = 0
    for s1, e1 in segs1:
        for s2, e2 in segs2:
            lo, hi = max(s1, s2), min(e1, e2)
            if hi >= lo:
                total += hi - lo + 1
    return total


def find_cds_overlaps(genes, min_overlap_bp):
    """Sweep-line scan for CDS-to-CDS overlapping gene pairs. Pairs whose overlap is under
    min_overlap_bp are dropped here already - not a real overlap, see module docstring."""
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


def classify_minor_position(bigger_gene, smaller_cds_segments):
    """Where a minor overlap sits on the bigger gene's CDS: "flank" (only touches its first or
    last CDS segment - the two gene models plausibly disagree only at the boundary, both genes
    likely real), "inside" (touches an internal segment - more likely the smaller gene is a
    spurious call sitting in what's actually an intron), or "single_exon" (bigger gene has only
    one CDS segment total, flank/inside doesn't apply). Same logic as
    plot_final_annotation_qc.py's version of this check."""
    segs = bigger_gene["cds_segments"]
    if len(segs) <= 1:
        return "single_exon"
    outer = {segs[0], segs[-1]}
    overlapped = {s for s in segs for ss, se in smaller_cds_segments
                  if max(s[0], ss) <= min(s[1], se)}
    if not overlapped:
        return "inside"  # shouldn't happen (ov_bp>0 implies some segment matched) - fall through safely
    return "flank" if overlapped <= outer else "inside"


def assign_new_ids(genes, kept_ids, strain_index, id_prefix):
    ordered = sorted(kept_ids, key=lambda gid: (genes[gid]["seqname"], genes[gid]["start"]))
    width = max(5, len(str(len(ordered))))
    return {gid: f"{id_prefix}{strain_index}g{i:0{width}d}" for i, gid in enumerate(ordered, start=1)}


def add_original_id_attr(attrs, old_id):
    return attrs.rstrip(";") + f";original_ID={old_id}"


def resolve_overlaps(genes, overlap_pairs, ref_tag, present_in, n_good_transfers):
    """Returns {gene_id: reason} for every gene this genome's overlap pairs decide to drop."""
    removed = {}
    for gene1_id, gene2_id, ov_bp in overlap_pairs:
        if gene1_id in removed or gene2_id in removed:
            continue  # already resolved by an earlier overlap in this genome
        g1, g2 = genes[gene1_id], genes[gene2_id]
        smaller_bp = min(g1["cds_bp"], g2["cds_bp"])
        if smaller_bp == 0:
            continue
        pct_of_smaller = ov_bp / smaller_bp
        if pct_of_smaller < 0.2:
            # minor overlap - only auto-kept if it's also "flank" (only touches the bigger
            # gene's outermost CDS segment): the two gene models likely just disagree at the
            # boundary, both genes are probably real. "inside" (touches an internal segment,
            # i.e. sits in what's actually an intron) or "single_exon" falls through to the
            # same case-based resolution as a substantial/contained overlap instead - a minor
            # overlap buried inside the bigger gene is still more likely a spurious call.
            bigger, smaller = (g1, g2) if g1["cds_bp"] >= g2["cds_bp"] else (g2, g1)
            if classify_minor_position(bigger, smaller["cds_segments"]) == "flank":
                continue  # minor + flank - keep both

        g1_is_ref, g2_is_ref = g1["source"] == ref_tag, g2["source"] == ref_tag

        if g1_is_ref and g2_is_ref:
            continue  # case 1: both reference-derived - not this pipeline's call, keep both

        if g1_is_ref or g2_is_ref:
            ref_gene, other_gene = (g1, g2) if g1_is_ref else (g2, g1)
            if other_gene["has_domain"]:
                continue  # case 2: uncertain - keep both, leave for manual review
            removed[other_gene["id"]] = (
                f"overlaps the reference ('{ref_tag}') gene {ref_gene['id']} "
                f"({round(100*pct_of_smaller,1)}% of its own CDS), no protein domain"
            )
            continue

        g1_domain, g2_domain = g1["has_domain"], g2["has_domain"]
        if g1_domain != g2_domain:
            # case 3/4: exactly one side has a domain - keep it, drop the other
            winner, loser = (g1, g2) if g1_domain else (g2, g1)
            removed[loser["id"]] = f"overlaps {winner['id']} ({round(100*pct_of_smaller,1)}% of its own CDS); {winner['id']} has a protein domain, this one doesn't"
            continue
        if g1_domain and g2_domain:
            continue  # case 5: both have evidence - uncertain, keep both, leave for manual review

        # case 6: neither is reference, neither has a domain - fall back to panel-wide support.
        g1_n_present = len(present_in.get(g1["id"], ()))
        g2_n_present = len(present_in.get(g2["id"], ()))
        if g1_n_present <= 1 and g2_n_present <= 1:
            removed[g1["id"]] = f"overlaps {g2['id']} ({round(100*pct_of_smaller,1)}% of its own CDS); neither has a protein domain, and both are present in only 1 genome panel-wide"
            removed[g2["id"]] = f"overlaps {g1['id']} ({round(100*pct_of_smaller,1)}% of its own CDS); neither has a protein domain, and both are present in only 1 genome panel-wide"
            continue
        if g1_n_present <= 1:
            removed[g1["id"]] = f"overlaps {g2['id']} ({round(100*pct_of_smaller,1)}% of its own CDS); no protein domain, and present in only 1 genome panel-wide"
            continue
        if g2_n_present <= 1:
            removed[g2["id"]] = f"overlaps {g1['id']} ({round(100*pct_of_smaller,1)}% of its own CDS); no protein domain, and present in only 1 genome panel-wide"
            continue
        # both present in >1 genome panel-wide - keep whichever has more good_<strain>
        # transfers panel-wide, tie broken by CDS length.
        gt1, gt2 = n_good_transfers.get(g1["id"], 0), n_good_transfers.get(g2["id"], 0)
        if gt1 != gt2:
            winner, loser, metric = (g1, g2, f"{gt1} vs {gt2}") if gt1 > gt2 else (g2, g1, f"{gt2} vs {gt1}")
        else:
            winner, loser = (g1, g2) if g1["cds_bp"] >= g2["cds_bp"] else (g2, g1)
            metric = f"tied on good_<strain> transfers panel-wide ({gt1}), kept the longer CDS"
        removed[loser["id"]] = f"overlaps {winner['id']} ({round(100*pct_of_smaller,1)}% of its own CDS); neither has a protein domain, both present in >1 genome, {winner['id']} more panel-wide supported ({metric})"
    return removed


def write_filtered_gff(gff_path, out_path, genes, kept_ids, id_mapping):
    with open(gff_path) as fh:
        header_lines = [l for l in fh if l.startswith("#")]

    with open(out_path, "w") as out_fh:
        out_fh.writelines(header_lines)
        with open(gff_path) as fh:
            current_gene_kept = False
            current_gene_id = None
            for line in fh:
                if line.startswith("#") or not line.strip():
                    continue
                fields = line.rstrip("\n").split("\t")
                if len(fields) < 9:
                    continue
                feature, attrs = fields[2], fields[8]
                if feature == "protein_coding_gene":
                    m = ID_RE.search(attrs)
                    gene_id = m.group(1) if m else None
                    current_gene_id = gene_id
                    current_gene_kept = gene_id in kept_ids
                    if current_gene_kept:
                        new_id = id_mapping[gene_id]
                        attrs = add_original_id_attr(attrs, gene_id)
                        attrs = attrs.replace(f"ID={gene_id}", f"ID={new_id}", 1)
                        fields[2] = "gene"  # get_pangenes only clusters feature type "gene"
                        fields[8] = attrs
                        out_fh.write("\t".join(fields) + "\n")
                    continue
                if feature not in CHILD_FEATURE_TYPES:
                    current_gene_kept = True
                    current_gene_id = None
                    out_fh.write(line)
                    continue
                if current_gene_kept:
                    if feature == "pseudogenic_transcript":
                        fields[2] = "transcript"  # get_pangenes' expected child type
                    if current_gene_id in id_mapping and feature in ("mRNA", "pseudogenic_transcript"):
                        attrs = attrs.replace(f"Parent={current_gene_id}", f"Parent={id_mapping[current_gene_id]}", 1)
                    fields[8] = attrs
                    out_fh.write("\t".join(fields) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--strains", required=True, help="Comma-separated genome names or a file with one per line - first one must be the reference, same as the rest of this pipeline's ORDER")
    parser.add_argument("--final-dir", required=True, help="Directory with <strain>_final_annotation.gff (this pipeline's raw output, before filtering)")
    parser.add_argument("--out-dir", default="./filtered_annotation", help="Where to write the filtered GFFs + reports")
    parser.add_argument("--min-overlap-bp", type=int, default=20,
                         help="CDS-to-CDS overlaps under this many bp are ignored entirely - boundary-rounding noise, not treated as a real overlap (default: 20)")
    parser.add_argument("--reference-source-tag", default="main",
                         help="The source tag marking the reference-derived tier in this pipeline's output (default: 'main')")
    parser.add_argument("--min-rescued-coverage", type=float, default=0.5,
                         help="Every rescued_<genome> gene (this pipeline's lowest-confidence Liftoff tier - it never had to pass a coverage/identity bar to get in) below this Liftoff coverage is dropped outright, regardless of ORF/domain/overlap status (default: 0.5)")
    parser.add_argument("--id-prefix", default="Afu", help="Prefix for renamed gene IDs (default: 'Afu', this project's own convention - change for other species)")
    args = parser.parse_args()

    strains = read_strains(args.strains)
    os.makedirs(args.out_dir, exist_ok=True)

    # --- Phase 0: panel-wide stats (needed for case 6, computed across ALL strains up front) ---
    present_in = defaultdict(set)
    n_good_transfers = defaultdict(int)
    for s in strains:
        sources = parse_gene_sources_only(os.path.join(args.final_dir, f"{s}_final_annotation.gff"))
        for gene_id, source in sources.items():
            present_in[gene_id].add(s)
            if source.startswith("good_"):
                n_good_transfers[gene_id] += 1
    print(f"Panel-wide stats built from {len(strains)} genomes: {len(present_in)} distinct gene IDs", file=sys.stderr)

    # --- Phase 1: per genome, filter + write ---
    summary_rows = []
    for i, s in enumerate(strains, start=1):
        gff_path = os.path.join(args.final_dir, f"{s}_final_annotation.gff")
        out_path = os.path.join(args.out_dir, f"{s}_final_annotation_filtered.gff")
        report_path = os.path.join(args.out_dir, f"{s}_filter_report.tsv")

        print(f"=== Genome {i}/{len(strains)}: {s} ===", file=sys.stderr)
        genes = parse_gff(gff_path)

        removed = {}
        for gene_id, gene in genes.items():
            if not gene["extra_copy_number"] or gene["extra_copy_number"] == 0:
                continue
            if not gene["valid_ORF"]:
                removed[gene_id] = "extra copy with no valid ORF"

        for gene_id, gene in genes.items():
            if gene_id in removed or not gene["source"].startswith("rescued_"):
                continue
            if gene["coverage"] is not None and gene["coverage"] < args.min_rescued_coverage:
                removed[gene_id] = f"rescued transfer, Liftoff coverage {gene['coverage']:.2f} < {args.min_rescued_coverage}"

        surviving = {gid: g for gid, g in genes.items() if gid not in removed}
        overlap_pairs = find_cds_overlaps(surviving, args.min_overlap_bp)
        removed.update(resolve_overlaps(surviving, overlap_pairs, args.reference_source_tag, present_in, n_good_transfers))

        kept_ids = set(genes) - set(removed)
        id_mapping = assign_new_ids(genes, kept_ids, i, args.id_prefix)
        write_filtered_gff(gff_path, out_path, genes, kept_ids, id_mapping)

        with open(report_path, "w") as rep_fh:
            rep_fh.write("gene_id\tsource\tseqname\treason\n")
            for gene_id, reason in removed.items():
                g = genes[gene_id]
                rep_fh.write(f"{gene_id}\t{g['source']}\t{g['seqname']}\t{reason}\n")

        n_total = len(genes)
        n_removed = len(removed)
        print(f"  {n_total} protein-coding genes -> {n_total - n_removed} kept, "
              f"{n_removed} removed ({round(100*n_removed/n_total,1)}%) -> {out_path}", file=sys.stderr)
        summary_rows.append((s, n_total, n_total - n_removed, n_removed))

    with open(os.path.join(args.out_dir, "filter_summary.tsv"), "w") as fh:
        fh.write("strain\tn_original\tn_kept\tn_removed\n")
        for s, n_total, n_kept, n_removed in summary_rows:
            fh.write(f"{s}\t{n_total}\t{n_kept}\t{n_removed}\n")

    print(f"All genomes filtered. Outputs are in {args.out_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()
