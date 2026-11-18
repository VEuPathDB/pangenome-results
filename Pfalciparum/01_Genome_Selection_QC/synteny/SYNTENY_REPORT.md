### Synteny vs 3D7  (minimap2 -x asm10, alignments ≥2000 bp)

| Strain | Query pieces (clean) | 3D7 covered | Aln identity¹ | Raw % rev² | Internal inv.³ | Verdict |
| :--- | ---: | ---: | ---: | ---: | ---: | :--- |
| **7G8-2019** | 22 (17) | 22.7 Mb (97.1%) | 86.2% | 1% | 0.00 Mb (0.0%) | 1 scaffold(s) joining ≥2 ref chroms end-to-end |
| **7G8** | 17 (16) | 22.6 Mb (96.9%) | 86.0% | 1% | 0.04 Mb (0.2%) | 2 scaffold(s) joining ≥2 ref chroms end-to-end |
| **CD01** | 19 (16) | 22.9 Mb (98.1%) | 83.7% | 2% | 0.00 Mb (0.0%) | 3 scaffold(s) joining ≥2 ref chroms end-to-end |
| **Dd2** | 16 (15) | 22.5 Mb (96.4%) | 85.8% | 2% | 0.07 Mb (0.3%) | 1 scaffold(s) joining ≥2 ref chroms end-to-end |
| **GA01** | 20 (15) | 22.7 Mb (97.3%) | 84.0% | 3% | 0.12 Mb (0.5%) | 3 scaffold(s) joining ≥2 ref chroms end-to-end |
| **GB4** | 26 (21) | 22.8 Mb (97.5%) | 84.5% | 4% | 0.00 Mb (0.0%) | 1 scaffold(s) joining ≥2 ref chroms end-to-end |
| **GN01** | 19 (16) | 23.2 Mb (99.3%) | 83.1% | 2% | 0.12 Mb (0.5%) | 1 inversion block(s) ≥20kb (0.12 Mb); 1 scaffold(s) joining ≥2 ref chroms end-to-end |
| **HB3** | 28 (25) | 22.5 Mb (96.6%) | 85.3% | 2% | 0.00 Mb (0.0%) | Collinear — 1:1, no rearrangements |
| **IT** | 27 (22) | 22.5 Mb (96.6%) | 84.1% | 3% | 0.03 Mb (0.1%) | 1 scaffold(s) joining ≥2 ref chroms end-to-end |
| **KE01** | 21 (19) | 22.6 Mb (96.8%) | 85.8% | 1% | 0.00 Mb (0.0%) | Collinear — 1:1, no rearrangements |
| **KH01** | 22 (16) | 22.8 Mb (97.8%) | 84.4% | 2% | 0.07 Mb (0.3%) | 2 scaffold(s) joining ≥2 ref chroms end-to-end |
| **KH02** | 21 (18) | 22.6 Mb (96.9%) | 84.8% | 2% | 0.00 Mb (0.0%) | 2 scaffold(s) joining ≥2 ref chroms end-to-end |
| **ML01** | 114 (75) | 23.0 Mb (98.6%) | 79.5% | 8% | 0.00 Mb (0.0%) | Collinear — 1:1, no rearrangements |
| **NF135C10** | 23 (18) | 22.7 Mb (97.3%) | 83.6% | 6% | 0.00 Mb (0.0%) | 6 scaffold(s) joining ≥2 ref chroms end-to-end |
| **NF166** | 32 (27) | 22.7 Mb (97.4%) | 85.4% | 1% | 0.00 Mb (0.0%) | Collinear — 1:1, no rearrangements |
| **NF54** | 30 (29) | 23.2 Mb (99.6%) | 95.3% | 1% | 0.00 Mb (0.0%) | Collinear — 1:1, no rearrangements |
| **SD01** | 19 (17) | 22.5 Mb (96.4%) | 85.9% | 1% | 0.00 Mb (0.0%) | Collinear — 1:1, no rearrangements |
| **SN01** | 36 (30) | 22.9 Mb (98.2%) | 84.3% | 3% | 0.03 Mb (0.1%) | Collinear — 1:1, no rearrangements |
| **TG01** | 79 (53) | 23.1 Mb (99.2%) | 78.3% | 6% | 0.00 Mb (0.0%) | 1 scaffold(s) joining ≥2 ref chroms end-to-end |

