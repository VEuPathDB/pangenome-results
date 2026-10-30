# *Toxoplasma gondii* Pangenome — Summary

> **Quick read for an overview of the analysis and key findings.**
> For the full technical report — methods, parameters, tables, and figures — see
> [README.md](README.md).

---


## Analysis progress

| Step | Description | Status |
| :--- | :--- | :---: |
| [01 – Genome Selection & QC](README.md#01--genome-selection--qc) | Strain selection, species check, contig profiling, synteny | ✅ Complete |
| [02 – TE Annotation & Clean Up](README.md#02--te-annotation--clean-up) | Transposable element annotation, candidate validation | ✅ Complete |
| [03 – *de novo* Genome Annotation](README.md#03--de-novo-genome-annotation) | Gene prediction on cleaned assemblies | ⏭️ Not needed |
| [04 – Protein evidence (InterProScan and PSAURON)](README.md#04--protein-evidence-interproscan-and-psauron) | Functional domain annotation; PSAURON scores | ✅ Complete |
| [05 – Cross-genome Annotation Integration](README.md#05--cross-genome-annotation-integration) | Merging and standardising annotations across strains | ✅ Complete |
| [06 – GET_PANGENES](README.md#06--get_pangenes) | Synteny-based ortholog clustering (core / accessory) | ✅ Complete |
| [07 – Post-GET_PANGENES Adjusting and Visualisation](README.md#07--post-get_pangenes-adjusting-and-visualisation) | Safe fix, figures and explorer (done); curation and removal of false genes | 🔄 In progress |

---

## Key results so far

### 01 – Genome Selection & QC

- **15 strains selected** from ToxoDB. 4 additional strains were excluded due to absence of gene annotation. As expected, the 14 strains compared with the reference ME49 all have high whole-genome ANI against it (98.7–99.7%).
- **Small contigs are numerous and gene-bearing.** The panel contains **34,066 sub-10kb contigs** — 93–99% of each genome's contig count — except RH-88, which is a notably
  cleaner assembly (only 62 small contigs). These small contigs carry
  **2,388 protein-coding genes** across the panel, including 289 known SRS/ROP/GRA/RON/AP2/MIC
  virulence-family genes and ~636 organelle-genome genes.
- **All contigs shorter than 10 kb were excluded**, as a panel-wide rule, instead of classifying each small contig (their origin - assembly artifacts, organellar fragments - could not be told reliably). It removed 2,388 annotated genes.
- **Apicoplast and redundant contigs removed.** The apicoplast genome was found in 14 contigs of 10 genomes (blastn of ME49 `KE138841`); 41 contigs that duplicate part of a longer contig of the same assembly were found in ME49 and RH88. These 52 contigs (332 genes) are removed before the step 05 build. The mitochondrion was not screened (ME49 has no mitochondrial contig).
- **Chromosome structure and macro-synteny are highly conserved across all lineages.** 93.4–95.8% of the ME49 reference is covered in 1:1 collinear blocks, with no inter-chromosomal translocations or arm-scale rearrangements across any lineage. While scaffold-level dot-plots visually show frequent reverse alignments (~40–60% red), this reflects arbitrary scaffold deposition orientation. 
- **One recurrent inversion polymorphism identified:** a ~70 kb inverted block at the end
  of chromosome IX is shared by 4 strains (CAST, RUB, VAND, TgCatPRC2) — a real
  segregating variant, absent from the remaining 10 strains.
- **RH-88** carries a unique ~515 kb inversion on chromosome IV (prominently visible in the dot-plot) and is assembled as 13 chromosomes (one scaffold joins ME49 chrVIIb + chrVIII end-to-end), along with 4 chromosomes deposited in reverse orientation (chrX, chrVI, chrIII, chrIb).
- **Cross-chromosomal alignment at chrIII ↔ chrX (~80–85 kb):** In 5 independent strains (ARI, CAST, COUG, MAS, RH-88), the scaffold covering chromosome X carries a terminal segment that also aligns to the end of ME49 chromosome III. Because this identical pattern recurs across phylogenetically distant lineages, it is unlikely to reflect independent translocations or assembly chimeras in each strain; rather, it appears to indicate shared sequence homology (consistent with a subtelomeric segmental duplication) between chromosomes III and X within the ME49 reference itself.
- **Literature review pending on chromosomal observations:** A dedicated literature review is planned to further clarify these chromosome-level questions.

### 02 – TE Annotation & Clean Up

- ***T. gondii* has no bona fide transposable elements.** We know this from the literature,
  but we ran the TE candidate discovery pipeline anyway. As expected, no genuine *T. gondii*
  TE families were found — candidates were low-complexity / tandem satellite repeats or
  conserved sequences, not mobile elements.
- **Contaminant contigs**. Human L1 LINE elements were recovered as apparent TE candidates in multiple strains,
  including the reference genome ME49. They were recovered from short contigs, which the <10 kb filter of step 01 removes.
- **No GFF filtering was applied** — it is expected that the contaminants contigs were removed with the <10kb filter.

### 03 – *de novo* Genome Annotation

Not needed: all 15 strains already have a genome annotation (GFF, from ToxoDB/VEuPathDB).

### 04 – Protein evidence (InterProScan and PSAURON)

- InterProScan was run on every strain's proteins. 56–62% of the protein-coding genes of each
  strain carry an InterPro/PFAM domain, so no strain stands out as poorly annotated.

### 05 – Cross-genome Annotation Integration

- **Basket annotation.** The genes of all strains that lie at the same place form a basket; each basket gets one panel
  model (ME49's when it has one), written into every strain where it fits. **8,365 panel genes**: the 8,026 ME49 genes
  and 339 genes not in the ME49 annotation.
- **No gene is lost without a reason:** every gene of every strain's own annotation has a final model or a written
  reason. 143 real copies of a gene in one strain were kept apart; tandem arrays (e.g. ROP5, SRS) keep their copies.
- **7,900–8,159 genes per strain**, about 2,000 fewer than in their own annotations, mainly because genes annotated in
  pieces are replaced by one model. 4,153 genes were eliminated by the quality rules (PSAURON, < 100 aa, no valid ORF),
  half of them for PSAURON alone; 301–454 genes per strain were added where the strain had no gene.
- **94% of the genes have a valid ORF**; 4,414 have an ORF broken by the assembly (N or contig end).

### 06 – GET_PANGENES

- **8,386 pangenes** across the 15 strains.

### 07 – Post-GET_PANGENES Adjusting *(in progress)*

- **Safe fix:** 87 genes moved back to the pangene of their gene, and 50 genes that `get_pangenes` had split over
  several pangenes joined again. **8,264 pangenes**: 7,754 core (15 strains), 71 soft-core, 269 shell, 170 cloud.
- **The core settles at about 7,750 pangenes**; RH88 has the most singletons (55).
- **The cloud is enriched in cytochrome b / cytochrome c oxidase domains** (probably mitochondrial DNA in the nuclear
  assemblies), SRS domains and rhoptry kinases.
- 168 pangenes have an invalid ORF in more than half of their strains (69 of them with PSAURON < 0.5); they are the
  candidates for curation.
- Still to do: curation and removal of false genes, and the final figures.

---

## Important caveats

- **Small contigs are being dropped by an arbitrary length cutoff, not per-strain review.**
  Unlike the Afum panel (which was largely chromosome-scale after cleanup), most *T. gondii*
  assemblies are highly fragmented (thousands of scaffolds). Rather than reviewing each small
  contig individually, the panel drops every contig <10kb outright — a simple blanket rule
  that knowingly costs 2,388 real genes (289 known virulence-family genes among them). It was
  applied to every strain.
- **Organellar DNA (NUMTs/NUPTs) is abundant and strain-variable.** *T. gondii* carries
  >11,000 organellar DNA insertions (>1 Mb) in the nuclear genome. The apicoplast contigs were removed; the mitochondrion
  was not screened, and the cytochrome genes in the cloud are probably mitochondrial copies in the nuclear assemblies.
- **Lineage-specific copy-number variation at key loci** (e.g. ROP5: 6 copies in Type I/III
  vs. 11 in Type II) will appear as gene gain/loss in the pangenome matrix. These loci
  require manual review rather than relying on the matrix alone.
- **Some genes are still split over several pangenes.** 208 baskets remain split after the safe fix, where a pangene also
  holds genes of other baskets (e.g. neighbouring members of a gene family); they can inflate the cloud and are left for
  curation. 109 pangenes hold more than one gene of a strain.
- **The pangenome is preliminary** until the curation (removal of false genes) is done.
- The pangenome matrix captures **gene presence/absence only** — virulence differences
  between lineages are driven largely by allelic variation within shared genes (ROP kinases,
  GRA effectors, SRS surface antigens), which require separate targeted analyses.

---


[↑ Back to top](#analysis-progress) &nbsp;|&nbsp; [Back to Pangenome Pipeline](../../README.md)
