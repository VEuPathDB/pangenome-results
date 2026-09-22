### Contig-redundancy screen (report only)

Self-alignment: `minimap2 -xasm5 -DP <asm> <asm>` (same call `purge_dups` uses). A contig is flagged **small-redundant** when ≥ 90% of its length aligns (≥ 95% identity, ≥ 1000 bp) to a *longer* contig of the same assembly. **small-unplaced** = a small contig with < 50% of its length aligned to AF293 and not flagged redundant. Nothing is removed here — decide per contig from the tables below.

| Genome | Contigs | large (≥1 Mb) | small | small bp | redundant | redundant bp | genes on redundant | unplaced | genes on unplaced |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| AF293 | 8 | 8 | 0 | 0.00 Mb | 0 | 0 kb | 0 | 0 | 0 |
| A1160 | 10 | 8 | 2 | 1.25 Mb | 0 | 0 kb | 0 | 0 | 0 |
| A1163 | 48 | 9 | 39 | 1.31 Mb | 0 | 0 kb | 0 | 34 | 10 |
| GCA_040126065.1 | 8 | 8 | 0 | 0.00 Mb | 0 | 0 kb | 0 | 0 | 0 |
| GCA_040142845.1 | 9 | 8 | 1 | 0.59 Mb | 0 | 0 kb | 0 | 1 | 200 |
| GCA_040142855.1 | 12 | 9 | 3 | 0.27 Mb | 0 | 0 kb | 0 | 1 | 58 |
| GCA_040142865.1 | 22 | 13 | 9 | 0.96 Mb | 0 | 0 kb | 0 | 5 | 40 |
| GCA_040142875.1 | 13 | 9 | 4 | 1.48 Mb | 0 | 0 kb | 0 | 1 | 195 |
| GCA_040142885.1 | 9 | 8 | 1 | 0.53 Mb | 0 | 0 kb | 0 | 0 | 0 |
| GCA_040142945.1 | 11 | 9 | 2 | 1.46 Mb | 0 | 0 kb | 0 | 0 | 0 |
| GCA_040142955.1 | 20 | 12 | 8 | 3.10 Mb | 0 | 0 kb | 0 | 3 | 302 |
| GCA_040142975.1 | 18 | 9 | 9 | 1.42 Mb | 0 | 0 kb | 0 | 3 | 13 |
| GCA_040167795.1 | 10 | 9 | 1 | 0.51 Mb | 0 | 0 kb | 0 | 0 | 0 |
| GCA_040167805.1 | 25 | 11 | 14 | 5.82 Mb | 0 | 0 kb | 0 | 4 | 56 |
| GCA_058970245.1 | 8 | 8 | 0 | 0.00 Mb | 0 | 0 kb | 0 | 0 | 0 |
| GCA_058972525.1 | 11 | 9 | 2 | 0.50 Mb | 0 | 0 kb | 0 | 1 | 0 |
| GCA_058972625.1 | 10 | 8 | 2 | 0.56 Mb | 0 | 0 kb | 0 | 2 | 196 |

#### Flagged contigs per genome

**AF293** — none flagged.

**A1160** — none flagged.

