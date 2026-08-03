"""Day-1 feasibility check for QL-2026-01.

One question: can per-gauge metrics be joined to coordinates and a country?

BLIND BY CONSTRUCTION. This script reads gauge *identifiers* and *locations* only. It never
opens a metric file and never reads a skill value. Which gauges carry a published metric is
established from filenames in the archive listing; what those metrics say is not established
here and must not be, because the strata this study will build are supposed to exist before
the outcome does.

    python3 03-harness/00_day1_join_check.py

Reads only 02-data/interim/ (extracted from the manifested archives in 02-data/raw/).
Writes nothing except stdout.
"""
import csv
import re
import subprocess
import sys
from pathlib import Path

STUDY = Path(__file__).resolve().parent.parent
INTERIM = STUDY / "02-data" / "interim"
RAW = STUDY / "02-data" / "raw"
META = INTERIM / "metadata"
GROUPS = INTERIM / "gauge_groups_for_paper" / "dual_lstm"

# The one line that keeps this honest. If a concatenated metric table is ever unpacked into
# the tree, this check must be re-read before it is trusted.
FORBIDDEN = re.compile(r"(precision|recall|per_gauge)/GRDC_\d+\.csv$")


def gauges_with_published_metrics():
    """Gauge IDs that have a per-gauge metric file, from the archive listing alone.

    `tar tzf` reads names, not contents. No metric value is decompressed.
    """
    out = subprocess.run(
        ["tar", "tzf", str(RAW / "metrics.tgz")],
        capture_output=True, text=True, check=True,
    ).stdout.splitlines()

    per_gauge = {}          # evaluation group -> set of gauge ids
    for name in out:
        if not FORBIDDEN.search(name):
            continue
        gid = Path(name).stem                       # GRDC_1234567
        group = str(Path(name).parent.parent)       # .../full_run, .../continent_splits
        per_gauge.setdefault(group, set()).add(gid)
    return per_gauge


def read_csv(path, key=None):
    with open(path, newline="", encoding="utf-8", errors="replace") as fh:
        rows = list(csv.DictReader(fh))
    return {r[key]: r for r in rows} if key else rows


def read_group(path):
    return {ln.strip() for ln in path.read_text().splitlines() if ln.strip()}


def main():
    print("=" * 72)
    print("QL-2026-01 day-1 join check")
    print("=" * 72)

    # ---- 1. which gauges have a published per-gauge metric --------------------------
    groups = gauges_with_published_metrics()
    print("\n[1] Per-gauge metric files, by evaluation group")
    for g, ids in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        print(f"    {len(ids):>6}  {g}")

    evaluated = set().union(*groups.values())
    print(f"\n    union of all groups: {len(evaluated):,} distinct gauge ids")

    # The paper's headline evaluation set.
    grdc_filtered = read_group(GROUPS / "grdc_filtered.txt")
    print(f"    grdc_filtered.txt:   {len(grdc_filtered):,} gauge ids")

    # ---- 2. can they be joined to a country? ----------------------------------------
    country = read_csv(META / "basin_county.csv", key="gauge_id")
    print(f"\n[2] basin_county.csv: {len(country):,} rows, gauge_id -> Country")
    hit = evaluated & set(country)
    print(f"    evaluated gauges with a country:  {len(hit):,} / {len(evaluated):,}"
          f"  ({100 * len(hit) / len(evaluated):.1f}%)")
    missing_country = evaluated - set(country)
    if missing_country:
        print(f"    UNMATCHED: {len(missing_country):,}  e.g. {sorted(missing_country)[:5]}")

    # ---- 3. can they be joined to coordinates? --------------------------------------
    stations = read_csv(META / "grdc_stations_20220320.csv", key="grdc_no")
    stations = {f"GRDC_{k}": v for k, v in stations.items()}
    print(f"\n[3] grdc_stations_20220320.csv: {len(stations):,} rows")

    matched = evaluated & set(stations)
    print(f"    evaluated gauges present:         {len(matched):,} / {len(evaluated):,}"
          f"  ({100 * len(matched) / len(evaluated):.1f}%)")

    def usable(gid):
        r = stations.get(gid)
        if not r:
            return False
        try:
            lat, lon = float(r["lat"]), float(r["long"])
        except (TypeError, ValueError):
            return False
        # A gauge at (0,0) is a null island artefact, not a gauge in the Gulf of Guinea.
        return -90 <= lat <= 90 and -180 <= lon <= 180 and not (lat == 0 and lon == 0)

    with_coords = {g for g in evaluated if usable(g)}
    print(f"    with usable lat/long:             {len(with_coords):,} / {len(evaluated):,}"
          f"  ({100 * len(with_coords) / len(evaluated):.1f}%)")

    full = with_coords & set(country)
    print(f"\n    JOINABLE (metric + coords + country): {len(full):,} / {len(evaluated):,}"
          f"  ({100 * len(full) / len(evaluated):.1f}%)")

    # ---- 4. does the join survive on the African subset? -----------------------------
    africa = read_group(GROUPS / "continent_splits" / "africa.txt")
    print(f"\n[4] continent_splits/africa.txt: {len(africa):,} gauge ids")
    af_eval = africa & evaluated
    af_full = africa & full
    print(f"    African gauges with a metric file:    {len(af_eval):,}")
    print(f"    African gauges fully joinable:        {len(af_full):,}"
          f"  ({100 * len(af_full) / len(af_eval):.1f}% of African evaluated)"
          if af_eval else "    no African gauges evaluated")

    countries = sorted((GROUPS / "country_splits").glob("*.txt"))
    print(f"\n    country_splits/: {len(countries)} countries")
    ng = read_group(GROUPS / "country_splits" / "nigeria.txt")
    print(f"    nigeria.txt: {len(ng)} gauges, {len(ng & evaluated)} with a metric file, "
          f"{len(ng & full)} fully joinable")

    # ---- 5. the other gauge table — is the deployment surface in here? ---------------
    hybas = read_csv(META / "hybas_gauges_info_lev12.csv")
    ids = {r["unique_gauge_id"] for r in hybas if r.get("unique_gauge_id")}
    print(f"\n[5] hybas_gauges_info_lev12.csv: {len(hybas):,} rows, {len(ids):,} unique gauge ids")
    by_cont = {}
    for r in hybas:
        by_cont[r.get("continent") or "(blank)"] = by_cont.get(r.get("continent") or "(blank)", 0) + 1
    for c, n in sorted(by_cont.items(), key=lambda kv: -kv[1]):
        print(f"    {n:>7}  {c}")
    grdc_like = {i for i in ids if i.startswith("GRDC_")}
    print(f"    of which GRDC_*: {len(grdc_like):,}")
    print(f"    overlap with evaluated gauges: {len(grdc_like & evaluated):,}")
    print(f"    NOT evaluated: {len(ids) - len(grdc_like & evaluated):,}")

    # ---- verdict --------------------------------------------------------------------
    print("\n" + "=" * 72)
    rate = 100 * len(full) / len(evaluated)
    af_rate = 100 * len(af_full) / len(af_eval) if af_eval else 0
    verdict = "PASS" if rate >= 90 and af_rate >= 90 else "REVIEW"
    print(f"VERDICT: {verdict} — {rate:.1f}% globally, {af_rate:.1f}% Africa")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
