"""The primary metric, the secondary metrics, and Gates D, E and F.

    python3 04-analysis/02_primary.py --permute 20260806
    python3 04-analysis/02_primary.py --unblind

Reads only the evidence frame written by `01_evidence.py`, so it opens no metric table itself
and inherits whichever mode produced that frame.

P_unevidenced (PROTOCOL §5) is the proportion of the study-region population living in reach of
at least one forecast point, that lives in reach of no *evidenced* forecast point. In reach is
defined by the developer's own geometry, the HydroBASINS level-12 polygon their inventory
assigns each gauge to, rather than by a radius we invent. The denominator is population in
reach and never total African population, because people with no forecast point near them at
all are a different question, reported separately as a raw count.

NO CONFIDENCE INTERVAL IS PRINTED ON A POPULATION SHARE, and §9 requires the reason be given
wherever the number appears. A population-weighted share computed over a modelled raster has no
sampling error to quote. Its uncertainty is model error in WorldPop, which is structured rather
than random and far larger than any interval we could print, so a Wilson interval around it
would decorate it with a precision we do not have. Counts of basins and gauges do get Wilson
intervals, because there the sampling interpretation is real.

THE THREE GATES ARE EVALUATED HERE AND THEIR VERDICTS ARE BINDING, not advisory. They were
written before any number existed precisely so that a bad answer is a decision already taken
rather than a negotiation held once the answer is known.
"""
import argparse
import json
import sys
from pathlib import Path

import pandas as pd

STUDY = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(STUDY / "_lib"))
from stats import fmt, wilson                              # noqa: E402

RESULTS = STUDY / "05-results"
DEFS = {"generous": "evidenced_generous", "rp2": "evidenced_rp2", "rp5": "evidenced_rp5"}
SURFACES = {"worldpop": "pop_worldpop", "ghspop": "pop_ghspop"}

GATE_D_PP = 10.0        # spread across the three definitions above which no headline is published
GATE_E_PP = 5.0         # spread across population surfaces above which the spread is the result
GATE_F_PP = 5.0         # difference below which the null stands


