### Contig-redundancy screen (report only)

Self-alignment: `minimap2 -xasm5 -DP <asm> <asm>` (same call `purge_dups` uses). A contig is flagged **small-redundant** when ≥ 90% of its length aligns (≥ 95% identity, ≥ 1000 bp) to a *longer* contig of the same assembly. **small-unplaced** = a small contig with < 50% of its length aligned to ME49 and not flagged redundant. Nothing is removed here — decide per contig from the tables below.

| Genome | Contigs | large (≥1 Mb) | small | small bp | redundant | redundant bp | genes on redundant | unplaced | genes on unplaced |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ME49 | 47 | 14 | 33 | 0.60 Mb | 6 | 94 kb | 22 | 0 | 0 |
| ARI | 47 | 21 | 26 | 8.20 Mb | 0 | 0 kb | 0 | 9 | 98 |
| CAST | 56 | 23 | 33 | 6.83 Mb | 0 | 0 kb | 0 | 21 | 253 |
| COUG | 58 | 21 | 37 | 10.23 Mb | 0 | 0 kb | 0 | 18 | 200 |
| FOU | 105 | 23 | 82 | 20.44 Mb | 0 | 0 kb | 0 | 36 | 595 |
| GAB2 | 84 | 24 | 60 | 13.37 Mb | 0 | 0 kb | 0 | 31 | 172 |
| GT1 | 33 | 14 | 19 | 0.28 Mb | 0 | 0 kb | 0 | 7 | 9 |
| MAS | 143 | 16 | 127 | 33.16 Mb | 0 | 0 kb | 0 | 34 | 270 |
| p89 | 93 | 22 | 71 | 18.73 Mb | 0 | 0 kb | 0 | 37 | 390 |
| RH88 | 135 | 13 | 122 | 2.67 Mb | 100 | 1724 kb | 89 | 18 | 47 |
| RUB | 89 | 21 | 68 | 13.82 Mb | 0 | 0 kb | 0 | 40 | 262 |
| TgCATBr9 | 93 | 24 | 69 | 15.15 Mb | 0 | 0 kb | 0 | 37 | 402 |
| TgCatPRC2 | 103 | 25 | 78 | 16.60 Mb | 0 | 0 kb | 0 | 29 | 169 |
| VAND | 83 | 24 | 59 | 14.22 Mb | 0 | 0 kb | 0 | 26 | 125 |
| VEG | 30 | 14 | 16 | 0.42 Mb | 0 | 0 kb | 0 | 14 | 25 |

#### Flagged contigs per genome

**ME49**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `KE139140` | 20,306 | small-redundant | - | 0% | 99% | KE138866,TGME49_chrVI | 9 |
| `KE139816` | 17,865 | small-redundant | - | 0% | 98% | KE138892,KE139822,KE139843 | 1 |
| `KE138868` | 16,277 | small-redundant | - | 0% | 100% | KE138866,KE139140,TGME49_chrVI | 6 |
| `KE139842` | 15,749 | small-redundant | - | 0% | 99% | KE138892,KE139822,TGME49_chrII | 2 |
| `KE139130` | 12,872 | small-redundant | - | 0% | 100% | KE138874,TGME49_chrXII | 3 |
| `KE139841` | 11,018 | small-redundant | - | 0% | 96% | KE138892,KE139817,KE139819 | 1 |

**ARI**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `KQ973631` | 519,160 | small-unplaced | - | 0% | 0% | - | 67 |
| `KQ973640` | 92,034 | small-unplaced | - | 0% | 0% | - | 4 |
| `KQ973641` | 64,530 | small-unplaced | - | 0% | 0% | - | 3 |
| `KQ973642` | 59,472 | small-unplaced | - | 0% | 13% | KQ973640 | 3 |
| `KQ973644` | 25,095 | small-unplaced | - | 0% | 0% | - | 3 |
| `KQ973645` | 22,122 | small-unplaced | - | 0% | 0% | - | 4 |
| `KQ973648` | 20,875 | small-unplaced | - | 0% | 0% | - | 1 |
| `KQ973650` | 15,482 | small-unplaced | - | 0% | 15% | KQ973648 | 2 |
| `KQ973646` | 14,476 | small-unplaced | - | 0% | 0% | - | 11 |

**CAST**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `ML130755` | 500,473 | small-unplaced | - | 0% | 0% | - | 64 |
| `ML130707` | 430,029 | small-unplaced | - | 0% | 0% | - | 70 |
| `ML130723` | 421,199 | small-unplaced | - | 0% | 0% | - | 69 |
| `ML130730` | 64,043 | small-unplaced | - | 0% | 0% | - | 2 |
| `ML130745` | 63,055 | small-unplaced | - | 0% | 0% | - | 3 |
| `ML130718` | 54,510 | small-unplaced | - | 0% | 4% | ML130756 | 5 |
| `ML130710` | 46,993 | small-unplaced | - | 0% | 0% | - | 1 |
| `ML130757` | 46,826 | small-unplaced | - | 0% | 0% | - | 3 |
| `ML130734` | 44,686 | small-unplaced | - | 0% | 0% | - | 4 |
| `ML130724` | 41,849 | small-unplaced | - | 0% | 0% | - | 1 |
| `ML130702` | 38,414 | small-unplaced | KE138892 | 3% | 0% | - | 2 |
| `ML130748` | 25,315 | small-unplaced | - | 0% | 0% | - | 0 |
| `ML130758` | 24,817 | small-unplaced | - | 0% | 0% | - | 4 |
| `ML130739` | 24,060 | small-unplaced | - | 0% | 0% | - | 3 |
| `ML130754` | 23,933 | small-unplaced | - | 0% | 0% | - | 5 |
| `ML130768` | 23,370 | small-unplaced | - | 0% | 0% | - | 2 |
| `ML130709` | 18,349 | small-unplaced | - | 0% | 0% | - | 11 |
| `ML130738` | 18,216 | small-unplaced | - | 0% | 0% | - | 2 |
| `ML130762` | 15,390 | small-unplaced | - | 0% | 10% | ML130706 | 2 |
| `ML130736` | 13,469 | small-unplaced | KE139830 | 18% | 0% | - | 0 |
| `ML130741` | 11,405 | small-unplaced | - | 0% | 0% | - | 0 |

