"""Attach GHS-POP population to the basin frame — the second surface Gate E requires.

BLIND. No metric value is read.

WHY A SECOND SURFACE AT ALL. PROTOCOL §9 forbids putting a confidence interval on a
population share, because the uncertainty there is model error in the population surface, not
sampling error. Gate E replaces the interval with something honest: run the primary metric on
two independently constructed surfaces and report the spread. WorldPop and GHS-POP disagree
most in sparsely mapped Africa, which is exactly where this study looks — so the spread is the
uncertainty, and either figure alone would be false precision.

WHY THIS IS A SEPARATE SCRIPT FROM 02_. GHS-POP ships as Mollweide (ESRI:54009) tiles on a
1,000,000 m grid, not as per-country rasters. A basin can straddle two tiles, so contributions
must be **accumulated** across tiles rather than assigned — getting that wrong would silently
truncate every basin on a tile boundary.

    python3 03-harness/02b_add_ghspop.py
    python3 03-harness/02b_add_ghspop.py --tiles R9_C20,R9_C21

Streams like its siblings: download, sum, manifest, delete.
"""
import argparse
import json
import subprocess
import sys
import zipfile
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
SCRATCH = INTERIM / "_scratch_ghs"

sys.path.insert(0, str(LIB))
from blind import require_absent          # noqa: E402 — path must be set before the import

# Structural blinding, PROTOCOL §10 as amended in v1.8: the shared helper, and the whole
# metrics tree rather than named subdirectories inside it. See DECISIONS.md 2026-08-06.
require_absent(INTERIM / "metrics")

BASE = ("https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/"
        "GHS_POP_E2020_GLOBE_R2023A_54009_100/V1-0/tiles/"
        "GHS_POP_E2020_GLOBE_R2023A_54009_100_V1_0_{tile}.zip")

# GHSL R2023A global Mollweide grid: 1,000,000 m tiles, R1..R18 north to south,
# C1..C36 west to east. Derived from the basin extent in 02b's companion probe; the range
# below covers the African continent with a margin.
ROWS = range(5, 15)
COLS = range(17, 25)
MOLLWEIDE = "ESRI:54009"


def manifest(path, url, notes):
    subprocess.run([sys.executable, str(LIB / "manifest.py"), "QL-2026-01", str(path),
                    "--url", url, "--licence", "CC BY 4.0", "--notes", notes,
                    "--transient"], check=True)


def sum_tile(tif_path, basins_moll, acc):
    """Add this tile's population into `acc`, keyed by HYBAS_ID.

    Accumulates rather than assigns: a basin straddling a tile edge gets a partial sum from
    each tile, and the total is only correct if they are added. Nodata is excluded, never
    treated as zero.
    """
    with rasterio.open(tif_path) as src:
        left, bottom, right, top = src.bounds
        # Only basins intersecting this tile need masking — the rest would just raise.
        cand = basins_moll.cx[left:right, bottom:top]
        nd = src.nodata
        for hid, geom in zip(cand["HYBAS_ID"], cand.geometry):
            if geom is None or geom.is_empty:
                continue
            try:
                arr, _ = mask(src, [geom], crop=True, filled=True,
                              nodata=nd if nd is not None else -200)
            except ValueError:
                continue
            a = arr[0].astype("float64")
            ndv = nd if nd is not None else -200
            valid = np.isfinite(a) & (a != ndv)
            if not valid.any():
                continue
            acc[hid] = acc.get(hid, 0.0) + float(np.clip(a[valid], 0, None).sum())
    return acc


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tiles", help="comma-separated tile ids, e.g. R9_C20")
    a = ap.parse_args()

    geom = gpd.read_parquet(OUT / "basins_af_geom.parquet")
    attrs = pd.read_parquet(OUT / "basins_af.parquet")
    print(f"reprojecting {len(geom):,} basins to Mollweide ...")
    basins_moll = geom.to_crs(MOLLWEIDE)

    tiles = a.tiles.split(",") if a.tiles else [f"R{r}_C{c}" for r in ROWS for c in COLS]
    print(f"{len(tiles)} candidate tiles")
    SCRATCH.mkdir(parents=True, exist_ok=True)
    for stale in SCRATCH.iterdir():
        stale.unlink()

    acc, got, absent = {}, 0, []
    for i, tile in enumerate(tiles, 1):
        url = BASE.format(tile=tile)
        dest = SCRATCH / f"{tile}.zip"
        print(f"[{i}/{len(tiles)}] {tile} ... ", end="", flush=True)
        ok = False
        for _ in range(3):
            r = subprocess.run(["curl", "-sSfL", "--retry", "2", "--retry-delay", "3",
                                "-o", str(dest), url], capture_output=True)
            if r.returncode == 0 and dest.exists() and dest.stat().st_size > 0:
                ok = True
                break
            dest.unlink(missing_ok=True)
        if not ok:
            # Most absent tiles are open ocean and have no data by construction. Recorded
            # so the distinction between "ocean" and "we failed to fetch it" is visible.
            print("absent")
            absent.append(tile)
            continue

        manifest(dest, url, f"GHS-POP R2023A 100m Mollweide tile {tile}, epoch 2020. "
                            f"Summed into basins then deleted.")
        try:
            with zipfile.ZipFile(dest) as z:
                tif = next(n for n in z.namelist() if n.endswith(".tif"))
                z.extract(tif, SCRATCH)
            before = len(acc)
            sum_tile(SCRATCH / tif, basins_moll, acc)
            (SCRATCH / tif).unlink(missing_ok=True)
            print(f"ok  (+{len(acc) - before:,} basins, {len(acc):,} total)")
        except Exception as e:                       # noqa: BLE001
            print(f"FAILED: {e}")
            absent.append(tile)
        finally:
            dest.unlink(missing_ok=True)

    attrs["pop_ghspop"] = attrs["HYBAS_ID"].map(acc)
    attrs.to_parquet(OUT / "basins_af.parquet", index=False)

    ghs = pd.to_numeric(attrs["pop_ghspop"], errors="coerce")
    wp = pd.to_numeric(attrs["pop_worldpop"], errors="coerce")
    print(f"\npop_ghspop: {int(ghs.notna().sum()):,} / {len(attrs):,} basins")
    print(f"total GHS-POP  : {ghs.sum():,.0f}")
    print(f"total WorldPop : {wp.sum():,.0f}")
    if wp.sum():
        print(f"continental difference: {100*(ghs.sum()-wp.sum())/wp.sum():+.1f}%")

    (OUT / "ghspop_run.json").write_text(json.dumps(
        {"tiles_requested": len(tiles), "tiles_absent": absent,
         "basins_populated": int(ghs.notna().sum()),
         "total_ghspop": float(ghs.sum()), "total_worldpop": float(wp.sum())}, indent=2))
    print("\nGate E can now be computed. No metric value has been read.")


if __name__ == "__main__":
    main()
