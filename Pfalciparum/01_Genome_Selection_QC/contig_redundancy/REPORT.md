### Contig-redundancy screen (report only)

Self-alignment: `minimap2 -xasm5 -DP <asm> <asm>` (same call `purge_dups` uses). A contig is flagged **small-redundant** when ≥ 90% of its length aligns (≥ 95% identity, ≥ 1000 bp) to a *longer* contig of the same assembly. **small-unplaced** = a small contig with < 50% of its length aligned to 3D7 and not flagged redundant. Nothing is removed here — decide per contig from the tables below.

| Genome | Contigs | large (≥0.5 Mb) | small | small bp | redundant | redundant bp | genes on redundant | unplaced | genes on unplaced |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 3D7 | 16 | 14 | 2 | 0.04 Mb | 0 | 0 kb | 0 | 0 | 0 |
| 7G8-2019 | 22 | 15 | 7 | 0.37 Mb | 1 | 32 kb | 7 | 2 | 17 |
| 7G8 | 17 | 14 | 3 | 0.10 Mb | 0 | 0 kb | 0 | 1 | 3 |
| CD01 | 19 | 14 | 5 | 0.23 Mb | 0 | 0 kb | 0 | 5 | 43 |
| Dd2 | 16 | 14 | 2 | 0.04 Mb | 0 | 0 kb | 0 | 0 | 0 |
| GA01 | 20 | 14 | 6 | 0.29 Mb | 2 | 33 kb | 0 | 2 | 36 |
| GB4 | 26 | 14 | 12 | 0.69 Mb | 0 | 0 kb | 0 | 10 | 115 |
| GN01 | 19 | 14 | 5 | 0.14 Mb | 1 | 24 kb | 5 | 2 | 12 |
| HB3 | 28 | 14 | 14 | 0.35 Mb | 3 | 35 kb | 3 | 5 | 12 |
| IT | 27 | 14 | 13 | 0.34 Mb | 2 | 29 kb | 0 | 8 | 32 |
| KE01 | 21 | 14 | 7 | 0.24 Mb | 0 | 0 kb | 0 | 5 | 31 |
| KH01 | 22 | 14 | 8 | 0.35 Mb | 1 | 23 kb | 4 | 4 | 21 |
| KH02 | 21 | 14 | 7 | 0.29 Mb | 2 | 21 kb | 2 | 3 | 25 |
| NF166 | 32 | 14 | 18 | 1.18 Mb | 1 | 31 kb | 1 | 13 | 192 |
| NF54 | 30 | 14 | 16 | 1.20 Mb | 2 | 38 kb | 15 | 0 | 0 |
| SN01 | 36 | 14 | 22 | 0.74 Mb | 2 | 40 kb | 8 | 14 | 91 |

#### Flagged contigs per genome

**3D7** — none flagged.

**7G8-2019**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `VBRD01000009.1` | 32,271 | small-redundant | - | 0% | 96% | VBRD01000001.1,VBRD01000003.1,VBRD01000004.1 | 7 |
| `VBRD01000002.1` | 50,795 | small-unplaced | - | 0% | 32% | VBRD01000001.1,VBRD01000003.1,VBRD01000006.1 | 10 |
| `VBRD01000007.1` | 46,910 | small-unplaced | - | 0% | 39% | VBRD01000001.1,VBRD01000003.1,VBRD01000004.1 | 7 |

**7G8**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `Pf7G8_00_1` | 40,060 | small-unplaced | - | 0% | 45% | Pf7G8_01,Pf7G8_02,Pf7G8_03 | 3 |

**CD01**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `PfCD01_00_2` | 81,166 | small-unplaced | - | 0% | 33% | PfCD01_01,PfCD01_02,PfCD01_03 | 18 |
| `PfCD01_00_1` | 67,521 | small-unplaced | - | 0% | 54% | PfCD01_00_2,PfCD01_01,PfCD01_02 | 17 |
| `PfCD01_00_5` | 52,563 | small-unplaced | - | 0% | 33% | PfCD01_00_1,PfCD01_00_2,PfCD01_01 | 4 |
| `PfCD01_00_3` | 17,564 | small-unplaced | - | 0% | 76% | PfCD01_13,PfCD01_14 | 3 |
| `PfCD01_00_4` | 6,822 | small-unplaced | - | 0% | 0% | - | 1 |

**Dd2** — none flagged.

**GA01**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `PfGA01_00_3` | 17,284 | small-redundant | - | 0% | 100% | PfGA01_04,PfGA01_13 | 0 |
| `PfGA01_00_1` | 15,586 | small-redundant | - | 0% | 100% | PfGA01_01,PfGA01_03 | 0 |
| `PfGA01_00_2` | 131,075 | small-unplaced | - | 0% | 11% | PfGA01_01,PfGA01_02,PfGA01_03 | 23 |
| `PfGA01_00_4` | 67,311 | small-unplaced | - | 0% | 34% | PfGA01_00_2,PfGA01_01,PfGA01_02 | 13 |

