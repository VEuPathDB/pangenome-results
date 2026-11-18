# *Plasmodium falciparum* Pangenome — Summary

> **⚠️ Draft results – do not use.** These are draft results of the current version of the pangenome pipeline, provided to document the pipeline outputs. They must not be used for any analysis or publication.

> **Quick read for an overview of the analysis and key findings.**
> For the methods, parameters, tables and figures, see the [full report](README.md).

---

## Analysis progress

| Step | Description | Status |
| :--- | :--- | :---: |
| [01 – Genome Selection & QC](README.md#01--genome-selection--qc) | Strain selection, species check, contig profiling, synteny, organelle and redundancy screens, contig removal | ✅ Complete |
| [02 – TE Annotation & Clean Up](README.md#02--te-annotation--clean-up) | Transposable element annotation, candidate validation | ✅ Complete |
| 03 – *de novo* Genome Annotation | Gene prediction on cleaned assemblies | ⏭️ Not needed |
| 04 – Protein evidence (InterProScan and PSAURON) | Functional domain annotation; PSAURON scores | ⏳ To do |
| 05 – Cross-genome Annotation Integration | Merging and standardising annotations across strains | ⏳ To do |
| 06 – GET_PANGENES | Synteny-based ortholog clustering (core / accessory) | ⏳ To do |
| 07 – Post-GET_PANGENES Adjusting and Visualisation | Safe fix, curation and removal of false genes, final figures and explorer | ⏳ To do |
| 08 – Final GFF | Final annotation, with the genes left out of the pangenome put back | ⏳ To do |

---

## Key results so far

### 01 – Genome Selection & QC

- **20 genomes downloaded from PlasmoDB (release 71); 16 kept for the pangenome.** All 20 are *P. falciparum* (ANI 99.53–99.99% to the 3D7 reference) and near chromosome-level (N50 1.46–1.82 Mb).
- **4 genomes excluded:**
  - **ML01 and TG01** come from multiple infections. Each carries ~2.5 Mb of extra sequence in many small contigs (117 and 79 contigs), and ML01 also has contigs of human origin.
  - **SD01** has chromosome 4 assembled inside chromosome 7.
  - **NF135C10** has chromosomes 7 and 8 swapping arms at ~0.5 Mb.
- **NF54 is almost identical to 3D7** (99.99% ANI), as expected: 3D7 is a clone of NF54.
- **The other genomes are collinear with 3D7.** Every inversion ≥ 20 kb (9 in total) lies at a chromosome end, in the hypervariable subtelomeres.
- **Organelles removed.** 15 of the 16 genomes carry the apicoplast and the mitochondrion as one contig each; CD01 has neither. Both organelles were removed from all genomes (30 contigs, 1,308 genes), so every genome is nuclear-only.
- **13 redundant contigs removed** (228 kb, 23 genes). Each is ≥ 94% duplicated in a longer contig of the same assembly, and has either no genes or genes that all have an identical copy elsewhere. Four other redundant-looking contigs were kept because they carry variant-family genes (PfEMP1, *rifin*, *stevor*) found nowhere else in their genome.

### 02 – TE Annotation & Clean Up

- ***P. falciparum* has no transposable elements.** This is known from the literature; the TE candidate pipeline was run anyway, and no TE was confirmed in the manual curation.
- **Human contamination in ML01.** The only TE sequences found were human LINEs, on three small ML01 contigs. ML01 is excluded from the pangenome, so they are removed with it.

### 03 – *de novo* Genome Annotation

Not needed: all 16 genomes already have a genome annotation (GFF, from PlasmoDB).
