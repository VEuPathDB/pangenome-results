# *Aspergillus fumigatus* Pangenome — Summary

> **Quick read for an overview of the analysis and key findings.**
> For the full technical report — methods, parameters, tables, and figures — see
> [README.md](README.md).

---


## Analysis progress

| Step | Description | Status |
| :--- | :--- | :---: |
| [01 – Genome Selection & QC](README.md#01--genome-selection--qc) | Strain selection, species check, organelle removal, synteny | ✅ Complete |
| [02 – TE Annotation & Clean Up](README.md#02--te-annotation--clean-up) | Transposable element annotation, TE-gene overlap filtering | ✅ Complete |
| [03 – *de novo* Genome Annotation](README.md#03--de-novo-genome-annotation) | Gene prediction on cleaned assemblies | ⏭️ Not needed (all strains already annotated) |
| [04 – Protein evidence (InterProScan and PSAURON)](README.md#04--protein-evidence-interproscan-and-psauron) | Functional domain annotation; PSAURON scores | ✅ Complete |
| [05 – Cross-genome Annotation Integration](README.md#05--cross-genome-annotation-integration) | Merging and standardising annotations across strains | ✅ Complete |
| [06 – GET_PANGENES](README.md#06--get_pangenes) | Synteny-based ortholog clustering (core / accessory) | ✅ Complete |
| [07 – Post-GET_PANGENES Adjusting and Visualisation](README.md#07--post-get_pangenes-adjusting-and-visualisation) | Manual review and refinement of pangene calls | 🔄 In progress |
| 08 – Pangenome Visualisation | Figures, presence/absence matrix, summary stats (prototype flow; now part of step 07) | ✅ Complete |

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
  alignment identity) and should be interpreted with caution.

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

- Each strain's annotation is rebuilt from the reference's transferred genes, the strain's own genes and genes transferred from the other strains,
  as in the *T. gondii* panel. Two versions go on to `get_pangenes`: **with filtering** (7a) and **no filtering** (7b, genes only tagged).
- The filter removed **2.2% of the genes** (4,307 of 192,136; 1.9-2.7% per strain), leaving 10,838 to 11,509 genes per strain.

### 06 – GET_PANGENES

- **12,984 pangenes with filtering** and **13,693 without**, across the 17 strains.

### 07 – Post-GET_PANGENES Adjusting *(in progress)*

- Not analysed yet. About 3% of the pangenes hold more than one gene of the same strain (443 with filtering, 454 without).

### 08 – Pangenome Visualisation

- **The pangenome is still growing:** adding the 17th strain still adds about 70 pangenes with filtering and about 97 without. The core is
  10,254 pangenes (79%) with filtering and 10,433 (76%) without; 9% and 12% of the pangenes are in one strain only. ATCC 46645 has the most
  singletons (213 and 230).
- **The cloud looks different from the core.** Cloud pangenes have shorter proteins (median 204 aa against 383 aa in the core, no filtering),
  fewer domains (42% of genes against 77%), and sit more often on contigs below 200 kb (11% against none of the core).
- **Many cloud pangenes have genes without a valid ORF:** 39% with filtering and 57% without, against about 2% of the core. Without filtering,
  14% of the cloud pangenes are mostly made of overlapping genes with no domain or specific description, against 1.6% of the core.
- **InterPro enrichment.** The cloud is enriched in domains of unknown function (DUF3435, DUF3723), acyl transferase and protein kinase-like
  domains; without filtering also in the orsellinic acid biosynthesis cluster protein D. The DUFs may point to Starship elements, to be confirmed.
  The core is enriched in the armadillo-type fold, sugar transporter and OB-fold domains.
- Preliminary: pangenes with more than one gene of the same strain are not resolved yet.

---

## Important caveats

- Two strains (**A1160** and **A1163**) are derived laboratory strains from the CEA10
  lineage and carry engineered sequences (a *Aspergillus niger* gene in A1163; a
  zeocin-resistance cassette replacing *akuB* in A1160). These sequences will appear as
  "accessory" but are **lab artefacts, not biology**.
- The synteny-based approach requires chromosome-level assemblies for the most reliable calls.
  Sub-telomeric accessory regions — where most lineage-specific genes live — are the least
  certain part of any pangenome, including this one.
- **Invalid ORFs in the cloud.** A large share of the cloud is made of transfers with a broken ORF, so cloud-related figures may overstate
  the strain-specific content; additional filtering could be considered.
- The pangenome matrix captures **gene presence/absence only**. Azole resistance in
  *A. fumigatus* is driven largely by *sequence variants within* core genes (e.g., *cyp51A*
  promoter repeats + coding substitutions), which require a separate targeted analysis.

---

## Files

| File | Description |
| :--- | :--- |
| [README.md](README.md) | Full technical report — all methods, parameters, tables, figures |
| [genome_order.txt](genome_order.txt) | Ordered list of the 17 strains used |
| [01_Genome_Selection_QC/](01_Genome_Selection_QC/) | QC outputs: ANI, synteny, organelle and redundancy screens |
| [02_TE_annotation_Clean_Up/](02_TE_annotation_Clean_Up/) | TE library, RepeatMasker results, TE-gene overlap |
| 03_denovo_Genome_Annotation/ | *de novo* gene predictions |
| 04_InterProScan/ | Domain annotations |
| [05_Cross-genome_annotation_integration/](05_Cross-genome_annotation_integration/) | Merged annotation files |
| 06_GET_PANGENES/ | Pangene clusters |
| [07_Post_GET_PANGENES_adjusting/](07_Post_GET_PANGENES_adjusting/) | Reviewed and curated pangene calls |
| 08_Pangenome_Visualisation/ | Figures and summary tables |

---

[↑ Back to top](#analysis-progress) &nbsp;|&nbsp; [Back to Pangenome Pipeline](../../README.md)
