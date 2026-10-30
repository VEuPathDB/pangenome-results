#!/usr/bin/env python3
"""
One-off fix, Afum only.

RepeatMasker for Afum was run on the assemblies BEFORE the step-01 contig drop
(organelle + redundant contigs). The RepeatMasker output therefore still carries
hits on contigs that were removed afterwards. This rewrites the outputs so they
match the final dataset:

  - <name>.out / .ori.out : drop hit lines whose query contig (column 5) is gone
  - <name>.out.gff        : drop feature lines whose seqid (column 1) is gone
  - <name>.tbl            : correct the "total length:" line (the only field
                            summarize_te_content.py reads; other totals are left
                            as-is with a comment)

Two ways to say which contigs are gone:

  --drop-list FILE   the step-01 manifest, "<genome>  <contig>" per line
                     (01_Genome_Selection_QC/drop_contigs.txt). Removes exactly
                     those contigs. total length is corrected by subtracting the
                     removed contigs' length inferred from the .out.

  --genomes-dir DIR  the final assemblies. Removes any contig not a header in
                     genomes/<genome_id>; total length is set to the exact
                     assembly size. More accurate - use it if you have the
                     post-drop assemblies here.

Input folders: RM_<genome_id>/ (as left by run_repeatmasker.slurm.sh) or loose
<genome>.fna.out files, in --rm-indir or one level down. RepeatMasker scratch
dirs with no .out (RM_<pid>.<timestamp>/, trfResults-*) are ignored. Cleaned
output goes to --outdir as RM_<genome_id>/, originals untouched.

Normal pipeline order is drop-contigs (step 01) THEN RepeatMasker, so this is
not part of the general pipeline.

Usage:
    python3 fix_repeatmasker_after_contig_drop.py \
        --rm-indir . \
        --drop-list 01_Genome_Selection_QC/drop_contigs.txt \
        --outdir repeatmasker_contig_filtered
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

TBL_LENGTH_RE = re.compile(r"^(\s*total length:\s*)([\d,]+)(\s*bp.*)$", re.IGNORECASE)
ACC_RE = re.compile(r"GC[AF]_\d+\.\d+")
FASTA_EXTS = (".fna", ".fasta", ".fa")


def trim_accession(s: str) -> str:
    m = ACC_RE.search(s)
    return m.group(0) if m else s


def strip_ext(stem: str) -> str:
    for ext in FASTA_EXTS:
        if stem.endswith(ext):
            return stem[: -len(ext)]
    return stem


def out_stem(out_path: Path) -> str:
    n = out_path.name
    return n[: -len(".ori.out")] if n.endswith(".ori.out") else n[: -len(".out")]


def read_fasta_contigs(path: Path) -> dict:
    lengths: dict = {}
    cur = None
    with path.open() as fh:
        for line in fh:
            if line.startswith(">"):
                cur = line[1:].split()[0]
                lengths[cur] = 0
            elif cur is not None:
                lengths[cur] += len(line.strip())
    return lengths


def parse_drop_list(path: Path) -> dict:
    """{genome: set(contigs)} from a '<genome>  <contig>' manifest ('#' comments)."""
    out: dict = {}
    for raw in path.read_text().splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 2:
            print(f"WARNING: ignoring malformed drop-list line: {raw!r}", file=sys.stderr)
            continue
        out.setdefault(parts[0], set()).add(parts[1])
    return out


def load_genomes(genomes_dir: Path) -> dict:
    out: dict = {}
    files = []
    for ext in FASTA_EXTS:
        files += sorted(genomes_dir.glob(f"*{ext}"))
    for p in files:
        gid = trim_accession(strip_ext(p.name))
        lengths = read_fasta_contigs(p)
        out[gid] = {"contigs": set(lengths), "total_len": sum(lengths.values())}
    return out


def parse_out(out_path: Path):
    """Yield (contig, inferred_contig_len) per hit line (contig_len = end + left)."""
    for i, line in enumerate(out_path.read_text().splitlines()):
        if i < 3:
            continue
        f = line.split()
        if len(f) < 8:
            continue
        try:
            end = int(f[6])
            left = int(f[7].strip("()"))
        except ValueError:
            continue
        yield f[4], end + left


def contig_lengths_from_out(out_path: Path) -> dict:
    lengths: dict = {}
    for contig, ln in parse_out(out_path):
        if ln > lengths.get(contig, 0):
            lengths[contig] = ln
    return lengths


def find_out_files(rm_indir: Path):
    seen, result = set(), []
    for p in sorted(list(rm_indir.glob("*.out")) + list(rm_indir.glob("*/*.out"))):
        if p.name.endswith(".ori.out"):
            continue
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            result.append(p)
    return result


def genome_id_for(out_path: Path, stem: str):
    """Candidate genome ids for this run: from the .out name and the folder name."""
    cands = [strip_ext(stem), trim_accession(strip_ext(stem))]
    folder = out_path.parent.name
    for pref in ("RM_", "R_"):
        if folder.startswith(pref):
            folder = folder[len(pref):]
    cands += [folder, trim_accession(folder)]
    # de-dup, keep order
    seen, ordered = set(), []
    for c in cands:
        if c and c not in seen:
            seen.add(c)
            ordered.append(c)
    return ordered


def filter_lines(path: Path, drop: set, kind: str) -> tuple:
    removed, hit = 0, set()
    out = []
    for i, line in enumerate(path.read_text().splitlines(keepends=True)):
        if kind == "out":
            if i < 3:
                out.append(line)
                continue
            f = line.split()
            contig = f[4] if len(f) >= 5 else None
        else:
            if line.startswith("#") or not line.strip():
                out.append(line)
                continue
            contig = line.split("\t", 1)[0]
        if contig is not None and contig in drop:
            removed += 1
            hit.add(contig)
        else:
            out.append(line)
    path.write_text("".join(out))
    return removed, hit


def patch_tbl(path: Path, new_total) -> None:
    if new_total is None:
        return
    note = ("# NOTE: 'total length' patched by fix_repeatmasker_after_contig_drop.py "
            "(contigs removed after RepeatMasker ran); other totals below are stale.\n")
    out = [note]
    for line in path.read_text().splitlines(keepends=True):
        m = TBL_LENGTH_RE.match(line)
        if m:
            line = f"{m.group(1)}{int(new_total)}{m.group(3)}\n"
        out.append(line)
    path.write_text("".join(out))


def tbl_total(path: Path):
    for line in path.read_text().splitlines():
        m = TBL_LENGTH_RE.match(line)
        if m:
            return int(m.group(2).replace(",", ""))
    return None


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rm-indir", default=".",
                    help="folder with the RepeatMasker outputs (RM_*/ subdirs or loose *.out); default: .")
    ap.add_argument("--drop-list",
                    help="step-01 manifest: '<genome>  <contig>' per line (# comments ok)")
    ap.add_argument("--genomes-dir",
                    help="final assemblies <genome_id>.fna|.fasta|.fa; used instead of --drop-list")
    ap.add_argument("--outdir", required=True,
                    help="where the cleaned RM_<genome_id>/ folders go (new dir)")
    args = ap.parse_args()

    if not args.drop_list and not args.genomes_dir:
        ap.error("give --drop-list or --genomes-dir")

    rm_indir = Path(args.rm_indir)
    outdir = Path(args.outdir)

    dropmap = parse_drop_list(Path(args.drop_list)) if args.drop_list else None
    genomes = load_genomes(Path(args.genomes_dir)) if args.genomes_dir else None
    if args.genomes_dir and not genomes:
        sys.exit(f"ERROR: no *.fna / *.fasta / *.fa in {args.genomes_dir}/")

    out_files = find_out_files(rm_indir)
    if not out_files:
        listing = ", ".join(sorted(p.name for p in rm_indir.iterdir())[:25]) or "(empty)"
        sys.exit(f"ERROR: no RepeatMasker *.out files in {rm_indir}/ or its immediate "
                 f"subfolders.\n{rm_indir}/ contains: {listing}")

    outdir.mkdir(parents=True, exist_ok=True)
    grand_total = 0
    done: dict = {}

    for op in out_files:
        stem = out_stem(op)
        ids = genome_id_for(op, stem)

        # resolve to a canonical genome id + the drop set
        gid = None
        drop: set = set()
        how = ""
        if genomes is not None:
            match = next((c for c in ids if c in genomes), None)
            if match is None:
                # last resort: which assembly do the .out contigs belong to
                rc = set(contig_lengths_from_out(op))
                best, bf = None, 0.0
                for g, info in genomes.items():
                    fr = len(rc & info["contigs"]) / len(rc) if rc else 0
                    if fr > bf:
                        best, bf = g, fr
                match = best if bf >= 0.5 else None
                how = f"contig overlap {bf:.0%}" if match else ""
            else:
                how = "name"
            if match is None:
                sys.exit(f"ERROR: could not match {op} to an assembly in {args.genomes_dir}/ "
                         f"(tried {ids})")
            gid = match
            present = set(contig_lengths_from_out(op)) | set(genomes[gid]["contigs"])
            drop = {c for c in set(contig_lengths_from_out(op)) if c not in genomes[gid]["contigs"]}
        else:
            match = next((c for c in ids if c in dropmap), None)
            gid = match or ids[0]
            drop = dropmap.get(match, set()) if match else set()
            how = "drop-list" + ("" if match else " (no entry - nothing to drop)")

        if gid in done:
            print(f"WARNING: {op.name} and {done[gid]} both resolve to {gid}; later wins",
                  file=sys.stderr)
        done[gid] = op.name

        dest = outdir / f"RM_{gid}"
        if dest.exists():
            shutil.rmtree(dest)
        dest.mkdir(parents=True)
        for sib in sorted(op.parent.glob(f"{stem}*")):
            # skip .ori.out (pre-ProcessRepeats, overlapping hits) so downstream
            # steps that expect "exactly one .out" per folder are not confused
            if sib.is_file() and not sib.name.endswith(".ori.out"):
                shutil.copy2(sib, dest / sib.name)

        # work out the new total length before filtering the .out
        new_total = None
        if genomes is not None:
            new_total = genomes[gid]["total_len"]
        else:
            inferred = contig_lengths_from_out(op)
            old = None
            for t in sorted(dest.glob("*.tbl")):
                old = tbl_total(t)
                if old is not None:
                    break
            removed_bp = sum(inferred.get(c, 0) for c in drop)
            if old is not None:
                new_total = old - removed_bp
            elif inferred:
                new_total = sum(v for c, v in inferred.items() if c not in drop)

        removed_lines, hit = 0, set()
        for f in sorted(dest.glob("*.out")):
            n, h = filter_lines(f, drop, "out")
            removed_lines += n
            hit |= h
        for f in sorted(dest.glob("*.gff")) + sorted(dest.glob("*.gff3")):
            n, h = filter_lines(f, drop, "gff")
            removed_lines += n
            hit |= h
        for f in sorted(dest.glob("*.tbl")):
            patch_tbl(f, new_total)

        grand_total += removed_lines
        tag = f"{op.name}  ->  RM_{gid}/  ({how})"
        if drop:
            miss = drop - hit
            extra = f"; {sorted(miss)} not seen in the .out" if miss else ""
            print(f"{tag}: removed {removed_lines} line(s) for "
                  f"{', '.join(sorted(drop))}{extra}")
        else:
            print(f"{tag}: nothing to drop")

    print(f"\nDone. {len(out_files)} run(s) -> {outdir}/  ({grand_total} line(s) removed)")


if __name__ == "__main__":
    main()
