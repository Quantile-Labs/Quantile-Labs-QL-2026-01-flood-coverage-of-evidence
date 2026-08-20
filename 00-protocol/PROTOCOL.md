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

Appended, never edited. Every amendment below was made **before any metric value was read** —
all of it is documentary evidence from the paper and the released code, which is what Gates A
and B instructed.

| Date | Section | Change | Reason |
|---|---|---|---|
| 2026-08-04 | §10 Gate B | **RESOLVED.** The three rows per return period are **tolerance windows of 0, 1 and 2 days**. Source: `notebooks/backend/return_period_metrics.py` — `RETURN_PERIOD_TIME_WINDOWS = [Timedelta(0d), Timedelta(1d), Timedelta(2d)]`, and the metric frame is `MultiIndex.from_product([RETURN_PERIODS, return_period_time_windows])`. Columns are `LEAD_TIMES = list(range(8))`, lead 0–7 days. `RETURN_PERIODS = [1.01, 2, 5, 10, 20, 50]`. Repo pinned at commit `1e88caf`, manifested. | The window is the slack allowed between a predicted threshold crossover and an observed one when counting a hit. Q4 is **not** dropped. |
| 2026-08-04 | §5 metric of record | **Specified: tolerance window = 2 days.** The metric of record for Q4 is F1 at return period 2.0, **window 2 days**, lead time 0, `google/2014/dual_lstm/full_run`. | The protocol fixed return period and lead time but could not fix the window, whose existence was unknown until Gate B. The paper uses the 2-day window for its own headline figures — *"We considered a model to have correctly predicted an event with a given return period if the modelled hydrograph and the observed hydrograph both crossed their respective return period threshold flow values within two days of each other."* Matching it makes our numbers comparable to theirs. Windows 0 and 1 are reported as a sensitivity, not chosen between. |
| 2026-08-04 | §5, §9 | **Degenerate precision/recall values must be identified and reported separately.** `_true_positives_fraction_in_window()` returns **1** where there are no observed events *and* no predicted events, and **1** where `discard_nans_in_window` is set and no observed data surrounds any predicted event; it returns **0** where there are no predicted events but observed events exist. A gauge can therefore score a perfect 1.0 because nothing ever happened there, not because anything was forecast well. | Discovered by reading the released code, before loading any value. This does not change the frozen definition of *evidenced* — a published value is still a published value — but a population-weighted skill distribution that silently includes degenerate 1.0s would overstate skill, and at high return periods, where events are rarest, that risk is greatest. The count of degenerate values is reported as its own line at every return period, and Q4 is reported both including and excluding them. Neither version is designated the headline until both are computed; if they disagree materially, the disagreement is the result. |
| 2026-08-04 | §10 Gate A | **RESOLVED against the deployment-surface reading. The conservative default applies.** `hybas_gauges_info_lev12.csv` is **not** the Flood Hub serving inventory. It is the research gauge inventory used to assign each gauge a HydroBASINS level-12 polygon so that cross-validation splits keep one gauge per polygon — its only use in the released code (`create_ungauged_experiments_gauge_groups.ipynb`, cell 10; `loading_utils.load_hydroatlas_info_file`). Evidence: composition is GRDC 10,648 + Caravan 9,334 + national agency sources; operational-looking fields are empty (`is_alerting` is set on **2 of 41,905** rows); no product figure appears anywhere in the release. | The Note is framed explicitly as "the gauge inventory published with the 2024 paper". The product's own figures (~5,000 verified, ~240,000 lower-confidence) appear as context, clearly marked as not our denominator. The frame is not upgraded without a citable source, and none exists. |
| 2026-08-04 | §4, §8 | **The African forecast-point denominator is corrected before use: 6,772 is not a count of gauges.** Of the 6,772 African rows, **3,682 are `hybas_*` entries with no station code, no site name and no provider station — HydroBASINS polygon identifiers, not physical gauges** (all 3,682 are African; none appear on any other continent). The remaining 3,090 are real gauges: GRDC 1,683, DWS South Africa 1,295, MAWLR Namibia 112. | Reporting 6,772 as African forecast points would inflate the denominator by 119% and make the headline wrong in the subject's disfavour. The sample construction in §8 counts real gauges and `hybas_*` polygon entries separately, reports both, and states which the primary metric uses. |
| 2026-08-04 | §3 | **CORRECTION to frozen text. §3 states that the Nature paper "discloses Africa F1 of 0.15–0.21 at the 5-year return period itself". That is wrong and must not be repeated.** The 0.15 and 0.21 are the **South America** row read across two different models. Verified from committed cell outputs in `figure_4_continent_reliability_scores_distributions.ipynb` at pinned commit `1e88caf`. At the 5-year return period, 0-day lead: **Africa GloFAS 0.169748, Africa AI model 0.262328**; South America GloFAS 0.147253, South America AI 0.210967. Africa is **not** the lowest-scoring continent — South America is — and the AI model's African mean is ~55% above GloFAS's. | Caught before publication and before the figure was used in any claim. The paper's own prose sentence reconciles exactly to South America (GloFAS 0.1473→0.15, AI 0.2110→0.21; Europe 0.3199→0.32, SW Pacific 0.4564→0.46), so the misattribution happened downstream of the paper, in our own background notes. |
| 2026-08-04 | §3 | **The "not a rebuttal" framing is narrowed to what can actually be defended.** The paper's *text* discloses no Africa F1 anywhere. Fig. 4 is boxplots — medians and quartiles — so the continent **means** appear in neither the article nor the Extended Data; they exist only in the companion repository's committed cell outputs, and are recomputable from Zenodo `10.5281/zenodo.10397664`. The Note may say Africa's performance *is recoverable from the published artefacts*, citing Fig. 4 **plus the repository**. It may **not** say the paper stated Africa's score. | The stronger reading would not survive a check by anyone who opens the paper, and this Note's entire posture depends on being scrupulous about what the developer did and did not publish. The Africa result that **is** in the text is the null at the 1-year return period, where the AI model does not beat GloFAS: mean difference 0.004197, p = 0.069605, d = 0.028121 (cell 27), matching the published P = 0.07, d = 0.03. |
| 2026-08-04 | §5 | **Experiment and period are specified for Q4, having been under-specified at freeze.** `EXPERIMENT_NAMES['kfold_splits'] = 'AI Model'` and `EXPERIMENT_NAMES['full_run'] = 'Gauged Basins Run'` (`evaluation_utils.py:32–34`). **What the paper reports as "the AI model" is `kfold_splits`, not `full_run`** — `full_run` is the model evaluated at gauges it was trained on. The paper's Fig. 4 tables further read the **1980** datasets, not 2014. Accordingly: the *evidenced* definition in §5 **stays on `full_run`** — it is a presence test, `full_run` covers all 5,678 gauges, and it therefore remains the most generous reading. Q4's **skill values** are reported for three experiments side by side: `kfold_splits` (the paper's comparability anchor), `continent_splits` (Africa held out of training — the cut that actually bears on ungauged African basins), and `full_run` (gauged, optimistic). Period: 2014 primary as frozen, **1980 reported alongside**, because the paper's published continent means are 1980. | Discovered before any value was loaded. Reporting a population-weighted skill distribution off `full_run` alone would have described the model where it was trained while the Note's subject is forecast points where it was not — the single most damaging error available in this design, and one no reader could have caught from our figures. No experiment is designated the headline until all three are computed; if they disagree, the disagreement is the result. |
| 2026-08-04 | §10 | **NEW GATE H — the `hybas_*` denominator. Raised by the week-one pre-mortem, which found that the 2026-08-04 correction may itself be an over-correction, in the subject's favour.** The 3,682 `hybas_*` entries are all African, appear on no other continent, carry coordinates and HydroBASINS IDs, and 676 carry river names. **A table of ungauged prediction points in Africa is exactly what a model whose contribution is prediction in ungauged basins would need.** If that is what they are, they are not noise to strip from the denominator — they are the most relevant points in the study: places with a forecast, no gauge, and therefore no possible published metric. **Condition → action:** establish what `provider = 23` / `data_source = catalogue.csv` designates, from primary sources, **before the primary metric is computed**. Resolved as prediction points → they are in the denominator and the distinction is reported. Resolved as non-forecast basin bookkeeping → excluded, and the exclusion reported. **Unresolved → both denominators are reported with equal prominence and no single headline figure is published.** | Reversing this choice moves the African denominator from 3,090 to 6,772 and could move the primary metric by more than every other design decision combined. The facts in the 2026-08-04 correction are verified; the *inference* that polygon IDs are not forecast points is not, and it sat in the decisions log among six things that were verified, which made it look established. Settled before the number exists, not after. |
| 2026-08-04 | §5, §9, §12 | **Disclosure and language commitments carried from the pre-mortem disposition table.** (a) **"Measured" is banned** from the title, abstract and every headline claim; the word is **"published"** — our finding is about what was published, and "never been measured" asserts something a black-box tier cannot know. Enforced in the claim-ladder pass. (b) **GRDC record length and station density are reported in the same figure as the population weighting**, and named in the abstract if coverage tracks the historical gauge network — that network is the most defensible alternative explanation for any spatial pattern we find, and it is not a decision by the developer. (c) **HydroSHEDS basin polygons and the Geofabrik OSM extract are manifested with hashes and extract dates before use, never streamed** — neither is in the Zenodo release, both are moving targets, and terciles cut on a live database are not reproducible. (d) **Gate E is non-negotiable**: GHS-POP is acquired in the same session as WorldPop. | Each of these is a way the Note gets demolished that costs almost nothing to prevent in week one and cannot be retrofitted in week eight. |
| 2026-08-04 | §3 | **The welcome clause.** The Note states in its opening — not defensively at the end — that **if the developer publishes coverage figures that supersede ours, that is the outcome we wanted.** Further: the first paragraph carries the disclaimers, the version scope and the frame; the limits box is not permitted to be the first place a reader meets them. | The likeliest good-faith rebuttal is "that is a 2024 supplementary table, our system serves something else, here is the real coverage" — which would be right, better than ours, and a genuinely good outcome for the world. Saying so in advance costs nothing and removes the sting. And a reader who reaches a limits box has already formed the view the headline gave them. |
| 2026-08-04 | §1 | **THE VERSION QUESTION IS RESOLVED. §1 states we have not established which version serves Flood Hub; we now have, from the developer's own repository.** `google-research/flood-forecasting` (OpenHydroNet), pinned at commit `affbaaa` (2026-06-16), manifested. Its README states that the repository "implements the state-of-the-art models that power Google FloodHub", and designates: **Handoff-Forecast-LSTM — "Former production model"**, referencing Nearing et al., Nature 2024; **Mean-Embedding-Forecast-LSTM — "Current production model (as of December 2025)"**, referencing Gauch et al., *How to deal with missing input data*, HESS **29**:6221 (2025). **The architecture whose per-gauge evidence this study analyses is the developer's own designated *former* production model.** Scope precisely: the as-of date is theirs (December 2025) and the repository HEAD is 2026-06-16; we claim nothing about August 2026 beyond what they state. | This converts the Note's largest unfixable weakness into a citable, date-stamped fact, and it strengthens the study's premise rather than undermining it: the entire published per-gauge evidence base pertains to a superseded architecture. §1's original wording stands as written; this row governs. |
| 2026-08-04 | §2 | **Access tier restated as a choice, not a limit. Pretrained weights for the Flood Hub architecture are publicly released** (`pretrained-models/`, 79 MB, `model_epoch055.pt` plus config and scalers). White-box access is therefore *available* to us. **We decline it and remain no-query by design.** | This Note's subject is what has been *published about* forecast points, not what a model can be made to do. Running released weights would generate new evidence and answer a different question. The Note states this as a deliberate scope decision, because a reader who knows the weights are public will otherwise assume we did not know. |
| 2026-08-04 | §7, §8 | **A second published per-gauge evidence artefact is brought into scope and accounted for: `pretrained-models/.../test_metrics.csv`, 10,137 basins with NSE and KGE. It contains ZERO African basins** — seven Caravan constituent datasets (hysets 6,392; camelsbr 870; lamah 825; camelsgb 671; camels 670; camelscl 491; camelsaus 218), none covering Africa. **It must not be cited as skill evidence in any case**: the developer's own README warns the models "were trained on the FULL historical data period (1982–2023). There is NO temporal holdout/test split", making any such evaluation "fundamentally invalid, artificially inflated … due to in-sample evaluation (data leakage)". | A referee would otherwise ask why we ignored published per-basin metrics. We did not: they add nothing to Africa's evidence base, for two independent reasons, and the second is the developer's own disclosure. Reporting both reasons is more informative than reporting neither. |
| 2026-08-04 | §8 | **Recorded, with its scope stated tightly: the operational-settings training basin list contains no African basins.** `example-configs/multimet-basins-list-without-chirps.txt` — the `train_basin_file` for `floodhub-settings-config.yml`, which the developer describes as replicating "the training settings of the current (2025) operational FloodHub model as closely as possible within this open-source framework" — holds **15,955 basins across 7 Caravan datasets, 0 African**; North America alone is 80.4%. **This establishes what can be publicly replicated, NOT what Google trained on internally.** The binding constraint is redistribution rights: the 2024 work used 741 African GRDC gauges that cannot be redistributed. The Note may say the operational model's behaviour in Africa **cannot be independently replicated from the released artefacts**. It may **not** say the model was not trained on African data. | This is precisely the inference that would demolish the Note if over-claimed, and it is one sentence away from the defensible version. Written into the protocol now, before the sentence gets drafted. |
| 2026-08-04 | §3 | **Credit is due in the Note's own text and is not optional.** The developer has open-sourced the production model architectures, released pretrained weights, and published a blunt warning against the most likely misuse of those weights. That is materially more transparency than the field's norm and the Note says so plainly, in its own voice, near the front. | A Note about gaps in published evidence that omits what *has* been published is not a fair account, and would deserve the reception it got. |
| 2026-08-04 | §10 Gate H | **RESOLVED to the UNRESOLVED branch — deliberately. Both competing readings are ruled out; two denominators are reported and no single headline figure is published.** Evidence: (a) the 3,682 `hybas_*` rows carry **zero** station-derived fields — no drainage area, altitude, warning/danger level, site name, station code or organisation — only HydroATLAS-join fields every row has; (b) the identifier is self-referential, `hybas_` + `HYBAS_ID`, with `HYBAS_ID == original_hybas_id` for all 3,682; (c) **only 71 of 3,682 share a level-12 basin with a real African gauge — 98% disjoint**; (d) they concentrate where the gauge network is absent (South Sudan 1,145, Angola 552, Chad 422, Nigeria 149) against a real-gauge distribution that is 55% South Africa; (e) **3,682 is 1.6% of the 224,827 African level-12 basins** in the release's own `hybas_country_list.csv`; (f) **no primary source documents what `provider = 23` / `data_source = catalogue.csv` designates.** | (c) and (d) kill the "bookkeeping duplicate" reading — these are not repeats of gauged basins, they are complementary to them. (e) kills the "these are the ungauged prediction surface" reading as a complete account: if forecasts are issued at ungauged basins, the surface is far larger than 1.6% of them. What they *are* is undocumented, and the gate's own condition — established from primary sources — is not met. Reporting both denominators is the honest disposition, not a failure to decide. |
| 2026-08-04 | §4, §5, §8 | **The denominator becomes an explicit ladder, reported in full in the first table, with the primary metric computed at every rung.** (1) **741** African gauges with published per-gauge metrics; (2) **3,090** real African gauges in the published inventory (**6,772** rows including the 3,682 undocumented `hybas_*` entries); (3) **224,827** African HydroBASINS level-12 basins (`hybas_country_list.csv`, 1,034,373 rows globally, 21.7% African); (4) the product display surface — ~5,000 verified and ~240,000 lower-confidence points — **not enumerable from any released artefact and therefore never used as our denominator.** | A single denominator was always going to be the weakest joint in this Note, and Gate H established that no single one is defensible. A ladder is stronger than a choice: it shows the reader exactly how the answer depends on what you count, and it removes the temptation to pick the rung that gives the best number. Rung 4 is stated and explicitly not used, so nobody has to wonder whether we forgot it. |
| 2026-08-04 | §9, §10 | **Unverified claim quarantined and recorded so it cannot leak into the Note.** A web source asserts the model "provides predictions over 1.03 million HydroBASINS level-12 watersheds", which matches `hybas_country_list.csv` at 1,034,373 rows. **This match is not evidence.** That file is the global HydroBASINS level-12 basin→country table, and ~1.03 million is the size of HydroBASINS itself, not a Google design choice. The Flood Hub documentation confirms only "approximately 16,000 streamflow gauges" for *training*. **The Note may not state that the model predicts at 1.03 million locations unless a primary source is found.** | This is the same failure mode that produced the Africa F1 error — a plausible number from a secondary source, corroborated by a coincidence. Written into the protocol rather than left to memory, because the coincidence is seductive enough that a future session would probably accept it. |
| 2026-08-04 | §10 Gate G | **The right of reply carries specific questions, sent with the draft, not just an invitation to comment.** At minimum: (1) what do `provider = 23` / `data_source = catalogue.csv` designate in `hybas_gauges_info_lev12.csv`, and are forecasts issued at those 3,682 African locations? (2) at how many locations does Flood Hub issue forecasts in Africa, verified and lower-confidence? (3) which model version currently serves Africa, and are per-gauge African metrics published for it anywhere? (4) is any evaluation of the current production model in Africa planned or complete? **Questions we could not answer are published with the Note alongside whatever answers are given, including "no answer received".** | Gate H, the denominator ladder and the version scope are all questions the subject can settle in a sentence each and we cannot settle at any price. Asking precisely is the difference between a right of reply that improves the work and one that produces a bland statement. Publishing the unanswered questions is not a rebuke — it is the honest record of what the public evidence cannot support. |
| 2026-08-05 | §9, §10 Gate E | **Gate E's premise is corrected before it is used: WorldPop and GHS-POP are NOT independent with respect to stratum 3, and their spread is systematic rather than random.** Measured, blind, before any metric value was read: continentally the two agree to **−3.7%** (1,273,594,049 against 1,322,374,091), but by mapping-density tercile — T1_sparse **28.5%**, T2 68.2%, T3_dense 109.3% of WorldPop; and **GHS-POP is exactly zero in 66.8% of sparse basins against WorldPop's 6.3%**. The mechanism is that GHS-POP derives from built-up-surface detection while WorldPop unconstrained distributes census counts by covariates, so GHS-POP's zeros are a property of settlement detection — **the same dependency stratum 3 measures**. **Consequences, binding:** (a) the Note may not describe GHS-POP as an independent check; (b) the Gate E spread is reported **with its mechanism stated**, never as a bare range; (c) **the surface giving the larger headline may not be selected** — where the two differ, the range is the result; (d) GHS-POP's zeros may not be reported as evidence that nobody lives in a basin. | Choosing unconstrained WorldPop kept the *primary* weight independent of settlement detection, but the comparator does not share that property, and a spread presented as neutral uncertainty would misrepresent a systematic divergence as noise. This is the pre-mortem's third demolition scenario arriving in week one with numbers attached, and it lands where the study is most exposed: WorldPop yields the larger and more quotable figure in exactly the sparse basins the Note is about. Fixed before the primary metric exists so the temptation cannot operate. |
| 2026-08-05 | §7, §9 | **Recorded as a substantive limitation in its own right, not merely a data caveat: in sparsely mapped Africa the population is itself contested, by a factor of about three and a half between two mainstream published surfaces.** Reported in the limits box in its own paragraph. | Directly relevant to this Note's subject rather than incidental to it. Wherever the map is thin, both how many people live there and — separately, still blind — what has been published about their forecast point are uncertain. Stating the first plainly is a precondition for making any honest claim about the second, and it must be reported whichever way the metric analysis later falls. |
| 2026-08-05 | §8 stratum 3 | **DEVIATION, declared: equal-frequency terciles of OSM feature density do not exist where more than a third of basins have zero features.** Chad, the first country processed, has **5,045 of 9,667 basins (52.2%) at exactly zero**. `pd.qcut` would have silently collapsed to two bins and the Note would have reported a three-way stratification it never performed. **Replacement cut, pre-committed before any further country is processed:** where the zero share exceeds 1/3, `T1_sparse` = zero features, and `T2`/`T3_dense` = median split of the non-zero remainder. The zero share is reported for every country and in the limits box. Where the zero share is below 1/3, equal-frequency terciles are used as originally written. | The stratum exists to identify sparsely mapped basins, and in the sparsest places the honest answer is a point mass at zero, not a smooth distribution. A cut rule chosen after seeing which gave the better contrast would be exactly the post-hoc tuning the pre-registration exists to prevent — so it is fixed here, on the first country, before the rest. |
| 2026-08-05 | §8 stratum 3 | **Recorded, and it settles what stratum 3 is measuring: the feature mix is 95.1% buildings to 4.9% roads** (Chad, 2,655,881 building polygons against 136,166 road features). The stratum may therefore be described as **settlement mapping density**, as §8 assumes. | Had roads dominated, this variable would have been a road-mapping index and calling it settlement density would have been wrong. Checked rather than assumed, and re-checked per country as the run proceeds. |
| 2026-08-05 | §7 | **Zero features and unprocessed are now distinguished in the harness, after a bug that conflated them.** A basin inside a successfully downloaded extract with no features is recorded as **0**; a basin in a country never downloaded stays **NA**. The first version stored both as NA, which dropped Chad's 5,045 zero-feature basins — the least-mapped 52% — out of stratum 3 entirely and would have biased the tercile cut towards better-mapped ground. | Self-refuting for a study whose entire subject is the difference between "nothing is there" and "nothing was measured". Same principle already applied to nodata in the population sums. |
| 2026-08-04 | §5 | **The 5,678 vs 4,089 gap is documented, and is not evidence of empty metric files.** The paper states that gauges were excluded from evaluation *"because it was not possible to match those gauges to a GloFAS pixel"*, with further exclusions for drainage area < 500 km² and > 10% disagreement between reported and modelled drainage area — **exclusions made for the GloFAS comparison**. A gauge can therefore carry published Google metrics without being in the 4,089-gauge comparison set. | Supports the frozen generous definition of *evidenced* rather than undermining it, and lowers the expected exposure to Gate D. The actual null count is still computed at analysis time under the frozen definition; nothing here is assumed. |
| 2026-08-06 | §10 structural blinding | **SELF-REPORTED DEVIATION. The structural-blinding guard was inert from 2026-08-04 to 2026-08-06 — the entire strata and covariate build ran without it.** §10 states that those scripts "fail loudly if a metric table is reachable". They could not: each named `metrics/return_period_metrics` and `metrics/hydrograph_metrics/per_gauge`, and **neither path was ever extracted into `02-data/interim/`**, so the check never had anything to match. What *was* extracted, on 2026-08-03T19:57:33Z and unguarded throughout, is `metrics/concatenated_return_period_metrics` (4 `.pkl` files) and `metrics/hydrograph_metrics/per_metric/{google,glofas}/{1980,2014}` — 172 files, all outcome values. **Blinding held in fact, and the evidence is offered as evidence rather than as reassurance:** (a) no harness script other than `00_day1_join_check.py` references the metrics tree at all, and that one reads a `tar tzf` archive listing, never an extracted file; (b) the frozen source for *evidenced*, `metrics/return_period_metrics/` at 113,585 entries, **has never been extracted and remains sealed inside `metrics.tgz`**; (c) every input the six scripts open is accounted for in `MANIFEST.csv`. **The honest statement of what a reader may rely on: the discipline held, the mechanism enforcing it did not, and for those three days nothing automatic would have caught a violation.** | §10 calls that assert "the second person this study does not have", and this Note's central claim is about the difference between what is asserted and what is evidenced — so the protocol may not carry an unqualified structural-blinding claim for a period when the structure was not there. Recorded in the protocol rather than only in `DECISIONS.md` because it qualifies a §10 commitment, and a deviation logged only in the working notes is a deviation a reader has to go looking for. |
| 2026-08-06 | §10 structural blinding | **Remedy, applied and verified: all six harness scripts now call `_lib/blind.py:require_absent()` against the whole `02-data/interim/metrics` tree**, replacing six inline copies that each named subdirectories. Verified: all six refuse to run in the present tree; the helper passes when the path is absent; a missing or renamed symbol raises `ImportError`. **The rule going forward is that the guard targets the outcome tree, never a path inside it, and is imported, never restated.** The lesson is recorded in the helper's own docstring so it does not have to be rediscovered by the next study. | Two failure modes, one of which was reasoned into deliberately. Enumerating forbidden names fails the moment a name is not the one you guessed. And the original rationale — "restated rather than imported so that deleting one script cannot silently disarm the other" — had the direction backwards: an inline copy fails **open**, running on regardless, while a missing import fails **closed**. Fail-closed is the only property worth having in a guard. |
| 2026-08-06 | §8 stratum 4 | **Stratum 4 built and its cut recorded: bands are cut on WorldPop unconstrained, left-closed and right-open** — `[0, 10k)`, `[10k, 100k)`, `[100k, 1M)`, `[1M, ∞)`. Result: 204,214 / 22,535 / 1,535 / 60 basins. **1,684 basins with no population value carry no band — NA, never `<10k`.** | §8 named the band edges but not which surface cuts them or which side of an edge is closed. WorldPop carries the primary weight because it has no settlement-detection dependency, and cutting the stratum on GHS-POP would have reintroduced through the band exactly what the weight was chosen to avoid — concrete rather than theoretical since the 2026-08-05 measurement, GHS-POP being exactly zero in 66.8% of sparse basins. The interval convention is stated because 100,000 is also the §6 harm threshold, and a basin of exactly 100,000 people falls in `100k-1M`. |
| 2026-08-06 | §8, §9 Gate E | **`pop_band_ghspop` is added to the frame as a declared sensitivity column, outside the seven strata §8 enumerates, and is declared here so it is not mistaken for one.** It never supplies a headline and is never an alternative to `pop_band`; it exists so the Gate E spread is visible in the frame rather than recoverable only by someone who thought to recompute it. | §8 says anything not on its list is exploratory and must be labelled exploratory. This is a covariate for a required disclosure rather than a new slice of the results, but the distinction is fine enough to be worth writing down instead of leaving to a reader's charity. Gate E consequence (b) requires the spread to travel with the figure, and a column that must be re-derived to be seen will not be seen. |
| 2026-08-06 | §9 Gate E | **Binding addition to the Gate E consequences: band agreement between the two population surfaces may not be reported as agreement between the surfaces.** Measured blind: of 210,547 basins carrying both, **95.5% fall in the same band** — but the disagreement runs opposite to expectation (T1_sparse 0.2%, T2 3.4%, T3_dense 11.6%), and **inside the *agreed* `<10k` band in the sparse tercile GHS-POP is 25.1% of WorldPop, 7,132,103 people against 28,436,154 across 84,995 basins.** Mechanism: sparse basins hold too few people for a ~3.5x divergence to cross a band edge, so the coarse cut absorbs it. **Wherever the band table appears, the within-band spread appears with it.** | The 95.5% is the single most quotable reassurance this frame produces, and it is wrong in the study's own favour — the exact direction of error this Note is least able to afford. Band agreement is a statement about a cut, not about a population. Consistent with consequence (b), which forbids reporting the spread as a bare range: reporting a bare *agreement* rate is the same error with the sign reversed. |
| 2026-08-07 | §10 Gate F | **Gate F's comparator is specified: gauge-count coverage is computed on rung 2 of the denominator ladder, the 3,090 real African gauges, and on no other rung.** The gate as written named "gauge-count coverage" without naming a rung, and a blind dry run against permuted labels showed the verdict flipping across all three: rung 2b, all 6,772 inventory rows, gives 6.9% coverage and a 5.5 pp difference, so H0 rejected; **rung 2 gives 15.2% and 2.8 pp, so H0 stands**; rung 1, the 741 gauges holding a metric file, gives 63.3% and 50.9 pp, so H0 rejected. Population-weighted coverage was 12.4% throughout. | A gate returning three different verdicts on data with no real association is measuring its own denominator rather than the world. Rung 2 is the only rung on which both sides of the comparison can carry evidence at all: rung 2b includes the 3,682 undocumented `hybas_` entries, which cannot hold a metric by construction and so guarantee a low gauge count for a reason unconnected to evidence, while rung 1 conditions on the very thing being measured and compares the evidence base against itself. Chosen blind, and the number that would result was visible for every option before the choice was made, which is why the reasoning is recorded here rather than in a footnote written afterwards. |
| 2026-08-07 | §5 metric of record | **F1 is not published per gauge and is derived by us.** `google/2014/dual_lstm/full_run/` contains exactly two metric directories, `precision` and `recall`, 5,678 gauges each. The metric of record for Q4, F1 at return period 2.0, tolerance window 2 days, lead time 0, is therefore computed here as the harmonic mean of the two released values. **Where either input is null the derived F1 is null and never zero.** The Note attributes the derivation to us wherever the figure appears. | §5 already anticipated this in saying "F1 because the paper uses it, and because precision and recall are what the release contains", but it did not say in terms that the arithmetic is ours. Presenting a computed F1 as though the developer had published it would misstate the evidence base, which is the single thing this study cannot get wrong. Nulling rather than zeroing follows the rule applied everywhere else here: a gauge with no published precision has no published F1, and calling that zero invents a measurement. |
| 2026-08-07 | §5 secondary 3, §9 | **Binding: the mapping-density tercile table is published with its permuted null baseline in the same table, never alone.** Measured blind, permuted P_unevidenced by tercile is T1_sparse 99.3%, T2 97.3%, T3_dense 86.6%, a 12.7 pp spread on data with no real association, and it tracks the share of forecast points holding a metric file at all, 1.7%, 6.6% and 14.7%. Permutation scrambles which filed gauge is evidenced but does not touch which points have a file, because file presence is a property of the release. | The gradient is a genuine result, since the frozen definition of *evidenced* counts absence of a file and absence of content alike, and both are absences of published evidence. But it is the most quotable thing this study will produce, and most of it is a statement about where gauges were evaluated at all rather than about which evaluations returned a value. Published bare, it invites every reader to attribute it to the wrong mechanism, and the correction would never catch up with the headline. The baseline costs one column. |
| 2026-08-07 | §5 | **The Note reports the structural floor of the primary metric alongside the primary metric itself.** From file presence alone, established by the day-1 check on 2026-08-03 with no value read, 55,234,096 of the 71,248,661 people in reach of an African forecast point are in reach of no gauge that holds a metric file, so **P_unevidenced cannot fall below 77.5% however generous the content proves to be**, and the outcome is confined to `[77.5%, 100%]`. | It is the most robust number in the study, it depends on no judgement about content, and it survives every disagreement a reader might have with the definition of *evidenced*. Reporting it also sets the reader's expectations honestly about what the unread values decide, which is where the answer falls inside a 22.5 pp band rather than what kind of answer it is. Recorded before unblinding so that it cannot later look like a floor chosen because the headline needed support. |

## 11a. Post-unblinding amendments

**Everything in this section was written after the values were read, and none of it carries
pre-registration force.** It is kept out of the §11 table deliberately, because that table
opens by stating that every amendment in it was made before any metric value was read, and
appending post-hoc work to it would falsify a sentence in the frozen text. The two are
separated so that a reader can tell, without taking our word for it, which commitments were
made blind and which were not.

**What prompted these, stated exactly.** An adversarial self-review of the first full draft,
run by the operator on 2026-08-20 as a rehearsal for external review, in which two referee
reports were written against the draft from two assumed positions: an operational hydrologist
and a forecast-verification statistician. **No independent reviewer has read this draft. The
two hydrologists the red team asked for have not been approached, and that step remains open.**
The exercise is worth what a rehearsal is worth and no more, which is why it is recorded here
by what it actually was rather than by the name of the thing it stands in for. The three
questions put to it are the ones the real reviewers will be asked: whether the basin-level
definition of *in reach* is defensible, whether the framing around the Global Runoff Data
Centre archive is fair to the developer, and whether the derived F1 is a legitimate
recombination.

**What they may and may not do.** None of the additions below replaces the primary metric. The
pre-registered result stands as computed on 2026-08-12 and the headline does not move. Each
addition is published beside the frozen result under a heading that says it is post-hoc, and
where an addition disagrees with the frozen result the disagreement is the finding and both
numbers are printed. Anything here that changes how a pre-registered number is *reported*,
rather than what it is, is marked binding and takes effect in the Note.

| Date | Section | Change | Reason |
|---|---|---|---|
| 2026-08-20 | §4 unit of analysis | **POST-HOC SENSITIVITY, not pre-registered: P_unevidenced is recomputed with population accumulated over the basins downstream of each forecast point, for one and two steps of the `NEXT_DOWN` topology already carried in the basin frame.** The frozen definition of *in reach*, the level-12 basin containing the point, remains primary and is what the headline reports. The sensitivity is published beside it, with the frozen figure first. | The referee objection is that a level-12 basin is the wrong shape for reach: the median unit here is 137 km², a river forecast serves people downstream of the gauge rather than uphill of it, and the containing polygon both truncates the served population at its boundary and counts hillslope residents who will never see that river. For a ratio the two errors partly cancel, but only if they are symmetric between evidenced and unevidenced points, and they are not. Evidenced gauges sit on a median upstream area of 2,651 km² against 1,560 km² for unevidenced ones, so the truncation removes more population from the evidenced side and the direction of the resulting bias is upward in P_unevidenced. That direction was argued in review and never measured. It is cheap to measure, the topology is already on disk, and an objection that can be answered with a join should not be answered with a paragraph. |
| 2026-08-20 | §9 Gate E | **POST-HOC SENSITIVITY, admitted for the headline only and forbidden in stratum 3. WorldPop constrained, maxar_v1, UN-adjusted, 2020, is added as a third population surface for P_unevidenced and for nothing else.** It may not be used for the mapping-density tercile table, for stratum 3, or for any figure or sentence that crosses population with OSM density. Where it is reported, it is reported as a third surface and never as a replacement for either pre-registered one, and the Gate E consequences already binding on WorldPop and GHS-POP bind it too, including the rule that the surface giving the larger headline may not be selected. | The objection, that unconstrained WorldPop distributes population onto land nobody lives on and that this matters most in the sparsest basins, is valid for the headline and invalid for the tercile table, and the two halves have to be separated rather than answered together. The constrained product places population onto detected building footprints; stratum 3 measures settlement mapping density; using one to weight the other would manufacture the correlation this study exists to test. That reasoning was recorded in `03-harness/02_add_population.py` when unconstrained was chosen on 2026-08-04 and it has not weakened, so it is restated here as a binding prohibition rather than left as a comment in a script where a later reader could miss it. The headline carries no mapping-density term, so the circularity does not arise there and the sensitivity is worth having. |
| 2026-08-20 | §5, §7 | **POST-HOC ANALYSIS, descriptive only: the 741 African gauges holding a metric file are joined to Global Runoff Data Centre daily-record metadata, `grdc_stations_20220320.csv`, fields `d_start`, `d_end`, `d_yrs`, and the evidenced rate is reported against record end year and record length.** No model is fitted, no threshold is chosen, no causal claim is made, and the result is reported as an association whether it is strong or absent. The join key and the unmatched count are reported with it. | The Note reports that 242 of the 741 carry a published value against 59.5% for the released set as a whole, and offers no mechanism for the shortfall. A gauge whose observed record ends before the evaluation period cannot yield a metric however the evaluation was designed, and a great many African holdings in this archive terminate in the 1980s and 1990s. If that is what the data show, it is a property of a century-old observational archive rather than a decision by anyone at Google, and it strengthens the alternative explanation this Note is already obliged to give. The metadata is on disk and manifested, so the check costs a join. Recorded here as post-hoc because it was not pre-registered, and reported as descriptive because a black-box tier cannot support more. |
| 2026-08-20 | §9 | **BINDING CORRECTION to how Q4 is reported, not to what it is. The population-weighted mean F1 is published with its Kish effective sample size and a gauge-level bootstrap interval, and the weighted-against-unweighted difference may not be printed without both.** Measured post hoc: the effective sample size of the population weights is 16.6 against 218 gauges, one basin carries 16.3% of the weight and the ten largest carry 61.6%. | The Note prints 0.385 unweighted against 0.331 population-weighted across 218 African gauges, and a reader reasonably takes that as a comparison across 218 gauges. It is in effect an average over about seventeen, and the difference has no stated uncertainty on either side. §9 refuses confidence intervals on population shares and that refusal is correct, because a share computed over a modelled raster has no sampling interpretation worth quoting. It does not extend to the gauges, which are a finite real sample where a bootstrap is well defined and cheap. Declining an interval in the one place it belongs was our error rather than a defensible reading of §9, and it is corrected here rather than defended. |
| 2026-08-20 | §5 metric of record | **NOT COMPUTABLE, established and recorded: a population-weighted micro-average F1 cannot be derived from the release.** The frozen path publishes precision and recall and nothing else. No true-positive, false-positive, false-negative or event count appears anywhere in `metrics.tgz`, including the four `concatenated_return_period_metrics` pickles, which were opened and hold the same two quantities in a different container. A precision and a recall fix a contingency table only up to a scale factor, so any pooled table would rest on a count we invented. **Consequences, binding:** (a) the Note states plainly that every F1 it reports is a weighted macro-average across gauges and may not be read as the skill facing an average person; (b) per-gauge event counts are added to the right-of-reply questions. | The referee point is correct and is not a matter of taste: F1 is a nonlinear function of a contingency table, so a weighted mean of per-gauge F1 values and the F1 of a pooled table are different quantities, and the second is the one the question about population weighting actually asks. Where the released artefacts cannot answer a fair question, the honest response is to name the quantity, show why it is out of reach, and ask the developer for the one number that would put it in reach. Recording the impossibility is worth as much to a later reader as computing the value would have been. |

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
