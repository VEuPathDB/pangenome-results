# *Aspergillus fumigatus* Pangenome — Summary

> **Quick read for an overview of the analysis and key findings.**
> For the full technical report — methods, parameters, tables, and figures — see
> [README.md](README.md).

---

A pangenome analysis of **17 *Aspergillus fumigatus* genomes** (16 non-reference strains + the
reference Af293), spanning clinical and environmental isolates from Europe, North America,
and New Zealand. The goal is to identify core genes (present in all strains), accessory genes
(present in some), and understand how gene content variation relates to traits. The analysis follows an 8-step pipeline developed for eukaryotic species.

---

## Analysis progress

| Step | Description | Status |
| :--- | :--- | :---: |
| [01 – Genome Selection & QC](#01--genome-selection--qc) | Strain selection, species check, organelle removal, synteny | ✅ Complete |
| [02 – TE Annotation & Clean Up](#02--te-annotation--clean-up) | Transposable element annotation, TE-gene overlap filtering | ✅ Complete |
| [03 – *de novo* Genome Annotation](#0308--in-progress) | Gene prediction on cleaned assemblies | 🔄 In progress |
| [04 – InterProScan](#0308--in-progress) | Functional domain annotation | 🔄 In progress |
| [05 – Cross-genome Annotation Integration](#0308--in-progress) | Merging and standardising annotations across strains | 🔄 In progress |
| [06 – GET_PANGENES](#0308--in-progress) | Synteny-based ortholog clustering (core / accessory) | 🔄 In progress |
| [07 – Post-GET_PANGENES Adjusting](#0308--in-progress) | Manual review and refinement of pangene calls | 🔄 In progress |
| [08 – Pangenome Visualisation](#0308--in-progress) | Figures, presence/absence matrix, summary stats | 🔄 In progress |

---

## Key results so far

### 01 – Genome Selection & QC

- **17 strains selected**, including chromosome-level long-read assemblies (ONT/PacBio) from
  the UCR panel alongside the three FungiDB genomes (Af293, A1160, A1163).
- **All 17 confirmed as *A. fumigatus* sensu stricto** by whole-genome ANI against Af293
  (99.2–99.6%). No cryptic sibling species detected.
- **30 contigs removed across 9 of the 17 strains** before analysis: 12 organelle
  (mitochondrial) contigs from 4 strains (AF293, AF100-9B, ATCC 42202, 47-4), and 18
  redundant/duplicated contigs from 5 strains (A1163, H237, 08-19-02-30, B5233, eAF1090) —
  preventing inflated gene counts. After cleanup, only **36 sub-10kb contigs remain across
  the entire panel**, carrying just 4 genes combined.
- **Chromosome structure is highly conserved.** All 16 strains show 1:1 collinearity with
  Af293's 8 chromosomes; no translocations or chromosome fusions detected.
- **One recurrent inversion polymorphism identified:** a ~707 kb inverted block on
  chromosome 2 is shared by 4 strains (W72310, eAF1023, eAF1090, eAF1436) — a real
  segregating variant in the population, not an assembly error.
- ⚠️ **ATCC 46645** is the lowest-quality assembly in the panel (most fragmented, lowest
  alignment identity) and should be interpreted with caution.

### 02 – TE Annotation & Clean Up

- **TE content is low throughout the panel: 1.9–5.7% of each genome** (~0.5–1.75 Mb).
  This is typical for a compact *Aspergillus* genome.
- **LTR/Gypsy elements dominate** (55–65% of all TE content), followed by DNA/Tc1-Mariner
  and LTR/Copia — the rank order is the same in every strain.
- **TE family composition carries a sub-lineage signal.** The 4 strains sharing the
  chromosome-2 inversion also share a distinct TE profile (depletion of major Gypsy families;
  enrichment of `Gypsy-3_AF`), suggesting this is a genuine genetic sub-group.
- **337 TE-derived gene models were removed** from the GFF annotations across all genomes
  before downstream steps — preventing transposon fragments from being counted as real genes.
- **Only 56 genes across the whole panel fall in the ambiguous zone** (20–80% TE overlap)
  and require manual review. AF293 contributes more of these than any other strain, likely
  reflecting differences in the original annotation era.

### 03–08 — In progress

Results for *de novo* annotation, InterProScan, pangene clustering, and visualisation will
be added here as each step is completed.

---

## Important caveats

- Two strains (**A1160** and **A1163**) are derived laboratory strains from the CEA10
  lineage and carry engineered sequences (a *Aspergillus niger* gene in A1163; a
  zeocin-resistance cassette replacing *akuB* in A1160). These sequences will appear as
  "accessory" but are **lab artefacts, not biology**.
- The synteny-based approach requires chromosome-level assemblies for the most reliable calls.
  Sub-telomeric accessory regions — where most lineage-specific genes live — are the least
  certain part of any pangenome, including this one.
- The pangenome matrix captures **gene presence/absence only**. Azole resistance in
  *A. fumigatus* is driven largely by *sequence variants within* core genes (e.g., *cyp51A*
  promoter repeats + coding substitutions), which require a separate targeted analysis.

---

## Files

| File | Description |
| :--- | :--- |
| [README.md](README.md) | Full technical report — all methods, parameters, tables, figures |
| [genome_order.txt](genome_order.txt) | Ordered list of the 17 strains used |
| 01_Genome_Selection_QC/ *(working data, not published here)* | QC outputs: ANI, synteny, organelle and redundancy screens |
| 02_TE_annotation_Clean_Up/ *(working data, not published here)* | TE library, RepeatMasker results, TE-gene overlap |
| 03_denovo_Genome_Annotation/ *(working data, not published here)* | *de novo* gene predictions |
| 04_InterProScan/ *(working data, not published here)* | Domain annotations |
| 05_Cross-genome_annotation_integration/ *(working data, not published here)* | Merged annotation files |
| 06_GET_PANGENES/ *(working data, not published here)* | Pangene clusters |
| 07_Post_GET_PANGENES_adjusting/ *(working data, not published here)* | Reviewed and curated pangene calls |
| 08_Pangenome_Visualisation/ *(working data, not published here)* | Figures and summary tables |

---

[↑ Back to top](#analysis-progress) &nbsp;|&nbsp; [Back to Pangenome Pipeline](../../README.md)
