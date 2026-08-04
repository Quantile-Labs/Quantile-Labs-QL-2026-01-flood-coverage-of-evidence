# Protocol — QL-2026-01 Coverage of evidence: Google Flood Hub

**Version:** 1.0
**Drafted:** 2026-08-03 · **Frozen:** 2026-08-04
**Timestamp / hash:** see `PROTOCOL.sha256`, and the signed tag
`QL-2026-01-protocol-v1.0`. Re-hash this file and compare.
**Status:** locked

> Amendments are **appended** to §11, never made by editing the text above. A protocol whose
> history is editable is not a pre-registration.

Written after the day-1 join check (2026-08-03, `07-admin/RUNLOG.md`) and before any metric
value has been read. What that check established: gauge identifiers, coordinates and countries.
What it did not establish, deliberately: anything about skill. The definitions below are
therefore set in ignorance of the numbers they will produce, which is the only condition under
which they are worth anything.

## 1. Subject and version under test

**Subject:** Google Flood Hub, the public river flood forecasting service, and the per-gauge
evaluation artefacts released alongside Nearing, Cohen, Dube et al., *Global prediction of
extreme floods in ungauged watersheds*, Nature **627**:559–563 (2024).

**Artefacts under analysis:** Zenodo `10.5281/zenodo.10397664`, CC BY 4.0, files dated
26 October 2023 — `metrics.tgz` (sha256 `237559b9abbe…`), `metadata.tgz` (`59c6b8310d17…`),
`gauge_groups_for_paper.tgz` (`a72a2b777ef3…`). Full rows in `02-data/manifests/MANIFEST.csv`.

**Version statement, and its limit.** These artefacts describe the model of the 2024 Nature
paper. A v2 exists — Cohen, Amira, Aschner et al., *Extending Medium-Range Global Flood
Forecasts: Google Global Flood Forecasting Model Version 2*, EGUsphere 2026-2283, posted
29 April 2026 (ME-LSTM, Caravan training expanded 5,680 → 15,923 gauges, GraphCast forcings),
which does not report Africa separately and whose open review was stopped on a code-archiving
policy breach (CEC1, 8 June 2026).

**We have not established which version serves Flood Hub as of 2026-08-03, and the Note will say
so in those words rather than assume.** Every claim in this study is date-stamped to the 2024
release. No claim is made about what v2 does or does not evaluate. If the serving version
becomes establishable from a primary source before publication, that is recorded as an amendment
under §11 and the framing adjusted; it changes no definition below.

## 2. Access tier

**Black box, and in fact stricter: no system is queried at all.** This is a reanalysis of
published artefacts. The Flood Hub API is not called — it serves no historical forecasts and its
terms are non-commercial. The trained models (`trained-models.tgz`) and model data
(`model_data.tgz`) are on Zenodo and are deliberately not downloaded.

**Claims this tier forecloses, and which therefore may not appear in the Note at any strength:**

- that the model is accurate, or inaccurate, at any point without a published metric
- any statement of *why* the evaluation set falls where it does — that is mechanism, and
  mechanism is unavailable without access we do not have and did not seek
- any inference from a gauge's published metric to the forecast quality experienced by a person
  living near it

**The line this study holds:** *absence of a published metric is not evidence of poor skill.*
It appears in bold in the limits box, and the red-team pass in `06-report/RED-TEAM.md` is
instructed to hunt for sentences that violate it.

## 3. Question and hypotheses

**Question, stated so it can be falsified:**

> Among people living in reach of a Google Flood Hub river forecast point in Africa, what
> proportion live in reach only of points for which no per-gauge skill metric has been
> published?

**H0:** population-weighted evidence coverage does not differ materially from gauge-count
evidence coverage — the published evaluation set is distributed with respect to population no
differently from the forecast network as a whole.

**H1:** the two differ. **Direction is not predicted.** The evaluation set may be concentrated
where people are, in which case coverage weighted by population is *better* than the per-gauge
count suggests. That is a finding and it is published as one.

**What would falsify our expectation:** we hold no expectation to falsify, and this is load
bearing. If ≥ 90% of the in-reach African population lives in an evidenced basin, the Note's
headline is that the published evidence base tracks population well, and it says so without
hedging, at the same length and prominence as the opposite result. Q4 is included precisely
because its direction is genuinely unknown: a gauge protecting two million people and one
protecting two thousand count equally in the paper's per-gauge distributions, and reweighting
can move the number either way.

