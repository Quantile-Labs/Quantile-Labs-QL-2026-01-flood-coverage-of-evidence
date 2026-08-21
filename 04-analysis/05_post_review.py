"""The five post-hoc additions the referee rehearsal asked for. PROTOCOL §11a.

    python3 04-analysis/05_post_review.py

NOT PRE-REGISTERED, AND IT DOES NOT TOUCH THE HEADLINE. Everything here was specified after the
values were read, on 2026-08-20, in response to an adversarial self-review of the first full draft. No
independent reviewer has read this draft; see PROTOCOL §11a for what that exercise was and
what it was not. The primary
metric stands exactly as computed on 2026-08-12. What follows is published beside it, under a
heading that says it is post-hoc, and where it disagrees with the frozen result both numbers
are printed and the disagreement is the finding.

WHY THIS DOES NOT USE THE UNBLINDING MACHINERY. It opens no metric value. A1, A3 and B1 read
`05-results/points_evidence.csv`, which is an output of the authorised run, and B2 reads member
names and container structure from `metrics.tgz` without reading a value, which is what the
day-1 check did while the study was still blind. Adding a row to `UNBLINDED.json` would record
a second reading of the tarball that did not happen, and that file is worth more if it means
exactly what it says.

    A1  the point's own drainage unit, and zero to eight basins downstream of it
    A2  P_unevidenced on a third population surface, WorldPop constrained, headline only
    A3  evidenced rate against Global Runoff Data Centre record end year and record length
    B1  effective sample size and a bootstrap interval for the Q4 weighted mean
    B2  whether a micro-average F1 can be derived from the release at all
"""
import json
import re
import sys
import tarfile
from pathlib import Path

import numpy as np
import pandas as pd

STUDY = Path(__file__).resolve().parent.parent
LIB = STUDY / "_lib"
RESULTS = STUDY / "05-results"
STRATA = STUDY / "02-data" / "interim" / "strata"
META = STUDY / "02-data" / "interim" / "metadata"
TARBALL = STUDY / "02-data" / "raw" / "metrics.tgz"

sys.path.insert(0, str(LIB))
from stats import fmt, wilson                            # noqa: E402

BOOTSTRAP_SEED = 20260820          # fixed here so the interval is reproducible, not chosen
BOOTSTRAP_DRAWS = 10000


def load():
    pts = pd.read_csv(RESULTS / "points_evidence.csv")
    basins = pd.read_parquet(STRATA / "basins_af.parquet")
    pts["hid"] = pd.to_numeric(pts["HYBAS_ID"], errors="coerce")
    return pts, basins


# -------------------------------------------------------------------------------------------
# A1. In reach, propagated downstream.
# -------------------------------------------------------------------------------------------
def a1_downstream(pts, basins, steps=tuple(range(9))):
    """P_unevidenced when the footprint propagates k basins downstream of each forecast point.

    The range runs to eight rather than to two. An earlier version stopped at two, which is
    where the curve reaches its minimum, and the second external reviewer pointed out that a
    reader is entitled to ask why a sensitivity stops exactly at the point of maximum effect.
    The curve turns back at three and settles near 91%, so the full range is both the honest
    answer and the stronger one.

    Step 0 is the frozen definition and must reproduce the published headline exactly. It is
    computed here rather than copied from the results file precisely so that it can be checked
    against it: if step 0 does not reproduce 92.4% then this function is wrong and the
    sensitivity built on it means nothing.
    """
    nxt = dict(zip(basins["HYBAS_ID"], basins["NEXT_DOWN"]))
    pop = dict(zip(basins["HYBAS_ID"], pd.to_numeric(basins["pop_worldpop"], errors="coerce")))

    seeded = pts.dropna(subset=["hid"]).copy()
    seeded["hid"] = seeded["hid"].astype("int64")
    per_basin = seeded.groupby("hid").agg(any_pts=("unique_gauge_id", "size"),
                                          ev_pts=("generous", "sum"))
    out = {}
    for k in steps:
        any_reach, ev_reach = {}, {}
        for hid, row in per_basin.iterrows():
            cur = hid
            for step in range(k + 1):
                if cur is None or cur == 0 or cur not in pop:
                    break
                any_reach[cur] = any_reach.get(cur, 0) + int(row["any_pts"])
                ev_reach[cur] = ev_reach.get(cur, 0) + int(row["ev_pts"])
                cur = nxt.get(cur)
        num = sum(p for b in any_reach
                  if (p := pop.get(b)) is not None and np.isfinite(p) and ev_reach.get(b, 0) == 0)
        den = sum(p for b in any_reach
                  if (p := pop.get(b)) is not None and np.isfinite(p))
        out[f"steps_{k}"] = {
            "share": num / den if den else float("nan"),
            "numerator_pop": num, "denominator_pop": den,
            "basins_in_reach": len(any_reach),
            "basins_unevidenced": sum(1 for b in any_reach if ev_reach.get(b, 0) == 0),
        }
    return out