**A1163**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `scf_000012_A_fumigatus_A1163` | 28,481 | small-unplaced | - | 0% | 10% | scf_000007_A_fumigatus_A1163,scf_000009_A_fumigatus_A1163 | 4 |
| `scf_000013_A_fumigatus_A1163` | 17,043 | small-unplaced | - | 0% | 6% | scf_000002_A_fumigatus_A1163 | 0 |
| `scf_000014_A_fumigatus_A1163` | 15,960 | small-unplaced | - | 0% | 0% | - | 4 |
| `scf_000015_A_fumigatus_A1163` | 15,381 | small-unplaced | - | 0% | 0% | - | 1 |
| `scf_000017_A_fumigatus_A1163` | 10,276 | small-unplaced | - | 0% | 0% | - | 0 |
| `scf_000018_A_fumigatus_A1163` | 8,530 | small-unplaced | Chr2 | 13% | 0% | - | 0 |
| `scf_000019_A_fumigatus_A1163` | 5,988 | small-unplaced | - | 0% | 35% | scf_000003_A_fumigatus_A1163 | 0 |
| `scf_000021_A_fumigatus_A1163` | 4,622 | small-unplaced | - | 0% | 0% | - | 0 |
| `scf_000022_A_fumigatus_A1163` | 4,110 | small-unplaced | - | 0% | 0% | - | 0 |
| `scf_000023_A_fumigatus_A1163` | 3,974 | small-unplaced | - | 0% | 0% | - | 0 |
| `scf_000024_A_fumigatus_A1163` | 3,954 | small-unplaced | - | 0% | 0% | - | 0 |
| `scf_000025_A_fumigatus_A1163` | 3,591 | small-unplaced | - | 0% | 0% | - | 0 |
| `scf_000026_A_fumigatus_A1163` | 3,426 | small-unplaced | - | 0% | 0% | - | 0 |
| `scf_000027_A_fumigatus_A1163` | 3,415 | small-unplaced | - | 0% | 0% | - | 0 |
| `scf_000028_A_fumigatus_A1163` | 3,180 | small-unplaced | - | 0% | 0% | - | 0 |
| `scf_000029_A_fumigatus_A1163` | 3,157 | small-unplaced | - | 0% | 35% | scf_000015_A_fumigatus_A1163 | 0 |
| `scf_000030_A_fumigatus_A1163` | 3,003 | small-unplaced | - | 0% | 0% | - | 0 |
| `scf_000033_A_fumigatus_A1163` | 1,822 | small-unplaced | - | 0% | 0% | - | 0 |
| `scf_000034_A_fumigatus_A1163` | 1,774 | small-unplaced | - | 0% | 0% | - | 0 |
| `scf_000035_A_fumigatus_A1163` | 1,644 | small-unplaced | - | 0% | 0% | - | 0 |
| `scf_000036_A_fumigatus_A1163` | 1,621 | small-unplaced | - | 0% | 0% | - | 0 |
| `scf_000037_A_fumigatus_A1163` | 1,526 | small-unplaced | - | 0% | 0% | - | 0 |
| `scf_000038_A_fumigatus_A1163` | 1,512 | small-unplaced | - | 0% | 0% | - | 0 |
| `scf_000040_A_fumigatus_A1163` | 1,385 | small-unplaced | - | 0% | 0% | - | 0 |
| `scf_000042_A_fumigatus_A1163` | 1,326 | small-unplaced | - | 0% | 0% | - | 0 |
| `scf_000043_A_fumigatus_A1163` | 1,307 | small-unplaced | - | 0% | 0% | - | 0 |
| `scf_000044_A_fumigatus_A1163` | 1,294 | small-unplaced | - | 0% | 0% | - | 0 |
| `scf_000045_A_fumigatus_A1163` | 1,247 | small-unplaced | - | 0% | 0% | - | 1 |
| `scf_000046_A_fumigatus_A1163` | 1,236 | small-unplaced | - | 0% | 0% | - | 0 |
| `scf_000047_A_fumigatus_A1163` | 1,204 | small-unplaced | - | 0% | 0% | - | 0 |
| `scf_000051_A_fumigatus_A1163` | 1,161 | small-unplaced | - | 0% | 0% | - | 0 |
| `scf_000052_A_fumigatus_A1163` | 1,150 | small-unplaced | - | 0% | 0% | - | 0 |
| `scf_000054_A_fumigatus_A1163` | 1,070 | small-unplaced | - | 0% | 0% | - | 0 |
| `scf_000055_A_fumigatus_A1163` | 1,044 | small-unplaced | - | 0% | 0% | - | 0 |

**GCA_040126065.1** — none flagged.

**GCA_040142845.1**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `JBBFMX010000009.1` | 587,617 | small-unplaced | Chr4 | 15% | 18% | CM079236.1,CM079239.1,CM079240.1 | 200 |

**GCA_040142855.1**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `JBBFMT010000010.1` | 176,224 | small-unplaced | Chr3 | 21% | 21% | CM079223.1,JBBFMT010000002.1 | 58 |