def p_unevidenced(basins, ev_col, pop_col):
    """Return (share, numerator_pop, denominator_pop, basins_num, basins_denom).

    Basins carrying no population value are excluded from both numerator and denominator and
    counted separately by the caller. They are NA rather than zero: a basin nobody measured is
    not a basin nobody lives in, and averaging over it would quietly assert the opposite.
    """
    m = (basins["points"] > 0) & basins[pop_col].notna()
    denom = float(basins.loc[m, pop_col].sum())
    num_m = m & (basins[ev_col] == 0)
    num = float(basins.loc[num_m, pop_col].sum())
    return (num / denom if denom else float("nan")), num, denom, int(num_m.sum()), int(m.sum())


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--permute", type=int, metavar="SEED")
    g.add_argument("--unblind", action="store_true")
    a = ap.parse_args()
    tag = "" if a.unblind else f".permuted-{a.permute}"

    basins = pd.read_parquet(RESULTS / f"basins_evidence{tag}.parquet")
    points = pd.read_csv(RESULTS / f"points_evidence{tag}.csv")

    print("=" * 78)
    print(f"QL-2026-01  stage 2, primary metric and gates   "
          f"mode={'unblind' if a.unblind else 'permute'}"
          + ("" if a.unblind else f" seed={a.permute}"))
    if not a.unblind:
        print("PERMUTED. Gate verdicts below are a test of the machinery, not of the world.")
    print("=" * 78)

    out = {"mode": "unblind" if a.unblind else "permute",
           "seed": None if a.unblind else a.permute, "primary": {}}

    # ---- primary metric, three definitions by two surfaces --------------------------------
    print("\nP_unevidenced, population in reach of no evidenced forecast point")
    print(f"  {'definition':<12}{'surface':<10}{'share':>9}{'numerator':>16}{'denominator':>16}")
    for dname, col in DEFS.items():
        for sname, pcol in SURFACES.items():
            share, num, den, bn, bd = p_unevidenced(basins, col, pcol)
            out["primary"][f"{dname}__{sname}"] = {
                "share": share, "numerator_pop": num, "denominator_pop": den,
                "basins_numerator": bn, "basins_denominator": bd}
            print(f"  {dname:<12}{sname:<10}{100*share:>8.1f}%{num:>16,.0f}{den:>16,.0f}")

    unpop = int(((basins["points"] > 0) & basins["pop_worldpop"].isna()).sum())
    print(f"\n  basins in reach with no WorldPop value, excluded and counted: {unpop:,}")
    out["basins_in_reach_without_population"] = unpop

    # ---- Gate D, across the three definitions on the primary surface ----------------------
    shares = [out["primary"][f"{d}__worldpop"]["share"] for d in DEFS]
    spread_d = 100 * (max(shares) - min(shares))
    gate_d = spread_d > GATE_D_PP
    print(f"\nGate D  spread across the three definitions: {spread_d:.1f} pp "
          f"(threshold {GATE_D_PP})")
    print(f"        {'NO SINGLE HEADLINE NUMBER IS PUBLISHED' if gate_d else 'headline permitted'}")
    out["gate_d"] = {"spread_pp": spread_d, "threshold_pp": GATE_D_PP,
                     "verdict": "no_headline" if gate_d else "headline_permitted"}

    # ---- Gate E, across population surfaces on the frozen definition ----------------------
    spread_e = 100 * abs(out["primary"]["generous__worldpop"]["share"]
                         - out["primary"]["generous__ghspop"]["share"])
    gate_e = spread_e > GATE_E_PP
    print(f"\nGate E  spread across population surfaces: {spread_e:.1f} pp "
          f"(threshold {GATE_E_PP})")
    print(f"        {'THE SPREAD IS THE RESULT, limits box leads with it' if gate_e else 'within tolerance'}")
    print("        Reported with its mechanism in either case: the two surfaces are NOT")
    print("        independent with respect to mapping density (PROTOCOL §11, 2026-08-05).")
    out["gate_e"] = {"spread_pp": spread_e, "threshold_pp": GATE_E_PP,
                     "verdict": "spread_is_the_result" if gate_e else "within_tolerance",
                     "independent": False}

    # ---- secondary 1, gauge-count coverage, and Gate F ------------------------------------
    # Gate F's comparator is rung 2 of the denominator ladder, the real African gauges, fixed
    # by amendment on 2026-08-07 after a permuted dry run showed the verdict flipping across
    # all three rungs. Rung 2b includes the 3,682 undocumented `hybas_` entries, which cannot
    # hold a metric by construction and so depress the count for a reason unconnected to
    # evidence; rung 1 conditions on holding a metric file and compares the evidence base
    # against itself. Rung 2 is the only one where both sides can carry evidence. The other
    # rungs are still printed, because the ladder is reported in full and because a reader
    # should be able to see what the gate would have said elsewhere.
    n_points = len(points)
    n_ev = int(points["generous"].sum())
    real = points[~points["is_hybas_entry"]]
    withfile = points[points["has_metric_file"]]
    n_real, n_real_ev = len(real), int(real["generous"].sum())
    print(f"\nGauge-count coverage, the unweighted comparator")
    print(f"  rung 2b, all forecast points  : {fmt(n_ev, n_points)}")
    print(f"  rung 2,  real gauges  [GATE F]: {fmt(n_real_ev, n_real)}")
    print(f"  rung 1,  gauges with a file   : "
          f"{fmt(int(withfile['generous'].sum()), len(withfile))}")
    cov_count = n_real_ev / n_real if n_real else float("nan")
    cov_pop = 1 - out["primary"]["generous__worldpop"]["share"]
    diff_f = 100 * abs(cov_pop - cov_count)
    gate_f = diff_f < GATE_F_PP
    print(f"\nGate F  population-weighted coverage {100*cov_pop:.1f}% against gauge-count "
          f"{100*cov_count:.1f}%")
    print(f"        difference {diff_f:.1f} pp (threshold {GATE_F_PP})")
    print(f"        {'H0 STANDS, the evidence base tracks population closely' if gate_f else 'H0 rejected'}")
    out["secondary_gauge_count_coverage"] = {
        "rung_2b_all_points": {"evidenced": n_ev, "n": n_points,
                               "coverage": n_ev / n_points, "wilson": wilson(n_ev, n_points)},
        "rung_2_real_gauges": {"evidenced": n_real_ev, "n": n_real, "coverage": cov_count,
                               "wilson": wilson(n_real_ev, n_real), "gate_f_comparator": True},
        "rung_1_with_file": {"evidenced": int(withfile["generous"].sum()),
                             "n": int(len(withfile)),
                             "coverage": float(withfile["generous"].mean())}}
    out["gate_f"] = {"difference_pp": diff_f, "threshold_pp": GATE_F_PP,
                     "comparator_rung": 2, "comparator_n": n_real,
                     "coverage_population": cov_pop, "coverage_gauge_count": cov_count,
                     "verdict": "null_stands" if gate_f else "null_rejected"}

    # ---- secondary 3, coverage by mapping-density tercile ---------------------------------
    # The floor column is binding (amendment 2026-08-07). It is P_unevidenced if every gauge
    # holding a metric file turned out to be evidenced, so it isolates the part of the gradient
    # driven purely by which points have a file at all, which permutation does not touch and
    # which is a property of the release rather than of its contents. Published bare, the
    # tercile gradient invites attribution to the wrong mechanism, and the correction would
    # never catch up with the headline. The column costs nothing.
    print("\nP_unevidenced by OSM mapping-density tercile, with its structural floor")
    print(f"  {'tercile':<12}{'P_unev':>9}{'floor':>9}{'attributable':>14}"
          f"{'pop in reach':>16}{'basins':>9}")
    tercile = {}
    for t in ["T1_sparse", "T2", "T3_dense"]:
        sub = basins[basins["osm_density_tercile"] == t]
        share, num, den, bn, bd = p_unevidenced(sub, "evidenced_generous", "pop_worldpop")
        m = (sub["points"] > 0) & sub["pop_worldpop"].notna()
        floor = (float(sub.loc[m & (sub["points_with_file"] == 0), "pop_worldpop"].sum()) / den
                 if den else float("nan"))
        tercile[t] = {"share": share, "structural_floor": floor,
                      "attributable_to_null_content_pp": 100 * (share - floor),
                      "numerator_pop": num, "denominator_pop": den, "basins_in_reach": bd}
        print(f"  {t:<12}{100*share:>8.1f}%{100*floor:>8.1f}%"
              f"{100*(share-floor):>13.1f}pp{den:>16,.0f}{bd:>9,}")
    out["secondary_by_tercile"] = tercile
    print("  'floor' is P_unevidenced if every gauge holding a metric file were evidenced,")
    print("  so 'attributable' is the only part the metric contents decide.")

    # The same decomposition for the headline, also binding.
    mall = (basins["points"] > 0) & basins["pop_worldpop"].notna()
    den_all = float(basins.loc[mall, "pop_worldpop"].sum())
    floor_all = float(basins.loc[mall & (basins["points_with_file"] == 0),
                                 "pop_worldpop"].sum()) / den_all
    out["structural_floor"] = {
        "share": floor_all, "population_in_reach": den_all,
        "population_with_no_filed_gauge_in_reach": floor_all * den_all,
        "band_pp": 100 * (1 - floor_all)}
    print(f"\nStructural floor of the primary metric: {100*floor_all:.1f}%")
    print(f"  P_unevidenced is confined to [{100*floor_all:.1f}%, 100.0%] by file presence")
    print(f"  alone, a {100*(1-floor_all):.1f} pp band, before any metric value is read.")

    # ---- secondary 4, country table -------------------------------------------------------
    rows = []
    for iso, sub in basins[basins["points"] > 0].groupby("iso3"):
        share, num, den, bn, bd = p_unevidenced(sub, "evidenced_generous", "pop_worldpop")
        rows.append({"iso3": iso, "forecast_points": int(sub["points"].sum()),
                     "evidenced_points": int(sub["evidenced_generous"].sum()),
                     "population_in_reach": den, "p_unevidenced": share,
                     "basins_in_reach": bd})
    country = pd.DataFrame(rows).sort_values("population_in_reach", ascending=False)
    country.to_csv(RESULTS / f"country_table{tag}.csv", index=False)
    print(f"\nCountry table: {len(country)} countries with >=1 forecast point")
    print(country.head(8).to_string(index=False,
          formatters={"population_in_reach": "{:,.0f}".format,
                      "p_unevidenced": "{:.1%}".format}))

    (RESULTS / f"primary{tag}.json").write_text(json.dumps(out, indent=2) + "\n")
    print(f"\nwrote {RESULTS.name}/primary{tag}.json and country_table{tag}.csv")
    if not a.unblind:
        print("\nStill blind. Every number above is a machinery test.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
