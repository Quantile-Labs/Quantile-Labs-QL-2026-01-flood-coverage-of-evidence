---
title: "Africa's published flood-forecast evidence base is thin nearly everywhere, and no thinner where more people live"
study: QL-2026-01
type: Note            # Note | Review | Finding
date: 2026-08-12
access_tier: black box
protocol_hash: b05c0b932ddb9c6db2f192ff5804570197470175e50ed21ce7520839321d2248
protocol_url: https://github.com/Quantile-Labs/Quantile-Labs-QL-2026-01-flood-coverage-of-evidence
doi: 10.5281/zenodo.21843331          # protocol v1.9; concept DOI 10.5281/zenodo.21822780
licence: CC BY 4.0
# Anchors, and the limit of what they establish. The protocol hash above is stamped into the
# Bitcoin blockchain (00-protocol/timestamps/) and the repository is archived at Software
# Heritage as swh:1:snp:5918a1abf7ffa5d946009a89a9c8a6be4fa1eed5. The anchors were made on
# 2026-08-06 and 2026-08-07, so those are the externally verifiable dates, and the 2026-08-04
# freeze recorded against protocol v1.0 is our own record rather than an attested fact.
---

# Africa's published flood-forecast evidence base is thin nearly everywhere, and no thinner where more people live