¹ minimap2 gap-compressed identity over aligned regions only; depressed by divergent repeats — whole-genome ANI is the better divergence metric.  
² fraction of aligned bp on the reverse strand *before* per-contig orientation correction; for scaffold assemblies this is ~coin-flip scaffold orientation, not biology.  
³ alignment blocks ≥20 kb that run against their own query contig's dominant orientation on the same reference chromosome — the orientation-corrected inversion signal.

#### Per-strain detail

**7G8-2019** — 60 alignments, 22 query pieces (17 clean 1:1), 22.66 Mb of 3D7 covered (97.1%), identity 86.2%.  
  Inversions: none ≥20 kb.  
  Multi-chrom scaffold VBRD01000020.1: v3 3284 kb, v3 90 kb [join].  
  Multi-chrom scaffold VBRD01000006.1: v3 1310 kb, v3 70 kb [join], v3 53 kb [join], v3 26 kb [segdup].  
  Multi-chrom scaffold VBRD01000017.1: v3 1265 kb, v3 78 kb [join].  

**7G8** — 56 alignments, 17 query pieces (16 clean 1:1), 22.61 Mb of 3D7 covered (96.9%), identity 86.0%.  
  Inversions: v3:1,491,771-1,534,828 (43 kb).  
  Multi-chrom scaffold Pf7G8_14: v3 3284 kb, v3 90 kb [join].  
  Multi-chrom scaffold Pf7G8_12: v3 2142 kb, v3 75 kb [join], v3 43 kb [join].  
  Multi-chrom scaffold Pf7G8_05: v3 1310 kb, v3 57 kb [join], v3 53 kb [join], v3 23 kb [join].  
  Multi-chrom scaffold Pf7G8_06: v3 1274 kb, v3 61 kb [join].  

**CD01** — 43 alignments, 19 query pieces (16 clean 1:1), 22.88 Mb of 3D7 covered (98.1%), identity 83.7%.  
  Inversions: none ≥20 kb.  
  Multi-chrom scaffold PfCD01_14: v3 3257 kb, v3 102 kb [join], v3 44 kb [join].  
  Multi-chrom scaffold PfCD01_12: v3 2134 kb, v3 60 kb [join], v3 47 kb [join].  
  Multi-chrom scaffold PfCD01_05: v3 1312 kb, v3 93 kb [segdup], v3 59 kb [join], v3 35 kb [join], v3 23 kb [join].  
  Multi-chrom scaffold PfCD01_01: v3 531 kb, v3 82 kb [segdup], v3 54 kb [join].  

**Dd2** — 63 alignments, 16 query pieces (15 clean 1:1), 22.50 Mb of 3D7 covered (96.4%), identity 85.8%.  
  Inversions: v3:325-48,585 (48 kb); v3:1,410,597-1,434,821 (24 kb).  
  Multi-chrom scaffold PfDd2_09: v3 1427 kb, v3 58 kb [join].  
  Multi-chrom scaffold PfDd2_05: v3 1304 kb, v3 47 kb [join], v3 36 kb [join], v3 30 kb [join], v3 28 kb [join].  
  Multi-chrom scaffold PfDd2_02: v3 829 kb, v3 54 kb [join].  

**GA01** — 54 alignments, 20 query pieces (15 clean 1:1), 22.70 Mb of 3D7 covered (97.3%), identity 84.0%.  
  Inversions: v3:1,296,676-1,413,730 (117 kb).  
  Multi-chrom scaffold PfGA01_14: v3 3271 kb, v3 89 kb [join], v3 52 kb [join].  
  Multi-chrom scaffold PfGA01_11: v3 2004 kb, v3 55 kb [join].  
  Multi-chrom scaffold PfGA01_10: v3 1600 kb, v3 109 kb [join].  
  Multi-chrom scaffold PfGA01_05: v3 1313 kb, v3 51 kb [join].  
  Multi-chrom scaffold PfGA01_03: v3 1028 kb, v3 89 kb [join].  
  Multi-chrom scaffold PfGA01_02: v3 841 kb, v3 100 kb [join].  

**GB4** — 61 alignments, 26 query pieces (21 clean 1:1), 22.76 Mb of 3D7 covered (97.5%), identity 84.5%.  
  Inversions: none ≥20 kb.  
  Multi-chrom scaffold PfGB4_14: v3 3275 kb, v3 117 kb [segdup].  
  Multi-chrom scaffold PfGB4_11: v3 1948 kb, v3 117 kb [join], v3 83 kb [join].  
  Multi-chrom scaffold PfGB4_07: v3 1367 kb, v3 64 kb [join].  
  Multi-chrom scaffold PfGB4_05: v3 1307 kb, v3 64 kb [segdup].  
  Multi-chrom scaffold PfGB4_01: v3 541 kb, v3 63 kb [join], v3 32 kb [join].  
  Multi-chrom scaffold PfGB4_00_30: v3 79 kb, v3 64 kb [segdup].  

