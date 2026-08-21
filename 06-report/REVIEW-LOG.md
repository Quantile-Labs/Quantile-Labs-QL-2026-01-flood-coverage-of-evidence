# External review — QL-2026-01

**Append only.** Reviews of the draft by people outside Quantile Labs, what they said, and what
changed as a result. Every point is recorded with its disposition, including the points we
declined, with the reason. A reviewer is not an endorser and none of the people below has
approved this Note or is responsible for it.

Distinct from `REPLY-LOG.md`, which records the subject's right of reply. This log is about
technical review before that clock starts.

## Reviewers

| # | Field | Sent | Draft reviewed | Responded | Conflicts declared |
|---|---|---|---|---|---|
| 1 | hydrology | 2026-08-21 | commit `42f301a`, protocol v1.10 | 2026-08-21 | not yet on file |
| 2 | | | | | |

## Reviewer 1, received 2026-08-21

Four points against the four questions we asked, plus a closing recommendation. No error of fact
was found and no new test was proposed. Three points endorse what the draft already does. One
asks for a change and we have made part of it and declined the rest.

### 1. Level-12 basins understate reach. **Accepted in part.**

*"Defensible as a strict, local baseline, but hydrologically conservative... Bringing your 1-to-2
step downstream routing into the primary presentation, rather than keeping it strictly post-hoc,
will head off criticisms that you artificially constrained the spatial footprint of a forecast
point."*

**What we changed.** The downstream figures now appear in the Results section beside the headline
rather than only in the post-review section, with the denominators they imply. A reader meeting
92.4% now sees 91.1% and 90.3% in the same breath.

**What we declined, and why.** We have not made the downstream reading the primary metric. The
containing-basin definition governs because it was frozen before any value was read, and
replacing a primary metric once the values are in view is the specific move pre-registration
exists to prevent. The direction of the change makes no difference to that: the downstream
reading gives a *lower* headline, so adopting it would cost us rather than pay us, and the
argument would be exactly as bad if it paid us. Both readings are printed and the Note says which
is which.

### 2. Separate validation availability from model performance. **Already done, no change.**

The draft carries this in three places: *"This finding concerns publication and not performance"*,
*"That is not a decision by the developer and it should not be read as one"*, and *"Nothing in
these data supports treating the distribution as a choice anyone at Google made."*

**One phrase from the review we have not adopted.** The reviewer describes African hydrometric
decay as *"well-documented"*. It may well be, and we have not read that literature, so writing
"well-documented" would be an unsupported claim about a body of work we have not surveyed. That
is the same failure the first claim-ladder pass caught and removed, where the draft asserted a
concern was "widely held" having surveyed nobody. If we want the stronger sentence we need
citations to put behind it, and until then we report the record-end association we measured and
stop there.

### 3. The derived F1 is exact per gauge; say macro-average when pooling. **Confirmed, already done.**

Independent confirmation that deriving per-gauge F1 from published precision and recall needs no
contingency counts, which is the question we asked. The macro-average statement was added on
2026-08-20 under PROTOCOL §11a and is in the skill section: *"Every F1 below is therefore a mean
of per-gauge values, and it may not be read as the skill facing an average person."*

### 4. Record-end interpretation needs guardrails. **Endorsed, guardrails already present.**

The reviewer's coinage *"metric shadow"* is not adopted. It is vivid, and vivid is the risk: a
shadow implies something cast over a place, which is nearer to a claim about the subject than to
the absence of a published number. **Held open pending reviewer 2.**

### What this review did not do

Recorded because a reader weighing it should know. It found no error, recomputed nothing, and did
not engage the parts of the Note we judge most exposed: the effective sample size behind the
population-weighted skill mean, the choice of denominator rung for the headline, Gate F's
comparator being counted in different units on each side, or the handling of degenerate precision
and recall values at rare return periods. One review that broadly agrees is not the same as a
draft that has been broken, and the second reviewer therefore matters more rather than less.
