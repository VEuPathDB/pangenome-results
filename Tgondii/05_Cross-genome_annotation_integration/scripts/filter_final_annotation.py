#!/usr/bin/env python3
"""
Post-process every strain's <genome>_final_annotation.gff (this pipeline's output) with three
filters: resolving overlapping-gene pairs, then dropping unsupported extra-copy genes, then the
rescued-coverage floor. Reads ALL genomes in --strains in one run and decides ONE global verdict
per gene (by its original ID, shared across every genome that carries it) - a gene dropped
anywhere in the panel is dropped from every genome's output, even where its own local copy never
overlapped anything. A gene is never partially removed: all-or-nothing across the whole panel.

Execution order matters:

0) Panel-wide stats, from every genome's RAW genes (before any filtering): how many genomes
   carry each gene (`present_in`), how many of those are good_<genome> transfers, and - from a
   first CDS-overlap scan of every genome - how many genomes each gene has a *qualifying*
   overlap in (`collides_in`; a "minor + flank" overlap, auto-kept below, does not count).

1) Overlap resolution, decided globally per gene, using every genome's full raw gene set
   (including genes that would later fail the extra-copy/rescue-coverage checks in step 2 - an
   overlap dispute is settled before those checks ever run).

   A minor overlap (< 20% of the smaller gene's own CDS) that sits on the bigger gene's
   outermost CDS segment ("flank") is left alone: the two gene models most likely just disagree
   at the boundary, and both genes are probably real. Keep both, done.

   Everything else - minor-but-not-flank, or "substantial"/"contained" (>= 20%, sized against
   whichever gene is smaller) - needs a decision. A gene "has evidence" if it has a protein
   domain (InterPro/PFAM Dbxref hit) or a specific description (anything other than
   "hypothetical protein", "unspecified product", or empty - see GENERIC_DESCRIPTIONS below;
   --require-domain-only turns off the description half, domain-only, like this script used to
   work).

   Whichever gene has more evidence wins:
     - one gene is main, the other has no evidence -> main wins, the other is a drop candidate,
       run through the panel check below.
     - one gene is main, the other also has evidence -> keep both.
     - neither is main, only one has evidence -> that one wins, the other is a drop candidate,
       run through the panel check below.
     - neither is main, both have evidence -> keep both.
     - neither is main, neither has evidence -> no local evidence to decide by at all; no panel
       check here either - the two genes are compared directly by panel-wide good_<genome>
       transfer count instead (more wins, tied -> the longer CDS wins). This also naturally
       covers a panel-private gene: with nowhere to have transferred well into, it has 0
       good_<genome> transfers and loses to any better-supported opponent on its own.

   The panel check (cases above where one gene lost to main or to an evidence-haver) - using
   the panel-wide stats from step 0:
     - present in <= 2 genomes -> dropped (too little support to weigh against anything else).
     - present in > 2 genomes but with a qualifying overlap in only 1 of them -> NOT dropped -
       more likely a Liftoff boundary glitch specific to that one genome than real evidence the
       gene is spurious.
     - present in > 2 genomes with a qualifying overlap in >= --min-overlap-genomes (default 2)
       of them -> dropped, a real recurring conflict.

2) Extra-copy genes (extra_copy_number > 0), among whatever survived step 1, are kept only if
   they have a valid ORF - dropped otherwise (--extra-copy-require-valid-orf, on by default). No
   contig-size or domain check: a genuine extra copy (real tandem duplication, real gene family
   expansion) can legitimately sit on a short contig or lack a domain hit on its own.

3) Every rescued_<genome> gene, among whatever survived steps 1-2, below
   --min-rescued-coverage (default 0.5) Liftoff coverage is dropped outright. rescued_<genome>
   is this pipeline's lowest-confidence tier (round 2 of the build step - a genome's *entire*
   transfer, unfiltered, added only as a last resort) - it never had to clear a coverage/identity
   bar to get into the final annotation in the first place, unlike good_<genome>, so this is the
   one basic quality floor that tier gets.

4) Every kept protein-coding gene/pseudogene is relabeled to feature type "gene" (whatever it
   was called before), and its "pseudogenic_transcript" child (if any) to "transcript" - the one
   thing get_pangenes' own parser actually requires. Non-coding RNA genes are left exactly as
   they are.

5) Every kept gene's ID is renumbered to "<id-prefix><strain-index>g<00001, 00002, ...>". The
   original ID is kept in a new "original_ID=" attribute.

Every removed gene is logged with why, in each genome's own --out-dir/<genome>_filter_report.tsv
- nothing is silently dropped.

Known limitation - "protein domain" is only as good as the source annotation: a genome whose
ORIGINAL annotation never recorded InterPro/PFAM hits at all will have every gene sourced from
it test has_domain=False unconditionally, not because those genes lack real domains, but because
this annotation source never recorded them.

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
from urllib.parse import unquote_plus

ID_RE = re.compile(r"ID=([^;]+)")
PARENT_RE = re.compile(r"Parent=([^;]+)")
DESCRIPTION_RE = re.compile(r"(?:^|;)description=([^;]+)")
PRODUCT_RE = re.compile(r"(?:^|;)product=([^;]+)")

# A description this generic counts as no evidence at all - same as having no description.
GENERIC_DESCRIPTIONS = {
    "hypothetical protein", "hypothetical protein, conserved", "conserved hypothetical protein",
    "unspecified product", "unknown function", "unnamed protein product", "",
}

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
            desc_m = DESCRIPTION_RE.search(attrs) or PRODUCT_RE.search(attrs)
            description = unquote_plus(desc_m.group(1).strip().lower()) if desc_m else ""
            genes[feat_id] = {
                "id": feat_id, "seqname": seqname, "source": source,
                "start": int(start), "end": int(end), "strand": strand,
                "extra_copy_number": _int_attr(attrs, "extra_copy_number"),
                "valid_ORF": _valid_orf(attrs),
                "coverage": _float_attr(attrs, "coverage"),
                "description": description,
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


def has_evidence(gene, require_domain_only):
    if gene["has_domain"]:
        return True
    if require_domain_only:
        return False
    return gene["description"] not in GENERIC_DESCRIPTIONS


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
    one CDS segment total, flank/inside doesn't apply)."""
    segs = bigger_gene["cds_segments"]
    if len(segs) <= 1:
        return "single_exon"
    outer = {segs[0], segs[-1]}
    overlapped = {s for s in segs for ss, se in smaller_cds_segments
                  if max(s[0], ss) <= min(s[1], se)}
    if not overlapped:
        return "inside"  # shouldn't happen (ov_bp>0 implies some segment matched) - fall through safely
    return "flank" if overlapped <= outer else "inside"


