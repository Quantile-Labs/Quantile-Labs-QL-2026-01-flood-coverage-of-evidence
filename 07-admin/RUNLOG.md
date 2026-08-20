# Run log — QL-2026-01

**Append only.** One row per execution of anything in `03-harness/` or `04-analysis/`.

`blind?` — `blind` (outcome absent or permuted) or `UNBLINDED`.
The unblinding row is the important one: it records the single authorised run against real
outcomes. A re-run after a post-unblinding bug fix gets its own row with the reason.

> **Rows marked ⟲ were reconstructed on 2026-08-06, not written at run time.** Between
> 2026-08-04 and 2026-08-05 nine executions were logged in `DECISIONS.md` but never entered
> here, and the omission was not noticed until the frame was reviewed. They are reconstructed
> from three independent contemporaneous records — `MANIFEST.csv` acquisition timestamps, git
> commit times and blob hashes, and output-file mtimes — and each row states which of those
> supplied its timestamp.
>
> **A reconstructed row is weaker evidence than a contemporaneous one and is not presented as
> equivalent.** What is solid: which script version ran, when, on which inputs, and what it
> produced. What is *not* recoverable is the intermediate `basins_af.parquet` hash at each
> run's start — the file is mutated in place, so every run overwrote the previous state before
> anyone hashed it. Those cells say so rather than being left blank. From 2026-08-06 the row
> is written when the run starts, not afterwards.

