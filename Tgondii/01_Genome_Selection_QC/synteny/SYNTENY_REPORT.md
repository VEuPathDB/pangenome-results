### Synteny vs ME49  (minimap2 -x asm10, alignments ≥2000 bp)

| Strain | Query pieces (clean) | ME49 covered | Aln identity¹ | Raw % rev² | Internal inv.³ | Verdict |
| :--- | ---: | ---: | ---: | ---: | ---: | :--- |
| **ARI** | 123 (121) | 62.3 Mb (94.9%) | 91.9% | 50% | 0.00 Mb (0.0%) | Collinear — 1:1, no rearrangements |
| **CAST** | 120 (116) | 62.2 Mb (94.7%) | 83.1% | 54% | 0.07 Mb (0.1%) | Collinear — 1:1, no rearrangements |
| **COUG** | 130 (127) | 62.3 Mb (94.9%) | 87.0% | 52% | 0.00 Mb (0.0%) | Collinear — 1:1, no rearrangements |
| **FOU** | 197 (186) | 61.7 Mb (94.1%) | 82.4% | 58% | 0.00 Mb (0.0%) | Collinear — 1:1, no rearrangements |
| **GAB2-2007-GAL-DOM2** | 127 (119) | 62.1 Mb (94.7%) | 86.8% | 43% | 0.00 Mb (0.0%) | Collinear — 1:1, no rearrangements |
| **GT1** | 518 (512) | 62.6 Mb (95.4%) | 85.1% | 2% | 0.00 Mb (0.0%) | Collinear — 1:1, no rearrangements |
| **MAS** | 256 (250) | 61.3 Mb (93.4%) | 83.7% | 48% | 0.00 Mb (0.0%) | 1 scaffold(s) joining ≥2 ref chroms end-to-end |
| **RH88** | 169 (78) | 62.9 Mb (95.8%) | 83.3% | 27% | 0.51 Mb (0.8%) | 1 inversion block(s) ≥20kb (0.51 Mb); 1 scaffold(s) joining ≥2 ref chroms end-to-end |
| **RUB** | 154 (139) | 62.1 Mb (94.6%) | 82.1% | 53% | 0.07 Mb (0.1%) | Collinear — 1:1, no rearrangements |
| **TgCATBr9** | 164 (153) | 61.9 Mb (94.3%) | 82.5% | 46% | 0.00 Mb (0.0%) | Collinear — 1:1, no rearrangements |
| **TgCatPRC2** | 165 (155) | 62.1 Mb (94.6%) | 88.7% | 38% | 0.07 Mb (0.1%) | Collinear — 1:1, no rearrangements |
| **VAND** | 158 (150) | 62.0 Mb (94.5%) | 83.1% | 60% | 0.07 Mb (0.1%) | Collinear — 1:1, no rearrangements |
| **VEG** | 249 (241) | 62.6 Mb (95.4%) | 88.5% | 1% | 0.00 Mb (0.0%) | Collinear — 1:1, no rearrangements |
| **p89** | 171 (164) | 61.9 Mb (94.4%) | 82.8% | 51% | 0.00 Mb (0.0%) | Collinear — 1:1, no rearrangements |

¹ minimap2 gap-compressed identity over aligned regions only; depressed by divergent repeats — whole-genome ANI is the better divergence metric.  
² fraction of aligned bp on the reverse strand *before* per-contig orientation correction; for scaffold assemblies this is ~coin-flip scaffold orientation, not biology.  
³ alignment blocks ≥20 kb that run against their own query contig's dominant orientation on the same reference chromosome — the orientation-corrected inversion signal.

#### Per-strain detail

**ARI** — 141 alignments, 123 query pieces (121 clean 1:1), 62.27 Mb of ME49 covered (94.9%), identity 91.9%.  
  Inversions: none ≥20 kb.  
  Multi-chrom scaffold KQ973612: chrX 2651 kb, chrIII 84 kb [join].  

**CAST** — 142 alignments, 120 query pieces (116 clean 1:1), 62.17 Mb of ME49 covered (94.7%), identity 83.1%.  
  Inversions: chrIX:4,973,697-5,043,090 (69 kb).  
  Multi-chrom scaffold ML130701: chrX 3252 kb, chrIII 84 kb [join].  