**GN01** — 49 alignments, 19 query pieces (16 clean 1:1), 23.17 Mb of 3D7 covered (99.3%), identity 83.1%.  
  Inversions: v3:1,294,699-1,418,192 (123 kb).  
  Multi-chrom scaffold PfGN01_14: v3 3254 kb, v3 113 kb [segdup], v3 44 kb [join].  
  Multi-chrom scaffold PfGN01_11: v3 1960 kb, v3 73 kb [join], v3 63 kb [join].  
  Multi-chrom scaffold PfGN01_03: v3 1035 kb, v3 73 kb [join].  
  Multi-chrom scaffold PfGN01_01: v3 615 kb, v3 66 kb [segdup].  

**HB3** — 75 alignments, 28 query pieces (25 clean 1:1), 22.53 Mb of 3D7 covered (96.6%), identity 85.3%.  
  Inversions: none ≥20 kb.  
  Multi-chrom scaffold PfHB3_14: v3 3269 kb, v3 118 kb [segdup], v3 39 kb [join].  
  Multi-chrom scaffold PfHB3_05: v3 1308 kb, v3 48 kb [join], v3 44 kb [segdup].  
  Multi-chrom scaffold PfHB3_07: v3 1317 kb, v3 48 kb [join], v3 24 kb [join].  
  Multi-chrom scaffold PfHB3_06: v3 1313 kb, v3 62 kb [segdup].  

**IT** — 77 alignments, 27 query pieces (22 clean 1:1), 22.54 Mb of 3D7 covered (96.6%), identity 84.1%.  
  Inversions: v3:18,336-44,487 (26 kb).  
  Multi-chrom scaffold PfIT_14: v3 3274 kb, v3 57 kb [join], v3 44 kb [join], v3 44 kb [join].  
  Multi-chrom scaffold PfIT_12: v3 2204 kb, v3 63 kb [join], v3 27 kb [join].  
  Multi-chrom scaffold PfIT_11: v3 1853 kb, v3 61 kb [join].  
  Multi-chrom scaffold PfIT_05: v3 1342 kb, v3 66 kb [join].  
  Multi-chrom scaffold PfIT_07: v3 1339 kb, v3 55 kb [join].  
  Multi-chrom scaffold PfIT_06: v3 1288 kb, v3 100 kb [join].  

**KE01** — 43 alignments, 21 query pieces (19 clean 1:1), 22.59 Mb of 3D7 covered (96.8%), identity 85.8%.  
  Inversions: none ≥20 kb.  
  Multi-chrom scaffold PfKE01_14: v3 3269 kb, v3 52 kb [join], v3 45 kb [join].  
  Multi-chrom scaffold PfKE01_05: v3 1317 kb, v3 38 kb [join], v3 22 kb [join].  

**KH01** — 58 alignments, 22 query pieces (16 clean 1:1), 22.82 Mb of 3D7 covered (97.8%), identity 84.4%.  
  Inversions: v3:12,151-61,631 (49 kb); v3:2,015,704-2,038,178 (22 kb).  
  Multi-chrom scaffold PfKH01_14: v3 3277 kb, v3 78 kb [join], v3 35 kb [join].  
  Multi-chrom scaffold PfKH01_06: v3 1356 kb, v3 56 kb [join], v3 52 kb [join], v3 49 kb [join].  
  Multi-chrom scaffold PfKH01_05: v3 1303 kb, v3 54 kb [join], v3 42 kb [join].  
  Multi-chrom scaffold PfKH01_04: v3 1058 kb, v3 62 kb [join].  
  Multi-chrom scaffold PfKH01_00_27: v3 93 kb, v3 62 kb [join].  

**KH02** — 61 alignments, 21 query pieces (18 clean 1:1), 22.60 Mb of 3D7 covered (96.9%), identity 84.8%.  
  Inversions: none ≥20 kb.  
  Multi-chrom scaffold PfKH02_11: v3 1960 kb, v3 115 kb [join].  
  Multi-chrom scaffold PfKH02_10: v3 1601 kb, v3 30 kb [segdup], v3 20 kb [segdup].  
  Multi-chrom scaffold PfKH02_08: v3 1353 kb, v3 59 kb [join], v3 58 kb [join].  
  Multi-chrom scaffold PfKH02_06: v3 1322 kb, v3 101 kb [segdup], v3 24 kb [join].  

