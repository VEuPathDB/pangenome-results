#!/bin/bash
#SBATCH --job-name=plot_filter_qc
#SBATCH --partition=low
#SBATCH --output=filter_qc_plots/logs/%x_%j.out
#SBATCH --error=filter_qc_plots/logs/%x_%j.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=01:00:00

set -euo pipefail

# Run this after 7a (filter_final_annotation_job.sh) has finished. Submit from your project
# folder. The log folder must exist BEFORE submitting (SLURM does not create it):
#     mkdir -p filter_qc_plots/logs && sbatch 05_Cross-genome_annotation_integration/scripts/plot_filter_qc_job.sh

# Edit these for your run.
STRAINS="genome_order.txt"                   # comma-separated names or a file with one per line, first = the reference (same as ORDER)
ORIGINAL_DIR="expanded_annotation"           # build_final_annotation_basic.sh's OUTPUT_DIR (before filtering)
FILTERED_DIR="filtered_annotation"           # 7a's OUT_DIR (after filtering)
MIN_OVERLAP_BP="20"                          # same --min-overlap-bp used for the real 7a run
OUT_DIR="filter_qc_plots"                    # where to write the plots and summary.tsv

set +u
module purge
### ADAPT ### — put micromamba on the PATH, then activate the env (needs Python 3 + matplotlib):
export MAMBA_ROOT_PREFIX="/home/aludwig/hc-storage/micromamba"
export MAMBA_EXE="/home/aludwig/hc-storage/bin/micromamba/micromamba"
eval "$("$MAMBA_EXE" shell hook --shell bash --root-prefix "$MAMBA_ROOT_PREFIX")"
micromamba activate plots
### END ADAPT ###
set -u

# Locate the .py. Under `sbatch` the wrapper is copied to a spool dir, so
# ${BASH_SOURCE[0]} is useless there - fall back to the standard layout
# relative to the directory you submitted from.
PY=""
for cand in \
    "$(dirname "${BASH_SOURCE[0]}")/plot_filter_qc.py" \
    "${SLURM_SUBMIT_DIR:-$PWD}/05_Cross-genome_annotation_integration/scripts/plot_filter_qc.py" \
    "05_Cross-genome_annotation_integration/scripts/plot_filter_qc.py"
do
    [[ -f "$cand" ]] && { PY="$cand"; break; }
done
[[ -n "$PY" ]] || { echo "ERROR: cannot find plot_filter_qc.py (run from the project folder)" >&2; exit 1; }
mkdir -p "$OUT_DIR"

python3 "$PY" \
  --strains "$STRAINS" \
  --original-dir "$ORIGINAL_DIR" \
  --filtered-dir "$FILTERED_DIR" \
  --min-overlap-bp "$MIN_OVERLAP_BP" \
  --out-dir "$OUT_DIR"

echo "QC plots completed. Outputs are in $OUT_DIR"
