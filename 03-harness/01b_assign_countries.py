"""Assign every African basin to a country by geometry, and count where that disagrees
with the developer's own assignment.

BLIND. Countries are a stratum, not an outcome.

PROTOCOL §4 requires both assignments to be kept: the developer's governs evidence counting,
the boundary file governs population, and **every disagreement is counted and reported** rather
than silently resolved. This script produces that count.

It also settles what rung 3 of the denominator ladder actually is. The HydroSHEDS "af" region
is not the same set as "basins in African countries" — it reaches into Iberia, Yemen and the
Mediterranean islands — and 34,496 basins carry no country at all in the developer's list.
Rung 3 is therefore reported as a range with its definitions, not as one number.

    python3 03-harness/01b_assign_countries.py
"""
import csv
import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

STUDY = Path(__file__).resolve().parent.parent
LIB = STUDY.parent / "_lib"
INTERIM = STUDY / "02-data" / "interim"
OUT = INTERIM / "strata"
ADM0 = STUDY / "02-data" / "raw" / "geoBoundariesCGAZ_ADM0.gpkg"

sys.path.insert(0, str(LIB))
from blind import require_absent          # noqa: E402 — path must be set before the import

# Structural blinding, PROTOCOL §10 as amended in v1.8: the shared helper, and the whole
# metrics tree rather than named subdirectories inside it. See DECISIONS.md 2026-08-06.
require_absent(INTERIM / "metrics")

# UN M49 Africa, ISO3. The study region, fixed here.
AFRICA_ISO3 = {
    "DZA", "AGO", "BEN", "BWA", "BFA", "BDI", "CPV", "CMR", "CAF", "TCD", "COM", "COG", "COD",
    "DJI", "EGY", "GNQ", "ERI", "SWZ", "ETH", "GAB", "GMB", "GHA", "GIN", "GNB", "CIV", "KEN",
    "LSO", "LBR", "LBY", "MDG", "MWI", "MLI", "MRT", "MUS", "MAR", "MOZ", "NAM", "NER", "NGA",
    "RWA", "STP", "SEN", "SYC", "SLE", "SOM", "ZAF", "SSD", "SDN", "TZA", "TGO", "TUN", "UGA",
    "ZMB", "ZWE", "ESH",
}


def main():
    print("=" * 74)
    print("QL-2026-01  country assignment  (blind)")
    print("=" * 74)

    geom = gpd.read_parquet(OUT / "basins_af_geom.parquet")
    attrs = pd.read_parquet(OUT / "basins_af.parquet")
    print(f"\nbasins in the HydroSHEDS 'af' region: {len(geom):,}")

    adm = gpd.read_file(ADM0)
    iso_col = next(c for c in adm.columns if c.lower() in ("shapegroup", "shapeiso", "iso_a3"))
    adm = adm[[iso_col, "geometry"]].rename(columns={iso_col: "iso3"})
    print(f"ADM0 polygons: {len(adm):,}")

    # Representative points, not centroids: a centroid can fall outside a concave basin, and
    # a coastal basin's centroid can land in the sea. representative_point() is guaranteed
    # inside the polygon.
    pts = geom.copy()
    pts["geometry"] = pts.geometry.representative_point()
    if pts.crs != adm.crs:
        pts = pts.to_crs(adm.crs)

    print("\nspatial join ...")
    joined = gpd.sjoin(pts, adm, how="left", predicate="within")
    joined = joined.drop_duplicates(subset="HYBAS_ID", keep="first")
    geo_iso = dict(zip(joined["HYBAS_ID"], joined["iso3"]))

    attrs["iso3"] = attrs["HYBAS_ID"].map(geo_iso)
    attrs["in_study_region"] = attrs["iso3"].isin(AFRICA_ISO3)

    unassigned = attrs["iso3"].isna().sum()
    in_region = int(attrs["in_study_region"].sum())
    print(f"\n  assigned to a country : {len(attrs) - unassigned:,}")
    print(f"  no country (offshore) : {unassigned:,}")
    print(f"  in study region       : {in_region:,}")
    print(f"  outside study region  : {len(attrs) - in_region - unassigned:,}")

    # --- disagreement with the developer's own assignment (PROTOCOL §4) -------------------
    dev = {}
    with open(INTERIM / "metadata" / "hybas_country_list.csv") as f:
        for r in csv.DictReader(f):
            hid = r["HyBAS ID"]
            if hid.startswith("hybas_"):
                dev[int(hid[6:])] = (r["Country"] or "").strip()
    attrs["country_developer"] = attrs["HYBAS_ID"].map(dev)

    both = attrs[attrs["iso3"].notna() & attrs["country_developer"].notna()
                 & (attrs["country_developer"] != "") & (attrs["country_developer"] != "None")]
    dev_blank = int(((attrs["country_developer"].isna())
                     | (attrs["country_developer"].isin(["", "None"]))).sum())
    print(f"\n  developer list blank/None for : {dev_blank:,} basins")
    print(f"  comparable on both            : {len(both):,}")

    rung3 = {
        "hydrosheds_af_region_total": int(len(attrs)),
        "geometrically_in_african_countries": in_region,
        "no_country_offshore_or_unmatched": int(unassigned),
        "developer_list_blank_or_None": dev_blank,
        "note": ("Rung 3 is reported as a range with definitions, never as one number. The "
                 "HydroSHEDS 'af' region is not the set of basins in African countries."),
    }
    (OUT / "rung3_definitions.json").write_text(json.dumps(rung3, indent=2))

    attrs.to_parquet(OUT / "basins_af.parquet", index=False)
    print(f"\n  wrote iso3 + country_developer into basins_af.parquet")
    print("\nNo metric value has been read.")
    print("=" * 74)


if __name__ == "__main__":
    main()