**GB4**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `PfGB4_00_32` | 143,692 | small-unplaced | - | 0% | 5% | PfGB4_01,PfGB4_03,PfGB4_04 | 23 |
| `PfGB4_00_4` | 108,848 | small-unplaced | - | 0% | 50% | PfGB4_00_32,PfGB4_01,PfGB4_02 | 19 |
| `PfGB4_00_30` | 87,679 | small-unplaced | - | 0% | 43% | PfGB4_00_32,PfGB4_00_4,PfGB4_01 | 13 |
| `PfGB4_00_33` | 78,854 | small-unplaced | - | 0% | 40% | PfGB4_00_30,PfGB4_00_32,PfGB4_00_4 | 21 |
| `PfGB4_00_5` | 69,462 | small-unplaced | - | 0% | 37% | PfGB4_00_30,PfGB4_00_32,PfGB4_00_33 | 16 |
| `PfGB4_00_31` | 61,730 | small-unplaced | - | 0% | 29% | PfGB4_00_30,PfGB4_00_32,PfGB4_00_33 | 12 |
| `PfGB4_00_61` | 59,829 | small-unplaced | - | 0% | 30% | PfGB4_00_30,PfGB4_00_31,PfGB4_00_32 | 6 |
| `PfGB4_00_66` | 12,619 | small-unplaced | - | 0% | 89% | PfGB4_00_30,PfGB4_00_31,PfGB4_00_32 | 2 |
| `PfGB4_00_26` | 11,372 | small-unplaced | - | 0% | 86% | PfGB4_00_4,PfGB4_12,PfGB4_13 | 3 |
| `PfGB4_00_16` | 7,376 | small-unplaced | - | 0% | 79% | PfGB4_00_31,PfGB4_03 | 0 |

**GN01**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `PfGN01_00_5` | 24,162 | small-redundant | - | 0% | 100% | PfGN01_01,PfGN01_02,PfGN01_03 | 5 |
| `PfGN01_00_6` | 48,702 | small-unplaced | - | 0% | 31% | PfGN01_03,PfGN01_06,PfGN01_07 | 7 |
| `PfGN01_00_7` | 31,040 | small-unplaced | - | 0% | 85% | PfGN01_00_6,PfGN01_01,PfGN01_06 | 5 |

**HB3**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `PfHB3_00_0` | 13,275 | small-redundant | - | 0% | 100% | PfHB3_00_1,PfHB3_00_20,PfHB3_06 | 0 |
| `PfHB3_00_14` | 11,586 | small-redundant | - | 0% | 100% | PfHB3_05 | 3 |
| `PfHB3_00_26` | 10,375 | small-redundant | - | 0% | 100% | PfHB3_00_0,PfHB3_00_1,PfHB3_00_20 | 0 |
| `PfHB3_00_1` | 77,447 | small-unplaced | Pf3D7_11_v3 | 13% | 50% | PfHB3_01,PfHB3_02,PfHB3_03 | 8 |
| `PfHB3_00_20` | 51,034 | small-unplaced | - | 0% | 51% | PfHB3_00_1,PfHB3_01,PfHB3_02 | 3 |
| `PfHB3_00_8` | 34,851 | small-unplaced | - | 0% | 43% | PfHB3_06,PfHB3_14 | 1 |
| `PfHB3_00_19` | 30,382 | small-unplaced | - | 0% | 77% | PfHB3_00_1,PfHB3_02,PfHB3_03 | 0 |
| `PfHB3_00_34` | 6,609 | small-unplaced | - | 0% | 0% | - | 0 |

**IT**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `PfIT_00_8` | 17,178 | small-redundant | - | 0% | 100% | PfIT_10,PfIT_14 | 0 |
| `PfIT_00_5` | 12,211 | small-redundant | - | 0% | 94% | PfIT_00_8,PfIT_10,PfIT_14 | 0 |
| `PfIT_00_4` | 39,951 | small-unplaced | - | 0% | 39% | PfIT_00_10,PfIT_01,PfIT_02 | 5 |
| `PfIT_00_11` | 39,238 | small-unplaced | - | 0% | 39% | PfIT_01,PfIT_02,PfIT_03 | 13 |
| `PfIT_00_9` | 36,284 | small-unplaced | - | 0% | 69% | PfIT_00_11,PfIT_00_4,PfIT_01 | 11 |
| `PfIT_00_2` | 23,847 | small-unplaced | - | 0% | 50% | PfIT_12 | 0 |
| `PfIT_00_3` | 21,778 | small-unplaced | - | 0% | 43% | PfIT_00_2,PfIT_00_4,PfIT_12 | 0 |
| `PfIT_00_6` | 17,765 | small-unplaced | - | 0% | 84% | PfIT_04,PfIT_08,PfIT_12 | 3 |
| `PfIT_00_1` | 10,617 | small-unplaced | - | 0% | 10% | PfIT_08 | 0 |
| `PfIT_00_7` | 7,505 | small-unplaced | - | 0% | 87% | PfIT_00_5,PfIT_00_8,PfIT_10 | 0 |