**COUG**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `KZ624813.1` | 373,778 | small-unplaced | - | 0% | 0% | - | 68 |
| `KZ624835.1` | 355,300 | small-unplaced | - | 0% | 0% | - | 52 |
| `KZ624889.1` | 200,513 | small-unplaced | - | 0% | 0% | - | 23 |
| `KZ624807.1` | 116,094 | small-unplaced | - | 0% | 0% | - | 7 |
| `KZ624846.1` | 111,808 | small-unplaced | - | 0% | 0% | - | 2 |
| `KZ624878.1` | 109,367 | small-unplaced | - | 0% | 0% | - | 12 |
| `KZ624827.1` | 48,169 | small-unplaced | - | 0% | 0% | - | 2 |
| `KZ624847.1` | 46,689 | small-unplaced | - | 0% | 0% | - | 1 |
| `KZ624890.1` | 41,922 | small-unplaced | - | 0% | 0% | - | 2 |
| `KZ624866.1` | 33,248 | small-unplaced | - | 0% | 0% | - | 4 |
| `KZ624856.1` | 31,085 | small-unplaced | - | 0% | 0% | - | 3 |
| `KZ624822.1` | 20,074 | small-unplaced | - | 0% | 37% | KZ624827.1 | 1 |
| `KZ624801.1` | 18,523 | small-unplaced | - | 0% | 0% | - | 8 |
| `KZ624876.1` | 18,068 | small-unplaced | - | 0% | 0% | - | 2 |
| `KZ624840.1` | 17,698 | small-unplaced | - | 0% | 0% | - | 4 |
| `KZ624815.1` | 17,666 | small-unplaced | - | 0% | 0% | - | 9 |
| `KZ624824.1` | 14,908 | small-unplaced | - | 0% | 0% | - | 0 |
| `KZ624803.1` | 10,373 | small-unplaced | - | 0% | 0% | - | 0 |

**FOU**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `KN003098` | 540,627 | small-unplaced | - | 0% | 0% | - | 81 |
| `KN000271` | 359,831 | small-unplaced | - | 0% | 0% | - | 54 |
| `KN000272` | 331,441 | small-unplaced | - | 0% | 0% | - | 55 |
| `KN000273` | 331,355 | small-unplaced | - | 0% | 0% | - | 65 |
| `KN000275` | 308,413 | small-unplaced | - | 0% | 0% | - | 53 |
| `KN003099` | 302,779 | small-unplaced | - | 0% | 0% | - | 56 |
| `KN000276` | 270,519 | small-unplaced | - | 0% | 0% | - | 53 |
| `KN000285` | 189,129 | small-unplaced | - | 0% | 0% | - | 20 |
| `KN000286` | 183,684 | small-unplaced | - | 0% | 0% | - | 30 |
| `KN000290` | 171,698 | small-unplaced | - | 0% | 0% | - | 24 |
| `KN000291` | 147,066 | small-unplaced | - | 0% | 0% | - | 30 |
| `KN000293` | 100,171 | small-unplaced | - | 0% | 0% | - | 17 |
| `KN000295` | 83,922 | small-unplaced | - | 0% | 0% | - | 2 |
| `KN000298` | 59,198 | small-unplaced | KE140935 | 6% | 0% | - | 6 |
| `KN000299` | 55,312 | small-unplaced | - | 0% | 5% | KN003102 | 2 |
| `KN000300` | 54,798 | small-unplaced | - | 0% | 0% | - | 3 |
| `KN000301` | 49,142 | small-unplaced | - | 0% | 2% | KN003102 | 3 |
| `KN000302` | 46,426 | small-unplaced | - | 0% | 0% | - | 5 |
| `KN000303` | 43,473 | small-unplaced | - | 0% | 0% | - | 1 |
| `KN000306` | 35,773 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN000307` | 29,098 | small-unplaced | - | 0% | 0% | - | 4 |
| `KN000308` | 27,195 | small-unplaced | - | 0% | 0% | - | 2 |
| `KN000309` | 26,846 | small-unplaced | - | 0% | 0% | - | 3 |
| `KN000310` | 24,829 | small-unplaced | - | 0% | 0% | - | 4 |
| `KN000313` | 20,543 | small-unplaced | - | 0% | 0% | - | 1 |
| `KN000314` | 19,847 | small-unplaced | - | 0% | 0% | - | 2 |
| `KN000315` | 19,416 | small-unplaced | - | 0% | 0% | - | 3 |
| `KN000316` | 17,674 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN000317` | 16,791 | small-unplaced | - | 0% | 0% | - | 7 |
| `KN000318` | 16,599 | small-unplaced | chrV | 27% | 0% | - | 2 |
| `KN000319` | 16,354 | small-unplaced | - | 0% | 0% | - | 1 |
| `KN000320` | 15,527 | small-unplaced | KE138870 | 19% | 0% | - | 0 |
| `KN000322` | 13,662 | small-unplaced | - | 0% | 22% | KN000321 | 1 |
| `KN000325` | 12,007 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN000326` | 10,982 | small-unplaced | - | 0% | 10% | KN000310 | 0 |
| `KN000327` | 10,673 | small-unplaced | - | 0% | 0% | - | 5 |

**GAB2**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `KN003143` | 425,481 | small-unplaced | - | 0% | 0% | - | 64 |
| `KN003151` | 188,867 | small-unplaced | - | 0% | 0% | - | 23 |
| `KN003156` | 109,587 | small-unplaced | - | 0% | 0% | - | 6 |
| `KN003155` | 103,764 | small-unplaced | - | 0% | 0% | - | 5 |
| `KN003158` | 65,484 | small-unplaced | - | 0% | 0% | - | 9 |
| `KN003159` | 55,711 | small-unplaced | - | 0% | 0% | - | 15 |
| `KN003160` | 54,623 | small-unplaced | - | 0% | 0% | - | 3 |
| `KN003162` | 39,086 | small-unplaced | - | 0% | 0% | - | 2 |
| `KN003161` | 38,368 | small-unplaced | KE138892 | 3% | 0% | - | 4 |
| `KN003164` | 31,760 | small-unplaced | - | 0% | 0% | - | 1 |
| `KN003167` | 31,004 | small-unplaced | - | 0% | 0% | - | 1 |
| `KN003163` | 30,335 | small-unplaced | - | 0% | 0% | - | 3 |
| `KN003165` | 30,100 | small-unplaced | - | 0% | 0% | - | 2 |
| `KN003170` | 24,648 | small-unplaced | chrVIIa | 31% | 0% | - | 3 |
| `KN003168` | 23,791 | small-unplaced | KE139178 | 8% | 5% | KN003145 | 3 |
| `KN003171` | 23,717 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN003175` | 20,256 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN003172` | 17,901 | small-unplaced | - | 0% | 0% | - | 1 |
| `KN003179` | 17,373 | small-unplaced | - | 0% | 0% | - | 4 |
| `KN003174` | 16,958 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN003173` | 16,815 | small-unplaced | - | 0% | 0% | - | 4 |
| `KN003176` | 15,796 | small-unplaced | - | 0% | 0% | - | 5 |
| `KN003177` | 15,523 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN003178` | 15,201 | small-unplaced | - | 0% | 10% | KN003138 | 3 |
| `KN003188` | 13,433 | small-unplaced | - | 0% | 0% | - | 3 |
| `KN003183` | 12,908 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN003182` | 12,717 | small-unplaced | - | 0% | 0% | - | 1 |
| `KN003185` | 11,947 | small-unplaced | - | 0% | 0% | - | 4 |
| `KN003193` | 11,709 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN003190` | 11,557 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN003187` | 10,299 | small-unplaced | - | 0% | 0% | - | 3 |

