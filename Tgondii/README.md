# *Toxoplasma gondii* Pangenome Analysis

> **⚠️ Draft results – do not use.** These are draft results of the current version of the pangenome pipeline, provided to document the pipeline outputs. They must not be used for any analysis or publication.

This document tracks the execution, parameters, and results of the pangenome analysis for ***Toxoplasma gondii***, following the steps from the [`pangenome_analysis`](https://github.com/VEuPathDB/pangenome-pipeline/blob/main/README.md) pipeline.

> **Note:** this report was written while the pipeline was being developed. Some commands, folder names and links refer to earlier versions of the pipeline and may not match the current [pipeline repository](https://github.com/VEuPathDB/pangenome-pipeline).

---

## Species Biology & Pangenome Considerations

* **Obligate intracellular apicomplexan, extremely broad host range.** *Toxoplasma gondii*
  infects essentially any warm-blooded animal as an intermediate host (asexual tachyzoite /
  bradyzoite stages); the sexual cycle — and the only stage where genetic recombination can
  occur — happens exclusively in the gut of felids (cats), the definitive host.

* **No transposable elements.** A systematic apicomplexan-wide mobilome screen
  ([Rodriguez & Makalowski, 2022](https://doi.org/10.3390/genes13050887), using
  RepeatModeler, RepeatMasker, LTRpred, MGEScan and TEclass — largely the same toolkit this
  pipeline's [TE candidate pipeline](https://github.com/VEuPathDB/pangenome-pipeline/blob/main/02_TE_annotation_Clean_Up/README.md)
  uses) found **no bona fide TEs in *T. gondii*, nor in its closest relatives** *Hammondia*,
  *Neospora*, and *Sarcocystis* (the whole family came back negative; *Cryptosporidium* too).
  TEs are present elsewhere in Apicomplexa (*Eimeria*, some *Babesia*/*Theileria* species,
  *Ascogregarina*, *Gregarina*), so this is a real, lineage-specific absence, not a detection
  failure. Their own RepeatModeler runs *did* produce candidate repeat families for
  *Toxoplasma* — on curation these turned out to be conserved host genes or low-complexity
  regions, not TEs. What repetitive DNA *T. gondii* genuinely has is tandem/satellite repeat
  (the TGR1A/1E/2/4 and ABGTg7/ABGTg8.2 families), concentrated in subtelomeres — not mobile
  elements. **Implication for [step 02](#02--te-annotation--clean-up):** expect the curated
  TE library to end up small or empty, and most TE candidates to fail curation.

* **Organellar DNA (NUMT/NUPT) insertion into the nuclear genome is massive, ongoing, and
  strain-variable.**
  [Namasivayam et al. (2023)](https://doi.org/10.1073/pnas.2308569120) found **>11,000
  organellar DNA insertions totalling >1 Mb** in the compact 65 Mb *T. gondii* nuclear
  genome — nuclear mitochondrial DNA (NUMTs) and nuclear plastid/apicoplast DNA (NUPTs) —
  continuously acquired and a significant source of **intraspecific** variation, i.e. it
  differs from strain to strain within the panel, not just between *T. gondii* and its
  organelle. **Implication for [step 01](#01--genome-selection--qc):** the
  [organelle screen](https://github.com/VEuPathDB/pangenome-pipeline/blob/main/01_Genome_Selection_QC/README.md#10-organelle-screen)
  should expect to find many more, and more scattered, organellar fragments in the nuclear
  assemblies — most will be small fragments
  genuinely embedded in nuclear contigs (real nuclear DNA — keep, per the existing
  fragment-vs-whole-organelle-contig rule) rather than a handful of whole-organelle contigs
  to drop, so this step will likely need many manual judgment calls.
  Also, unlike a fungus, *T. gondii* carries **two organelles to screen** — mitochondrion
  *and* apicoplast (a relict, non-photosynthetic plastid retained by most Apicomplexa) — both
  need their own contig/fragment identified before the
  [organelle screen](https://github.com/VEuPathDB/pangenome-pipeline/blob/main/01_Genome_Selection_QC/README.md#10-organelle-screen)
  can be run.

* **Population structure is clonal despite an obligate sexual cycle.** Type I, II and III
  are the three dominant clonal lineages across Europe and North America; South American and
  African isolates are far more genetically diverse ("atypical") and don't fit the three-type
  scheme. The clonality is explained by **self-mating**: a single strain can complete both
  micro- and macro-gametogenesis and fertilize itself in the cat gut, so true out-crossing
  only happens when a cat is co-infected with two distinct strains
  ([Wendte et al., 2010](https://doi.org/10.1371/journal.pgen.1001261)). This panel's
  reference, **ME49, is Type II**; the panel also includes Type I (**GT1**, **RH-88**) and
  Type III (**VEG**), alongside several atypical South American / African isolates — so
  lineage-associated loci (see next point) will be well represented.

* **ROP5 — a tandemly duplicated virulence locus whose copy number differs between the
  lineages in this panel.** ROP5 is a cluster of tandemly duplicated, polymorphic rhoptry
  pseudokinases: **6 copies in Type I and Type III, 11 copies in Type II** (this panel's
  reference, ME49, is Type II). Deleting the whole cluster attenuates an otherwise
  highly-virulent strain — it's a major, causal driver of the mouse-virulence differences
  between lineages ([Behnke et al., 2011](https://doi.org/10.1073/pnas.1015338108)). A plain
  presence/absence pangene matrix will read this as ordinary gene gain/loss; it's a
  tandem-array copy-number difference at one locus. `GET_PANGENES` collinearity should help
  place the copies, but review this locus by hand rather than trusting the matrix alone.
  **ROP** (rhoptry), **GRA**
  (dense granule) and **SRS** (surface antigen) are comparably large, fast-evolving secreted
  effector families worth the same scrutiny — telling paralogs from orthologs across such an
  expanded family is where synteny-based calls are least reliable.

* **Haploid, but the transient diploid stage is obligate-in-cat, not
  incidental.** Tachyzoites and bradyzoites (everything outside the cat) are haploid — clean
  presence/absence and copy-number calls, no allele phasing needed. The zygote formed after fertilization in the cat gut is briefly diploid
  before meiosis produces haploid sporozoites; none of the assemblies in this panel are from
  that transient stage.

[↑ Back to top](#analysis-steps)

---

## Analysis Steps

- [01 – Genome Selection & QC](#01--genome-selection--qc)
- [02 – TE Annotation & Clean Up](#02--te-annotation--clean-up)
- [03 – *de novo* Genome Annotation](#03--de-novo-genome-annotation)
- [04 – Protein evidence (InterProScan and PSAURON)](#04--protein-evidence-interproscan-and-psauron)
- [05 – Cross-genome Annotation Integration](#05--cross-genome-annotation-integration)
- [06 – GET_PANGENES](#06--get_pangenes)
- [07 – Post-GET_PANGENES Adjusting and Visualisation](#07--post-get_pangenes-adjusting-and-visualisation)
- [08 – Final GFF](#08--final-gff) (to do)

---

## 01 – Genome Selection & QC


### Genomes selected (15 genomes with available GFF annotations in ToxoDB / VEuPathDB)
(*Info retrieved with Claude - need review)
| Source | Accession / Identifier | Strain / Isolate | Assembly Name | Assembly Level | Total Size (Mb) | Scaffolds / Chromosomes | Scaffold N50 (Mb) | BUSCO Genomic (%) | Protein-Coding Genes | Total Genes | Clade / Lineage & Origin |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ToxoDB** | `GCA_000250965.2` | **ARI** | `TGARI v2` | Scaffold | 64.67 Mb | 2,723 | 2.27 Mb | 98.5% | 9,958 | 10,148 | Clade / Haplogroup XII (USA) |
| **ToxoDB** | `GCA_000256705.2` | **CAST** | `TGCAST v2` | Scaffold | 64.89 Mb | 2,661 | 2.65 Mb | 99.3% | 9,497 | 9,697 | Castells isolate, human congenital (USA) |
| **ToxoDB** | `GCA_000338675.2` | **COUG** | `TGCOUG_v2` | Scaffold | 64.97 Mb | 105 (4,205) | 2.59 Mb | 99.3% | 9,869 | 10,042 | Cougar isolate, Haplogroup XI (Canada) |
| **ToxoDB** | `GCA_000224905.2` | **FOU** | `TGFOU1v02` | Scaffold | 64.50 Mb | 2,869 | 1.44 Mb | 97.0% | 10,117 | 10,297 | Atypical Amazonian clade (French Guiana) |
| **ToxoDB** | `GCA_000325525.2` | **GAB2-2007-GAL-DOM2** | `TGGABGALDOM2_v2.1` | Scaffold | 63.54 Mb | 2,481 | 1.73 Mb | 97.0% | 9,136 | 9,296 | African isolate (Gabon) |
| **ToxoDB** | `GCA_000149715.2` | **GT1** | `TGGT1` | Chromosome (14) | 65.04 Mb | 14 (1,601) | 2.73 Mb | 99.3% | 8,460 | 8,637 | **Type I** (Virulent reference; Goat, USA) |
| **ToxoDB** | `GCA_000224865.2` | **MAS** | `TGMAS1 v2` | Scaffold | 63.29 Mb | 2,180 | 0.98 Mb | 98.3% | 10,005 | 10,176 | Atypical isolate (Massachusetts, USA) |
| **ToxoDB** | `GCF_000006565.2` | **ME49** *(Ref)* | `TGA4` | Chromosome (14) | 65.63 Mb | 14 (2,276) | 4.97 Mb | 99.6% | 8,140 | 8,778 | **Type II** (Primary Reference; Sheep, USA) |
| **ToxoDB** | `GCA_000224885.2` | **p89** | `TGP89A v02` | Scaffold | 64.13 Mb | 2,150 | 1.60 Mb | 98.5% | 9,701 | 9,874 | Haplogroup IX (Pig, USA) |
| **ToxoDB** | `GCA_013099955.1` | **RH-88** | `tgrh88` | Chromosome (13) | 67.02 Mb | 13 (196) | 6.69 Mb | 99.3% | 8,316 | 8,654 | **Type I** (Virulent lab strain; Sabin 1939) |
| **ToxoDB** | `GCA_000224805.2` | **RUB** | `TGRUB v2` | Scaffold | 64.93 Mb | 2,424 | 2.21 Mb | 98.7% | 10,027 | 10,213 | Rubin isolate, Haplogroup V (USA) |
| **ToxoDB** | `GCA_000224825.2` | **TgCatBr9** | `TGCATBR9_v2` | Scaffold | 64.58 Mb | 2,452 | 1.51 Mb | 97.2% | 9,834 | 10,007 | Atypical South American (Cat, Brazil) |
| **ToxoDB** | `GCA_000256725.2` | **TgCatPRC2** | `TGCATPRC2 v2` | Scaffold | 64.16 Mb | 3,060 | 1.49 Mb | 98.9% | 10,121 | 10,300 | Asian isolate (Cat, China) |
| **ToxoDB** | `GCA_000224845.2` | **VAND** | `TGVAND v2` | Scaffold | 64.24 Mb | 2,137 | 1.73 Mb | 99.1% | 9,255 | 9,426 | Vandewalle, Atypical Amazonian (French Guiana) |
| **ToxoDB** | `GCA_000150015.2` | **VEG** | `TGVEG` | Chromosome (14) | 64.47 Mb | 14 (1,340) | 3.77 Mb | 99.3% | 8,410 | 8,563 | **Type III** (Non-virulent in mice; AIDS patient, USA) |

### Sequencing technology & SRA runs

| Strain / Isolate | Assembly Accession | BioProject | BioSample | Sequencing Tech & Platform | Assembly Method | Long-Read / Medium-Read Runs (PacBio / 454) | Short-Read Runs (Illumina / Sanger) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RH-88** | `GCA_013099955.1` | `PRJNA279557` | `SAMN12710240` | PacBio RS II SMRT | HGAP v3 | `SRR11430644` (PacBio SMRT, ~3.08 Gb) | - |
| **ME49** *(Ref)* | `GCF_000006565.2` | `PRJNA28893` | `SAMN00255192` | Roche 454 GS FLX Titanium + Sanger | Celera Assembler v1.92 | `SRR173013`, `SRR173023`, `SRR173027`, `SRR173028` (454) | `SRR350746` (Illumina RNA-seq) |
| **GT1** | `GCA_000149715.2` | `PRJNA16727` | `SAMN02953654` | Sanger + Illumina GA II | Newbler v2.6 | - | `SRR516419` (Illumina WGS), `SRR350745` (RNA-seq), Sanger runs (`SRR9418208-20`) |
| **VEG** | `GCA_000150015.2` | `PRJNA19097` | `SAMN01081685` | Illumina GA II + Sanger | Newbler v2.6 | - | `SRR516406` (Illumina GA II WGS) |
| **ARI** | `GCA_000250965.2` | `PRJNA71477` | `SAMN02953804` | Roche 454 Titanium + Illumina GA II | Newbler v2.5.3 | `SRR350747`, `SRR350748`, `SRR350749` (454 WGS) | `SRR350724` (Illumina GA II) |
| **CAST** | `GCA_000256705.2` | `PRJNA61553` | `SAMN00736208` | Roche 454 Titanium + Illumina GA II | Newbler v2.6 | 454 Titanium (JCVI) | `SRR350735` (Illumina GA II) |
| **COUG** | `GCA_000338675.2` | `PRJNA71479` | `SAMN02953803` | Roche 454 Titanium + Illumina GA II | Newbler v2.6 | `SRR350750`, `SRR350751`, `SRR350752` (454 WGS) | `SRR350733` (Illumina GA II) |
| **FOU** | `GCA_000224905.2` | `PRJNA61561` | `SAMN02953791` | Roche 454 Titanium + Illumina GA II | Newbler v2.5.3 | `SRR118423`, `SRR118424`, `SRR118425` (454 WGS) | `SRR094466` (Illumina GA II) |
| **GAB2-2007-GAL-DOM2** | `GCA_000325525.2` | `PRJNA80767` | `SAMN02953812` | Roche 454 Titanium + Illumina GA II | Newbler v2.6 | `SRR515158`, `SRR515159`, `SRR515972-75` (454) | `SRR516046` (Illumina GA II) |
| **MAS** | `GCA_000224865.2` | `PRJNA61545` | `SAMN02953790` | Roche 454 Titanium + Illumina GA II | Newbler v2.5.3 | `SRR094425`, `SRR094426`, `SRR114860-61`, `SRR187754` (454) | `SRR094469` (Illumina GA II) |
| **p89** | `GCA_000224885.2` | `PRJNA61547` | `SAMN02953792` | Roche 454 Titanium + Illumina GA II | Newbler v2.5.3 | `SRR094411`, `SRR094412`, `SRR173026` (454 WGS) | `SRR094468` (Illumina GA II) |
| **RUB** | `GCA_000224805.2` | `PRJNA61119` | `SAMN02898938` | Roche 454 Titanium + Illumina GA II | Newbler v2.5.3 | `SRR173015`, `SRR173016`, `SRR173017`, `SRR173020`, `SRR173025` (454) | `SRR350720` (Illumina GA II) |
| **TgCatBr9** | `GCA_000224825.2` | `PRJNA61549` | `SAMN02953794` | Roche 454 Titanium + Illumina GA II | Newbler v2.5.3 | `SRR350756`, `SRR350757`, `SRR350758` (454 WGS) | `SRR350728` (Illumina GA II) |
| **TgCatPRC2** | `GCA_000256725.2` | `PRJNA80769` | `SAMN02953811` | Roche 454 Titanium + Illumina GA II | Newbler v2.6 | `SRR515129`, `SRR515130`, `SRR515131`, `SRR515132` (454) | `SRR516208` (Illumina GA II) |
| **VAND** | `GCA_000224845.2` | `PRJNA60839` | `SAMN02898923` | Roche 454 Titanium + Illumina GA II | Newbler v2.5.3 | `SRR173018`, `SRR173019`, `SRR173022`, `SRR173024` (454) | `SRR094467` (Illumina GA II) |

### Genomes excluded (no structural annotation / GFF available in ToxoDB)

| Strain / Isolate | Accession | Reason for Exclusion |
| :--- | :--- | :--- |
| **CtCo5** | Unannotated in ToxoDB (No GFF / 0 genes) |
| **RH 2016** | Unannotated in ToxoDB (No GFF / 0 genes) |
| **strain ME49sc**  | Unannotated scaffold set (No GFF / 0 genes) |
| **TgCATBr5**  | Unannotated in ToxoDB (No GFF / 0 genes) |

### File organization and renaming

```bash
# FASTAs -> genomes/<strain>.fna
cd genomes
for f in ToxoDB-71_Tgondii*_Genome.fasta; do
    n=${f#ToxoDB-71_Tgondii}; n=${n%_Genome.fasta}
    mv "$f" "$n.fna"
done
cd ..
```

```bash
# GFFs -> gff_originals/<strain>.gff3
cd gff_originals
for f in ToxoDB-71_Tgondii*.gff; do
    n=${f#ToxoDB-71_Tgondii}; n=${n%.gff}
    mv "$f" "$n.gff3"
done
cd ..
```
### Header formatting & renaming

```bash
sbatch 01_Genome_Selection_QC/scripts/rename_headers_slurm.sh
```

### Species check (whole-genome ANI vs ME49, `skani`)

```bash
sbatch 01_Genome_Selection_QC/scripts/check_species.slurm.sh
```

All 14 genomes are *T. gondii* — **ANI 98.7–99.7 %** to ME49, aligned fraction 0.93–0.98,
every genome `same_species`. No contamination or wrong-species assemblies. Full table:
[`species_check.tsv`](01_Genome_Selection_QC/species_check/species_check.tsv).

| Strain | ANI to ME49 (%) | | Strain | ANI to ME49 (%) |
| :--- | ---: | --- | :--- | ---: |
| ARI | 99.68 | | MAS | 98.83 |
| VEG | 99.34 | | RH88 | 98.79 |
| TgCatPRC2 | 99.22 | | VAND | 98.75 |
| COUG | 99.15 | | FOU | 98.74 |
| GAB2-2007-GAL-DOM2 | 99.00 | | p89 | 98.74 |
| GT1 | 98.94 | | RUB | 98.74 |
| CAST | 98.85 | | TgCATBr9 | 98.74 |

### Contig size profile

```bash
sbatch 01_Genome_Selection_QC/scripts/contig_size_profile.slurm.sh
```

**34,066 sub-10kb contigs across the panel** — 93–99% of each genome's contig count for every
strain except one. **RH88 is the outlier**: only 62 sub-10kb contigs out of 197 total (32%),
against thousands for every other genome (2,030–4,205, 93–99%). RH88 is a visibly cleaner
assembly than the rest of the panel.

![Contig size distribution by genome](01_Genome_Selection_QC/contig_size_profile/plots/contig_size_profile_by_genome.png)

These small contigs are **not gene-free** — ME49 alone has 504 genes (84
protein_coding/pseudogene) sitting on its 2,218 sub-10kb contigs; every other non-RH88 genome
has 120–309 genes (120–281 protein_coding/pseudogene) on its small contigs too. RH88 has only
5 genes (1 protein_coding/pseudogene) on its 62 small contigs. So this panel can't be treated
as "small = safe to drop by default" — some of this is likely real accessory/fragmented
sequence, not just adapter/contamination junk, and needs the organelle and contamination
screens (and probably manual inspection) before any of it is removed.

**Protein-coding genes that a blanket ≤10kb drop would eliminate** (2,388 total across the
panel, from [`contig_size_profile/small_contig_genes.tsv`](01_Genome_Selection_QC/contig_size_profile/small_contig_genes.tsv)):

| Genome | protein_coding genes | | Genome | protein_coding genes |
| :--- | ---: | --- | :--- | ---: |
| GT1 | 281 | | VAND | 131 |
| FOU | 258 | | GAB2 | 120 |
| COUG | 205 | | VEG | 120 |
| ARI | 187 | | ME49 | 84 |
| TgCATBr9 | 178 | | RH88 | 1 |
| MAS | 176 | | | |
| p89 | 174 | | | |
| RUB | 166 | | | |
| CAST | 159 | | | |
| TgCatPRC2 | 148 | | | |

Of these 2,388, only 289 are the known SRS/ROP/GRA/RON/AP2/MIC virulence-family genes and
~636 look like organelle-genome genes (ribosomal proteins, RNA polymerase, cytochrome —
apicoplast/mitochondrial signatures); the remainder are ordinary genes with no specific
justification for dropping other than contig size alone.

![protein_coding/pseudogene genes by contig size bin](01_Genome_Selection_QC/contig_size_profile/plots/pc_pseudogenes_by_contig_size_bin_by_genome.png)

### Synteny analysis (vs reference ME49)

Whole-genome alignments were generated with `minimap2 -x asm10` and plotted with `plot_dotplot.py`:

```bash
sbatch 01_Genome_Selection_QC/scripts/synteny_vs_ref.slurm.sh
```

| Assembly / Strain | Synteny Dotplot vs ME49 | Assembly / Strain | Synteny Dotplot vs ME49 |
| :--- | :---: | :--- | :---: |
| **ARI** (`GCA_000250965.2`) | ![ARI vs ME49](01_Genome_Selection_QC/synteny/ARI_vs_ME49.png) | **CAST** (`GCA_000256705.2`) | ![CAST vs ME49](01_Genome_Selection_QC/synteny/CAST_vs_ME49.png) |
| **COUG** (`GCA_000338675.2`) | ![COUG vs ME49](01_Genome_Selection_QC/synteny/COUG_vs_ME49.png) | **FOU** (`GCA_000224905.2`) | ![FOU vs ME49](01_Genome_Selection_QC/synteny/FOU_vs_ME49.png) |
| **GAB2-2007-GAL-DOM2** (`GCA_000325525.2`) | ![GAB2-2007-GAL-DOM2 vs ME49](01_Genome_Selection_QC/synteny/GAB2-2007-GAL-DOM2_vs_ME49.png) | **GT1** (`GCA_000149715.2`) | ![GT1 vs ME49](01_Genome_Selection_QC/synteny/GT1_vs_ME49.png) |
| **MAS** (`GCA_000224865.2`) | ![MAS vs ME49](01_Genome_Selection_QC/synteny/MAS_vs_ME49.png) | **p89** (`GCA_000224885.2`) | ![p89 vs ME49](01_Genome_Selection_QC/synteny/p89_vs_ME49.png) |
| **RH-88** (`GCA_013099955.1`) | ![RH88 vs ME49](01_Genome_Selection_QC/synteny/RH88_vs_ME49.png) | **RUB** (`GCA_000224805.2`) | ![RUB vs ME49](01_Genome_Selection_QC/synteny/RUB_vs_ME49.png) |
| **TgCatBr9** (`GCA_000224825.2`) | ![TgCATBr9 vs ME49](01_Genome_Selection_QC/synteny/TgCATBr9_vs_ME49.png) | **TgCatPRC2** (`GCA_000256725.2`) | ![TgCatPRC2 vs ME49](01_Genome_Selection_QC/synteny/TgCatPRC2_vs_ME49.png) |
| **VAND** (`GCA_000224845.2`) | ![VAND vs ME49](01_Genome_Selection_QC/synteny/VAND_vs_ME49.png) | **VEG** (`GCA_000150015.2`) | ![VEG vs ME49](01_Genome_Selection_QC/synteny/VEG_vs_ME49.png) |

#### Quantitative summary

Recomputed from the PAF alignments (alignments ≥ 2 000 bp) with orientation correction (each
query contig is first assigned its own dominant orientation, so only blocks running *against
their own contig* count as inversions — the raw red in a scaffold dot-plot is mostly the
arbitrary orientation of independent scaffolds, not biology):

```bash
python 01_Genome_Selection_QC/scripts/synteny_report.py \
    01_Genome_Selection_QC/synteny --ref-mb 65.63 \
    --md 01_Genome_Selection_QC/synteny/SYNTENY_REPORT.md \
    --tsv 01_Genome_Selection_QC/synteny/SYNTENY_REPORT.tsv
```

Full per-strain detail (every inversion block and cross-chromosome scaffold, with
coordinates): [`SYNTENY_REPORT.md`](01_Genome_Selection_QC/synteny/SYNTENY_REPORT.md) ·
[`SYNTENY_REPORT.tsv`](01_Genome_Selection_QC/synteny/SYNTENY_REPORT.tsv).

| Strain | Lineage / origin | Query pieces (clean 1:1) | ME49 covered | Aln identity¹ | Inversion ≥ 20 kb | Verdict |
| :--- | :--- | ---: | ---: | ---: | :--- | :--- |
| **ARI** | HG XII, USA | 123 (121) | 62.3 Mb (94.9 %) | 91.9 % | – | Collinear, 1:1 |
| **CAST** | Castells, HG XI-like, USA | 120 (116) | 62.2 Mb (94.7 %) | 83.1 % | chrIX ~69 kb | Collinear, 1:1 |
| **COUG** | Cougar, HG XI, Canada | 130 (127) | 62.3 Mb (94.9 %) | 87.0 % | – | Collinear, 1:1 |
| **FOU** | Atypical Amazonian, Fr. Guiana | 197 (186) | 61.7 Mb (94.1 %) | 82.4 % | – | Collinear, 1:1 |
| **GAB2-2007-GAL-DOM2** | African, Gabon | 127 (119) | 62.1 Mb (94.7 %) | 86.8 % | – | Collinear, 1:1 |
| **GT1** | **Type I**, goat, USA | 518 (512) | 62.6 Mb (95.4 %) | 85.1 % | – | Collinear, 1:1 (contiguous asm: 1.7 % rev) |
| **MAS** | Atypical, Massachusetts | 256 (250) | 61.3 Mb (93.4 %) | 83.7 % | – | Collinear, 1:1; 2 scaffolds tile a chromosome junction |
| **RH-88** | **Type I**, lab (Sabin 1939) | 169 (78) | 62.9 Mb (95.8 %) | 83.3 % | chrIV ~515 kb | 13-chromosome assembly — one scaffold joins ME49 chrVIIb + chrVIII |
| **RUB** | Rubin, HG V, USA | 154 (139) | 62.1 Mb (94.6 %) | 82.1 % | chrIX ~69 kb | Collinear, 1:1 |
| **TgCatBr9** | Atypical S. American, Brazil | 164 (153) | 61.9 Mb (94.3 %) | 82.5 % | – | Collinear, 1:1 |
| **TgCatPRC2** | Asian (Chinese 1), China | 165 (155) | 62.1 Mb (94.6 %) | 88.7 % | chrIX ~72 kb | Collinear, 1:1 |
| **VAND** | Atypical Amazonian, Fr. Guiana | 158 (150) | 62.0 Mb (94.5 %) | 83.1 % | chrIX ~69 kb | Collinear, 1:1 |
| **VEG** | **Type III**, non-virulent, USA | 249 (241) | 62.6 Mb (95.4 %) | 88.5 % | – | Collinear, 1:1 (contiguous asm: 1.0 % rev) |
| **p89** | HG IX, pig, USA | 171 (164) | 61.9 Mb (94.4 %) | 82.8 % | – | Collinear, 1:1 |

¹ minimap2 gap-compressed identity, aligned regions only — structurally low because divergent
repeat families partially align; genome-wide **ANI (98.7–99.7 %)** is the real divergence figure.

#### Findings (*Info retrieved with Claude - need review)

- **Universal collinearity.** All 14 dot-plots are a single clean diagonal staircase: 1:1
  correspondence with the 14 ME49 chromosomes, **no translocations and no arm-scale
  inversions** in any lineage (I/II/III, HG V/IX/XI/XII, African, atypical
  Amazonian/South-American/Asian). *T. gondii* has a very stable karyotype.
- **The red in the scaffold plots is orientation, not biology.** After per-contig
  orientation correction the inverted signal is ≈ 0 for every scaffold assembly. The three
  contiguous assemblies give the honest figure: **GT1 1.7 % reverse, VEG 1.0 %, RH88 27 %**
  (RH88 inflated by whole chromosomes assembled in reverse — chrX, chrVI, chrIII, chrIb).
- **One recurrent real inversion:** a **~70 kb inverted block near the end of ME49 chrIX
  (~4.97–5.05 Mb)** in **CAST, RUB, VAND and TgCatPRC2** — an inversion polymorphism shared
  across several lineages; absent from ARI/COUG/GT1/VEG/FOU/GAB2/p89/TgCatBr9.
- **RH-88** carries a **~515 kb inversion at chrIV:2.17–2.69 Mb** (RH88 only) and is
  assembled as **13 chromosomes**, with scaffold **CM023089** joining ME49 **chrVIIb (~5 Mb)
  + chrVIII (~7 Mb)** end to end — treat as an assembly/nomenclature difference to confirm.
- **Recurrent chrIII ↔ chrX segment (~80–85 kb):** the scaffold covering ME49 chrX also
  carries ~80 kb aligning to chrIII in ARI, CAST, COUG, MAS and RH88 → a **segmental
  duplication in the ME49 reference itself**, not a per-strain event.
- **~5–6 % of ME49 is uncovered in every strain** (3.0–4.3 Mb), consistently: subtelomeres,
  tandem gene-family arrays (*SRS/SAG*, *ROP/RON*, *AP2*), and ME49 reference gaps — not
  strain-specific loss. Implication: `GET_PANGENES` collinearity evidence is reliable
  genome-wide; subtelomeric family calls are the least certain.

> **Label note — GAB2.** `species_check.tsv` lists this isolate as `GAB2`, while the synteny
> files and tables use `GAB2-2007-GAL-DOM2`; same genome (`GCA_000325525.2`). The synteny
> folder also holds a redundant `GAB2_vs_ME49.{paf,png}` identical to
> `GAB2-2007-GAL-DOM2_vs_ME49.{paf,png}` — safe to delete.

### Short contig removal — arbitrary ≤10kb cutoff (done)

Decided to drop every contig <10kb from every genome, panel-wide, as a blanket length cutoff
rather than a per-contig evidence check (blastn-based screening was tried and dropped — see
step 02 for why the underlying contamination concern is real). This is an **arbitrary**
cutoff: it knowingly discards the [2,388 protein-coding genes](#contig-size-profile) on those
contigs (including 289 known virulence-family genes), accepted as the cost of a simple,
panel-wide rule.

Script (Tgondii-only, not part of the general pipeline template):
[`01_Genome_Selection_QC/scripts/drop_short_contigs.slurm.sh`](01_Genome_Selection_QC/scripts/drop_short_contigs.slurm.sh).
**Already run** (before step 04). One run does everything: builds the drop list, backs up every
affected genome's FASTA + GFF (untouched copy in
`01_Genome_Selection_QC/backup_before_short_contig_drop/`, the only way back if needed),
writes the gene-cost summary (`01_Genome_Selection_QC/dropped_genes_summary.tsv`), then
rewrites `genomes/`/`gff_originals/` in place — no separate confirmation step. Check: none of
the 3,089 genes listed in `contig_size_profile/small_contig_genes.tsv` (across all 15 genomes)
is present in the GFFs used from step 04 onward.

Command that was run:
```bash
sbatch 01_Genome_Selection_QC/scripts/drop_short_contigs.slurm.sh
```

### Contig redundancy screen (done)

Long-read assemblies can leave small contigs that are really a duplicated slice of a larger contig
(an uncollapsed repeat or a haplotig-style overlap); their genes would be counted twice and inflate the
pangenome. The screen was run on the genomes without contigs below 10 kb; the gene counts below come from an
annotation made before the step 05 build. Its list is applied before the build
([step 05, step 4b](#step-4b-redundant-and-apicoplast-contigs-removed-before-the-build-tgondii-only-done)).

```bash
sbatch 01_Genome_Selection_QC/scripts/contig_redundancy_final.slurm.sh
```

Each genome is aligned against itself (`minimap2 -xasm5 -DP`, the `purge_dups` call). A contig is
**flagged** (`small-redundant`) when it is smaller than 1 Mb and at least 90 % of it aligns, at 95 %
identity or more, to a longer contig of the same assembly. A flag only makes the contig a candidate:
for the contigs that carry genes, every gene is then searched by BLAST in its own assembly, and the
contig is **DROP-OK** when each gene has a copy elsewhere (at least 98 % identity over at least 90 % of the
gene, on an annotated gene) or **REVIEW** when some gene has none. Nothing was removed. Report:
[`REPORT.md`](01_Genome_Selection_QC/contig_redundancy_final/REPORT.md).

#### Per-genome summary

All contigs in this table are at least 10 kb (the shortest is 10,016 bp), because shorter contigs were
removed from every genome in step 01. Contigs are split by length:

- **large**: 1 Mb or more. These are chromosomes or big pieces of them and are never flagged. Several genomes
  have more large contigs than the 14 chromosomes because some chromosomes are split in the assembly.
- **small**: from 10 kb to 1 Mb. Only small contigs can be flagged.

`total Mb` is the size of the whole assembly and `small Mb` the part of it in small contigs. `redundant` and
`unplaced` count the small contigs of that class; the `genes` column beside each is how many annotated genes
sit on them. `small-unplaced` contigs do not map to ME49 and are not duplicated, so they are not candidates.

| Genome | contigs | total Mb | large (≥ 1 Mb) | small (10 kb - 1 Mb) | small Mb | redundant | redundant bp | genes | unplaced | genes |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **ME49** | 47 | 63.1 | 14 | 33 | 0.60 | 6 | 94 kb | 22 | – | – |
| **ARI** | 47 | 63.0 | 21 | 26 | 8.20 | – | – | – | 9 | 98 |
| **CAST** | 56 | 63.2 | 23 | 33 | 6.83 | – | – | – | 21 | 253 |
| **COUG** | 58 | 62.7 | 21 | 37 | 10.23 | – | – | – | 18 | 200 |
| **FOU** | 105 | 62.6 | 23 | 82 | 20.44 | – | – | – | 36 | 595 |
| **GAB2** | 84 | 62.0 | 24 | 60 | 13.37 | – | – | – | 31 | 172 |
| **GT1** | 33 | 60.9 | 14 | 19 | 0.28 | – | – | – | 7 | 9 |
| **MAS** | 143 | 61.8 | 16 | 127 | 33.16 | – | – | – | 34 | 270 |
| **p89** | 93 | 62.8 | 22 | 71 | 18.73 | – | – | – | 37 | 390 |
| **RH88** | 135 | 66.6 | 13 | 122 | 2.67 | 100 | 1724 kb | 89 | 18 | 47 |
| **RUB** | 89 | 63.4 | 21 | 68 | 13.82 | – | – | – | 40 | 262 |
| **TgCATBr9** | 93 | 63.0 | 24 | 69 | 15.15 | – | – | – | 37 | 402 |
| **TgCatPRC2** | 103 | 62.6 | 25 | 78 | 16.60 | – | – | – | 29 | 169 |
| **VAND** | 83 | 62.9 | 24 | 59 | 14.22 | – | – | – | 26 | 125 |
| **VEG** | 30 | 63.1 | 14 | 16 | 0.42 | – | – | – | 14 | 25 |

Only ME49 and RH88 have flagged contigs; the other 13 genomes are clean.

#### Flagged contigs that carry genes

`covered by` is the longer contig that holds the copy that would stay. `REVIEW (n)` is the number of genes
on the contig with no copy elsewhere.

| Genome | Contig | Length | % dup | covered by | Genes | Verdict |
| :--- | :--- | ---: | ---: | :--- | ---: | :--- |
| **ME49** | `KE139140` | 20,306 | 99 % | `KE138866`, `TGME49_chrVI` | 9 | DROP-OK |
| **ME49** | `KE139816` | 17,865 | 98 % | `KE138892`, `KE139822`, `KE139843` | 1 | DROP-OK |
| **ME49** | `KE138868` | 16,277 | 100 % | `KE138866`, `KE139140`, `TGME49_chrVI` | 6 | DROP-OK |
| **ME49** | `KE139842` | 15,749 | 99 % | `KE138892`, `KE139822`, `TGME49_chrII` | 2 | DROP-OK |
| **ME49** | `KE139130` | 12,872 | 100 % | `KE138874`, `TGME49_chrXII` | 3 | REVIEW (1) |
| **ME49** | `KE139841` | 11,018 | 96 % | `KE138892`, `KE139817`, `KE139819` | 1 | REVIEW (1) |
| **RH88** | `JAAUHK010000015` | 42,350 | 97 % | `CM023090`, `CM023091`, `CM023092` | 4 | REVIEW (3) |
| **RH88** | `JAAUHK010000023` | 31,785 | 97 % | `CM023087`, `CM023090`, `CM023092` | 4 | REVIEW (1) |
| **RH88** | `JAAUHK010000025` | 30,311 | 100 % | `CM023094` | 13 | REVIEW (3) |
| **RH88** | `JAAUHK010000012` | 28,810 | 92 % | `CM023087`, `CM023091`, `JAAUHK010000002` | 1 | DROP-OK |
| **RH88** | `JAAUHK010000005` | 28,644 | 100 % | `CM023094`, `JAAUHK010000025` | 9 | REVIEW (2) |
| **RH88** | `JAAUHK010000108` | 27,454 | 100 % | `CM023093`, `JAAUHK010000038`, `JAAUHK010000115` | 1 | DROP-OK |
| **RH88** | `JAAUHK010000010` | 26,922 | 90 % | `CM023087` | 10 | REVIEW (2) |
| **RH88** | `JAAUHK010000009` | 26,667 | 100 % | `CM023090`, `JAAUHK010000006`, `JAAUHK010000026` | 1 | DROP-OK |
| **RH88** | `JAAUHK010000019` | 23,363 | 100 % | `CM023090`, `JAAUHK010000006`, `JAAUHK010000009` | 1 | DROP-OK |
| **RH88** | `JAAUHK010000018` | 22,487 | 96 % | `CM023090`, `CM023091`, `JAAUHK010000002` | 2 | REVIEW (1) |
| **RH88** | `JAAUHK010000020` | 22,198 | 100 % | `CM023087`, `CM023090`, `CM023091` | 1 | DROP-OK |
| **RH88** | `JAAUHK010000031` | 19,995 | 100 % | `CM023094`, `JAAUHK010000005`, `JAAUHK010000025` | 9 | REVIEW (1) |
| **RH88** | `JAAUHK010000028` | 19,262 | 94 % | `CM023082` | 6 | REVIEW (2) |
| **RH88** | `JAAUHK010000069` | 18,672 | 100 % | `CM023090`, `CM023091`, `JAAUHK010000002` | 1 | DROP-OK |
| **RH88** | `JAAUHK010000071` | 17,563 | 100 % | `CM023093`, `JAAUHK010000038`, `JAAUHK010000108` | 1 | DROP-OK |
| **RH88** | `JAAUHK010000072` | 16,787 | 99 % | `CM023086`, `CM023087`, `CM023090` | 3 | DROP-OK |
| **RH88** | `JAAUHK010000039` | 16,651 | 100 % | `CM023085` | 3 | DROP-OK |
| **RH88** | `JAAUHK010000057` | 15,666 | 100 % | `CM023091` | 2 | DROP-OK |
| **RH88** | `JAAUHK010000058` | 15,460 | 99 % | `CM023090`, `CM023092`, `JAAUHK010000002` | 1 | DROP-OK |
| **RH88** | `JAAUHK010000063` | 15,308 | 100 % | `CM023092`, `JAAUHK010000002`, `JAAUHK010000014` | 1 | DROP-OK |
| **RH88** | `JAAUHK010000149` | 15,293 | 100 % | `CM023092`, `JAAUHK010000002`, `JAAUHK010000014` | 1 | REVIEW (1) |
| **RH88** | `JAAUHK010000061` | 15,121 | 100 % | `JAAUHK010000032`, `JAAUHK010000033`, `JAAUHK010000034` | 1 | REVIEW (1) |
| **RH88** | `JAAUHK010000081` | 14,965 | 100 % | `CM023093` | 2 | DROP-OK |
| **RH88** | `JAAUHK010000099` | 14,209 | 100 % | `CM023088` | 6 | DROP-OK |
| **RH88** | `JAAUHK010000030` | 13,384 | 99 % | `JAAUHK010000032`, `JAAUHK010000033`, `JAAUHK010000034` | 3 | REVIEW (3) |
| **RH88** | `JAAUHK010000114` | 13,239 | 99 % | `CM023093` | 2 | DROP-OK |

RH88 has 74 more flagged contigs with **no gene** (1.17 Mb, the largest 34 kb): pure duplicated sequence. With no
gene in the final annotation they add nothing to the pangenome, so there is no need to remove them.

Notes:
- **RH88** REVIEW contigs include genes that look like organelle genes (cytochrome b, cytochrome c oxidase
  subunit III, RNA polymerase B and C2, ORF C and D). They are repeated, or have no copy at 98 % identity,
  and belong with the organelle screen more than with this one.
- **ME49** `KE139130`: one gene (a KRUF family protein) has a 99.9 % identical copy on `KE138874`, but it
  covers only 67 % of the gene. `KE139841`: its one gene (hypothetical protein) has no copy above 98 %.
  ME49 is the reference and its genes form the `main` layer.

#### Contigs just under the cut

The 90 % cut is a line drawn on a continuous value, so contigs at 75-89 % duplicated are probably redundant
too. There are 14 (2 in ME49, 12 in RH88), and 9 of them carry genes (33 in total; the other 5, all in RH88,
have no gene). Their genes have not been checked by BLAST yet.

| Genome | Contig | Length | % dup | covered by | Genes |
| :--- | :--- | ---: | ---: | :--- | ---: |
| **ME49** | `KE138866` | 20,505 | 89 % | `TGME49_chrVI` | 7 |
| **ME49** | `KE139812` | 12,974 | 86 % | `KE139847`, `TGME49_chrVIIa` | 4 |
| **RH88** | `JAAUHK010000004` | 79,187 | 80 % | `CM023083` | 3 |
| **RH88** | `JAAUHK010000011` | 39,556 | 83 % | `CM023086`, `CM023087`, `CM023090` | 4 |
| **RH88** | `JAAUHK010000007` | 39,225 | 82 % | `CM023086`, `CM023087`, `CM023090` | 3 |
| **RH88** | `JAAUHK010000026` | 27,933 | 77 % | `CM023090`, `JAAUHK010000006` | 3 |
| **RH88** | `JAAUHK010000051` | 26,503 | 88 % | `CM023093` | 4 |
| **RH88** | `JAAUHK010000021` | 22,331 | 85 % | `CM023093`, `JAAUHK010000051` | 4 |
| **RH88** | `JAAUHK010000073` | 20,079 | 84 % | `CM023092`, `JAAUHK010000002`, `JAAUHK010000014` | 1 |

#### Decision

Contigs with no gene are not removed: with no gene in the final annotation they add nothing to the pangenome.
All contigs that carry genes are removed, whatever the BLAST verdict: the 32 flagged contigs (DROP-OK and REVIEW)
and the 9 just under the cut, 41 contigs in total (8 in ME49, 33 in RH88, 0.93 Mb, 144 genes), listed by
[`make_removal_list.py`](01_Genome_Selection_QC/scripts/make_removal_list.py) in
[`redundant_contigs_removed.tsv`](01_Genome_Selection_QC/redundant_contigs_removed.tsv). They are removed before the build
([step 05, step 4b](#step-4b-redundant-and-apicoplast-contigs-removed-before-the-build-tgondii-only-done)).


### Organelle screen — apicoplast (done)

Contigs that hold the apicoplast genome are removed with the redundant contigs: their genes are organellar, not
nuclear. The mitochondrion was not screened: the ME49 assembly has no mitochondrial contig to use as a reference. In ME49, 20 of the 43 reference genes with an invalid ORF are on the apicoplast contig.

**The reference.** ToxoDB does not label the apicoplast. ME49 contig `KE138841` was identified as the apicoplast genome
because it is 35,372 bp, the size of the *T. gondii* apicoplast genome (~35 kb), and its 58 genes are the typical
apicoplast set: ribosomal proteins (S3, S4, S5, S7, L2, L11), RNA polymerase subunits, elongation factor Tu and Ycf24
(SufB).

**Finding it in every genome.** `KE138841` is blastn'd against every genome, and a contig is called apicoplast when at
least 90% of the **contig** is covered by the hits. The share of the contig is used, not the share of the apicoplast:
most assemblies collapse the apicoplast inverted repeat into one copy, so their apicoplast contig is ~24 kb and covers
only ~71% of the 35 kb reference, while being 100% apicoplast. Contigs with a smaller share are apicoplast DNA inserted
in the nuclear genome (NUPTs, 0-2% of a nuclear contig at 80-98% identity) and are kept.

**This screen was run locally (on the Mac), not on the cluster:** the same steps as
[`screen_apicoplast.slurm.sh`](01_Genome_Selection_QC/scripts/screen_apicoplast.slurm.sh) (`samtools faidx` of
`KE138841`, one `blastn` per genome, then [`apicoplast_contigs.py`](01_Genome_Selection_QC/scripts/apicoplast_contigs.py)),
typed by hand. The wrapper was written afterwards to repeat it on the cluster and has not been run there yet (it now
lives in step 01 and counts the genes on the GFFs prepared for Liftoff):

```bash
sbatch 01_Genome_Selection_QC/scripts/screen_apicoplast.slurm.sh
```

`apicoplast_contigs.py` writes
[`apicoplast_screen/apicoplast_contigs.tsv`](01_Genome_Selection_QC/apicoplast_screen/apicoplast_contigs.tsv) in the
column layout of `redundant_contigs_removed.tsv`.
[`remove_contigs_before_build.py`](05_Cross-genome_annotation_integration/scripts/remove_contigs_before_build.py) reads both lists
([step 4b](#step-4b-redundant-and-apicoplast-contigs-removed-before-the-build-tgondii-only-done)). Every contig with a hit is in `apicoplast_screen/apicoplast_hits.tsv`.

14 apicoplast contigs in 10 genomes, 93-100% of each contig covered, 99-100% identity:

| Genome | Apicoplast contig(s) | Length (bp) | Genes (before step 05) |
|---|---|---:|---:|
| ME49 | KE138841 | 35,372 | 31 |
| RH88 | CM023094, JAAUHK010000005, JAAUHK010000025, JAAUHK010000031, JAAUHK010000024 | 35,031; 28,644; 30,311; 19,995; 10,279 | 29; 1; 0; 4; 0 |
| CAST | ML130699 | 24,092 | 33 |
| FOU | KN003104 | 24,410 | 29 |
| MAS | KN046792 | 24,390 | 30 |
| RUB | KN042410 | 24,358 | 30 |
| TgCATBr9 | KZ793385.1 | 24,383 | 30 |
| TgCatPRC2 | KQ986331 | 18,165 | 19 |
| VAND | KN044611 | 24,393 | 30 |
| p89 | KN000232 | 24,386 | 29 |

ARI, COUG, GAB2, GT1 and VEG have no apicoplast contig in their assembly, only NUPTs in nuclear contigs.


[↑ Back to top](#analysis-steps)

---

## 02 – TE Annotation & Clean Up

### 02.1 TE Candidate Discovery Pipeline

The TE candidate pipeline was run on the 15 *T. gondii* genomes:

```bash
bash 02_TE_annotation_Clean_Up/slurm/run_pipeline_slurm.sh
```

**Output:** **106 non-redundant candidate TE consensus sequences** across the panel
(`all_MCHelper_curated_sequences_NR.cdhit80.fa`); **25 of those** pass the RepBase/TE-peptide
filter (`final_potential_new_TEs.fa`).

### 02.2 TE-Aid — visual validation of the candidates

Ran TE-Aid (coverage plot / self dot-plot / ORFs / hits to known TE proteins) on the
**unfiltered non-redundant set**, `final_TE_candidates_after_MCHelper/all_MCHelper_curated_sequences_NR.cdhit80.fa`
— not the RepBase/peptide-filtered `final_potential_new_TEs.fa` — to also see the candidates
that filter would have dropped (e.g. solo-LTR-only families) before curating into the final
library:

```bash
sbatch 02_TE_annotation_Clean_Up/scripts/run_te_aid.slurm.sh
```

(`INPUT_FASTA`/`OUTDIR` in the script set to the `all_MCHelper_curated_sequences_NR.cdhit80.fa`
pair, not the default.)

**Output:** `te_aid_all_MCHelper_NR_cdhit80/` — one folder per candidate with its TE-Aid figure,
plus `te_aid_run_summary.tsv` (candidate · genome it ran against · status).

### 02.3 Manual curation of TE candidates

All 106 TE candidates retrieved by the pipeline were manually inspected using the TE-Aid
figures and compared against RepBase/known TE databases.

#### Findings

- **No bona fide *T. gondii* transposable elements were identified.** Consistent with the
  published apicomplexan mobilome literature (Rodriguez & Makalowski, 2022), the curated
  TE library ended up empty of genuine *T. gondii* TEs. 

- **Human L1 LINE elements detected as apparent TE candidates in multiple strains,
  including the reference genome ME49.** **5 of the 106 candidates** (all discovered in the
  ME49 assembly: `rnd-1_family-14/20/31/36/56`) showed the hallmarks of bona fide LINEs
  (TE-Aid coverage profile, ORF structure, hits to known RT domains) — but database comparison
  identified them as **human L1 (LINE-1) consensus sequences**. Their presence in multiple genomes (they are in short contigs <10 kb) including ME49 indicates
  **human host-cell DNA contamination** (most likely from the cell-culture system used to
  propagate the parasite) present in several assemblies of the panel — confirming the panel
  does carry contigs of contamination origin, not just fragmented real sequence.

[↑ Back to top](#analysis-steps)

---

## 03 – *de novo* Genome Annotation

**Not needed.** All 15 strains in the panel already have gene annotation.

[↑ Back to top](#analysis-steps)

---

## 04 – Protein evidence (InterProScan and PSAURON)

### Running InterProScan

`interpro_manifest.tsv` for this panel (15 genomes, `CHUNK_SIZE=1000`): **150 total chunks**.
Submit the array job with:
```bash
mkdir -p interpro/logs
N=$(($(wc -l < interpro/interpro_manifest.tsv) - 1))
sbatch --array=1-${N}%20 04_InterProScan/scripts/interproscan_array_job.slurm.sh
```
(currently 150, but always recomputed from the manifest, not hardcoded - see
[`04_InterProScan/README.md`](https://github.com/VEuPathDB/pangenome-pipeline/blob/main/04_Protein_evidence/README.md) for why).

Protein extraction ran on `gff_originals/` (this species has no `gff_cleaned/`). The array job
**finished**: all 150 chunks completed (each chunk's `.out` ends with
`Finished <genome> chunk <N>`).

### Merging the chunk results

Combines the per-chunk InterProScan output into one lookup table per genome
(`interpro/interpro_lookup/`) and checks completeness:
```bash
sbatch 04_InterProScan/scripts/merge_interpro_job.slurm.sh
```
A protein reported as absent from the chunk output is a `NOTE`, not an error: InterProScan only
writes a row when it finds a hit, so it is a protein with no domain hits. Only a missing chunk
file (`WARNING`) means the results are incomplete.

### Adding the domain evidence to the GFFs

Writes the `InterPro:`/`PFAM:` evidence into the `Dbxref=` of each CDS line, reading
`gff_originals/` (`GFF_INDIR` is set to that in this species' copy of the script) and writing
new GFFs to `gff_with_interpro/` (the input is never modified):
```bash
sbatch 04_InterProScan/scripts/update_interpro_in_gff.slurm.sh
```
`gff_with_interpro/` is the input for step 05.

### PSAURON on every protein

Scores every protein of `interpro/proteins/` (the files extracted for InterProScan, 15 genomes) with PSAURON
(group container `GAQA_psauron.sif`, PSAURON 1.0.8), one array task per genome, into `psauron/<genome>.csv`.
Step 05 reads this folder (`PSAURON_DIR="psauron"`) to decide which genes without an ME49 gene can enter the panel,
and to settle overlaps.
```bash
mkdir -p psauron/logs
N=$(grep -v '^#' genome_order.txt | awk 'NF' | wc -l)
sbatch --array=1-${N} 04_InterProScan/scripts/psauron_array_job.slurm.sh
```
Ran on 2026-10-21: all 15 genomes complete, every protein scored (each log ends with `N scores for N proteins`).
Before that, step 05 scored only its candidates inside the job (`RUN_PSAURON="yes"`,
`basket_annotation/psauron_candidates.csv`).

[↑ Back to top](#analysis-steps)

---

## 05 – Cross-genome Annotation Integration

### Step 1: Native annotation check

Run **once**, after [step 04](#04--protein-evidence-interproscan-and-psauron), on `gff_with_interpro/` (the GFFs with the
domain evidence written in), so that the domain columns and plots are real. Output folder for
this run: `annotation_check_with_interpro/`.
```bash
sbatch 05_Cross-genome_annotation_integration/scripts/analyze_input_gffs_job.sh
```
(`GFF_DIR="gff_with_interpro"` is the script's default; for the run above `OUT_DIR` was set to
`annotation_check_with_interpro`. Full description of every output file:
[general README](https://github.com/VEuPathDB/pangenome-pipeline/blob/main/05_Cross-genome_annotation_integration/README.md#step-1-native-annotation-check).)

**Genes per genome** - 8,000 to 10,000 protein-coding genes per genome, split by whether the
gene carries InterPro/PFAM evidence (56-62% do, in every genome, so no genome stands out
as missing domain annotation). ME49 is the only genome with pseudogenes (24, red sliver on top).

![Protein-coding genes per genome, with and without domain evidence](05_Cross-genome_annotation_integration/annotation_check_with_interpro/01_gene_counts_protein_coding.png)

**Gene types** - every gene category found. Nearly everything is protein-coding; the rest are
non-coding RNA genes (`ncRNA_other`, 144-334 per genome; RH88 has the most at 334), 147 tRNA
genes in VEG only, and 24 pseudogenes in ME49. No genome has unclassified genes.

![Gene categories per genome](05_Cross-genome_annotation_integration/annotation_check_with_interpro/02_gene_biotype_breakdown.png)

**CDS-to-CDS overlaps** - gene pairs whose coding sequences actually overlap, split by strand.
Most genomes have 1-22 pairs; ME49 (33), TgCATBr9 (29) and VEG (27) have the most.
The whole-gene overlap (UTR included) is much larger in ME49 (672 pairs, mostly opposite-strand
UTR-only), which is why the CDS-level count is the one that matters.

![CDS-overlapping gene pairs per genome, by strand](05_Cross-genome_annotation_integration/annotation_check_with_interpro/05_cds_overlap_counts.png)

**Overlap severity** - the same pairs by how much of the smaller gene's CDS is covered:
minor (< 20%), substantial (20-80%), contained (>= 80%). Every genome except RH88 has some
contained pairs; TgCATBr9 and VEG have the most (20 and 16). The pair list with descriptions,
sizes and `has_domain` is `cds_overlapping_pairs.tsv`.

![CDS overlap severity per genome](05_Cross-genome_annotation_integration/annotation_check_with_interpro/06_cds_overlap_severity.png)

Also in that folder: `03_gene_overlap_counts.png` (whole-gene overlap, UTR included),
`04_core_overlap_counts.png` (CDS/exon extent only), and the tables
(`gene_biotype_counts.tsv`, `overlap_counts.tsv`, `feature_attribute_table.tsv`, one
`<genome>_gene_classification.tsv` per genome).

The overlaps are kept (see below); this check is what showed which genes to look at.

### Step 2: Genes removed before Liftoff (kill-list filter, done)

Genes with overlapping CDS are **kept** (not enough evidence to say which are wrong - most look
like gene-model errors, not false genes). The only genes removed are 5 *ME49* protein-coding
genes whose CDS lies entirely inside one of 5 pseudogenes (same strand, no other gene overlaps
those pseudogenes). The pseudogenes are confirmed as correct and are **kept**; the overlapping
genes are removed. Listed in `kill_list_manual.tsv` (project root):

| Removed gene | Description | Overlaps pseudogene | Overlap (bp) |
|---|---|---|---|
| `TGME49_242250` | rhoptry kinase family protein ROP19B | `TGME49_500106` | 1533 |
| `TGME49_224780` | SAG-related sequence SRS40B | `TGME49_500133` | 657 |
| `TGME49_220950` | hypothetical protein | `TGME49_500154` | 1015 |
| `TGME49_321710` | Kinase-like \| domain-containing protein | `TGME49_500317` | 965 |
| `TGME49_321700` | Kinase-like \| domain-containing protein | `TGME49_500405` | 800 |

Removing them (40 GFF lines including their exons/transcripts) is done by
[`remove_genes_from_gff_job.sh`](https://github.com/VEuPathDB/pangenome-pipeline/blob/main/05_Cross-genome_annotation_integration/README.md#step-2-remove-specific-genes-from-the-gffs-optional-manual-kill-list),
reading `gff_with_interpro/` and writing every genome to `gff_curated/` (genomes without an
entry in the list are copied unchanged):
```bash
sbatch 05_Cross-genome_annotation_integration/scripts/remove_genes_from_gff_job.sh
```
`kill_list_manual.tsv` has no header, one gene per line: `genome<TAB>gene_id`
(e.g. `ME49	TGME49_242250`). Run this step **before** "Prepare the GFFs for Liftoff" below.

### Step 3: Prepare the GFFs for Liftoff (done)

[`prepare_for_liftoff_job.sh`](https://github.com/VEuPathDB/pangenome-pipeline/blob/main/05_Cross-genome_annotation_integration/README.md#step-3-prepare-the-gffs-for-liftoff)
reads `gff_curated/` and writes to `gff_for_liftoff/`: genes reduced to their coding sequence
(no UTRs), protein-coding genes and pseudogenes unified to `protein_coding_gene`, and the
non-coding RNA genes (tRNA, rRNA, other ncRNA) removed, so they are neither transferred by Liftoff nor
clustered by `get_pangenes`. This is what goes into Liftoff:
```bash
sbatch 05_Cross-genome_annotation_integration/scripts/prepare_for_liftoff_job.sh
```

Result (`gff_for_liftoff/prepare_for_liftoff_report.tsv`; `liftoff_feature_types.txt` contains
only `protein_coding_gene`). Per genome: transcripts processed, UTR lines deleted, exons
clipped or deleted to the coding extent, genes resized, and total bp cut from gene spans:

| Genome | Transcripts | UTR lines deleted | Exons clipped | Exons deleted | Genes resized | bp trimmed |
|---|---|---|---|---|---|---|
| ME49 | 8115 | 15384 | 13465 | 687 | 7507 | 11047634 |
| ARI | 9771 | 737 | 736 | 1 | 735 | 3608 |
| CAST | 9338 | 545 | 543 | 1 | 543 | 14698 |
| COUG | 9664 | 741 | 740 | 0 | 740 | 2084 |
| FOU | 9859 | 683 | 682 | 1 | 681 | 2783 |
| GAB2 | 9016 | 379 | 378 | 1 | 378 | 4803 |
| GT1 | 8179 | 85 | 83 | 2 | 80 | 6054 |
| MAS | 9829 | 701 | 701 | 0 | 701 | 2316 |
| p89 | 9527 | 581 | 581 | 0 | 581 | 2083 |
| RH88 | 8315 | 46 | 26 | 19 | 22 | 30467 |
| RUB | 9861 | 718 | 716 | 2 | 716 | 2994 |
| TgCATBr9 | 9656 | 586 | 584 | 2 | 581 | 12112 |
| TgCatPRC2 | 9973 | 885 | 884 | 1 | 884 | 2236 |
| VAND | 9124 | 417 | 417 | 0 | 416 | 642 |
| VEG | 8296 | 0 | 89 | 0 | 89 | 1606 |

*ME49* carries by far the most UTR annotation (15,384 lines, 11 Mb removed from gene spans); the
other genomes have only a few hundred UTR lines or fewer. *VEG* has no UTR lines at all, but 89
of its exons extended past the CDS and were clipped.

Step 3 also removes the non-coding genes (tRNA, rRNA, ncRNA) from each genome's own annotation, and retypes the
reference pseudogenes. Genes retyped or removed:

| Genome | Retyped to `protein_coding_gene` | Non-coding genes removed |
|---|---:|---:|
| ME49 | 24 pseudogenes | 194 |
| ARI | | 155 |
| CAST | | 165 |
| COUG | | 148 |
| FOU | | 159 |
| GAB2 | | 144 |
| GT1 | | 149 |
| MAS | | 158 |
| p89 | | 154 |
| RH88 | | 334 |
| RUB | | 161 |
| TgCATBr9 | | 161 |
| TgCatPRC2 | | 153 |
| VAND | | 149 |
| VEG | 8,296 (typed `gene`) | 147 (tRNAs) |

The 24 *ME49* pseudogenes keep `ebi_biotype=pseudogene` on their gene line, so they stay identifiable.

### Step 4: Liftoff, all-against-all (done)

[`liftoff_all_vs_all.sh`](https://github.com/VEuPathDB/pangenome-pipeline/blob/main/05_Cross-genome_annotation_integration/README.md#step-4-liftoff)
lifts every genome's prepared annotation (`gff_for_liftoff/`) onto every other genome's
FASTA (`genomes/`) - 15 genomes, so 210 pairs. Run as one job per source genome:
```bash
mkdir -p liftoff_output/logs
sbatch --array=1-15 05_Cross-genome_annotation_integration/scripts/liftoff_all_vs_all.sh
```
Results go to `liftoff_output/polished/`, job logs to `liftoff_output/logs/`. Resubmitting skips pairs that are already done.

#### ME49 genes transferred with a valid ORF

A ME49 gene that maps well onto the other genomes but has no valid ORF in any of them likely has a wrong
gene model in ME49: the sequence is there, the model does not translate on it. "Maps well" means median
Liftoff coverage and identity ≥ 0.9 over the genomes the gene reached. The ME49 model is never checked on
ME49 itself (there is no ME49→ME49 transfer).

```bash
mkdir -p liftoff_transfer_stats/logs
sbatch 05_Cross-genome_annotation_integration/scripts/liftoff_transfer_stats_job.sh
```

| | |
| :---: | :---: |
| ![ME49 genes by number of genomes with a valid ORF](05_Cross-genome_annotation_integration/liftoff_transfer_stats/ME49_valid_orf_hist.png) | ![ME49 transfers by target genome](05_Cross-genome_annotation_integration/liftoff_transfer_stats/ME49_by_reference.png) |

- **8,047 ME49 genes transferred; 5,740 (71%) have a valid ORF in all 14 genomes.** 3.8% (VEG) to 10.1%
  (FOU) of ME49's genes reach a genome with an invalid ORF.
- **102 genes have a valid ORF in none of the genomes they reached.** 32 of them reached all 14.
- **105 candidate wrong models** (`ME49_candidates.tsv`): transferred to ≥ 11 of the 14 genomes, valid ORF
  in ≤ 20% of them, maps well. Selenoproteins are expected false positives (their in-frame TGA reads as a stop).

### Step 4b: Redundant and apicoplast contigs removed before the build (Tgondii only, done)

The [redundant contigs](#contig-redundancy-screen-done) and the [apicoplast contigs](#organelle-screen--apicoplast-done)
(step 01) were found after Liftoff had run. Removing them from the build's inputs gives the same result as removing them before Liftoff, without
running Liftoff again: no gene on those contigs, no transfer of their genes into the other genomes, and no transfer onto
them. The places those transfers had taken are free again during the build, so the genes that belong there come in.

[`remove_contigs_before_build.py`](05_Cross-genome_annotation_integration/scripts/remove_contigs_before_build.py) reads both lists
(`01_Genome_Selection_QC/redundant_contigs_removed.tsv` and `01_Genome_Selection_QC/apicoplast_screen/apicoplast_contigs.tsv`;
a contig in both is removed once) and
writes new folders: `gff_for_liftoff_nonredundant/`, `liftoff_output/polished_nonredundant/` (a file with nothing to
remove is a link) and `genomes_nonredundant/` (the genomes without those contigs, for `get_pangenes`). Run on the cluster
with its wrapper:
```bash
sbatch 05_Cross-genome_annotation_integration/scripts/remove_contigs_before_build.slurm.sh
```

**52 contigs in 10 genomes** (41 redundant, 14 apicoplast, 3 in both) and **332 genes** of the genomes' own
annotations removed; 2,799 transfers onto those contigs and 474 transfers of their genes removed from the Liftoff
outputs (`contigs_removed_before_build.tsv`; the run wrote it to the old step 09 folder, the wrapper now writes it to
`05_Cross-genome_annotation_integration/`):

| Genome | Contigs | Own genes removed |
|---|---:|---:|
| ME49 | 9 | 49 |
| RH88 | 35 | 86 |
| CAST | 1 | 31 |
| FOU | 1 | 28 |
| MAS | 1 | 28 |
| p89 | 1 | 28 |
| RUB | 1 | 27 |
| TgCATBr9 | 1 | 28 |
| TgCatPRC2 | 1 | 19 |
| VAND | 1 | 8 |

### Step 5: Basket annotation (done)

[`basket_annotation_job.sh`](https://github.com/VEuPathDB/pangenome-pipeline/blob/main/05_Basket_annotation_integration/README.md#step-5-basket-annotation) groups the genes of all genomes that lie at the same
place into baskets, picks each basket's winner (the panel gene), and writes each genome's models. The reference is
ME49.
Run on the cluster on 29 October 2026 (job 1723532), both modes, with the step 04 PSAURON scores and the curators'
list of the genes deleted in ToxoDB 66, from `05_Basket_annotation_integration/scripts_keep_all_genes/` into
`basket_annotation_keep_all_genes/`:
```bash
mkdir -p basket_annotation_keep_all_genes/logs
sbatch --export=ALL,NATIVE_DIR=gff_for_liftoff_nonredundant,TRANSFER_DIR=liftoff_output/polished_nonredundant,DOMAIN_DIR=annotation_check_with_interpro,GENOME_DIR=genomes_nonredundant,OLD_REFERENCE_GFF=ToxoDB-65_TgondiiME49.gff,CURATION_REMOVED_LIST=curation_removed_genes_ME49.txt,ID_PREFIX=Tg,PLOT_LABEL=Toxo 05_Basket_annotation_integration/scripts_keep_all_genes/basket_annotation_job.sh
```

All checks passed, and every gene of every genome's own annotation has a final model or a written reason (gene
fate: 0 genes without a record). The final GFFs of `prefer_panel_model`
(`basket_annotation_keep_all_genes/gff_prefer_panel_model_final/`) go to get_pangenes.

**Panel genes.** 8,365 panel genes: the 8,026 ME49 genes (24 of them pseudogenes) and 339 genes not in the ME49
annotation. 143 copies of a gene in one genome were split off into baskets of their own; 91 of them became panel
genes. 64 panel genes were removed: 52 lost an opposite-strand overlap, 12 are genes the curators deleted.

![Panel genes kept and removed](05_Basket_annotation_integration/basket_annotation_keep_all_genes/plots/Toxo_panel_genes.png)

**Genes per genome.** 7,900 (MAS) to 8,159 (RH88) genes per genome. ME49 has 8,074: its 8,026 genes and 48 genes not in
its annotation.

![Genes per genome: own annotation and final, both modes](05_Basket_annotation_integration/basket_annotation_keep_all_genes/plots/Toxo_gene_counts.png)

**From each genome's own annotation to the final GFF.** Most strains have about 2,000 genes fewer than in their own
annotation, mainly because genes annotated in pieces are replaced by one model (168 to 1,922 pieces per genome; GT1,
VEG and RH88 have the fewest). The other losses: 87 to 286 genes per genome on contigs removed in step 01 (contigs <
10 kb, apicoplast and redundant contigs), 242 to 351 eliminated by the quality rules, and 11 to 24 removed at the end of
step 05. 301 to 454 genes per genome were added where the genome had no gene.

![Each genome from its own annotation to the final GFF](05_Basket_annotation_integration/basket_annotation_keep_all_genes/plots/Toxo_prefer_panel_model_gene_balance.png)

**Genes eliminated by the quality rules.** 4,153 genes in the 14 genomes besides ME49, half of them for PSAURON alone.

![Genes eliminated by the quality rules, by their signs](05_Basket_annotation_integration/basket_annotation_keep_all_genes/plots/Toxo_prefer_panel_model_eliminated_reasons.png)

![PSAURON of the eliminated genes](05_Basket_annotation_integration/basket_annotation_keep_all_genes/plots/Toxo_prefer_panel_model_eliminated_psauron.png)

![PSAURON of the genes eliminated by PSAURON only](05_Basket_annotation_integration/basket_annotation_keep_all_genes/plots/Toxo_prefer_panel_model_eliminated_psauron_only.png)

These three figures were made with
[`gene_fate_job.sh`](https://github.com/VEuPathDB/pangenome-pipeline/blob/main/05_Basket_annotation_integration/README.md#running-it), which redoes the gene
fate and its figures on the results already written, with the step 01 files of the removed contigs:
```bash
export PLOT_LABEL=Toxo
export REMOVED_GENES="contig_size_profile/small_contig_genes.tsv:contig < 10 kb"
export REMOVED_CONTIGS="09_Redundant_Contig_Removal/apicoplast_screen/apicoplast_contigs.tsv:apicoplast contig|09_Redundant_Contig_Removal/redundant_contigs_removed.tsv:redundant contig"
export ORIGINAL_GFF_DIR=gff_originals
sbatch --export=ALL 05_Basket_annotation_integration/scripts_keep_all_genes/gene_fate_job.sh
```

**Where each model comes from.** In `prefer_panel_model`, 6,888 to 7,441 genes per genome take the panel model in place
of the genome's own; 212 to 332 fill a place where the genome had no gene; 130 to 330 take another valid model closer
to the panel model; 28 genes in all are the genome's own gene, back where the panel model could not be placed (e.g.
ARI's SAG2C, swapped with SAG2D by Liftoff).

![Origin of each genome's models, both modes](05_Basket_annotation_integration/basket_annotation_keep_all_genes/plots/Toxo_model_origin.png)

**ORF quality.** 112,596 of the 119,647 genes (94%) have a valid ORF. 4,414 have an ORF broken by the assembly (an N in
the CDS or near a contig end). 2,637 have an invalid ORF not explained by the assembly, 36 of them in ME49. miniprot
repaired 33; the others are mostly frameshifts and internal stops.

![ORF quality per genome, both modes](05_Basket_annotation_integration/basket_annotation_keep_all_genes/plots/Toxo_orf_quality.png)

![Genes with an invalid ORF, by miniprot result](05_Basket_annotation_integration/basket_annotation_keep_all_genes/plots/Toxo_miniprot.png)

**Tandem arrays.** 21 baskets hold a tandem array (e.g. ROP5, SRS and family D genes); 21 extra copies were added.

[↑ Back to top](#analysis-steps)

---

## 06 – GET_PANGENES

`get_pangenes` on the final GFFs of step 05 (`prefer_panel_model`, `basket_annotation_keep_all_genes/`), on the
cluster on 2026-11-12, with the jobs' defaults:
```bash
sbatch --wait 06_GET_PANGENES/scripts/link_for_get_pangenes_basket.slurm.sh
sbatch 06_GET_PANGENES/scripts/run_get_pangenes_basket_job.sh
```
**8,387 pangenes** (`for_get_pangenes_basket_prefer_panel_model_pangenes/`).

[↑ Back to top](#analysis-steps)

---

## 07 – Post-GET_PANGENES Adjusting and Visualisation

The pangenome is fixed where it is safe, looked at, cleaned of the genes found false during curation, and looked at
again ([step 07 README](https://github.com/VEuPathDB/pangenome-pipeline/blob/main/07_Post_GET_PANGENES_adjusting/README.md)). Parts 1–3 and the reference
gene check were run on the cluster on 2026-11-12, right after `get_pangenes`, with the jobs' defaults (step 05 in
`basket_annotation_keep_all_genes/`):
```bash
mkdir -p pangenome_inspection/logs pangenome_fixed/logs pangenome_plots/logs pangenome_explorer/logs reference_check/logs
J1=$(sbatch --parsable 06_GET_PANGENES/scripts/run_get_pangenes_basket_job.sh)
J2=$(sbatch --parsable --dependency=afterok:$J1 07_Post_GET_PANGENES_adjusting/scripts/inspect_pangenome_job.sh)
J3=$(sbatch --parsable --dependency=afterok:$J2 07_Post_GET_PANGENES_adjusting/scripts/fix_pangenome_safe_job.sh)
sbatch --dependency=afterok:$J3 --export=ALL,SET=preliminary 07_Post_GET_PANGENES_adjusting/scripts/plot_all_job.sh
sbatch --dependency=afterok:$J3 --export=ALL,SET=preliminary 07_Post_GET_PANGENES_adjusting/scripts/build_explorer_job.sh
sbatch --dependency=afterok:$J3 07_Post_GET_PANGENES_adjusting/scripts/reference_check_job.sh
```

| | `get_pangenes` | After the safe fix (preliminary) | Final |
|---|---:|---:|---:|
| Pangenes | 8,387 | 8,265 | 8,178 |
| Core (15) | | 7,754 | 7,729 |
| Soft-core (14) | | 71 | 67 |
| Shell (3-13) | | 270 | 248 |
| Cloud (1-2) | | 170 | 134 |

### 1. Inspection

Job 1732101. Tables in `07_Post_GET_PANGENES_adjusting/pangenome_inspection/`.

**Absences** (a pangene with no gene in a genome): 6,361.

| Code | Category | Absences |
|---|---|---:|
| 1a | same gene, in another pangene: can be moved | 748 |
| 1b | same gene, in a pangene shared with the other genomes | 258 |
| 1c | same gene, in no pangene | 7 |
| 2a | another gene in the place, no transfer | 492 |
| 2b | another gene in the place, over a transfer | 309 |
| 3 | transfer not used by step 05 | 551 |
| 4 | place much shorter: likely deletion | 436 |
| 5 | empty place | 760 |
| 6 | contig edge | 2,290 |
| 7 | flanking genes split | 47 |
| 8 | region absent | 463 |

**Pangenes with more than one gene of a strain:** 110. Most hold genes of different panel genes that `get_pangenes`
grouped together (unrelated 29, other 21, copy 20, fragment 18, split 11, no reference 6, tandem copy 5).

### 2. Safe fix

Job 1732102. **87 genes** were moved back to the pangene of their gene, and 37 pangenes left empty disappeared. 661
candidate moves were left alone: 327 genes claimed by more than one pangene, 320 that would have gone in the other
direction of a merge, and 14 chains. Then **50 baskets** that `get_pangenes` had split over several pangenes were joined
(85 pangenes joined into another; `joins.tsv`), e.g. TGME49_310430, split over 7 pangenes and now one pangene of 15
strains. 8,387 → **8,265 pangenes**. 208 split baskets were not joined (`basket_splits_not_joined.tsv`): in 206 a
pangene also holds genes of other baskets, in 2 a strain has two genes of the basket.

The 4,541 absences left, by verdict: absent 1,588, assembly 1,942, copy dropped by step 05 668, elsewhere 343.

**Low-confidence pangenes** (`pangene_lists/pangene_quality.tsv`): 166 have an invalid ORF in more than 50% of their
strains. 68 of them also have a PSAURON score below 0.5, and 116 have no InterPro domain. In 54 the same defect is in
every invalid strain (2 or more), so it is shared (or the model is wrong). 19 more are reference pseudogenes. **Genes in
no pangene:** 18, all with a CDS below 100 bp.

### 3. Preliminary look

Jobs 1732103 (figures) and 1732104 (explorer). Figures: `07_Post_GET_PANGENES_adjusting/pangenome_plots/preliminary/`;
explorer: `07_Post_GET_PANGENES_adjusting/pangenome_explorer/preliminary/explorer_standalone.html`.

![Pangenome and core genome size, preliminary](07_Post_GET_PANGENES_adjusting/pangenome_plots/preliminary/Toxo_preliminary_pancore.png)

The core settles at about 7,750 pangenes (Tettelin 7,764, Willenbrock 7,711).

![Pangene occupancy, preliminary](07_Post_GET_PANGENES_adjusting/pangenome_plots/preliminary/Toxo_preliminary_occupancy.png)

![Singletons per genome, preliminary](07_Post_GET_PANGENES_adjusting/pangenome_plots/preliminary/Toxo_preliminary_singletons.png)

RH88 has the most singletons (55), then ME49 (16) and TgCatPRC2 (8).

![Soft-core pangenes missing per genome, preliminary](07_Post_GET_PANGENES_adjusting/pangenome_plots/preliminary/Toxo_preliminary_softcore_missing.png)

TgCatPRC2 misses 17 of the 71 soft-core pangenes.

![POCS heatmap](07_Post_GET_PANGENES_adjusting/pangenome_plots/preliminary/Toxo_preliminary_POCS_heatmap.png)

![InterPro enrichment, preliminary](07_Post_GET_PANGENES_adjusting/pangenome_plots/preliminary/Toxo_preliminary_domain_enrichment.png)

The cloud is enriched in cytochrome b / cytochrome c oxidase domains (14 of its 92 pangenes with a domain), SRS
domains (23), rhoptry kinases and V-ATPase proteolipid subunits; nothing is enriched in the core. The cytochrome genes
are mitochondrial genes; their copies in the cloud are pieces of mitochondrial DNA in the nuclear assemblies.

The explorer has the VEuPathDB OrthoMCL orthogroup of each pangene's ME49 genes, from the ToxoDB "Genes by Ortholog
Pattern" download for ME49 (`GenesByOrthologPattern_Summary.txt`, the job's `OG_TABLE`), linked by the ME49 gene IDs.
Only the ME49 genes have an orthogroup: the genes of the other strains are not looked up, so a pangene with no ME49
gene has none. Giving every gene of every strain its orthogroup is a step still to do. 8,115 of the 8,265 pangenes have an orthogroup (6,003 orthogroups). 852 orthogroups are in two or
more pangenes, which hold 2,972 pangenes: genes that OrthoMCL groups together but that sit at different places in the
genomes. For example `OG8_0012049` (SRS genes) is in 43 pangenes.

### Reference gene check

The 48 genes the pipeline added to ME49, with RNA-seq (the 84 bigWigs of the VEuPathDB ME49 RNA-seq datasets) and the
ToxoDB intron junctions. Job 1732105, with the job's defaults (this run's folders, the bigWig folder and
`unifiedIntronJunction.gff`); the page is `07_Post_GET_PANGENES_adjusting/reference_check/reference_check.html`.

The 48 genes were curated on the page:

| Decision | Genes |
|---|---:|
| false gene: deleted from every strain | 23 |
| mitochondrial (cytochrome b, cox1, cox3): left out of the pangenome | 17 |
| kept now, to delete from the reference GFF later (decided in [step 08](https://github.com/VEuPathDB/pangenome-pipeline/blob/main/08_Final_GFF/README.md)) | 5 |
| new gene, kept | 3 |

### 4. Removal after curation

Run on 2026-11-13 with the jobs' defaults (`PANGENE_PREFIX=Tg`):
```bash
mkdir -p pangenome_final/logs
J4=$(sbatch --parsable --export=ALL,ACTIONS= 07_Post_GET_PANGENES_adjusting/scripts/remove_panel_genes_job.sh)
sbatch --dependency=afterok:$J4 --export=ALL,SET=final 07_Post_GET_PANGENES_adjusting/scripts/plot_all_job.sh
sbatch --dependency=afterok:$J4 --export=ALL,SET=final 07_Post_GET_PANGENES_adjusting/scripts/build_explorer_job.sh
```

- `genes_to_remove.tsv`: the panel genes of the 23 false genes (reason `curation: false gene (ME49 <gene>)`).
- `genes_to_exclude_from_pangenome.tsv`: 37 mitochondrial panel genes (reason `mito: <description>`), found by domain
  and by name. By domain: besides the 17 ME49 genes, every panel gene of a pangene where a gene has a cytochrome b,
  cox1 or cox3 InterPro domain (IPR005797, IPR005798, IPR016174, IPR027387, IPR036150, IPR000883, IPR023615,
  IPR023616, IPR036927, IPR000298, IPR013833, IPR035973). By name: the four ME49 pseudogenes "cytochrome
  domain-containing protein" (TGME49_500051, TGME49_500088, TGME49_500165, TGME49_500209), short broken copies with
  no domain found, one of which shares pangenes with cytochrome b genes. The PrsW metalloprotease (TGME49_215010),
  which shares a pangene with one cox1 piece, is kept; the nuclear subunits of complex III ("cytochrome b-c1 complex
  subunit") are not mitochondrial genes and are kept.
- `strain_genes_to_remove.tsv`: empty.

**326 genes** were removed (21 to 23 per strain) and **323 genes** left out of the pangenome; 87 pangenes left empty
disappeared (64 of them mitochondrial). 8,265 → **8,178 pangenes**, renamed `Tg_pan_00001` to `Tg_pan_08178` (old
names in `pangenome_final/pangene_ids.tsv`). Tables in `07_Post_GET_PANGENES_adjusting/pangenome_final/`.

### 5. Final look

Figures: `07_Post_GET_PANGENES_adjusting/pangenome_plots/final/`; explorer:
`07_Post_GET_PANGENES_adjusting/pangenome_explorer/final/explorer_standalone.html`.

![Pangenome and core genome size, final](07_Post_GET_PANGENES_adjusting/pangenome_plots/final/Toxo_final_pancore.png)

The core settles at about 7,700 pangenes (Tettelin 7,738, Willenbrock 7,687).

![Pangene occupancy, final](07_Post_GET_PANGENES_adjusting/pangenome_plots/final/Toxo_final_occupancy.png)

![Singletons per genome, final](07_Post_GET_PANGENES_adjusting/pangenome_plots/final/Toxo_final_singletons.png)

RH88 has the most singletons (38), then ME49 (12) and TgCatPRC2 (6).

![Soft-core pangenes missing per genome, final](07_Post_GET_PANGENES_adjusting/pangenome_plots/final/Toxo_final_softcore_missing.png)

TgCatPRC2 misses 17 of the 67 soft-core pangenes.

![InterPro enrichment, final](07_Post_GET_PANGENES_adjusting/pangenome_plots/final/Toxo_final_domain_enrichment.png)

The cytochrome domains are no longer enriched in the cloud. The cloud is enriched in SRS domains (23 of its 58
pangenes with a domain), rhoptry kinases, protein kinases and V-ATPase proteolipid subunits; nothing is enriched in the
core.

8,106 of the 8,178 final pangenes have an orthogroup (6,001 orthogroups; 850 in two or more pangenes).

[↑ Back to top](#analysis-steps) &nbsp;|&nbsp; [Back to Pangenome Pipeline](https://github.com/VEuPathDB/pangenome-pipeline/blob/main/README.md)

---

## 08 – Final GFF

To do. The final annotation (one GFF3 per strain) will be made from the GFFs of step 07; the plan and the
decisions still to make are in the [step 08 README](https://github.com/VEuPathDB/pangenome-pipeline/blob/main/08_Final_GFF/README.md).

[↑ Back to top](#analysis-steps) &nbsp;|&nbsp; [Back to Pangenome Pipeline](https://github.com/VEuPathDB/pangenome-pipeline/blob/main/README.md)
