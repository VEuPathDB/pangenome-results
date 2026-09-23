# *Toxoplasma gondii* Pangenome Analysis

This document tracks the execution, parameters, and results of the pangenome analysis for ***Toxoplasma gondii***, following the steps from the [`pangenome_analysis`](../../README.md) pipeline.

---

## Species Biology & Pangenome Considerations

* **Obligate intracellular apicomplexan, extremely broad host range.** *Toxoplasma gondii*
  infects essentially any warm-blooded animal as an intermediate host (asexual tachyzoite /
  bradyzoite stages); the sexual cycle — and the only stage where genetic recombination can
  occur — happens exclusively in the gut of felids (cats), the definitive host.

* **No transposable elements.** A systematic apicomplexan-wide mobilome screen
  ([Rodriguez & Makalowski, 2022](https://doi.org/10.3390/genes13050887), using
  RepeatModeler, RepeatMasker, LTRpred, MGEScan and TEclass — largely the same toolkit this
  pipeline's [TE candidate pipeline](../../02_TE_annotation_Clean_Up/README.md)
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
  [organelle screen](../../01_Genome_Selection_QC/README.md#10-organelle-screen)
  should expect to find many more, and more scattered, organellar fragments in the nuclear
  assemblies than the single small NUMT seen in the Afum panel — most will be small fragments
  genuinely embedded in nuclear contigs (real nuclear DNA — keep, per the existing
  fragment-vs-whole-organelle-contig rule) rather than a handful of whole-organelle contigs
  to drop, so this step will likely need more manual judgment call volume here than for Afum.
  Also, unlike a fungus, *T. gondii* carries **two organelles to screen** — mitochondrion
  *and* apicoplast (a relict, non-photosynthetic plastid retained by most Apicomplexa) — both
  need their own contig/fragment identified before the
  [organelle screen](../../01_Genome_Selection_QC/README.md#10-organelle-screen)
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
  place the copies, but review this locus by hand rather than trusting the matrix alone —
  same caveat as the efflux-transporter / BGC loci noted for Afum. **ROP** (rhoptry), **GRA**
  (dense granule) and **SRS** (surface antigen) are comparably large, fast-evolving secreted
  effector families worth the same scrutiny — telling paralogs from orthologs across such an
  expanded family is where synteny-based calls are least reliable.

* **Haploid, like Afum, but the transient diploid stage is obligate-in-cat, not
  incidental.** Tachyzoites and bradyzoites (everything outside the cat) are haploid — clean
  presence/absence and copy-number calls, no allele phasing needed, same as the fungal panels
  in this project. The zygote formed after fertilization in the cat gut is briefly diploid
  before meiosis produces haploid sporozoites; none of the assemblies in this panel are from
  that transient stage.

[↑ Back to top](#analysis-steps)

---

## Analysis Steps

- [01 – Genome Selection & QC](#01--genome-selection--qc)
- [02 – TE Annotation & Clean Up](#02--te-annotation--clean-up)
- [03 – *de novo* Genome Annotation](#03--de-novo-genome-annotation)
- [04 – InterProScan](#04--interproscan)
- [05 – Cross-genome Annotation Integration](#05--cross-genome-annotation-integration)
- [06 – GET_PANGENES](#06--get_pangenes)
- [07 – Post-GET_PANGENES Adjusting](#07--post-get_pangenes-adjusting)
- [08 – Pangenome Visualisation](#08--pangenome-visualisation)

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

## 04 – InterProScan

### Running InterProScan

`interpro_manifest.tsv` for this panel (15 genomes, `CHUNK_SIZE=1000`): **150 total chunks**.
Submit the array job with:
```bash
mkdir -p interpro/logs
N=$(($(wc -l < interpro/interpro_manifest.tsv) - 1))
sbatch --array=1-${N}%20 04_InterProScan/scripts/interproscan_array_job.slurm.sh
```
(currently 150, but always recomputed from the manifest, not hardcoded - see
[`04_InterProScan/README.md`](../../04_InterProScan/README.md) for why).

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

[↑ Back to top](#analysis-steps)

---

## 05 – Cross-genome Annotation Integration

### Step 1: Native annotation check

Run **once**, after [step 04](#04--interproscan), on `gff_with_interpro/` (the GFFs with the
domain evidence written in), so that the domain columns and plots are real. Output folder for
this run: `annotation_check_with_interpro/`.
```bash
sbatch 05_Cross-genome_annotation_integration/scripts/analyze_input_gffs_job.sh
```
(`GFF_DIR="gff_with_interpro"` is the script's default; for the run above `OUT_DIR` was set to
`annotation_check_with_interpro`. Full description of every output file:
[general README](../../05_Cross-genome_annotation_integration/README.md#step-1-native-annotation-check).)

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

### Genes removed before Liftoff (kill-list filter)

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
[`remove_genes_from_gff_job.sh`](../../05_Cross-genome_annotation_integration/README.md#step-2-remove-specific-genes-from-the-gffs-optional-manual-kill-list),
reading `gff_with_interpro/` and writing every genome to `gff_curated/` (genomes without an
entry in the list are copied unchanged):
```bash
sbatch 05_Cross-genome_annotation_integration/scripts/remove_genes_from_gff_job.sh
```
`kill_list_manual.tsv` has no header, one gene per line: `genome<TAB>gene_id`
(e.g. `ME49	TGME49_242250`). Run this step **before** "Prepare the GFFs for Liftoff" below.

### Prepare the GFFs for Liftoff

[`prepare_for_liftoff_job.sh`](../../05_Cross-genome_annotation_integration/README.md#step-3-prepare-the-gffs-for-liftoff)
reads `gff_curated/` and writes to `gff_for_liftoff/`: genes reduced to their coding sequence
(no UTRs), protein-coding genes and pseudogenes unified to `protein_coding_gene`, and the
non-coding RNA genes given a different type (`ncRNA_gene`, `tRNA_gene`) so Liftoff - which only
transfers the types in `liftoff_feature_types.txt` - does not copy them onto other genomes. Each
genome keeps its own non-coding genes. This is what goes into Liftoff:
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

Gene types changed (only where the type had to change):

| Genome | From | To | Genes |
|---|---|---|---|
| ME49 | `pseudogene` | `protein_coding_gene` | 24 |
| VEG | `gene` | `protein_coding_gene` | 8296 |
| VEG | `gene` | `tRNA_gene` | 147 |

The 24 *ME49* pseudogenes keep `ebi_biotype=pseudogene` on their gene line, so they stay
identifiable. All other genomes already used `protein_coding_gene`/`ncRNA_gene`, so nothing was
retyped there; their non-coding genes (`ncRNA_gene`, 144-334 per genome) are already outside
the type list Liftoff transfers.

### Liftoff (all-against-all)

[`liftoff_all_vs_all.sh`](../../05_Cross-genome_annotation_integration/README.md#step-4-liftoff)
lifts every genome's prepared annotation (`gff_for_liftoff/`) onto every other genome's
FASTA (`genomes/`) - 15 genomes, so 210 pairs. Run as one job per source genome:
```bash
mkdir -p liftoff_output/logs
sbatch --array=1-15 05_Cross-genome_annotation_integration/scripts/liftoff_all_vs_all.sh
```
Results go to `liftoff_output/polished/`, job logs to `liftoff_output/logs/`. Resubmitting skips pairs that are already done.

### Build each genome's final annotation

[`build_final_annotation_basic.sh`](../../05_Cross-genome_annotation_integration/README.md#step-5-build-each-genomes-final-annotation)
builds one annotation per genome anchored on its own coordinates. The reference is ME49 (first line
of `genome_order.txt`). The layers are the reference's confident transfers (`main`), then the
genome's own annotation from `gff_for_liftoff/` - which is where its non-coding genes come back in -
then the other genomes' good transfers (`good_<genome>`), then everything left (`rescued_<genome>`).
Run after all Liftoff jobs have finished, one job per genome:
```bash
mkdir -p expanded_annotation/logs
sbatch --array=1-15 05_Cross-genome_annotation_integration/scripts/build_final_annotation_basic.sh
```
Results: `expanded_annotation/<genome>_final_annotation.gff`, job logs in `expanded_annotation/logs/`.

[↑ Back to top](#analysis-steps)

---

### Gene analysis (before filtering)

QC on the raw build output, before [step 7](../../05_Cross-genome_annotation_integration/README.md#step-7-extra-copies-and-overlapping-genes)'s
filter runs. Output folder: `final_annotation_qc_plots/`.
```bash
mkdir -p final_annotation_qc_plots/logs
sbatch 05_Cross-genome_annotation_integration/scripts/plot_final_annotation_qc_job.sh
```
(Full description of every output file:
[general README](../../05_Cross-genome_annotation_integration/README.md#step-6-gene-analysis-before-filtering).)

**Gene counts** - each genome's final build has 9,249-9,933 protein-coding genes, well above
its own original annotation (8,000-10,000), since genes are being pulled in from every other
genome too.

![Protein-coding genes: own original annotation vs. this pipeline's build](05_Cross-genome_annotation_integration/final_annotation_qc_plots/01_gene_counts.png)

**Valid-ORF rate.** ME49 sits at only 9.4%, far below every other genome (77-89%) - expected,
not a quality problem: ME49 is the reference, so its `main` genes are used as-is and never go
through Liftoff, meaning they never get the `valid_ORF=` flag Liftoff computes for a transfer.
This metric just doesn't apply to genes that were never transferred.

![% of genes with a valid ORF, per genome](05_Cross-genome_annotation_integration/final_annotation_qc_plots/02_valid_orf_rate.png)

**Extra copies** - RH88 (179) and ME49 (61) stand out; every other genome has 14 or fewer.

![Extra-copy genes, split by valid ORF](05_Cross-genome_annotation_integration/final_annotation_qc_plots/03_extra_copies.png)

**CDS-overlap severity** - 8,222 CDS-overlapping pairs across the panel, split minor/substantial/contained.

![CDS-overlap severity per genome](05_Cross-genome_annotation_integration/final_annotation_qc_plots/04_overlap_severity.png)

**Source composition** - where each genome's final genes came from (`main`/original/`good_*`/`rescued_*`).

![Source composition per genome](05_Cross-genome_annotation_integration/final_annotation_qc_plots/05_source_composition.png)

**Overlap strand** - the same 8,222 pairs, split by strand instead of severity: only **13 are
same-strand** (the ones that "shouldn't normally happen"), the other **8,209 are
opposite-strand**. Same-strand pairs are rare enough on this panel to review by hand, one by one.

![CDS-overlapping pairs per genome, by strand](05_Cross-genome_annotation_integration/final_annotation_qc_plots/06_overlap_strand.png)

**Overlap domain support** - of the 8,222 pairs, only **29 have InterPro/PFAM domain evidence on
both genes**, **5,008 on exactly one**, and **3,185 on neither**. Domain evidence resolves most
of the panel outright (see the refined overlap-resolution rule in the
[general README](../../05_Cross-genome_annotation_integration/README.md#step-7-extra-copies-and-overlapping-genes));
1,166 pairs (954 distinct genes) are left with no domain evidence on either side and still need
a resolution criterion.

![CDS-overlapping pairs per genome, by domain support](05_Cross-genome_annotation_integration/final_annotation_qc_plots/07_overlap_domain_support.png)

**Putting severity and domain support together** - every one of the 8,222 pairs falls into
exactly one of six cases, decided by whether each gene is `main` and whether it carries domain
evidence (full rationale in the
[general README](../../05_Cross-genome_annotation_integration/README.md#step-7-extra-copies-and-overlapping-genes)):

| # | Case | Rule | Pairs |
|---|---|---|---:|
| 1 | `main` × `main` | keep both | 237 |
| 2 | `main` × other, other **has** a domain | keep both | 18 |
| 3 | `main` × other, other has **no** domain | keep only `main` | 6,368 |
| 4 | other × other, **one** has a domain | keep only the one with a domain | 420 |
| 5 | other × other, **both** have a domain | keep both | 13 |
| 6 | other × other, **neither** has a domain | **not yet decided** | 1,166 |

Cases 1-5 (7,056 pairs, 86%) are unambiguous. Case 6 - 1,166 pairs, 954 distinct genes - is the
open problem: 99.6% opposite-strand, 113 `minor` severity, 63.5% "hypothetical protein" on both
sides.

Also in that folder: `summary.tsv` (the numbers behind every plot above), `extra_copy_genes.tsv`
(every extra-copy gene, with description/location/domain/valid-ORF), `cds_overlapping_pairs.tsv`
(every pair above, one row each) and `overlap_domain_summary.tsv` (the domain-support numbers
above, per genome).

[↑ Back to top](#analysis-steps)

### Filtering — 7a pre-filter (done)

Ran [`filter_final_annotation.py`](05_Cross-genome_annotation_integration/scripts/filter_final_annotation.py)
on all 15 genomes (rule details in the
[general README](../../05_Cross-genome_annotation_integration/README.md#7a-pre-filter-drop-unsupported-genes-before-get_pangenes)).
Output: `filtered_annotation/<genome>_final_annotation_filtered.gff` - `gene`-typed, IDs
renumbered `Tg<strain-index>g<00001, ...>`, original ID kept in `original_ID=`.

| Genome | n_original | n_kept | n_removed | % removed |
|---|---:|---:|---:|---:|
| ME49 | 9,425 | 8,880 | 545 | 5.8% |
| ARI | 9,583 | 9,064 | 519 | 5.4% |
| CAST | 9,530 | 8,983 | 547 | 5.7% |
| COUG | 9,728 | 9,186 | 542 | 5.6% |
| FOU | 9,933 | 9,372 | 561 | 5.6% |
| GAB2 | 9,478 | 8,967 | 511 | 5.4% |
| GT1 | 9,249 | 8,731 | 518 | 5.6% |
| MAS | 9,744 | 9,198 | 546 | 5.6% |
| p89 | 9,686 | 9,110 | 576 | 5.9% |
| RH88 | 9,724 | 9,105 | 619 | 6.4% |
| RUB | 9,763 | 9,216 | 547 | 5.6% |
| TgCATBr9 | 9,911 | 9,366 | 545 | 5.5% |
| TgCatPRC2 | 9,747 | 9,234 | 513 | 5.3% |
| VAND | 9,478 | 8,913 | 565 | 6.0% |
| VEG | 9,380 | 8,860 | 520 | 5.5% |

### Filtering — 7b no pre-filter / tag (done)

Ran [`tag_final_annotation.py`](05_Cross-genome_annotation_integration/scripts/tag_final_annotation.py)
on all 15 genomes (rule details in the
[general README](../../05_Cross-genome_annotation_integration/README.md#7b-no-pre-filtering-tag-decide-after-get_pangenes)).
Nothing removed - same `gene`-typing/ID-renumbering as 7a, plus an `intersect=` tag on every
gene recording what it overlaps (`NA`/`with_main`/`with_other_with_domain`/`with_other_no_domain`).
Output: `tagged_annotation/<genome>_final_annotation_tagged.gff` + `<genome>_intersect_pairs.tsv`.

| Genome | n_total | NA | with_main | with_other_with_domain | with_other_no_domain |
|---|---:|---:|---:|---:|---:|
| ME49 | 9,425 | 8,408 | 546 | 2 | 469 |
| ARI | 9,583 | 8,621 | 440 | 25 | 497 |
| CAST | 9,530 | 8,559 | 429 | 24 | 518 |
| COUG | 9,728 | 8,772 | 400 | 37 | 519 |
| FOU | 9,933 | 9,034 | 347 | 47 | 505 |
| GAB2 | 9,478 | 8,519 | 443 | 15 | 501 |
| GT1 | 9,249 | 8,251 | 470 | 20 | 508 |
| MAS | 9,744 | 8,812 | 397 | 36 | 499 |
| p89 | 9,686 | 8,726 | 405 | 40 | 515 |
| RH88 | 9,724 | 8,699 | 493 | 14 | 518 |
| RUB | 9,763 | 8,806 | 391 | 45 | 521 |
| TgCATBr9 | 9,911 | 9,000 | 361 | 43 | 507 |
| TgCatPRC2 | 9,747 | 8,784 | 425 | 30 | 508 |
| VAND | 9,478 | 8,484 | 424 | 35 | 535 |
| VEG | 9,380 | 8,378 | 483 | 15 | 504 |

[↑ Back to top](#analysis-steps)

---

## 06 – GET_PANGENES

[↑ Back to top](#analysis-steps)

---

## 07 – Post-GET_PANGENES Adjusting

[↑ Back to top](#analysis-steps)

---

## 08 – Pangenome Visualisation


---

[↑ Back to top](#analysis-steps) &nbsp;|&nbsp; [Back to Pangenome Pipeline](../../README.md)

