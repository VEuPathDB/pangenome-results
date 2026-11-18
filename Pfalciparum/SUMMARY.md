# *Plasmodium falciparum* Pangenome — Summary

> **⚠️ Draft results – do not use.** These are draft results of the current version of the pangenome pipeline, provided to document the pipeline outputs. They must not be used for any analysis or publication.

> **Quick read for an overview of the analysis and key findings.**
> For the methods, parameters, tables and figures, see the [full report](README.md).

---


## Analysis progress

| Step | Description | Status |
| :--- | :--- | :---: |
| [01 – Genome Selection & QC](README.md#01--genome-selection--qc) | Strain selection, species check, contig profiling, synteny, organelle screen | 🔄 In progress |
| [02 – TE Annotation & Clean Up](README.md#02--te-annotation--clean-up) | Transposable element annotation, candidate validation | ✅ Complete |
| [03 – *de novo* Genome Annotation](https://github.com/VEuPathDB/pangenome-pipeline/blob/main/03_denovo_Genome_Annotation/README.md) | Gene prediction on cleaned assemblies | ⏭️ Not needed |
| [04 – Protein evidence (InterProScan and PSAURON)](https://github.com/VEuPathDB/pangenome-pipeline/blob/main/04_Protein_evidence/README.md) | Functional domain annotation; PSAURON scores | ⏳ To do |
| [05 – Cross-genome Annotation Integration](https://github.com/VEuPathDB/pangenome-pipeline/blob/main/05_Basket_annotation_integration/README.md) | Merging and standardising annotations across strains | ⏳ To do |
| [06 – GET_PANGENES](https://github.com/VEuPathDB/pangenome-pipeline/blob/main/06_GET_PANGENES/README.md) | Synteny-based ortholog clustering (core / accessory) | ⏳ To do |
| [07 – Post-GET_PANGENES Adjusting and Visualisation](https://github.com/VEuPathDB/pangenome-pipeline/blob/main/07_Post_GET_PANGENES_adjusting/README.md) | Safe fix, curation and removal of false genes, final figures and explorer | ⏳ To do |
| [08 – Final GFF](https://github.com/VEuPathDB/pangenome-pipeline/blob/main/08_Final_GFF/README.md) | Final annotation: model of genes with a broken ORF, UTRs, other transcripts and non-coding genes put back, gene IDs, InterProScan on the final proteins | ⏳ To do |

---

## Key results so far

### 01 – Genome Selection & QC

- **20 annotated genomes from PlasmoDB (release 71), 16 kept for the pangenome.** All 20 are *P. falciparum*
  (whole-genome ANI 99.53–99.99% to the 3D7 reference).
- **The assemblies are near chromosome level.** N50 is 1.46–1.82 Mb and most genomes have 16–36 contigs.
- **Four genomes are excluded:**
  - **ML01 and TG01** come from multiple infections. Each carries ~2.5 Mb of extra sequence in many small contigs
    (117 and 79 contigs), with ~600 more genes than the other genomes; ML01 also carries contigs of human origin.
  - **SD01**: chromosome 4 is assembled inside chromosome 7.
  - **NF135C10**: chromosomes 7 and 8 swap arms at ~0.5 Mb.
- **The other genomes are collinear with 3D7** (96–100% of 3D7 covered). All inversions of 20 kb or more lie in the
  subtelomeres, within ~125 kb of a chromosome end.
- **NF54 is almost identical to 3D7** (99.99% ANI), as expected for the parent of the 3D7 clone.
- **Organelles.** 15 of the 16 kept genomes have the apicoplast and the mitochondrion each as one contig of its own;
  CD01 has neither. No organelle fragment was found inside a nuclear contig.

### 02 – TE Annotation & Clean Up

- ***P. falciparum* has no transposable elements**, as known from the literature. The TE candidate pipeline confirmed
  no TE candidate.
- **Human contamination in ML01.** The only TE sequences found were human LINEs, on three small ML01 contigs; they are
  removed with ML01.

### 03 – *de novo* Genome Annotation

Not needed: all genomes already have a genome annotation (GFF, from PlasmoDB).

---

## Important caveats

- **Subtelomeric gene families will dominate the accessory genome.** The large variant antigen families (*var*,
  *rifin*, *stevor*) sit in subtelomeres that cannot be aligned between isolates. A synteny-based method resolves
  the core well, but some accessory genes and singletons in these families may come from the poor alignment.
- **Closely related genomes in the panel.** NF54 and 3D7 are nearly identical, and the panel holds two assemblies of
  7G8 (`7G8` and `7G8-2019`). Both 7G8 assemblies are kept for now; near-duplicate genomes weight the shared genes
  of their lineage in the pangenome counts.
- **The pangenome shows gene presence/absence, not sequence variation.** Important differences between strains, such
  as drug-resistance mutations in *kelch13* or *pfcrt*, are point mutations in shared genes and do not appear in the
  pangenome matrix.

---


[↑ Back to top](#analysis-progress) &nbsp;|&nbsp; [Back to Pangenome Pipeline](https://github.com/VEuPathDB/pangenome-pipeline/blob/main/README.md)
