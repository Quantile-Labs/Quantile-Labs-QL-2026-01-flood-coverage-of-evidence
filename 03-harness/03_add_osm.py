"""Attach OSM feature density to the basin frame — stratum 3.

BLIND. Mapping density is a stratum, never an outcome, and no metric value is read.

WHAT THIS MEASURES, AND WHAT IT DOES NOT. OSM feature density reflects **mapper attention**,
not settlement. A basin with few features may be empty, or may be unmapped. That ambiguity is
the point: the study asks whether published evidence is thinnest where the map is thinnest, and
this variable is the map's thinness. It is never used as a population proxy (PROTOCOL §7).

PINNED, NOT LATEST. Geofabrik's `-latest-` files move daily; terciles cut on a moving database
are not reproducible. This uses the dated snapshot and records the date in the manifest, per the
week-one pre-mortem disposition (item 6).

STREAMING, for the same reason as 02_: Nigeria's extract alone is 2.1 GB against ~6 GB free.
Download, count into basins, manifest, delete.

    python3 03-harness/03_add_osm.py --countries TCD
    python3 03-harness/03_add_osm.py                 # all, long-running

DO NOT RUN CONCURRENTLY WITH 02_add_population.py. Both read, modify and rewrite
basins_af.parquet, so running them at the same time loses whichever finishes first. They are
sequential steps, not parallel ones.

NOTE ON GROUPED EXTRACTS. Geofabrik does not publish one extract per country. Senegal and
Gambia share one; Morocco's includes Western Sahara. Counts from a grouped extract are joined
to basins spatially, so each basin still gets only the features inside it — but the download
list is by extract, not by country, and the mapping below records which is which.
"""
import argparse
import json
import subprocess
import sys
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd

STUDY = Path(__file__).resolve().parent.parent
LIB = STUDY.parent / "_lib"
INTERIM = STUDY / "02-data" / "interim"
OUT = INTERIM / "strata"
SCRATCH = INTERIM / "_scratch_osm"

_FORBIDDEN = [INTERIM / "metrics" / "return_period_metrics",
              INTERIM / "metrics" / "hydrograph_metrics" / "per_gauge"]
for _p in _FORBIDDEN:
    if _p.exists():
        sys.exit(f"REFUSING TO RUN: {_p} exists. Strata must be built blind.")

# Pinned snapshot date. Geofabrik redirected africa-latest -> africa-260803 on 2026-08-04.
SNAPSHOT = "260803"
URL = "https://download.geofabrik.de/africa/{slug}-" + SNAPSHOT + "-free.shp.zip"

# ISO3 -> Geofabrik extract slug. Grouped extracts are shared by several ISO3 codes; the
# spatial join still assigns features to the right basins.
SLUG = {
    "DZA": "algeria", "AGO": "angola", "BEN": "benin", "BWA": "botswana",
    "BFA": "burkina-faso", "BDI": "burundi", "CMR": "cameroon", "CPV": "cape-verde",
    "CAF": "central-african-republic", "TCD": "chad", "COM": "comores", "COG": "congo-brazzaville",
    "COD": "congo-democratic-republic", "DJI": "djibouti", "EGY": "egypt",
    "GNQ": "equatorial-guinea", "ERI": "eritrea", "SWZ": "swaziland", "ETH": "ethiopia",
    "GAB": "gabon", "GMB": "senegal-and-gambia", "GHA": "ghana", "GIN": "guinea",
    "GNB": "guinea-bissau", "CIV": "ivory-coast", "KEN": "kenya", "LSO": "lesotho",
    "LBR": "liberia", "LBY": "libya", "MDG": "madagascar", "MWI": "malawi", "MLI": "mali",
    "MRT": "mauritania", "MUS": "mauritius", "MAR": "morocco", "MOZ": "mozambique",
    "NAM": "namibia", "NER": "niger", "NGA": "nigeria", "RWA": "rwanda",
    "STP": "sao-tome-and-principe", "SEN": "senegal-and-gambia", "SYC": "seychelles",
    "SLE": "sierra-leone", "SOM": "somalia", "ZAF": "south-africa", "SSD": "south-sudan",
    "SDN": "sudan", "TZA": "tanzania", "TGO": "togo", "TUN": "tunisia", "UGA": "uganda",
    "ZMB": "zambia", "ZWE": "zimbabwe", "ESH": "morocco",
}
LAYERS = ["gis_osm_buildings_a_free_1", "gis_osm_roads_free_1"]


