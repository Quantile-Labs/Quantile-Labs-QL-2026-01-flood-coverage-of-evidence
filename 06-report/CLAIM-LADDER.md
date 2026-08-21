# Claim ladder for QL-2026-01

PROTOCOL §9 requires every substantive sentence in the Note to be labelled **A** (measured),
**B** (inferred, with assumptions named), or **C** (interpretation), and it restricts the title,
the opening, and anything quotable to rung A. This study is black box, so §9 adds that any
sentence explaining *why* is rung C at best and is a candidate for cutting.

Pass run 2026-08-12 against `NOTE.md` at first full draft, before the right of reply.

## Verdict

Four rung violations found, all four fixed. Two were omissions instead of overreach, and the
more serious of the two would have been very hard to correct after publication because it
concerned what the Note failed to say and not what it said.

## The four

**1. The most defensible alternative explanation was missing entirely.** `RED-TEAM.md` §2 names
the historical gauge network as the explanation a reader must be given, and PROTOCOL §11
(2026-08-04) pre-committed to naming it *in the abstract* and not the discussion if coverage
turned out to track it. Coverage tracks it emphatically: all 741 African gauges holding a metric
file are GRDC stations, and 211 of the 242 evidenced points, 87.2%, are in South Africa. The
draft mentioned none of this. **Fixed** by adding it to the opening, adding a results subsection
reporting the association at rung A, and adding a rung boundary in *What this does not establish*
stating that we cannot attribute its cause.

This is the failure the red team predicted in its own words: *"A reader who takes our map as an
indictment of the developer has misread it, and if the Note lets them, the Note is at fault, not
the reader."* The draft was letting them.

**2. "That concern is widely held" was an unsupported claim about the discourse**, rung C
wearing the clothes of background, and we surveyed nobody. **Fixed** by replacing it with what
we can support, that we pre-registered the concern as our hypothesis and found against it.

**3. `RED-TEAM.md` §7 requires the Note to say plainly and early that we never looked at the
product, and why.** The draft said we queried no system but never gave the reason, leaving a
reader to assume we chose not to bother. **Fixed** in the opening: the API requires approval and
serves no history.

**4. The section heading "What was measured" collided with the word the study bans.** The word
is *published*, enforced in this pass, and a heading using *measured* about our own procedure sat
one line above a paragraph explaining why the distinction matters. **Fixed**, renamed to *What
was computed*.

## Rung assignment of the load-bearing sentences

| Sentence, abbreviated | Rung | Note |
|---|---|---|
| Title, a noun phrase naming the object of study | A | Asserts nothing, so it cannot overreach. The finding moves to the standfirst beneath it, which is rung A: Gate F at 0.26 pp and the 92.4% share. |
| Population-weighted coverage 7.6% against gauge-count 7.8% | A | Primary comparison, pre-registered threshold. |
| 92.4% of 71,248,661 people in reach carry no published metric | A | Frozen definition, denominator on the figure. |
| Moves to 94.1% under the strictest definition, spread 1.6 pp | A | Pre-registered sensitivity. |
| Nineteen people of 915,349 in the sparsest tercile | A | Reported unrounded precisely because 100% was the quotable version. |
| Structural floor of 77.5% from file presence alone | A | Computed from day-one information, no value read. |
| 242 of 741, against 59.5% globally and a permuted null of 63.3% | A | The null baseline is what makes it a claim and not a number. |
| All 741 are GRDC stations; 87.2% of evidenced points in South Africa | A | Read from the released inventory. |
| Derived F1 0.262328 reproduces the developer's committed output | A | Exact to six decimal places. |
| Unweighted 0.385 against population-weighted 0.331 | A | Developer's released values, our harmonic mean, stated as ours. |
| "The ceiling was set by hydrological infrastructure long before any model was trained" | **B** | Inference from the GRDC dependency. Assumption named in the same paragraph. Not in the opening. |
| GHS-POP and WorldPop differ by mechanism, detection against covariates | **B** | From product documentation, not measured by us. Limits box only. |
| "The African record was assembled through colonial administration, war, structural adjustment, and drought" | **C** | Historical interpretation. Retained because it protects the subject, and it is not quotable as a finding. |
| Any statement about why the evaluation set falls where it does | **absent** | Foreclosed at this tier. Explicitly disclaimed rather than written. |

## Second pass, 2026-08-20, against the post-review draft

A rehearsal for external review, written by us against our own draft from two assumed positions.
**No independent reviewer has read this Note.** Five substantive points, all acted on, recorded
as PROTOCOL §11a. Two of them were rung violations of a kind the first pass did not look for,
because both concerned a number that was correctly computed and incorrectly framed.

**5. A comparison was printed at rung A that the data support only at rung B, and arguably not
at all.** The draft gave the unweighted mean F1 as 0.385 and the population-weighted mean as
0.331 across 218 African gauges, with no uncertainty on either. The weights concentrate so hard
that the effective sample size is 16.6, and a bootstrap puts the difference at -0.107 to 0.177.
**Fixed** by publishing the effective sample size and the intervals, and by stating that the two
are not distinguishable and that the Note draws nothing from the gap. The lesson is narrower
than it looks: §9 refuses intervals on population shares for a good reason, and that refusal was
carried across to a quantity where it did not apply.

