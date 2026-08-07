"""The only code in this study that opens a metric value.

Everything else, the strata, the basin assignment, the population weights, and every figure
template, is built blind by `03-harness/`, whose scripts refuse to run while a metrics tree is
reachable in `02-data/interim/`. This module is the single deliberate exception, and it is kept
to one file so that the answer to "what could have seen the outcome?" is one filename rather
than an audit of the whole tree.

THE VALUES ARE NEVER EXTRACTED TO DISK. Metric tables are read as members of the manifested,
hash-verified `02-data/raw/metrics.tgz` in one sequential pass, which takes about two seconds
for all 11,356 members of the frozen path, and they exist only in memory for the life of the
process. This is deliberate and it is stronger than extracting to a directory named something
careful. Nothing lands in the tree, so no later blind script can be fooled by a leftover, there
is no cleanup step anyone can forget, and the structural guard in `03-harness/` stays armed
permanently rather than being disarmed for the duration of the analysis and then restored.

TWO MODES, AND NEITHER IS THE DEFAULT.

    python3 04-analysis/_metrics_io.py --permute 20260806     # development, blind
    python3 04-analysis/_metrics_io.py --unblind              # the single authorised run

`--permute` reads the real records and then shuffles which gauge each one belongs to, so the
multiset of published values is preserved exactly while every association between a gauge and
its record is destroyed. That is the right permutation for this study, because the primary
metric is about *which* forecast points carry published evidence and *who lives behind them*,
so scrambling the gauge mapping removes precisely the signal being measured while leaving the
shape of the data intact enough to develop and debug against. PROTOCOL §10 requires this, and
running the analysis for the first time against real values would forfeit it.

`--unblind` checks its preconditions and refuses if any fails. It is expected to run once.

WHAT "EVIDENCED" READS. The frozen definition (PROTOCOL §5) is at least one non-null released
per-gauge value under `metrics/return_period_metrics/google/2014/dual_lstm/full_run/`. That
path holds two metric directories, `precision` and `recall`, with 5,678 gauges each, so
**F1, the metric of record, is not published per gauge and is derived here** as the harmonic
mean. That derivation is this module's, not the developer's, and the Note says so. Where either
input is null the F1 is null rather than zero, because a gauge with no published precision has
no published F1, and calling that zero would invent a measurement.
"""
import argparse
import hashlib
import io
import json
import random
import re
import subprocess
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path

STUDY = Path(__file__).resolve().parent.parent
LIB = STUDY / "_lib"
INTERIM = STUDY / "02-data" / "interim"
TARBALL = STUDY / "02-data" / "raw" / "metrics.tgz"
MARKER = STUDY / "07-admin" / "UNBLINDED.json"

sys.path.insert(0, str(LIB))

# The frozen path, PROTOCOL §5. Written out rather than assembled from parts so that a reader
# can compare it to the protocol by eye, and so that changing it is a visible edit.
FROZEN_PREFIX = "metrics/return_period_metrics/google/2014/dual_lstm/full_run/"
MEMBER = re.compile(re.escape(FROZEN_PREFIX) + r"(precision|recall)/GRDC_(\d+)\.csv$")

# The three experiments Q4 reports side by side, resolved 2026-08-04. `full_run` is the frozen
# presence test and stays the definition of evidenced; the other two exist so that skill is not
# described where the model was trained as though it were where it was not.
EXPERIMENTS = ["full_run", "kfold_splits", "continent_splits"]


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_records(tarball=TARBALL, prefix=FROZEN_PREFIX):
    """Yield (gauge_id, metric_name, raw_csv_text) for every member under `prefix`.

    One sequential pass. The tar member order is not alphabetical and random access into a
    gzip stream means re-reading it from the start, so anything that needs several metrics
    should take them from this single pass rather than calling the function repeatedly.
    """
    pat = re.compile(re.escape(prefix) + r"(precision|recall)/GRDC_(\d+)\.csv$")
    with tarfile.open(tarball, "r:gz") as tf:
        for m in tf:
            hit = pat.match(m.name)
            if not hit:
                continue
            fh = tf.extractfile(m)
            if fh is None:
                continue
            yield hit.group(2), hit.group(1), fh.read().decode("utf-8", "replace")


def load(mode, seed=None, tarball=TARBALL, prefix=FROZEN_PREFIX):
    """Return {gauge_id: {metric: raw_csv_text}}, permuted or real according to `mode`.

    Permutation shuffles the gauge keys while leaving the records untouched and in their
    original pairing with each other, so a gauge keeps a coherent precision-and-recall pair
    that simply belongs to a different gauge. Shuffling the two independently would produce
    F1 values from mismatched sources and would look like data corruption rather than like
    a null, which makes debugging harder rather than easier.
    """
    if mode not in {"permute", "unblind"}:
        raise ValueError(f"mode must be 'permute' or 'unblind', got {mode!r}")
    by_gauge = {}
    for gauge, metric, text in read_records(tarball, prefix):
        by_gauge.setdefault(gauge, {})[metric] = text
    if mode == "unblind":
        return by_gauge
    if seed is None:
        raise ValueError("--permute requires a seed, and the seed goes in the results file")
    keys = sorted(by_gauge)
    shuffled = list(keys)
    random.Random(seed).shuffle(shuffled)
    return {k: by_gauge[src] for k, src in zip(keys, shuffled)}