**GCA_040142865.1**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `JBBFMV010000015.1` | 118,941 | small-unplaced | - | 0% | 5% | CM079216.1,JBBFMV010000003.1,JBBFMV010000006.1 | 32 |
| `JBBFMV010000016.1` | 81,767 | small-unplaced | - | 0% | 11% | JBBFMV010000002.1,JBBFMV010000004.1 | 7 |
| `JBBFMV010000022.1` | 29,607 | small-unplaced | - | 0% | 13% | JBBFMV010000004.1,JBBFMV010000012.1,JBBFMV010000014.1 | 1 |
| `JBBFMV010000023.1` | 13,292 | small-unplaced | Chr4 | 48% | 0% | - | 0 |
| `JBBFMV010000026.1` | 3,768 | small-unplaced | - | 0% | 0% | - | 0 |

**GCA_040142875.1**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `JBBFMU010000011.1` | 598,771 | small-unplaced | Chr4 | 2% | 7% | CM079217.1,CM079218.1,CM079219.1 | 195 |

**GCA_040142885.1** — none flagged.

**GCA_040142945.1** — none flagged.

**GCA_040142955.1**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `JBBFMY010000015.1` | 507,592 | small-unplaced | Chr7 | 3% | 13% | CM079241.1,JBBFMY010000001.1,JBBFMY010000002.1 | 175 |
| `JBBFMY010000017.1` | 236,713 | small-unplaced | - | 0% | 2% | JBBFMY010000002.1,JBBFMY010000003.1,JBBFMY010000006.1 | 91 |
| `JBBFMY010000018.1` | 128,831 | small-unplaced | - | 0% | 59% | JBBFMY010000001.1,JBBFMY010000004.1,JBBFMY010000013.1 | 36 |

**GCA_040142975.1**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `JBBFNB010000018.1` | 31,396 | small-unplaced | - | 0% | 78% | JBBFNB010000002.1,JBBFNB010000006.1,JBBFNB010000009.1 | 11 |
| `JBBFNB010000022.1` | 15,311 | small-unplaced | Chr8 | 25% | 21% | CM079252.1 | 2 |
| `JBBFNB010000023.1` | 3,927 | small-unplaced | - | 0% | 0% | - | 0 |

**GCA_040167795.1** — none flagged.

**GCA_040167805.1**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `JBDLLN010000021.1` | 189,308 | small-unplaced | - | 0% | 6% | CM079259.1,JBDLLN010000002.1,JBDLLN010000003.1 | 51 |
| `JBDLLN010000023.1` | 36,169 | small-unplaced | Chr6 | 19% | 42% | JBDLLN010000005.1,JBDLLN010000006.1 | 4 |
| `JBDLLN010000024.1` | 23,921 | small-unplaced | - | 0% | 49% | JBDLLN010000002.1,JBDLLN010000023.1 | 1 |
| `JBDLLN010000025.1` | 12,454 | small-unplaced | - | 0% | 44% | JBDLLN010000006.1,JBDLLN010000023.1 | 0 |

**GCA_058970245.1** — none flagged.

**GCA_058972525.1**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `JBVBAJ010000011.1` | 66,821 | small-unplaced | - | 0% | 71% | CM180068.1,CM180070.1,CM180071.1 | 0 |

**GCA_058972625.1**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `JBVBAK010000009.1` | 491,081 | small-unplaced | Chr4 | 2% | 4% | CM180075.1,CM180076.1,CM180077.1 | 180 |
| `JBVBAK010000010.1` | 69,367 | small-unplaced | - | 0% | 57% | JBVBAK010000001.1 | 16 |

#### How to read this

- **small-redundant + 0 genes** — safe to drop (pure duplicated sequence).
- **small-redundant + genes > 0** — check the genes: BLASTp the proteins on that contig against the retained contigs; drop only if every gene has a ≥ 98% identity / ≥ 90% coverage hit elsewhere (otherwise the contig carries real sequence and should stay).
- **small-unplaced** — not redundant and doesn't map to the reference: could be genuine accessory content, a divergent subtelomere, or contamination. Inspect (BLAST vs nt, check gene annotations) before deciding.
- **large** contigs are never auto-flagged; if a genome shows more than 8, a chromosome is split — that's fragmentation, handled separately from redundancy.

Per-contig tables: `contig_redundancy/<label>.contigs.tsv`.