def is_qualifying_overlap(g1, g2, ov_bp):
    """A "minor + flank" overlap is auto-kept and doesn't count as a real conflict - everything
    else (minor-but-not-flank, substantial, contained) needs a decision. Returns
    (qualifies: bool, pct_of_smaller: float)."""
    smaller_bp = min(g1["cds_bp"], g2["cds_bp"])
    if smaller_bp == 0:
        return False, 0.0
    pct = ov_bp / smaller_bp
    if pct < 0.2:
        bigger, smaller = (g1, g2) if g1["cds_bp"] >= g2["cds_bp"] else (g2, g1)
        if classify_minor_position(bigger, smaller["cds_segments"]) == "flank":
            return False, pct
    return True, pct


def assign_new_ids(genes, kept_ids, strain_index, id_prefix):
    ordered = sorted(kept_ids, key=lambda gid: (genes[gid]["seqname"], genes[gid]["start"]))
    width = max(5, len(str(len(ordered))))
    return {gid: f"{id_prefix}{strain_index}g{i:0{width}d}" for i, gid in enumerate(ordered, start=1)}


def add_original_id_attr(attrs, old_id):
    return attrs.rstrip(";") + f";original_ID={old_id}"


def panel_check(gene_id, opponent_id, pct, present_in, collides_in, min_overlap_genomes, note):
    """Applied to a gene that locally lost an evidence comparison (or, in the neither-has-
    evidence case, to each side independently) before actually dropping it. Returns a reason
    string if it should be dropped, else None (survives - not enough panel-wide evidence either
    way, or an isolated collision more likely explained by Liftoff boundary noise)."""
    n_present = len(present_in.get(gene_id, ()))
    n_collide = len(collides_in.get(gene_id, ()))
    if n_present <= 2:
        return f"overlaps {opponent_id} ({round(100*pct,1)}% of its own CDS); {note}present in only {n_present} genome(s) panel-wide"
    if n_collide <= 1:
        return None
    if n_collide >= min_overlap_genomes:
        return f"overlaps {opponent_id} ({round(100*pct,1)}% of its own CDS); {note}present in {n_present} genomes, overlapping something in {n_collide} of them"
    return None


