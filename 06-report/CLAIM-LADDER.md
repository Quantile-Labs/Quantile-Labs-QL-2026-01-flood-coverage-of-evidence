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
| Title, "thin nearly everywhere, and no thinner where more people live" | A | Both halves are measured quantities. The second is Gate F at 0.26 pp. |
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

## Standing checks, re-run each draft

- `measured` appears only where the Note refuses the word, currently two instances, both of
  them inside the disclaimer.
- `unproven` appears nowhere.
- No sentence contains both a population figure and a skill figure. Checked by parsing and not by reading.
- Every numerical claim reconciles against `05-results/`. Currently 21 of 21.
- No claim about the currently serving model, and the version uncertainty is reported instead
  of resolved.