**What this study is not.** It is not a rebuttal of the Nature paper. That paper discloses
Africa F1 of 0.15–0.21 at the 5-year return period itself, and states its scope explicitly —
riverine only, no claim for pluvial, flash or dam-related flooding. The gap this Note addresses
sits between that disclosure and the deployment surface. The Note's first paragraph says so.

## 4. Unit of analysis

**The row is a HydroBASINS level-12 basin** within the study region.

Chosen because it is the developer's own spatial unit — `metadata/hybas_gauges_info_lev12.csv`
associates each gauge with a level-12 `HYBAS_ID` — so "in reach" is defined by the subject's own
geometry rather than by a radius we invent. Population is summed over basin polygons; each basin
carries a count of forecast points and a count of evidenced forecast points.

Two secondary unit sets, both pre-specified: the **gauge** (for comparability with how the paper
counts) and the **country** (for the reporting table).

**Study region:** the African continent. Gauge membership uses the developer's own
`continent_splits/africa.txt` and `country_splits/`; population and boundaries use
GADM/geoBoundaries African countries. Where the two disagree about a gauge's country, the
developer's assignment governs for evidence counting and the boundary file governs for
population, and every such disagreement is counted and reported rather than resolved silently.

## 5. Metrics

### Primary metric — one

**P_unevidenced** — the proportion of the study-region population living in reach of at least one
forecast point, that lives in reach of **no** evidenced forecast point.

    numerator   = population in basins with ≥1 forecast point and 0 evidenced forecast points
    denominator = population in basins with ≥1 forecast point

Reported as a percentage with its denominator on the chart, never bare. The denominator is
*population in reach*, not total African population: people with no forecast point near them at
all are a different question, reported separately as a raw count and never folded into this
figure.

### Definition of "evidenced" — frozen here, before it is computed

A forecast point is **evidenced** iff it has **at least one non-null released per-gauge value**
in the return-period metric tables under
`metrics/return_period_metrics/google/2014/dual_lstm/full_run/`.

This is deliberately the **most generous defensible reading**: a gauge counts as evidenced on
the slightest published evidence. Where a design choice could bias toward or against the
subject, this study takes the option that flatters the subject — and says that it has.

The day-1 check found 5,678 gauges with a metric *file*, against the 4,089 the Nature paper
reports as its evaluation set. A file existing may not mean a value was published. That is why
"evidenced" is defined on non-null content rather than on file existence, and why the count of
file-present-but-all-null gauges is reported as its own line rather than absorbed into either
category.

Two stricter definitions are pre-registered as **sensitivity analyses**, not as alternatives to
be chosen between after the fact: non-null at the 2-year return period, and non-null at the
5-year return period. All three appear in the same table. If they disagree materially, the
disagreement is itself the finding, and the generous definition still supplies the headline.

### Secondary metrics

1. **Gauge-count coverage** — evidenced gauges / all forecast points, unweighted. The comparator
   that makes the primary metric interpretable.
2. **Population-weighted skill distribution (Q4)** — the distribution of published skill across
   evidenced African gauges, each weighted by the population of its basin, against the unweighted
   per-gauge distribution. Skill is the developer's released value, never one we compute from
   hydrographs.
3. **Coverage by mapping-density stratum** — P_unevidenced within terciles of OSM feature density.
4. **Country table** — forecast points, evidenced points, population in reach, P_unevidenced, for
   every African country with ≥1 forecast point.

### The metric of record for Q4, and one thing not yet known

Q4's skill value is **F1 at the 2-year return period at 0-day lead** for
`google/2014/dual_lstm/full_run`, derived from the released precision and recall. The 2014 split
governs; 1980 is a robustness check. F1 because the paper uses it, and because precision and
recall are what the release contains.

The released tables are indexed by return period (1.01, 2, 5, 10, 20, 50) with **three rows per
return period whose meaning is not established from the release documentation**, and lead times
0–7 as columns. This was read from row and column labels only; no value was read. **Gate B (§10)
resolves the row semantics before any value is loaded**, and the resolution is appended as an
amendment. If they cannot be resolved, Q4 is dropped.

## 6. Harm threshold

Set here, before any number exists. This study measures coverage of evidence, not failure, so the
threshold marks *materiality*, not harm caused:

A basin is **materially unevidenced** if it holds **≥ 100,000 residents**, contains at least one
forecast point, and contains no evidenced forecast point — **and** the next-downstream basin
(`NEXT_DOWN` in the level-12 table) contains no evidenced forecast point either.

