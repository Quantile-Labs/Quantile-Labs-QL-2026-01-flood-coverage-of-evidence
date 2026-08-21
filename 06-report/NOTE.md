---
title: "Population-weighted coverage of published flood-forecast evaluation in Africa"
study: QL-2026-01
type: Note            # Note | Review | Finding
date: 2026-08-12
access_tier: black box
protocol_hash: b05c0b932ddb9c6db2f192ff5804570197470175e50ed21ce7520839321d2248   # v1.9, the version the analysis ran under
protocol_hash_current: f95021475d98b7393bbd6528354304071ee2ac6badb21dcecd718c52eb524b01  # v1.10, post-hoc additions only, NOT yet anchored
protocol_url: https://github.com/Quantile-Labs/Quantile-Labs-QL-2026-01-flood-coverage-of-evidence
doi: 10.5281/zenodo.21843331          # protocol v1.9; concept DOI 10.5281/zenodo.21822780
licence: CC BY 4.0
# Anchors, and the limit of what they establish. The protocol hash above is stamped into the
# Bitcoin blockchain (00-protocol/timestamps/) and the repository is archived at Software
# Heritage as swh:1:snp:5918a1abf7ffa5d946009a89a9c8a6be4fa1eed5. The anchors were made on
# 2026-08-06 and 2026-08-07, so those are the externally verifiable dates, and the 2026-08-04
# freeze recorded against protocol v1.0 is our own record rather than an attested fact.
---

# Population-weighted coverage of published flood-forecast evaluation in Africa

*Coverage of the published evidence base tracks population closely. Between 81.2% and 92.4% of
the people behind an African forecast point are behind none carrying a published per-gauge
metric, and which end of that range you take depends on a choice about evaluation period that
our own protocol never justified.*