**COUG** — 144 alignments, 130 query pieces (127 clean 1:1), 62.27 Mb of ME49 covered (94.9%), identity 87.0%.  
  Inversions: none ≥20 kb.  
  Multi-chrom scaffold KZ624870.1: chrX 1177 kb, chrIII 79 kb [join].  

**FOU** — 221 alignments, 197 query pieces (186 clean 1:1), 61.74 Mb of ME49 covered (94.1%), identity 82.4%.  
  Inversions: none ≥20 kb.  
  Multi-chromosome scaffolds: none ≥50 kb.  

**GAB2-2007-GAL-DOM2** — 144 alignments, 127 query pieces (119 clean 1:1), 62.15 Mb of ME49 covered (94.7%), identity 86.8%.  
  Inversions: none ≥20 kb.  
  Multi-chromosome scaffolds: none ≥50 kb.  

**GT1** — 532 alignments, 518 query pieces (512 clean 1:1), 62.63 Mb of ME49 covered (95.4%), identity 85.1%.  
  Inversions: none ≥20 kb.  
  Multi-chromosome scaffolds: none ≥50 kb.  

**MAS** — 270 alignments, 256 query pieces (250 clean 1:1), 61.29 Mb of ME49 covered (93.4%), identity 83.7%.  
  Inversions: none ≥20 kb.  
  Multi-chrom scaffold KN044652: chrIX 338 kb, chrX 72 kb [join].  
  Multi-chrom scaffold KN044667: chrIII 190 kb, chrX 105 kb [join].  

**RH88** — 542 alignments, 169 query pieces (78 clean 1:1), 62.86 Mb of ME49 covered (95.8%), identity 83.3%.  
  Inversions: chrIV:2,172,002-2,686,594 (515 kb).  
  Multi-chrom scaffold CM023089: chrVIII 6976 kb, chrVIIb 5069 kb [join].  
  Multi-chrom scaffold CM023091: chrX 7484 kb, chrIII 85 kb [join].  
  Multi-chrom scaffold CM023087: chrVI 3656 kb, chrV 55 kb [segdup], chrXII 51 kb [join].  
  Multi-chrom scaffold CM023086: chrV 3289 kb, KE139425 72 kb [segdup].  
  Multi-chrom scaffold CM023083: chrII 2345 kb, KE139427 37 kb [join], KE139822 36 kb [join], KE139848 21 kb [join].  

**RUB** — 192 alignments, 154 query pieces (139 clean 1:1), 62.10 Mb of ME49 covered (94.6%), identity 82.1%.  
  Inversions: chrIX:4,973,942-5,043,090 (69 kb).  
  Multi-chromosome scaffolds: none ≥50 kb.  

**TgCATBr9** — 195 alignments, 164 query pieces (153 clean 1:1), 61.90 Mb of ME49 covered (94.3%), identity 82.5%.  
  Inversions: none ≥20 kb.  
  Multi-chromosome scaffolds: none ≥50 kb.  

**TgCatPRC2** — 192 alignments, 165 query pieces (155 clean 1:1), 62.06 Mb of ME49 covered (94.6%), identity 88.7%.  
  Inversions: chrIX:4,973,697-5,045,469 (72 kb).  
  Multi-chrom scaffold KQ983300: chrVIIa 303 kb, chrVI 63 kb [join].  

**VAND** — 188 alignments, 158 query pieces (150 clean 1:1), 62.03 Mb of ME49 covered (94.5%), identity 83.1%.  
  Inversions: chrIX:4,973,825-5,043,090 (69 kb).  
  Multi-chrom scaffold KN042487: chrXI 1213 kb, chrXII 79 kb [join].  

**VEG** — 273 alignments, 249 query pieces (241 clean 1:1), 62.63 Mb of ME49 covered (95.4%), identity 88.5%.  
  Inversions: none ≥20 kb.  
  Multi-chromosome scaffolds: none ≥50 kb.  

**p89** — 194 alignments, 171 query pieces (164 clean 1:1), 61.94 Mb of ME49 covered (94.4%), identity 82.8%.  
  Inversions: none ≥20 kb.  
  Multi-chromosome scaffolds: none ≥50 kb.  
