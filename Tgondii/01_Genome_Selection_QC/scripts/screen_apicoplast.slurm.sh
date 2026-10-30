#!/bin/bash
#SBATCH --job-name=screen_apicoplast
#SBATCH --partition=low
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=02:00:00
#SBATCH --output=screen_apicoplast_%j.out
#SBATCH --error=screen_apicoplast_%j.err
#
# Tgondii-only, step 01 (removal before step 05's build). Finds the apicoplast contig(s) of every genome: pulls the reference apicoplast (ME49 contig
# KE138841) out of the ME49 assembly, blastn's it against every genome, and calls a contig apicoplast when at least
# MIN_CONTIG_COV of the contig is covered by hits (apicoplast_contigs.py). The resulting apicoplast_contigs.tsv has the
# column layout of redundant_contigs_removed.tsv; both lists are read by step 05's
# remove_contigs_before_build.slurm.sh. Submit from the project folder:
#     sbatch 01_Genome_Selection_QC/scripts/screen_apicoplast.slurm.sh
#
# ─── ADAPT: the paths below (relative to the project folder) ───
SOURCE_GENOME="ME49"
APICOPLAST_CONTIG="KE138841"
GENOME_DIR="genomes"
ORDER="genome_order.txt"
GFF_DIR="gff_for_liftoff"; GFF_SUFFIX=".gff3"   # only to count genes per contig (the GFFs prepared for Liftoff)
MIN_CONTIG_COV="0.9"
OUT_DIR="01_Genome_Selection_QC/apicoplast_screen"
# ────────────────────────────────────────────────────────────────

set -euo pipefail
set +u
module purge
### ADAPT ### — put blastn / samtools / python3 on the PATH:
export MAMBA_ROOT_PREFIX="/home/aludwig/hc-storage/micromamba"
export MAMBA_EXE="/home/aludwig/hc-storage/bin/micromamba/micromamba"
eval "$("$MAMBA_EXE" shell hook --shell bash --root-prefix "$MAMBA_ROOT_PREFIX")"
micromamba activate bioinfo
### END ADAPT ###
set -u

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
PY=""
for cand in "$(dirname "${BASH_SOURCE[0]}")" "$PROJECT_DIR/01_Genome_Selection_QC/scripts" "01_Genome_Selection_QC/scripts"; do
    [[ -f "$cand/apicoplast_contigs.py" ]] && { PY="$cand/apicoplast_contigs.py"; break; }
done
[[ -n "$PY" ]] || { echo "ERROR: cannot find apicoplast_contigs.py (run from the project folder)" >&2; exit 1; }

mkdir -p "$OUT_DIR/blast"
samtools faidx "$GENOME_DIR/$SOURCE_GENOME.fna" "$APICOPLAST_CONTIG" > "$OUT_DIR/apicoplast.fna"
FMT='6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen'
while read -r g; do
    [[ -z "$g" || "$g" == \#* ]] && continue
    echo "=== $g"
    blastn -query "$OUT_DIR/apicoplast.fna" -subject "$GENOME_DIR/$g.fna" -dust no -outfmt "$FMT" \
        -evalue 1e-10 -max_target_seqs 100 > "$OUT_DIR/blast/$g.tsv" || true
done < <(awk '{print $1}' "$ORDER")

python3 "$PY" --blast-dir "$OUT_DIR/blast" --out-dir "$OUT_DIR" --min-contig-cov "$MIN_CONTIG_COV" \
    --gff-dir "$GFF_DIR" --gff-suffix "$GFF_SUFFIX"
echo "Done. See $OUT_DIR/apicoplast_contigs.tsv"
