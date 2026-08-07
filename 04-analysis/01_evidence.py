"""Apply the frozen definition of *evidenced* and attach it to forecast points and basins.

This is stage one of the analysis and the only stage that interprets a metric table. It reads
through `04-analysis/_metrics_io.py`, so it inherits that module's two modes and never causes a
metric value to be written to disk in raw form.

    python3 04-analysis/01_evidence.py --permute 20260806     # development, blind
    python3 04-analysis/01_evidence.py --unblind              # the authorised run

THE DEFINITION IS FROZEN AND IS NOT RE-LITIGATED HERE (PROTOCOL §5). A forecast point is
evidenced if it has at least one non-null released per-gauge value under
`metrics/return_period_metrics/google/2014/dual_lstm/full_run/`. That is the most generous
defensible reading, chosen because where a design choice could bias toward or against the
subject this study takes the option that flatters the subject and says that it has. Two stricter
readings are pre-registered as sensitivities rather than as alternatives to choose between after
the fact: non-null at the 2-year return period, and non-null at the 5-year. All three are
computed here and all three are reported in the same table.

WHAT COUNTS AS NON-NULL. A cell is non-null if it parses as a finite float. Empty strings, `nan`
in any casing, and anything unparseable are null. **A null is never read as a zero**, here or
anywhere else in this study, because a gauge with no published value has not been shown to
perform badly, it has not been shown to perform at all, and collapsing that distinction is the
precise failure this Note exists to describe.

THE THIRD CATEGORY IS COUNTED SEPARATELY. A gauge whose metric files exist but contain no
non-null value anywhere is *file-present-but-all-null*, and §5 requires it be reported on its own
line rather than absorbed into either evidenced or unevidenced. That number is expected to be
substantial, since 2,300 of the 5,678 gauges carry byte-identical records (DECISIONS.md
2026-08-07), and pretending it is zero would flatter the evidence base.
"""
import argparse
import json
import sys
from pathlib import Path

import pandas as pd

STUDY = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(STUDY / "_lib"))

from _metrics_io import load, preconditions, record_unblinding   # noqa: E402

STRATA = STUDY / "02-data" / "interim" / "strata"
RESULTS = STUDY / "05-results"

# The metric of record, PROTOCOL §5 as amended by Gate B: return period 2.0, tolerance window
# 2 days, lead time 0. Windows 0 and 1 are a sensitivity, never a choice.
RP_OF_RECORD, WINDOW_OF_RECORD, LEAD_OF_RECORD = "2.0", "2.0", 0


def parse_table(text):
    """Return {(return_period, window): [8 lead values, None where null]}.

    Parsed by reading the two index columns rather than by row position. The row order is
    documented and stable, but a file whose order differed would silently produce numbers for
    the wrong return period, and that is not a failure anyone would notice in a chart.
    """
    out = {}
    rows = [r.split(",") for r in text.strip().split("\n")]
    for r in rows[1:]:
        if len(r) < 3:
            continue
        vals = []
        for cell in r[2:]:
            try:
                v = float(cell)
                vals.append(v if v == v else None)      # NaN is not equal to itself
            except ValueError:
                vals.append(None)
        out[(r[0], r[1])] = vals
    return out


def classify(records):
    """Evidence class for one gauge under all three pre-registered definitions."""
    any_nonnull = at_rp2 = at_rp5 = False
    for text in records.values():
        for (rp, _win), vals in parse_table(text).items():
            has = any(v is not None for v in vals)
            if not has:
                continue
            any_nonnull = True
            if rp == "2.0":
                at_rp2 = True
            elif rp == "5.0":
                at_rp5 = True
    return {"generous": any_nonnull, "rp2": at_rp2, "rp5": at_rp5,
            "file_present_all_null": not any_nonnull}


