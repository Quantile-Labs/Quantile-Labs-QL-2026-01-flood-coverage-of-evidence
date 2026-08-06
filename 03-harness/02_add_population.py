"""Attach population to the basin frame, from two independent surfaces.

BLIND. Population is a covariate and a weight, never an outcome. No metric value is read here
either — the same assert as 01_ applies and is imported rather than restated.

WHY THIS STREAMS. WorldPop 100 m for Africa and GHS-POP 100 m global are tens of gigabytes
between them, against ~7 GB of free disk on this machine. So each country raster is downloaded,
summed into basins, hashed into the manifest, and deleted before the next one starts. Peak disk
stays under a gigabyte and the result is identical to holding everything at once. Every file is
recorded in MANIFEST.csv on arrival, so the run is reproducible without the bytes being kept.

    python3 03-harness/02_add_population.py --surface worldpop
    python3 03-harness/02_add_population.py --surface ghspop
    python3 03-harness/02_add_population.py --surface worldpop --countries NGA,TCD

PROTOCOL §9 and Gate E: both surfaces are required, and the spread between them — not either
figure — is the reported uncertainty on any population share. Running only one is not a
shortcut, it is an incomplete study.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.mask import mask

STUDY = Path(__file__).resolve().parent.parent
LIB = STUDY.parent / "_lib"
INTERIM = STUDY / "02-data" / "interim"
OUT = INTERIM / "strata"
SCRATCH = INTERIM / "_scratch_raster"

sys.path.insert(0, str(LIB))
from blind import require_absent          # noqa: E402 — path must be set before the import

# Same blinding guard as 01_build_strata.py, and now literally the same code. This block used
# to say "restated rather than imported so that deleting one script cannot silently disarm the
# other" — which had it backwards. The inline copy named two subdirectories that were never
# extracted, so it failed OPEN and guarded nothing; a missing import fails CLOSED. The target
# is the whole metrics tree. PROTOCOL §10 as amended v1.8, DECISIONS.md 2026-08-06.
require_absent(INTERIM / "metrics")

# WorldPop 100 m, UN-adjusted, 2020, UNCONSTRAINED. One file per country, ISO3-keyed.
#
# Unconstrained is chosen deliberately over the constrained (maxar_v1) product, and the reason
# is central to this study rather than incidental. The constrained product distributes
# population only onto detected building footprints. Stratum 3 slices basins by OSM feature
# density. Using a settlement-derived population surface to weight a comparison against
# settlement mapping density would manufacture the very correlation the study is testing, and
# a referee would be right to throw it out. Unconstrained is modelled from census and
# covariates without that footprint dependency, so the weight and the stratum stay independent.
#
# It costs roughly 50x the bytes (Djibouti: 10.5 MB against 202 kB). Streaming makes that a
# bandwidth question rather than a disk one.
WORLDPOP_URL = ("https://data.worldpop.org/GIS/Population/Global_2000_2020/2020/"
                "{iso3}/{iso3_lower}_ppp_2020_UNadj.tif")
# GHS-POP R2023A, 100 m Mollweide, 2020, per Mollweide tile.
GHSPOP_TILE_URL = ("https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/"
                   "GHS_POP_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/"
                   "GHS_POP_E2020_GLOBE_R2023A_54009_100_V1_0_{tile}.zip")


def manifest(path, url, licence, notes):
    """Record a file before it is deleted. Provenance outlives the bytes."""
    subprocess.run([sys.executable, str(LIB / "manifest.py"), "QL-2026-01", str(path),
                    "--url", url, "--licence", licence, "--notes", notes, "--transient"], check=True)


def zonal_sum(raster_path, basins, id_col="HYBAS_ID"):
    """Sum raster values within each basin polygon.

    Population counts are per-pixel totals, so the correct zonal statistic is a sum, and
    nodata must be excluded rather than treated as zero — a basin of nodata is unknown, not
    empty. That distinction is the difference between 'nobody lives here' and 'we did not
    measure here', which is the same distinction this whole study is about.
    """
    out = {}
    with rasterio.open(raster_path) as src:
        bas = basins.to_crs(src.crs)
        nodata = src.nodata
        for hid, geom in zip(bas[id_col], bas.geometry):
            if geom is None or geom.is_empty:
                continue
            try:
                arr, _ = mask(src, [geom], crop=True, filled=True,
                              nodata=nodata if nodata is not None else -9999)
            except ValueError:
                continue                      # polygon outside raster extent
            a = arr[0].astype("float64")
            nd = nodata if nodata is not None else -9999
            valid = np.isfinite(a) & (a != nd)
            if not valid.any():
                continue
            out[hid] = float(np.clip(a[valid], 0, None).sum())
    return out


def african_iso3(basins_with_country):
    """ISO3 codes present in the basin frame.

    geoBoundaries carries a few non-ISO `shapeGroup` values (e.g. "111"). Filtering them
    here keeps a permanent "NO RASTER" line out of the completion report, where it would
    look like a real coverage gap rather than a junk code. The basins behind such codes are
    still counted as unassigned and reported.
    """
    codes = {c for c in basins_with_country["iso3"].dropna().unique() if c}
    return sorted(c for c in codes if len(c) == 3 and c.isalpha())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--surface", choices=["worldpop", "ghspop"], required=True)
    ap.add_argument("--countries", help="comma-separated ISO3 subset, for testing")
    ap.add_argument("--force", action="store_true", help="re-do countries already populated")
    ap.add_argument("--keep-rasters", action="store_true",
                    help="do not delete after summing (needs the disk)")
    a = ap.parse_args()

    geom = gpd.read_parquet(OUT / "basins_af_geom.parquet")
    attrs = pd.read_parquet(OUT / "basins_af.parquet")
    if "iso3" not in attrs.columns:
        sys.exit("run 03-harness/01b_assign_countries.py first — basins have no iso3 column")
    basins = geom.merge(attrs[["HYBAS_ID", "iso3"]], on="HYBAS_ID")

    if a.surface == "ghspop":
        sys.exit(
            "GHS-POP is not implemented yet — it ships as Mollweide tiles, not per-country\n"
            "rasters, so it needs its own tile-selection step. Failing loudly rather than\n"
            "silently summing WorldPop into the pop_ghspop column, which would make Gate E\n"
            "compare a surface against itself and report a spread of zero."
        )

    isos = a.countries.split(",") if a.countries else african_iso3(basins)
    print(f"{a.surface}: {len(isos)} countries, {len(basins):,} basins")
    SCRATCH.mkdir(parents=True, exist_ok=True)

    col = "pop_worldpop" if a.surface == "worldpop" else "pop_ghspop"
    if col not in attrs.columns:
        attrs[col] = pd.NA

    # Clear anything a previous killed run left behind, so a partial download is never
    # mistaken for a complete one.
    for stale in SCRATCH.glob("*.tif"):
        print(f"removing orphaned {stale.name} ({stale.stat().st_size:,} bytes)")
        stale.unlink()

    # Resume: a country whose basins already carry a population value is skipped. Makes the
    # run restartable after a kill without re-downloading gigabytes.
    done = set(attrs.loc[pd.to_numeric(attrs[col], errors="coerce").notna(), "iso3"].dropna())

    totals, failed = {}, []
    for i, iso in enumerate(isos, 1):
        sub = basins[basins["iso3"] == iso]
        if sub.empty:
            continue
        if iso in done and not a.force:
            print(f"[{i}/{len(isos)}] {iso}  already populated — skipping")
            continue
        url = WORLDPOP_URL.format(iso3=iso, iso3_lower=iso.lower())
        dest = SCRATCH / f"{iso}.tif"
        print(f"[{i}/{len(isos)}] {iso}  {len(sub):,} basins ... ", end="", flush=True)

        # Retry before giving up. A country dropped here is not a cosmetic gap: DR Congo is
        # 17,900 basins, and losing it to one dropped connection would bias the denominator
        # towards exactly the well-connected places this study is not about.
        ok = False
        for attempt in range(1, 4):
            r = subprocess.run(["curl", "-sSfL", "--retry", "2", "--retry-delay", "3",
                                "-C", "-", "-o", str(dest), url], capture_output=True)
            if r.returncode == 0 and dest.exists() and dest.stat().st_size > 0:
                ok = True
                break
            print(f"(attempt {attempt} failed) ", end="", flush=True)
            dest.unlink(missing_ok=True)      # never leave a fragment that looks complete
        if not ok:
            print("NO RASTER")
            failed.append(iso)
            continue

        manifest(dest, url, "CC BY 4.0",
                 f"WorldPop 100m UNadj UNCONSTRAINED 2020, {iso}. Summed into basins then deleted; "
                 f"hash recorded so the run reproduces without retaining the raster.")
        totals.update(zonal_sum(dest, sub))
        if not a.keep_rasters:
            dest.unlink(missing_ok=True)

        # Checkpoint after every country. The first version of this script wrote once at the
        # end and a kill during country 14 destroyed thirteen countries of work.
        new = attrs["HYBAS_ID"].map(totals)
        attrs[col] = new.combine_first(pd.to_numeric(attrs[col], errors="coerce"))
        attrs.to_parquet(OUT / "basins_af.parquet", index=False)
        print(f"ok  ({len(totals):,} basins this run, checkpointed)")

    covered = pd.to_numeric(attrs[col], errors="coerce").notna().sum()
    print(f"\n{col}: {covered:,} / {len(attrs):,} basins ({100*covered/len(attrs):.1f}%)")

    # A country missing from the population layer is not a cosmetic gap. It removes its
    # basins from every population-weighted figure, and the countries most likely to fail
    # are not a random sample. Report the size of what is missing, loudly.
    missing_basins = 0
    if failed:
        missing_basins = int(basins[basins["iso3"].isin(failed)]["HYBAS_ID"].nunique())
        print(f"\n*** {len(failed)} COUNTRIES WITHOUT A RASTER — {missing_basins:,} basins "
              f"({100*missing_basins/len(attrs):.1f}% of the study region) ***")
        print(f"    {failed}")
        print("    These basins are NA, not zero. Re-run to retry before using this layer;")
        print("    if any remain, they must be named in the limits box, not averaged over.")

    (OUT / f"{a.surface}_run.json").write_text(json.dumps(
        {"surface": a.surface, "countries": len(isos), "basins_populated": int(covered),
         "countries_without_raster": failed, "basins_missing": missing_basins,
         "complete": not failed}, indent=2))
    print("No metric value has been read.")


if __name__ == "__main__":
    main()