**GT1**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `AAQM03000794` | 17,811 | small-unplaced | - | 0% | 0% | - | 0 |
| `AAQM03000328` | 15,822 | small-unplaced | - | 0% | 0% | - | 2 |
| `AAQM03000180` | 14,676 | small-unplaced | - | 0% | 7% | TGGT1_chrVI | 4 |
| `AAQM03000672` | 13,782 | small-unplaced | - | 0% | 0% | - | 2 |
| `AAQM03000679` | 13,022 | small-unplaced | - | 0% | 0% | - | 0 |
| `AAQM03000824` | 11,793 | small-unplaced | - | 0% | 0% | - | 0 |
| `AAQM03000669` | 11,695 | small-unplaced | - | 0% | 0% | - | 1 |

**MAS**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `KN046788` | 475,990 | small-unplaced | - | 0% | 0% | - | 79 |
| `KN044661` | 315,170 | small-unplaced | - | 0% | 0% | - | 57 |
| `KN044682` | 181,142 | small-unplaced | - | 0% | 0% | - | 21 |
| `KN044687` | 145,603 | small-unplaced | - | 0% | 0% | - | 29 |
| `KN044688` | 144,034 | small-unplaced | - | 0% | 0% | - | 19 |
| `KN044695` | 119,372 | small-unplaced | - | 0% | 0% | - | 18 |
| `KN044703` | 47,000 | small-unplaced | - | 0% | 0% | - | 5 |
| `KN044707` | 40,974 | small-unplaced | - | 0% | 0% | - | 8 |
| `KN044710` | 32,391 | small-unplaced | - | 0% | 0% | - | 2 |
| `KN044712` | 26,653 | small-unplaced | - | 0% | 0% | - | 2 |
| `KN044713` | 26,473 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN044714` | 25,094 | small-unplaced | - | 0% | 0% | - | 2 |
| `KN044715` | 23,387 | small-unplaced | - | 0% | 0% | - | 2 |
| `KN044717` | 22,676 | small-unplaced | - | 0% | 0% | - | 1 |
| `KN044718` | 22,266 | small-unplaced | - | 0% | 0% | - | 3 |
| `KN044719` | 19,760 | small-unplaced | - | 0% | 0% | - | 3 |
| `KN044721` | 17,935 | small-unplaced | - | 0% | 0% | - | 3 |
| `KN044722` | 17,913 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN044723` | 17,453 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN044724` | 16,901 | small-unplaced | - | 0% | 0% | - | 3 |
| `KN044725` | 16,688 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN044726` | 15,847 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN044728` | 15,132 | small-unplaced | - | 0% | 0% | - | 2 |
| `KN044729` | 14,841 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN044733` | 13,501 | small-unplaced | - | 0% | 0% | - | 2 |
| `KN044735` | 12,661 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN044736` | 12,142 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN044737` | 11,822 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN044738` | 11,608 | small-unplaced | - | 0% | 0% | - | 4 |
| `KN044739` | 11,546 | small-unplaced | - | 0% | 0% | - | 2 |
| `KN044740` | 11,159 | small-unplaced | - | 0% | 0% | - | 2 |
| `KN044741` | 11,102 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN044742` | 10,488 | small-unplaced | - | 0% | 0% | - | 1 |
| `KN044744` | 10,112 | small-unplaced | - | 0% | 0% | - | 0 |

**p89**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `KL998112` | 509,903 | small-unplaced | - | 0% | 0% | - | 71 |
| `KL998117` | 432,679 | small-unplaced | - | 0% | 0% | - | 67 |
| `KL998120` | 347,184 | small-unplaced | - | 0% | 0% | - | 42 |
| `KL998123` | 202,085 | small-unplaced | - | 0% | 0% | - | 28 |
| `KL998125` | 185,832 | small-unplaced | - | 0% | 0% | - | 23 |
| `KN000228` | 179,586 | small-unplaced | - | 0% | 0% | - | 35 |
| `KL998127` | 159,291 | small-unplaced | - | 0% | 0% | - | 33 |
| `KL998128` | 158,785 | small-unplaced | KE140117 | 2% | 2% | KL998083 | 10 |
| `KL998129` | 97,622 | small-unplaced | - | 0% | 0% | - | 3 |
| `KL998130` | 95,633 | small-unplaced | chrIX | 2% | 0% | - | 16 |
| `KL998132` | 63,606 | small-unplaced | KE140935 | 6% | 0% | - | 5 |
| `KL998133` | 60,624 | small-unplaced | - | 0% | 0% | - | 0 |
| `KL998134` | 52,351 | small-unplaced | - | 0% | 0% | - | 4 |
| `KL998135` | 50,889 | small-unplaced | - | 0% | 0% | - | 1 |
| `KL998136` | 49,543 | small-unplaced | - | 0% | 0% | - | 2 |
| `KL998137` | 49,144 | small-unplaced | - | 0% | 10% | KL998083,KL998128 | 3 |
| `KL998138` | 46,019 | small-unplaced | - | 0% | 0% | - | 2 |
| `KL998140` | 33,595 | small-unplaced | - | 0% | 0% | - | 8 |
| `KL998141` | 31,423 | small-unplaced | - | 0% | 0% | - | 3 |
| `KL998142` | 29,473 | small-unplaced | - | 0% | 0% | - | 1 |
| `KL998143` | 28,177 | small-unplaced | - | 0% | 0% | - | 2 |
| `KL998144` | 27,893 | small-unplaced | - | 0% | 4% | KL998092 | 4 |
| `KL998145` | 26,692 | small-unplaced | - | 0% | 0% | - | 0 |
| `KL998146` | 26,327 | small-unplaced | - | 0% | 0% | - | 2 |
| `KL998147` | 19,062 | small-unplaced | - | 0% | 0% | - | 3 |
| `KL998148` | 18,145 | small-unplaced | - | 0% | 0% | - | 1 |
| `KL998150` | 17,707 | small-unplaced | - | 0% | 0% | - | 0 |
| `KL998151` | 17,681 | small-unplaced | - | 0% | 0% | - | 1 |
| `KL998152` | 16,100 | small-unplaced | - | 0% | 0% | - | 1 |
| `KL998153` | 14,997 | small-unplaced | - | 0% | 0% | - | 3 |
| `KL998155` | 14,876 | small-unplaced | - | 0% | 0% | - | 1 |
| `KL998156` | 13,069 | small-unplaced | - | 0% | 0% | - | 2 |
| `KL998157` | 13,058 | small-unplaced | - | 0% | 0% | - | 4 |
| `KL998158` | 12,968 | small-unplaced | - | 0% | 24% | KL998154 | 1 |
| `KL998159` | 11,695 | small-unplaced | - | 0% | 0% | - | 1 |
| `KL998160` | 11,601 | small-unplaced | - | 0% | 13% | KL998144 | 1 |
| `KL998162` | 10,302 | small-unplaced | - | 0% | 0% | - | 6 |

