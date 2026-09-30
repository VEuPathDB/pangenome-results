#!/bin/bash
#SBATCH --job-name=plot_all
#SBATCH --partition=low
#SBATCH --output=pangenome_plots/logs/%x_%j.out
#SBATCH --error=pangenome_plots/logs/%x_%j.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=16G
#SBATCH --time=03:00:00

# Every pangenome plot of step 08 in one job, after get_pangenes has finished. Submit from your
# project folder. The log folder must exist BEFORE submitting (SLURM does not create it):
#
#     mkdir -p pangenome_plots/logs
#     sbatch 08_Pangenome_Visualisation/scripts/plot_all_job.sh --set 7b --label Afum7b
#     sbatch 08_Pangenome_Visualisation/scripts/plot_all_job.sh --set 7a --label Afum7a
#
# or with every folder given by hand:
#
#     sbatch 08_Pangenome_Visualisation/scripts/plot_all_job.sh \
#         --pangenes-dir for_get_pangenes_7b_pangenes --gff-dir for_get_pangenes_7b --label Afum7b --overlap yes
#
# Options (--pangenes-dir, --gff-dir and --label are required unless --set gives the first two):
#   --pangenes-dir DIR   get_pangenes output folder. The matrices are found by name, wherever they are below it
#                        (get_pangenes puts them in a subfolder whose name depends on the genome and the options)
#   --matrix-subdir NAME only when DIR holds more than one pangene_matrix.tr.tab: the subfolder to use
#   --gff-dir DIR        the GFFs given to get_pangenes (link_for_get_pangenes_*.slurm.sh's OUT_DIR)
#   --gff-suffix S       GFF name = <genome><S> inside --gff-dir           (default _for_get_pangenes.gff)
#   --label LABEL        prefix of every output file                       (e.g. Afum7b)
#   --set 7a|7b          shortcut: --pangenes-dir for_get_pangenes_<set>_pangenes, --gff-dir for_get_pangenes_<set>,
#                        and --overlap yes for 7b, no for 7a
#   --overlap yes|no     also plot the unsupported overlapping genes; needs the tagged 7b GFFs (intersect=)  (default no)
#   --contig-sizes FILE  step-01 table with genome_label, contig, length   (default contig_size_profile/contig_sizes.tsv)
#   --entry-list FILE    InterPro IPR id -> name, downloaded there if missing (default /home/aludwig/hc-storage/interpro_entry.list)
#   --out-dir DIR        output folder                                     (default pangenome_plots)
#   --core-missing A  --softcore-missing B  --cloud-max C   how the categories are cut, in numbers of genomes
#                        (default 0 1 2: core = all genomes, soft-core = missing from at most 1 genome, cloud = in at
#                        most 2 genomes, shell the rest)
#   --categories A,B  --alpha X  --min-total N  --min-count N  --top N    domain enrichment settings (default Core,Cloud 0.05 5 3 15):
#                        --min-total = entries carried by fewer pangenes in the whole universe are not tested;
#                        --min-count = only entries carried by at least N pangenes of the category are drawn
#
# It runs, in this order: plot_all.sh (pan/core curves joined and separate, occupancy, soft-core genes
# missing per genome, singletons, POCS heatmap), plot_domain_enrichment.py, plot_occupancy_properties.py (linear and log axis),
# plot_occupancy_contigs.py (contig size classes), and plot_occupancy_invalid.py (pangenes with mostly
# invalid ORFs, count, percentage and the share by category, and the same for unsupported overlapping genes with --overlap yes).
# A plot that fails does not stop the others; the job lists the failed ones at the end and exits with an error.

set -uo pipefail

PANGENES_DIR=""; MATRIX_SUBDIR=""; GFF_DIR=""; GFF_SUFFIX="_for_get_pangenes.gff"; LABEL=""; SET=""
OVERLAP="no"
CONTIG_SIZES="contig_size_profile/contig_sizes.tsv"
ENTRY_LIST="/home/aludwig/hc-storage/interpro_entry.list"
OUT_DIR="pangenome_plots"
CATEGORIES="Core,Cloud"; ALPHA="0.05"; MIN_TOTAL="5"; MIN_COUNT="3"; TOP="15"
CORE_MISSING="0"; SOFTCORE_MISSING="1"; CLOUD_MAX="2"

