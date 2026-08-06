"""Build the QL-2026-01 basin table and the strata that do not need a metric value.

BLIND BY CONSTRUCTION. This is the script the protocol's structural-blinding clause is about:
the strata, the basin assignment and the exposure frame are built before any skill value has
been loaded, so they cannot be nudged by having glimpsed the answer. The assert below is the
second person this study does not have. Do not weaken it.

    python3 03-harness/01_build_strata.py

Produces 02-data/interim/strata/:
    basins_af.parquet      one row per African HydroBASINS level-12 basin
    points_assigned.csv    every forecast point with its basin, or the reason it has none
    gate_c.json            basin-assignment rate — the Gate C test
    ladder.json            the four-rung denominator, counted

Population and OSM strata are added by 02_add_population.py and 03_add_osm.py, which stream
their inputs per country. They are separate scripts because those layers are tens of gigabytes
and this one must stay runnable in a minute on a laptop.
"""
import csv
import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

STUDY = Path(__file__).resolve().parent.parent
LIB = STUDY / "_lib"
INTERIM = STUDY / "02-data" / "interim"
OUT = INTERIM / "strata"
META = INTERIM / "metadata"
GROUPS = INTERIM / "gauge_groups_for_paper" / "dual_lstm"
BASINS_SHP = INTERIM / "hydrobasins" / "hybas_af_lev12_v1c.shp"

sys.path.insert(0, str(LIB))
from blind import require_absent          # noqa: E402 — path must be set before the import

# ---------------------------------------------------------------------------------------
# The blinding assert. Metric tables live inside the manifested tarballs and are never
# unpacked into the tree; if one ever is, this script must not run until it is understood
# why. PROTOCOL §10 "structural blinding", amended v1.8.
#
# The target is the WHOLE metrics tree, and the check is the shared helper rather than an
# inline copy. Both of those are corrections: this script previously named two subdirectories
# that were never extracted, so it guarded nothing from 2026-08-04 to 2026-08-06 while other
# metric directories sat in the tree. See _lib/blind.py and DECISIONS.md 2026-08-06.
# ---------------------------------------------------------------------------------------
require_absent(INTERIM / "metrics")

# Pre-registered strata cut points (PROTOCOL §8). Fixed here, before any number exists.
POP_BANDS = [(0, 10_000), (10_000, 100_000), (100_000, 1_000_000), (1_000_000, float("inf"))]
POP_BAND_NAMES = ["<10k", "10k-100k", "100k-1M", ">=1M"]
MATERIAL_POP_THRESHOLD = 100_000          # PROTOCOL §6 harm threshold
GATE_C_THRESHOLD = 0.90                   # PROTOCOL §10 Gate C


def read_group(p):
    return {ln.strip() for ln in Path(p).read_text().splitlines() if ln.strip()}