The downstream condition is included because a gauge downstream of a populated basin carries real
information about it, and a threshold ignoring that would overstate the finding. The 100,000
figure is a round number at the scale of a large town, chosen before seeing the basin population
distribution. If it later proves to sit on a cliff in that distribution, the sensitivity of the
count to it is reported — the threshold is not moved.

## 7. Ground truth

**No flood-event ground truth is used, and none is needed.** This study measures what has been
published about forecast points, not whether forecasts were right. That design choice is what
makes it affordable, and it is also what keeps it honest.

Two exclusions are settled and not revisited:

- **Inundation History (1999–2020, 128 m) is a frequency raster — how often each pixel was wet.
  It has no event dates and is not event ground truth.** Admissible for water masking,
  normal-extent priors and exposure weighting only.
- **The Flood API serves no historical forecasts**, so no retrospective skill claim can be built
  from it.

**The sources actually relied on, and how their error propagates:**

| Source | Role | Error, and where it lands |
|---|---|---|
| Zenodo per-gauge metrics | defines *evidenced* | Complete for the released set. The risk is definitional, not measurement — handled by the three-definition sensitivity in §5. |
| `grdc_stations_20220320.csv` | gauge coordinates | Station coordinates can be imprecise relative to the river reach; propagates into basin assignment. Handled by Gate C. |
| `hybas_gauges_info_lev12.csv` | forecast-point inventory, basin assignment | **Its identity is not yet established — Gate A.** The largest single risk in the design. |
| WorldPop 100 m | population | **A model, not a census, with spatially structured error largest in sparsely mapped areas — exactly what stratum 3 slices on.** A confound, not noise. Not reducible by any interval we could quote. |
| OSM via Geofabrik | mapping density | Reflects mapper attention, not settlement. Used to define strata only, never as a population proxy. |
| GADM / geoBoundaries | country assignment | Disputed and imprecise boundaries; disagreements with the developer's assignment are counted and reported (§4). |

The WorldPop dependency gets its own sentence because it is what a hostile referee should attack
first: **population error and mapping sparsity are correlated, so the strata in §8 and the weights
in §5 share a common source of error.** Stated in the limits box, sized by Gate E.

## 8. Sample construction and disaggregation

**Frame:** every forecast point in the study region, from the inventory resolved by Gate A.

**Inclusion:** point lies within an African country boundary and can be assigned to a level-12
basin.

**Exclusion, each counted and reported rather than silently dropped:** no usable coordinates;
coordinates at (0,0); not assignable to a basin; basin with no population estimate.

**Pre-specified strata — the exhaustive list. Anything not here is exploratory and is labelled
exploratory in the text.**

1. Country (African countries with ≥1 forecast point)
2. Evidence class — evidenced / unevidenced / file-present-but-null
3. OSM mapping-density tercile, on building + highway feature count per km² within the basin,
   terciles cut on the study-region basin distribution
4. Basin population band — <10k, 10k–100k, 100k–1M, ≥1M
5. Upstream area quartile (`UP_AREA`), cut on the study-region distribution
6. Return period — 1.01, 2, 5, 10, 20, 50 *(Q4 only)*
7. Lead time — 0 and 7 days *(Q4 only)*

**No other slice enters the results section as a finding.** Multiplicity is handled by this list
being fixed: seven strata chosen before the data, not seven survivors of forty attempts.

## 9. Statistical approach and uncertainty budget

**Proportions of gauges or basins** — Wilson score intervals via `_lib/stats.py`, `fmt(k, n)`.
Never a bare proportion; the denominator goes on the chart, not in a footnote.

**Population shares carry no confidence interval, and the Note says why.** A population-weighted
share computed over a modelled raster has no sampling error to quote — the uncertainty is model
error in WorldPop, which is structured rather than random and much larger than any interval we
could print. A Wilson interval around a population share would decorate it with a precision we do
not have. Instead: a point estimate, plus a sensitivity analysis re-running the primary metric
against an independent population surface (GHS-POP), with the spread between the two reported as
the honest uncertainty on that number.

**What the intervals do not cover, stated wherever they appear:** they cover sampling variation in
counts. They do not cover WorldPop's model error, our basin-assignment decisions, the definition
of *evidenced*, or the identity of the forecast-point inventory. Those are larger than the
intervals and are named in the limits box.

**Known confounders — handled, or only reported:**

