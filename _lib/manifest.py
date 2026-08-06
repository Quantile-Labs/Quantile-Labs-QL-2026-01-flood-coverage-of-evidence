"""Data provenance. Every file entering 02-data/raw/ gets a row, on arrival.

    python3 _lib/manifest.py QL-2026-01 02-data/raw/metrics.tgz \
        --url https://zenodo.org/records/10397664 --licence "CC BY 4.0"
    python3 _lib/manifest.py QL-2026-01 --verify
"""
import argparse
import csv
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
def resolve(study):
    """Accept a short id (QL-2026-01) or the full folder name.

    Two layouts are supported. In the internal monorepo, `_lib/` sits beside the study
    folders and ROOT holds them all. In a published single-study repo, `_lib/` is vendored
    inside the study and ROOT *is* the study — detected by `00-protocol/` being present.
    The published repo has to run from a plain clone, with no sibling directories to find.
    """
    if (ROOT / "00-protocol").is_dir():
        if ROOT.name == study or ROOT.name.startswith(study):
            return ROOT
        raise SystemExit(f"{study!r} does not match the study in this repo ({ROOT.name})")
    d = ROOT / study
    if d.is_dir():
        return d
    hits = sorted(p for p in ROOT.glob(f"{study}*") if p.is_dir())
    if len(hits) == 1:
        return hits[0]
    if not hits:
        raise SystemExit(f"no study folder matching {study!r} under {ROOT}")
    raise SystemExit(f"{study!r} is ambiguous: {[h.name for h in hits]}")


COLS = ["acquired_utc", "source_url", "local_path", "sha256", "bytes", "licence", "notes",
        "transient"]

# `transient` — recorded, hashed, then deliberately deleted.
#
# Some inputs are too large to keep. QL-2026-01 streams ~16 GB of population rasters and OSM
# extracts through a machine with 6 GB free: each file is downloaded, hashed into this
# manifest, used, and removed. The provenance outlives the bytes, and anyone can re-fetch
# from source_url and check the hash.
#
# Without this flag `--verify` reports every streamed file as MISSING and exits non-zero on
# every run, which teaches the operator to ignore a check whose entire value is that it fails
# loudly. A provenance tool nobody reads is worse than none. So: transient files absent from
# disk are reported and pass; transient files PRESENT are still hash-checked; non-transient
# files absent are failures, exactly as before.


def _migrate(mp):
    """Add the `transient` column to a manifest written before it existed.

    Rewrites the header only. Existing values are copied through unchanged — this is a
    schema migration, not an edit to the record, and the append-only rule is about the
    content of rows rather than the shape of the table.
    """
    if not mp.exists() or mp.stat().st_size == 0:
        return
    with open(mp, newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows or "transient" in rows[0]:
        return
    for r in rows:
        r["transient"] = ""
    with open(mp, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    print(f"migrated {mp.name}: added `transient` column to {len(rows)} existing rows")


def sha256(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while block := fh.read(chunk):
            h.update(block)
    return h.hexdigest()


def manifest_path(study):
    return resolve(study) / "02-data" / "manifests" / "MANIFEST.csv"


def add(study, target, url, licence, notes, transient=False):
    mp = manifest_path(study)
    mp.parent.mkdir(parents=True, exist_ok=True)
    _migrate(mp)
    new = not mp.exists() or mp.stat().st_size == 0
    p = Path(target).resolve()
    row = {
        "acquired_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_url": url,
        "local_path": str(p.relative_to(resolve(study))) if str(p).startswith(str(resolve(study))) else str(p),
        "sha256": sha256(p),
        "bytes": p.stat().st_size,
        "licence": licence,
        "notes": notes,
        "transient": "yes" if transient else "",
    }
    with open(mp, "a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        if new:
            w.writeheader()
        w.writerow(row)
    print(f"recorded {row['local_path']}  sha256 {row['sha256'][:12]}...  {row['bytes']:,} bytes")


def verify(study):
    mp = manifest_path(study)
    if not mp.exists():
        sys.exit(f"no manifest at {mp}")
    bad = missing = ok = gone = 0
    with open(mp) as fh:
        for row in csv.DictReader(fh):
            f = resolve(study) / row["local_path"]
            is_transient = (row.get("transient") or "").strip().lower() in ("yes", "true", "1")
            if not f.exists():
                if is_transient:
                    # Deleted by design. Re-fetchable from source_url and checkable against
                    # the recorded hash, so provenance is intact.
                    gone += 1
                else:
                    print(f"MISSING  {row['local_path']}")
                    missing += 1
            elif sha256(f) != row["sha256"]:
                print(f"MISMATCH {row['local_path']}")
                bad += 1
            else:
                ok += 1
    print(f"\n{ok} ok, {bad} mismatched, {missing} missing, {gone} transient (deleted by design)")
    # A silent upstream revision looks exactly like a corrupted download. Fail loudly.
    # Transient absences are not failures; a transient file still on disk is hash-checked
    # like any other, so this cannot be used to wave through a corrupted file.
    sys.exit(1 if (bad or missing) else 0)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("study")
    ap.add_argument("file", nargs="?")
    ap.add_argument("--url", default="")
    ap.add_argument("--licence", default="")
    ap.add_argument("--notes", default="")
    ap.add_argument("--transient", action="store_true",
                    help="file will be deleted after use; hash is kept, absence is not a failure")
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()
    verify(a.study) if a.verify else add(a.study, a.file, a.url, a.licence, a.notes, a.transient)
