### Synteny vs AF293  (minimap2 -x asm10, alignments ≥2000 bp)

| Strain | Query pieces (clean) | AF293 covered | Aln identity¹ | Raw % rev² | Internal inv.³ | Verdict |
| :--- | ---: | ---: | ---: | ---: | ---: | :--- |
| **A1160** | 10 (9) | 28.4 Mb (96.6%) | 89.4% | 60% | 0.03 Mb (0.1%) | 2 scaffold(s) joining ≥2 ref chroms end-to-end |
| **A1163** | 28 (23) | 28.2 Mb (95.9%) | 89.9% | 31% | 0.03 Mb (0.1%) | 3 scaffold(s) joining ≥2 ref chroms end-to-end |
| **GCA_040126065.1** | 9 (9) | 28.1 Mb (95.8%) | 90.2% | 58% | 0.00 Mb (0.0%) | Collinear — 1:1, no rearrangements |
| **GCA_040142845.1** | 15 (14) | 28.2 Mb (96.0%) | 90.3% | 31% | 0.03 Mb (0.1%) | 3 scaffold(s) joining ≥2 ref chroms end-to-end |
| **GCA_040142855.1** | 12 (10) | 28.4 Mb (96.6%) | 90.1% | 68% | 0.00 Mb (0.0%) | Collinear — 1:1, no rearrangements |
| **GCA_040142865.1** | 26 (20) | 28.4 Mb (96.6%) | 90.3% | 70% | 0.00 Mb (0.0%) | Collinear — 1:1, no rearrangements |
| **GCA_040142875.1** | 16 (15) | 28.4 Mb (96.7%) | 89.5% | 32% | 0.02 Mb (0.1%) | Collinear — 1:1, no rearrangements |
| **GCA_040142885.1** | 9 (9) | 28.0 Mb (95.4%) | 88.1% | 34% | 0.00 Mb (0.0%) | Collinear — 1:1, no rearrangements |
| **GCA_040142945.1** | 13 (13) | 28.1 Mb (95.5%) | 88.1% | 33% | 0.00 Mb (0.0%) | Collinear — 1:1, no rearrangements |
| **GCA_040142955.1** | 20 (15) | 28.2 Mb (96.1%) | 86.7% | 68% | 1.40 Mb (4.8%) | 3 inversion block(s) ≥20kb (1.40 Mb); 2 scaffold(s) joining ≥2 ref chroms end-to-end |
| **GCA_040142975.1** | 22 (20) | 28.3 Mb (96.3%) | 89.3% | 43% | 0.45 Mb (1.6%) | 1 inversion block(s) ≥20kb (0.45 Mb) |
| **GCA_040167795.1** | 10 (9) | 28.1 Mb (95.8%) | 85.8% | 51% | 0.73 Mb (2.6%) | 2 inversion block(s) ≥20kb (0.73 Mb) |
| **GCA_040167805.1** | 25 (20) | 27.7 Mb (94.2%) | 88.8% | 60% | 0.00 Mb (0.0%) | Collinear — 1:1, no rearrangements |
| **GCA_058970245.1** | 8 (7) | 28.2 Mb (96.0%) | 85.4% | 65% | 0.73 Mb (2.6%) | 2 inversion block(s) ≥20kb (0.73 Mb) |
| **GCA_058972525.1** | 12 (10) | 28.3 Mb (96.2%) | 85.0% | 20% | 0.71 Mb (2.5%) | 1 inversion block(s) ≥20kb (0.71 Mb) |
| **GCA_058972625.1** | 10 (9) | 27.9 Mb (95.0%) | 88.0% | 35% | 0.71 Mb (2.5%) | 1 inversion block(s) ≥20kb (0.71 Mb) |

¹ minimap2 gap-compressed identity over aligned regions only; depressed by divergent repeats — whole-genome ANI is the better divergence metric.  
² fraction of aligned bp on the reverse strand *before* per-contig orientation correction; for scaffold assemblies this is ~coin-flip scaffold orientation, not biology.  
³ alignment blocks ≥20 kb that run against their own query contig's dominant orientation on the same reference chromosome — the orientation-corrected inversion signal.

#### Per-strain detail

