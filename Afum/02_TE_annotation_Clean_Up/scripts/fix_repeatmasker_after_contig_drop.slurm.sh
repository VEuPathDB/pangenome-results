#!/bin/bash
#SBATCH --job-name=fix_rm_contigs
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:30:00
#SBATCH --output=fix_rm_contigs_%j.out
#SBATCH --error=fix_rm_contigs_%j.err
#
# Afum-only fix. RepeatMasker was run on the assemblies BEFORE the step-01 contig
# drop, so each RM_<genome_id>/ still has hits on contigs that were removed after.
# This rewrites the .out / .gff / .tbl to match the final dataset, into a new
# folder (originals untouched). Pure Python, stdlib only — a few seconds.
#
# Submit from your project folder (the one holding the RM_<genome_id>/ dirs):
#     sbatch 02_TE_annotation_Clean_Up/scripts/fix_repeatmasker_after_contig_drop.slurm.sh
#
# ─── ADAPT: the paths below, the ### ADAPT ### block, and the #SBATCH lines ───
RM_INDIR="."                                           # holds the RM_<genome_id>/ dirs
DROP_LIST="01_Genome_Selection_QC/drop_contigs.txt"     # the step-01 manifest
OUTDIR="repeatmasker_contig_filtered"                   # cleaned RM_<genome_id>/ go here (new dir)
#
# Alternative: instead of the manifest, compare against the final assemblies
# (more accurate .tbl 'total length'). Leave DROP_LIST="" and set:
GENOMES=""                                              # e.g. "genomes"
# ────────────────────────────────────────────────────────────────────────────

set -euo pipefail

# Locate the .py. Under `sbatch` the wrapper is copied to a spool dir, so
# ${BASH_SOURCE[0]} is useless there — fall back to the standard layout relative
# to the directory you submitted from.
PY=""
for cand in \
    "$(dirname "${BASH_SOURCE[0]}")/fix_repeatmasker_after_contig_drop.py" \
    "${SLURM_SUBMIT_DIR:-$PWD}/02_TE_annotation_Clean_Up/scripts/fix_repeatmasker_after_contig_drop.py" \
    "02_TE_annotation_Clean_Up/scripts/fix_repeatmasker_after_contig_drop.py"
do
    [[ -f "$cand" ]] && { PY="$cand"; break; }
done
[[ -n "$PY" ]] || { echo "ERROR: cannot find fix_repeatmasker_after_contig_drop.py (run from the project folder)" >&2; exit 1; }

### ADAPT ### — put a python3 (>= 3.6, stdlib only) on the PATH. Any env works;
#              the step-01 / synteny env is fine, or the system python3:
# set +u
# module load python/3.11 || true
# set -u
### END ADAPT ###

command -v python3 >/dev/null || { echo "ERROR: python3 not on PATH" >&2; exit 1; }
compgen -G "$RM_INDIR"/RM_*/ >/dev/null || compgen -G "$RM_INDIR"/R_*/ >/dev/null \
    || compgen -G "$RM_INDIR"/*.out >/dev/null \
    || { echo "ERROR: no RM_<genome_id>/ folders or *.out files in $RM_INDIR" >&2; exit 1; }

SRC_ARGS=()
if [[ -n "${DROP_LIST:-}" ]]; then
    [[ -f "$DROP_LIST" ]] || { echo "ERROR: drop list not found: $DROP_LIST" >&2; exit 1; }
    SRC_ARGS=(--drop-list "$DROP_LIST")
elif [[ -n "${GENOMES:-}" ]]; then
    [[ -d "$GENOMES" ]] || { echo "ERROR: genomes folder not found: $GENOMES" >&2; exit 1; }
    SRC_ARGS=(--genomes-dir "$GENOMES")
else
    echo "ERROR: set DROP_LIST or GENOMES at the top of the script" >&2; exit 1
fi

python3 "$PY" --rm-indir "$RM_INDIR" "${SRC_ARGS[@]}" --outdir "$OUTDIR"

echo "Done — cleaned RM folders in $OUTDIR/"