**KE01**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `PfKE01_00_1` | 68,005 | small-unplaced | - | 0% | 26% | PfKE01_02,PfKE01_03,PfKE01_04 | 13 |
| `PfKE01_00_3` | 43,944 | small-unplaced | - | 0% | 40% | PfKE01_01,PfKE01_02,PfKE01_04 | 4 |
| `PfKE01_00_6` | 31,856 | small-unplaced | - | 0% | 45% | PfKE01_00_3,PfKE01_02,PfKE01_04 | 10 |
| `PfKE01_00_2` | 31,080 | small-unplaced | - | 0% | 49% | PfKE01_04,PfKE01_07,PfKE01_08 | 4 |
| `PfKE01_00_4` | 17,937 | small-unplaced | - | 0% | 72% | PfKE01_04 | 0 |

**KH01**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `PfKH01_00_26` | 23,260 | small-redundant | - | 0% | 95% | PfKH01_04 | 4 |
| `PfKH01_00_3` | 73,898 | small-unplaced | - | 0% | 45% | PfKH01_00_27,PfKH01_01,PfKH01_02 | 11 |
| `PfKH01_00_25` | 22,215 | small-unplaced | - | 0% | 66% | PfKH01_04,PfKH01_12,PfKH01_13 | 6 |
| `PfKH01_00_1` | 19,295 | small-unplaced | - | 0% | 89% | PfKH01_02,PfKH01_03,PfKH01_05 | 2 |
| `PfKH01_00_2` | 13,268 | small-unplaced | - | 0% | 85% | PfKH01_04,PfKH01_07 | 2 |

**KH02**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `PfKH02_00_6` | 14,305 | small-redundant | Pf3D7_13_v3 | 100% | 100% | PfKH02_01,PfKH02_11,PfKH02_13 | 2 |
| `PfKH02_00_3` | 6,708 | small-redundant | - | 0% | 98% | PfKH02_04,PfKH02_14 | 0 |
| `PfKH02_00_4` | 119,196 | small-unplaced | - | 0% | 20% | PfKH02_02,PfKH02_03,PfKH02_04 | 25 |
| `PfKH02_00_1` | 61,654 | small-unplaced | - | 0% | 21% | PfKH02_09 | 0 |
| `PfKH02_00_5` | 28,026 | small-unplaced | - | 0% | 53% | PfKH02_00_1,PfKH02_09 | 0 |

**NF166**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `VBRE01000025.1` | 31,444 | small-redundant | - | 0% | 99% | VBRE01000014.1 | 1 |
| `VBRE01000022.1` | 136,077 | small-unplaced | - | 0% | 27% | VBRE01000001.1,VBRE01000003.1,VBRE01000006.1 | 23 |
| `VBRE01000020.1` | 108,942 | small-unplaced | Pf3D7_07_v3 | 35% | 26% | VBRE01000001.1,VBRE01000003.1,VBRE01000004.1 | 30 |
| `VBRE01000030.1` | 108,267 | small-unplaced | - | 0% | 28% | VBRE01000001.1,VBRE01000003.1,VBRE01000004.1 | 21 |
| `VBRE01000008.1` | 107,213 | small-unplaced | - | 0% | 25% | VBRE01000001.1,VBRE01000003.1,VBRE01000004.1 | 20 |
| `VBRE01000002.1` | 99,961 | small-unplaced | - | 0% | 43% | VBRE01000001.1,VBRE01000003.1,VBRE01000004.1 | 26 |
| `VBRE01000013.1` | 81,126 | small-unplaced | - | 0% | 28% | VBRE01000001.1,VBRE01000002.1,VBRE01000003.1 | 12 |
| `VBRE01000029.1` | 59,255 | small-unplaced | - | 0% | 33% | VBRE01000002.1,VBRE01000003.1,VBRE01000004.1 | 17 |
| `VBRE01000015.1` | 56,845 | small-unplaced | - | 0% | 59% | VBRE01000001.1,VBRE01000002.1,VBRE01000003.1 | 9 |
| `VBRE01000028.1` | 51,123 | small-unplaced | - | 0% | 38% | VBRE01000001.1,VBRE01000002.1,VBRE01000003.1 | 7 |
| `VBRE01000027.1` | 46,726 | small-unplaced | - | 0% | 28% | VBRE01000001.1,VBRE01000002.1,VBRE01000003.1 | 6 |
| `VBRE01000026.1` | 35,954 | small-unplaced | - | 0% | 67% | VBRE01000001.1,VBRE01000002.1,VBRE01000003.1 | 6 |
| `VBRE01000019.1` | 30,748 | small-unplaced | - | 0% | 85% | VBRE01000001.1,VBRE01000002.1,VBRE01000003.1 | 7 |
| `VBRE01000010.1` | 24,017 | small-unplaced | - | 0% | 83% | VBRE01000001.1,VBRE01000002.1,VBRE01000003.1 | 8 |