**ML01** — 215 alignments, 114 query pieces (75 clean 1:1), 23.01 Mb of 3D7 covered (98.6%), identity 79.5%.  
  Inversions: none ≥20 kb.  
  Multi-chrom scaffold PfML01_14: v3 3245 kb, v3 27 kb [join], v3 24 kb [join].  
  Multi-chrom scaffold PfML01_12: v3 2215 kb, v3 74 kb [join].  
  Multi-chrom scaffold PfML01_11: v3 1972 kb, v3 62 kb [join].  
  Multi-chrom scaffold PfML01_00_145: v3 71 kb, v3 52 kb [segdup].  

**NF135C10** — 71 alignments, 23 query pieces (18 clean 1:1), 22.70 Mb of 3D7 covered (97.3%), identity 83.6%.  
  Inversions: none ≥20 kb.  
  Multi-chrom scaffold VBRG01000021.1: v3 3257 kb, v3 67 kb [join], v3 49 kb [join].  
  Multi-chrom scaffold VBRG01000020.1: v3 2793 kb, v3 49 kb [join], v3 36 kb [join].  
  Multi-chrom scaffold VBRG01000015.1: v3 1406 kb, v3 49 kb [join], v3 48 kb [join], v3 40 kb [join].  
  Multi-chrom scaffold VBRG01000013.1: v3 1008 kb, v3 450 kb [join], v3 25 kb [join].  
  Multi-chrom scaffold VBRG01000003.1: v3 1003 kb, v3 82 kb [join], v3 34 kb [join].  
  Multi-chrom scaffold VBRG01000005.1: v3 928 kb, v3 77 kb [join], v3 48 kb [join].  

**NF166** — 55 alignments, 32 query pieces (27 clean 1:1), 22.73 Mb of 3D7 covered (97.4%), identity 85.4%.  
  Inversions: none ≥20 kb.  
  Multi-chrom scaffold VBRE01000007.1: v3 1323 kb, v3 59 kb [segdup], v3 24 kb [join].  

**NF54** — 34 alignments, 30 query pieces (29 clean 1:1), 23.25 Mb of 3D7 covered (99.6%), identity 95.3%.  
  Inversions: none ≥20 kb.  
  Multi-chrom scaffold VBRF01000027.1: v3 3290 kb, v3 55 kb [join].  

**SD01** — 45 alignments, 19 query pieces (17 clean 1:1), 22.49 Mb of 3D7 covered (96.4%), identity 85.9%.  
  Inversions: none ≥20 kb.  
  Multi-chrom scaffold PfSD01_14: v3 3215 kb, v3 89 kb [join].  
  Multi-chrom scaffold PfSD01_07: v3 1420 kb, v3 1067 kb [segdup], v3 29 kb [segdup].  

**SN01** — 76 alignments, 36 query pieces (30 clean 1:1), 22.91 Mb of 3D7 covered (98.2%), identity 84.3%.  
  Inversions: v3:12,561-45,705 (33 kb).  
  Multi-chrom scaffold PfSN01_14: v3 3289 kb, v3 150 kb [segdup], v3 27 kb [join].  
  Multi-chrom scaffold PfSN01_11: v3 1954 kb, v3 56 kb [join].  
  Multi-chrom scaffold PfSN01_06: v3 1333 kb, v3 67 kb [join].  
  Multi-chrom scaffold PfSN01_05: v3 1310 kb, v3 45 kb [join], v3 34 kb [join].  

**TG01** — 145 alignments, 79 query pieces (53 clean 1:1), 23.14 Mb of 3D7 covered (99.2%), identity 78.3%.  
  Inversions: none ≥20 kb.  
  Multi-chrom scaffold PfTG01_14: v3 3269 kb, v3 94 kb [segdup], v3 65 kb [join].  
  Multi-chrom scaffold PfTG01_11: v3 2021 kb, v3 94 kb [join].  
  Multi-chrom scaffold PfTG01_08: v3 1363 kb, v3 63 kb [join], v3 26 kb [join], v3 21 kb [join].  
  Multi-chrom scaffold PfTG01_04: v3 1202 kb, v3 95 kb [segdup], v3 41 kb [segdup].  
  Multi-chrom scaffold PfTG01_03: v3 1010 kb, v3 72 kb [join].  