| UTC | Script | Git SHA | Inputs (sha256 prefix) | blind? | Outputs | Notes |
|---|---|---|---|---|---|---|
| 2026-08-03T20:02:01Z | `03-harness/00_day1_join_check.py` | c88d5c6 (script uncommitted at run time; committed this session, file sha256 `5d464eedf9b1`) | metrics.tgz `237559b9abbe` · metadata.tgz `59c6b8310d17` · gauge_groups_for_paper.tgz `a72a2b777ef3` | blind | stdout only — no file written | Day-1 feasibility. Reads gauge identifiers and coordinates only; opens no metric file and reads no skill value. Result: 5,678/5,678 joinable globally, 741/741 Africa. |
| ⟲ 2026-08-04T21:52:07Z | `03-harness/01_build_strata.py` | f9d9e3c, file sha256 `c3e8808f5bdf`. Script mtime 21:51:58Z, committed 22:00:47Z — run then committed, unmodified since | hybas_af_lev12_v1c.shp `33524f6e6424` · metadata.tgz `59c6b8310d17` · gauge_groups_for_paper.tgz `a72a2b777ef3` | blind | `basins_af.parquet` · `basins_af_geom.parquet` · `points_assigned.csv` · `gate_c.json` · `ladder.json` | Strata frame: 230,028 African level-12 basins, strata 1 and 5 cut, population/OSM columns created empty. **Gate C PASS** — 6,772/6,772 points assign (100%). Blinding assert armed and passed. Timestamp from output mtime. |
| ⟲ 2026-08-04T21:57:27Z | `03-harness/01b_assign_countries.py` | f9d9e3c, file sha256 `0681be2d7dc3`. Script mtime 21:57:15Z | geoBoundariesCGAZ_ADM0.gpkg `6bdeb27072cf` · `basins_af.parquet` (hash at run time not captured — see note above) | blind | `basins_af.parquet` (+`iso3`, `in_study_region`, `country_developer`) · `rung3_definitions.json` | Country stratum by geometry, plus the developer-vs-boundary disagreement count PROTOCOL §4 requires. 229,744 basins in the study region. Timestamp from `rung3_definitions.json` mtime. |
| ⟲ 2026-08-04T21:59:27Z → 22:48:35Z | `03-harness/02_add_population.py --surface worldpop` | f9d9e3c, file sha256 `3ee95a954584` — the pre-fix version | 13 WorldPop rasters, manifested transient, first `AGO` 21:59:27Z, last 22:48:35Z | blind | **none retained — the run's work was destroyed** | **FAILED RUN, logged rather than omitted.** Killed during country 14. This version wrote the parquet once at the end, so 13 countries / 30,495 basins of completed zonal sums were lost. Bug and fix (checkpoint after every country) logged in DECISIONS.md 2026-08-05. Window from manifest acquisition timestamps. |
| ⟲ 2026-08-05T07:02:05Z → 07:04:30Z | `03-harness/03_add_osm.py --countries TCD` (two invocations) | eb86bb7 `7e236c7da040` at start; three bugs fixed in **uncommitted** edits during the test, committed 07:35:50Z as 4ea8263 `60448e521987` | chad.shp.zip `e22ed9f4a3cd`, Geofabrik snapshot 260803 | blind | `basins_af.parquet` (Chad only) · `osm_run.json` | Harness test on one country. Found the zero-vs-unprocessed conflation, the 52.2%-zero tercile deviation, and the 95.1/4.9 building-to-road mix. **The intermediate script states between the two invocations were never committed and cannot be reproduced exactly** — the recorded endpoints bracket them. Window from manifest timestamps. |
| ⟲ 2026-08-05T07:47:41Z → 10:36:55Z | `03-harness/02_add_population.py --surface worldpop` | bdbd1ae, file sha256 `52ca5c8fb866` | 35 WorldPop rasters, manifested transient | blind | `basins_af.parquet` (`pop_worldpop`) · `worldpop_run.json` | Main WorldPop run, now checkpointed per country. **DR Congo failed silently** — 1.04 GB file, dropped connection, 97 MB fragment left behind, 17,900 basins (7.8% of the study region) marked "no raster". Caught by the completion report, not by the run itself. Window from manifest timestamps. |
| ⟲ 2026-08-05T11:07:12Z → 12:15:25Z | `03-harness/02_add_population.py --surface worldpop` | bdbd1ae, file sha256 `52ca5c8fb866` (unchanged from the previous row; the script was edited at 12:16:39Z, *after* this run finished) | 21 WorldPop rasters, manifested transient — 58 distinct countries across all three invocations | blind | `basins_af.parquet` · `worldpop_run.json` | Retry run. DR Congo recovered, 17,735 of 17,900 basins. **Layer complete: 228,344 / 230,028 basins (99.3%), 1,322,374,091 people.** The one entry in `countries_without_raster` is the junk geoBoundaries code `"111"`, not a country. Window from manifest timestamps; `worldpop_run.json` mtime 12:15:27Z. |
| ⟲ 2026-08-05T12:18:17Z → 13:17:16Z | `03-harness/03_add_osm.py` | bdbd1ae, file sha256 `b250c4187047` — **no retry logic in this version** | 50 Geofabrik country extracts, snapshot 260803, manifested transient | blind | `basins_af.parquet` (`osm_feature_count`, `osm_feature_density`, `osm_density_tercile`) · `osm_run.json` | Continent-wide run. **Lesotho dropped** on a transient failure while its file was present and served fine later — the population harness had retry logic and this one did not. Window from manifest timestamps. |
| ⟲ 2026-08-05T13:20:01Z | `03-harness/03_add_osm.py --countries LSO` | d45db0a, file sha256 `366cfad496b6`; retry logic added at 13:19:53Z, eight seconds before this run | lesotho.shp.zip `3ecd619a74f6` | blind | `basins_af.parquet` · `osm_run.json` | Lesotho recovered. **Stratum 3 complete: 229,744 / 230,028 (99.9%); within Africa, complete.** ⚠ **This single-country run overwrote `osm_run.json`**, which now reports `extracts: 1, countries_processed: ["LSO"]` — the continent-wide totals (39.3% zero-feature basins, 86.4/13.6 feature mix) survive only in DECISIONS.md. The file is a run report, not a layer summary, and should not be cited as one. |
| ⟲ 2026-08-05T14:44:47Z → 15:14:49Z | `03-harness/02b_add_ghspop.py` | 3b009d3, file sha256 `20d186e7d426`. Script mtime 14:44:07Z, committed 15:19:35Z | 63 distinct GHS-POP R2023A Mollweide tiles (65 fetches — `R9_C20` and `R9_C21` twice), manifested transient | blind | `basins_af.parquet` (`pop_ghspop`) · `ghspop_run.json` | 211,932 basins, 1,273,594,049 people, −3.7% against WorldPop continentally. 80 tiles requested, 17 absent by construction (open ocean), **0 fetch failures** — the absent/failed distinction kept separate so an ocean tile cannot hide a dropped download. Basins carrying both surfaces: 210,547. This run produced the Gate E non-independence finding. Window from manifest timestamps. |
| 2026-08-06T09:11:51Z | `03-harness/02c_add_pop_band.py` | uncommitted at run time, file sha256 `9991808879b4` | `basins_af.parquet` `e9cee1979886` (hashed immediately before the run) | blind | `basins_af.parquet` `2239bf9eab0b` · `pop_band_run.json` | Stratum 4, the last blind stratum. Bands cut on WorldPop unconstrained per PROTOCOL §8, left-closed/right-open; `pop_band_ghspop` written alongside as a **declared sensitivity, not an alternative**. 228,344 basins banded, 1,684 left NA rather than `<10k`. First row written with input and output hashes captured at run time. Ran under the **old, narrower blinding guard**; the guard was widened later the same day after it was found inert (DECISIONS.md 2026-08-06) and this script now refuses until the metrics tree is moved. Output unaffected — it reads only the basin frame. |

