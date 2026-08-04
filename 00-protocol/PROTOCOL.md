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
| 2026-08-04 | §5 | **The 5,678 vs 4,089 gap is documented, and is not evidence of empty metric files.** The paper states that gauges were excluded from evaluation *"because it was not possible to match those gauges to a GloFAS pixel"*, with further exclusions for drainage area < 500 km² and > 10% disagreement between reported and modelled drainage area — **exclusions made for the GloFAS comparison**. A gauge can therefore carry published Google metrics without being in the 4,089-gauge comparison set. | Supports the frozen generous definition of *evidenced* rather than undermining it, and lowers the expected exposure to Gate D. The actual null count is still computed at analysis time under the frozen definition; nothing here is assumed. |

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