**Access tier:** black box, so we queried no system and can say nothing about how Flood Hub
behaves today, only about what the 2024 release published.
**System and version:** the gauge inventory and per-gauge metrics released with Nearing et al.,
*Nature* 627, 559–563 (2024), Zenodo `10.5281/zenodo.10397664`, retrieved 2026-08-03.
**Protocol:** frozen 2026-08-04, amended through v1.9, sha256 `b05c0b93…`, anchored
independently before the analysis was run. It now stands at v1.10, sha256 `f9502147…`, which
adds the post-hoc section §11a and nothing the frozen result depends on. **v1.10 is not
anchored**, and the version that matters for the pre-registration claim is v1.9, which is.
**Data and code:** [10.5281/zenodo.21843331](https://doi.org/10.5281/zenodo.21843331).
**Conflicts:** none declared, see `CONFLICTS.md`.

This Note reports what the published record contains, and it makes no claim about how well the
model works anywhere. The qualifications below belong at the top of the document instead of in a
box at the foot of it, because a reader who arrives at a limits box has already formed the view
the headline gave them.

The absence of a published metric is not evidence of poor skill, and a reader who finishes this
Note believing that unmeasured means unreliable has been misled by us rather than informed.
Google may well have evaluated performance at every one of the locations we describe as carrying
no published value, since internal work is invisible to a black-box study by definition, so our
subject throughout is what was *published* and never what was *measured*.

**Coverage of the published evidence base tracks which gauges were still reporting when the
evaluation window opened, and that is not the developer's doing.** The Global Runoff Data Centre
archive reaches most of the continent: 32 African countries hold at least one gauge with a metric
file. Published values exist for 11. What is narrow here is not the archive's map but its
calendar. The frozen definition reads an evaluation period running from 2014, and of the 463
African gauges whose daily record ends before 2014, exactly one carries a published value, while
241 of the 278 whose record runs to 2014 or beyond do. A station that stopped reporting in 1991
cannot be scored against 2014, whoever is doing the scoring. Where our maps look sparse, the most
defensible reading is that this is where the observations were still arriving, and anyone taking
the pattern below as an indictment of Google has misread it.

**What the developer has published is more than the field's norm, and that belongs here rather
than in a footnote.** They open-sourced the production model architectures, released the
pretrained weights, and published a blunt warning against the most likely misuse of those
weights. They released per-gauge precision and recall for 5,678 gauges under an open licence,
which is why this Note can exist at all, and a study of what is missing from a release is only
honest if it says first what the release contains. Almost nothing else in operational flood
forecasting is open to this degree, and every criticism below is possible because of a decision
to publish that most of the field has not made.

We did not look at the Flood Hub product itself, and there is no screenshot here, no gauge list
pulled from the service, and no API call, because the API requires approval and serves no
history, so this is a reanalysis of the released artefacts and nothing beyond them.

If the developer responds by publishing coverage figures that supersede ours, that is not a
rebuttal we intend to resist, it is the outcome we would most like this Note to produce.

> ### Limits of this claim
>
> **Absence of a published metric is not evidence of poor skill.** This is the sentence the whole
> Note is built to protect, and every figure below should be read through it.
>
> **The headline is a range because our own definition was narrower than we claimed.** The frozen
> definition of *evidenced* reads one of the two evaluation periods the release publishes, and the
> other carries values for twice as many African gauges. That is worth eleven points and it is the
> largest single uncertainty in this Note, larger than every other sensitivity we measured put
> together. It is our error, it was found by a reviewer rather than by us, and it is described in
> full rather than folded into a confidence interval, because it is not that kind of uncertainty.
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
> **No population share here carries a confidence interval, and the omission is intended.** A
> share computed over a modelled raster has no sampling error worth quoting, and printing one
> would dress the figure in a precision we do not have, so we give the spread across population
> surfaces instead. That spread is not an independence check, for the reason given two
> paragraphs above, and it is reported with its mechanism rather than as a bare range.
>
> **Where an interval does belong, it is now there, and in the first draft it was not.** The
> population-weighted skill figures rest on weights that concentrate very hard: ten basins carry
> 61.6% of the total weight, and the effective sample size is 16.6 against 218 gauges. The
> weighted and unweighted means are not distinguishable once that is accounted for, and the Note
> says so where it reports them rather than leaving the reader to assume otherwise.

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

**The headline is the null.** There is no support in these data for the concern that published
evaluation is scarcer where more people are exposed. We pre-registered that concern as our
hypothesis and found against it, and the null holds however the comparison is drawn.

**The gate as we ran it compared two different denominators, and we are reporting that rather
than quietly repairing it.** Gate F sets population-weighted coverage against gauge-count
coverage. The population side was computed over all 5,734 basins holding any inventory point and
the gauge side over the 3,090 real gauges, which are different rungs of the ladder below. Our
2026-08-07 amendment reasoned carefully about which rung the gauge side belonged on and never
made the same decision for the population side. The difference it reported, 0.26 points, is
therefore two mismatched denominators very nearly cancelling.

| Comparison | Population-weighted | Counted | Difference |
|---|---:|---:|---:|
| As pre-registered and run, mismatched rungs | 7.57% | 7.83% | 0.26 pp |
| Both on real gauges | 10.54% | 7.83% | 2.71 pp |
| Both on all inventory points | 7.57% | 3.57% | 4.00 pp |

**The verdict is unchanged.** Every matching sits inside the five-point threshold fixed before
any value was read, so H0 stands whichever you take. What changes is the story around it. Matched
on real gauges the difference runs the *other* way from the concern we pre-registered: coverage is
better where people are, 10.5% against 7.8%. Found by the second external reviewer, verified, and
recorded in the protocol as a defect in a pre-registered gate rather than corrected in place, so
that the gate keeps the verdict it actually returned.

One further caution about this comparison, since it is the load-bearing one. The two sides are not
quite the same shape: the population side asks whether a basin holds any evidenced point, while
the gauge side counts gauges. Where a basin holds several points the first runs mechanically
higher. It is a fair comparison and a same-shape one would be fairer.

![Coverage of the published evidence base does not depend on population. Weighted by population
in reach, 7.6%. Counted per gauge on rung 2, 7.8%. Difference 0.26 percentage points against a
Gate F threshold of 5. The figure shows the comparison as pre-registered and run; the two sides
sit on different rungs and the matched versions, 2.71 and 4.00 points, are in the table
above.](figures/fig1-gate-f.svg)

### The absolute level is high, and it is a range rather than a number

Of the 71,248,661 people behind a forecast point in the published African inventory, **between
81.2% and 92.4% are behind none carrying a published per-gauge metric**. We are not able to give
you one number, and the reason is a mistake of ours rather than a property of the world.

The frozen definition of *evidenced* reads the metric tables published for the evaluation period
running from 2014. The same release publishes the same tables for a period running from 1980, and
they carry values for twice as many African gauges, 486 of 741 against 242. Read that way, the
figure is 81.2%. Nobody chose the narrower reading: it was fixed on day two while settling a
different question, and it survived a red team, a claim-ladder pass and a referee rehearsal before
the second external reviewer of this Note found it in a week. Our protocol claims the frozen
definition is the most generous reading available and that where a choice could cut either way we
take the option that flatters the subject. On this axis both claims are false, by eleven points,
in the direction that flatters us.

Our own pre-registered Gate D says that where the primary metric moves by more than ten points
across defensible definitions, no single headline number may be published, and that a range
honestly presented is a publishable result while a point estimate chosen from several is not.
Eleven points is more than ten. So the range is the result.

![The headline is a range because of one choice nobody made deliberately. The African
population behind a forecast point carrying no published per-gauge metric runs from 81.2% to
92.4%. Of the four choices that move that figure, which evaluation period is read moves it 11.2
percentage points, how far downstream the footprint runs moves it 2.1, how strict the definition
is moves it 1.6, and which population surface is used moves it 0.4. Gate D forbids a single
headline figure above 10 points.](figures/fig5-period-range.svg)

| Definition of *evidenced* | African gauges evidenced | P_unevidenced |
|---|---:|---:|
| Evaluation period from 1980, and the union of both | 486 of 741 | **81.2%** |
| Evaluation period from 2014, the frozen definition | 242 of 741 | **92.4%** |

Within the frozen reading the figure is stable: it moves 1.6 points across the stricter
return-period definitions, reaching 94.1% at the five-year reading, and 0.4 points across three
population surfaces. That stability is real and it is also the reason the period problem went
unnoticed for so long, because everything we thought to vary barely moved the answer.

Both of those statements concern coverage, neither concerns skill, and combining them into one
sentence would misrepresent both.

**How far a forecast point reaches, and what happens when you let it reach further.** Our unit
is the level-12 basin holding the point, which is the developer's own geometry and was fixed
before any value was read. Strictly it is the point's own drainage unit rather than its reach,
and we use the plainer word below only where the distinction does not matter. It is a
conservative footprint, because flood waves travel down channel networks and a gauge near a basin
outlet plainly informs people below it. Letting the footprint propagate downstream, one basin at
a time:

| Steps downstream | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P_unevidenced | 92.43 | 91.09 | 90.28 | 90.55 | 90.87 | 90.93 | 91.05 | 91.16 | 91.10 |
| Basins | 5,734 | 7,802 | 9,357 | 10,556 | 11,520 | 12,320 | 13,002 | 13,589 | 14,095 |

The curve reaches its minimum at two steps and turns back, settling near 91%. **Under the frozen
definition of *evidenced*, the figure sits between 90.3% and 92.4% across every footprint from
zero to eight basins downstream**, which is a stronger robustness claim than any single
sensitivity. An earlier draft stopped at two steps, which is exactly where the effect is largest,
and the second external reviewer was right that a reader would be entitled to wonder why. The
full curve is published because it is the honest answer and because it happens to be the better
one for us.

### The answer depends on what you count, so here is every rung

No single denominator survived scrutiny, so the protocol committed in advance to reporting all of
them with the primary metric computed at each.

![Population in reach of no evidenced forecast point at each denominator: basins holding an
evaluated gauge 66.3%, basins holding a real gauge 89.5%, basins holding any inventory point
92.4%, all study-region basins 99.6%.](figures/fig4-denominator-ladder.svg)

| Denominator | Basins | Population in reach | P_unevidenced |
|---|---:|---:|---:|
| Basins holding a gauge that was evaluated | 741 | 16,014,565 | 66.3% |
| Basins holding a real gauge | 2,123 | 51,178,147 | 89.5% |
| Basins holding any inventory point | 5,734 | 71,248,661 | 92.4% |
| All study-region basins | 229,744 | 1,319,838,500 | 99.6% |

Every figure in this table is computed under the frozen definition of *evidenced*, so each is the
upper end of its own range. Read on the 1980 evaluation period the whole column falls by roughly
eleven points. The product's own display surface would be a fifth rung, and because it is not enumerable from
anything in the release we never use it. A reader who prefers a different rung can take it from
this table, and publishing the ladder in place of one number is what makes that possible.

### Most of the geography was settled before any value was read

Coverage falls as mapping density falls, and the pattern is strong enough to invite a
straightforward reading that would be mostly wrong. Beside each figure below is the level it
would sit at if every gauge holding a metric file turned out to be evidenced, separating the part
driven by whether a location was evaluated at all from the part driven by what that evaluation
returned.

![Most of the mapping-density gradient was settled before any value was read. Sparsest third
99.998% against a floor of 99.3%, middle third 99.8% against 95.5%, densest third 91.7% against
75.8%.](figures/fig2-mapping-density.svg)

| Mapping density | Population in reach | P_unevidenced | Floor from file presence | Attributable to content |
|---|---:|---:|---:|---:|
| Sparsest third | 915,349 | 99.998% | 99.3% | 0.7 pp |
| Middle third | 5,192,492 | 99.8% | 95.5% | 4.3 pp |
| Densest third | 65,140,820 | 91.7% | 75.8% | 15.9 pp |

In the sparsest third of African basins by mapping density, nineteen people out of 915,349 live
in reach of an evidenced forecast point. The gradient is real, and it speaks overwhelmingly to
where gauges were evaluated in the first place instead of to what those evaluations returned. Both are absences of published evidence and the frozen definition
counts them together, but they are different mechanisms with different implications, and a
version of this table without its floor column would have been quoted for the wrong one.

That correction applies to the headline as well, since from file presence alone 55,234,096 of the
71,248,661 people in reach live behind no gauge holding a metric file at all, so the primary
metric could not have fallen below 77.5% whatever the contents proved to be. The published values
determined where the answer fell within a 22.5-point band, and not what kind of answer it was.

### Where a metric file exists, African gauges more often carry no value

Of the 741 African gauges holding a metric file, 242 are evidenced, a rate of 32.7% against 59.5%
for the released set as a whole. Because the analysis was first run against permuted labels, we
know that chance alone would have produced 63.3%, so the shortfall is a real association and not
an artefact of which gauges happened to be evaluated. Thirty-six of the 47 African countries
holding a forecast point in the inventory have no evidenced point at all, and 47,633,255 people
live in reach of those points.

This finding concerns publication and not performance, since it establishes only that African
gauges which were evaluated more often carry no released value, and it says nothing whatever
about how those gauges would score if a value existed.

### The pattern follows the gauge archive, which predates the model by a century

Every one of the 741 African gauges holding a metric file is a Global Runoff Data Centre
station, and the evidenced points among them are concentrated to a degree that makes the
geography of this Note largely a geography of that archive.

![The published evidence base follows a century-old gauge archive. South Africa holds 211 of
the 242 evidenced African forecast points, 87.2%, with Liberia, Namibia, Guinea, Lesotho and
Angola holding between 3 and 8 each.](figures/fig3-gauge-archive.svg)

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
weighted by the population of its basin instead of counted once. Our derived F1 for the 1980
datasets under the `kfold_splits` experiment at the five-year return period is 0.262328, which
reproduces the value in the developer's own committed notebook output exactly, so what follows is
commensurable with their reporting and not a parallel construction. F1 is defined as twice
precision times recall over their sum, so deriving it per gauge from the two published values
takes no liberty and involves no approximation. What it is not is a quantity you can average
across gauges and read as the skill facing a person, for the reason the next paragraph gives.

F1 is not published per gauge, since the release carries precision and recall alone, so every F1
here is our harmonic mean of the two, with a null in either input producing a null and never a
zero. Every F1 below is therefore a mean of per-gauge values, and it may not be read as the skill
facing an average person. Those are different quantities, because F1 is not linear in the counts
it comes from, and the second one cannot be computed from this release at all: precision and
recall alone fix a gauge's contingency table only up to a scale factor, and no event or outcome
count is published anywhere in the archive. We asked the developer for those counts in the
questions at the foot of this Note.

For the frozen 2014 `full_run` reading at the two-year return period, **a two-day tolerance
window** and zero-day lead, the unweighted mean across 218 African gauges is 0.385 and the
population-weighted mean is 0.331. The window is named here because it moves the figure further
than anything else available to us, as the cautions below set out.
**Those two numbers are not distinguishable on these data and the Note draws nothing from the gap
between them.** Population weighting concentrates hard: the effective sample size of the weights
is 16.6 against 218 gauges, one basin carries 16.3% of the total weight and the ten largest carry
61.6%, so the weighted figure is in effect an average over about seventeen gauges rather than
218. A bootstrap over gauges puts the unweighted mean at 0.385 with a 95% interval of 0.352 to
0.418, the weighted mean at 0.331 with an interval of 0.201 to 0.499, and their difference at
-0.107 to 0.177, which spans zero comfortably. The first draft of this Note printed the pair
without any of that, and a reader would have taken it as a comparison across 218 gauges.

All three experiments appear side by side in the results file, because reporting the gauged run
alone would describe the model where it was trained, while the locations this Note concerns are
ones where it was not. The cut that speaks to the product's actual use, `continent_splits`, which
holds Africa out entirely, gives 0.347 unweighted against 0.339 weighted at the same reading.

**Degenerate values are not a curiosity at the rare end, and an earlier draft of this Note treated
them as one.** The released code returns a precision or a recall of exactly 1 where no event was
observed and none predicted, so a gauge can score perfectly because nothing happened there. Our
protocol committed on 2026-08-04 to reporting the count at every return period with the figures
both including and excluding them, and the first draft did that only for the fifty-year case. It
matters well before then. The strict count is pairs where precision and recall are both exactly 1;
the broad count is either of them.

| Return period | Gauges | Degenerate, strict | Degenerate, broad | Mean F1 | Excluding strict | Excluding broad |
|---|---:|---:|---:|---:|---:|---:|
| 1.01 yr | 230 | 0 | 0 | 0.326 | 0.326 | 0.326 |
| 2 yr | 218 | 4 | 48 | 0.385 | 0.374 | 0.320 |
| 5 yr | 120 | 21 | 50 | 0.386 | 0.256 | 0.105 |
| 10 yr | 42 | 13 | 18 | 0.449 | 0.202 | 0.107 |
| 20 yr | 15 | 5 | 6 | 0.411 | 0.117 | 0.056 |
| 50 yr | 3 | 3 | 3 | 1.000 | undefined | undefined |

At the metric of record the strict reading moves the mean by 1.1 points and the broad reading by
6.5. Beyond the five-year return period the published mean is dominated by gauges that scored
perfectly because no qualifying event occurred, and by twenty years the figure is built on fifteen
gauges of which a third are degenerate under the strict reading. **Any statement about extreme
events needs its denominator and its degenerate count attached to it, and this Note makes none.**
The one-sided flag that produced the strict column alone was found by external review and
corrected on 2026-08-21.

The other caution is the tolerance window, meaning the slack allowed between a predicted and an
observed threshold crossing. It moves the figure further than any other choice available to us,
from 0.154 at zero days to 0.385 at the two days the paper itself uses.

## Added after review, and none of it pre-registered

Everything in this section was specified after the values were read, on 2026-08-20, and it
carries none of the weight the rest of the Note does. It is separated rather than folded in so
that a reader can see which of our commitments were made blind and which were not. The protocol
records it as §11a, in its own table, because §11 opens by stating that every amendment in it
was made before any metric value was read and appending this to it would have made that sentence
false.

**What prompted it, stated exactly.** An adversarial self-review, written by us against our own
draft from two assumed positions, an operational hydrologist and a forecast-verification
statistician. **No independent reviewer has read this Note.** The two hydrologists our red team
asked for have not been approached. This was a rehearsal, it is worth what a rehearsal is worth,
and it is named here for what it was rather than for the thing it stands in for. Two of the five
points it raised changed what the Note may print, and both corrections are in the sections above
rather than quarantined here.

### The headline survives a harder definition of reach, and moves the way the objection predicted

The frozen definition of *in reach* is the level-12 basin containing the forecast point, which
is the developer's own geometry. The objection is that this is the wrong shape: a river forecast
serves people downstream, the median basin here is 137 km², and evidenced gauges sit on larger
rivers than unevidenced ones, median upstream area 2,651 km² against 1,560 km². Truncating reach
at the basin boundary should therefore drop more population from the evidenced side than from
the unevidenced side, and inflate our figure.

It does, and not by much.

| Reach | Basins in reach | Population in reach | P_unevidenced |
|---|---:|---:|---:|
| Containing basin only, the frozen definition | 5,734 | 71,248,661 | 92.4% |
| One basin downstream as well | 7,802 | 91,227,692 | 91.1% |
| Two basins downstream as well | 9,357 | 104,908,720 | 90.3% |

The frozen figure remains the headline, because it is the one that was fixed before any value
was read, and the objection was right about the direction while the effect is 1.3 points at one
step and 2.2 at two. The first row was recomputed from the topology rather than copied across
from the primary results, and it reproduces 92.43% exactly, which is the only reason the other
two rows are worth reading.

### What the frozen evaluation period cost, and how we came to measure it

This is the largest number in this Note and it was produced by the review process rather than by
us. The frozen definition of *evidenced* reads one evaluation period. The release publishes two.

| Definition | African gauges evidenced | Evidenced globally | P_unevidenced |
|---|---:|---:|---:|
| Period from 2014, frozen | 242 of 741 | 59.5% | 92.43% |
| Period from 1980 | 486 of 741 | 89.0% | 81.22% |
| Union of both, the genuinely most generous reading | 486 of 741 | | 81.22% |

The union equals the 1980 figure exactly, so every gauge evidenced under the frozen definition is
also evidenced under the other, and the second path adds 244 African gauges the first missed.

Measuring this required reading metric values a second time, which this study is built to do only
once. That second read is recorded in `07-admin/UNBLINDED.json` with its reason and its timestamp,
it appears in the run log as a second authorised read, and it did not touch the frozen pipeline:
`01_evidence.py` and `02_primary.py` have not been re-run and their outputs are unchanged.

**We would rather have found this ourselves.** It was raised by the second external reviewer, who
sized it at about seven points from the tables alone before we computed eleven. It had survived a
red team written in week one, a claim-ladder pass that found four other things, a referee
rehearsal, and a first external review. The general lesson is not that our checks were weak, since
several of them worked, but that every one of them examined choices we knew we had made. Nobody
had made this one. It was a restriction inherited on day two while a different question was being
settled, and an unmade decision leaves no trace for a reviewer of decisions to find.

### The shortfall in African evidenced gauges is mostly the evaluation window, by construction

The Note reports above that 242 of the 741 African gauges holding a metric file carry a value
under the frozen definition. An earlier draft called the explanation a mechanism we had
discovered. It is closer to a restatement of the inclusion criterion, and saying so costs us the
better story and is what the data support.

The frozen path evaluates over a period running from 2014. The released code titles the same
figures `2014-2022` for that path and `1980-2021` for the other. A gauge whose daily record ended
before 2014 has no observations inside that window, so no metric can be computed for it however
the evaluation was designed. All 741 match to Global Runoff Data Centre station records, and the
split falls exactly where the window opens:

| Daily record ends | Evidenced | Of | Rate |
|---|---:|---:|---:|
| Before 2014 | 1 | 463 | 0.2% |
| 2014 or later | 241 | 278 | 86.7% |

There are no gauges in this set whose record ends between 2012 and 2014, so the cliff is sharp
rather than a gradient, and it sits on the boundary. **This is what a definitional cut looks like,
not what a dose-response looks like**, and an earlier draft's decadal bins made it appear to be
the second. We have dropped the record-length table that sat beside it, because long records are
old records and the two variables are the same one wearing different clothes.

What is not definitional are the exceptions, and they are the only informative rows here. One
gauge carries a published value despite a record ending in 2002, which under a strict reading
should not exist and suggests the recorded end date is wrong for that station or that a value
reached the table another way. Thirty-seven gauges carry no value despite records running to 2017
or later, so overlapping the window is necessary and not sufficient: a gauge also needs enough
qualifying events inside it. Records ending in 2018 are evidenced at 4 of 15 against 53 of 59 for
2019, which is the shape of a threshold on how much usable overlap there is rather than of a
policy.

This is the same fact as the eleven-point range at the top of this Note, seen from the other side.
The gauges the 2014 window excludes are largely the ones the 1980 window includes, which is why
reading the other path doubles the evidenced count. One choice about evaluation period drives both
numbers.

### A third population surface

The frozen weight is WorldPop unconstrained, which distributes census counts by covariates with
no built-up mask and so places some people on ground nobody lives on. The objection is that
this matters most in the thinly mapped basins, which is where this Note spends much of its
attention. We added WorldPop constrained, which places population only onto detected building
footprints, as a third surface, fetched for all 58 countries in the study region.

**It is admitted for the headline and forbidden everywhere else in this Note, and the reason is
not administrative.** Our mapping-density strata cut basins by how densely OpenStreetMap has
recorded settlement. A population surface derived from detected buildings, used to weight a
comparison against detected settlement, would manufacture the correlation the study exists to
test. That is why unconstrained was chosen on day one, the reasoning has not weakened, and the
protocol now forbids the constrained surface in stratum 3 as a binding rule rather than leaving
it to judgement.

On the headline the three surfaces agree closely. P_unevidenced is 92.3% on the constrained
surface against 92.4% unconstrained and 92.0% on GHS-POP, a spread of 0.4 points across all
three. The constrained denominator is slightly the larger of the two WorldPop readings,
72,075,273 people against 71,248,661, which is what you would expect from a surface that pulls
population onto built-up land, since built-up land in this inventory tends to sit near the
rivers the forecast points are on.

Fourteen basins that hold a forecast point carry no population value on the frozen surface
either, and they are dropped from the primary metric on both sides of the ratio. That is the same
rule and the same reasoning as below, and it is stated here because a Note that makes this much of
the difference between nothing being there and nothing being recorded should not leave its own
fourteen cases in a results file.

One property of the constrained surface has to be stated rather than absorbed. Of the 5,734
basins in reach, 427 carry no constrained value at all, holding 210,705 people on the
unconstrained surface. That is not a country we failed to fetch, because every country was
fetched. It is the surface having no valid pixel anywhere in those basins, and our rule
throughout has been that a basin of nodata is unknown rather than empty. The comparison above
therefore runs over the 5,307 basins where a constrained value exists, and it is reported that
way rather than as a continental figure. The same distinction between nothing being there and
nothing being recorded is the one this whole Note is about, so it would be poor practice to
quietly resolve it in our own favour here.

### The two corrections that are not in this section

The other two points the rehearsal raised changed how numbers already in the Note must be
reported, so they are in the results above rather than here. The population-weighted skill mean
now carries its effective sample size and a bootstrap interval, and the Note no longer draws
anything from the gap between the weighted and unweighted figures. And every F1 here is now
labelled as a mean across gauges rather than as the skill facing an average person, because the
second quantity cannot be computed from what the release publishes.

## What this does not establish

Several inferences a reader might reasonably reach are not supported by any of it.

The model's performance in Africa, or anywhere else, is outside what we can speak to. We
computed no skill value from hydrographs and evaluated no forecast, and the skill figures above
are the developer's own released values recombined.

Nothing here shows that these locations were never evaluated. What it shows is that the 2024
release published no per-gauge value for them, and internal evaluation would be invisible to us
either way.

The system now serving Flood Hub is equally beyond our reach. A second version exists, posted to
EGUsphere in April 2026, whose Africa-specific reporting we could not locate, and we were unable
to establish which version serves the product, an uncertainty we report openly instead of
resolving by assumption.

Coverage being worse where people live is contradicted by our own pre-registered test, so any
reading of the 81.2% to 92.4% range that implies it runs against the result printed immediately
above it.

Why the evaluation set falls where it does is a question we cannot answer. We can show that it
follows the Global Runoff Data Centre archive, and we cannot show what gave that archive its
shape, which is a matter of a century of hydrological infrastructure and not of a model. Nothing
in these data supports treating the distribution as a choice anyone at Google made.

Nor do we claim that no metric has ever been published for these locations anywhere. The
artefacts named at the top of this Note contain none, and we did not survey everything the
developer has ever released.

## Reproduction

```bash
git clone https://github.com/Quantile-Labs/Quantile-Labs-QL-2026-01-flood-coverage-of-evidence
cd Quantile-Labs-QL-2026-01-flood-coverage-of-evidence
python3 _lib/manifest.py QL-2026-01 --verify
python3 04-analysis/01_evidence.py --unblind
python3 04-analysis/02_primary.py --unblind
python3 04-analysis/03_q4_skill.py --unblind

# The post-hoc additions of 2026-08-20, which are not part of the pre-registered result.
# The first re-fetches roughly a gigabyte of population rasters and takes a while.
python3 03-harness/02d_add_worldpop_constrained.py
python3 04-analysis/05_post_review.py

# The second authorised read, 2026-08-21. This one opens metric values, so it requires a reason
# and records itself in 07-admin/UNBLINDED.json.
python3 04-analysis/06_period_sensitivity.py --unblind --rerun-reason "..."
```

Figures are regenerated from the results files by `04-analysis/04_figures.py`, five of them, and
are committed as SVG, so a change to a chart shows up as a reviewable diff and not an opaque binary swap. Every
value plotted appears in the table beside it and in the machine-readable results, so the charts
carry nothing a reader cannot also read as text.

Inputs and checksums are in `02-data/manifests/MANIFEST.csv`, every judgement call is in
`07-admin/DECISIONS.md`, every execution is in `07-admin/RUNLOG.md`, the adversarial review
we ran against ourselves is in `RED-TEAM.md`, and external review of the draft, with every point
we declined and why, is in `REVIEW-LOG.md`. Where our own record is weaker than it appears, and
in two places it is, the logs say so at the point where it is weaker instead of leaving it to be
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
5. Will you publish per-gauge event counts, or the true-positive, false-positive and
   false-negative counts behind the released precision and recall? Without them no one outside
   Google can pool the released metrics correctly, which is what any population-weighted reading
   of them requires.

## Corrections

None to date. Corrections will be published as prominently as the original.
