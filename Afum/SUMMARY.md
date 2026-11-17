# *Aspergillus fumigatus* Pangenome — Summary

> **Quick read for an overview of the analysis and key findings.**
> For the methods, parameters, tables and figures, see the [full report](README.md).

---


## Analysis progress

| Step | Description | Status |
| :--- | :--- | :---: |
| [01 – Genome Selection & QC](README.md#01--genome-selection--qc) | Strain selection, species check, organelle removal, synteny, assembly assessment | ✅ Complete |
| [02 – TE Annotation & Clean Up](README.md#02--te-annotation--clean-up) | Transposable element annotation, TE-gene overlap filtering | ✅ Complete |
| [03 – *de novo* Genome Annotation](README.md#03--de-novo-genome-annotation) | Gene prediction on cleaned assemblies | ⏭️ Not needed (all strains already annotated) |
| [04 – Protein evidence (InterProScan and PSAURON)](README.md#04--protein-evidence-interproscan-and-psauron) | Functional domain annotation; PSAURON scores | ✅ Complete |
| [05 – Cross-genome Annotation Integration](README.md#05--cross-genome-annotation-integration) | Merging and standardising annotations across strains | ✅ Complete |
| [06 – GET_PANGENES](README.md#06--get_pangenes) | Synteny-based ortholog clustering (core / accessory) | ✅ Complete |
| [07 – Post-GET_PANGENES Adjusting and Visualisation](README.md#07--post-get_pangenes-adjusting-and-visualisation) | Safe fix, curation and removal of false genes, final figures and explorer | ✅ Complete |
| [08 – Final GFF](https://github.com/VEuPathDB/pangenome-pipeline/blob/main/08_Final_GFF/README.md) | Final annotation: model of genes with a broken ORF, UTRs, other transcripts and non-coding genes put back, gene IDs, InterProScan on the final proteins | ⏳ To do |

---

## Key results so far

### 01 – Genome Selection & QC

- **17 strains selected**, including chromosome-level long-read assemblies alongside the three FungiDB genomes (Af293, A1160, A1163).
- **All 16 strains compared with the reference Af293 are confirmed as *A. fumigatus* sensu stricto** by
  whole-genome ANI (99.2–99.6%).
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
  alignment identity) and should be interpreted with caution. The assembly assessment also shows it as the outlier:
  largest genome (30.5 Mb), most genes (10,665) and one of the lowest N50s (1.96 Mb).
- **Two annotation styles** in the panel: A1160, A1163, D141 and AF293 have more genes than mRNAs and fewer exons; the
  other 13 genomes have isoforms (more mRNAs than genes).

### 02 – TE Annotation & Clean Up

- **TE content is low throughout the panel: 1.9–5.7% of each genome** (~0.5–1.75 Mb).
  This is typical for a compact *Aspergillus* genome.
- **LTR/Gypsy elements dominate** (55–65% of all TE content), followed by DNA/Tc1-Mariner
  and LTR/Copia — the rank order is the same in every strain.
- **TE family composition carries a sub-lineage signal.** The 4 strains sharing the
  chromosome-2 inversion also share a distinct TE profile (depletion of major Gypsy families;
  enrichment of `Gypsy-3_AF`), suggesting this is a genuine genetic sub-group.
- **339 TE-derived gene models were removed** from the GFF annotations across all genomes
  before downstream steps — preventing transposon fragments from being counted as real genes.
- **Only 56 genes across the whole panel fall in the ambiguous zone** (20–80% TE overlap)
  and require manual review. AF293 contributes more of these than any other strain, likely
  reflecting differences in the original annotation era.

### 03–04

Not needed for *de novo* annotation (all strains already annotated); InterProScan was run on every strain (see the [full report](README.md#04--protein-evidence-interproscan-and-psauron)).

### 05 – Cross-genome Annotation Integration

- **Basket annotation.** The genes of all strains that lie at the same place form a basket; each basket gets one panel
  model (AF293's when it has one), written into every strain where it fits. **11,542 panel genes**: the 10,015 AF293
  genes and 1,527 genes not in the AF293 annotation.
- **Copies of a gene in one strain are kept apart:** 561 copies became genes of their own.
- **10,016–10,608 genes per strain.** Most strains gain genes: 489–717 per strain were added where
  the strain had no gene. 3,246 genes were eliminated by the quality rules (PSAURON, < 100 aa, no valid ORF).
- **98% of the genes have a valid ORF**; only 56 have an ORF broken by the assembly.

### 06 – GET_PANGENES

- **11,758 pangenes** across the 17 strains.

### 07 – Post-GET_PANGENES Adjusting

- **Safe fix:** 120 genes moved back to the pangene of their gene, and 174 genes that `get_pangenes` had split over
  several pangenes joined again. **11,468 pangenes**: 9,638 core (17 strains), 133 soft-core, 862 shell, 835 cloud.
- **The core settles at about 9,600 pangenes**; ATCC 46645 has the most singletons (142). AF293 misses 37 of the 133
  soft-core pangenes.
- **The cloud is enriched** in protein kinases, DUF3435 (the captains of Starship elements), the subtelomeric
  hrmA-associated cluster protein and the orsellinic acid/F9775 cluster protein D (subtelomeric and secondary
  metabolite clusters), and in transposase domains from the transposon Afu1g00140: below the 80% TE-overlap cut of step 02, so kept there,
  but confirmed as a TE; it is removed in the curation.
- **Curation:** of the 308 genes the pipeline added to AF293, 175 were judged false and deleted from every strain with
  the transposon (176 panel genes, 2,458 genes); 102 were kept; 31 to delete in AF293 only are left for the group.
- **Final pangenome: 11,278 pangenes**, named `Af_pan_00001`–`Af_pan_11278`: 9,536 core, 125 soft-core, 803 shell,
  814 cloud. The core settles at about 9,500 pangenes; the transposase domains are no longer enriched in the cloud.

---

## Important caveats

- Two strains (**A1160** and **A1163**) are derived laboratory strains from the CEA10
  lineage and carry engineered sequences (a *Aspergillus niger* gene in A1163; a
  zeocin-resistance cassette replacing *akuB* in A1160). These sequences will appear as
  "accessory" but are **lab artefacts, not biology**.
- The synteny-based approach requires chromosome-level assemblies for the most reliable calls.
  Sub-telomeric accessory regions — where most lineage-specific genes live — are the least
  certain part of any pangenome, including this one.
- **Some genes are still split over several pangenes.** 256 baskets remain split after the safe fix, where a pangene also
  holds genes of other baskets; they can inflate the cloud and are left for curation.
- **Short effector genes.** The < 100 aa rule of step 05 eliminates short proteins, and fungal effectors can be shorter.
  A list of protected genes (e.g. predicted effectors) is planned, so that their baskets are never eliminated.
- **The final GFF is not made yet** ([step 08](https://github.com/VEuPathDB/pangenome-pipeline/blob/main/08_Final_GFF/README.md)): what to do with
  broken ORFs, the gene IDs, and what to put back (UTRs, other transcripts, non-coding genes) are still to be decided.
- The pangenome matrix captures **gene presence/absence only**. Azole resistance in
  *A. fumigatus* is driven largely by *sequence variants within* core genes (e.g., *cyp51A*
  promoter repeats + coding substitutions), which require a separate targeted analysis.

---

## Files

| File | Description |
| :--- | :--- |
| [Full report](README.md) | Full technical report — all methods, parameters, tables, figures |
| [genome_order.txt](genome_order.txt) | Ordered list of the 17 strains used |
| [01_Genome_Selection_QC/](01_Genome_Selection_QC/) | QC outputs: ANI, synteny, organelle and redundancy screens |
| [02_TE_annotation_Clean_Up/](02_TE_annotation_Clean_Up/) | TE library, RepeatMasker results, TE-gene overlap |
| [03_denovo_Genome_Annotation/](03_denovo_Genome_Annotation/) | *de novo* gene predictions |
| [04_InterProScan/](04_InterProScan/) | Domain annotations and PSAURON scores |
| [05_Basket_annotation_integration/](05_Basket_annotation_integration/) | Basket annotation: final GFFs, gene fate, figures |
| [06_GET_PANGENES/](06_GET_PANGENES/) | Pangene clusters |
| [07_Post_GET_PANGENES_adjusting/](07_Post_GET_PANGENES_adjusting/) | Reviewed and curated pangene calls |

---

[↑ Back to top](#analysis-progress) &nbsp;|&nbsp; [Back to Pangenome Pipeline](https://github.com/VEuPathDB/pangenome-pipeline/blob/main/README.md)
