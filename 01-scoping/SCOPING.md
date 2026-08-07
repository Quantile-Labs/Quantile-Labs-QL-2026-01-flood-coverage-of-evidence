# Scoping — QL-2026-01

Written before the protocol. If the answers rule out an honest
evaluation, the study stops here and DECISIONS.md records why.

**1. Is the system deployed and making consequential decisions?**

Yes. Google Flood Hub is a public, operational river flood forecasting service, and its
outputs are used by third parties to trigger real actions. Two documented examples: anticipatory
cash transfers by GiveDirectly in Kogi State and by the IRC in Benue during the September–October
2024 Niger–Benue floods, released 5–7 days ahead of peak off the Flood API. A household deciding
whether to move on the strength of a forecast point is a consequential decision, and the person
making it has no way to see whether that point's accuracy has ever been measured.

The service surface is far larger than the published evaluation. The Nature paper (Nearing,
Cohen, Dube et al., *Global prediction of extreme floods in ungauged watersheds*, Nature
627:559–563, 2024) reports metrics for 4,089 gauges. The product presents on the order of 5,000
verified points across ~100 countries and ~240,000 lower-confidence points across 150+, with 40
African countries in expert mode. That gap between what is evaluated and what is displayed is the
object of this study.

**2. Does ground truth exist, or can it be built?**

Not required, and deliberately so. This Note does not measure forecast skill, so it needs no
flood-event ground truth — the thing that made the funded version of this work unaffordable. What
it needs is a coverage register: which forecast points have a published per-gauge metric, where
those points are, and how many people live in reach of them. Every input is already published:

- per-gauge metrics and gauge metadata, Zenodo `10.5281/zenodo.10397664`, CC BY 4.0
- population, WorldPop 100 m, CC BY 4.0
- settlement mapping density, OpenStreetMap via Geofabrik, ODbL
- administrative units, GADM / geoBoundaries

Where skill *is* discussed (Q4, the population-weighted distribution), the numbers are the
developer's own released metrics, reweighted. No metric is computed by us from raw hydrographs.

Two truth-adjacent traps are already ruled out. **Inundation History (1999–2020, 128 m) is a
frequency raster — how often each pixel was wet — with no event dates. It is not event ground
truth** and is admissible only for water masking, normal-extent priors and exposure weighting.
And the Flood API serves no historical forecasts, so no retrospective skill claim can be built
from it.

The real limitation is not truth, it is exposure: WorldPop is itself a model with spatially
structured error, and that error is largest in exactly the sparsely mapped places this study
stratifies on. That belongs in the uncertainty budget and the limits box, not in the interval.

**3. What access is obtainable, and therefore what could this establish?**

Black box, and in fact less than black box: no system is queried at all. The study reanalyses
published artefacts. The trained models and model data are on Zenodo but are not downloaded and
not used.

What this can establish (rung A — directly measured): how many African forecast points carry a
published metric and how many do not; where each sits; what population lives in reach of each
class; how published skill distributes when weighted by population exposed rather than counted
per gauge; and whether the presence of a published metric covaries with mapping density and
population.

What this forecloses, and what must therefore never appear in the Note: any statement about
whether the model is accurate at an unevaluated point, and any statement about *why* the
evaluation set falls where it does. Both are mechanism, and mechanism is unavailable at this
tier. **Absence of a published metric is not evidence of poor skill.**

One version question is open and may not be resolvable: v2 exists (Cohen et al., EGUsphere
2026-2283, 29 April 2026 — ME-LSTM, Caravan training 5,680 → 15,923 gauges, GraphCast forcings),
Africa is not reported separately in it, and referees on the open review flag ambiguity about
what is operational in Flood Hub versus what is in the paper. Every claim is date-stamped to a
named version; where the serving version cannot be established, the Note says so rather than
guessing. That uncertainty is a reportable observation, not a blocker.

**4. Does any conflict disqualify us?**

No. See `CONFLICTS.md` — none declared, refreshed at publication. No funding was received for
this study from any party. The subject is a Google product and Google.org funded the
GiveDirectly and IRC programmes cited above; neither relationship touches us.

The nearer risk is not a conflict but a posture. This Note is not a rebuttal of the Nature paper
— that paper discloses Africa F1 of 0.15–0.21 at the 5-year return period itself, and its scope
statements (riverine only; no claim for pluvial, flash or dam-related flooding) are explicit. The
finding sits between that disclosure and the deployment surface, and the Note says so in its first
paragraph.

**5. Would the finding be publishable whatever it concluded?**

Yes, and this is the question the study turns on.

The framing is symmetric because it is about coverage of evidence, not about skill. If most
African forecast points that people actually see turn out to be backed by a published metric, that
is a genuine and publishable result — it retires a concern that is widely assumed and never
checked, and it is a credit to the developer. If they are not, that is the map of where the
evidence is thin, which is useful to the developer and to anyone relying on the service.

Q4 carries the same symmetry and is the reason to run it. A gauge protecting two million people
and one protecting two thousand count equally in the paper's per-gauge distributions. Reweighted
by population exposed, the distribution may look better than the per-gauge figure, or worse. **I
do not know which, and the protocol is frozen before I can find out.** If I did know, the result
would already have been decided.