def resolve_overlaps_globally(genes_by_strain, args, present_in, n_good_transfers, collides_in, qualifying_by_strain):
    """One pass over every genome's qualifying overlap pairs, building ONE verdict per gene ID
    (by original ID, shared across the panel) - {gene_id: reason}. A gene already in verdict is
    skipped in any later pair it's part of (already decided, and verdicts never reverse)."""
    verdict = {}
    for s, genes in genes_by_strain.items():
        for gid1, gid2, ov_bp, pct in qualifying_by_strain[s]:
            if gid1 in verdict and gid2 in verdict:
                continue
            g1, g2 = genes[gid1], genes[gid2]
            g1_is_ref = g1["source"] == args.reference_source_tag
            g2_is_ref = g2["source"] == args.reference_source_tag

            if g1_is_ref and g2_is_ref:
                continue  # both reference-derived - not this pipeline's call, keep both

            if g1_is_ref or g2_is_ref:
                ref_gene, other = (g1, g2) if g1_is_ref else (g2, g1)
                if has_evidence(other, args.require_domain_only):
                    continue  # uncertain - keep both
                if other["id"] in verdict:
                    continue
                reason = panel_check(other["id"], ref_gene["id"], pct, present_in, collides_in,
                                      args.min_overlap_genomes,
                                      f"no evidence, overlaps the reference ('{args.reference_source_tag}') gene {ref_gene['id']}; ")
                if reason:
                    verdict[other["id"]] = reason
                continue

            g1_ev = has_evidence(g1, args.require_domain_only)
            g2_ev = has_evidence(g2, args.require_domain_only)

            if g1_ev != g2_ev:
                winner, loser = (g1, g2) if g1_ev else (g2, g1)
                if loser["id"] in verdict:
                    continue
                reason = panel_check(loser["id"], winner["id"], pct, present_in, collides_in,
                                      args.min_overlap_genomes,
                                      f"no evidence, {winner['id']} has evidence; ")
                if reason:
                    verdict[loser["id"]] = reason
                continue

            if g1_ev and g2_ev:
                continue  # both have evidence - uncertain, keep both

            if gid1 in verdict or gid2 in verdict:
                continue
            # neither has evidence, neither is main - no panel-presence/recurrence check here
            # (that's only for cases 3/4 above); compare the two genes directly by panel-wide
            # good_<genome> transfer count instead (tie -> longer CDS wins). This also covers
            # a panel-private gene naturally: with no genome to transfer well into, it has 0
            # good_<genome> transfers and loses to any better-supported opponent on its own.
            gt1, gt2 = n_good_transfers.get(gid1, 0), n_good_transfers.get(gid2, 0)
            if gt1 != gt2:
                winner, loser, metric = (g1, g2, f"{gt1} vs {gt2}") if gt1 > gt2 else (g2, g1, f"{gt2} vs {gt1}")
            else:
                winner, loser = (g1, g2) if g1["cds_bp"] >= g2["cds_bp"] else (g2, g1)
                metric = f"tied on good_<genome> transfers panel-wide ({gt1}), kept the longer CDS"
            verdict[loser["id"]] = (
                f"overlaps {winner['id']} ({round(100*pct,1)}% of its own CDS); neither has evidence, "
                f"{winner['id']} more supported panel-wide ({metric})"
            )
    return verdict


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
    parser.add_argument("--min-overlap-genomes", type=int, default=2,
                         help="For a gene present in >2 genomes panel-wide: it needs a qualifying overlap in at least this many of them to count as a real, recurring conflict rather than an isolated Liftoff boundary glitch (default: 2)")
    parser.add_argument("--require-domain-only", action="store_true",
                         help="Only a protein domain counts as evidence - ignore description text entirely (default: off, a specific description also counts)")
    parser.add_argument("--reference-source-tag", default="main",
                         help="The source tag marking the reference-derived tier in this pipeline's output (default: 'main')")
    parser.add_argument("--extra-copy-require-valid-orf", action=argparse.BooleanOptionalAction, default=True,
                         help="Drop an extra-copy gene (extra_copy_number > 0) unless it has a valid ORF (default: on; use --no-extra-copy-require-valid-orf to keep every extra copy regardless of ORF)")
    parser.add_argument("--min-rescued-coverage", type=float, default=0.5,
                         help="Every rescued_<genome> gene (this pipeline's lowest-confidence Liftoff tier - it never had to pass a coverage/identity bar to get in) below this Liftoff coverage is dropped outright, regardless of ORF/evidence/overlap status (default: 0.5)")
    parser.add_argument("--id-prefix", default="Afu", help="Prefix for renamed gene IDs (default: 'Afu', this project's own convention - change for other species)")
    args = parser.parse_args()

    strains = read_strains(args.strains)
    os.makedirs(args.out_dir, exist_ok=True)

    # --- Step 0: parse every genome's raw genes, and panel-wide stats from all of them ---
    genes_by_strain = {}
    present_in = defaultdict(set)
    n_good_transfers = defaultdict(int)
    for s in strains:
        genes = parse_gff(os.path.join(args.final_dir, f"{s}_final_annotation.gff"))
        genes_by_strain[s] = genes
        for gid, g in genes.items():
            present_in[gid].add(s)
            if g["source"].startswith("good_"):
                n_good_transfers[gid] += 1
    print(f"Panel-wide presence built from {len(strains)} genomes: {len(present_in)} distinct gene IDs", file=sys.stderr)

    # First CDS-overlap scan of every genome, to know - panel-wide - how many genomes each gene
    # has a *qualifying* overlap in (minor+flank doesn't count, see module docstring).
    collides_in = defaultdict(set)
    qualifying_by_strain = {}
    for s, genes in genes_by_strain.items():
        overlap_pairs = find_cds_overlaps(genes, args.min_overlap_bp)
        qualifying = []
        for gid1, gid2, ov_bp in overlap_pairs:
            qualifies, pct = is_qualifying_overlap(genes[gid1], genes[gid2], ov_bp)
            if not qualifies:
                continue
            qualifying.append((gid1, gid2, ov_bp, pct))
            collides_in[gid1].add(s)
            collides_in[gid2].add(s)
        qualifying_by_strain[s] = qualifying
    print(f"Overlap scan: {sum(len(v) for v in qualifying_by_strain.values())} qualifying pairs across the panel", file=sys.stderr)

    # --- Step 1: resolve overlaps globally - one verdict per gene ID, panel-wide ---
    verdict = resolve_overlaps_globally(genes_by_strain, args, present_in, n_good_transfers, collides_in, qualifying_by_strain)
    print(f"Overlap resolution: {len(verdict)} genes dropped panel-wide", file=sys.stderr)

    # --- Steps 2-3: extra copies, then rescued-coverage floor - only among overlap survivors ---
    for s, genes in genes_by_strain.items():
        for gid, g in genes.items():
            if gid in verdict:
                continue
            if g["extra_copy_number"] and args.extra_copy_require_valid_orf and not g["valid_ORF"]:
                verdict[gid] = "extra copy with no valid ORF"
    for s, genes in genes_by_strain.items():
        for gid, g in genes.items():
            if gid in verdict or not g["source"].startswith("rescued_"):
                continue
            if g["coverage"] is not None and g["coverage"] < args.min_rescued_coverage:
                verdict[gid] = f"rescued transfer, Liftoff coverage {g['coverage']:.2f} < {args.min_rescued_coverage}"

    # --- Steps 4-5: write every genome's output, applying the same verdicts everywhere ---
    summary_rows = []
    for i, s in enumerate(strains, start=1):
        genes = genes_by_strain[s]
        gff_path = os.path.join(args.final_dir, f"{s}_final_annotation.gff")
        out_path = os.path.join(args.out_dir, f"{s}_final_annotation_filtered.gff")
        report_path = os.path.join(args.out_dir, f"{s}_filter_report.tsv")

        kept_ids = {gid for gid in genes if gid not in verdict}
        id_mapping = assign_new_ids(genes, kept_ids, i, args.id_prefix)
        write_filtered_gff(gff_path, out_path, genes, kept_ids, id_mapping)

        with open(report_path, "w") as rep_fh:
            rep_fh.write("gene_id\tsource\tseqname\treason\n")
            for gid, g in genes.items():
                if gid in verdict:
                    rep_fh.write(f"{gid}\t{g['source']}\t{g['seqname']}\t{verdict[gid]}\n")

        n_total = len(genes)
        n_removed = sum(1 for gid in genes if gid in verdict)
        print(f"  {s}: {n_total} protein-coding genes -> {n_total - n_removed} kept, "
              f"{n_removed} removed ({round(100*n_removed/n_total,1) if n_total else 0}%) -> {out_path}", file=sys.stderr)
        summary_rows.append((s, n_total, n_total - n_removed, n_removed))

    with open(os.path.join(args.out_dir, "filter_summary.tsv"), "w") as fh:
        fh.write("strain\tn_original\tn_kept\tn_removed\n")
        for s, n_total, n_kept, n_removed in summary_rows:
            fh.write(f"{s}\t{n_total}\t{n_kept}\t{n_removed}\n")

    print(f"All genomes filtered. Outputs are in {args.out_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()