**6. "F1" was used for a quantity the reader would understand as a different one.** Every F1
here is a mean of per-gauge values, not the skill facing an average person, and the second
cannot be computed from a release that publishes precision and recall without counts. **Fixed**
in the skill section, with the missing counts added to the right-of-reply questions.

Two further points changed the Note without changing a rung: the downstream-reach sensitivity
and the record-end join, both reported in their own section marked as post-hoc. One point was
refused in part, on the grounds that a settlement-derived population surface may not be used to
weight a comparison against settlement mapping density.

### Rung assignment of the sentences added since the first pass

| Sentence, abbreviated | Rung | Note |
|---|---|---|
| P_unevidenced is 91.1% one basin downstream and 90.3% two | A | Computed. Reported beside the frozen 92.4%, never in place of it. |
| 0 of 146 evidenced where the record ends in the 1980s, 241 of 281 where it ends in 2010 or later | A | Read from GRDC station metadata, all 741 matched. |
| "A gauge whose observations stop in 1991 cannot be scored against a test period two decades later" | **B** | Inference, and the assumption is stated in the same paragraph. Not in the opening, not in the standfirst. |
| "The archive stopped recording across much of Africa when the institutions that fed it were cut" | **C** | Historical interpretation, retained because it protects the subject and is not quotable as a finding. |
| Weighted and unweighted skill means are not distinguishable | A | Bootstrap, seed and draws recorded. |
| A micro-average F1 cannot be derived from the release | A | Established from the archive's own contents, not asserted. |
| Any claim that the weighted mean is lower than the unweighted one | **absent** | Was rung A in the first draft, is not supported, and has been removed rather than hedged. |

## Third pass, 2026-08-21, after the second external review

The pass that mattered. The second reviewer found nine things, all verified, and two of them were
rung violations of the most serious kind available to this study: a headline number presented at
rung A that a defensible alternative definition moves by eleven points, and two pre-registered
commitments the draft did not keep.

**7. The headline was a point estimate that could not survive its own Gate D.** 92.4% was rung A
and stated as a fact about the world. It is a fact about one evaluation period, chosen without
argument, and the other period the release publishes gives 81.2%. **Fixed** by leading with the
range in the title area, the standfirst, the limits box and the results, and by saying in the
Note's own voice that the narrowing was our error and a reviewer found it.

**8. Two pre-registered commitments were unkept, and unkept commitments are worse than absent
ones.** The 2026-08-04 amendment required degenerate counts at every return period with figures
including and excluding; the draft gave the fifty-year case only. The same day's amendment called
the credit paragraph "not optional"; it was absent entirely. **Both fixed.** Recorded here rather
than only in `DECISIONS.md` because a claim ladder that checks what the Note says, and never what
the Note promised to say, is checking half the thing.

### Rung assignment of the sentences added or changed in this pass

| Sentence, abbreviated | Rung | Note |
|---|---|---|
| "Between 81.2% and 92.4%" | A | Both ends computed. Neither is a point estimate and the Note never picks one. |
| 486 of 741 African gauges evidenced on the 1980 path against 242 | A | Second authorised read, disclosed. |
| "Our protocol claims the frozen definition is the most generous reading and on this axis that is false" | A | A claim about our own document, checkable against it. |
| P_unevidenced sits between 90.3% and 92.4% across zero to eight steps downstream | A | Full curve published. |
| 1 of 463 evidenced before 2014, 241 of 278 after | A | Join to GRDC metadata, all 741 matched. |
| "This is what a definitional cut looks like, not a dose-response" | **B** | Inference from the code's own period labels, `2014-2022` and `1980-2021`, named in the same paragraph. |
| Gate F matched gives 2.71 pp and 4.00 pp, verdict unchanged | A | Recomputed from the ladder already in the results file. |
| Broad degeneracy moves the metric of record from 0.385 to 0.320 | A | Both readings printed, neither called the truth. |
| The credit paragraph | **C**, deliberately | A judgement that the release is more open than the field's norm. Kept because §11 requires it and because it is true. |
| "The archive's spatial footprint is broad and its calendar is narrow" | A | 32 countries with files, 11 with values. |
| Any single headline number | **absent** | Foreclosed by Gate D once the eleven-point spread was measured. |

## Standing checks, re-run each draft

- `measured` appears only where the Note refuses the word, currently two instances, both of
  them inside the disclaimer.
- `unproven` appears nowhere.
- No sentence contains both a population figure and a skill figure. Checked by parsing and not by reading.
- Every numerical claim reconciles against `05-results/`. Currently 21 of 21 in the
  pre-registered sections, and 35 of 35 across the post-review section and the two corrected
  paragraphs, checked against `post_review.json` by parsing rather than by reading.
- Nothing in the post-review section is quoted in the title, the standfirst or the
  opening, and the section says in its first sentence that it is not pre-registered. The one
  exception is deliberate: the range now leads the standfirst, because Gate D requires it to.
- Every figure is generated from a results file, and every value plotted appears in the table
  beside it. The downstream curve is stored in `post_review.json` rather than computed for the
  chart, checked at all nine points.
- No claim about the currently serving model, and the version uncertainty is reported instead
  of resolved.