**RH88**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `JAAUHK010000015` | 42,350 | small-redundant | chrV | 33% | 97% | CM023090,CM023091,CM023092 | 4 |
| `JAAUHK010000115` | 33,730 | small-redundant | - | 0% | 100% | CM023093,JAAUHK010000038 | 0 |
| `JAAUHK010000023` | 31,785 | small-redundant | - | 0% | 97% | CM023087,CM023090,CM023092 | 4 |
| `JAAUHK010000025` | 30,311 | small-redundant | KE138841 | 69% | 100% | CM023094 | 13 |
| `JAAUHK010000055` | 29,811 | small-redundant | KE140722 | 78% | 95% | JAAUHK010000033,JAAUHK010000034,JAAUHK010000041 | 0 |
| `JAAUHK010000012` | 28,810 | small-redundant | - | 0% | 92% | CM023087,CM023091,JAAUHK010000002 | 1 |
| `JAAUHK010000005` | 28,644 | small-redundant | KE138841 | 100% | 100% | CM023094,JAAUHK010000025 | 9 |
| `JAAUHK010000006` | 28,514 | small-redundant | - | 0% | 100% | CM023090 | 0 |
| `JAAUHK010000047` | 28,476 | small-redundant | KE139832 | 52% | 96% | JAAUHK010000033,JAAUHK010000034,JAAUHK010000041 | 0 |
| `JAAUHK010000108` | 27,454 | small-redundant | - | 0% | 100% | CM023093,JAAUHK010000038,JAAUHK010000115 | 1 |
| `JAAUHK010000010` | 26,922 | small-redundant | KE139140 | 98% | 90% | CM023087 | 10 |
| `JAAUHK010000009` | 26,667 | small-redundant | - | 0% | 100% | CM023090,JAAUHK010000006,JAAUHK010000026 | 1 |
| `JAAUHK010000080` | 24,267 | small-redundant | KE140722 | 87% | 99% | JAAUHK010000033,JAAUHK010000034,JAAUHK010000041 | 0 |
| `JAAUHK010000019` | 23,363 | small-redundant | KE139063 | 5% | 100% | CM023090,JAAUHK010000006,JAAUHK010000009 | 1 |
| `JAAUHK010000095` | 23,051 | small-redundant | KE138872 | 58% | 93% | JAAUHK010000033,JAAUHK010000034,JAAUHK010000041 | 0 |
| `JAAUHK010000048` | 22,591 | small-redundant | KE138872 | 74% | 96% | JAAUHK010000033,JAAUHK010000034,JAAUHK010000041 | 0 |
| `JAAUHK010000018` | 22,487 | small-redundant | - | 0% | 96% | CM023090,CM023091,JAAUHK010000002 | 2 |
| `JAAUHK010000020` | 22,198 | small-redundant | chrV | 82% | 100% | CM023087,CM023090,CM023091 | 1 |
| `JAAUHK010000032` | 21,215 | small-redundant | KE140738 | 66% | 98% | JAAUHK010000033,JAAUHK010000034,JAAUHK010000041 | 0 |
| `JAAUHK010000068` | 20,939 | small-redundant | KE138872 | 54% | 97% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000040` | 20,837 | small-redundant | - | 0% | 100% | CM023090,JAAUHK010000006,JAAUHK010000009 | 0 |
| `JAAUHK010000031` | 19,995 | small-redundant | KE138841 | 100% | 100% | CM023094,JAAUHK010000005,JAAUHK010000025 | 9 |
| `JAAUHK010000146` | 19,704 | small-redundant | KE139166 | 50% | 99% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000097` | 19,546 | small-redundant | KE139166 | 38% | 97% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000028` | 19,262 | small-redundant | - | 0% | 94% | CM023082 | 6 |
| `JAAUHK010000075` | 18,954 | small-redundant | - | 0% | 100% | CM023087,CM023091,JAAUHK010000002 | 0 |
| `JAAUHK010000042` | 18,719 | small-redundant | - | 0% | 100% | CM023086 | 0 |
| `JAAUHK010000069` | 18,672 | small-redundant | - | 0% | 100% | CM023090,CM023091,JAAUHK010000002 | 1 |
| `JAAUHK010000070` | 18,629 | small-redundant | chrV | 28% | 100% | CM023087,CM023091,JAAUHK010000002 | 0 |
| `JAAUHK010000050` | 18,556 | small-redundant | - | 0% | 100% | CM023090,JAAUHK010000006,JAAUHK010000009 | 0 |
| `JAAUHK010000052` | 17,948 | small-redundant | KE139832 | 45% | 96% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000083` | 17,918 | small-redundant | KE138876 | 60% | 100% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000126` | 17,891 | small-redundant | chrIX | 23% | 100% | CM023090,JAAUHK010000006,JAAUHK010000009 | 0 |
| `JAAUHK010000071` | 17,563 | small-redundant | - | 0% | 100% | CM023093,JAAUHK010000038,JAAUHK010000108 | 1 |
| `JAAUHK010000144` | 17,426 | small-redundant | KE141015 | 85% | 97% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000072` | 16,787 | small-redundant | - | 0% | 99% | CM023086,CM023087,CM023090 | 3 |
| `JAAUHK010000096` | 16,772 | small-redundant | - | 0% | 100% | CM023090,JAAUHK010000006,JAAUHK010000009 | 0 |
| `JAAUHK010000039` | 16,651 | small-redundant | KE140399 | 13% | 100% | CM023085 | 3 |
| `JAAUHK010000074` | 16,612 | small-redundant | - | 0% | 100% | CM023086 | 0 |
| `JAAUHK010000045` | 16,587 | small-redundant | KE139166 | 67% | 99% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000013` | 16,299 | small-redundant | - | 0% | 100% | CM023090,JAAUHK010000006,JAAUHK010000009 | 0 |
| `JAAUHK010000091` | 15,978 | small-redundant | KE140467 | 16% | 100% | CM023088 | 0 |
| `JAAUHK010000163` | 15,945 | small-redundant | KE140582 | 48% | 99% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000148` | 15,928 | small-redundant | - | 0% | 100% | CM023093,JAAUHK010000038,JAAUHK010000071 | 0 |
| `JAAUHK010000057` | 15,666 | small-redundant | - | 0% | 100% | CM023091 | 2 |
| `JAAUHK010000101` | 15,527 | small-redundant | - | 0% | 100% | CM023090,JAAUHK010000006,JAAUHK010000009 | 0 |
| `JAAUHK010000121` | 15,470 | small-redundant | KE140722 | 65% | 96% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000058` | 15,460 | small-redundant | - | 0% | 99% | CM023090,CM023092,JAAUHK010000002 | 1 |
| `JAAUHK010000105` | 15,457 | small-redundant | KE138876 | 81% | 99% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000056` | 15,409 | small-redundant | KE138876 | 73% | 98% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000103` | 15,366 | small-redundant | - | 0% | 100% | CM023091 | 0 |
| `JAAUHK010000063` | 15,308 | small-redundant | KE139817 | 55% | 100% | CM023092,JAAUHK010000002,JAAUHK010000014 | 1 |
| `JAAUHK010000149` | 15,293 | small-redundant | KE139817 | 100% | 100% | CM023092,JAAUHK010000002,JAAUHK010000014 | 1 |
| `JAAUHK010000124` | 15,286 | small-redundant | - | 0% | 100% | CM023090,JAAUHK010000006,JAAUHK010000009 | 0 |
| `JAAUHK010000178` | 15,229 | small-redundant | KE138872 | 44% | 97% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000168` | 15,176 | small-redundant | KE139165 | 71% | 99% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000173` | 15,174 | small-redundant | KE138872 | 55% | 98% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000061` | 15,121 | small-redundant | KE138876 | 77% | 100% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 1 |
| `JAAUHK010000125` | 15,046 | small-redundant | - | 0% | 100% | CM023090,JAAUHK010000006,JAAUHK010000009 | 0 |
| `JAAUHK010000081` | 14,965 | small-redundant | KE138862 | 38% | 100% | CM023093 | 2 |
| `JAAUHK010000106` | 14,710 | small-redundant | KE138872 | 68% | 100% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000171` | 14,651 | small-redundant | KE140556 | 74% | 98% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000082` | 14,548 | small-redundant | KE138872 | 58% | 100% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000174` | 14,261 | small-redundant | KE140722 | 76% | 100% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000076` | 14,226 | small-redundant | KE138878 | 27% | 98% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000099` | 14,209 | small-redundant | chrVIIa | 83% | 100% | CM023088 | 6 |
| `JAAUHK010000147` | 14,188 | small-redundant | - | 0% | 100% | CM023093,JAAUHK010000038,JAAUHK010000071 | 0 |
| `JAAUHK010000180` | 14,132 | small-redundant | KE138876 | 53% | 90% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000139` | 14,119 | small-redundant | KE139166 | 78% | 100% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000172` | 14,109 | small-redundant | - | 0% | 100% | CM023091 | 0 |
| `JAAUHK010000120` | 14,065 | small-redundant | KE139839 | 60% | 100% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000065` | 13,792 | small-redundant | KE138872 | 65% | 100% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000165` | 13,726 | small-redundant | KE139165 | 36% | 92% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000131` | 13,614 | small-redundant | KE140738 | 58% | 100% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000053` | 13,542 | small-redundant | KE138878 | 56% | 100% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000109` | 13,468 | small-redundant | KE139165 | 50% | 100% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000119` | 13,448 | small-redundant | KE138876 | 64% | 100% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000030` | 13,384 | small-redundant | KE139836 | 88% | 99% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 3 |
| `JAAUHK010000094` | 13,375 | small-redundant | KE138876 | 55% | 99% | JAAUHK010000030,JAAUHK010000032,JAAUHK010000033 | 0 |
| `JAAUHK010000088` | 13,356 | small-redundant | KE138876 | 96% | 100% | JAAUHK010000030,JAAUHK010000032,JAAUHK010000033 | 0 |
| `JAAUHK010000114` | 13,239 | small-redundant | - | 0% | 99% | CM023093 | 2 |
| `JAAUHK010000037` | 12,942 | small-redundant | KE140738 | 82% | 99% | JAAUHK010000030,JAAUHK010000032,JAAUHK010000033 | 0 |
| `JAAUHK010000164` | 12,804 | small-redundant | KE138876 | 67% | 100% | JAAUHK010000030,JAAUHK010000032,JAAUHK010000033 | 0 |
| `JAAUHK010000170` | 12,762 | small-redundant | KE138876 | 56% | 92% | JAAUHK010000030,JAAUHK010000032,JAAUHK010000033 | 0 |
| `JAAUHK010000046` | 12,539 | small-redundant | KE139165 | 75% | 92% | JAAUHK010000030,JAAUHK010000032,JAAUHK010000033 | 0 |
| `JAAUHK010000137` | 12,494 | small-redundant | KE138878 | 57% | 100% | JAAUHK010000030,JAAUHK010000032,JAAUHK010000033 | 0 |
| `JAAUHK010000128` | 12,344 | small-redundant | KE138876 | 54% | 97% | JAAUHK010000030,JAAUHK010000032,JAAUHK010000033 | 0 |
| `JAAUHK010000086` | 12,278 | small-redundant | KE139832 | 27% | 100% | JAAUHK010000030,JAAUHK010000032,JAAUHK010000033 | 0 |
| `JAAUHK010000183` | 11,228 | small-redundant | KE138876 | 59% | 100% | JAAUHK010000030,JAAUHK010000032,JAAUHK010000033 | 0 |
| `JAAUHK010000077` | 11,057 | small-redundant | KE140556 | 70% | 98% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000116` | 11,046 | small-redundant | KE139166 | 51% | 99% | JAAUHK010000030,JAAUHK010000032,JAAUHK010000033 | 0 |
| `JAAUHK010000166` | 10,824 | small-redundant | - | 0% | 100% | JAAUHK010000030,JAAUHK010000032,JAAUHK010000033 | 0 |
| `JAAUHK010000107` | 10,337 | small-redundant | KE140738 | 94% | 94% | JAAUHK010000030,JAAUHK010000032,JAAUHK010000033 | 0 |
| `JAAUHK010000098` | 10,302 | small-redundant | KE139166 | 73% | 100% | JAAUHK010000030,JAAUHK010000032,JAAUHK010000033 | 0 |
| `JAAUHK010000123` | 10,296 | small-redundant | KE139832 | 68% | 100% | JAAUHK010000030,JAAUHK010000032,JAAUHK010000033 | 0 |
| `JAAUHK010000024` | 10,279 | small-redundant | KE138841 | 80% | 96% | CM023094,JAAUHK010000005,JAAUHK010000025 | 0 |
| `JAAUHK010000129` | 10,253 | small-redundant | KE138876 | 37% | 98% | JAAUHK010000030,JAAUHK010000032,JAAUHK010000033 | 0 |
| `JAAUHK010000176` | 10,206 | small-redundant | KE139166 | 50% | 98% | JAAUHK010000030,JAAUHK010000032,JAAUHK010000033 | 0 |
| `JAAUHK010000145` | 10,180 | small-redundant | KE140556 | 58% | 100% | JAAUHK010000030,JAAUHK010000032,JAAUHK010000033 | 0 |
| `JAAUHK010000078` | 10,144 | small-redundant | KE140722 | 65% | 99% | JAAUHK010000030,JAAUHK010000032,JAAUHK010000033 | 0 |
| `JAAUHK010000003` | 116,436 | small-unplaced | KE138903 | 12% | 2% | CM023090 | 2 |
| `JAAUHK010000002` | 97,714 | small-unplaced | KE139817 | 19% | 53% | CM023086,CM023087,CM023090 | 5 |
| `JAAUHK010000004` | 79,187 | small-unplaced | KE139848 | 21% | 80% | CM023083 | 3 |
| `JAAUHK010000038` | 60,965 | small-unplaced | - | 0% | 87% | CM023093 | 0 |
| `JAAUHK010000008` | 60,946 | small-unplaced | - | 0% | 31% | CM023081,CM023083,CM023087 | 7 |
| `JAAUHK010000017` | 47,576 | small-unplaced | - | 0% | 54% | CM023086,CM023087,CM023090 | 3 |
| `JAAUHK010000016` | 43,284 | small-unplaced | - | 0% | 24% | CM023085 | 5 |
| `JAAUHK010000011` | 39,556 | small-unplaced | - | 0% | 83% | CM023086,CM023087,CM023090 | 4 |
| `JAAUHK010000007` | 39,225 | small-unplaced | - | 0% | 82% | CM023086,CM023087,CM023090 | 3 |
| `JAAUHK010000014` | 33,523 | small-unplaced | KE138884 | 6% | 68% | CM023087,CM023090,CM023092 | 2 |
| `JAAUHK010000034` | 33,024 | small-unplaced | KE139166 | 30% | 78% | JAAUHK010000041 | 0 |
| `JAAUHK010000022` | 27,554 | small-unplaced | - | 0% | 80% | CM023087,CM023091,JAAUHK010000002 | 0 |
| `JAAUHK010000051` | 26,503 | small-unplaced | - | 0% | 88% | CM023093 | 4 |
| `JAAUHK010000027` | 23,444 | small-unplaced | - | 0% | 68% | CM023093,JAAUHK010000051 | 0 |
| `JAAUHK010000021` | 22,331 | small-unplaced | - | 0% | 85% | CM023093,JAAUHK010000051 | 4 |
| `JAAUHK010000073` | 20,079 | small-unplaced | - | 0% | 84% | CM023092,JAAUHK010000002,JAAUHK010000014 | 1 |
| `JAAUHK010000054` | 18,389 | small-unplaced | KE138872 | 23% | 89% | JAAUHK010000032,JAAUHK010000033,JAAUHK010000034 | 0 |
| `JAAUHK010000029` | 15,111 | small-unplaced | - | 0% | 14% | JAAUHK010000008,JAAUHK010000072 | 4 |

**RUB**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `KN040019` | 341,078 | small-unplaced | - | 0% | 0% | - | 63 |
| `KN040021` | 333,564 | small-unplaced | - | 0% | 0% | - | 58 |
| `KN040028` | 182,829 | small-unplaced | - | 0% | 0% | - | 22 |
| `KN040030` | 142,217 | small-unplaced | - | 0% | 2% | KN039997 | 6 |
| `KN040033` | 103,768 | small-unplaced | - | 0% | 0% | - | 3 |
| `KN040034` | 101,694 | small-unplaced | - | 0% | 0% | - | 4 |
| `KN040035` | 98,727 | small-unplaced | - | 0% | 1% | KN039999 | 14 |
| `KN040036` | 62,628 | small-unplaced | - | 0% | 0% | - | 5 |
| `KN040037` | 58,088 | small-unplaced | KE140935 | 7% | 0% | - | 5 |
| `KN040038` | 49,401 | small-unplaced | - | 0% | 22% | KN040036 | 2 |
| `KN040039` | 49,370 | small-unplaced | - | 0% | 14% | KN039997,KN040030 | 4 |
| `KN040040` | 49,364 | small-unplaced | - | 0% | 0% | - | 4 |
| `KN040041` | 47,228 | small-unplaced | - | 0% | 0% | - | 7 |
| `KN040042` | 46,326 | small-unplaced | - | 0% | 0% | - | 1 |
| `KN040043` | 45,616 | small-unplaced | - | 0% | 0% | - | 2 |
| `KN040044` | 43,951 | small-unplaced | - | 0% | 0% | - | 8 |
| `KN040045` | 42,109 | small-unplaced | - | 0% | 0% | - | 3 |
| `KN040047` | 40,757 | small-unplaced | - | 0% | 9% | KN040022,KN040035 | 6 |
| `KN040048` | 39,693 | small-unplaced | - | 0% | 0% | - | 2 |
| `KN040049` | 38,593 | small-unplaced | - | 0% | 0% | - | 2 |
| `KN040050` | 34,629 | small-unplaced | - | 0% | 8% | KN040047 | 7 |
| `KN040051` | 29,902 | small-unplaced | - | 0% | 12% | KN039988,KN040045 | 4 |
| `KN040052` | 29,821 | small-unplaced | - | 0% | 0% | - | 4 |
| `KN040053` | 26,894 | small-unplaced | - | 0% | 0% | - | 2 |
| `KN040054` | 25,922 | small-unplaced | - | 0% | 0% | - | 1 |
| `KN040055` | 24,770 | small-unplaced | - | 0% | 4% | KN040050 | 7 |
| `KN040056` | 24,606 | small-unplaced | chrVIIb | 10% | 0% | - | 5 |
| `KN040057` | 23,987 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN040058` | 22,812 | small-unplaced | - | 0% | 0% | - | 1 |
| `KN040059` | 21,210 | small-unplaced | - | 0% | 0% | - | 2 |
| `KN040061` | 19,873 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN040062` | 17,241 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN040063` | 16,590 | small-unplaced | - | 0% | 0% | - | 1 |
| `KN040064` | 16,182 | small-unplaced | - | 0% | 0% | - | 1 |
| `KN040065` | 14,840 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN040066` | 14,066 | small-unplaced | - | 0% | 0% | - | 1 |
| `KN040067` | 13,071 | small-unplaced | - | 0% | 0% | - | 1 |
| `KN040068` | 12,142 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN040069` | 11,578 | small-unplaced | - | 0% | 34% | KN040050,KN040055,KN040062 | 4 |
| `KN040070` | 10,683 | small-unplaced | - | 0% | 0% | - | 0 |