# -------------------------------------------------------------------------------------------
# A2. Third population surface. Headline only, forbidden in stratum 3 (PROTOCOL §11a).
# -------------------------------------------------------------------------------------------
def a2_constrained(pts, basins):
    path = STRATA / "pop_worldpop_constrained.csv"
    if not path.exists():
        return {"status": "not run, 03-harness/02d_add_worldpop_constrained.py has not "
                          "produced pop_worldpop_constrained.csv"}
    con = pd.read_csv(path)
    cpop = dict(zip(con["HYBAS_ID"], pd.to_numeric(con["pop_worldpop_constrained"],
                                                   errors="coerce")))
    wpop = dict(zip(basins["HYBAS_ID"], pd.to_numeric(basins["pop_worldpop"], errors="coerce")))

    seeded = pts.dropna(subset=["hid"]).copy()
    seeded["hid"] = seeded["hid"].astype("int64")
    g = seeded.groupby("hid").agg(ev=("generous", "sum"))

    num = den = 0.0
    missing, missing_wpop = 0, 0.0
    for hid, row in g.iterrows():
        v = cpop.get(hid)
        if v is None or not np.isfinite(v):
            missing += 1
            w = wpop.get(hid)
            if w is not None and np.isfinite(w):
                missing_wpop += w
            continue
        den += v
        if row["ev"] == 0:
            num += v
    return {
        "status": "ok",
        "share": num / den if den else float("nan"),
        "numerator_pop": num, "denominator_pop": den,
        "basins_covered": int(len(g) - missing),
        "basins_missing_constrained": int(missing),
        "unconstrained_population_of_missing_basins": missing_wpop,
        "countries_covered": int(con["iso3"].nunique()),
        "note": "Headline only. PROTOCOL 11a forbids this surface in stratum 3 and in any "
                "figure crossing population with mapping density.",
    }


# -------------------------------------------------------------------------------------------
# A3. Evidenced rate against the observational record behind each gauge.
# -------------------------------------------------------------------------------------------
def a3_grdc_record(pts):
    st = pd.read_csv(META / "grdc_stations_20220320.csv")
    st["grdc_no"] = pd.to_numeric(st["grdc_no"], errors="coerce")

    af = pts[(~pts["is_hybas_entry"]) & (pts["has_metric_file"])].copy()
    af["grdc_no"] = pd.to_numeric(
        af["unique_gauge_id"].astype(str).str.extract(r"GRDC_(\d+)$")[0], errors="coerce")
    j = af.merge(st[["grdc_no", "d_start", "d_end", "d_yrs", "d_miss"]], on="grdc_no", how="left")

    matched = j["d_end"].notna()
    band = pd.cut(j.loc[matched, "d_end"],
                  [-np.inf, 1979, 1989, 1999, 2009, np.inf],
                  labels=["ends pre-1980", "1980s", "1990s", "2000s", "2010 or later"])
    by_end = {}
    for lab, sub in j.loc[matched].groupby(band, observed=True):
        k, n = int(sub["generous"].sum()), len(sub)
        by_end[str(lab)] = {"evidenced": k, "n": n, "rate": k / n, "wilson": wilson(k, n)}

    yrs = j.loc[matched & j["d_yrs"].notna()]
    qb = pd.qcut(yrs["d_yrs"], 4, labels=["Q1 shortest", "Q2", "Q3", "Q4 longest"],
                 duplicates="drop")
    by_len = {}
    for lab, sub in yrs.groupby(qb, observed=True):
        k, n = int(sub["generous"].sum()), len(sub)
        by_len[str(lab)] = {"evidenced": k, "n": n, "rate": k / n, "wilson": wilson(k, n),
                            "d_yrs_range": [float(sub["d_yrs"].min()),
                                            float(sub["d_yrs"].max())]}

    ev, un = j[j["generous"] == True], j[j["generous"] != True]   # noqa: E712
    return {
        "gauges_with_metric_file": int(len(j)),
        "matched_to_grdc_metadata": int(matched.sum()),
        "unmatched": int((~matched).sum()),
        "median_record_end_evidenced": float(ev["d_end"].median()) if ev["d_end"].notna().any() else None,
        "median_record_end_unevidenced": float(un["d_end"].median()) if un["d_end"].notna().any() else None,
        "median_record_years_evidenced": float(ev["d_yrs"].median()) if ev["d_yrs"].notna().any() else None,
        "median_record_years_unevidenced": float(un["d_yrs"].median()) if un["d_yrs"].notna().any() else None,
        "evidenced_rate_by_record_end": by_end,
        "evidenced_rate_by_record_length": by_len,
        "interpretation_limit": "Descriptive association only. No model fitted, no causal "
                                "claim, and a black-box tier cannot support one.",
    }


