"""Cut the basin population band — stratum 4 of PROTOCOL §8, the last stratum that can be
built without a metric value.

BLIND. The band is a slice of a covariate that already exists in the frame; nothing new is
read and no outcome is touched.

NOTE ON THE RUN OF RECORD. The 2026-08-06T09:11:51Z execution logged in RUNLOG.md ran under
the old, narrow guard, which named two subdirectories that had never been extracted and so
could not fire. The guard was widened later the same day, once the defect was found, and then
converted across every harness script to the shared `_lib/blind.py` helper. Re-running this
script now correctly refuses until the metrics tree is moved out of `02-data/interim/`. The
output is unaffected — this script reads only the basin frame — but the sequence is recorded
rather than smoothed over.

    python3 03-harness/02c_add_pop_band.py

WHICH SURFACE CUTS THE BAND. `pop_band` is cut on **WorldPop unconstrained**, the primary
weight. That is not a coin toss. 02_add_population.py chose unconstrained WorldPop precisely
because it carries no dependency on settlement detection, which stratum 3 measures; cutting
the population stratum on the settlement-derived surface instead would import that dependency
back into the frame through the side door.

The 2026-08-05 Gate E measurement makes the alternative concrete rather than theoretical:
GHS-POP is 28.5% of WorldPop inside the sparse tercile and exactly zero in 66.8% of sparse
basins, so a GHS-POP band would drop a large share of sparsely mapped basins into `<10k` for
a reason that is a property of the sensor, not of the people. A second column,
`pop_band_ghspop`, is therefore written alongside it and labelled a **sensitivity, not an
alternative**: the protocol's binding consequence (c) is that where the two surfaces differ
the range is the result, so the disagreement has to be visible in the frame rather than
discoverable only by someone who thought to recompute it.

BOUNDARIES ARE LEFT-CLOSED, RIGHT-OPEN: [0, 10k) [10k, 100k) [100k, 1M) [1M, inf). Stated
because 100,000 is also the §6 harm threshold, and a reader is entitled to know on which side
of the line a basin of exactly 100,000 people falls. It falls in `100k-1M`.

BASINS WITH NO POPULATION VALUE KEEP NO BAND. 1,684 basins carry no WorldPop value (146
offshore, 79 behind a junk geoBoundaries code, 1,459 otherwise unassigned) and 18,096 carry no
GHS-POP value. They are NA, never `<10k`. A basin nobody measured is not a basin nobody lives
in — the same distinction the zonal sums preserve, and the distinction this whole study is
about.
"""
import json
import sys
from pathlib import Path

import pandas as pd

STUDY = Path(__file__).resolve().parent.parent
LIB = STUDY.parent / "_lib"
INTERIM = STUDY / "02-data" / "interim"
OUT = INTERIM / "strata"

sys.path.insert(0, str(LIB))
from blind import require_absent          # noqa: E402 — path must be set before the import

# Structural blinding, PROTOCOL §10 as amended in v1.8: the shared helper, and the WHOLE
# metrics tree rather than named subdirectories inside it.
#
# 01_ through 03_ each named `metrics/return_period_metrics` and
# `metrics/hydrograph_metrics/per_gauge`. Neither was ever extracted, so the guard could not
# fire, while `metrics/concatenated_return_period_metrics` and
# `metrics/hydrograph_metrics/per_metric/` sat there unguarded from day 1 — both outcome
# values. Blinding held in fact, since no script opens those paths, but the safeguard meant
# to make that structural was inert for the whole build. Found 2026-08-06, logged, and fixed
# in every script rather than only this one.
require_absent(INTERIM / "metrics")

# Pre-registered in PROTOCOL §8 and restated verbatim from 01_build_strata.py. Not re-derived
# from the data, not tuned to give equal-sized bands — these are the numbers frozen before any
# population value existed, and an equal-frequency cut here would be a deviation.
POP_BAND_EDGES = [0, 10_000, 100_000, 1_000_000, float("inf")]
POP_BAND_NAMES = ["<10k", "10k-100k", "100k-1M", ">=1M"]
MATERIAL_POP_THRESHOLD = 100_000          # PROTOCOL §6 harm threshold


def cut_band(values):
    """Bands per §8, left-closed and right-open. NA in, NA out."""
    v = pd.to_numeric(values, errors="coerce")
    return pd.cut(v, bins=POP_BAND_EDGES, labels=POP_BAND_NAMES, right=False,
                  include_lowest=True)