**TgCATBr9**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `KZ792174.1` | 726,067 | small-unplaced | - | 0% | 0% | - | 135 |
| `KZ793375.1` | 468,435 | small-unplaced | - | 0% | 0% | - | 64 |
| `KZ791488.1` | 364,986 | small-unplaced | - | 0% | 0% | - | 53 |
| `KZ792213.1` | 183,658 | small-unplaced | - | 0% | 0% | - | 25 |
| `KZ792917.1` | 158,771 | small-unplaced | - | 0% | 0% | - | 32 |
| `KZ791142.1` | 112,684 | small-unplaced | - | 0% | 0% | - | 6 |
| `KZ793196.1` | 72,216 | small-unplaced | - | 0% | 0% | - | 2 |
| `KZ791957.1` | 59,291 | small-unplaced | KE140935 | 7% | 0% | - | 5 |
| `KZ791261.1` | 54,101 | small-unplaced | - | 0% | 0% | - | 3 |
| `KZ793305.1` | 53,561 | small-unplaced | - | 0% | 0% | - | 5 |
| `KZ792895.1` | 52,288 | small-unplaced | - | 0% | 0% | - | 8 |
| `KZ792066.1` | 50,235 | small-unplaced | - | 0% | 0% | - | 0 |
| `KZ791789.1` | 50,213 | small-unplaced | - | 0% | 16% | KZ791142.1,KZ793296.1 | 4 |
| `KZ790956.1` | 50,132 | small-unplaced | - | 0% | 0% | - | 2 |
| `KZ791157.1` | 48,118 | small-unplaced | - | 0% | 0% | - | 1 |
| `KZ791677.1` | 45,291 | small-unplaced | - | 0% | 0% | - | 8 |
| `KZ792196.1` | 44,705 | small-unplaced | - | 0% | 0% | - | 2 |
| `KZ792740.1` | 43,914 | small-unplaced | chrII | 8% | 0% | - | 2 |
| `KZ792021.1` | 40,024 | small-unplaced | - | 0% | 0% | - | 2 |
| `KZ792902.1` | 34,195 | small-unplaced | - | 0% | 0% | - | 7 |
| `KZ791125.1` | 29,969 | small-unplaced | - | 0% | 0% | - | 4 |
| `KZ793288.1` | 26,394 | small-unplaced | chrX | 4% | 0% | - | 1 |
| `KZ791013.1` | 26,330 | small-unplaced | - | 0% | 0% | - | 2 |
| `KZ791970.1` | 26,271 | small-unplaced | - | 0% | 0% | - | 3 |
| `KZ791949.1` | 23,742 | small-unplaced | - | 0% | 0% | - | 4 |
| `KZ791690.1` | 19,435 | small-unplaced | - | 0% | 0% | - | 3 |
| `KZ792366.1` | 19,331 | small-unplaced | - | 0% | 0% | - | 0 |
| `KZ791211.1` | 17,725 | small-unplaced | - | 0% | 0% | - | 7 |
| `KZ792701.1` | 16,965 | small-unplaced | - | 0% | 0% | - | 1 |
| `KZ791987.1` | 16,013 | small-unplaced | - | 0% | 0% | - | 0 |
| `KZ792710.1` | 15,703 | small-unplaced | - | 0% | 0% | - | 1 |
| `KZ793372.1` | 15,315 | small-unplaced | - | 0% | 0% | - | 2 |
| `KZ791791.1` | 14,014 | small-unplaced | - | 0% | 0% | - | 4 |
| `KZ791095.1` | 13,268 | small-unplaced | - | 0% | 0% | - | 1 |
| `KZ791327.1` | 13,198 | small-unplaced | - | 0% | 0% | - | 2 |
| `KZ792006.1` | 11,517 | small-unplaced | - | 0% | 0% | - | 0 |
| `KZ791854.1` | 10,725 | small-unplaced | - | 0% | 0% | - | 1 |

