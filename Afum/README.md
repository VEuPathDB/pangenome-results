# *Aspergillus fumigatus* Pangenome Analysis

This document tracks the execution, parameters, and results of the pangenome analysis for ***Aspergillus fumigatus***, following the steps from the [`pangenome_analysis`](../../README.md) pipeline.

---

## Species Biology & Pangenome Considerations

* **Environmental saprobe, opportunistic pathogen.** *Aspergillus fumigatus* is ubiquitous and highly adaptable, with isolates found globally in environmental and clinical niches. It is a decomposer of warm organic matter — and the same traits that let it thrive there make it a pathogen: it grows at body temperature and survives up to ~50 °C, tolerates low oxygen and oxidative stress, scavenges iron efficiently, and releases huge numbers of tiny (2–3 µm) conidia that reach the alveoli. Importantly, none of this represents host specialization — environmental and clinical isolates fall in the same genetic lineages, not separate populations ([Rhodes et al., 2022](https://doi.org/10.1038/s41564-022-01091-2); [Barber et al., 2021](https://doi.org/10.1038/s41564-021-00993-x)). 

* **Compact nuclear genome** - The average genome size is ~29–30 Mb ([Barber et al. 2021](https://pubmed.ncbi.nlm.nih.gov/34819642/); [Lofgren et al. 2022](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3001890)), 8 chromosomes, ~9,500–10,000 protein-coding genes — with no dispensable accessory chromosomes (unlike *Fusarium*, where whole pathogenicity chromosomes are gained and lost, [Ma et al., 2010](https://doi.org/10.1038/nature08850)). 


* Barber et al. (2021) and Lofgren et al. (2022) analysed the **pangenomes** of *A. fumigatus*. The number of genomes analysed was 300 and 260, respectively, mostly genome assemblies generated from Illumina reads. Genomes were annotated with Funannotate. Their strategy for identifying pangenes involved **protein homology searches** that do not separate orthologs and paralogs, so the number of accessory genes is likely underestimated. Moreover, paralog genes can take on distinct functional roles, so they should be considered separately in this kind of analysis. 

* From Barber et al. (2021), the total number of core genes was 7,563, with 3,344 accessory genes (1,043 are cloud – defined as present in less than 5% of the samples). Lofgren et al. (2022) identified 8,866 core genes (they had fewer genomes, so the number of core genes might be higher due to the soft-core genes) and ~6,400 accessory genes (2,109 singletons).

* One of the main concerns regarding *A. fumigatus* is the emergence of azole resistance, a frontline treatment for infections caused by this species. The primary resistance to the drugs is due to mutations in the gene cyp51a, which encodes a target of the triazoles. Barber et al. (2021) analysed 44 strains resistant to triazole and identified that 15 of them contained mutations in cyp51a while 29 were resistant by unknown mechanisms. 

* Interestingly, one of the genetic clusters (cluster 5), which is statistically enriched for clinical isolates, contains significantly more accessory genes than other clusters (Barber et al. 2021) , illustrating how the accessory genome could be a major driver of how the strains adapt, survive and cause disease. 

* Using the get_pangenes approach would help separate paralogs and orthologs and certainly improve the precision of the pan-genes; however, well-assembled, chromosome-level genomes would be necessary for a syntenic ortholog approach and only a limited number are available.

* Recently, [Chown et al (2026)](https://www.biorxiv.org/content/10.64898/2026.04.14.718449v1.full) presented the largest eukaryotic pangenome assembled to date, with 1,000 *A. fumigatus* isolates collected across 34 countries. The authors emphasised that in previous pangenomes, the **paralogs cyp1a and cypb** clustered together. So, they used a different approach to cluster the genes (network-based approach). Using this approach, the authors doubled the number of orthogroups (from 10,005 to 22,198) and indicated that the pangenome could still be open for this species. The authors also identified **85 accessory orthogroups associated with itraconazole**.  Several of these orthogroups encoded the **DUF3435**, a domain present in a special TE superfamily, the Starships. Of the 3304 accessory orthogroups, 1485 show lineage-dependent distribution, while the remaining varied independently of the phylogeny. They found that the lineage-dependent group of accessory genes is notably linked to **Starships and other TEs**. Interestingly, gene turnover in this species is estimated to be very low, with only **2 gains/losses of orthogroups per century**. 

* **Divergence times are loosely constrained.** [Qin et al. 2025](https://www.sciencedirect.com/science/article/pii/S0926669025010155) put some strain splits at ~0.4 mya, but such dates scale with the assumed mutation rate and number of generations per year — neither well known for an environmental fungus — so the estimates carry large uncertainty and differ between studies. What is consistent is that the population is only **shallowly structured** — two weakly differentiated clades ([Rhodes et al. 2022](https://doi.org/10.1038/s41564-022-01091-2)), ~5 genetic clusters ([Barber et al. 2021](https://pubmed.ncbi.nlm.nih.gov/34819642/)) — with substantial **recombination**, so there is no single genome-wide divergence time and lineage boundaries are fuzzy. 

*   **Haploid.** One chromosome set per nucleus (*n* = 8) through the ordinary vegetative and asexual cycle. Hyphal compartments are often multinucleate, but the nuclei are independently haploid — not diploid. This keeps the pangenome clean: gene presence/absence and copy number are read straight from a single genome, with no heterozygous alleles to phase and no allele dropout, unlike in diploid or dikaryotic fungi.

*   **Heterokaryosis.** Hyphal fusion can bring genetically distinct haploid nuclei into one mycelium (heterokaryon) — limited between unlike strains by vegetative incompatibility. Rare fusion of unlike nuclei then yields a transient diploid that haploidises by mitotic recombination and chromosome loss (the parasexual cycle), a non-meiotic route to new genotypes. Its contribution to in-nature genetic exchange is unclear: the population recombination signal is mostly meiotic.
*   **Sex & recombination.** Heterothallic (*MAT1-1* / *MAT1-2*); transient diploid zygotes undergo meiosis to haploid ascospores. Meiotic recombination is the main source of genetic exchange in the population — it is substantial enough that environmental and clinical populations are neither clonal nor panmictic ([Lofgren et al., 2022](https://doi.org/10.1371/journal.pbio.3001890)). The meiotic crossover rate is the highest measured in any eukaryote — ~30 crossovers per chromosome pair, ~0.42 cM/kb — so genetic linkage decays within ~1 kb and clonally-derived haplotypes are broken up quickly ([Auxier et al., 2023](https://doi.org/10.1371/journal.pbio.3002278)). Within-host microevolution during chronic infection looks different: largely clonal (one lineage replicating in place, accumulating mutations) rather than cross-strain recombination ([Engel et al., 2020](https://doi.org/10.1183/23120541.00020-2020)).
*   **Cryptic species.** Section *Fumigati* contains sibling species (*A. lentulus*, *A. udagawae*, *A. viridinutans*, *A. thermomutatus*) that morphology and single-locus barcoding do not resolve ([Lamoth, 2016](https://doi.org/10.3389/fmicb.2016.00683)) — one sibling species mislabelled as *A. fumigatus* inflates the accessory genome. The whole-genome ANI check in step 01 catches these (same species ≥ 99% ANI; cryptic siblings ~90–93%).

*   **Reference strain: Af293.** This pipeline uses **Af293** as the primary reference — the FungiDB standard, 8 chromosomes, extensively curated since [Nierman et al., 2005](https://doi.org/10.1038/nature04332). **A1160 and A1163 belong to the CEA10 lineage**, an unrelated clinical isolate from a different clade of the species. Same species (~99.5 % ANI), but the two lineages differ in chromosome structure and accessory-gene content (detailed in *Af293 vs CEA10* below). Keep their coordinates and annotations separate — do not merge CEA10-lineage assemblies into the Af293 coordinate system.
*   **Multigene families that make orthology hard:** ABC/MFS transporters (efflux, resistance), cytochrome P450s, secreted proteases and CAZymes, cell-wall enzymes (chitin and β-1,3-glucan synthases; [Gow et al., 2017](https://doi.org/10.1128/microbiolspec.FUNK-0035-2016)), hydrophobins (*RodA* rodlet layer), and secondary-metabolite BGCs (gliotoxin, fumagillin, fumitremorgins, siderophores, helvolic acid). The BGCs are clustered, subtelomeric, and chromatin-regulated in ways that vary between isolates ([Colabardini et al., 2022](https://doi.org/10.1371/journal.pgen.1010001)) — a binary orthogroup matrix shatters each cluster into single genes, so analyse clusters in parallel.
*   **Presence/absence is not the whole story.** Four kinds of variation matter — presence/absence, copy number, allelic (e.g. a *cyp51A* substitution), and regulatory/structural (e.g. the *cyp51A* promoter tandem repeat TR34/TR46, or a BGC rearrangement). The matrix captures only the first.

### Af293 vs CEA10 — where the two reference lineages differ

Af293 and CEA10 (the parental isolate of A1163 and A1160) are unrelated clinical isolates
from different clades of *A. fumigatus*. They are firmly the same species — whole-genome
ANI ~99.5 % (step 01), ~98 % of each genome aligns end-to-end, and core genes are >99.3 %
identical at the nucleotide level ([Fedorova et al., 2008](https://doi.org/10.1371/journal.pgen.1000046)).
The differences between them are **concentrated in specific regions, not spread across the genome**:

*   **Assembly completeness.** The 2005 Af293 assembly was a milestone but still has sequence
    gaps and no coverage of centromeres or ribosomal repeats. Long-read resequencing of
    CEA10 (PacBio SMRT + Oxford Nanopore + Illumina) produced a full telomere-to-telomere
    assembly — and a near-complete one for its derivative A1160 — filling those gaps, giving
    an accurate ribosomal-repeat sequence, and resolving the centromeres, which turn out to
    be long transposon arrays on all 8 chromosomes ([Bowyer et al., 2022](https://doi.org/10.1038/s41467-022-32924-7)).

*   **Chromosome structure.** Rearrangements between the two lineages sit almost entirely
    within ~300 kb of the chromosome ends. The largest is a ~500 kb exchange between the
    ends of chromosomes 1 and 6, seen independently in the A1163 draft and in the
    telomere-to-telomere CEA10 assembly ([Fedorova et al., 2008](https://doi.org/10.1371/journal.pgen.1000046);
    [Bowyer et al., 2022](https://doi.org/10.1038/s41467-022-32924-7)). Af293 chromosome 1
    additionally carries a ~400 kb subtelomeric stretch that does not align to A1163
    ([Fedorova et al., 2008](https://doi.org/10.1371/journal.pgen.1000046)) — in our step 02
    TE analysis this region shows Starship hallmarks (to confirm). These
    same breakpoints recur in unrelated isolates across the species, so they look like
    reused fragile sites rather than one-off events ([Bowyer et al., 2022](https://doi.org/10.1038/s41467-022-32924-7)).

*   **Accessory genes are subtelomeric.** Isolate-unique genes are ~1.2 % of Af293 (~140
    genes) and ~2.3 % of A1163 (~220 genes), grouped into ~13 "genomic islands" near the
    chromosome ends. These islands are enriched for pseudogenes and transposons — TE density
    ~4 % versus ~1 % in the conserved core ([Fedorova et al., 2008](https://doi.org/10.1371/journal.pgen.1000046)).
    This is where presence/absence differences between the lineages actually live.

*   **Transposable elements.** TEs (repetitive, mobile DNA) are scattered genome-wide but
    concentrate in two places: the centromeres of all 8 chromosomes, which are long TE
    arrays ([Bowyer et al., 2022](https://doi.org/10.1038/s41467-022-32924-7)), and the
    subtelomeric accessory islands ([Fedorova et al., 2008](https://doi.org/10.1371/journal.pgen.1000046)).
    The subtelomeric regions are where genes are gained, lost, and shuffled, so their exact
    repeat content differs from one lineage to the next.

*   **Secondary-metabolite (BGC) clusters.** Across 66 *A. fumigatus* strains, SM gene
    clusters vary in five ways: whole-cluster presence/absence, gene gain/loss within a
    cluster, loss-of-function point mutations, allelic clusters (different non-homologous
    versions at the same locus), and clusters located at different genomic positions in
    different strains ([Lind et al., 2017](https://doi.org/10.1371/journal.pbio.2003583)).
    Documented cases affect the gliotoxin, fumigaclavine, and helvolic-acid clusters. A
    binary presence/absence matrix breaks each cluster into isolated genes, so BGCs should
    be analysed as whole units.

### Gene loci to watch in this panel

Some loci behave in ways a plain presence/absence matrix will misread — either because they
are engineered lab artefacts, or because recombination and selection make them unusually
variable.

*   **Engineered marker cassettes in the CEA10-lineage assemblies.** Two genomes in this set
    are *derived* laboratory strains, not wild isolates, and their assemblies carry
    non-native sequence ([Bertuzzi et al., 2021](https://doi.org/10.1093/mmy/myaa075)):
    *   **A1163** (`GCA_000150145.1`) is a CEA17 derivative carrying an **ectopically
        integrated *Aspergillus niger* *pyrG*** (`An12g03570`, annotated `AFUB_047540`) —
        a cross-species gene that will look like an accessory gene. Its native *pyrG* (`AFUB_024310`) also carries the CEA17
        loss-of-function point mutation (C→T at +1413, Gln→stop).
    *   **A1160** (`GCA_024220425.1`) is Δ*akuB*^KU80^: the native NHEJ gene *akuB*
        (`AFUB_019720`) is **replaced by a *zeo–pyrG* cassette** — a second copy of
        *A. fumigatus pyrG* plus a bacterial zeocin-resistance gene (*ble*, from
        *Streptoalloteichus hindustanus*) under a synthetic promoter. Expect a duplicated
        *pyrG* (inflated copy number) and a bacterial ORF with no ortholog anywhere else in
        the panel.
    *   **Practical effect:** these show up as A1160/A1163-specific "accessory" genes or as
        copy-number anomalies. Flag `AFUB_047540`, the *ble* ORF, and the extra *pyrG* and
        exclude them from biological interpretation. The wild-type ATCC 46645 and D141 in
        this panel are the *parental* isolates (*akuA*^KU70^-intact), not the AfS
        NHEJ-deletion derivatives, so they are clean.
*   **_cyp51A_ (azole resistance).** *cyp51A* is essential and present in every *A. fumigatus*
    genome, so in the pangenome matrix it is just a core gene marked "present" everywhere —
    the matrix shows nothing interesting about it. All the variation that matters is *inside*
    the gene and its promoter: coding substitutions (L98H, Y121F/T289A) combined with a
    promoter tandem repeat (TR34, TR46). The resistance effect is epistatic — it is the
    *combination* that confers resistance, not the individual changes. High recombination
    assembles these multi-site haplotypes readily: a single cross between a TR34 parent and
    an L98H parent already yields ~0.2 % recombinant TR34/L98H offspring
    ([Auxier et al., 2023](https://doi.org/10.1371/journal.pbio.3002278)). **Do not rely on
    the pangenome matrix for *cyp51A* — analyse it separately, at the level of sequence
    variants and the promoter repeat.**
*   **Efflux transporters.** The ABC/MFS efflux families (e.g. *cdr1B*, *mdr1*-family, and
    the undescribed transporter `AFUA_6G03080` fine-mapped as an acriflavine-resistance
    determinant in [Auxier et al., 2023](https://doi.org/10.1371/journal.pbio.3002278)) are
    large, multi-copy and fast-evolving, so telling true orthologs from paralogs is hard.
    `GET_PANGENES` helps where gene order is conserved, but copies in the subtelomeric /
    TE-rich regions (where much of this family lives) are where collinearity evidence is
    weakest — review those calls by hand.

*   **_MAT_ locus (mating type).** One genomic locus, in a conserved syntenic position
    (flanked by *SLA2* and *APN2*). Each genome carries one of two versions there:
    *MAT1-1-1* (alpha-box gene) or *MAT1-2-1* (HMG-box gene) — unrelated gene families, not
    alleles, with essentially no sequence similarity between them. (Af293 is *MAT1-2*; the
    CEA10 lineage is *MAT1-1*.) **How `GET_PANGENES` will treat this locus is worth checking
    once step 06 runs**: because it relies on sequence similarity as well as collinearity, it
    most likely reports *MAT1-1-1* and *MAT1-2-1* as two separate pangenes, each present in
    only the strains of that mating type (~half the panel). If so, that pattern is the mating
    system, not gene gain/loss — do not interpret it as accessory-genome variation.

*   ***het* genes (heterokaryon incompatibility).** A handful of genes that control whether
    two strains' hyphae can fuse. They sit at ordinary genomic positions but carry unusually
    divergent alleles between strains — balancing selection has kept very different alleles
    circulating for millions of years ([Auxier et al., 2023](https://doi.org/10.1371/journal.pbio.3002278),
    citing earlier work). Expect high sequence divergence at these few genes; it is expected
    biology, not contamination or misassembly.

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
  - [With filtering (7a)](#with-filtering-7a)
  - [No filtering (7b)](#no-filtering-7b)

---

## 01 – Genome Selection & QC

### 01.1 Genomes selected

Figures below are **as downloaded** from NCBI / FungiDB — before the organelle contigs were
stripped (see the *Organelle screen* section below).

| Source | Accession / Identifier | Strain / Isolate | Assembly Name | Assembly Level | Total Size (Mb) | Contigs / Scaffolds | Scaffold N50 (Mb) | GC (%) | Protein-Coding Genes | Origin / Sample Type |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FungiDB** | AF293 (`GCA_000002655.1`) | Af293 | `ASM265v1` | Chromosome | 29.38 Mb | 19 / 8 | 3.95 Mb | 50.0% | 9,630 | Clinical (Invasive Aspergillosis, UK) |
| **FungiDB** | A1160 (`GCA_024220425.1`) | A1160 | `ASM2422042v1` | Chromosome | 29.26 Mb | 10 / 10 | 3.80 Mb | 49.5% | ~9,900 | Clinical / Host-associated (Manchester, UK) |
| **FungiDB** | A1163 (`GCA_000150145.1`) | A1163 | `ASM15014v1` | Scaffold | 29.21 Mb | 223 / 55 | 3.79 Mb | 49.5% | 9,929 | Clinical (CEA10 lineage derivative) |
| **NCBI** | `GCA_040126065.1` | AF100-9B | `UCR_Afum_AF100-9B_1.0` | Complete Genome | 28.30 Mb | 8 / 8 | 3.76 Mb | 49.5% | 9,912 | Clinical (Sputum, Cystic Fibrosis, NH, USA) |
| **NCBI** | `GCA_058970245.1` | eAF1023 | `UCR_Afum_eAF1023_1.0` | Complete Genome | 27.75 Mb | 8 / 8 | 3.76 Mb | 50.0% | 10,025 | Environmental (Wheat, NY, USA; Azole-sens.) |
| **NCBI** | `GCA_040142845.1` | ATCC 42202 | `UCR_Afum_ATCC42202_1.0` | Chromosome | 28.89 Mb | 15 / 15 | 4.71 Mb | 49.5% | 9,960 | Clinical (Sputum, SC, USA) |
| **NCBI** | `GCA_040142945.1` | B5233 | `UCR_Afum_B5233_1.0` | Chromosome | 28.84 Mb | 13 / 13 | 3.95 Mb | 49.5% | 9,933 | Clinical (Pulmonary lesion, MD, USA) |
| **NCBI** | `GCA_040142885.1` | ATCC 13073 | `UCR_Afum_ATCC13073_1.0` | Chromosome | 28.63 Mb | 9 / 9 | 3.91 Mb | 49.5% | 9,892 | Clinical (Pulmonary lesion, MD, USA) |
| **NCBI** | `GCA_058972525.1` | eAF1090 | `UCR_Afum_eAF1090_1.0` | Chromosome | 28.30 Mb | 12 / 12 | 3.89 Mb | 50.0% | 10,230 | Environmental (Apple, PA, USA; Azole-sens.) |
| **NCBI** | `GCA_040142975.1` | H237 | `UCR_Afum_H237_1.0` | Chromosome | 29.20 Mb | 23 / 23 | 3.85 Mb | 49.5% | 10,018 | Clinical (Invasive Aspergillosis, UK) |
| **NCBI** | `GCA_058972625.1` | eAF1436 | `UCR_Afum_eAF1436_1.0` | Chromosome | 28.22 Mb | 10 / 10 | 3.83 Mb | 49.5% | 10,026 | Environmental (Longwood, GA, USA; Azole-res.) |
| **NCBI** | `GCA_040167795.1` | W72310 | `UCR_Afum_W72310_1.0` | Chromosome | 28.15 Mb | 10 / 10 | 3.81 Mb | 50.0% | 10,072 | Clinical (ABPA sputum, NY, USA) |
| **NCBI** | `GCA_040142855.1` | 47-10 (AF221) | `UCR_Afum_47-10_1.0` | Chromosome | 29.16 Mb | 12 / 12 | 3.78 Mb | 49.5% | 10,010 | Environmental (Sawmill wood, New Zealand) |
| **NCBI** | `GCA_040142875.1` | 08-19-02-30 | `UCR_Afum_08-19-02-30_1.0` | Chromosome | 29.06 Mb | 16 / 16 | 3.65 Mb | 49.5% | 10,018 | Environmental (Soil, Netherlands) |
| **NCBI** | `GCA_040142865.1` | 47-4 (AF250) | `UCR_Afum_47-4_1.0` | Chromosome | 29.10 Mb | 26 / 26 | 2.64 Mb | 49.5% | 10,039 | Environmental (Hospital, Manchester, UK) |
| **NCBI** | `GCA_040167805.1` | D141 | `UCR_Afum_D141_1.0` | Chromosome | 28.70 Mb | 28 / 25 | 2.02 Mb | 49.0% | 9,618 | Clinical (Aspergilloma patient, 1980) |
| **NCBI** | `GCA_040142955.1` | ATCC 46645 | `UCR_Afum_ATCC46645_1.0` | Chromosome | 30.53 Mb | 20 / 20 | 1.96 Mb | 49.0% | 10,495 | Clinical (Lung pus / left bronchus, UK) |

**AF293 annotation.** The AF293 GFF used in this panel is the *patched* annotation
(`patched_AfumigatusAf293.gff3`: 10,124 protein-coding genes, 435 of them with new `Afu293_` IDs, and
1,863 genes with changed coordinates compared with the previous version), not the FungiDB download
counted in the table. The only contig eliminated from it is the mitochondrial `mito_A_fumigatus_Af293`
(149 features): the assembly had already lost it in the organelle screen, so only the GFF needed
cleaning. The rest of the GFF is the 8 chromosomes; no small contigs were carried in it.

### 01.2 Sequencing technology & SRA runs

| Strain / Isolate | Assembly Accession | BioProject | BioSample | Sequencing Tech & Platform | Assembly & Polishing Method | Long-Read SRA Run | Short-Read / Polishing Run |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Af293** | `GCA_000002655.1` | `PRJNA131` | `SAMN00115746` | Sanger shotgun WGS | Whole genome shotgun (Nierman et al. 2005) | *N/A (Sanger)* | `SRR068952` (Illumina GA II) |
| **A1160** | `GCA_024220425.1` | `PRJNA838920` | `SAMN28487500` | PacBio SMRT + Oxford Nanopore + Illumina | HGAP v4.0; MaSuRCA v2.0 (Bowyer et al. 2022) | `PRJCA038423` / `PRJNA1129834` | Illumina HiSeq |
| **A1163** | `GCA_000150145.1` | `PRJNA18733` | `SAMN00115744` | Sanger + 454 pyrosequencing | Fedorova et al. 2008 | *N/A (Sanger/454)* | `SRR068950` (Illumina GA II) |
| **AF100-9B** | `GCA_040126065.1` | `PRJNA1078832` | `SAMN40019356` | Oxford Nanopore MinION + Illumina NovaSeq | Canu v2.2; Pilon v1.24 | `SRR28036233` (ONT) | Illumina NovaSeq |
| **ATCC 42202** | `GCA_040142845.1` | `PRJNA1078816` | `SAMN40018943` | Oxford Nanopore MinION + Illumina NextSeq | Canu v2.2; Pilon v1.24 | `SRR28035763` (ONT) | `SRR28035764` (NextSeq) |
| **B5233** | `GCA_040142945.1` | `PRJNA1078823` | `SAMN40018988` | Oxford Nanopore MinION + Illumina NextSeq | Canu v2.2; Pilon v1.24 | `SRR28036164` (ONT) | `SRR28036165` (NextSeq) |
| **ATCC 13073** | `GCA_040142885.1` | `PRJNA1078813` | `SAMN40018940` | Oxford Nanopore MinION + Illumina NextSeq | Canu v2.2; Pilon v1.24 | `SRR28035696` (ONT) | `SRR28035697` (NextSeq) |
| **H237** | `GCA_040142975.1` | `PRJNA1078831` | `SAMN40019230` | Oxford Nanopore MinION + Illumina NextSeq | Canu v2.2; Pilon v1.24 | `SRR28036204` (ONT) | `SRR28036205` (NextSeq) |
| **W72310** | `GCA_040167795.1` | `PRJNA614926` | `SAMN14440150` | Oxford Nanopore MinION + Illumina NovaSeq | Canu v2.2; Pilon v1.24 | `SRR28036234` (ONT) | Illumina NovaSeq |
| **47-10 (AF221)** | `GCA_040142855.1` | `PRJNA1078800` | `SAMN40018856` | Oxford Nanopore MinION + Illumina NextSeq | Canu v2.2; Pilon v1.24 | `SRR28035000` (ONT) | `SRR28035001` (NextSeq) |
| **08-19-02-30** | `GCA_040142875.1` | `PRJNA1078798` | `SAMN40018744` | Oxford Nanopore MinION + Illumina NextSeq | Canu v2.2 | `SRR28034999` (ONT) | Illumina NextSeq |
| **47-4 (AF250)** | `GCA_040142865.1` | `PRJNA1078810` | `SAMN40018895` | Oxford Nanopore MinION + Illumina NextSeq | Canu v2.2; Pilon v1.24 | `SRR28035400` (ONT) | `SRR28035401` (NextSeq) |
| **D141** | `GCA_040167805.1` | `PRJNA1078828` | `SAMN40019052` | Oxford Nanopore MinION + Illumina NextSeq | Canu v2.2; Pilon v1.24 | `SRR28036197` (ONT) | `SRR28036198` (NextSeq) |
| **ATCC 46645** | `GCA_040142955.1` | `PRJNA1078818` | `SAMN40018950` | Oxford Nanopore MinION + Illumina NextSeq | Canu v2.2; Pilon v1.24 | `SRR28035789` (ONT) | Illumina NextSeq |
| **eAF1023** | `GCA_058970245.1` | `PRJNA1399635` | `SAMN54501365` | Oxford Nanopore PromethION + Illumina NextSeq | Celera Assembler v2.2; MaSuRCA POLCA; Medaka v2.1.1 | `SRS27929841` (ONT) | Illumina NextSeq |
| **eAF1090** | `GCA_058972525.1` | `PRJNA1399639` | `SAMN54502638` | Oxford Nanopore PromethION + Illumina NextSeq | Celera Assembler v2.2; MaSuRCA POLCA; Medaka v2.1.1 | `SRS27929861` (ONT) | Illumina NextSeq |
| **eAF1436** | `GCA_058972625.1` | `PRJNA1399637` | `SAMN54502190` | Oxford Nanopore PromethION + Illumina NextSeq | Celera Assembler v2.2; MaSuRCA POLCA; Medaka v2.1.1 | `SRS27929862` (ONT) | Illumina NextSeq |



### 01.3 Header formatting & renaming

```bash
sbatch 01_Genome_Selection_QC/scripts/rename_headers_slurm.sh
```

### 01.4 Species check (whole-genome ANI vs AF293, `skani`)

```bash
sbatch 01_Genome_Selection_QC/scripts/check_species.slurm.sh
```

All 16 genomes are *A. fumigatus* sensu stricto — **ANI 99.2–99.6 %** to AF293, aligned
fraction 0.90–0.97, every genome `same_species`. No cryptic *Fumigati* siblings, no
contamination. Full table: [`species_check.tsv`](01_Genome_Selection_QC/species_check/species_check.tsv).

| Strain | ANI to AF293 (%) | | Strain | ANI to AF293 (%) |
| :--- | ---: | --- | :--- | ---: |
| A1160 | 99.59 | | ATCC 13073 | 99.45 |
| A1163 | 99.59 | | B5233 | 99.45 |
| 47-10 | 99.59 | | ATCC 46645 | 99.39 |
| 47-4 | 99.59 | | D141 | 99.39 |
| ATCC 42202 | 99.57 | | eAF1436 | 99.32 |
| H237 | 99.50 | | eAF1023 | 99.23 |
| 08-19-02-30 | 99.50 | | W72310 | 99.22 |
| AF100-9B | 99.48 | | eAF1090 | 99.22 |

### 01.5 Organelle screen (mitochondrion, `blastn` + `screen_organelles.py`)

The AF293 mitochondrial contig (`mito_A_fumigatus_Af293`, 31,765 bp) was extracted and
`blastn`-ed against every assembly, then each genome classified by how the mitochondrion is
represented:

```bash
sbatch 01_Genome_Selection_QC/scripts/screen_organelles.slurm.sh
```

Full table: [`organelle_screen.tsv`](01_Genome_Selection_QC/organelle_screen/organelle_screen.tsv).

| Call | Genomes | Notes |
| :--- | :--- | :--- |
| Own contig, one copy | **AF293** | reference — mito is its own 31.8 kb contig |
| Own contig, over-length | **AF100-9B** (`GCA_040126065.1`) | mito assembled as a ~2× head-to-tail concatemer on its own 67 kb contig (`CP146368.1`); not a nuclear insertion |
| **Multiple copies — assembly artifact** | **ATCC 42202** (`GCA_040142845.1`) — 6 pure-mito contigs; **47-4 / AF250** (`GCA_040142865.1`) — 4 pure-mito contigs | mito assembled several times over; do not keep as-is |
| Fragment only (NUMT) | **eAF1436** (`GCA_058972625.1`) | one ~5.4 kb piece (17 % of the mito) on a 3.8 Mb nuclear contig — **keep** |
| No assembled mito | A1160, A1163, 47-10, 08-19-02-30, ATCC 13073, B5233, ATCC 46645, H237, W72310, D141, eAF1023, eAF1090 | only ≤123 bp NUMT hits — below the reporting threshold, so **not listed in the TSV** except W72310 (`absent`, no hit at all); the nuclear assemblies simply exclude the organelle |

**Resolution.** The mitochondrion is not handled uniformly across the set — most assemblies
drop it, ATCC 42202 carries it on 6 contigs and 47-4 on 4, and AF100-9B carries a doubled
mito contig. Left as-is, ATCC 42202 and 47-4 would inject the full mito gene set several
times over as spurious "accessory" genes. **Drop the pure-mito contigs below** (the mito
match spans the whole contig) **from the assemblies before annotation (step 03), so
`GET_PANGENES` (step 06) sees nuclear genes only.**

| Genome | Contig to remove | Contig length | Mito DNA on the contig | % of contig |
| :--- | :--- | ---: | ---: | ---: |
| **AF293** | `mito_A_fumigatus_Af293` | 31,765 bp | 31,764 bp | 100 % |
| **AF100-9B** (`GCA_040126065.1`) | `CP146368.1` | 67,192 bp | 67,188 bp | 100 % |
| **ATCC 42202** (`GCA_040142845.1`) | `JBBFMX010000010.1` | 108,077 bp | 108,073 bp | 100 % |
| **ATCC 42202** | `JBBFMX010000011.1` | 69,941 bp | 69,937 bp | 100 % |
| **ATCC 42202** | `JBBFMX010000012.1` | 47,426 bp | 47,423 bp | 100 % |
| **ATCC 42202** | `JBBFMX010000013.1` | 45,115 bp | 45,079 bp | 99.9 % |
| **ATCC 42202** | `JBBFMX010000014.1` | 36,928 bp | 36,926 bp | 100 % |
| **ATCC 42202** | `JBBFMX010000015.1` | 20,838 bp | 20,819 bp | 99.9 % |
| **47-4 / AF250** (`GCA_040142865.1`) | `JBBFMV010000017.1` | 51,966 bp | 51,964 bp | 100 % |
| **47-4 / AF250** | `JBBFMV010000018.1` | 45,492 bp | 45,488 bp | 100 % |
| **47-4 / AF250** | `JBBFMV010000020.1` | 32,521 bp | 32,519 bp | 100 % |
| **47-4 / AF250** | `JBBFMV010000021.1` | 32,012 bp | 32,010 bp | 100 % |

Contigs longer than ~32 kb (the mito length) are tandem mito copies — the mito sequence
tiles the entire contig, so the whole thing is organellar and safe to drop.

**Keep** — mito-derived DNA is a negligible slice of a large nuclear contig (NUMT, not the organelle):

| Genome | Contig | Contig length | Mito DNA on the contig | % of contig |
| :--- | :--- | ---: | ---: | ---: |
| **eAF1436** (`GCA_058972625.1`) | `CM180077.1` | 3,827,124 bp | ~5,420 bp | 0.1 % |
| all others with any hit | (nuclear chromosomes) | 1.8–5.1 Mb | 51–127 bp | ~0 % |

These 12 contigs are in [`01_Genome_Selection_QC/drop_contigs.txt`](01_Genome_Selection_QC/drop_contigs.txt).
They were removed from `genomes/` and `gff_originals/` with the shared
[contig-removal tool](../../01_Genome_Selection_QC/README.md#12-remove-the-unwanted-contigs) —
the wrapper does a dry run, then applies:

```bash
sbatch 01_Genome_Selection_QC/scripts/drop_contigs_slurm.sh
```

Result — nuclear contigs remaining: **AF293** 8, **AF100-9B** 8, **ATCC 42202** 9, **47-4** 22.
GFF feature lines dropped: AF293 149, AF100-9B 1, ATCC 42202 495, 47-4 238. The other 12
genomes were already mito-free and were not touched. (The genome table above still shows the
*as-downloaded* contig counts, which included the organelle contigs.)

### 01.6 Synteny analysis (vs reference AF293)

Whole-genome alignments were generated with `minimap2 -x asm10` and plotted with `plot_dotplot.py`:

```bash
sbatch 01_Genome_Selection_QC/scripts/synteny_vs_ref.slurm.sh
```

| Assembly / Strain | Synteny Dotplot vs AF293 | Assembly / Strain | Synteny Dotplot vs AF293 |
| :--- | :---: | :--- | :---: |
| **A1160** (`GCA_024220425.1`) | ![A1160 vs AF293](01_Genome_Selection_QC/synteny/A1160_vs_AF293.png) | **A1163** (`GCA_000150145.1`) | ![A1163 vs AF293](01_Genome_Selection_QC/synteny/A1163_vs_AF293.png) |
| **ATCC 42202** (`GCA_040142845.1`) | ![GCA_040142845.1 vs AF293](01_Genome_Selection_QC/synteny/GCA_040142845.1_vs_AF293.png) | **47-10** (`GCA_040142855.1`) | ![GCA_040142855.1 vs AF293](01_Genome_Selection_QC/synteny/GCA_040142855.1_vs_AF293.png) |
| **47-4** (`GCA_040142865.1`) | ![GCA_040142865.1 vs AF293](01_Genome_Selection_QC/synteny/GCA_040142865.1_vs_AF293.png) | **08-19-02-30** (`GCA_040142875.1`) | ![GCA_040142875.1 vs AF293](01_Genome_Selection_QC/synteny/GCA_040142875.1_vs_AF293.png) |
| **ATCC 13073** (`GCA_040142885.1`) | ![GCA_040142885.1 vs AF293](01_Genome_Selection_QC/synteny/GCA_040142885.1_vs_AF293.png) | **B5233** (`GCA_040142945.1`) | ![GCA_040142945.1 vs AF293](01_Genome_Selection_QC/synteny/GCA_040142945.1_vs_AF293.png) |
| **ATCC 46645** (`GCA_040142955.1`) | ![GCA_040142955.1 vs AF293](01_Genome_Selection_QC/synteny/GCA_040142955.1_vs_AF293.png) | **H237** (`GCA_040142975.1`) | ![GCA_040142975.1 vs AF293](01_Genome_Selection_QC/synteny/GCA_040142975.1_vs_AF293.png) |
| **W72310** (`GCA_040167795.1`) | ![GCA_040167795.1 vs AF293](01_Genome_Selection_QC/synteny/GCA_040167795.1_vs_AF293.png) | **D141** (`GCA_040167805.1`) | ![GCA_040167805.1 vs AF293](01_Genome_Selection_QC/synteny/GCA_040167805.1_vs_AF293.png) |
| **eAF1023** (`GCA_058970245.1`) | ![GCA_058970245.1 vs AF293](01_Genome_Selection_QC/synteny/GCA_058970245.1_vs_AF293.png) | **eAF1090** (`GCA_058972525.1`) | ![GCA_058972525.1 vs AF293](01_Genome_Selection_QC/synteny/GCA_058972525.1_vs_AF293.png) |
| **eAF1436** (`GCA_058972625.1`) | ![GCA_058972625.1 vs AF293](01_Genome_Selection_QC/synteny/GCA_058972625.1_vs_AF293.png) | **AF100-9B** (`GCA_040126065.1`) | ![GCA_040126065.1 vs AF293](01_Genome_Selection_QC/synteny/GCA_040126065.1_vs_AF293.png) |

#### Quantitative summary

Recomputed from the PAF alignments (alignments ≥ 2 000 bp) with orientation correction (each
query contig is first assigned its own dominant orientation, so only blocks running *against
their own contig* count as inversions — the raw red in a scaffold dot-plot is mostly the
arbitrary orientation of independent scaffolds, not biology):

```bash
python 01_Genome_Selection_QC/scripts/synteny_report.py \
    01_Genome_Selection_QC/synteny --ref-mb 29.38 \
    --md 01_Genome_Selection_QC/synteny/SYNTENY_REPORT.md \
    --tsv 01_Genome_Selection_QC/synteny/SYNTENY_REPORT.tsv
```

Full per-strain detail (every inversion block and cross-chromosome scaffold, with
coordinates): [`SYNTENY_REPORT.md`](01_Genome_Selection_QC/synteny/SYNTENY_REPORT.md) ·
[`SYNTENY_REPORT.tsv`](01_Genome_Selection_QC/synteny/SYNTENY_REPORT.tsv).

| Accession | Strain | Origin | Query pieces (clean 1:1) | AF293 covered | Aln identity¹ | Inversion ≥ 20 kb | Verdict |
| :--- | :--- | :--- | ---: | ---: | ---: | :--- | :--- |
| `GCA_024220425.1` | **A1160** | CEA10-derived, *MAT1-1*, UK | 10 (9) | 28.4 Mb (96.6 %) | 89.4 % | – | Collinear, 1:1 (see CEA10 note) |
| `GCA_000150145.1` | **A1163** | CEA10 lineage | 28 (23) | 28.2 Mb (95.9 %) | 89.9 % | ~33 kb | Collinear, 1:1 (see CEA10 note) |
| `GCA_040126065.1` | **AF100-9B** | Clinical, sputum (CF), NH USA | 9 (9) | 28.1 Mb (95.8 %) | 90.2 % | – | Collinear, 1:1 — no inversions or joins |
| `GCA_040142845.1` | **ATCC 42202** | Clinical, sputum, SC USA | 15 (14) | 28.2 Mb (96.0 %) | 90.3 % | ~32 kb | Collinear, 1:1 |
| `GCA_040142855.1` | **47-10 / AF221** | Env., sawmill, New Zealand | 12 (10) | 28.4 Mb (96.6 %) | 90.1 % | – | Collinear, 1:1 |
| `GCA_040142865.1` | **47-4 / AF250** | Env., hospital, Manchester UK | 26 (20) | 28.4 Mb (96.6 %) | 90.3 % | – | Collinear, 1:1 |
| `GCA_040142875.1` | **08-19-02-30** | Env., soil, Netherlands | 16 (15) | 28.4 Mb (96.7 %) | 89.5 % | ~22 kb | Collinear, 1:1 |
| `GCA_040142885.1` | **ATCC 13073** | Clinical, MD USA | 9 (9) | 28.0 Mb (95.4 %) | 88.1 % | – | Collinear, 1:1 — no inversions or joins |
| `GCA_040142945.1` | **B5233** | Clinical, MD USA | 13 (13) | 28.1 Mb (95.5 %) | 88.1 % | – | Collinear, 1:1 — no inversions or joins |
| `GCA_040142955.1` | **ATCC 46645** | Clinical, UK | 20 (15) | 28.2 Mb (96.1 %) | 86.7 % | chr6 ×2 + chr1, 1.4 Mb | Noisiest assembly — see caveat |
| `GCA_040142975.1` | **H237** | Clinical (IA), UK | 22 (20) | 28.3 Mb (96.3 %) | 89.3 % | chr8 ~453 kb | Collinear, 1:1 + one large inversion |
| `GCA_040167795.1` | **W72310** | Clinical (ABPA), NY USA | 10 (9) | 28.1 Mb (95.8 %) | 85.8 % | **chr2 ~707 kb** + ~26 kb | Collinear, 1:1 + shared chr2 inversion |
| `GCA_040167805.1` | **D141** | Clinical (aspergilloma, 1980) | 25 (20) | 27.7 Mb (94.2 %) | 88.8 % | – | Collinear, 1:1 (lowest coverage) |
| `GCA_058970245.1` | **eAF1023** | Env., wheat, NY USA (azole-S) | 8 (7) | 28.2 Mb (96.0 %) | 85.4 % | **chr2 ~707 kb** + ~26 kb | Collinear, 1:1 + shared chr2 inversion |
| `GCA_058972525.1` | **eAF1090** | Env., apple, PA USA (azole-S) | 12 (10) | 28.3 Mb (96.2 %) | 85.0 % | **chr2 ~707 kb** | Collinear, 1:1 + shared chr2 inversion |
| `GCA_058972625.1` | **eAF1436** | Env., GA USA (azole-R) | 10 (9) | 27.9 Mb (95.0 %) | 88.0 % | **chr2 ~707 kb** | Collinear, 1:1 + shared chr2 inversion |

¹ minimap2 gap-compressed identity, aligned regions only — structurally low because divergent
repeat families partially align; genome-wide **ANI (99.2–99.6 %)** is the real divergence figure.

#### Findings

- **1:1 chromosome correspondence in all 16.** Each query chromosome/large scaffold is a
  single clean diagonal to one AF293 chromosome; 8 chromosomes throughout. **No gross
  translocation, no fusion/fission** — consistent with *A. fumigatus* having no
  dispensable/accessory chromosomes.
- **A shared ~707 kb inversion on chromosome 2 (chr2:0.79–1.50 Mb)** in **W72310, eAF1023,
  eAF1090 and eAF1436** — a clean strand flip flanked by collinear sequence, i.e. a real
  **segregating inversion polymorphism**, not an assembly artifact. Absent from AF293,
  A1160/A1163 and the ATCC/UCR clinical set.
- **Two isolate-specific large inversions:** **H237 chr8:0.67–1.12 Mb (~450 kb)** and
  **ATCC 46645** (chr6 ~800 kb + ~390 kb, chr1 ~210 kb).
- **ATCC 46645 (`GCA_040142955.1`) — caveat.** Noisiest of the set: lowest minimap2
  alignment identity (86.7 %), smallest fraction of the genome alignable to AF293 (0.90 in
  the `skani` check), scaffold N50 ~2 Mb, most inversion signal (1.4 Mb) and several
  scaffold-end cross-chromosome hits. Its whole-genome ANI to AF293 (99.39 %) is still
  firmly *A. fumigatus*, so this is most likely **assembly quality, not biology** — do not
  use it as a structural reference; consider re-checking the assembly.
- **CEA10 lineage (A1160 + A1163) — note.** Both independent CEA10-lineage assemblies (A1160
  is chromosome-grade) reproducibly show the same sub-megabase segments (~50–500 kb) at the
  ends of the scaffolds carrying AF293 chr1 / chr6 / chr7 / chr8 — **lineage-specific
  subtelomeric / segmental divergence**, consistent with the documented Af293-vs-CEA10
  structural differences, *not* a whole-arm reciprocal translocation (no large off-diagonal
  block). Worth a targeted look at the chr1/chr6 junction if BGC / subtelomere content
  matters downstream.
- **Cross-chromosome hits in the chromosome-complete UCR genomes are almost all paralogous**
  (same query region hitting two AF293 chromosomes) → transporter / P450 / subtelomeric
  repeat families, not structural joins.
- **~3.3–5.8 % of AF293 is uncovered** per strain (D141 highest): TE-rich subtelomeres and
  the accessory BGC-bearing regions — where *A. fumigatus* accessory content and assembly
  gaps both concentrate. Implication: `GET_PANGENES` collinearity evidence is reliable
  genome-wide; subtelomeric / BGC calls are the least certain and should be reviewed as
  clusters.

### 01.7 Contig-redundancy screen

Several Canu+Nanopore assemblies carry many more contigs than the 8 chromosomes. Canu can
leave small contigs that are really a duplicated slice of a chromosome (uncollapsed repeat,
haplotig-style overlap, extra rDNA copy); their genes would be counted twice and inflate the
pangenome.

```bash
sbatch 01_Genome_Selection_QC/scripts/contig_redundancy.slurm.sh
```

Self-aligns each genome (`minimap2 -xasm5 -DP`, the `purge_dups` call), combined with the
vs-AF293 PAFs above and `gff_originals/` gene counts. One row per contig, classed
`large` (≥ 1 Mb) / `small-redundant` (≥ 90 % duplicated in a longer contig of the same
assembly) / `small-placed` / `small-unplaced`. Per-contig flagged tables (regenerated on
each run): [`contig_redundancy/REPORT.md`](01_Genome_Selection_QC/contig_redundancy/REPORT.md)
+ `contig_redundancy/<label>.contigs.tsv`.

#### Per-genome summary

Counts per genome. `redundant` / `unplaced` count the flagged **small** contigs; the `genes`
column beside each is how many annotated genes sit on them. `large` > 8 means one chromosome
is split into ≥ 2 pieces each ≥ 1 Mb — fragmentation, which this screen leaves alone.

| Genome | contigs | large | small | redundant | redundant bp | genes | unplaced | genes |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **AF293** | 8 | 8 | 0 | 0 | – | – | 0 | – |
| **A1160** | 10 | 8 | 2 | 0 | – | – | 0 | – |
| **A1163** | 55 | 9 | 46 | 7 | 24 kb | 0 | 34 | 10 |
| **AF100-9B** (`GCA_040126065.1`) | 8 | 8 | 0 | 0 | – | – | 0 | – |
| **ATCC 42202** (`GCA_040142845.1`) | 9 | 8 | 1 | 0 | – | – | 1 | 200 |
| **47-10** (`GCA_040142855.1`) | 12 | 9 | 3 | 0 | – | – | 1 | 58 |
| **47-4** (`GCA_040142865.1`) | 22 | 13 | 9 | 0 | – | – | 5 | 40 |
| **08-19-02-30** (`GCA_040142875.1`) | 16 | 9 | 7 | 2 | 103 kb | 29 | 2 | 206 |
| **ATCC 13073** (`GCA_040142885.1`) | 9 | 8 | 1 | 0 | – | – | 0 | – |
| **B5233** (`GCA_040142945.1`) | 13 | 9 | 4 | 2 | 163 kb | 49 | 0 | – |
| **ATCC 46645** (`GCA_040142955.1`) | 20 | 12 | 8 | 0 | – | – | 3 | 302 |
| **H237** (`GCA_040142975.1`) | 23 | 9 | 14 | 5 | 190 kb | 80 | 3 | 13 |
| **W72310** (`GCA_040167795.1`) | 10 | 9 | 1 | 0 | – | – | 0 | – |
| **D141** (`GCA_040167805.1`) | 25 | 11 | 14 | 0 | – | – | 4 | 56 |
| **eAF1023** (`GCA_058970245.1`) | 8 | 8 | 0 | 0 | – | – | 0 | – |
| **eAF1090** (`GCA_058972525.1`) | 12 | 9 | 3 | 1 | 29 kb | 6 | 1 | 0 |
| **eAF1436** (`GCA_058972625.1`) | 10 | 8 | 2 | 0 | – | – | 2 | 196 |

6 of 16 assemblies are clean, nothing flagged: **AF293**, **A1160**, **AF100-9B**,
**ATCC 13073**, **W72310**, **eAF1023**.

#### Contigs to consider dropping

One row per contig. Each is ≥ 90 % duplicated in a longer contig of its own assembly (or
close to it). For contigs carrying genes, BLASTp the proteins against the retained contigs
first and drop only if every gene has a near-identical copy there. `covered by` = the longer
contig(s) holding the copy that stays — none of them are themselves on this list. A1163
contig names are abbreviated; the full name is `<id>_A_fumigatus_A1163`.

| Genome | Contig | Length | ref chr | % to ref | % dup | covered by | Genes |
| :--- | :--- | ---: | :--- | ---: | ---: | :--- | ---: |
| **B5233** (`GCA_040142945.1`) | `JBBFMZ010000012.1` | 85,746 | chr4 | 100 % | 100 % | `JBBFMZ010000010.1`, `JBBFMZ010000011.1` | 26 |
| **B5233** | `JBBFMZ010000013.1` | 76,895 | chr4 | 99 % | 100 % | `JBBFMZ010000010.1`, `JBBFMZ010000011.1`, `JBBFMZ010000012.1` | 23 |
| **H237** (`GCA_040142975.1`) | `JBBFNB010000013.1` | 54,084 | chr1 | 100 % | 95 % | `JBBFNB010000002.1` | 22 |
| **H237** | `JBBFNB010000014.1` | 45,109 | chr5 | 100 % | 100 % | `JBBFNB010000006.1` | 22 |
| **H237** | `JBBFNB010000015.1` | 36,068 | chr6 | 100 % | 100 % | `CM079250.1`, `JBBFNB010000004.1` | 18 |
| **H237** | `JBBFNB010000017.1` | 33,966 | chr7 | 100 % | 97 % | `CM079251.1` | 13 |
| **H237** | `JBBFNB010000021.1` | 21,017 | chr4 | 100 % | 100 % | `JBBFNB010000010.1`, `JBBFNB010000011.1` | 5 |
| **08-19-02-30** (`GCA_040142875.1`) | `JBBFMU010000012.1` | 58,894 | chr4 | 89 % | 96 % | `JBBFMU010000005.1`, `JBBFMU010000011.1` | 16 |
| **08-19-02-30** | `JBBFMU010000014.1` | 44,513 | chr4 | 92 % | 90 % | `JBBFMU010000005.1`, `JBBFMU010000011.1`, `JBBFMU010000012.1` | 13 |
| **08-19-02-30** | `JBBFMU010000016.1` | 29,130 | chr4 | 39 % | 85 % | `JBBFMU010000005.1`, `JBBFMU010000011.1`, `JBBFMU010000012.1` | 11 |
| **eAF1090** (`GCA_058972525.1`) | `JBVBAJ010000012.1` | 28,793 | – | 0 % | 100 % | `CM180068.1`, `CM180070.1`, `CM180071.1` | 6 |
| **A1163** | `scf_000016` | 11,690 | chr7 | 100 % | 100 % | `scf_000008` | 0 |
| **A1163** | `scf_000020` | 5,007 | – | 0 % | 100 % | `scf_000007` | 0 |
| **A1163** | `scf_000032` | 2,593 | – | 0 % | 100 % | `scf_000007`, `scf_000009` | 0 |
| **A1163** | `scf_000041` | 1,342 | chr4 | 95 % | 96 % | `scf_000011` | 0 |
| **A1163** | `scf_000049` | 1,175 | chr4 | 98 % | 100 % | `scf_000011` | 0 |
| **A1163** | `scf_000050` | 1,174 | chr4 | 98 % | 100 % | `scf_000011` | 0 |
| **A1163** | `scf_000053` | 1,136 | chr4 | 99 % | 100 % | `scf_000011` | 0 |

Notes:
- **B5233** `JBBFMZ010000013.1` lists `JBBFMZ010000012.1` among its `covered by`, and `…012.1`
  is itself on the list — both still trace back to the chr4 contigs `…010.1`/`…011.1`, so
  dropping both is safe.
- **08-19-02-30** `JBBFMU010000016.1` is technically `small-unplaced` (39 % to AF293, 85 %
  duplicated — just under the 90 % cutoff). Its 11 genes were not covered by the
  `check_redundant_genes` run (that only does `small-redundant`). It's on the drop list and
  has been applied — the post-drop re-run of this screen confirms it's gone (08-19-02-30 now
  shows 1 flagged `small-unplaced` contig, down from 2).


Confirm the gene-carrying rows before dropping — for every gene on a flagged contig,
[`check_redundant_genes.py`](01_Genome_Selection_QC/scripts/check_redundant_genes.py) cuts its
span, `blastn`s it against the whole assembly, keeps the best hit off its own contig, and
checks it lands on an annotated gene:

```bash
sbatch 01_Genome_Selection_QC/scripts/check_redundant_genes.slurm.sh
```

Per genome: `contig_redundancy/<label>.redundant_genes.{tsv,fa,blast.tsv}` — the per-gene
table (with the GFF `product` / `description` of the gene and of its match elsewhere), the
extracted gene sequences, and the raw blastn hits. Per-contig verdict: **DROP-OK** (every
gene has a ≥ 98 % / ≥ 90 %-coverage copy on an annotated gene elsewhere) or **REVIEW** (the
log lists the unconfirmed genes and what they are).

| Genome | DROP-OK | REVIEW (unconfirmed genes) |
| :--- | :--- | :--- |
| **08-19-02-30** | `JBBFMU010000012.1` | `JBBFMU010000014.1` (2) |
| **B5233** | `JBBFMZ010000012.1` | `JBBFMZ010000013.1` (1) |
| **H237** | `JBBFNB010000014.1`, `…017.1`, `…021.1` | `JBBFNB010000013.1` (1), `…015.1` (2) |
| **eAF1090** | – | `JBVBAJ010000012.1` (2) |

The REVIEW rows are 1–2 genes each — read their descriptions in the TSV before deciding
(a real single-copy gene → keep the contig; a mapping artefact at a repeat edge → still drop).

#### Gene-rich unplaced contigs — inspect, likely keep

Not redundancy: `small-unplaced` contigs that don't map to AF293 but carry many genes — one
~0.5–0.6 Mb / ~180–200-gene contig in each of **ATCC 42202**, **ATCC 46645** (3 contigs,
302 genes), **eAF1436**, **08-19-02-30**; smaller ones in **47-10**, **47-4**, **D141**. They
align only 10–20 % to AF293, consistent with the ~3–6 % of AF293 left uncovered in the
synteny step and with CEA10-lineage subtelomeric divergence. Most likely real accessory /
divergent subtelomeric sequence — keep, but BLAST vs `nt` first to rule out contamination.

#### Decision

**18 contigs** are dropped — B5233 ×2, H237 ×5, 08-19-02-30 ×3, eAF1090 ×1, A1163 ×7. 17 are
`small-redundant` (either DROP-OK, or their 1–2 REVIEW genes inspected and confirmed as
duplicates/artefacts); the 18th, 08-19-02-30 `JBBFMU010000016.1`, is `small-unplaced` at 85 %
duplicated (11 genes, not covered by `check_redundant_genes`). All 18 are applied — a
post-drop re-run of the contig-redundancy screen
([`contig_redundancy/`](01_Genome_Selection_QC/contig_redundancy/REPORT.md)) confirms zero
`small-redundant` contigs remain flagged anywhere in the panel.

Added to the cumulative
[`drop_contigs.txt`](01_Genome_Selection_QC/drop_contigs.txt) manifest (12 organelle +
18 redundant). Re-running is safe — `drop_contigs.py` skips contigs already gone from both
the FASTA and the GFF:

```bash
sbatch 01_Genome_Selection_QC/scripts/drop_contigs_slurm.sh
```

**Not dropped:** the `small-unplaced` gene-rich contigs (ATCC 42202, ATCC 46645, eAF1436,
47-10, 47-4, D141 — kept as likely accessory content).

### 01.8 Contig size profile

> This screen normally runs *before* organelle/redundancy filtering (the organelle screen and
> contig-redundancy screen above) — for Afum
> it was added after that filtering had already happened, so the numbers below are for the
> **already-cleaned** assembly (organelle + redundant contigs already removed), not the raw
> download.

```bash
sbatch 01_Genome_Selection_QC/scripts/contig_size_profile.slurm.sh
```

Out of 17 genomes, only **2** have any contig under 10 kb left: **A1163** (32 contigs, but
only 1 gene total on them) and **GCA_040142865.1** (3 contigs, 3 genes). Every other genome
has zero. 36 sub-10kb contigs across the whole panel, carrying 4 genes combined — consistent
with the organelle/redundancy cleanup already having removed the residual junk, not evidence
of further contamination worth chasing.

| | |
| :---: | :---: |
| ![Contig size distribution by genome](01_Genome_Selection_QC/contig_size_profile/plots/contig_size_profile_by_genome.png) |

Genes overwhelmingly sit on chromosome-scale (≥1 Mb) contigs across the panel, as expected;
the small secondary bump on 100 kb–1 Mb contigs is the fragmented assemblies' large unplaced
scaffolds (already discussed in the contig-redundancy screen above), not evidence of anything new:

![protein_coding/pseudogene genes by contig size bin](01_Genome_Selection_QC/contig_size_profile/plots/pc_pseudogenes_by_contig_size_bin_by_genome.png)

[↑ Back to top](#analysis-steps)

---

## 02 – TE Annotation & Clean Up

We run TE candidate pipeline for all *A. fumigatus genomes*. The TE library was manually curated. Then we run Complementary TE Screen pipeline and a few new TEs were addef to the lib. 

Final library: `Afum_curated_TE_lib_final_180826.fa`

### 02.1 TE annotation (RepeatMasker)

Ran RepeatMasker on every assembly with the curated library
(`LIB="Afum_curated_TE_lib_final_180826.fa"` in the script), one `RM_<genome_id>/` folder
per genome:

```bash
sbatch 02_TE_annotation_Clean_Up/scripts/run_repeatmasker.slurm.sh
```

> ⚠️ This was run **before** the step-01 contig drop (see 02.2).

### 02.2 RepeatMasker was run before the step-01 contig drop — fix the annotation

For Afum, RepeatMasker (curated `Afum_curated_TE_lib_final_180826.fa`) was run on the
assemblies **before** the 30 contigs in
[`01_Genome_Selection_QC/drop_contigs.txt`](01_Genome_Selection_QC/drop_contigs.txt)
(12 organelle + 18 redundant) were removed. Each `RM_<genome_id>/` output therefore still
carries hits on contigs that were dropped afterwards — which would add mitochondrial /
haplotig TE to the per-genome totals and make `summarize_te_content.py` divide by the
pre-drop genome length.

Scripts: [`scripts/fix_repeatmasker_after_contig_drop.slurm.sh`](02_TE_annotation_Clean_Up/scripts/fix_repeatmasker_after_contig_drop.slurm.sh)
· [`scripts/fix_repeatmasker_after_contig_drop.py`](02_TE_annotation_Clean_Up/scripts/fix_repeatmasker_after_contig_drop.py)
(what it calls). For every `RM_<genome_id>/` (matched to its genome by the folder name / the
`.out` file name) it drops from `.out` / `.gff` the lines on the contigs listed for that
genome in the manifest, corrects the `.tbl` `total length:` (old total minus the removed
contigs' length, read from the `.out`), and copies the rest to
`repeatmasker_contig_filtered/RM_<genome_id>/`. Originals untouched; genomes with no manifest
entry (e.g. A1160) are just copied through. The wrapper defaults to
`RM_INDIR="."`, `DROP_LIST="01_Genome_Selection_QC/drop_contigs.txt"` — submit from the
project folder:

```bash
sbatch 02_TE_annotation_Clean_Up/scripts/fix_repeatmasker_after_contig_drop.slurm.sh
```

(`DROP_LIST=""` + `GENOMES="genomes"` in the wrapper is the alternative — removes *any*
contig not in the assembly and sets `total length` exactly — used if the post-drop
assemblies are present.)

Cleaned output: `repeatmasker_contig_filtered/RM_<genome_id>/` — this is what 02.3 and the
TE-overlap step run on, not the raw `RM_<genome_id>/`.

This is Afum-only: the general pipeline expects the contig drop (step 01) to happen
**before** RepeatMasker, so the script is not part of it.

### 02.3 TE composition across the panel

```bash
# INDIR="repeatmasker_contig_filtered" in the script
sbatch 02_TE_annotation_Clean_Up/scripts/summarize_te_content.slurm.sh
```

Numbers: [`te_content_summary/te_content_summary.tsv`](02_TE_annotation_Clean_Up/te_content_summary/te_content_summary.tsv)
· superfamily / family tables and `per_contig/` alongside. Plots label FungiDB genomes by
name (`AF293`, `A1160`, `A1163`) and the rest by accession (`GCA_…`) — strain ↔ accession in
the [01.1 table](#011-genomes-selected).

| | |
| :---: | :---: |
| ![Genome size](02_TE_annotation_Clean_Up/te_content_summary/plots/genome_size_bp.png) | ![Total TE bp](02_TE_annotation_Clean_Up/te_content_summary/plots/total_te_bp.png) |
| ![Superfamily composition](02_TE_annotation_Clean_Up/te_content_summary/plots/superfamily_composition.png) | ![Family composition](02_TE_annotation_Clean_Up/te_content_summary/plots/family_composition.png) |
| ![Divergence vs total TE](02_TE_annotation_Clean_Up/te_content_summary/plots/divergence_vs_total_te.png) | |

Genome size is the post-drop assembly length (from the corrected `.tbl`), not the
as-downloaded figure in [01.1](#011-genomes-selected).

#### Findings

- **Genome size is tight (27.8–29.4 Mb) — ATCC 46645 (`GCA_040142955.1`) is the one
  exception at 30.5 Mb**, the same assembly that is most fragmented and highest-TE (see
  below); its extra ~1 Mb is largely those unplaced repeat contigs. Genome size otherwise
  does not track TE content.
- **Low TE load throughout, 1.9–5.7 % of the genome** (≈0.53–1.75 Mb) — typical for a
  compact *Aspergillus* genome, no TE-rich outlier. Median ~3.6 %.
- **Superfamily rank order is conserved (LTR/Gypsy ≈55–65 % of the TE > DNA/Tc1-Mariner >
  LTR/Copia in all 17), but family composition is not — there is lineage structure.** Most
  clearly, **W72310 (`GCA_040167795.1`), eAF1023 (`GCA_058970245.1`) and eAF1090
  (`GCA_058972525.1`)** share a distinct mobilome: the main LTR/Gypsy families
  (`Gypsy-5/6/1_AF`) depleted 2–3× vs the rest, `Tad1-1_AF` essentially gone (0.001 % vs
  0.42 % in AF293), and they carry **`Gypsy-3_AF`** (0.25–0.32 % of the genome) which is
  absent (< 0.005 %) from 12 of the other 14. These same three carry the shared
  chromosome-2 ~707 kb inversion ([01.6](#016-synteny-analysis-vs-reference-af293)) — they
  are a genetic sub-group and the TE profile tracks it (W72310 has a standard Canu/Pilon
  assembly, so this is not a repeat-collapse artefact of the eAF POLCA/Medaka pipeline).
- **At the other end a family set (`Gypsy-5`, `Gypsy-2`, `Copia-4`, `Gypsy-4_2`, `AFUT1_AF`)
  is coordinately elevated** in ATCC 13073 (`GCA_040142885.1`), B5233 (`GCA_040142945.1`),
  ATCC 46645 (`GCA_040142955.1`) and D141 (`GCA_040167805.1`) — real in the two clean
  assemblies (13073, B5233), partly inflated by unplaced repeat contigs in the two
  fragmented ones (46645, D141).
- **No strain gains or loses a whole superfamily**, family count is stable (42–49 per
  genome), and the "extra" family (`Gypsy-3_AF`) is itself a Gypsy — so this is standing
  variation in an inherited repertoire (families differentially retained / amplified per
  lineage), not horizontal acquisition of a new element.
- **Most of the between-strain spread is assembly contiguity, not biology.** The two
  highest — **ATCC 46645** (`GCA_040142955.1`, 5.7 %) and **D141** (`GCA_040167805.1`,
  5.5 %) — are the two most fragmented assemblies (scaffold N50 ≈ 2 Mb; ATCC 46645 is the
  one flagged "noisiest, re-check the assembly" in [01.6](#016-synteny-analysis-vs-reference-af293)).
  Their excess TE sits on a handful of tiny (< 250 kb), repeat-saturated contigs — e.g. D141
  `JBDLLN…023/024/025.1` are 12–36 kb at **70–85 % TE** — i.e. unplaced repeat fragments a
  broken assembly failed to fold into a chromosome, not extra elements. Restrict any
  quantitative comparison to chromosome-scale contigs, or drop those fragments first.
- **A small genuine signal remains.** **ATCC 13073** and **B5233** (`GCA_040142885.1` /
  `GCA_040142945.1`, both 5.4 %, both clean 9-contig chromosome assemblies, both MD-USA
  clinical) have TE **uniformly elevated on every chromosome** (4–8 %), ~1.5–2 pp above
  AF293 — a real modest difference, not a fragmentation artefact, in a matched pair.
- **The structure is genetic, not clinical/environmental.** The
  W72310 / eAF1023 / eAF1090 sub-group mixes one clinical (W72310) and two environmental
  isolates; and the CEA10 lineage (A1160 3.6 %, A1163 3.2 %) sits next to AF293 (3.0 %).
  Total TE load spans the same range in both niches (env 1.9–4.0 %, clinical 2.1–5.7 %), so
  *load* is not niche-informative — but *family profile* does carry a sub-lineage signal.
- **The library is not biasing the comparison.** Mean divergence from the curated consensi
  is 8–10 % in every genome and the divergence-vs-TE scatter is flat — the AF293-anchored
  library is not systematically under-calling TE in the more divergent strains. `Tad1-1_AF`
  varies ~400× across the panel (AF293 0.42 %, ATCC 42202 `GCA_040142845.1` 0.30 %,
  W72310 / eAF1023 / eAF1090 ~0 %); AF293 being a library source may inflate its value
  slightly, but ATCC 42202 is not a source, so the LINE really is differentially retained.
- **The three eAF PromethION genomes are not a block.** eAF1023 and eAF1090
  (`GCA_058970245.1` / `GCA_058972525.1`) are the two lowest (1.9 %), nearly identical, and
  in the W72310 sub-group profile — but eAF1436 (`GCA_058972625.1`), from the *same*
  sequencing/assembly pipeline, is at 4.0 % with a normal family profile (`Gypsy-3_AF` only
  0.05 %) despite also carrying the chr2 inversion. So the low eAF1023 / eAF1090 values are
  not a Celera/POLCA/Medaka repeat-collapse effect, and the sub-group is
  W72310 + eAF1023 + eAF1090, not "the eAF set".
  A BUSCO-duplication check on eAF1023/eAF1090 would still be worth doing.


### 02.4 TE overlap with gene models

`te_gene_overlap.slurm.sh` — one job, one output folder. On the cleaned RM annotation
(`TE_INDIR="repeatmasker_contig_filtered"` in the wrapper) and `gff_originals/`, it (1)
computes the non-redundant TE overlap over the CDS of every gene and (2) extracts the
spliced CDS sequence (FASTA) of the genes in the `MIN_PCT`–`MAX_PCT` band (default 20–80%):

```bash
sbatch 02_TE_annotation_Clean_Up/scripts/te_gene_overlap.slurm.sh
```

**Output,** all in `te_annotation_integration/`:

- `gene_te_overlap.tsv` — gene description, `TE_overlap_pct`, dominant TE name, 5′/3′/internal/mixed
  position per gene. Genes with 0% overlap are left out; this table carries everything needed
  for review, no need to go back to the GFF.
- `protein_coding_threshold_summary.tsv` / `pseudogene_threshold_summary.tsv` — gene counts
  across candidate overlap cutoffs.
- `plots/` — the distribution/threshold figures.
- `flagged_genes_cds.fna` — spliced CDS of the flagged genes.

A `WARNING: N requested gene(s) have NO sequence …` block at the end of the log lists any gene
that didn't make it into the FASTA and why.

| | |
| :---: | :---: |
| ![Protein-coding CDS/TE overlap, nonzero](02_TE_annotation_Clean_Up/te_annotation_integration/plots/protein_coding_te_overlap_hist_nonzero.png) | ![Pseudogene overlap with TEs](02_TE_annotation_Clean_Up/te_annotation_integration/plots/pseudogene_te_overlap_hist.png) |

![CDS/TE overlap by genome](02_TE_annotation_Clean_Up/te_annotation_integration/plots/protein_coding_te_overlap_by_genome.png)

| | |
| :---: | :---: |
| ![20-80% inspect band by genome](02_TE_annotation_Clean_Up/te_annotation_integration/plots/protein_coding_inspect_band_by_genome.png) | ![Overlap position by TE-overlap %](02_TE_annotation_Clean_Up/te_annotation_integration/plots/protein_coding_overlap_position_by_pct.png) |

#### Findings

- **TE-overlapping genes are rare.** Only 56 genes pool into the 20–80% "inspect" band across the whole panel. AF293 is a clear outlier having more TE-overlapping genes than any other genome.

- **Pseudogenes are barely annotated in this panel, so there's little to say.** Only 21
  `pseudogene`-typed records total: 19 in A1163, 1 in AF293, 1 in eAF1090
  (`GCA_058972525.1`); none of the 14 NCBI/UCR GFFs tag any. 20 of the 21 have ~0% TE
  overlap. 
  
- **Practical consequence for step 05 / downstream filtering:** applying the pipeline's
  ≥80% reclassify cutoff uniformly will remove a disproportionate share of AF293's gene
  count (92 genes) relative to every other genome (13–44). That is expected and correct —
  it corrects a real, historical annotation-era difference, not new noise the filter is
  introducing — but worth remembering if "AF293 has fewer protein-coding genes after TE
  filtering" comes up when comparing gene counts later.

#### Removing TE-derived genes from the GFFs

Eliminated-band genes (≥80% overlap) manually reviewed and confirmed as genuine TE-derived
models, safe to remove. The 20–80% "flagged"/inspect band is not yet reviewed.

```bash
sbatch 02_TE_annotation_Clean_Up/scripts/build_te_kill_lists.slurm.sh
```

339 confirmed TE-derived genes removed from every genome's GFF, output in `gff_cleaned/`.

[↑ Back to top](#analysis-steps)

---

## 03 – *de novo* Genome Annotation

No need as all genomes used have annotation

[↑ Back to top](#analysis-steps)

---

## 04 – InterProScan

### 04.1 Running InterProScan

```bash
sbatch 04_InterProScan/scripts/extract_proteins.slurm.sh          # gff_cleaned/ -> interpro/proteins/*.faa
sbatch 04_InterProScan/scripts/build_interpro_manifest.slurm.sh   # interpro/interpro_manifest.tsv
```

`interpro_manifest.tsv` for this panel (17 genomes, `CHUNK_SIZE=1000`): **184 total chunks**.
Submit the array job with:
```bash
mkdir -p interpro/logs
N=$(($(wc -l < interpro/interpro_manifest.tsv) - 1))
sbatch --array=1-${N}%20 04_InterProScan/scripts/interproscan_array_job.slurm.sh
```
(currently 184, but always recomputed from the manifest, not hardcoded - see
[`04_InterProScan/README.md`](../../04_InterProScan/README.md) for why: a bare
`sbatch interproscan_array_job.slurm.sh` with no `--array=...` only runs 1 smoke-test task).

Protein extraction ran on `gff_cleaned/` (step 02's TE-kill-list output — organelle,
redundant-contig, and TE-derived genes already removed). The array job **finished**: all 184
chunks completed (each chunk's `.out` ends with `Finished <genome> chunk <N>`).

### 04.2 Merging the chunk results

Combines the per-chunk InterProScan output into one lookup table per genome
(`interpro/interpro_lookup/`) and checks completeness:
```bash
sbatch 04_InterProScan/scripts/merge_interpro_job.slurm.sh
```
A protein reported as absent from the chunk output is a `NOTE`, not an error: InterProScan only
writes a row when it finds a hit, so it is a protein with no domain hits. Only a missing chunk
file (`WARNING`) means the results are incomplete.

### 04.3 Adding the domain evidence to the GFFs

Writes the `InterPro:`/`PFAM:` evidence into the `Dbxref=` of each CDS line, reading
`gff_cleaned/` and writing new GFFs to `gff_with_interpro/` (the input is never modified):
```bash
sbatch 04_InterProScan/scripts/update_interpro_in_gff.slurm.sh
```
This ran successfully; `gff_with_interpro/` is the input for step 05.

[↑ Back to top](#analysis-steps)

---

## 05 – Cross-genome Annotation Integration

### Step 1: Native annotation check

Run **once**, after [step 04](#04--interproscan), on `gff_with_interpro/` (the GFFs with the
domain evidence written in), so that the domain columns and plots are real. Output folder for
this run: `annotation_check/`.
```bash
sbatch 05_Cross-genome_annotation_integration/scripts/analyze_input_gffs_job.sh
```

**Genes per genome** - 9,601 to 10,464 protein-coding genes per genome, split by whether the
gene carries InterPro/PFAM evidence (81-84% do, in every genome, so no genome stands out as
missing domain annotation).

![Protein-coding genes per genome, with and without domain evidence](05_Cross-genome_annotation_integration/annotation_check/01_gene_counts_protein_coding.png)

**Gene types** - every gene category found. Nearly everything is protein-coding. The
non-coding genes are reported differently by the two groups of genomes: AF293 (262), A1160 and
A1163 (180 each) carry them as `ncRNA_other` and have no tRNA category, while the 14 `GCA_`
genomes carry 160-172 tRNA genes each and no `ncRNA_other`. Pseudogenes are only in A1163 (19),
AF293 (1) and GCA_058972525.1 (1). No genome has rRNA or unclassified genes.

![Gene categories per genome](05_Cross-genome_annotation_integration/annotation_check/02_gene_biotype_breakdown.png)

**Whole-gene overlaps** - pairs of genes whose annotated spans touch, UTR included. The 14 `GCA_`
genomes have 579-849 each (mostly opposite-strand), AF293 has 246 and A1160/A1163 have 8-9.
Almost all of these disappear once the UTRs are left out: the core-span count (CDS/exon extent
only) is 0-4 per `GCA_` genome. So the CDS-level count below is the one that matters.

**CDS-to-CDS overlaps** - gene pairs whose coding sequences actually overlap, split by strand.
Most genomes have 0-2 pairs. AF293 has the most (16, all opposite-strand); A1160 and A1163 have
4 each, and GCA_040126065.1 has 4 (2 same-strand, 2 opposite-strand).

![CDS-overlapping gene pairs per genome, by strand](05_Cross-genome_annotation_integration/annotation_check/05_cds_overlap_counts.png)

**Overlap severity** - the same pairs by how much of the smaller gene's CDS is covered:
minor (< 20%), substantial (20-80%), contained (>= 80%). AF293 has 6 minor, 5 substantial and 5
contained pairs; every other genome has at most 2 contained pairs. The pair list with
descriptions, sizes and `has_domain` is `cds_overlapping_pairs.tsv`.

![CDS overlap severity per genome](05_Cross-genome_annotation_integration/annotation_check/06_cds_overlap_severity.png)

Also in that folder: `03_gene_overlap_counts.png` (whole-gene overlap, UTR included),
`04_core_overlap_counts.png` (CDS/exon extent only), and the tables
(`gene_biotype_counts.tsv`, `overlap_counts.tsv`, `feature_attribute_table.tsv`, one
`<genome>_gene_classification.tsv` per genome).

### Prepare the GFFs for Liftoff

No genes are removed by a kill list for this species (no `gff_curated/`), so
[`prepare_for_liftoff_job.sh`](../../05_Cross-genome_annotation_integration/README.md#step-3-prepare-the-gffs-for-liftoff)
reads `gff_with_interpro/` (step 04's output) directly and writes to `gff_for_liftoff/`: genes
reduced to their coding sequence (no UTRs), protein-coding genes and pseudogenes unified to
`protein_coding_gene`, and tRNA genes given their own type (`tRNA_gene`) so Liftoff - which only
transfers the types in `liftoff_feature_types.txt` (here just `protein_coding_gene`) - does not
copy them onto other genomes. Each genome keeps its own non-coding genes.
```bash
sbatch 05_Cross-genome_annotation_integration/scripts/prepare_for_liftoff_job.sh
```

Result (`gff_for_liftoff/prepare_for_liftoff_report.tsv`), per genome: transcripts processed, UTR
lines deleted, exons clipped or deleted to the coding extent, genes resized, and total bp cut
from gene spans:

| Genome | Transcripts | UTR lines deleted | Exons clipped | Exons deleted | Genes resized | bp trimmed |
|---|---|---|---|---|---|---|
| AF293 | 10014 | 13075 | 11786 | 973 | 6968 | 4125804 |
| A1160 | 9887 | 8378 | 7246 | 611 | 4745 | 2473229 |
| A1163 | 9896 | 8385 | 7253 | 611 | 4749 | 2474427 |
| GCA_040126065.1 | 10447 | 13120 | 11016 | 1522 | 6197 | 3550275 |
| GCA_040142845.1 | 10433 | 13203 | 11118 | 1512 | 6313 | 3427091 |
| GCA_040142855.1 | 10464 | 12662 | 10791 | 1329 | 6203 | 3240086 |
| GCA_040142865.1 | 10532 | 13058 | 11030 | 1468 | 6235 | 3399232 |
| GCA_040142875.1 | 10455 | 13029 | 10938 | 1479 | 6225 | 3363389 |
| GCA_040142885.1 | 10429 | 12979 | 10871 | 1536 | 6048 | 3551366 |
| GCA_040142945.1 | 10365 | 12898 | 10834 | 1513 | 6094 | 3460373 |
| GCA_040142955.1 | 11031 | 13641 | 11410 | 1655 | 6366 | 3536240 |
| GCA_040142975.1 | 10407 | 12560 | 10656 | 1363 | 6103 | 3315548 |
| GCA_040167795.1 | 10533 | 13086 | 11059 | 1440 | 6331 | 3475645 |
| GCA_040167805.1 | 9858 | 10343 | 8885 | 945 | 5130 | 2652914 |
| GCA_058970245.1 | 10679 | 13607 | 11088 | 1893 | 5849 | 3639004 |
| GCA_058972525.1 | 10848 | 13831 | 11320 | 1817 | 6070 | 3706944 |
| GCA_058972625.1 | 10765 | 13605 | 10947 | 2006 | 5693 | 3682416 |

Gene types changed (only where the type had to change):

| Genome | From | To | Genes |
|---|---|---|---|
| A1163 | `pseudogene` | `protein_coding_gene` | 19 |
| AF293 | `pseudogene` | `protein_coding_gene` | 1 |
| GCA_040126065.1 | `gene` | `protein_coding_gene` | 9906 |
| GCA_040126065.1 | `gene` | `tRNA_gene` | 165 |
| GCA_040142845.1 | `gene` | `protein_coding_gene` | 9940 |
| GCA_040142845.1 | `gene` | `tRNA_gene` | 170 |
| GCA_040142855.1 | `gene` | `protein_coding_gene` | 9997 |
| GCA_040142855.1 | `gene` | `tRNA_gene` | 170 |
| GCA_040142865.1 | `gene` | `protein_coding_gene` | 10026 |
| GCA_040142865.1 | `gene` | `tRNA_gene` | 170 |
| GCA_040142875.1 | `gene` | `protein_coding_gene` | 9963 |
| GCA_040142875.1 | `gene` | `tRNA_gene` | 169 |
| GCA_040142885.1 | `gene` | `protein_coding_gene` | 9880 |
| GCA_040142885.1 | `gene` | `tRNA_gene` | 171 |
| GCA_040142945.1 | `gene` | `protein_coding_gene` | 9874 |
| GCA_040142945.1 | `gene` | `tRNA_gene` | 168 |
| GCA_040142955.1 | `gene` | `protein_coding_gene` | 10464 |
| GCA_040142955.1 | `gene` | `tRNA_gene` | 170 |
| GCA_040142975.1 | `gene` | `protein_coding_gene` | 9927 |
| GCA_040142975.1 | `gene` | `tRNA_gene` | 167 |
| GCA_040167795.1 | `gene` | `protein_coding_gene` | 10052 |
| GCA_040167795.1 | `gene` | `tRNA_gene` | 165 |
| GCA_040167805.1 | `gene` | `protein_coding_gene` | 9601 |
| GCA_040167805.1 | `gene` | `tRNA_gene` | 172 |
| GCA_058970245.1 | `gene` | `protein_coding_gene` | 10006 |
| GCA_058970245.1 | `gene` | `tRNA_gene` | 160 |
| GCA_058972525.1 | `gene` | `protein_coding_gene` | 10205 |
| GCA_058972525.1 | `gene` | `tRNA_gene` | 166 |
| GCA_058972525.1 | `pseudogene` | `protein_coding_gene` | 1 |
| GCA_058972625.1 | `gene` | `protein_coding_gene` | 10008 |
| GCA_058972625.1 | `gene` | `tRNA_gene` | 165 |

- The 14 NCBI-style genomes (`GCA_...`) type every gene as plain `gene`, so the script separated
  them by content: protein-coding genes (9,601-10,464 per genome) became `protein_coding_gene`
  and the 160-172 tRNA genes became `tRNA_gene`.
- The FungiDB-style genomes (AF293, A1160, A1163) already used `protein_coding_gene` and
  `ncRNA_gene`, so only their pseudogenes (AF293 1, A1163 19, A1160 none) were retyped, and
  their pseudogene status stays visible in the biotype attribute (`ebi_biotype=pseudogene`).
- One NCBI-style genome (`GCA_058972525.1`) also had 1 pseudogene retyped; it keeps `gene_biotype=pseudogene`.

### Liftoff (all-against-all)

[`liftoff_all_vs_all.sh`](../../05_Cross-genome_annotation_integration/README.md#step-4-liftoff)
lifts every genome's prepared annotation (`gff_for_liftoff/`) onto every other genome's
FASTA (`genomes/`) - 17 genomes, so 272 pairs. Run as one job per source genome:
```bash
mkdir -p liftoff_output/logs
sbatch --array=1-17 05_Cross-genome_annotation_integration/scripts/liftoff_all_vs_all.sh
```
Results go to `liftoff_output/polished/`, job logs to `liftoff_output/logs/`. Resubmitting skips pairs that are already done.

### Build each genome's final annotation

[`build_final_annotation_basic.sh`](../../05_Cross-genome_annotation_integration/README.md#step-5-build-each-genomes-final-annotation)
builds one annotation per genome anchored on its own coordinates. The reference is AF293 (first line
of `genome_order.txt`). The layers are the reference's confident transfers (`main`), then the
genome's own annotation from `gff_for_liftoff/` - which is where its non-coding genes come back in -
then the other genomes' good transfers (`good_<genome>`), then everything left (`rescued_<genome>`).
Run after all Liftoff jobs have finished, one job per genome:
```bash
mkdir -p expanded_annotation/logs
sbatch --array=1-17 05_Cross-genome_annotation_integration/scripts/build_final_annotation_basic.sh
```
Results: `expanded_annotation/<genome>_final_annotation.gff`, job logs in `expanded_annotation/logs/`.

### Step 6: Built annotation check

QC on the raw build output, before [step 7](../../05_Cross-genome_annotation_integration/README.md#step-7-final-annotation-if-using-step-5-pre-get_pangenes)'s
filter runs. Output folder: `final_annotation_qc_plots/`.
```bash
mkdir -p final_annotation_qc_plots/logs
sbatch 05_Cross-genome_annotation_integration/scripts/plot_final_annotation_qc_job.sh
```
(Full description of every output file:
[general README](../../05_Cross-genome_annotation_integration/README.md#step-6-built-annotation-check-if-using-step-5).)

**Gene counts** - each genome's final build has 11,074-11,776 protein-coding genes, above its own original
annotation (9,601-10,464), since genes are being pulled in from every other genome too.

![Protein-coding genes: own original annotation vs. this pipeline's build](05_Cross-genome_annotation_integration/final_annotation_qc_plots/01_gene_counts.png)

**Extra copies** - ATCC 42202 (76), ATCC 46645 (60) and 08-19-02-30 (56) stand out; every other genome has
between 11 and 46.

![Extra-copy genes, split by valid ORF](05_Cross-genome_annotation_integration/final_annotation_qc_plots/03_extra_copies.png)

**CDS-overlap severity** - 4,997 CDS-overlapping pairs across the panel, split minor (669), substantial (1,953)
and contained (2,375).

![CDS-overlap severity per genome](05_Cross-genome_annotation_integration/final_annotation_qc_plots/04_overlap_severity.png)

**Source composition** - where each genome's final genes came from (`main`/original/`good_*`/`rescued_*`).

![Source composition per genome](05_Cross-genome_annotation_integration/final_annotation_qc_plots/05_source_composition.png)

**Overlap strand** - the same 4,997 pairs, split by strand instead of severity: only **13 are same-strand**
(the ones that "shouldn't normally happen"), the other **4,984 are opposite-strand**.

![CDS-overlapping pairs per genome, by strand](05_Cross-genome_annotation_integration/final_annotation_qc_plots/06_overlap_strand.png)

**Overlap domain support** - of the 4,997 pairs, **129 have InterPro/PFAM domain evidence on both genes**,
**2,918 on exactly one**, and **1,950 on neither**. These counts use protein domains only; the 7a filter also
counts a specific description as evidence (see below).

![CDS-overlapping pairs per genome, by domain support](05_Cross-genome_annotation_integration/final_annotation_qc_plots/07_overlap_domain_support.png)

**Pairs by case** - the 4,997 pairs of the raw build, by whether each gene is `main` and whether it carries a
protein domain:

| # | Case | Pairs |
|---|---|---:|
| 1 | `main` × `main` | 190 |
| 2 | `main` × other, other **has** a domain | 161 |
| 3 | `main` × other, other has **no** domain | 3,293 |
| 4 | other × other, **one** has a domain | 369 |
| 5 | other × other, **both** have a domain | 20 |
| 6 | other × other, **neither** has a domain | 964 |

Case 6 - 964 pairs, 633 distinct genes: 99.9% opposite-strand, 233 `minor` severity.

Also in that folder: `summary.tsv` (the numbers behind every plot above), `extra_copy_genes.tsv`
(every extra-copy gene, with description/location/domain/valid-ORF), `cds_overlapping_pairs.tsv`
(every pair above, one row each) and `overlap_domain_summary.tsv` (the domain-support numbers
above, per genome).

[↑ Back to top](#analysis-steps)

---

### Filtering — 7a pre-filter (done)

Ran [`filter_final_annotation.py`](../../05_Cross-genome_annotation_integration/scripts/filter_final_annotation.py)
on all 17 genomes (rule details in the
[general README](../../05_Cross-genome_annotation_integration/README.md#7a-filter-drop-unsupported-genes-before-get_pangenes)).
Output: `filtered_annotation/<genome>_final_annotation_filtered.gff`, with the genes typed `gene` and
renumbered `Afu<strain-index>g<00001, ...>`, original ID kept in `original_ID=`. The figures come from
`plot_filter_qc_job.sh` (`filter_qc_plots/`).

The filter removed **4,307 of 192,136 genes (2.2%)**, between 1.9% and 2.7% per genome:

| Genome | n_original | n_kept | n_removed | % removed |
|---|---:|---:|---:|---:|
| AF293 | 11,295 | 11,048 | 247 | 2.2% |
| A1160 | 11,397 | 11,148 | 249 | 2.2% |
| A1163 | 11,393 | 11,160 | 233 | 2.0% |
| GCA_040126065.1 | 11,091 | 10,846 | 245 | 2.2% |
| GCA_040142845.1 | 11,242 | 10,933 | 309 | 2.7% |
| GCA_040142855.1 | 11,428 | 11,157 | 271 | 2.4% |
| GCA_040142865.1 | 11,375 | 11,116 | 259 | 2.3% |
| GCA_040142875.1 | 11,363 | 11,087 | 276 | 2.4% |
| GCA_040142885.1 | 11,074 | 10,838 | 236 | 2.1% |
| GCA_040142945.1 | 11,081 | 10,868 | 213 | 1.9% |
| GCA_040142955.1 | 11,776 | 11,509 | 267 | 2.3% |
| GCA_040142975.1 | 11,370 | 11,096 | 274 | 2.4% |
| GCA_040167795.1 | 11,408 | 11,141 | 267 | 2.3% |
| GCA_040167805.1 | 11,082 | 10,841 | 241 | 2.2% |
| GCA_058970245.1 | 11,229 | 11,000 | 229 | 2.0% |
| GCA_058972525.1 | 11,449 | 11,191 | 258 | 2.3% |
| GCA_058972625.1 | 11,083 | 10,850 | 233 | 2.1% |

Before and after filtering, per genome:

![Genes before and after filtering](05_Cross-genome_annotation_integration/filter_qc_plots/01_gene_counts.png)

Why each gene was removed (read from the figure): about half of the removed genes overlapped a
reference-derived (`main`) gene and had no evidence themselves. The rest are low-coverage `rescued_`
transfers, ties between two genes with no evidence, genes that overlapped a gene with evidence, and
extra copies with no valid ORF.

![Why each gene was removed](05_Cross-genome_annotation_integration/filter_qc_plots/03_removal_reasons.png)

Extra-copy genes fall from 11-76 per genome to 0-25; GCA_040142955.1 (25) and GCA_058972525.1 (13)
keep the most.

![Extra-copy genes before and after filtering](05_Cross-genome_annotation_integration/filter_qc_plots/02_extra_copies.png)

CDS-overlapping gene pairs fall from 262-303 per genome to 94-110, and the pairs where one gene is
contained in the other from 128-149 to 43-48. The rules keep some overlaps on purpose (small overlaps
at a gene's end, pairs where both genes have evidence); which case the remaining pairs belong to was
not checked.

![CDS-overlap severity before and after filtering](05_Cross-genome_annotation_integration/filter_qc_plots/04_overlap_severity.png)

Which layer each gene comes from (`main`, the genome's own annotation, `good_` and `rescued_`
transfers):

![Source composition before and after filtering](05_Cross-genome_annotation_integration/filter_qc_plots/05_source_composition.png)

### Filtering — 7b no pre-filter / tag (done)

Ran [`tag_final_annotation.py`](05_Cross-genome_annotation_integration/scripts/tag_final_annotation.py)
on all 17 genomes (rule details in the
[general README](../../05_Cross-genome_annotation_integration/README.md#7b-no-filtering-tag-decide-after-get_pangenes)).
Nothing removed - same `gene`-typing/ID-renumbering as 7a, plus an `intersect=` tag on every
gene recording what it overlaps (`NA`/`with_main`/`with_other_with_domain`/`with_other_no_domain`).
Output: `tagged_annotation/<genome>_final_annotation_tagged.gff` + `<genome>_intersect_pairs.tsv`.

```bash
sbatch 05_Cross-genome_annotation_integration/scripts/tag_final_annotation_job.sh
```

| Genome | n_total | NA | with_main | with_other_with_domain | with_other_no_domain |
|---|---:|---:|---:|---:|---:|
| AF293 | 11,295 | 10,768 | 250 | 15 | 262 |
| A1160 | 11,397 | 10,869 | 224 | 30 | 274 |
| A1163 | 11,393 | 10,867 | 224 | 32 | 270 |
| GCA_040126065.1 | 11,091 | 10,564 | 220 | 32 | 275 |
| GCA_040142845.1 | 11,242 | 10,686 | 220 | 30 | 306 |
| GCA_040142855.1 | 11,428 | 10,880 | 222 | 32 | 294 |
| GCA_040142865.1 | 11,375 | 10,827 | 223 | 32 | 293 |
| GCA_040142875.1 | 11,363 | 10,784 | 220 | 34 | 325 |
| GCA_040142885.1 | 11,074 | 10,553 | 210 | 28 | 283 |
| GCA_040142945.1 | 11,081 | 10,575 | 210 | 29 | 267 |
| GCA_040142955.1 | 11,776 | 11,234 | 211 | 35 | 296 |
| GCA_040142975.1 | 11,370 | 10,810 | 220 | 33 | 307 |
| GCA_040167795.1 | 11,408 | 10,851 | 196 | 38 | 323 |
| GCA_040167805.1 | 11,082 | 10,553 | 206 | 33 | 290 |
| GCA_058970245.1 | 11,229 | 10,705 | 202 | 36 | 286 |
| GCA_058972525.1 | 11,449 | 10,905 | 199 | 37 | 308 |
| GCA_058972625.1 | 11,083 | 10,564 | 208 | 30 | 281 |

[↑ Back to top](#analysis-steps)

---

## 06 – GET_PANGENES

Ran `get_pangenes` twice, on the 7a GFFs (`filtered_annotation/`, filtered before) and on the 7b GFFs
(`tagged_annotation/`, nothing pre-filtered), 17 genomes each:
```bash
sbatch 06_GET_PANGENES/scripts/link_for_get_pangenes_7a.slurm.sh
sbatch 06_GET_PANGENES/scripts/run_get_pangenes_7a_job.sh
sbatch 06_GET_PANGENES/scripts/link_for_get_pangenes_7b.slurm.sh
sbatch 06_GET_PANGENES/scripts/run_get_pangenes_7b_job.sh
```
Result: **12,984 pangenes** with filtering (7a) and **13,693 pangenes** without (7b)
(`for_get_pangenes_7{a,b}_pangenes/pangene_matrix*.tab`; `pangene_matrix_genes.tr.tab` lists the gene IDs
of every genome in every pangene).

[↑ Back to top](#analysis-steps)

---

## 07 – Post-GET_PANGENES Adjusting

[↑ Back to top](#analysis-steps)

---

## 08 – Pangenome Visualisation

> **Preliminary.** Some pangenes hold more than one gene of the same genome (443 with filtering, 454 without
> filtering) and have not been examined yet ([step 07](#07--post-get_pangenes-adjusting)). The figures below count
> them as they are. They will be updated once those pangenes are resolved.

The same figures for the two sets of pangenes: **with filtering** (7a, filtered before `get_pangenes`) and
**no filtering** (7b, tagged, nothing removed). Every figure also comes as `.svg`, and files start with the
label (`Afum7a`/`Afum7b`). They come from
[`plot_all_job.sh`](../../08_Pangenome_Visualisation/scripts/plot_all_job.sh), one run for each set:
```bash
mkdir -p pangenome_plots/logs
sbatch 08_Pangenome_Visualisation/scripts/plot_all_job.sh --set 7a --label Afum7a
sbatch 08_Pangenome_Visualisation/scripts/plot_all_job.sh --set 7b --label Afum7b
```
Genomes are labelled by their accession, except AF293, A1160 and A1163. The strain of each accession is in the
[genome table of step 01](#01--genome-selection--qc).

---

### With filtering (7a)

*Pangenes from the GFFs filtered before `get_pangenes`.*

**Pangenome and core genome size** - genomes are added one at a time in 100 random orders. The pangenome
grows to 12,984 pangenes (all 17 genomes), still growing by about 70 per genome at the end. The core falls
to 10,254; the fitted curves put its plateau at 10,295 (Tettelin) and 10,238 (Willenbrock).
`Afum7a_pancore_separate.png` shows the two curves in separate panels.

![Pangenome and core genome size, with filtering](08_Pangenome_Visualisation/pangenome_plots/Afum7a_pancore.png)

**Pangene occupancy** - how many genomes each pangene is present in. 10,254 pangenes (79%) are core,
132 are in 16 genomes (soft-core), 1,173 (9%) are in one genome only and 331 in two.

![Pangene occupancy, with filtering](08_Pangenome_Visualisation/pangenome_plots/Afum7a_occupancy.png)

**Singletons per genome** - ATCC 46645 has the most (213), then W72310 (121) and H237 (107); eAF1023 (15) and
B5233 (17) have the fewest.

![Singletons per genome, with filtering](08_Pangenome_Visualisation/pangenome_plots/Afum7a_singletons.png)

**POCS heatmap** - pairwise percentage of conserved sequences between genomes, clustered (complete linkage);
darker means more similar, and the colour scale covers the values between different genomes only.

![POCS heatmap, with filtering](08_Pangenome_Visualisation/pangenome_plots/Afum7a_POCS_heatmap.png)

**Gene properties by occupancy** - every pangene is used (12,984), including the ones with more than one gene in
a genome; the occupancy is the number of genomes the pangene is present in. Top: proportion of genes with an
InterPro/PFAM domain, averaged over the pangenes of each occupancy. Bottom: protein length, one value per pangene
(the median over all its genes). A Tukey HSD test compares the four categories on the value of each pangene, and the
p-value of core against cloud is written on each panel; it treats the genes of one pangene, which come from different
genomes, as independent samples, so it is optimistic. Core: 78% of genes with a domain, median 388 aa; cloud: 51% and 246 aa. The `_log` file shows protein length on a log axis.

![Gene properties by occupancy, with filtering](08_Pangenome_Visualisation/pangenome_plots/Afum7a_occupancy_properties.png)

**Contig size by occupancy** - the contigs that carry the pangenes, split into size classes. Every pangene is used
(12,984); each gets one value, the median length of the contigs of all its genes. The bars give the share of the
pangenes of each category in each class. Cloud pangenes are on contigs below 200 kb more often than the others:
11% of cloud pangenes (6% below 50 kb), against none of the core and shell pangenes; 22% are on contigs below 1 Mb,
against 1.5% of core. No pangene has a median contig below 10 kb, so the smallest class starts at 10 kb; the panel still
has 36 contigs below 10 kb, but they carry only 4 genes (see [step 01](#01--genome-selection--qc)).

![Contig size by occupancy, with filtering](08_Pangenome_Visualisation/pangenome_plots/Afum7a_contig_classes.png)

**Invalid ORFs by occupancy** - a gene is invalid when Liftoff found no valid open reading frame or the source
annotation calls it a pseudogene. A pangene is "mostly invalid" when more than 50% of its genes are invalid.
Mostly invalid: 39% of cloud pangenes (207 of 531), 19% of shell, 7% of soft-core and 1.9% of core (190 of
10,200). Pangenes with no gene that can be judged (1,343) are left out.
Even after the 7a filter, a large share of the cloud pangenes is mostly invalid, so additional filtering could be considered.

![Number of pangenes with mostly invalid ORFs, with filtering](08_Pangenome_Visualisation/pangenome_plots/Afum7a_occupancy_invalid_only.png)

![Percentage of pangenes with mostly invalid ORFs, with filtering](08_Pangenome_Visualisation/pangenome_plots/Afum7a_occupancy_invalid_percent.png)

![Share of invalid genes by category, with filtering](08_Pangenome_Visualisation/pangenome_plots/Afum7a_invalid_share.png)

**Share of invalid genes by category** - each bar is one category, from cloud to core, split by how many of the genes of a
pangene are invalid: none, up to half, more than half but not all, or all of them. In the cloud most pangenes have one or
two genes, so a pangene is either all valid or all invalid, and the segment of "all invalid" is about the same as the
share of "mostly invalid" pangenes in the two figures above.

**InterPro term enrichment** - for core and cloud pangenes, which InterPro entries are found more often than in the
remaining pangenes (one-sided Fisher test, Benjamini-Hochberg adjusted). Only pangenes with at least one InterPro
entry are counted (8,037 core, 765 cloud), and only entries carried by at least 5 pangenes are tested (1,055).
Cloud: 43 entries are enriched (adjusted p < 0.05, at least 3 pangenes); core: 9. The cloud hits include domains of
unknown function (DUF3435, DUF3723), acyl transferase and protein kinase-like domains; the core hits include the
armadillo-type fold, sugar transporter and OB-fold domains. A core pangene collects entries from the genes of up to 17
genomes, which may favour the core side.

![InterPro term enrichment, with filtering](08_Pangenome_Visualisation/pangenome_plots/Afum7a_domain_enrichment.png)

---

### No filtering (7b)

*Pangenes from the tagged GFFs, nothing removed.*

**Pangenome and core genome size** - the pangenome grows to 13,693 pangenes (all 17 genomes), still growing by
about 97 per genome at the end. The core falls to 10,433; the fitted curves put its plateau at 10,477 (Tettelin) and
10,426 (Willenbrock). `Afum7b_pancore_separate.png` shows the two curves in separate panels.

![Pangenome and core genome size, no filtering](08_Pangenome_Visualisation/pangenome_plots/Afum7b_pancore.png)

**Pangene occupancy** - 10,433 pangenes (76%) are core, 133 are in 16 genomes (soft-core), 1,596 (12%) are in one
genome only and 360 in two.

![Pangene occupancy, no filtering](08_Pangenome_Visualisation/pangenome_plots/Afum7b_occupancy.png)

**Singletons per genome** - ATCC 46645 has the most (230), then ATCC 42202 (178) and 08-19-02-30 (160); eAF1023 (14)
and B5233 (16) have the fewest. Genomes that have very close relatives in the panel (see the POCS heatmap) tend to have
fewer singletons, because what they share is present in more than one genome.

![Singletons per genome, no filtering](08_Pangenome_Visualisation/pangenome_plots/Afum7b_singletons.png)

**POCS heatmap** - same as above. The figure shows values rounded to integers: between different genomes they range
from 95 to 99. A1160 and A1163 are the most similar pair (100 after rounding), and ATCC 46645 (`GCA_040142955.1`) is
the genome with the lowest values against all the others (95-96).

![POCS heatmap, no filtering](08_Pangenome_Visualisation/pangenome_plots/Afum7b_POCS_heatmap.png)

**Gene properties by occupancy** - same method as above, on 13,693 pangenes. Core: 77% of genes with a domain,
median 383 aa; cloud: 42% and 204 aa.

![Gene properties by occupancy, no filtering](08_Pangenome_Visualisation/pangenome_plots/Afum7b_occupancy_properties.png)

**Contig size by occupancy** - same method as above, on 13,693 pangenes. 11% of cloud pangenes are on contigs below
200 kb (7% below 50 kb), against none of the core and shell pangenes; 28% are on contigs below 1 Mb, against 1.6% of
core.

![Contig size by occupancy, no filtering](08_Pangenome_Visualisation/pangenome_plots/Afum7b_contig_classes.png)

**Invalid ORFs by occupancy** - same method as above. Mostly invalid: 57% of cloud pangenes (535 of 940; 454 of the
729 singletons), 25% of shell, 8% of soft-core and 2.1% of core (214 of 10,379). Pangenes with no gene that can be
judged (1,372) are left out.

![Number of pangenes with mostly invalid ORFs, no filtering](08_Pangenome_Visualisation/pangenome_plots/Afum7b_occupancy_invalid_only.png)

![Percentage of pangenes with mostly invalid ORFs, no filtering](08_Pangenome_Visualisation/pangenome_plots/Afum7b_occupancy_invalid_percent.png)

![Share of invalid genes by category, no filtering](08_Pangenome_Visualisation/pangenome_plots/Afum7b_invalid_share.png)

**Share of invalid genes by category** - each bar is one category, from cloud to core, split by how many of the genes of a
pangene are invalid: none, up to half, more than half but not all, or all of them. In the cloud most pangenes have one or
two genes, so a pangene is either all valid or all invalid, and the segment of "all invalid" is about the same as the
share of "mostly invalid" pangenes in the two figures above.

**Unsupported overlapping genes by occupancy** - only possible without filtering, because it needs the `intersect=`
tag. A gene is unsupported when it is not from the reference layer (`main`), overlaps another gene, has no
InterPro/Pfam domain and has no specific description. A pangene is "mostly unsupported" when more than 50% of its genes
are unsupported. Mostly unsupported: 14% of cloud pangenes (273 of 1,956), 4.3% of shell, 0.8% of soft-core and 1.6%
of core (165 of 10,433). They are more common in the cloud than in the core.

![Number of pangenes mostly unsupported, no filtering](08_Pangenome_Visualisation/pangenome_plots/Afum7b_occupancy_unsupported_only.png)

![Percentage of pangenes mostly unsupported, no filtering](08_Pangenome_Visualisation/pangenome_plots/Afum7b_occupancy_unsupported_percent.png)

![Share of unsupported genes by category, no filtering](08_Pangenome_Visualisation/pangenome_plots/Afum7b_unsupported_share.png)

**Share of unsupported genes by category** - same layout as the share figure above, split by how many of the genes of a
pangene are unsupported.

**InterPro term enrichment** - same test as above, 8,052 core and 814 cloud pangenes with an InterPro entry, and 1,061
entries tested. Cloud: 47 entries are enriched; core: 6. The cloud hits include the same domains of unknown function,
acyl transferase and protein kinase-like domains, and the orsellinic acid/F9775 biosynthesis cluster protein D, which may
point to secondary metabolite clusters.

![InterPro term enrichment, no filtering](08_Pangenome_Visualisation/pangenome_plots/Afum7b_domain_enrichment.png)

---

[↑ Back to top](#analysis-steps) &nbsp;|&nbsp; [Back to Pangenome Pipeline](../../README.md)