def metric_of_record(records):
    """Derived F1 at the metric of record, or None if either input is null.

    F1 is NOT published per gauge. The release carries precision and recall only, so this is
    our derivation and the Note attributes it to us (DECISIONS.md 2026-08-07). Null in either
    input gives null rather than zero, because a gauge with no published precision has no
    published F1 and calling that zero would invent a measurement.
    """
    got = {}
    for metric in ("precision", "recall"):
        if metric not in records:
            return None
        cell = parse_table(records[metric]).get((RP_OF_RECORD, WINDOW_OF_RECORD))
        if cell is None or LEAD_OF_RECORD >= len(cell) or cell[LEAD_OF_RECORD] is None:
            return None
        got[metric] = cell[LEAD_OF_RECORD]
    p, r = got["precision"], got["recall"]
    return 0.0 if (p + r) == 0 else 2 * p * r / (p + r)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--permute", type=int, metavar="SEED")
    g.add_argument("--unblind", action="store_true")
    ap.add_argument("--rerun-reason")
    a = ap.parse_args()

    mode = "unblind" if a.unblind else "permute"
    tag = "" if a.unblind else f".permuted-{a.permute}"
    if a.unblind:
        failed = [c for c in preconditions() if not c[1]]
        if failed and not a.rerun_reason:
            for name, _ok, detail in failed:
                print(f"  [FAIL] {name}: {detail}")
            sys.exit("REFUSING TO UNBLIND, see 04-analysis/_metrics_io.py --check")

    print("=" * 78)
    print(f"QL-2026-01  stage 1, evidence class   mode={mode}"
          + ("" if a.unblind else f" seed={a.permute}"))
    if not a.unblind:
        print("PERMUTED. Every gauge-to-record association is scrambled. These numbers are")
        print("a dry run of the machinery and are not findings about anything.")
    print("=" * 78)

    records = load(mode, seed=None if a.unblind else a.permute)
    rows = []
    for gauge, recs in records.items():
        cls = classify(recs)
        cls.update(unique_gauge_id=f"GRDC_{gauge}", f1_of_record=metric_of_record(recs))
        rows.append(cls)
    ev = pd.DataFrame(rows)
    print(f"\ngauges with a metric file        : {len(ev):,}")
    print(f"  evidenced, generous definition : {int(ev.generous.sum()):,}")
    print(f"  evidenced at return period 2   : {int(ev.rp2.sum()):,}")
    print(f"  evidenced at return period 5   : {int(ev.rp5.sum()):,}")
    print(f"  file present but all null      : {int(ev.file_present_all_null.sum()):,}")
    print(f"  with a derived F1 of record    : {int(ev.f1_of_record.notna().sum()):,}")

    # ---- join to the African forecast-point inventory ------------------------------------
    pts = pd.read_csv(STRATA / "points_assigned.csv")
    pts = pts.merge(ev, on="unique_gauge_id", how="left")
    for c in ("generous", "rp2", "rp5", "file_present_all_null"):
        pts[c] = pts[c].fillna(False)
    pts["has_metric_file"] = pts["unique_gauge_id"].isin(ev["unique_gauge_id"])

    real = pts[~pts["is_hybas_entry"]]
    print(f"\nAfrican forecast points          : {len(pts):,}")
    print(f"  real gauges                    : {len(real):,}")
    print(f"  undocumented hybas_ entries    : {int(pts['is_hybas_entry'].sum()):,}"
          f"   (no metric file by construction)")
    print(f"  real gauges with a metric file : {int(real['has_metric_file'].sum()):,}")
    print(f"  real gauges evidenced          : {int(real['generous'].sum()):,}")

    # ---- aggregate to basins --------------------------------------------------------------
    basins = pd.read_parquet(STRATA / "basins_af.parquet")
    assigned = pts[pts["assigned"]].copy()
    assigned["hybas_int"] = pd.to_numeric(assigned["HYBAS_ID"], errors="coerce").astype("Int64")
    agg = assigned.groupby("hybas_int").agg(
        evidenced_generous=("generous", "sum"),
        evidenced_rp2=("rp2", "sum"),
        evidenced_rp5=("rp5", "sum"),
        points_all_null=("file_present_all_null", "sum"),
        points_with_file=("has_metric_file", "sum"))
    basins = basins.merge(agg, left_on="HYBAS_ID", right_index=True, how="left")
    for c in agg.columns:
        basins[c] = basins[c].fillna(0).astype(int)

    with_pt = basins["points"] > 0
    print(f"\nbasins with >=1 forecast point   : {int(with_pt.sum()):,}")
    print(f"  and >=1 evidenced point        : "
          f"{int((with_pt & (basins.evidenced_generous > 0)).sum()):,}")
    print(f"  and NO evidenced point         : "
          f"{int((with_pt & (basins.evidenced_generous == 0)).sum()):,}")

    RESULTS.mkdir(exist_ok=True)
    basins.to_parquet(RESULTS / f"basins_evidence{tag}.parquet", index=False)
    pts.to_csv(RESULTS / f"points_evidence{tag}.csv", index=False)
    (RESULTS / f"evidence_summary{tag}.json").write_text(json.dumps({
        "mode": mode, "seed": None if a.unblind else a.permute,
        "gauges_with_file": int(len(ev)),
        "evidenced_generous": int(ev.generous.sum()),
        "evidenced_rp2": int(ev.rp2.sum()),
        "evidenced_rp5": int(ev.rp5.sum()),
        "file_present_all_null": int(ev.file_present_all_null.sum()),
        "african_points": int(len(pts)), "african_real_gauges": int(len(real)),
        "african_real_with_file": int(real["has_metric_file"].sum()),
        "african_real_evidenced": int(real["generous"].sum()),
        "basins_with_points": int(with_pt.sum()),
        "basins_with_points_none_evidenced":
            int((with_pt & (basins.evidenced_generous == 0)).sum()),
    }, indent=2) + "\n")
    print(f"\nwrote {RESULTS.name}/basins_evidence{tag}.parquet and two companions")

    if a.unblind:
        record_unblinding(a.rerun_reason)
    else:
        print("\nStill blind. Nothing here is a finding.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