def report(attrs, col, band_col, label):
    v = pd.to_numeric(attrs[col], errors="coerce")
    n_val = int(v.notna().sum())
    print(f"\n{label}  ({band_col})")
    print(f"    basins with a value: {n_val:,} / {len(attrs):,}")
    print(f"    basins with none:    {len(attrs) - n_val:,}  (NA band, not '<10k')")
    counts = attrs[band_col].value_counts(dropna=False).reindex(POP_BAND_NAMES)
    print(f"    {'band':<10} {'basins':>9} {'share':>7} {'population':>16}")
    for name in POP_BAND_NAMES:
        n = int(counts.get(name, 0) or 0)
        pop = float(v[attrs[band_col] == name].sum())
        share = 100 * n / n_val if n_val else 0.0
        print(f"    {name:<10} {n:>9,} {share:>6.1f}% {pop:>16,.0f}")
    return {name: int(counts.get(name, 0) or 0) for name in POP_BAND_NAMES}


def main():
    attrs = pd.read_parquet(OUT / "basins_af.parquet")
    for col in ("pop_worldpop", "pop_ghspop"):
        if col not in attrs.columns:
            sys.exit(f"run 03-harness/02_add_population.py first — no {col} column")

    print("=" * 74)
    print("QL-2026-01  stratum 4, basin population band  (blind — no metric value is read)")
    print("=" * 74)
    print(f"bands (left-closed, right-open): {POP_BAND_NAMES}")
    print(f"cut on WorldPop unconstrained; §6 harm threshold {MATERIAL_POP_THRESHOLD:,} "
          f"is a band edge")

    attrs["pop_band"] = cut_band(attrs["pop_worldpop"])
    attrs["pop_band_ghspop"] = cut_band(attrs["pop_ghspop"])

    primary = report(attrs, "pop_worldpop", "pop_band", "PRIMARY — WorldPop unconstrained")
    sens = report(attrs, "pop_ghspop", "pop_band_ghspop",
                  "SENSITIVITY — GHS-POP (not an independent check; see Gate E)")

    # The Gate E spread, made visible in the frame rather than left to be rediscovered. Only
    # basins carrying BOTH surfaces can disagree, so they are the denominator here.
    both = attrs["pop_band"].notna() & attrs["pop_band_ghspop"].notna()
    same = int((attrs.loc[both, "pop_band"].astype(str)
                == attrs.loc[both, "pop_band_ghspop"].astype(str)).sum())
    n_both = int(both.sum())
    print(f"\nGate E, band agreement")
    print(f"    basins carrying both surfaces: {n_both:,}")
    print(f"    same band under both:          {same:,}  ({100*same/n_both:.1f}%)")
    print(f"    different band:                {n_both - same:,}  "
          f"({100*(n_both - same)/n_both:.1f}%)")

    # Where the disagreement lands. If it concentrates in the sparse tercile, the band is
    # entangled with stratum 3 in exactly the way Gate E warned about, and the Note has to
    # say so rather than report one band table as though it were the band table.
    if "osm_density_tercile" in attrs.columns:
        print("\n    disagreement by mapping-density tercile:")
        by_terc = {}
        for terc in ["T1_sparse", "T2", "T3_dense"]:
            m = both & (attrs["osm_density_tercile"] == terc)
            n = int(m.sum())
            if not n:
                continue
            d = int((attrs.loc[m, "pop_band"].astype(str)
                     != attrs.loc[m, "pop_band_ghspop"].astype(str)).sum())
            by_terc[terc] = {"basins": n, "disagree": d, "share": d / n}
            print(f"        {terc:<10} {d:>8,} / {n:>8,}  ({100*d/n:5.1f}%)")
    else:
        by_terc = {}

    attrs.to_parquet(OUT / "basins_af.parquet", index=False)
    print(f"\nwrote {(OUT / 'basins_af.parquet').relative_to(STUDY)}  ({len(attrs):,} rows)")

    (OUT / "pop_band_run.json").write_text(json.dumps({
        "edges": [e if e != float("inf") else None for e in POP_BAND_EDGES],
        "names": POP_BAND_NAMES,
        "interval": "left-closed, right-open",
        "primary_surface": "worldpop_unconstrained",
        "counts_worldpop": primary,
        "counts_ghspop": sens,
        "unbanded_worldpop": int(attrs["pop_band"].isna().sum()),
        "unbanded_ghspop": int(attrs["pop_band_ghspop"].isna().sum()),
        "band_agreement_both_surfaces": {"basins": n_both, "same_band": same},
        "disagreement_by_tercile": by_terc,
    }, indent=2))

    print("\n" + "=" * 74)
    print("Stratum 4 built. All five blind strata now populated; stratum 2 (evidence class)")
    print("requires unblinding and is not built here.")
    print("No metric value has been read.")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