**A1160** — 53 alignments, 10 query pieces (9 clean 1:1), 28.37 Mb of AF293 covered (96.6%), identity 89.4%.  
  Inversions: Chr7:1,807,654-1,840,596 (33 kb).  
  Multi-chrom scaffold CM044372.1: Chr1 4402 kb, Chr6 495 kb [join].  
  Multi-chrom scaffold CM044377.1: Chr6 3204 kb, Chr1 185 kb [segdup], Chr8 72 kb [join], Chr7 69 kb [join].  
  Multi-chrom scaffold CM044378.1: Chr7 1860 kb, Chr6 76 kb [join].  
  Multi-chrom scaffold CM044379.1: Chr8 1824 kb, Chr7 49 kb [join], Chr5 25 kb [join].  

**A1163** — 75 alignments, 28 query pieces (23 clean 1:1), 28.17 Mb of AF293 covered (95.9%), identity 89.9%.  
  Inversions: Chr7:1,807,654-1,840,596 (33 kb).  
  Multi-chrom scaffold scf_000001_A_fumigatus_A1163: Chr1 4400 kb, Chr6 495 kb [join].  
  Multi-chrom scaffold scf_000006_A_fumigatus_A1163: Chr6 1908 kb, Chr1 107 kb [join], Chr8 72 kb [join].  
  Multi-chrom scaffold scf_000007_A_fumigatus_A1163: Chr8 1819 kb, Chr7 76 kb [join].  
  Multi-chrom scaffold scf_000008_A_fumigatus_A1163: Chr7 1740 kb, Chr6 76 kb [join].  
  Multi-chrom scaffold scf_000009_A_fumigatus_A1163: Chr6 1267 kb, Chr1 79 kb [join], Chr7 66 kb [join].  

**GCA_040126065.1** — 36 alignments, 9 query pieces (9 clean 1:1), 28.15 Mb of AF293 covered (95.8%), identity 90.2%.  
  Inversions: none ≥20 kb.  
  Multi-chromosome scaffolds: none ≥50 kb.  

**GCA_040142845.1** — 65 alignments, 15 query pieces (14 clean 1:1), 28.19 Mb of AF293 covered (96.0%), identity 90.3%.  
  Inversions: Chr1:4,883,841-4,915,540 (32 kb).  
  Multi-chrom scaffold CM079236.1: Chr3 3955 kb, Chr6 1190 kb [join].  
  Multi-chrom scaffold CM079234.1: Chr1 4370 kb, Chr4 364 kb [segdup], Chr2 23 kb [segdup].  
  Multi-chrom scaffold JBBFMX010000005.1: Chr4 2880 kb, Chr1 191 kb [join].  
  Multi-chrom scaffold CM079238.1: Chr6 2538 kb, Chr3 116 kb [join].  

**GCA_040142855.1** — 56 alignments, 12 query pieces (10 clean 1:1), 28.39 Mb of AF293 covered (96.6%), identity 90.1%.  
  Inversions: none ≥20 kb.  
  Multi-chrom scaffold CM079226.1: Chr8 1825 kb, Chr7 251 kb [segdup], Chr5 21 kb [join].  

**GCA_040142865.1** — 108 alignments, 26 query pieces (20 clean 1:1), 28.38 Mb of AF293 covered (96.6%), identity 90.3%.  
  Inversions: none ≥20 kb.  
  Multi-chrom scaffold JBBFMV010000004.1: Chr6 2425 kb, Chr1 268 kb [segdup].  
  Multi-chrom scaffold JBBFMV010000003.1: Chr4 2441 kb, Chr7 188 kb [segdup].  

**GCA_040142875.1** — 101 alignments, 16 query pieces (15 clean 1:1), 28.40 Mb of AF293 covered (96.7%), identity 89.5%.  
  Inversions: Chr7:1,943,701-1,965,352 (22 kb).  
  Multi-chrom scaffold JBBFMU010000008.1: Chr7 1194 kb, Chr1 96 kb [segdup], Chr5 31 kb [join].  
  Multi-chrom scaffold JBBFMU010000009.1: Chr5 1131 kb, Chr6 65 kb [segdup].  
  Multi-chrom scaffold JBBFMU010000010.1: Chr7 716 kb, Chr2 34 kb [segdup], Chr3 24 kb [segdup].  