**TgCatPRC2**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `KQ983297` | 416,056 | small-unplaced | - | 0% | 0% | - | 70 |
| `KQ986326` | 292,629 | small-unplaced | - | 0% | 0% | - | 35 |
| `KQ983319` | 122,291 | small-unplaced | - | 0% | 0% | - | 5 |
| `KQ983324` | 69,423 | small-unplaced | - | 0% | 0% | - | 3 |
| `KQ983325` | 47,656 | small-unplaced | - | 0% | 0% | - | 0 |
| `KQ983328` | 46,078 | small-unplaced | - | 0% | 0% | - | 8 |
| `KQ983326` | 43,867 | small-unplaced | - | 0% | 0% | - | 7 |
| `KQ983330` | 43,840 | small-unplaced | - | 0% | 0% | - | 0 |
| `KQ983329` | 35,967 | small-unplaced | - | 0% | 0% | - | 1 |
| `KQ983333` | 33,303 | small-unplaced | - | 0% | 0% | - | 3 |
| `KQ983331` | 29,059 | small-unplaced | - | 0% | 0% | - | 3 |
| `KQ983335` | 28,573 | small-unplaced | - | 0% | 0% | - | 2 |
| `KQ983334` | 27,032 | small-unplaced | - | 0% | 0% | - | 6 |
| `KQ983336` | 24,370 | small-unplaced | - | 0% | 0% | - | 1 |
| `KQ983340` | 20,668 | small-unplaced | - | 0% | 0% | - | 0 |
| `KQ983343` | 20,399 | small-unplaced | - | 0% | 0% | - | 0 |
| `KQ983342` | 20,152 | small-unplaced | KE140747 | 6% | 0% | - | 7 |
| `KQ983337` | 18,728 | small-unplaced | - | 0% | 0% | - | 1 |
| `KQ983338` | 17,854 | small-unplaced | - | 0% | 0% | - | 4 |
| `KQ983341` | 16,874 | small-unplaced | - | 0% | 0% | - | 0 |
| `KQ983347` | 16,362 | small-unplaced | - | 0% | 0% | - | 2 |
| `KQ983344` | 16,132 | small-unplaced | KE138862 | 44% | 0% | - | 5 |
| `KQ983348` | 14,577 | small-unplaced | - | 0% | 0% | - | 0 |
| `KQ983351` | 11,989 | small-unplaced | - | 0% | 0% | - | 6 |
| `KQ983350` | 11,634 | small-unplaced | - | 0% | 22% | KQ983333 | 0 |
| `KQ983352` | 11,559 | small-unplaced | - | 0% | 0% | - | 0 |
| `KQ983360` | 11,485 | small-unplaced | - | 0% | 0% | - | 0 |
| `KQ983354` | 10,931 | small-unplaced | - | 0% | 0% | - | 0 |
| `KQ983357` | 10,620 | small-unplaced | KE139425 | 24% | 0% | - | 0 |

