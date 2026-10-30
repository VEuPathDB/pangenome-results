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
| [07 – Post-GET_PANGENES Adjusting and Visualisation](README.md#07--post-get_pangenes-adjusting-and-visualisation) | Manual review and refinement of pangene calls | 🔄 In progress |
| 08 – Pangenome Visualisation | Figures, presence/absence matrix, summary stats (prototype flow; now part of step 07) | ✅ Complete |
| [Redundancy check](README.md#redundancy-check-on-the-final-panel) | Duplicated contigs in the final panel | ✅ Complete |
| [09 – Redundant Contig Removal](README.md#09--redundant-contig-removal) | Genes of the redundant contigs removed from the GFFs and pangene matrices (*T. gondii* only) | ✅ Complete |

---

## Key results so far

### 01 – Genome Selection & QC

- **15 strains selected** from ToxoDB. 4 additional strains were excluded due to absence of gene annotation. As expected, the 14 strains compared with the reference ME49 all have high whole-genome ANI against it (98.7–99.7%).
- **Small contigs are numerous and gene-bearing.** The panel contains **34,066 sub-10kb contigs** — 93–99% of each genome's contig count — except RH-88, which is a notably
  cleaner assembly (only 62 small contigs). These small contigs carry
  **2,388 protein-coding genes** across the panel, including 289 known SRS/ROP/GRA/RON/AP2/MIC
  virulence-family genes and ~636 organelle-genome genes.
- **Organelle and redundant-contig screening were not run at this stage.** The protocol calls for removing organellar and redundant contigs. For *T. gondii*, these could not be identified reliably: organellar sequences occur across multiple contigs that are not consistently labeled, and nuclear contigs may contain organellar fragments (NUMTs/NUPTs). The origin of many small contigs also remains uncertain: they may be assembly artifacts, fragments of the unusual organellar genomes. As a panel-wide rule, **all contigs shorter than 10 kb were therefore excluded** instead of being classified individually. It removed 2,388 annotated genes. A redundancy screen was run later, on the final panel (see *Redundancy check on the final panel* below).
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

- Each strain's annotation is rebuilt from the reference's transferred genes, the strain's own genes
  and genes transferred from the other strains, giving **9,249–9,933 protein-coding genes per
  strain**. Non-coding RNA genes (tRNA, rRNA, ncRNA) are left out, because they were being typed as
  ordinary genes on the way.
- Two versions of the annotation go on to `get_pangenes`: **with filtering** (7a) and **no
  filtering** (7b, genes only tagged).
- The filter removed **6.7% of the genes** (9,710 of 144,359; 6.1–8.4% per strain). Two thirds of
  them overlapped a reference gene and had no evidence themselves; a quarter were low-coverage
  transfers from other strains.
- CDS-overlapping gene pairs fall from 476–552 per strain to 67–77.

### 06 – GET_PANGENES

- **11,031 pangenes without filtering** and **9,904 with filtering**, across the 15 strains.

### 07 – Post-GET_PANGENES Adjusting *(in progress)*

- **13.6% of the pangenes (1,501 without filtering, 1,374 with filtering) hold more than one gene of
  the same strain.** They are not overlapping genes (only 0.1% of the pairs overlap in the CDS):
  they are same-strand neighbours, 83% within 5 kb. Whether they are tandem copies or one gene
  split in two is still open.

### 08 – Pangenome Visualisation

- **The pangenome is still growing.** Adding the 15th strain still adds about 100 pangenes without filtering and about 70 with filtering.
  The core is 8,733 pangenes (79%) without filtering and 8,281 (84%) with filtering; 13% and 10% of the pangenes are in one strain only.
- **The cloud looks different from the core.** Cloud pangenes have shorter proteins (median 212 aa against 477 aa in the core, no filtering),
  fewer domains (40% of genes against 55%), and sit more often on short contigs (19% below 200 kb against 0.4% of the core).
- **Many cloud pangenes have genes without a valid ORF:** 68% without filtering and 50% with filtering, against 2-4% of the core. The
  singletons of this kind are almost all Liftoff transfers of the lowest-confidence layer, not genes of a strain's own annotation.
- **InterPro enrichment.** The cloud is enriched in dynein heavy chain (a long gene that may be annotated in pieces) and polyketide synthase
  domains; the core in methyltransferase, MFS transporter, WD40 and tetratricopeptide domains. The cytochrome b/b6 entries in the cloud may
  be organelle DNA inserted in the nucleus or poor transfers; this was not tested.
- Preliminary: pangenes with more than one gene of the same strain are not resolved yet.

### Redundancy check on the final panel

- Only **RH88** (100 flagged contigs, 1.7 Mb) and **ME49** (6 contigs, 94 kb) have contigs that are duplicated in their own assembly; the other
  13 strains have none. Contigs with no gene do not matter for the pangenome.

### 09 – Redundant Contig Removal

- The genes of the flagged contigs that carry genes, plus the contigs just under the cut (41 contigs, 0.93 Mb, 144 genes), were removed from the
  GFFs and the pangene matrices, without redoing the annotation. The original files were kept for comparison.
- The pangenome goes from 11,031 to 10,922 pangenes without filtering; all the pangenes removed are cloud, and the core does not change.
  RH88 goes from 226 to 145 singletons.

---

## Important caveats

- **Small contigs are being dropped by an arbitrary length cutoff, not per-strain review.**
  Unlike the Afum panel (which was largely chromosome-scale after cleanup), most *T. gondii*
  assemblies are highly fragmented (thousands of scaffolds). Rather than reviewing each small
  contig individually, the panel drops every contig <10kb outright — a simple blanket rule
  that knowingly costs 2,388 real genes (289 known virulence-family genes among them). It was
  applied to every strain.
- **Organellar DNA (NUMTs/NUPTs) is abundant and strain-variable.** *T. gondii* carries
  >11,000 organellar DNA insertions (>1 Mb) in the nuclear genome, and unlike Afum, two
  organelles must be screened — the mitochondrion and the apicoplast. Most hits will be
  genuine nuclear insertions to keep, not whole-organelle contigs to drop.
- **Lineage-specific copy-number variation at key loci** (e.g. ROP5: 6 copies in Type I/III
  vs. 11 in Type II) will appear as gene gain/loss in the pangenome matrix. These loci
  require manual review rather than relying on the matrix alone.
- **Pangenes with more than one gene per strain, and fragmented gene models, are not resolved yet.**
  They can inflate the cloud (singletons and low-occupancy pangenes), so cloud-related figures and
  enrichments are preliminary.
- **Invalid ORFs in the cloud.** A large share of the cloud is made of transfers with a broken ORF, so cloud-related figures may overstate
  the strain-specific content; additional filtering could be considered.
- The pangenome matrix captures **gene presence/absence only** — virulence differences
  between lineages are driven largely by allelic variation within shared genes (ROP kinases,
  GRA effectors, SRS surface antigens), which require separate targeted analyses.

---


[↑ Back to top](#analysis-progress) &nbsp;|&nbsp; [Back to Pangenome Pipeline](../../README.md)
