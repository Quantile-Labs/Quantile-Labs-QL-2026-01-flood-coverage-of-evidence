"""Q4, the population-weighted skill distribution, and the sensitivities §5 pre-registered.

    python3 04-analysis/03_q4_skill.py --permute 20260806
    python3 04-analysis/03_q4_skill.py --unblind

This is the last stage of the analysis, and it exists so that the single authorised run
computes the whole pre-registered study rather than the half of it that was easy. §5 secondary
metric 2 asks how published skill distributes across evidenced African gauges when each is
weighted by the population of its basin, against the unweighted per-gauge distribution, which
is how the paper counts. A gauge protecting two million people and one protecting two thousand
count equally in a per-gauge distribution, and whether that matters is the question.

WHAT IS REPORTED, AND WHY NONE OF IT IS DESIGNATED THE HEADLINE HERE.

**Three experiments, decided 2026-08-04 before any value was read.** `kfold_splits` is what the
paper calls the AI model and is the anchor for comparison with Figure 4. `continent_splits`
holds Africa out entirely and is the cut that speaks to ungauged performance, which is what the
product does. `full_run` is the frozen presence test and is the most optimistic, because it is
the gauged run. Reporting only `full_run` would describe the model where it was trained while
the subject of this Note is forecast points where it was not.

**Two dataset years.** 2014 governs as frozen. 1980 runs alongside because the paper's Figure 4
reads 1980, so it is the only comparable one (verification 2026-08-07).

**Degenerate values are counted, not silently averaged.** The released code's
`_true_positives_fraction_in_window()` returns 1 when there are no observed *and* no predicted
events, so a gauge can score perfectly because nothing ever happened there. Precision and recall
of exactly 1.0 together are therefore flagged, counted per return period, and Q4 is reported
both including and excluding them, with neither designated the headline. This bites hardest at
the rarest return periods, which is where the study is most likely to be quoted.

**Tolerance windows 0 and 1 are a sensitivity, never a choice.** Window 2 is the metric of
record because the paper uses it (Gate B). The other two are printed beside it so that nobody,
including us, can select one afterwards.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

STUDY = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(STUDY / "_lib"))

from _metrics_io import load                                   # noqa: E402

STRATA = STUDY / "02-data" / "interim" / "strata"
RESULTS = STUDY / "05-results"

EXPERIMENTS = ["kfold_splits", "continent_splits", "full_run"]
YEARS = ["2014", "1980"]
RETURN_PERIODS = ["1.01", "2.0", "5.0", "10.0", "20.0", "50.0"]
WINDOW_OF_RECORD = "2.0"
LEADS = [0, 7]                                                  # stratum 7
PREFIX = "metrics/return_period_metrics/google/{year}/dual_lstm/{exp}/"


def parse_table(text):
    out = {}
    for r in (row.split(",") for row in text.strip().split("\n")[1:]):
        if len(r) < 3:
            continue
        vals = []
        for cell in r[2:]:
            try:
                v = float(cell)
                vals.append(v if v == v else None)
            except ValueError:
                vals.append(None)
        out[(r[0], r[1])] = vals
    return out


def f1_at(recs, rp, window, lead):
    """Derived F1, plus two degeneracy flags. None where either input is null.

    TWO FLAGS, AND NEITHER IS DESIGNATED THE TRUTH. Corrected 2026-08-21 under PROTOCOL §11a
    after external review. This returned a single flag set only where precision *and* recall
    were both exactly 1.0. The released code's degenerate return is per quantity: it yields 1
    where there are no observed and no predicted events, and 1 again where no observed data
    surrounds any predicted event. So a gauge can be degenerate in one quantity and genuine in
    the other, and the old flag missed every such case. A published 1.0 cannot be told apart
    from a genuine 1.0 by its value, so the honest response is not to pick a better single rule
    but to report the strict reading, both equal to 1.0, and the broad reading, either equal to
    1.0, side by side and let a reader take the one they can defend.
    """
    if "precision" not in recs or "recall" not in recs:
        return None, (False, False)
    got = {}
    for m in ("precision", "recall"):
        cell = parse_table(recs[m]).get((rp, window))
        if cell is None or lead >= len(cell) or cell[lead] is None:
            return None, (False, False)
        got[m] = cell[lead]
    p, r = got["precision"], got["recall"]
    flags = (p == 1.0 and r == 1.0, p == 1.0 or r == 1.0)
    return (0.0 if (p + r) == 0 else 2 * p * r / (p + r)), flags


def weighted_median(values, weights):
    if len(values) == 0:
        return float("nan")
    order = np.argsort(values)
    v, w = np.asarray(values)[order], np.asarray(weights)[order]
    c = np.cumsum(w)
    if c[-1] == 0:
        return float("nan")
    return float(v[np.searchsorted(c, c[-1] / 2.0)])


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--permute", type=int, metavar="SEED")
    g.add_argument("--unblind", action="store_true")
    a = ap.parse_args()
    mode = "unblind" if a.unblind else "permute"
    tag = "" if a.unblind else f".permuted-{a.permute}"

    print("=" * 78)
    print(f"QL-2026-01  stage 3, Q4 population-weighted skill   mode={mode}"
          + ("" if a.unblind else f" seed={a.permute}"))
    if not a.unblind:
        print("PERMUTED. Distributions below are a machinery test, not a finding.")
    print("=" * 78)

    # African gauges and the population of the basin each sits in.
    pts = pd.read_csv(STRATA / "points_assigned.csv")
    basins = pd.read_parquet(STRATA / "basins_af.parquet")[["HYBAS_ID", "pop_worldpop"]]
    pts["hybas_int"] = pd.to_numeric(pts["HYBAS_ID"], errors="coerce").astype("Int64")
    pts = pts.merge(basins, left_on="hybas_int", right_on="HYBAS_ID", how="left",
                    suffixes=("", "_b"))
    pop = dict(zip(pts["unique_gauge_id"], pts["pop_worldpop"]))
    african = set(pts.loc[~pts["is_hybas_entry"], "unique_gauge_id"])
    print(f"\nAfrican real gauges in the inventory: {len(african):,}")

    out = {"mode": mode, "seed": None if a.unblind else a.permute, "results": {}}
    for year in YEARS:
        for exp in EXPERIMENTS:
            try:
                recs = load(mode, seed=None if a.unblind else a.permute,
                            prefix=PREFIX.format(year=year, exp=exp))
            except Exception as e:                       # experiment absent for this year
                print(f"\n{year}/{exp}: unavailable ({e})")
                continue
            recs = {f"GRDC_{k}": v for k, v in recs.items()}
            rows = []
            for gid in african & set(recs):
                w = pop.get(gid)
                if w is None or not np.isfinite(w):
                    continue                              # basin with no population value
                for rp in RETURN_PERIODS:
                    f1, deg = f1_at(recs[gid], rp, WINDOW_OF_RECORD, 0)
                    if f1 is None:
                        continue
                    rows.append({"gauge": gid, "rp": rp, "f1": f1,
                                 "degenerate": deg[0], "degenerate_broad": deg[1],
                                 "pop": float(w)})
            if not rows:
                print(f"\n{year}/{exp}: no evidenced African gauges")
                continue
            df = pd.DataFrame(rows)
            key = f"{year}/{exp}"
            out["results"][key] = {}
            print(f"\n{key}   evidenced African gauges with a derived F1: "
                  f"{df.gauge.nunique():,}   window {WINDOW_OF_RECORD}, lead 0")
            print(f"  {'return period':<15}{'n':>6}{'degen':>7}"
                  f"{'unweighted':>12}{'pop-weighted':>14}{'excl degen':>12}")
            for rp in RETURN_PERIODS:
                s = df[df.rp == rp]
                if s.empty:
                    continue
                nd = s[~s.degenerate]
                nb = s[~s.degenerate_broad]
                rec = {
                    "n": int(len(s)), "degenerate": int(s.degenerate.sum()),
                    "degenerate_broad": int(s.degenerate_broad.sum()),
                    "unweighted_mean_excl_degenerate_broad":
                        float(nb.f1.mean()) if len(nb) else float("nan"),
                    "pop_weighted_mean_excl_degenerate_broad":
                        float((nb.f1 * nb["pop"]).sum() / nb["pop"].sum())
                        if len(nb) and nb["pop"].sum() else float("nan"),
                    "unweighted_mean": float(s.f1.mean()),
                    "pop_weighted_mean": float(np.average(s.f1, weights=s["pop"]))
                        if s["pop"].sum() else float("nan"),
                    "pop_weighted_median": weighted_median(s.f1.values, s["pop"].values),
                    "unweighted_mean_excl_degenerate":
                        float(nd.f1.mean()) if len(nd) else float("nan"),
                    "pop_weighted_mean_excl_degenerate":
                        float(np.average(nd.f1, weights=nd["pop"]))
                        if len(nd) and nd["pop"].sum() else float("nan")}
                out["results"][key][rp] = rec
                print(f"  {rp:<15}{rec['n']:>6}{rec['degenerate']:>7}"
                      f"{rec['unweighted_mean']:>12.4f}{rec['pop_weighted_mean']:>14.4f}"
                      f"{rec['unweighted_mean_excl_degenerate']:>12.4f}")

    # Tolerance-window sensitivity on the frozen experiment only, so the table stays readable.
    print(f"\nTolerance-window sensitivity, 2014/full_run, return period 2.0, lead 0")
    recs = load(mode, seed=None if a.unblind else a.permute,
                prefix=PREFIX.format(year="2014", exp="full_run"))
    recs = {f"GRDC_{k}": v for k, v in recs.items()}
    sens = {}
    for win in ["0.0", "1.0", "2.0"]:
        vals, wts = [], []
        for gid in african & set(recs):
            w = pop.get(gid)
            if w is None or not np.isfinite(w):
                continue
            f1, _ = f1_at(recs[gid], "2.0", win, 0)
            if f1 is not None:
                vals.append(f1); wts.append(float(w))
        if vals:
            sens[win] = {"n": len(vals), "unweighted_mean": float(np.mean(vals)),
                         "pop_weighted_mean": float(np.average(vals, weights=wts))}
            mark = "  <- metric of record" if win == WINDOW_OF_RECORD else ""
            print(f"  window {win:<5} n={len(vals):<5} unweighted {np.mean(vals):.4f}"
                  f"   pop-weighted {np.average(vals, weights=wts):.4f}{mark}")
    out["window_sensitivity_2014_full_run_rp2_lead0"] = sens

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / f"q4_skill{tag}.json").write_text(json.dumps(out, indent=2) + "\n")
    print(f"\nwrote {RESULTS.name}/q4_skill{tag}.json")
    if not a.unblind:
        print("Still blind. No experiment is designated the headline; all are reported.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