| Confounder | Status |
|---|---|
| Population error correlated with mapping sparsity | **Reported, not handled.** Gate E sizes it; it cannot be removed. |
| Gauge density correlated with national income | Reported. GDP data ships with the release and is used descriptively only. |
| Basin size confounding population with catchment | **Handled** — stratum 5. |
| Historical gauge-network inheritance (colonial-era station siting) | **Reported, not handled.** It is a mechanism claim and we are black box: named as an alternative explanation in the discussion and in RED-TEAM.md, at rung C. |

**Claim ladder.** Every substantive sentence is labelled A (measured), B (inferred, assumptions
named) or C (interpretation). **Only rung A appears in the abstract, the title, or anything
quotable.** This Note being black box, any sentence explaining *why* is rung C at best and is a
candidate for cutting.

## 10. Decision gates

Pre-committed. Condition → action. Written so a bad answer is a decision, not a negotiation.

**Gate A — what is the forecast-point inventory?** `hybas_gauges_info_lev12.csv` holds 41,905
gauges, 6,772 in Africa, against 5,678 evaluated. It is the inventory shipped with the paper,
which is **not the same thing** as the ~5,000 verified and ~240,000 lower-confidence points the
product displays; neither product figure appears anywhere in this release.

- Identity as the Flood Hub serving inventory **can** be established from a primary source → the
  Note frames results against the deployment surface.
- It **cannot** → the frame becomes explicitly "the gauge inventory published with the 2024
  paper"; the product's own figures appear as context, clearly marked as not our denominator; the
  headline is worded to match. **This is the default.** The frame is not upgraded without a
  citable source.
- Either way, the denominator is stated in the first table.

**Gate B — metric table row semantics.** Resolve the three-rows-per-return-period structure from
the paper and `github.com/google-research-datasets/global_streamflow_model_paper` **before any
value is loaded**.

- Resolved → Q4 proceeds; the resolution is appended under §11.
- Not resolved → **Q4 is dropped from the Note entirely**, and its absence reported with the
  reason. Q1–Q3 depend on no metric value and proceed regardless. Guessing the semantics to keep
  Q4 alive is not an available option.

**Gate C — basin assignment.** If < 90% of forecast points assign to a level-12 basin, fall back
to a 10 km river-network buffer and report both, with the primary metric computed under each.

**Gate D — abandonment of the headline.** If the primary metric moves by more than 10 percentage
points across the three *evidenced* definitions in §5, no single headline number is published.
The Note presents the map, the method and the range, and states that a point estimate is not
defensible. A range honestly presented is a publishable result; a point estimate chosen from
three is not.

**Gate E — the population-error test.** If the primary metric computed on WorldPop and on GHS-POP
differ by more than 5 percentage points, the spread — not either figure — becomes the reported
result, and the limits box leads with it.

**Gate F — the null.** If population-weighted coverage and gauge-count coverage differ by less
than 5 percentage points, H0 stands and the Note's headline is that the published evidence base
tracks population closely. **Published with the same prominence as any other outcome.** It is a
useful result: it retires a widely assumed concern that nobody had checked.

**Gate G — right of reply.** Google receives the full draft, data and code, with **21 days
minimum** to respond, before publication. No exceptions. The reply is treated as peer review and
time is budgeted to act on it. An error they identify is fixed, and the fix logged in
`DECISIONS.md`.

**Single-shot discipline.** `04-analysis/` runs **once** against real values. Development happens
against permuted metric labels. Unblinding is logged in `RUNLOG.md` with the date and the git SHA
of the frozen code. A bug found after unblinding is fixed, logged, and the re-run disclosed in the
Note. Silent re-runs are how honest people produce dishonest numbers.

**Structural blinding.** Strata (§8), basin assignment, population weights and every figure
template are built before any metric value is loaded, in scripts that fail loudly if a metric
table is reachable. That assert is the second person this study does not have.

## 11. Amendments

| Date | Section | Change | Reason |
|---|---|---|---|
| | | | |

## 12. Conflicts

**Operator:** sole author. See `01-scoping/CONFLICTS.md`, repeated at publication.

No financial interest in Alphabet/Google or in any competitor in flood forecasting. No prior or
current employment, consulting, advisory or contract relationship with the subject, its vendors or
its regulator. **No funding was received for this study from any party.** No personal connection
to the subject or to the authors of the papers cited.

Noted for the reader to weigh rather than because we judge it material: Google.org funded the
GiveDirectly and IRC anticipatory-cash programmes cited in scoping as evidence of consequential
deployment. Neither organisation, nor Google.org, has any relationship with us or with this study.

Refreshed at publication — relationships change during a study, and a reader is better placed than
we are to decide what colours a result.