usage() { sed -n '/^# Every pangenome plot/,/^# A plot that fails/p' "$0" | sed 's/^# \{0,1\}//' 1>&2; exit 1; }
while [[ $# -gt 0 ]]; do
    case "$1" in
        --pangenes-dir)  PANGENES_DIR="$2"; shift 2 ;;
        --matrix-subdir) MATRIX_SUBDIR="$2"; shift 2 ;;
        --gff-dir)       GFF_DIR="$2"; shift 2 ;;
        --gff-suffix)    GFF_SUFFIX="$2"; shift 2 ;;
        --label)         LABEL="$2"; shift 2 ;;
        --set)           SET="$2"; shift 2 ;;
        --overlap)       OVERLAP="$2"; shift 2 ;;
        --contig-sizes)  CONTIG_SIZES="$2"; shift 2 ;;
        --entry-list)    ENTRY_LIST="$2"; shift 2 ;;
        --out-dir)       OUT_DIR="$2"; shift 2 ;;
        --core-missing)     CORE_MISSING="$2"; shift 2 ;;
        --softcore-missing) SOFTCORE_MISSING="$2"; shift 2 ;;
        --cloud-max)        CLOUD_MAX="$2"; shift 2 ;;
        --categories)    CATEGORIES="$2"; shift 2 ;;
        --alpha)         ALPHA="$2"; shift 2 ;;
        --min-total)     MIN_TOTAL="$2"; shift 2 ;;
        --min-count)     MIN_COUNT="$2"; shift 2 ;;
        --top)           TOP="$2"; shift 2 ;;
        -h|--help)       usage ;;
        *) echo "ERROR: unknown option $1" >&2; usage ;;
    esac
done
if [[ -n "$SET" ]]; then
    [[ "$SET" == "7a" || "$SET" == "7b" ]] || { echo "ERROR: --set must be 7a or 7b" >&2; exit 1; }
    [[ -n "$PANGENES_DIR" ]] || PANGENES_DIR="for_get_pangenes_${SET}_pangenes"
    [[ -n "$GFF_DIR" ]]      || GFF_DIR="for_get_pangenes_${SET}"
    [[ "$SET" == "7b" && "$OVERLAP" == "no" ]] && OVERLAP="yes"
fi
[[ -n "$PANGENES_DIR" && -n "$GFF_DIR" && -n "$LABEL" ]] || { echo "ERROR: --label and either --set or --pangenes-dir and --gff-dir are required" >&2; usage; }
[[ "$OVERLAP" == "yes" || "$OVERLAP" == "no" ]] || { echo "ERROR: --overlap must be yes or no" >&2; exit 1; }
[[ -d "$PANGENES_DIR" ]] || { echo "ERROR: get_pangenes folder not found: $PANGENES_DIR" >&2; exit 1; }
[[ -d "$GFF_DIR" ]]      || { echo "ERROR: GFF folder not found: $GFF_DIR" >&2; exit 1; }

# ── environment ────────────────────────────────────────────────────────────────────────────────
# SKIP_ENV=1 skips the micromamba block (already inside an environment, or running locally).
set +u
module purge 2>/dev/null || true
### ADAPT ### — put micromamba on the PATH, then activate the env (needs Python 3 + numpy + scipy + matplotlib + pandas + seaborn):
if [[ -z "${SKIP_ENV:-}" ]]; then
    export MAMBA_ROOT_PREFIX="/home/aludwig/hc-storage/micromamba"
    export MAMBA_EXE="/home/aludwig/hc-storage/bin/micromamba/micromamba"
    eval "$("$MAMBA_EXE" shell hook --shell bash --root-prefix "$MAMBA_ROOT_PREFIX")"
    micromamba activate synteny