**GCA_040142885.1** — 37 alignments, 9 query pieces (9 clean 1:1), 28.02 Mb of AF293 covered (95.4%), identity 88.1%.  
  Inversions: none ≥20 kb.  
  Multi-chromosome scaffolds: none ≥50 kb.  

**GCA_040142945.1** — 57 alignments, 13 query pieces (13 clean 1:1), 28.06 Mb of AF293 covered (95.5%), identity 88.1%.  
  Inversions: none ≥20 kb.  
  Multi-chromosome scaffolds: none ≥50 kb.  

**GCA_040142955.1** — 137 alignments, 20 query pieces (15 clean 1:1), 28.23 Mb of AF293 covered (96.1%), identity 86.7%.  
  Inversions: Chr6:2,928,545-3,728,695 (800 kb); Chr6:31,894-418,092 (386 kb); Chr1:4,400,414-4,610,243 (210 kb).  
  Multi-chrom scaffold JBBFMY010000001.1: Chr1 4178 kb, Chr7 158 kb [join].  
  Multi-chrom scaffold JBBFMY010000004.1: Chr4 2434 kb, Chr7 64 kb [join].  
  Multi-chrom scaffold JBBFMY010000011.1: Chr6 1003 kb, Chr2 75 kb [join], Chr3 57 kb [segdup], Chr4 57 kb [segdup].  
  Multi-chrom scaffold JBBFMY010000013.1: Chr5 582 kb, Chr7 148 kb [join], Chr6 78 kb [join].  

**GCA_040142975.1** — 77 alignments, 22 query pieces (20 clean 1:1), 28.29 Mb of AF293 covered (96.3%), identity 89.3%.  
  Inversions: Chr8:668,381-1,121,256 (453 kb).  
  Multi-chrom scaffold CM079250.1: Chr3 4087 kb, Chr7 53 kb [segdup].  
  Multi-chrom scaffold JBBFNB010000005.1: Chr4 2452 kb, Chr7 206 kb [segdup].  

**GCA_040167795.1** — 64 alignments, 10 query pieces (9 clean 1:1), 28.14 Mb of AF293 covered (95.8%), identity 85.8%.  
  Inversions: Chr2:789,133-1,496,307 (707 kb); Chr1:29,024-54,868 (26 kb).  
  Multi-chrom scaffold CM079253.1: Chr1 4594 kb, Chr7 164 kb [segdup], Chr8 97 kb [segdup].  
  Multi-chrom scaffold CM079256.1: Chr6 3673 kb, Chr3 77 kb [segdup].  

**GCA_040167805.1** — 102 alignments, 25 query pieces (20 clean 1:1), 27.68 Mb of AF293 covered (94.2%), identity 88.8%.  
  Inversions: none ≥20 kb.  
  Multi-chromosome scaffolds: none ≥50 kb.  

**GCA_058970245.1** — 41 alignments, 8 query pieces (7 clean 1:1), 28.22 Mb of AF293 covered (96.0%), identity 85.4%.  
  Inversions: Chr2:789,133-1,496,307 (707 kb); Chr1:29,024-54,868 (26 kb).  
  Multi-chrom scaffold CM179774.1: Chr1 4589 kb, Chr7 164 kb [segdup].  

**GCA_058972525.1** — 42 alignments, 12 query pieces (10 clean 1:1), 28.27 Mb of AF293 covered (96.2%), identity 85.0%.  
  Inversions: Chr2:789,133-1,496,307 (707 kb).  
  Multi-chrom scaffold CM180069.1: Chr2 4791 kb, Chr7 164 kb [segdup], Chr1 87 kb [segdup], Chr6 78 kb [segdup].  
  Multi-chrom scaffold CM180072.1: Chr6 3670 kb, Chr7 251 kb [segdup].  

**GCA_058972625.1** — 46 alignments, 10 query pieces (9 clean 1:1), 27.91 Mb of AF293 covered (95.0%), identity 88.0%.  
  Inversions: Chr2:789,133-1,496,307 (707 kb).  
  Multi-chrom scaffold CM180078.1: Chr6 3577 kb, Chr4 113 kb [segdup].  
