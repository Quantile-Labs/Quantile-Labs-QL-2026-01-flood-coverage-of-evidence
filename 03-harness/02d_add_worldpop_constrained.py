"""Third population surface, WorldPop constrained, for the headline only.

POST-HOC. Added 2026-08-20 after an operator adversarial self-review, under PROTOCOL §11a.
Not pre-registered, and it does not replace either surface that was.

    python3 03-harness/02d_add_worldpop_constrained.py
    python3 03-harness/02d_add_worldpop_constrained.py --countries DJI,GMB

WHAT THIS MAY BE USED FOR, AND WHAT IT MAY NOT.

The referee objection is that WorldPop unconstrained distributes census counts by covariates
with no built-up mask, so it places people on land nobody lives on, and that this bites hardest
in the sparsest basins. That is a fair objection to the headline and it is answerable by adding
a surface that does carry a built-up mask.

It is not a fair objection to the mapping-density tercile table, and answering it there would
break the study. The constrained product puts population onto detected building footprints.
Stratum 3 cuts basins by OSM feature density, which is settlement mapping. Weighting one by the
other manufactures the correlation the study exists to test, which is why unconstrained was
chosen on 2026-08-04 in `02_add_population.py` and why that choice still stands. §11a makes the
prohibition binding: this column feeds P_unevidenced and nothing else, and never a figure or a
sentence that crosses population with mapping density.

WHY THIS WRITES ITS OWN FILE INSTEAD OF A COLUMN IN THE BASIN FRAME.

`basins_af.parquet` was built blind, before any metric value was read, and that is most of what
makes it worth anything. Adding a post-hoc column to it after unblinding would leave the
provenance of the file needing a paragraph of explanation for every later reader. A separate
CSV costs one join in the analysis and keeps the blind artefact exactly as the blind phase left
it.
"""
import argparse
import subprocess
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

STUDY = Path(__file__).resolve().parent.parent
LIB = STUDY / "_lib"
INTERIM = STUDY / "02-data" / "interim"
OUT = INTERIM / "strata"
SCRATCH = INTERIM / "_scratch_raster"
DEST_CSV = OUT / "pop_worldpop_constrained.csv"

sys.path.insert(0, str(LIB))
from blind import require_absent          # noqa: E402 — path must be set before the import

require_absent(INTERIM / "metrics")

sys.path.insert(0, str(STUDY / "03-harness"))
_pop = __import__("02_add_population")    # reuse zonal_sum and african_iso3 rather than fork them
zonal_sum, african_iso3 = _pop.zonal_sum, _pop.african_iso3

# Two publication routes exist for the constrained product and neither covers every country.
# maxar_v1 is tried first because it is the one WorldPop documents as current; BSGM is the
# older building-settlement-growth route and covers some countries maxar does not. A country
# served by neither is reported as a gap rather than silently dropped, because a missing
# country in a population denominator is exactly the kind of hole this study is about.
URLS = [
    ("maxar_v1", "https://data.worldpop.org/GIS/Population/Global_2000_2020_Constrained/2020/"
                 "maxar_v1/{iso3}/{iso3_lower}_ppp_2020_UNadj_constrained.tif"),
    ("BSGM", "https://data.worldpop.org/GIS/Population/Global_2000_2020_Constrained/2020/"
             "BSGM/{iso3}/{iso3_lower}_ppp_2020_UNadj_constrained.tif"),
]


def manifest(path, url, notes):
    subprocess.run([sys.executable, str(LIB / "manifest.py"), "QL-2026-01", str(path),
                    "--url", url, "--licence", "CC BY 4.0", "--notes", notes, "--transient"],
                   check=True)


def fetch(iso, dest):
    """Return the route that worked, or None. Fragments are removed, never left behind."""
    for route, tpl in URLS:
        url = tpl.format(iso3=iso, iso3_lower=iso.lower())
        for _ in range(3):
            r = subprocess.run(["curl", "-sSfL", "--retry", "2", "--retry-delay", "3",
                                "-o", str(dest), url], capture_output=True)
            if r.returncode == 0 and dest.exists() and dest.stat().st_size > 0:
                return route, url
            dest.unlink(missing_ok=True)
    return None, None


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--countries", help="comma-separated ISO3 subset, for testing")
    a = ap.parse_args()

    geom = gpd.read_parquet(OUT / "basins_af_geom.parquet")
    attrs = pd.read_parquet(OUT / "basins_af.parquet")
    basins = geom.merge(attrs[["HYBAS_ID", "iso3"]], on="HYBAS_ID")

    isos = a.countries.split(",") if a.countries else african_iso3(basins)
    print(f"worldpop constrained: {len(isos)} countries, {len(basins):,} basins")
    SCRATCH.mkdir(parents=True, exist_ok=True)

    have = {}
    if DEST_CSV.exists():
        prev = pd.read_csv(DEST_CSV)
        have = dict(zip(prev["HYBAS_ID"], prev["pop_worldpop_constrained"]))
        done = set(prev["iso3"].dropna())
        print(f"resuming: {len(done)} countries already summed, {len(have):,} basins")
    else:
        done = set()

    iso_of = dict(zip(basins["HYBAS_ID"], basins["iso3"]))
    routes, failed = {}, []
    for i, iso in enumerate(isos, 1):
        sub = basins[basins["iso3"] == iso]
        if sub.empty or iso in done:
            continue
        dest = SCRATCH / f"{iso}_constrained.tif"
        print(f"[{i}/{len(isos)}] {iso}  {len(sub):,} basins ... ", end="", flush=True)
        route, url = fetch(iso, dest)
        if route is None:
            print("NO RASTER")
            failed.append(iso)
            continue
        manifest(dest, url, f"WorldPop 100m UNadj CONSTRAINED 2020 ({route}), {iso}. Post-hoc "
                            f"third surface under PROTOCOL 11a, headline only. Summed into "
                            f"basins then deleted; hash recorded so the run reproduces.")
        have.update(zonal_sum(dest, sub))
        dest.unlink(missing_ok=True)
        routes[iso] = route
        done.add(iso)

        # Checkpoint per country, same reason as the unconstrained run: a kill part way through
        # must not cost the countries already summed.
        rows = pd.DataFrame({"HYBAS_ID": list(have.keys()),
                             "pop_worldpop_constrained": list(have.values())})
        rows["iso3"] = rows["HYBAS_ID"].map(iso_of)
        rows.to_csv(DEST_CSV, index=False)
        print(f"ok  ({route}, {len(have):,} basins so far)")

    print(f"\nbasins with a constrained value: {len(have):,} of {len(basins):,}")
    if failed:
        print(f"no constrained raster published for {len(failed)} countries: {','.join(failed)}")
        print("These are reported as a coverage gap in the sensitivity, not dropped silently.")


if __name__ == "__main__":
    main()
