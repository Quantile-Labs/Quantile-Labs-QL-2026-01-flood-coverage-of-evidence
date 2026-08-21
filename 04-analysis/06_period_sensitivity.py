"""What the frozen period costs: *evidenced* recomputed on the 1980 path. PROTOCOL §11a.

    python3 04-analysis/06_period_sensitivity.py --unblind --rerun-reason "..."

NOT PRE-REGISTERED. Specified 2026-08-21, after the values were read, in response to the second
external reviewer. The frozen definition is unchanged and still governs the headline.

WHAT IS BEING TESTED, AND WHY IT IS THE PROTOCOL BEING TESTED RATHER THAN THE DATA.

§5 fixes *evidenced* as at least one non-null value under
`metrics/return_period_metrics/google/2014/dual_lstm/full_run/`, and says of that choice that it
is "the most generous defensible reading" and that where a design choice could bias toward or
against the subject this study takes the option that flatters the subject.

The release also publishes the same tables under `google/1980/dual_lstm/full_run/`. It carries
values for roughly twice as many African gauges. So the frozen definition is not the most
generous available, and the sentence claiming it is was written on 2026-08-04 about the
experiment axis, `full_run` against `kfold_splits`, and never revisited on the period axis. The
same day's amendment took 1980 seriously for Q4 skill and stopped there.

This script therefore reports P_unevidenced three ways: on the frozen 2014 path, on the 1980
path, and on the union, where a gauge counts as evidenced if either path carries a value. The
union is the truly most generous reading. Nothing here replaces the frozen figure. It measures
what the frozen figure cost, which is a number the Note owes its readers whichever way it falls.

THIS READS METRIC VALUES, SO IT IS A SECOND AUTHORISED RUN and it is disclosed as one: it takes
--rerun-reason, appends to UNBLINDED.json, and the Note says a second read happened and why.
"""
import argparse
import json
import sys
from pathlib import Path

import pandas as pd

STUDY = Path(__file__).resolve().parent.parent
LIB = STUDY / "_lib"
RESULTS = STUDY / "05-results"
STRATA = STUDY / "02-data" / "interim" / "strata"

sys.path.insert(0, str(LIB))
sys.path.insert(0, str(STUDY / "04-analysis"))
from stats import fmt                                       # noqa: E402
import importlib                                            # noqa: E402
_mio = importlib.import_module("_metrics_io")
_ev = importlib.import_module("01_evidence")

PATHS = {
    "frozen_2014": "metrics/return_period_metrics/google/2014/dual_lstm/full_run/",
    "alt_1980":    "metrics/return_period_metrics/google/1980/dual_lstm/full_run/",
}


def evidence_sets(prefix):
    """{gauge_id: classification} using the frozen classifier, on an arbitrary path.

    `01_evidence.classify` is imported rather than reimplemented. A second copy of the rule
    that defines this study's primary outcome, written to answer a question about that rule,
    is how you end up measuring the difference between two implementations instead of the
    difference between two paths.
    """
    by_gauge = _mio.load("unblind", prefix=prefix)
    return {g: _ev.classify(recs) for g, recs in by_gauge.items()}


def p_unevidenced(pts, basins, evidenced_ids):
    """The primary metric, computed exactly as 02_primary.py computes it, on a given set."""
    pop = dict(zip(basins["HYBAS_ID"], pd.to_numeric(basins["pop_worldpop"], errors="coerce")))
    seeded = pts.dropna(subset=["hid"]).copy()
    seeded["hid"] = seeded["hid"].astype("int64")
    seeded["ev"] = seeded["unique_gauge_id"].astype(str).str.replace("GRDC_", "", regex=False)
    seeded["is_ev"] = seeded["ev"].isin(evidenced_ids)
    g = seeded.groupby("hid").agg(any_pts=("unique_gauge_id", "size"), ev=("is_ev", "sum"))
    num = den = 0.0
    n_num = n_den = 0
    for hid, row in g.iterrows():
        v = pop.get(hid)
        if v is None or v != v:
            continue
        den += v; n_den += 1
        if row["ev"] == 0:
            num += v; n_num += 1
    return {"share": num / den if den else float("nan"), "numerator_pop": num,
            "denominator_pop": den, "basins_numerator": n_num, "basins_denominator": n_den}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--unblind", action="store_true", required=True)
    ap.add_argument("--rerun-reason", required=True,
                    help="the marker already exists, so this read must say why it is happening")
    a = ap.parse_args()

    print("=" * 78)
    print("QL-2026-01  stage 6, period sensitivity   PROTOCOL 11a, not pre-registered")
    print("SECOND AUTHORISED READ. Reason:", a.rerun_reason)
    print("=" * 78)

    sets = {name: evidence_sets(prefix) for name, prefix in PATHS.items()}
    pts = pd.read_csv(RESULTS / "points_evidence.csv")
    pts["hid"] = pd.to_numeric(pts["HYBAS_ID"], errors="coerce")
    basins = pd.read_parquet(STRATA / "basins_af.parquet")

    african = set(pts.loc[~pts["is_hybas_entry"], "unique_gauge_id"]
                  .astype(str).str.replace("GRDC_", "", regex=False))

    out = {"protocol_section": "11a", "pre_registered": False,
           "rerun_reason": a.rerun_reason, "paths": PATHS, "counts": {}, "primary": {}}

    ids = {}
    for name, cls in sets.items():
        ev = {g for g, c in cls.items() if c["generous"]}
        ids[name] = ev
        af_file = african & set(cls)
        af_ev = african & ev
        out["counts"][name] = {"gauges_with_file": len(cls), "evidenced_global": len(ev),
                               "african_with_file": len(af_file), "african_evidenced": len(af_ev)}
        print(f"\n{name}")
        print(f"  gauges with a file, global : {len(cls):,}")
        print(f"  evidenced, global          : {fmt(len(ev), len(cls))}")
        print(f"  African gauges with a file : {len(af_file):,}")
        print(f"  African evidenced          : {fmt(len(af_ev), len(af_file))}")

    ids["union"] = ids["frozen_2014"] | ids["alt_1980"]
    af_union = african & ids["union"]
    out["counts"]["union"] = {"evidenced_global": len(ids["union"]),
                              "african_evidenced": len(af_union)}
    print(f"\nunion of both paths")
    print(f"  African evidenced          : {len(af_union):,}")

    print(f"\n{'definition':<14}{'P_unevidenced':>15}{'shift from frozen':>20}")
    frozen = None
    for name in ("frozen_2014", "alt_1980", "union"):
        r = p_unevidenced(pts, basins, ids[name])
        out["primary"][name] = r
        if frozen is None:
            frozen = r["share"]
        shift = (r["share"] - frozen) * 100
        out["primary"][name]["shift_pp_from_frozen"] = shift
        print(f"{name:<14}{r['share']*100:14.2f}%{shift:19.2f}")

    gate_d = abs(min(v["share"] for v in out["primary"].values())
                 - max(v["share"] for v in out["primary"].values())) * 100
    out["spread_pp"] = gate_d
    out["gate_d_abandonment_threshold_pp"] = 10.0
    out["exceeds_gate_d_threshold"] = gate_d > 10.0
    print(f"\nspread across the three definitions: {gate_d:.2f} pp "
          f"(Gate D abandonment threshold 10 pp)")

    (RESULTS / "period_sensitivity.json").write_text(json.dumps(out, indent=2) + "\n")
    _mio.record_unblinding(reason=a.rerun_reason)
    print(f"\nwrote {(RESULTS / 'period_sensitivity.json').relative_to(STUDY)}")


if __name__ == "__main__":
    main()