**VAND**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `KN042504` | 346,857 | small-unplaced | KE140714 | 1% | 0% | - | 55 |
| `KN042514` | 155,285 | small-unplaced | - | 0% | 3% | KN042477 | 9 |
| `KN042516` | 95,508 | small-unplaced | KE138870 | 3% | 0% | - | 1 |
| `KN042517` | 74,792 | small-unplaced | - | 0% | 0% | - | 2 |
| `KN042518` | 59,598 | small-unplaced | KE140935 | 7% | 0% | - | 4 |
| `KN042519` | 56,330 | small-unplaced | - | 0% | 0% | - | 1 |
| `KN042520` | 52,576 | small-unplaced | - | 0% | 0% | - | 2 |
| `KN042522` | 50,502 | small-unplaced | - | 0% | 0% | - | 2 |
| `KN042523` | 49,630 | small-unplaced | - | 0% | 13% | KN042477,KN042514 | 2 |
| `KN042524` | 45,970 | small-unplaced | KE139814 | 28% | 0% | - | 2 |
| `KN042525` | 43,982 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN042526` | 42,299 | small-unplaced | - | 0% | 3% | KN042519 | 7 |
| `KN042528` | 39,919 | small-unplaced | - | 0% | 41% | KN042520 | 2 |
| `KN042529` | 39,052 | small-unplaced | - | 0% | 0% | - | 5 |
| `KN042530` | 32,519 | small-unplaced | - | 0% | 0% | - | 3 |
| `KN042531` | 28,591 | small-unplaced | - | 0% | 0% | - | 6 |
| `KN042532` | 24,717 | small-unplaced | - | 0% | 0% | - | 2 |
| `KN042533` | 22,203 | small-unplaced | - | 0% | 11% | KN042484 | 7 |
| `KN042535` | 19,145 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN042536` | 18,578 | small-unplaced | - | 0% | 0% | - | 4 |
| `KN042537` | 17,479 | small-unplaced | - | 0% | 0% | - | 1 |
| `KN042538` | 16,842 | small-unplaced | - | 0% | 0% | - | 2 |
| `KN042539` | 14,648 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN042540` | 12,356 | small-unplaced | - | 0% | 0% | - | 0 |
| `KN042541` | 12,157 | small-unplaced | - | 0% | 0% | - | 6 |
| `KN042543` | 10,323 | small-unplaced | - | 0% | 0% | - | 0 |

**VEG**

| contig | length | class | ref chr | % to ref | % dup in longer | covered by | genes |
| :--- | ---: | :--- | :--- | ---: | ---: | :--- | ---: |
| `KI544527` | 57,578 | small-unplaced | - | 0% | 3% | TGVEG_chrXII | 6 |
| `KI544532` | 44,204 | small-unplaced | KE139168 | 19% | 3% | TGVEG_chrXII | 3 |
| `KI544528` | 42,418 | small-unplaced | - | 0% | 0% | - | 1 |
| `KI544529` | 35,213 | small-unplaced | - | 0% | 0% | - | 0 |
| `KI544539` | 32,477 | small-unplaced | - | 0% | 0% | - | 1 |
| `KI544538` | 29,013 | small-unplaced | - | 0% | 0% | - | 0 |
| `KI544543` | 19,881 | small-unplaced | - | 0% | 0% | - | 1 |
| `KI544537` | 19,758 | small-unplaced | - | 0% | 25% | TGVEG_chrX | 0 |
| `KI544546` | 16,858 | small-unplaced | KE139827 | 27% | 0% | - | 0 |
| `KI544549` | 16,249 | small-unplaced | - | 0% | 9% | KI544538 | 0 |
| `KI544548` | 16,023 | small-unplaced | - | 0% | 6% | TGVEG_chrV | 4 |
| `KI544545` | 14,361 | small-unplaced | - | 0% | 0% | - | 7 |
| `KI544551` | 11,849 | small-unplaced | - | 0% | 21% | TGVEG_chrIX | 0 |
| `KI544544` | 11,640 | small-unplaced | - | 0% | 0% | - | 2 |

#### How to read this

- **small-redundant + 0 genes** — safe to drop (pure duplicated sequence).
- **small-redundant + genes > 0** — check the genes: BLASTp the proteins on that contig against the retained contigs; drop only if every gene has a ≥ 98% identity / ≥ 90% coverage hit elsewhere (otherwise the contig carries real sequence and should stay).
- **small-unplaced** — not redundant and doesn't map to the reference: could be genuine accessory content, a divergent subtelomere, or contamination. Inspect (BLAST vs nt, check gene annotations) before deciding.
- **large** contigs are never auto-flagged; if a genome shows more than 8, a chromosome is split — that's fragmentation, handled separately from redundancy.

Per-contig tables: `<self-dir>/<label>.contigs.tsv`.