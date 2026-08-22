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
| 1 | hydrology | 2026-08-21 | commit `42f301a`, protocol v1.10 | 2026-08-21 | none, 2026-08-22 |
| 2 | hydrology and forecast verification | 2026-08-21 | commit `42f301a`, protocol v1.10 | 2026-08-21 | none, 2026-08-22 |

Both reviewers declared no relationship with Google or Alphabet, recorded 2026-08-22 and set out
in `01-scoping/CONFLICTS.md` alongside our own.

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

## Reviewer 2, received 2026-08-21

Nine points, every checkable one verified independently before being acted on, and every one
correct. Two are live breaches of pre-registered commitments, one is a defect in a pre-registered
gate, and one changes the headline. This review found more than our red team, our claim ladder,
our referee rehearsal and reviewer 1 combined.

### 1. Gate F compares two different denominators. **Accepted.**

Verified: the population side is rung 2b and the gauge side is rung 2. Matched, the difference is
2.712 pp on rung 2 and 4.000 pp on rung 2b, against the 0.26 pp reported. **The verdict survives
both matchings.** The reviewer also spotted that our 2026-08-07 amendment reasoned about the rung
for the gauge side and recorded the population side as fixed without ever deciding it. All three
figures are now in the Note with a table, the gate keeps the verdict it returned, and the protocol
records it as a defect rather than repairing it in place.

### 2. The frozen definition of *evidenced* is not the most generous available. **Accepted, and it is the largest finding since unblinding.**

Verified and then measured on a second authorised read. P_unevidenced is 92.43% on the frozen 2014
path and **81.22%** on the 1980 path, a shift of 11.21 pp against the reviewer's indicative 7. The
Note now leads with the range. §5's claim that the frozen definition is the most generous reading,
and that we take the option flattering the subject, is false on this axis in the direction that
flattered us.

### 3. The downstream curve turns at two steps. **Accepted.**

Reproduced to the decimal: 92.43, 91.09, 90.28, 90.55, 90.87, 90.93, 91.05, 91.16, 91.10. We had
published the minimum. The full curve is now in the Results section and it is the stronger claim,
so the correction costs nothing and removes an attack. The naming point is taken: the unit is the
point's own drainage unit and the Note says so.

### 4. The GRDC framing is overstated in the specifics. **Accepted.**

Verified: 32 African countries hold a metric file, 11 hold a published value, South Africa is 36.7%
of filed gauges and 87.2% of evidenced points. The archive's spatial footprint is broad and its
calendar is narrow, and the opening now says that instead of the looser claim it made.

### 5. Stop calling the F1 derivation a recombination. **Accepted.** It is the definition of F1 and takes no liberty.

### 6. Degenerate values are a live breach of the 2026-08-04 commitment. **Accepted.**

The commitment was to report the count at every return period with figures including and excluding.
The draft did it only for the fifty-year case. Now a full table. The reviewer also found the
degeneracy flag one-sided and judged it minor. It is not: under the broad reading the metric of
record moves 0.385 to 0.320, against 0.374 under the strict reading.

### 7. The tolerance window is not named where the number is. **Accepted.**

### 8. The record-end result may be definitional rather than an association. **Accepted, and it is.**

Confirmed from the released code, which titles the two paths `2014-2022` and `1980-2021`. Split at
the window boundary rather than by decade: **1 of 463** evidenced where the record ends before
2014, **241 of 278** where it ends 2014 or later, with no gauges ending between 2012 and 2014. The
section now says it is definitional, the decadal bins are gone, the record-length table is dropped
as confounded with end year, and the exceptions are characterised: one gauge evidenced with a
record ending 2002, and thirty-seven unevidenced despite records running to 2017 or later.

### 9. Smaller items. **All accepted.**

The one-sided flag, the fourteen basins with no population value now in the Note's own text, and
the note that Gate F's two sides are not the same estimand even when matched.

### The credit paragraph

The reviewer found that the paragraph PROTOCOL §11 calls "not optional" was absent from the Note
entirely. It is now in the opening: open-sourced architectures, released weights, the published
warning against misuse, and the point that this Note exists because of a decision to publish that
most of the field has not made.

### Assessment

Reviewer 1 endorsed the draft and found nothing. Reviewer 2 found nine things, all real. That is
worth recording plainly, because "two hydrologists reviewed it" would suggest two comparable
inputs and they were not comparable. If a third reviewer is available, the marginal value of one
more looks high rather than low.
