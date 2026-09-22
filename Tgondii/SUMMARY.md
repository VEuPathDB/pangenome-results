# *Toxoplasma gondii* Pangenome — Summary

> **Quick read for an overview of the analysis and key findings.**
> For the full technical report — methods, parameters, tables, and figures — see
> [README.md](README.md).

---

A pangenome analysis of **15 *Toxoplasma gondii* genomes** spanning the three dominant
clonal lineages (Type I, II and III) plus diverse atypical South American, African, and
Asian isolates. The goal is to identify core and accessory genes and understand how gene
content varies across lineages differing in virulence and geographic origin. The analysis
follows the same 8-step pipeline used for *A. fumigatus*.

---

## Analysis progress

| Step | Description | Status |
| :--- | :--- | :---: |
| [01 – Genome Selection & QC](README.md#01--genome-selection--qc) | Strain selection, species check, contig profiling, synteny | ✅ Complete |
| [02 – TE Annotation & Clean Up](README.md#02--te-annotation--clean-up) | Transposable element annotation, candidate validation | ✅ Complete |
| [03 – *de novo* Genome Annotation](README.md#03--de-novo-genome-annotation) | Gene prediction on cleaned assemblies | ⏭️ Not needed (all strains already annotated) |
| [04 – InterProScan](README.md#04--interproscan) | Functional domain annotation | ✅ Complete |
| [05 – Cross-genome Annotation Integration](README.md#05--cross-genome-annotation-integration) | Merging and standardising annotations across strains | 🔄 In progress |
| [06 – GET_PANGENES](README.md#06--get_pangenes) | Synteny-based ortholog clustering (core / accessory) | 🔄 In progress |
| [07 – Post-GET_PANGENES Adjusting](README.md#07--post-get_pangenes-adjusting) | Manual review and refinement of pangene calls | 🔄 In progress |
| [08 – Pangenome Visualisation](README.md#08--pangenome-visualisation) | Figures, presence/absence matrix, summary stats | 🔄 In progress |

---

## Key results so far

### 01 – Genome Selection & QC

- **15 strains selected** from ToxoDB, including the three chromosome-level references
  (ME49 Type II, GT1 Type I, VEG Type III), one PacBio-assembled strain (RH-88 Type I),
  and 11 scaffold-level assemblies covering diverse lineages and geographic origins.
  4 additional strains were excluded due to absence of gene annotation (GFF) in ToxoDB.
- **All 15 confirmed as *T. gondii*** by whole-genome ANI against ME49 (98.7–99.7%).
  No contamination or wrong-species assemblies detected.
- **Small contigs are numerous but gene-bearing.** The panel contains **34,066 sub-10kb
  contigs** — 93–99% of each genome's contig count — except RH-88, which is a notably
  cleaner assembly (only 62 small contigs, 32% of its total). These small contigs carry
  **2,388 protein-coding genes** across the panel, including 289 known SRS/ROP/GRA/RON/AP2/MIC
  virulence-family genes and ~636 organelle-genome genes — not gene-free junk.
- **Decision: drop every contig <10kb, panel-wide, as an arbitrary blanket cutoff** — not a
  per-contig evidence check. Knowingly discards the 2,388 genes above (virulence-family genes
  included) as the accepted cost of a simple, panel-wide rule. Script
(`01_Genome_Selection_QC/scripts/drop_short_contigs.slurm.sh`) **already run** — see
[README.md](README.md#short-contig-removal--arbitrary-10kb-cutoff-done).
- **Chromosome structure is highly conserved across all lineages.** All 14 dot-plots show
  a clean 1:1 staircase to ME49's 14 chromosomes — no translocations or arm-scale
  rearrangements in any lineage (Type I/II/III, African, Amazonian, Asian).
- **One recurrent inversion polymorphism identified:** a ~70 kb inverted block at the end
  of chromosome IX is shared by 4 strains (CAST, RUB, VAND, TgCatPRC2) — a real
  segregating variant, absent from the remaining 10 strains.
- **RH-88** has a unique ~515 kb inversion on chromosome IV and is assembled as 13
  chromosomes (one scaffold joins ME49 chrVIIb + chrVIII) — an assembly/nomenclature
  difference to confirm.
- **A recurrent segmental duplication** in ME49 itself (~80–85 kb shared between chrIII
  and chrX) is detected in 5 strains — this is a reference feature, not per-strain events.

### 02 – TE Annotation & Clean Up

- ***T. gondii* has no bona fide transposable elements.** The TE candidate discovery
  pipeline was run on all 15 genomes and the candidates manually inspected with TE-Aid.
  No genuine *T. gondii* TE families were found — candidates were low-complexity /
  tandem satellite repeats or conserved sequences, not mobile elements.
- **Human L1 LINE elements were recovered as apparent TE candidates in multiple strains,
  including the reference genome ME49.** These are human host-cell DNA contamination
  (cell-culture origin), not *T. gondii* sequences — confirms the panel carries contigs of
  contamination origin. Handled via step 01's blanket <10kb contig cutoff (see above), not a
  targeted BLASTn removal.
- **No GFF filtering was applied** — because there are no *T. gondii* TEs, no
  TE-derived gene models need to be removed from the annotations.
- **Final curated TE library:** empty. No species-specific TE masking will be used.

### 03–08 — In progress

**03 – not needed:** all 15 strains already have a genome annotation (GFF, from
ToxoDB/VEuPathDB) — step 03 exists only for genomes with no annotation at all.

Results for InterProScan, cross-genome integration, pangene clustering, and visualisation
(04–08) will be added here as each step is completed.

---

## Important caveats

- **Small contigs are being dropped by an arbitrary length cutoff, not per-strain review.**
  Unlike the Afum panel (which was largely chromosome-scale after cleanup), most *T. gondii*
  assemblies are highly fragmented (thousands of scaffolds). Rather than reviewing each small
  contig individually, the panel drops every contig <10kb outright — a simple blanket rule
  that knowingly costs 2,388 real genes (289 known virulence-family genes among them), not yet
  applied (cluster down).
- **Organellar DNA (NUMTs/NUPTs) is abundant and strain-variable.** *T. gondii* carries
  >11,000 organellar DNA insertions (>1 Mb) in the nuclear genome, and unlike Afum, two
  organelles must be screened — the mitochondrion and the apicoplast. Most hits will be
  genuine nuclear insertions to keep, not whole-organelle contigs to drop.
- **Lineage-specific copy-number variation at key loci** (e.g. ROP5: 6 copies in Type I/III
  vs. 11 in Type II) will appear as gene gain/loss in the pangenome matrix. These loci
  require manual review rather than relying on the matrix alone.
- The pangenome matrix captures **gene presence/absence only** — virulence differences
  between lineages are driven largely by allelic variation within shared genes (ROP kinases,
  GRA effectors, SRS surface antigens), which require separate targeted analyses.

---

## Files

| File | Description |
| :--- | :--- |
| [README.md](README.md) | Full technical report — all methods, parameters, tables, figures |
| 01_Genome_Selection_QC/ *(working data, not published here)* | QC outputs: ANI, contig profile, synteny |
| 02_TE_annotation_Clean_Up/ *(working data, not published here)* | TE candidate pipeline, TE-Aid validation |
| 03_denovo_Genome_Annotation/ *(working data, not published here)* | *de novo* gene predictions |
| 04_InterProScan/ *(working data, not published here)* | Domain annotations |
| 05_Cross-genome_annotation_integration/ *(working data, not published here)* | Merged annotation files |
| 06_GET_PANGENES/ *(working data, not published here)* | Pangene clusters |
| 07_Post_GET_PANGENES_adjusting/ *(working data, not published here)* | Reviewed and curated pangene calls |
| 08_Pangenome_Visualisation/ *(working data, not published here)* | Figures and summary tables |

---

[↑ Back to top](#analysis-progress) &nbsp;|&nbsp; [Back to Pangenome Pipeline](../../README.md)
