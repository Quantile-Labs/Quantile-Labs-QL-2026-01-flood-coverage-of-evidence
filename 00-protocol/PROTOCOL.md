# Protocol — QL-2026-01 <title>

**Version:** 1.0
**Published:** <ISO date>
**Timestamp / hash:** <fill on publication — this is what makes it a pre-registration>
**Status:** locked

> Amendments are **appended** to §11, never made by editing the text above. A protocol whose
> history is editable is not a pre-registration.

## 1. Subject and version under test
Exact system, provider, version identifier, and the date window in which it was queried.
A finding is about a version at a time, never "the model."

## 2. Access tier
Black box / grey box / white box. State what we were given, and — explicitly — the claims
this tier forecloses.

## 3. Question and hypotheses
The question, stated so it can be falsified. The null. **What result would falsify our
expectation**, written before we know the answer.

## 4. Unit of analysis
What is the row. Reach, item, response, event.

## 5. Metrics
Primary metric first, singular. Secondary metrics. For each: definition, estimator,
uncertainty method, and the denominator it is computed over.

## 6. Harm threshold
Set here, before analysis. What level of failure constitutes harm, per stratum, and why.
This is the section that stops us picking a threshold that flatters the result.

## 7. Ground truth
Source, its known limitations, and how error in the truth source propagates into the metric.
If truth timing is coarser than the quantity being measured, say so here and say how it is
handled.

## 8. Sample construction and disaggregation
Sampling frame, inclusion and exclusion, and the pre-specified strata. Any slice not listed
here is exploratory and must be labelled as such in the report.

## 9. Statistical approach and uncertainty budget
Estimators, interval method, multiplicity handling, and the known confounders — with an
honest statement of which are handled and which are only reported.

## 10. Decision gates
Pre-committed. Condition → action. Written so a bad answer is a decision, not a negotiation.

## 11. Amendments
| Date | Section | Change | Reason |
|---|---|---|---|

## 12. Conflicts
Every person on the study: financial interests, prior employment, consulting relationships,
personal connections to the subject, its vendors and its regulator. Repeated at publication.