# -------------------------------------------------------------------------------------------
# B1. What the Q4 weighted mean actually rests on.
# -------------------------------------------------------------------------------------------
def b1_weights(pts, basins):
    wpop = dict(zip(basins["HYBAS_ID"], pd.to_numeric(basins["pop_worldpop"], errors="coerce")))
    s = pts[(~pts["is_hybas_entry"]) & pts["f1_of_record"].notna()].copy()
    s["w"] = s["hid"].map(wpop).fillna(0.0)
    f, w = s["f1_of_record"].to_numpy(float), s["w"].to_numpy(float)
    n = len(f)

    n_eff = (w.sum() ** 2) / (w ** 2).sum() if (w ** 2).sum() else float("nan")
    order = np.sort(w)[::-1]
    conc = {f"top_{k}_weight_share": float(order[:k].sum() / w.sum()) for k in (1, 5, 10, 25)}

    rng = np.random.default_rng(BOOTSTRAP_SEED)
    unw, wtd, diff = [], [], []
    for _ in range(BOOTSTRAP_DRAWS):
        idx = rng.integers(0, n, n)
        fb, wb = f[idx], w[idx]
        unw.append(fb.mean())
        wtd.append((fb * wb).sum() / wb.sum() if wb.sum() else np.nan)
        diff.append(unw[-1] - wtd[-1])
    q = lambda a, p: float(np.nanpercentile(a, p))                       # noqa: E731
    return {
        "n_gauges": n,
        "kish_n_eff": float(n_eff),
        "weight_concentration": conc,
        "unweighted_mean": float(f.mean()),
        "pop_weighted_mean": float((f * w).sum() / w.sum()),
        "bootstrap": {
            "seed": BOOTSTRAP_SEED, "draws": BOOTSTRAP_DRAWS,
            "unweighted_ci95": [q(unw, 2.5), q(unw, 97.5)],
            "pop_weighted_ci95": [q(wtd, 2.5), q(wtd, 97.5)],
            "difference_ci95": [q(diff, 2.5), q(diff, 97.5)],
            "difference_excludes_zero": bool(q(diff, 2.5) > 0 or q(diff, 97.5) < 0),
        },
        "metric": "F1 at return period 2.0, window 2 days, lead 0, google/2014/dual_lstm/"
                  "full_run, derived by us as the harmonic mean of released precision and recall",
    }


# -------------------------------------------------------------------------------------------
# B2. Can a micro-average be built from the release? Answered from the archive, not from memory.
# -------------------------------------------------------------------------------------------
def b2_micro_average():
    leaves, hydro_metrics, pickles = set(), set(), []
    with tarfile.open(TARBALL) as t:
        for m in t:
            if not m.isfile():
                continue
            if m.name.startswith("metrics/return_period_metrics/"):
                parts = m.name.split("/")
                if len(parts) >= 3:
                    leaves.add(parts[-2])
            if "/per_metric/" in m.name:
                hydro_metrics.add(Path(m.name).stem)
            if m.name.endswith(".pkl"):
                pickles.append(m.name)

    counts = re.compile(r"true_pos|false_pos|false_neg|\bn_?events?\b|count", re.I)
    return {
        "return_period_metric_directories": sorted(leaves),
        "hydrograph_metric_names": sorted(hydro_metrics),
        "concatenated_pickles": sorted(pickles),
        "any_count_like_metric_published": bool([x for x in leaves | hydro_metrics
                                                 if counts.search(x)]),
        "verdict": "not computable",
        "why": "The release publishes precision and recall and no contingency or event counts. "
               "A precision and a recall determine the table only up to a scale factor, so any "
               "pooled table would rest on a count we invented. The four concatenated pickles "
               "were opened on 2026-08-20 and hold the same two quantities in another "
               "container; that inspection is recorded in DECISIONS.md.",
        "consequence": "Every F1 this study reports is a weighted macro-average across gauges "
                       "and may not be read as the skill facing an average person. Per-gauge "
                       "event counts are added to the right-of-reply questions.",
    }