def load_points():
    """Every forecast point in the published inventory, with coordinates and its declared basin.

    Reads identifiers, coordinates and inventory bookkeeping only. Touches no metric.
    """
    rows = list(csv.DictReader(open(META / "hybas_gauges_info_lev12.csv", encoding="utf-8",
                                    errors="replace")))
    df = pd.DataFrame(rows)
    df = df[["unique_gauge_id", "longitude", "latitude", "HYBAS_ID", "NEXT_DOWN",
             "UP_AREA", "SUB_AREA", "continent", "provider", "data_source"]].copy()
    for c in ["longitude", "latitude", "UP_AREA", "SUB_AREA"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    # Gate H: undocumented entries are flagged, never silently dropped or silently kept.
    df["is_hybas_entry"] = df["unique_gauge_id"].str.startswith("hybas_")
    return df


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print("=" * 74)
    print("QL-2026-01  strata build  (blind — no metric value is read)")
    print("=" * 74)

    # ---- basins ------------------------------------------------------------------------
    print(f"\n[1] Reading {BASINS_SHP.name} ...")
    basins = gpd.read_file(BASINS_SHP)
    print(f"    African level-12 basins: {len(basins):,}")
    print(f"    CRS: {basins.crs}")
    keep = [c for c in ["HYBAS_ID", "NEXT_DOWN", "SUB_AREA", "UP_AREA", "PFAF_ID",
                        "ENDO", "COAST", "ORDER"] if c in basins.columns]
    basins = basins[keep + ["geometry"]]
    basins["HYBAS_ID"] = basins["HYBAS_ID"].astype("int64")

    # Stratum 5 — upstream-area quartiles, cut on the study-region distribution (§8).
    basins["up_area_quartile"] = pd.qcut(
        basins["UP_AREA"], 4, labels=["Q1", "Q2", "Q3", "Q4"], duplicates="drop")

    # ---- points ------------------------------------------------------------------------
    print("\n[2] Reading the published forecast-point inventory ...")
    pts = load_points()
    af = pts[pts["continent"] == "AFRICA"].copy()
    print(f"    inventory rows: {len(pts):,}   African: {len(af):,}")
    print(f"    of the African rows, undocumented hybas_* entries: {af['is_hybas_entry'].sum():,}")

    # ---- Gate C ------------------------------------------------------------------------
    # The developer supplies HYBAS_ID per point. Gate C asks whether those assignments land
    # in the basin file we hold — an independent check on the join, not a re-derivation.
    print("\n[3] Gate C — basin assignment")
    known = set(basins["HYBAS_ID"])
    af["hybas_int"] = pd.to_numeric(af["HYBAS_ID"], errors="coerce").astype("Int64")
    af["assigned"] = af["hybas_int"].isin(known)
    rate = af["assigned"].mean()
    print(f"    African points assigning to a level-12 basin: "
          f"{af['assigned'].sum():,} / {len(af):,}  ({100 * rate:.1f}%)")
    gate_c = {
        "threshold": GATE_C_THRESHOLD,
        "rate": float(rate),
        "assigned": int(af["assigned"].sum()),
        "total": int(len(af)),
        "verdict": "PASS" if rate >= GATE_C_THRESHOLD else "FALLBACK to 10 km buffer",
    }
    print(f"    → {gate_c['verdict']}")
    (OUT / "gate_c.json").write_text(json.dumps(gate_c, indent=2))

    # ---- the denominator ladder (§4, §5, §8) --------------------------------------------
    print("\n[4] Denominator ladder")
    evaluated = read_group(GROUPS / "grdc_filtered.txt")
    africa_eval = read_group(GROUPS / "continent_splits" / "africa.txt") & evaluated
    real_af = af[~af["is_hybas_entry"]]
    ladder = {
        "rung_1_evaluated_african_gauges": len(africa_eval),
        "rung_2_real_african_gauges": int(len(real_af)),
        "rung_2b_inventory_rows_incl_undocumented": int(len(af)),
        "rung_3_african_level12_basins": int(len(basins)),
        "rung_4_product_display_surface": None,   # not enumerable from any release — §10 Gate A
    }
    for k, v in ladder.items():
        print(f"    {k:<45} {'not enumerable' if v is None else format(v, ',')}")
    (OUT / "ladder.json").write_text(json.dumps(ladder, indent=2))

    # ---- basins that contain a forecast point -------------------------------------------
    print("\n[5] Basins containing at least one forecast point")
    counts = (af[af["assigned"]].groupby("hybas_int")
              .agg(points=("unique_gauge_id", "size"),
                   real_points=("is_hybas_entry", lambda s: int((~s).sum())),
                   undocumented_points=("is_hybas_entry", "sum")))
    basins = basins.merge(counts, left_on="HYBAS_ID", right_index=True, how="left")
    for c in ["points", "real_points", "undocumented_points"]:
        basins[c] = basins[c].fillna(0).astype(int)
    with_pt = int((basins["points"] > 0).sum())
    print(f"    basins with >=1 forecast point: {with_pt:,} / {len(basins):,} "
          f"({100 * with_pt / len(basins):.2f}%)")
    print(f"    basins with >=1 *real gauge*:   {int((basins['real_points'] > 0).sum()):,}")

    # Population columns are created empty and filled by 02_add_population.py. They exist
    # here so the schema is fixed before the numbers are, and so the harm-threshold and
    # population-band logic is written before any population value can influence it.
    basins["pop_worldpop"] = pd.NA
    basins["pop_ghspop"] = pd.NA
    basins["pop_band"] = pd.NA
    basins["osm_feature_density"] = pd.NA
    basins["osm_density_tercile"] = pd.NA

    out = OUT / "basins_af.parquet"
    basins.drop(columns="geometry").to_parquet(out, index=False)
    basins[["HYBAS_ID", "geometry"]].to_parquet(OUT / "basins_af_geom.parquet", index=False)
    print(f"\n    wrote {out.relative_to(STUDY)}  ({len(basins):,} rows)")

    af.drop(columns=["hybas_int"]).to_csv(OUT / "points_assigned.csv", index=False)
    print(f"    wrote {(OUT / 'points_assigned.csv').relative_to(STUDY)}  ({len(af):,} rows)")

    print("\n" + "=" * 74)
    print("Strata frame built. Population and OSM strata pending — 02_ and 03_.")
    print("No metric value has been read.")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