| 2026-08-07 → 2026-08-08 | `04-analysis/01_evidence.py --permute 20260806` | dry-run development across 61baf57..a1dc7de; final state `2a6c86df1560` | metrics.tgz `237559b9abbe` · basins_af.parquet · points_assigned.csv | **blind, permuted** | `basins_evidence.permuted-20260806.parquet` · `points_evidence.permuted-20260806.csv` · `evidence_summary.permuted-20260806.json` | Permuted development per PROTOCOL §10. Gauge-to-record association scrambled, seed 20260806. Outputs gitignored so a machinery test cannot be mistaken for a result. Final invocation 2026-08-08T07:17:58Z. |
| 2026-08-07 → 2026-08-08 | `04-analysis/02_primary.py --permute 20260806` | dry-run development across 61baf57..a1dc7de; final state `ea47288b738b` | `basins_evidence.permuted-20260806.parquet` | **blind, permuted** | `primary.permuted-20260806.json` · `country_table.permuted-20260806.csv` | Found Gate F mis-specified, the tercile gradient present under permutation, and the `[77.5%, 100%]` structural floor. All three logged in DECISIONS.md and three became protocol v1.9 amendments. Final invocation 2026-08-08T07:17:58Z. |
| 2026-08-08T07:18:14Z | `04-analysis/03_q4_skill.py --permute 20260806` | a1dc7de, file sha256 `3349ab0b7201` | metrics.tgz `237559b9abbe` · basins_af.parquet · points_assigned.csv | **blind, permuted** | `q4_skill.permuted-20260806.json` | Q4 across six experiment-year combinations plus the window sensitivity. Validated the population weighting: unweighted 0.4400 against population-weighted 0.4220 under permutation, which is the correct null. |

> **On the granularity of the three rows above.** Permuted development is iterative by design and
> each of those scripts was invoked repeatedly while being written. What is logged is the
> **permuted run of record** for each, the invocation whose outputs stand, with the commit range
> the development spanned. Individual intermediate invocations were not logged. This is a
> deliberate reading of "one row per execution" for blind development rather than an oversight,
> and it is recorded here so it is visible as a choice. **It does not extend to the authorised
> run**, which gets a row per invocation with no exceptions.