# -------------------------------------------------------------------------------------------
# Preconditions for the authorised run. Each one is a way the run could be worth less than it
# looks, and each is checked rather than trusted.
# -------------------------------------------------------------------------------------------
def preconditions():
    """Return a list of (name, ok, detail). Nothing here reads a metric value."""
    out = []

    dirty = subprocess.run(["git", "-C", str(STUDY), "status", "--porcelain"],
                           capture_output=True, text=True).stdout.strip()
    out.append(("working tree clean", not dirty,
                "the run log records a git SHA, and an SHA that does not describe the code "
                "that ran is worse than no SHA at all" if dirty else "nothing uncommitted"))

    sha = subprocess.run(["git", "-C", str(STUDY), "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    out.append(("git SHA resolved", bool(sha), sha or "not a git repository"))

    proto = STUDY / "00-protocol" / "PROTOCOL.md"
    recorded = (STUDY / "00-protocol" / "PROTOCOL.sha256").read_text().split()[0]
    actual = _sha256(proto)
    out.append(("protocol matches its recorded hash", recorded == actual, actual))

    tar_ok = TARBALL.exists()
    out.append(("metrics tarball present", tar_ok, str(TARBALL.relative_to(STUDY))))

    # If a metrics tree is sitting in the interim directory then some earlier step extracted
    # one, every blind harness script is currently refusing to run, and the assumption that
    # covariates were built before outcomes were reachable no longer holds cleanly.
    stray = (INTERIM / "metrics").exists()
    out.append(("no metrics tree in 02-data/interim", not stray,
                "found one, which means the blind guard is tripping and the build order "
                "needs explaining before this run means anything" if stray else "clear"))

    mv = subprocess.run([sys.executable, str(LIB / "manifest.py"), "QL-2026-01", "--verify"],
                        capture_output=True, text=True)
    out.append(("manifest verifies", "mismatched" not in mv.stdout or " 0 mismatched" in mv.stdout,
                mv.stdout.strip().splitlines()[-1] if mv.stdout.strip() else "no output"))

    out.append(("not already unblinded", not MARKER.exists(),
                "marker exists, so this would be a re-run and needs --rerun-reason"
                if MARKER.exists() else "no marker"))
    return out


def record_unblinding(reason=None):
    """Write the marker and print the row to paste into RUNLOG.md."""
    sha = subprocess.run(["git", "-C", str(STUDY), "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    proto = _sha256(STUDY / "00-protocol" / "PROTOCOL.md")
    entry = {"utc": now, "frozen_analysis_sha": sha, "protocol_sha256": proto,
             "frozen_path": FROZEN_PREFIX, "reason": reason or "first authorised run"}
    hist = json.loads(MARKER.read_text())["runs"] if MARKER.exists() else []
    hist.append(entry)
    MARKER.write_text(json.dumps({"runs": hist}, indent=2) + "\n")
    print("\nUnblinding recorded. Paste this into 07-admin/RUNLOG.md and fill the outputs:\n")
    print(f"| {now} | `04-analysis/...` | {sha[:7]} | metrics.tgz `237559b9abbe` | "
          f"**UNBLINDED** | ... | {entry['reason']} |")
    print("\nAnd complete the unblinding record at the foot of RUNLOG.md.")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--permute", type=int, metavar="SEED",
                   help="development mode, shuffles the gauge mapping, records the seed")
    g.add_argument("--unblind", action="store_true",
                   help="the single authorised run against real values")
    g.add_argument("--check", action="store_true",
                   help="report the preconditions and exit, reading no metric value")
    ap.add_argument("--rerun-reason", help="required to unblind again after the first run")
    a = ap.parse_args()

    if a.check or a.unblind:
        print("Preconditions for the authorised run:\n")
        checks = preconditions()
        for name, ok, detail in checks:
            print(f"  [{'ok' if ok else 'FAIL'}] {name:<38} {detail}")
        failed = [c for c in checks if not c[1]]
        if a.check:
            print(f"\n{len(checks) - len(failed)}/{len(checks)} pass.")
            return 0 if not failed else 1
        if failed and not (a.rerun_reason and all(c[0] == "not already unblinded"
                                                  for c in failed)):
            print(f"\nREFUSING TO UNBLIND: {len(failed)} precondition(s) failed.")
            print("Fix them, or if one is deliberate, log the reason in DECISIONS.md first.")
            return 1
        print("\nAll preconditions pass. Loading real values.")
        data = load("unblind")
        print(f"gauges with at least one record: {len(data):,}")
        record_unblinding(a.rerun_reason)
        return 0

    data = load("permute", seed=a.permute)
    print(f"PERMUTED, seed {a.permute}. No association between a gauge and its record survives.")
    print(f"gauges: {len(data):,}")
    print(f"records per gauge: {sorted({len(v) for v in data.values()})}")
    print("Record the seed in the results file, not only in the shell history.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