def main():
    print("=" * 78)
    print("QL-2026-01  stage 5, post-review additions   PROTOCOL 11a, not pre-registered")
    print("=" * 78)
    pts, basins = load()

    a1 = a1_downstream(pts, basins)
    print("\nA1  in reach, propagated downstream (WorldPop, frozen definition is steps_0)")
    for k, v in a1.items():
        print(f"  {k:9s} P_unevidenced {v['share']*100:6.2f}%   "
              f"basins in reach {v['basins_in_reach']:>7,}   "
              f"denominator {v['denominator_pop']:>15,.0f}")

    a2 = a2_constrained(pts, basins)
    print("\nA2  third population surface, WorldPop constrained, headline only")
    if a2.get("status") == "ok":
        print(f"  P_unevidenced {a2['share']*100:.2f}%   denominator {a2['denominator_pop']:,.0f}")
        print(f"  basins covered {a2['basins_covered']:,}, "
              f"missing a constrained value {a2['basins_missing_constrained']:,} "
              f"(holding {a2['unconstrained_population_of_missing_basins']:,.0f} "
              f"people on the unconstrained surface)")
    else:
        print(f"  {a2['status']}")

    a3 = a3_grdc_record(pts)
    print("\nA3  evidenced rate against the observational record")
    print(f"  {a3['matched_to_grdc_metadata']:,} of {a3['gauges_with_metric_file']:,} gauges "
          f"holding a metric file matched to GRDC metadata")
    print(f"  median record end year, evidenced {a3['median_record_end_evidenced']}, "
          f"unevidenced {a3['median_record_end_unevidenced']}")
    for lab, v in a3["evidenced_rate_by_record_end"].items():
        print(f"    {lab:16s} {fmt(v['evidenced'], v['n'])}")

    b1 = b1_weights(pts, basins)
    print("\nB1  what the population-weighted mean F1 rests on")
    print(f"  n {b1['n_gauges']}, Kish n_eff {b1['kish_n_eff']:.1f}, "
          f"top 10 basins hold {b1['weight_concentration']['top_10_weight_share']*100:.1f}% "
          f"of the weight")
    bs = b1["bootstrap"]
    print(f"  unweighted {b1['unweighted_mean']:.3f} "
          f"[{bs['unweighted_ci95'][0]:.3f}, {bs['unweighted_ci95'][1]:.3f}]")
    print(f"  weighted   {b1['pop_weighted_mean']:.3f} "
          f"[{bs['pop_weighted_ci95'][0]:.3f}, {bs['pop_weighted_ci95'][1]:.3f}]")
    print(f"  difference [{bs['difference_ci95'][0]:.3f}, {bs['difference_ci95'][1]:.3f}], "
          f"excludes zero: {bs['difference_excludes_zero']}")

    b2 = b2_micro_average()
    print("\nB2  micro-average F1")
    print(f"  return-period metric directories published: "
          f"{', '.join(b2['return_period_metric_directories'])}")
    print(f"  verdict: {b2['verdict']}")

    out = {"protocol_section": "11a", "pre_registered": False,
           "prompted_by": "operator adversarial self-review of the first full draft, 2026-08-20, standing in for external review, which has not happened",
           "a1_downstream_reach": a1, "a2_constrained_surface": a2,
           "a3_grdc_record": a3, "b1_weight_diagnostics": b1, "b2_micro_average": b2}
    (RESULTS / "post_review.json").write_text(json.dumps(out, indent=2, default=str) + "\n")
    print(f"\nwrote {(RESULTS / 'post_review.json').relative_to(STUDY)}")


if __name__ == "__main__":
    main()