| 2026-08-12T22:38:45Z | `04-analysis/01_evidence.py --unblind` | 884db25, file sha256 `2a6c86df1560` | metrics.tgz `237559b9abbe` · basins_af.parquet · points_assigned.csv | **UNBLINDED** | `basins_evidence.parquet` `60dea4460ee1` · `points_evidence.csv` `97d4b3041bc4` · `evidence_summary.json` `e761fdb95b07` | **The single authorised run.** All 7 preconditions passed. 3,378 of 5,678 gauges evidenced globally; 2,300 file-present-but-all-null; **242 of 741 African gauges with a metric file are evidenced**. Marker written to `07-admin/UNBLINDED.json`. |
| 2026-08-12T22:39:—Z | `04-analysis/02_primary.py --unblind` | 884db25, file sha256 `ea47288b738b` | `basins_evidence.parquet` `60dea4460ee1` | **UNBLINDED** | `primary.json` `1d09322b25be` · `country_table.csv` `f498267f3260` | **P_unevidenced = 92.4%** on WorldPop under the frozen generous definition. Gate D 1.6 pp, headline permitted. Gate E 0.4 pp, within tolerance. Gate F 0.3 pp, **H0 stands**. |
| 2026-08-12T22:40:—Z | `04-analysis/03_q4_skill.py --unblind` | 884db25, file sha256 `3349ab0b7201` | metrics.tgz `237559b9abbe` · basins_af.parquet · points_assigned.csv | **UNBLINDED** | `q4_skill.json` `c538ddb0e1bb` | Q4 across six experiment-year combinations plus the window sensitivity. No experiment designated the headline. |


> **Rows marked ✎ were written at the end of the session on 2026-08-20, not when the run
> started.** Timestamps are the output files' own mtimes and the git SHA is the commit the
> scripts were committed at, so what the rows record is solid. What they are not is
> contemporaneous, which is the third time this has happened and the reason the enforcement
> question in `DECISIONS.md` is still open. It was not decided unilaterally here, because
> having the scripts append their own rows changes what this log is.

| ✎ 2026-08-20T21:38:36Z | `03-harness/02d_add_worldpop_constrained.py` | 5ba8740 (run before commit; file sha256 `84303dd685e6`) | basins_af_geom.parquet · basins_af.parquet · 51 WorldPop constrained country rasters, each hashed into MANIFEST.csv on arrival and deleted | blind (no metric value read) | `02-data/interim/strata/pop_worldpop_constrained.csv` `88b9dd5647fc` | Post-hoc third population surface, PROTOCOL §11a. Headline only, forbidden in stratum 3. Writes its own file rather than a column in the blind-built basin frame. |
| ✎ 2026-08-20T21:39:20Z | `04-analysis/05_post_review.py` | 5ba8740 (run before commit; file sha256 `6a48af6e6587`) | `points_evidence.csv` · basins_af.parquet · `pop_worldpop_constrained.csv` · metrics.tgz `237559b9abbe` (member names and container structure only, no value read) | post-unblinding, and it reads no metric value | `05-results/post_review.json` `f86624c5ac39` | The five post-hoc additions under PROTOCOL §11a. Deliberately adds no row to `UNBLINDED.json`: the single shot was spent once, on 2026-08-12, and the marker should say that and nothing else. |

## Unblinding record

- **Date (UTC):** 2026-08-12T22:38:45Z
- **Frozen analysis SHA:** `884db25a1ac55451b51949ca46ff07aac7aa8ceb`
- **Protocol hash at time of run:** `b05c0b932ddb9c6db2f192ff5804570197470175e50ed21ce7520839321d2248` (v1.9,
  tag `QL-2026-01-protocol-v1.9`, anchored in Bitcoin and at Zenodo `10.5281/zenodo.21843331`
  before the run)
- **Authorised by:** Quantile Labs
- **Preconditions:** 7 of 7 passed, checked immediately before the run and recorded in
  `04-analysis/_metrics_io.py --check`
- **Prior blind development:** the full pipeline was built and exercised against permuted
  labels (seed 20260806) across 2026-08-07 and 2026-08-08, per §10. Three defects were found
  and fixed while blind, three of which became protocol v1.9 amendments.
- **Post-unblinding changes:** two, both on 2026-08-20, neither touching the primary metric.
  `03-harness/02d_add_worldpop_constrained.py` and `04-analysis/05_post_review.py` were added
  under protocol §11a after an adversarial self-review of the draft, and protocol v1.10 records
  what they are and what they may not be used for. **No script in the pre-registered pipeline
  was modified and none was re-run**, so `primary.json`, `q4_skill.json`, `evidence_summary.json`
  and `country_table.csv` are byte for byte what the authorised run produced.