The failure mode that would make this unpublishable is not a null result — it is a null result
smuggled in as an accusation. The decision gates in the protocol name the abandonment condition
explicitly, and the limits box is written before the results section.

---

**Decision:** proceed
**Date:** 2026-08-03
**Conditional on:** the day-1 join check — per-gauge metrics must join to coordinates and a
country. If it fails, this decision is superseded in `07-admin/DECISIONS.md` and QL-2026-04
opens instead. **Condition satisfied 2026-08-03**: 5,678/5,678 globally, 741/741 Africa.

---

## Correction — 2026-08-04

Appended rather than edited above, so the error and its correction are both visible.

**Question 4 above states that the Nature paper "discloses Africa F1 of 0.15–0.21 at the 5-year
return period itself". This is wrong.** Those two numbers are the **South America** row read
across two different models. The true values at the 5-year return period, 0-day lead, verified
from committed cell outputs in `figure_4_continent_reliability_scores_distributions.ipynb`
(repository pinned at commit `1e88caf`, manifested):

| | GloFAS | AI model |
|---|---|---|
| **Africa** | **0.169748** | **0.262328** |
| South America | 0.147253 | 0.210967 |
| Asia | 0.241195 | 0.275652 |
| North America | 0.246691 | 0.357473 |
| Europe | 0.319904 | 0.385691 |
| South West Pacific | 0.302418 | 0.456442 |

Africa is **not** the lowest-scoring continent — South America is — and at the 5-year return
period the AI model's African mean is roughly 55% above GloFAS's.

**The consequence for the posture of this study.** The paper's *text* discloses no Africa F1
anywhere. Figure 4 is boxplots, so the continent means are in neither the article nor the
Extended Data; they exist in the companion repository's committed cell outputs and are
recomputable from Zenodo. So the defensible statement is that **Africa's performance is
recoverable from the published artefacts** — citing Fig. 4 and the repository — and **not** that
the paper stated Africa's score.

This narrows the "not a rebuttal" claim without weakening it. The Africa result that *is* in the
paper's text is the null at the 1-year return period, where the AI model does not beat GloFAS
(mean difference 0.004197, p = 0.069605, d = 0.028121). Which return period is cited changes the
story considerably, and the Note must be explicit about which one it means every time.

The answer to question 5 is unaffected: the study remains publishable whatever it concludes.

---

## Verification — 2026-08-07

Appended, not edited. The 2026-08-04 correction above was itself flagged in `DECISIONS.md` as
needing direct verification against the paper rather than against a summary, because the
"not a rebuttal" posture rests on it. That verification is now done, from two primary sources
independently: the paper's open-access full text, and the committed cell outputs in the
manifested repository tarball at commit `1e88caf`.

**The correction above is confirmed, including its negative claim.** Read directly from the
paper: there is no numeric F1 for Africa anywhere in the main text, there is no per-continent
table of scores in the text or the Extended Data, Extended Data Table 1 lists metric *types*
rather than continent results, and Figure 4 is boxplots carrying no printed continent means.
Every per-continent number therefore exists only in the companion repository's committed cell
outputs and in what is recomputable from Zenodo, exactly as the correction said.

**The paper says two things about Africa's performance and no more.** The first is qualitative
and is the load-bearing one for this Note's framing:

> we were able to use AI-based forecasting to improve the skill of forecasts in Africa to be
> similar to what are currently available in Europe.

The second is in the Figure 4 caption, listing the exceptions to the AI model scoring higher
everywhere: *"Africa over 1-year return period events (P = 0.07, d = 0.03)"*. Those values match
cell 27 of `figure_4_continent_reliability_scores_distributions.ipynb` to the precision printed,
`pvalue=0.06960462965045766` and `0.02812128519231496`, which confirms the 2026-08-04 reading of
that cell.

**A provenance qualifier the correction above omits, and which the Note must carry.** The
Figure 4 continent means come from the **1980** datasets and, for the AI model, from the
**`kfold_splits`** experiment: cell 21 reads `f1s_by_lead_time['glofas_1980']` and cell 23 reads
`f1s_by_lead_time['google_1980']['kfold_splits']`, both at lead time 0. Our own metric of record
is `google/2014/dual_lstm/full_run`. **These are different datasets and different experiments,
so the two sets of numbers are not directly comparable and must never be placed in the same
column without saying so.** The three-way reporting already required for Q4 exists precisely to
make the comparable one available.

Figure 4 covers return periods 1.01, 2, 5 and 10 only, `RETURN_PERIODS[:-2]` in cell 25, which
matches the paper's text discussing 1, 2, 5 and 10-year events and never 20 or 50. The paper's
"1-year" is the code's `1.01`.

**Noted, not resolved here:** the developer's own notebook contains the test of the Europe
parity claim, cell 25, "Test Against GloFAS Europe", run for Africa at each return period. Its
outputs are committed. Whether the recoverable numbers support the sentence quoted above is a
question this study can answer, and it belongs to Q4 after unblinding rather than to scoping.
Recorded now so that the question is visibly one we arrived at before seeing our own results.