def manifest(path, url, notes):
    subprocess.run([sys.executable, str(LIB / "manifest.py"), "QL-2026-01", str(path),
                    "--url", url, "--licence", "ODbL", "--notes", notes, "--transient"], check=True)


def count_into_basins(zip_path, basins):
    """Count building polygons and road lines falling in each basin.

    Returns (total_counts, per_layer_counts). Layers are kept apart because if roads
    dominate, this variable is a road-mapping index and must be described as one rather
    than as "settlement mapping density".
    """
    counts, per_layer = {}, {}
    with zipfile.ZipFile(zip_path) as z:
        names = z.namelist()
        for layer in LAYERS:
            if not any(n.startswith(layer) for n in names):
                continue
            gdf = gpd.read_file(f"zip://{zip_path}!{layer}.shp")
            if gdf.empty:
                continue
            # Represent every feature by one interior point: a road crossing three basins
            # should not be counted three times, and polygon centroids can fall outside
            # concave shapes.
            gdf = gdf.set_geometry(gdf.geometry.representative_point())
            if gdf.crs != basins.crs:
                gdf = gdf.to_crs(basins.crs)
            j = gpd.sjoin(gdf[["geometry"]], basins[["HYBAS_ID", "geometry"]],
                          how="inner", predicate="within")
            vc = j["HYBAS_ID"].value_counts()
            per_layer[layer] = int(vc.sum())
            for hid, n in vc.items():
                counts[hid] = counts.get(hid, 0) + int(n)
            del gdf, j
    return counts, per_layer


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--countries", help="comma-separated ISO3 subset")
    a = ap.parse_args()

    geom = gpd.read_parquet(OUT / "basins_af_geom.parquet")
    attrs = pd.read_parquet(OUT / "basins_af.parquet")
    if "iso3" not in attrs.columns:
        sys.exit("run 01b_assign_countries.py first")
    basins = geom.merge(attrs[["HYBAS_ID", "iso3"]], on="HYBAS_ID")

    isos = a.countries.split(",") if a.countries else sorted(set(attrs["iso3"].dropna()) & set(SLUG))
    # One download per distinct extract, not per country.
    extracts = {}
    for iso in isos:
        if iso in SLUG:
            extracts.setdefault(SLUG[iso], []).append(iso)
    print(f"{len(isos)} countries -> {len(extracts)} Geofabrik extracts, snapshot {SNAPSHOT}")
    SCRATCH.mkdir(parents=True, exist_ok=True)

    totals, failed, processed, layer_totals = {}, [], [], {}
    for i, (slug, isos_here) in enumerate(sorted(extracts.items()), 1):
        sub = basins[basins["iso3"].isin(isos_here)]
        if sub.empty:
            continue
        url = URL.format(slug=slug)
        dest = SCRATCH / f"{slug}.shp.zip"
        print(f"[{i}/{len(extracts)}] {slug} ({'+'.join(isos_here)}) {len(sub):,} basins ... ",
              end="", flush=True)
        r = subprocess.run(["curl", "-sSfL", "-o", str(dest), url], capture_output=True)
        if r.returncode != 0 or not dest.exists():
            print("NO EXTRACT")
            failed.append(slug)
            continue
        manifest(dest, url, f"Geofabrik {slug} free shapefile extract, snapshot {SNAPSHOT}. "
                            f"Counted into basins then deleted; hash pins the snapshot so "
                            f"terciles are reproducible against a moving database.")
        try:
            c, per_layer = count_into_basins(dest, sub)
            totals.update(c)
            # A basin inside a successfully processed extract with no features has ZERO
            # features. It is not unknown. Recording it as NA would drop the least-mapped
            # basins out of stratum 3 — the exact places the stratum exists to identify —
            # and would bias the tercile cut towards better-mapped ground. Chad: 5,045 of
            # 9,667 basins are genuine zeros.
            for hid in sub["HYBAS_ID"]:
                totals.setdefault(hid, 0)
            processed.extend(isos_here)
            layer_totals[slug] = per_layer
        except Exception as e:                       # noqa: BLE001 — report, do not abort the run
            print(f"COUNT FAILED: {e}")
            failed.append(slug)
        finally:
            dest.unlink(missing_ok=True)
        nz = sum(1 for h in sub["HYBAS_ID"] if totals.get(h, 0) > 0)
        print(f"ok  ({nz:,} basins with features, {len(sub) - nz:,} genuine zeros)")

    if "osm_feature_count" not in attrs.columns:
        attrs["osm_feature_count"] = pd.NA
    new = attrs["HYBAS_ID"].map(totals)
    attrs["osm_feature_count"] = new.combine_first(
        pd.to_numeric(attrs["osm_feature_count"], errors="coerce"))

    # Density per km2. SUB_AREA is the basin's own area in km2, from HydroBASINS.
    area = pd.to_numeric(attrs["SUB_AREA"], errors="coerce").replace(0, pd.NA)
    attrs["osm_feature_density"] = pd.to_numeric(attrs["osm_feature_count"],
                                                 errors="coerce") / area

    # Terciles cut on the study-region distribution (PROTOCOL §8). Only basins inside a
    # successfully processed extract may be cut; anything not downloaded stays NA, because
    # confusing unprocessed with unmapped is the one error this stratum cannot make.
    covered = attrs["osm_feature_density"].notna()
    dens = attrs.loc[covered, "osm_feature_density"]
    zero_share = float((dens == 0).mean()) if len(dens) else 0.0

    # With more than a third of basins at exactly zero, equal-sized terciles do not exist:
    # qcut would silently collapse to two bins and the study would report a three-way
    # stratification it never performed. Detect it and say so.
    tercile_note = None
    if zero_share > 1 / 3:
        tercile_note = (f"{100*zero_share:.1f}% of covered basins have ZERO features, so "
                        f"equal-frequency terciles do not exist. Cut is: T1_sparse = zero "
                        f"features, T2/T3 = median split of the non-zero remainder. This is "
                        f"a deviation from the equal-frequency reading of PROTOCOL §8 and is "
                        f"reported as such.")
        print(f"\n*** {tercile_note}")
        nonzero = dens[dens > 0]
        med = nonzero.median() if len(nonzero) else 0
        attrs.loc[covered & (attrs["osm_feature_density"] == 0), "osm_density_tercile"] = "T1_sparse"
        attrs.loc[covered & (attrs["osm_feature_density"] > 0)
                  & (attrs["osm_feature_density"] <= med), "osm_density_tercile"] = "T2"
        attrs.loc[covered & (attrs["osm_feature_density"] > med), "osm_density_tercile"] = "T3_dense"
    else:
        attrs.loc[covered, "osm_density_tercile"] = pd.qcut(
            dens, 3, labels=["T1_sparse", "T2", "T3_dense"], duplicates="drop")

    attrs.to_parquet(OUT / "basins_af.parquet", index=False)
    print(f"\nosm density: {int(covered.sum()):,} / {len(attrs):,} basins  "
          f"({100*zero_share:.1f}% of them genuine zeros)")

    # If roads dominate, this is a road-mapping index and the Note must call it that.
    grand = {}
    for per in layer_totals.values():
        for k, v in per.items():
            grand[k] = grand.get(k, 0) + v
    if grand:
        tot = sum(grand.values())
        print("feature mix:")
        for k, v in sorted(grand.items(), key=lambda kv: -kv[1]):
            print(f"    {v:>12,}  {100*v/tot:5.1f}%  {k}")

    if failed:
        print(f"failed extracts ({len(failed)}): {failed}")
    (OUT / "osm_run.json").write_text(json.dumps(
        {"snapshot": SNAPSHOT, "extracts": len(extracts),
         "basins_with_density": int(covered.sum()), "zero_share": zero_share,
         "tercile_note": tercile_note, "feature_mix": grand,
         "countries_processed": sorted(set(processed)), "failed": failed}, indent=2))
    print("No metric value has been read.")


if __name__ == "__main__":
    main()