fi
### END ADAPT ###
set -u

for mod in numpy scipy matplotlib pandas seaborn; do
    python3 -c "import $mod" 2>/dev/null \
        || { echo "ERROR: the activated env has no python module '$mod' (needs numpy, scipy, matplotlib, pandas and seaborn)" >&2; exit 1; }
done

# Locate the scripts folder. Under `sbatch` the wrapper is copied to a spool dir, so
# ${BASH_SOURCE[0]} is useless there - fall back to the standard layout
# relative to the directory you submitted from.
SCRIPTS=""
for cand in \
    "$(dirname "${BASH_SOURCE[0]}")" \
    "${SLURM_SUBMIT_DIR:-$PWD}/08_Pangenome_Visualisation/scripts" \
    "08_Pangenome_Visualisation/scripts"
do
    [[ -f "$cand/plot_all.sh" ]] && { SCRIPTS="$(cd "$cand" && pwd)"; break; }
done
[[ -n "$SCRIPTS" ]] || { echo "ERROR: cannot find the 08 scripts folder (run from the project folder)" >&2; exit 1; }
mkdir -p "$OUT_DIR"

# ── find the matrices ──────────────────────────────────────────────────────────────────────────
# get_pangenes writes them in a subfolder named after the first genome and its options (for example
# <genome>_for_get_pangenes_0taxa_2neigh_algMmap_), so look for the file by name instead of guessing the folder.
SEARCH="$PANGENES_DIR"
[[ -n "$MATRIX_SUBDIR" ]] && SEARCH="$PANGENES_DIR/$MATRIX_SUBDIR"
FOUND=()
while IFS= read -r line; do FOUND+=("$line"); done < <(find "$SEARCH" -maxdepth 3 -name pangene_matrix.tr.tab 2>/dev/null | sort)
if [[ ${#FOUND[@]} -eq 0 ]]; then
    echo "ERROR: no pangene_matrix.tr.tab below $SEARCH (has get_pangenes finished?)" >&2; exit 1
elif [[ ${#FOUND[@]} -gt 1 ]]; then
    echo "ERROR: more than one pangene_matrix.tr.tab below $SEARCH; choose one with --matrix-subdir NAME:" >&2
    printf '  %s\n' "${FOUND[@]}" >&2; exit 1
fi
MATRIX="${FOUND[0]}"
GENES_MATRIX="$(dirname "$MATRIX")/pangene_matrix_genes.tr.tab"
[[ -f "$GENES_MATRIX" ]] || { echo "ERROR: $GENES_MATRIX not found next to $MATRIX" >&2; exit 1; }
echo "categories: core = missing from at most $CORE_MISSING genomes, soft-core = at most $SOFTCORE_MISSING, cloud = present in at most $CLOUD_MAX"
echo "label $LABEL | matrix $MATRIX | GFFs $GFF_DIR/<genome>$GFF_SUFFIX | overlap plot: $OVERLAP | output $OUT_DIR"

# ── run every plot; a failed plot is reported at the end and does not stop the others ────────
FAILED=()
step() {
    local name="$1"; shift
    echo; echo "=== $name"
    "$@" || { echo "FAILED: $name" >&2; FAILED+=("$name"); }
}
GENE_ARGS=(--genes-matrix "$GENES_MATRIX" --gff-dir "$GFF_DIR" --core-missing "$CORE_MISSING" --softcore-missing "$SOFTCORE_MISSING" --cloud-max "$CLOUD_MAX")
GFF_ARGS=("${GENE_ARGS[@]}" --gff-suffix "$GFF_SUFFIX")

export CORE_MISSING SOFTCORE_MISSING CLOUD_MAX   # plot_all.sh passes them to the occupancy plot
step "pan/core, occupancy, singletons, POCS" bash "$SCRIPTS/plot_all.sh" -i "$MATRIX" -o "$OUT_DIR" -l "$LABEL"

# Compute nodes may not reach the internet: download the list once on the login node,
# otherwise the plot falls back to IPR ids.
if [[ ! -f "$ENTRY_LIST" ]]; then
    curl -sfL -o "$ENTRY_LIST" "https://ftp.ebi.ac.uk/pub/databases/interpro/current_release/entry.list" \
        || { echo "WARNING: could not download the InterPro entry list; terms will be labelled by IPR id" >&2; rm -f "$ENTRY_LIST"; }
fi
ENTRY_ARGS=()
[[ -f "$ENTRY_LIST" ]] && ENTRY_ARGS+=(--entry-list "$ENTRY_LIST")
step "domain enrichment" python3 "$SCRIPTS/plot_domain_enrichment.py" "${GENE_ARGS[@]}" \
    -o "$OUT_DIR/${LABEL}_domain_enrichment" \
    --categories "$CATEGORIES" --alpha "$ALPHA" --min-total "$MIN_TOTAL" --min-count "$MIN_COUNT" --top "$TOP" \
    ${ENTRY_ARGS[@]+"${ENTRY_ARGS[@]}"}

step "gene properties by occupancy (linear axis)" python3 "$SCRIPTS/plot_occupancy_properties.py" "${GFF_ARGS[@]}" \
    -o "$OUT_DIR/${LABEL}_occupancy_properties"
step "gene properties by occupancy (log axis)" python3 "$SCRIPTS/plot_occupancy_properties.py" "${GFF_ARGS[@]}" --yscale log \
    -o "$OUT_DIR/${LABEL}_occupancy_properties_log"

if [[ -f "$CONTIG_SIZES" ]]; then
    step "contig size by occupancy category" python3 "$SCRIPTS/plot_occupancy_contigs.py" "${GFF_ARGS[@]}" \
        --contig-sizes "$CONTIG_SIZES" --style classes -o "$OUT_DIR/${LABEL}_contig_classes"
else
    echo; echo "WARNING: $CONTIG_SIZES not found; the contig size plot is skipped (--contig-sizes FILE)" >&2
    FAILED+=("contig size by occupancy category (no $CONTIG_SIZES)")
fi

step "mostly invalid ORFs, percentage" python3 "$SCRIPTS/plot_occupancy_invalid.py" "${GFF_ARGS[@]}" --style percent \
    -o "$OUT_DIR/${LABEL}_occupancy_invalid_percent"
step "mostly invalid ORFs, count" python3 "$SCRIPTS/plot_occupancy_invalid.py" "${GFF_ARGS[@]}" --style invalid \
    -o "$OUT_DIR/${LABEL}_occupancy_invalid_only"
step "invalid ORFs, share of invalid genes by category" python3 "$SCRIPTS/plot_occupancy_invalid.py" "${GFF_ARGS[@]}" --style share \
    -o "$OUT_DIR/${LABEL}_invalid_share"

if [[ "$OVERLAP" == "yes" ]]; then
    step "mostly unsupported overlapping genes, percentage" python3 "$SCRIPTS/plot_occupancy_invalid.py" --mark overlap \
        "${GFF_ARGS[@]}" --style percent -o "$OUT_DIR/${LABEL}_occupancy_unsupported_percent"
    step "mostly unsupported overlapping genes, count" python3 "$SCRIPTS/plot_occupancy_invalid.py" --mark overlap \
        "${GFF_ARGS[@]}" --style invalid -o "$OUT_DIR/${LABEL}_occupancy_unsupported_only"
    step "unsupported overlapping genes, share of unsupported genes by category" python3 "$SCRIPTS/plot_occupancy_invalid.py" --mark overlap \
        "${GFF_ARGS[@]}" --style share -o "$OUT_DIR/${LABEL}_unsupported_share"
fi

echo
if [[ ${#FAILED[@]} -gt 0 ]]; then
    echo "Finished with ${#FAILED[@]} failed step(s):" >&2
    printf '  - %s\n' "${FAILED[@]}" >&2
    exit 1
fi
echo "All plots completed. Outputs are in $OUT_DIR"