**NF54**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `VBRF01000002.1` | 24,050 | small-redundant | Pf3D7_07_v3 | 100% | 92% | VBRF01000001.1,VBRF01000003.1,VBRF01000004.1 | 9 |
| `VBRF01000029.1` | 14,237 | small-redundant | Pf3D7_07_v3 | 93% | 91% | VBRF01000001.1,VBRF01000002.1,VBRF01000003.1 | 6 |

**SN01**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `PfSN01_00_3` | 21,238 | small-redundant | - | 0% | 100% | PfSN01_00_1,PfSN01_00_17,PfSN01_00_2 | 5 |
| `PfSN01_00_18` | 18,782 | small-redundant | - | 0% | 92% | PfSN01_00_1,PfSN01_00_17,PfSN01_00_19 | 3 |
| `PfSN01_00_8` | 107,778 | small-unplaced | - | 0% | 12% | PfSN01_01,PfSN01_03,PfSN01_04 | 17 |
| `PfSN01_00_9` | 86,629 | small-unplaced | - | 0% | 14% | PfSN01_00_8,PfSN01_01,PfSN01_02 | 13 |
| `PfSN01_00_1` | 61,104 | small-unplaced | - | 0% | 41% | PfSN01_00_8,PfSN01_00_9,PfSN01_01 | 7 |
| `PfSN01_00_5` | 52,966 | small-unplaced | - | 0% | 49% | PfSN01_00_1,PfSN01_00_8,PfSN01_00_9 | 12 |
| `PfSN01_00_2` | 45,688 | small-unplaced | - | 0% | 57% | PfSN01_00_1,PfSN01_00_5,PfSN01_00_8 | 12 |
| `PfSN01_00_7` | 43,978 | small-unplaced | - | 0% | 16% | PfSN01_00_1,PfSN01_04,PfSN01_05 | 3 |
| `PfSN01_00_17` | 42,139 | small-unplaced | - | 0% | 39% | PfSN01_00_1,PfSN01_00_2,PfSN01_00_5 | 5 |
| `PfSN01_00_19` | 40,399 | small-unplaced | - | 0% | 0% | - | 2 |
| `PfSN01_00_12` | 28,738 | small-unplaced | - | 0% | 0% | - | 0 |
| `PfSN01_00_4` | 25,988 | small-unplaced | Pf3D7_08_v3 | 38% | 68% | PfSN01_00_1,PfSN01_00_9,PfSN01_01 | 10 |
| `PfSN01_00_6` | 24,118 | small-unplaced | - | 0% | 37% | PfSN01_00_1,PfSN01_00_2,PfSN01_00_5 | 4 |
| `PfSN01_00_20` | 20,769 | small-unplaced | Pf3D7_01_v3 | 7% | 77% | PfSN01_00_19,PfSN01_00_2,PfSN01_00_3 | 3 |
| `PfSN01_00_15` | 13,233 | small-unplaced | - | 0% | 8% | PfSN01_14 | 0 |
| `PfSN01_00_11` | 9,378 | small-unplaced | - | 0% | 70% | PfSN01_00_1,PfSN01_00_2,PfSN01_00_3 | 3 |

#### How to read this

- **small-redundant + 0 genes** — safe to drop (pure duplicated sequence).
- **small-redundant + genes > 0** — check the genes: BLASTp the proteins on that contig against the retained contigs; drop only if every gene has a ≥ 98% identity / ≥ 90% coverage hit elsewhere (otherwise the contig carries real sequence and should stay).
- **small-unplaced** — not redundant and doesn't map to the reference: could be genuine accessory content, a divergent subtelomere, or contamination. Inspect (BLAST vs nt, check gene annotations) before deciding.
- **large** contigs are never auto-flagged, no matter how many there are; a genome with noticeably more large contigs than the reference's chromosome count means a chromosome got split, not duplicated — that's fragmentation, handled separately from redundancy.

Per-contig tables: `contig_redundancy/<label>.contigs.tsv`.