**Access tier:** black box, so we queried no system and can say nothing about how Flood Hub
behaves today, only about what the 2024 release published.
**System and version:** the gauge inventory and per-gauge metrics released with Nearing et al.,
*Nature* 627, 559–563 (2024), Zenodo `10.5281/zenodo.10397664`, retrieved 2026-08-03.
**Protocol:** frozen 2026-08-04, amended through v1.9, sha256 `b05c0b93…`, anchored
independently before the analysis was run.
**Data and code:** [10.5281/zenodo.21843331](https://doi.org/10.5281/zenodo.21843331).
**Conflicts:** none declared, see `CONFLICTS.md`.

This Note reports what the published record contains, and it makes no claim about how well the
model works anywhere. Four things need saying at the top rather than being left to a box at the
bottom, because by the time a reader reaches a limits box they have already formed the view the
headline gave them.

The absence of a published metric is not evidence of poor skill, and a reader who finishes this
Note believing that unmeasured means unreliable has been misled by us rather than informed.
Google may well have evaluated performance at every one of the locations we describe as carrying
no published value, since internal work is invisible to a black-box study by definition, so our
subject throughout is what was *published* and never what was *measured*.

**Coverage of the published evidence base tracks the historical gauge network, and that network
is not the developer's doing.** Every one of the 741 African gauges carrying a metric file comes
from the Global Runoff Data Centre archive, and 211 of the 242 evidenced points, which is 87.2%,
lie in South Africa. Per-gauge metrics can exist only where a usable observational record exists,
and the African record was assembled over a century by national hydrological services through
colonial administration, war, structural adjustment, and drought. Where our maps look sparse,
the most defensible reading is that this is where the gauges are, and anyone taking the pattern
below as an indictment of Google has misread it.

We did not look at the Flood Hub product. There is no screenshot here, no gauge list pulled from
the service, and no API call, because the API requires approval and serves no history, so a
black-box reanalysis of the released artefacts is what this is and all it is.

If the developer responds by publishing coverage figures that supersede ours, that is not a
rebuttal we intend to resist, it is the outcome we would most like this Note to produce.

> ### Limits of this claim
>
> **Absence of a published metric is not evidence of poor skill.** This is the sentence the whole
> Note is built to protect, and every figure below should be read through it.
>
> We hold no information about internal evaluation, about the model currently serving Flood Hub,
> or about the roughly 5,000 verified and 240,000 lower-confidence display points the product
> reports, none of which is enumerable from any released artefact. Our frame is the inventory
> published with the 2024 paper, and a reader who wants conclusions about the live product will
> not find them here.
>
> **The population itself is contested where the map is thin.** Two mainstream published surfaces
> disagree about how many people live in sparsely mapped African basins by roughly three and a
> half times, and they are not independent of one another in the way an uncertainty range
> implies, because GHS-POP derives from built-up-surface detection while WorldPop distributes
> census counts by covariates. Where the map is thin, how many people live there is uncertain
> before anything about their forecast point is considered.
>
> **What the intervals cover, and what they do not.** Wilson intervals appear on counts of gauges
> and basins, where a sampling interpretation is real, and they cover sampling variation and
> nothing else. They do not cover model error in the population surfaces, our basin-assignment
> decisions, the definition of *evidenced*, or the identity of the forecast-point inventory, each
> of which is larger than the intervals.
>
> **Population shares carry no interval at all, deliberately.** A share computed over a modelled
> raster has no sampling error worth quoting, and printing one would decorate the figure with a
> precision we do not have. The honest uncertainty is the spread between two independent
> surfaces, which we report instead.

## What was asked

The question was whether the published evidence base for Google's flood forecasting in Africa is
distributed in proportion to the people living behind it, or whether it thins out where more
people are exposed. It was framed so that it could be answered either way, and the null, that
coverage tracks population closely, was pre-registered as a publishable result rather than as a
disappointment. That distinction turned out to matter, because the null is what we found, and the
gate that tested it was written, with its threshold, before any metric value had been read.

## What was computed

The unit of analysis is a HydroBASINS level-12 basin, chosen because it is the developer's own
spatial unit, so that being in reach of a forecast point is defined by their geometry rather than
by a radius we invent. Population was summed over basin polygons from WorldPop 100 m
unconstrained for 2020, with GHS-POP R2023A as a comparator, and mapping density came from
OpenStreetMap building and highway counts on a Geofabrik snapshot pinned at 2026-08-03.

A forecast point counts as **evidenced** if it carries at least one non-null released per-gauge
value under `metrics/return_period_metrics/google/2014/dual_lstm/full_run/`. That definition was
frozen before it was computed, and it is deliberately the most generous defensible reading, since
a gauge qualifies on the slightest published evidence. Where a design choice could bias toward or
against the subject, this study took the option that flatters the subject, and says so. Two
stricter readings, non-null at the two-year and at the five-year return period, were
pre-registered as sensitivities rather than as alternatives to be chosen afterwards.

The analysis was built and exercised against permuted labels before being run once against real
values, which is how three defects were caught while still blind. One was a decision gate whose
verdict changed depending on a denominator the protocol had failed to name, and discovering that
after unblinding would have meant choosing the denominator with the answer already in view.

## Results

**The headline is the null.** Population-weighted coverage of the published evidence base is
7.6%, and unweighted coverage across the same 3,090 real African gauges is 7.8%, a difference of
0.26 percentage points against a pre-registered threshold of five. The evidence base tracks
population closely, and there is no support in these data for the concern that published
evaluation is scarcer where more people are exposed. We pre-registered that concern as our
hypothesis and found against it, which is the result reported here.

Against that, the absolute level is low. Of the 71,248,661 people living in reach of any forecast
point in the published African inventory, 65,852,420, which is **92.4%**, live in reach of none
carrying a published per-gauge metric. The figure moves very little under the stricter
definitions, reaching 94.1% at the five-year reading, a spread of 1.6 points that leaves the
headline defensible as a single number rather than a range. It moves less still between
population surfaces, 92.4% against 92.0%, though that agreement should not be over-read, for
reasons the limits box gives.

Both of those statements are about coverage. Neither is a statement about skill, and they should
not be combined into one.

### The answer depends on what you count, so here is every rung

No single denominator survived scrutiny, so the protocol committed in advance to reporting all of
them with the primary metric computed at each.

| Denominator | Basins | Population in reach | P_unevidenced |
|---|---:|---:|---:|
| Basins holding a gauge that was evaluated | 741 | 16,014,565 | 66.3% |
| Basins holding a real gauge | 2,123 | 51,178,147 | 89.5% |
| Basins holding any inventory point | 5,734 | 71,248,661 | 92.4% |
| All study-region basins | 229,744 | 1,319,838,500 | 99.6% |

The product's own display surface would be a fifth rung, and because it is not enumerable from
anything in the release we never use it. A reader who prefers a different rung can take it from
this table, which is why the ladder is published rather than a single number.

### Most of the geography was settled before any value was read

Coverage falls as mapping density falls, and the pattern is strong enough to invite a
straightforward reading that would be mostly wrong. Beside each figure below is the level it
would sit at if every gauge holding a metric file turned out to be evidenced, which separates the
part driven by whether a location was evaluated at all from the part driven by what the
evaluation returned.

| Mapping density | Population in reach | P_unevidenced | Floor from file presence | Attributable to content |
|---|---:|---:|---:|---:|
| Sparsest third | 915,349 | 99.998% | 99.3% | 0.7 pp |
| Middle third | 5,192,492 | 99.8% | 95.5% | 4.3 pp |
| Densest third | 65,140,820 | 91.7% | 75.8% | 15.9 pp |

In the sparsest third of African basins by mapping density, nineteen people out of 915,349 live
in reach of an evidenced forecast point. The gradient is real, and it is overwhelmingly a
statement about where gauges were evaluated in the first place rather than about which
evaluations returned a value. Both are absences of published evidence and the frozen definition
counts them together, but they are different mechanisms with different implications, and a
version of this table without its floor column would have been quoted for the wrong one.

The same correction applies to the headline. From file presence alone, 55,234,096 of the
71,248,661 people in reach live behind no gauge holding a metric file at all, so the primary
metric could not have fallen below 77.5% whatever the contents proved to be. The published values
determined where the answer fell within a 22.5-point band, and not what kind of answer it was.

### Where a metric file exists, African gauges more often carry no value

Of the 741 African gauges holding a metric file, 242 are evidenced, which is 32.7% against 59.5%
for the released set as a whole. Because the analysis was first run against permuted labels, we
know what chance alone would have produced, which is 63.3%, so this is a real association rather
than an artefact of which gauges happened to be evaluated. Thirty-six of the 47 African countries
holding a forecast point in the inventory have no evidenced point at all, and 47,633,255 people
live in reach of those points.

This finding concerns publication and not performance. It says that African gauges which were
evaluated more often carry no released value, and it says nothing about how those gauges would
score if a value existed.

### The pattern follows the gauge archive, which predates the model by a century

Every one of the 741 African gauges holding a metric file is a Global Runoff Data Centre
station, and the evidenced points among them are concentrated to a degree that makes the
geography of this Note largely a geography of that archive.

| Country | Evidenced points | Forecast points in inventory | Share of all evidenced points in Africa |
|---|---:|---:|---:|
| South Africa | 211 | 1,718 | 87.2% |
| Liberia | 8 | 17 | 3.3% |
| Namibia | 6 | 157 | 2.5% |
| Guinea | 4 | 100 | 1.7% |
| Lesotho | 3 | 47 | 1.2% |
| Angola | 3 | 611 | 1.2% |

A per-gauge metric can exist only where there is a gauge with a usable observational record to
evaluate against, so the ceiling on published evidence in any country was set by hydrological
infrastructure long before any model was trained. We can report this association and we cannot
attribute its cause, because cause is a mechanism claim and mechanism is unavailable at a
black-box tier. What we can say is that the alternative explanation is strong, that it is not a
decision by the developer, and that it accounts for the geography at least as well as anything
about how the evaluation set was chosen.

### Published skill, weighted by the people behind it

Among African gauges that do carry published values, skill can be examined with each gauge
weighted by the population of its basin rather than counted once. Our derived F1 for the 1980
datasets under the `kfold_splits` experiment at the five-year return period is 0.262328, which
reproduces the value in the developer's own committed notebook output exactly, so what follows is
commensurable with their reporting rather than a parallel construction.

F1 is not published per gauge. The release carries precision and recall, so every F1 here is our
harmonic mean of the two, with a null in either input producing a null rather than a zero.

For the frozen 2014 `full_run` reading at the two-year return period and zero-day lead, the
unweighted mean across 218 African gauges is 0.385 and the population-weighted mean is 0.331. All
three experiments appear side by side in the results file, because reporting the gauged run alone
would describe the model where it was trained, while the locations this Note concerns are ones
where it was not.

Two cautions belong with those numbers rather than beneath them. The tolerance window, meaning
the slack allowed between a predicted and an observed threshold crossing, moves the figure more
than any other choice available to us, from 0.154 at zero days to 0.385 at the two days the paper
itself uses. And the rarest return periods rest on very little, since at the fifty-year reading
under the frozen experiment there are three African gauges, all three of which score perfectly
because no qualifying event occurred, which the released code produces by construction. Any
statement about extreme events needs its denominator attached to it.

## What this does not establish

It does not establish that the model performs poorly in Africa, or anywhere else. We computed no
skill value from hydrographs and evaluated no forecast, and the skill figures above are the
developer's own released values recombined.

It does not establish that these locations were never evaluated, only that the 2024 release
published no per-gauge value for them.

It does not establish anything about the system now serving Flood Hub. A second version exists,
posted to EGUsphere in April 2026, whose Africa-specific reporting we could not locate, and we
were unable to determine which version serves the product. That uncertainty is itself a
reportable observation, so we report it rather than resolving it by assumption.

It does not establish that coverage is worse where people are. Our own pre-registered test found
the opposite, and any reading of the 92.4% figure implying otherwise is contradicted by the
result printed immediately above it.

It does not establish why the evaluation set falls where it does. We can show that it follows
the Global Runoff Data Centre archive and we cannot show what produced that archive's shape,
which is a question about a century of hydrological infrastructure rather than about a model.
Nothing here supports treating the distribution as a choice anyone at Google made.

It does not establish that no metric has ever been published for these locations. It establishes
that the artefacts named at the top of this Note contain none, and we did not survey everything
the developer has ever released.

## Reproduction

```bash
git clone https://github.com/Quantile-Labs/Quantile-Labs-QL-2026-01-flood-coverage-of-evidence
cd Quantile-Labs-QL-2026-01-flood-coverage-of-evidence
python3 _lib/manifest.py QL-2026-01 --verify
python3 04-analysis/01_evidence.py --unblind
python3 04-analysis/02_primary.py --unblind
python3 04-analysis/03_q4_skill.py --unblind
```

Inputs and checksums are in `02-data/manifests/MANIFEST.csv`, every judgement call is in
`07-admin/DECISIONS.md`, every execution is in `07-admin/RUNLOG.md`, and the adversarial review
we ran against ourselves is in `RED-TEAM.md`. Where our own record is weaker than it appears, and
in two places it is, the logs say so at the point where it is weaker rather than leaving it to be
discovered.

## Right of reply

*To be completed. Google receives this draft, the data, and the code with a minimum of 21 days to
respond before publication, and the reply will be published in full and unedited, or its absence
noted. The following questions accompany it, and any left unanswered will be published alongside
the Note as questions the public evidence cannot settle.*

1. What do `provider = 23` and `data_source = catalogue.csv` designate in
   `hybas_gauges_info_lev12.csv`, and are forecasts issued at those 3,682 African locations?
2. At how many locations does Flood Hub issue forecasts in Africa, verified and lower-confidence?
3. Which model version currently serves Africa, and are per-gauge African metrics published for
   it anywhere?
4. Is any evaluation of the current production model in Africa planned or complete?

## Corrections

None to date. Corrections will be published as prominently as the original.
