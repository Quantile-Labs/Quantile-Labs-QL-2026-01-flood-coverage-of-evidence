# Red team — QL-2026-01

The strongest possible rebuttal of this Note, argued in good faith by someone who wants it to be
wrong. **Not a limitations section — a hostile referee report.** Written before anyone else sees
the draft. Published with the Note.

**Pre-mortem written 2026-08-04**, in week one, against protocol v1.2 — before the strata are
built, before any metric value has been read, and while the design can still change. A second
pass runs against the finished draft.

## 1. What would an annoyed expert at the subject organisation say?

> "You have measured the coverage of a supplementary data release, and written it up as though
> you measured the coverage of our product.
>
> The inventory you counted is the gauge table we used to build cross-validation splits for a
> 2024 paper. You established that yourself — it is why your own Gate A resolved the way it did.
> Flood Hub does not serve from that table. It serves ~5,000 verified and ~240,000
> lower-confidence points, none of which appear in your denominator, because they appear nowhere
> in the release. So your headline is a statement about a research artefact dressed in the
> language of people's lives.
>
> Worse, you have measured a **2024** release. The operational system has moved on — v2 trains on
> 15,923 gauges against the 5,680 you are working from. Your map of where the evidence is thin is
> a map of where it was thin two years ago, for a model that may no longer be the one running.
> You say you cannot establish which version serves Flood Hub. Then you cannot establish that
> your finding describes anything anyone is currently relying on.
>
> And the framing is doing work your data does not. 'Whose accuracy has never been published' is
> technically true and rhetorically an accusation. We published Africa's numbers — they are
> recoverable from Figure 4 and the repository, which you found in an afternoon. We disclosed
> that the model is riverine only. We disclosed the F1 range. You have taken a paper that was
> unusually forthcoming about its own limits and used its openness as the raw material for a
> story about opacity."

**How much of this lands: most of it.** The v2 objection and the denominator objection are both
strong and neither is fully answerable. See the disposition table.

## 2. Most defensible alternative explanation for this pattern?

Whatever spatial pattern we find in evidence coverage, the most defensible alternative
explanation is **the historical gauge network, not any decision by the developer.**

Per-gauge metrics can only exist where there is a gauge with a usable observational record. That
network was built over a century by national hydrological services under colonial administration,
war, structural adjustment and drought, and it is dense in South Africa and nearly absent in
Central Africa for reasons that have nothing to do with anyone at Google. If we report that
published evidence is concentrated in South Africa — 273 of 741 evaluated African gauges, 37% —
the honest reading is *that is where the gauges are*, and GRDC record availability is the
confounder that explains it.

A reader who takes our map as an indictment of the developer has misread it, and if the Note
lets them, the Note is at fault, not the reader. This is rung C mechanism and we are black box;
we can *report* the association with GRDC record density and we cannot attribute cause.

**Test that must be pre-committed:** report evidence coverage against GRDC record length and
station density in the same figure as the population weighting. If coverage tracks the gauge
network, say so in the abstract, not in the discussion.

## 3. Which single data choice, if reversed, most changes the result — and did I test it?

**The treatment of the 3,682 `hybas_*` entries. This is the most consequential open choice in
the study, and yesterday's correction may have been an over-correction in the subject's favour.**

On 2026-08-04 I recorded that 6,772 African "gauges" was wrong because 3,682 are `hybas_*`
polygon identifiers with no station code, no site name and no provider station, leaving 3,090
real gauges. Every fact in that sentence is verified. **The inference drawn from it is not.**

Those 3,682 entries are *all* African — they appear on no other continent. They carry
coordinates, HydroBASINS IDs, and 676 carry river names. A table of ungauged prediction points
in Africa is exactly what a model whose entire contribution is *prediction in ungauged basins*
would need. If that is what they are, then they are not noise to be stripped from the
denominator — **they are the single most relevant set of points in the study**, the places with
a forecast and no gauge and therefore no possible published metric.

Reversing this choice moves the African denominator from 3,090 to 6,772 and moves the primary
metric by an amount that could exceed every other design decision combined. It also flips the
direction of the error: excluding them understates unevidenced coverage, including them
overstates the count of things a person could actually see a forecast for.

**Did I test it? No — it is not yet testable, and that is the point of writing this in week
one.** What their `provider = 23` / `data_source = catalogue.csv` designation means is not
established from any primary source. It must be established before the primary metric is
computed, not after.

**→ This becomes Gate H.** See disposition.

Runner-up: the level-12 basin as the definition of "in reach". Reversing it to a 10 km buffer
(Gate C's fallback) changes which population attaches to which point everywhere, and level-12
basins in Africa are large enough that "someone in this basin" and "someone a forecast would
help" are not the same set of people.

## 4. If someone re-ran this and got a different answer, what is the most likely reason?

In descending order of likelihood:

1. **Population surface.** WorldPop and GHS-POP disagree materially in sparsely mapped Africa —
   that is why Gate E exists. A replicator using GHS-POP alone could differ by more than our
   headline's precision. Gate E already commits us to reporting the spread rather than a
   favourite.
2. **The `hybas_*` decision above.** A replicator who reads those 3,682 the other way gets a
   different number and is not wrong to.
3. **Basin polygon vintage.** HydroBASINS/HydroATLAS revisions change level-12 geometry; a
   replicator on a different release assigns different population to the same gauge. **Pin the
   HydroSHEDS version and hash it** — it is not in the Zenodo release and is therefore the one
   major input whose provenance we control entirely.
4. **OSM is a moving target.** Feature density measured in August 2026 is not what it was in
   2024 or will be in 2027. Terciles cut on a live database are not reproducible unless the
   extract date and file hash are fixed. Manifest the Geofabrik extract, do not stream it.
5. **The *evidenced* definition.** Three definitions are pre-registered precisely because this is
   contestable; Gate D suppresses the headline if they diverge by more than 10 points.

## 5. Which sentence would I most regret seeing quoted alone in a headline?

> *"X million Africans live behind flood forecasts whose accuracy has never been measured."*

It is the study's own question restated, it will be the first sentence a journalist lifts, and
**every word of it is defensible except the one nobody will notice: "measured".** Our finding is
about what was *published*, not about what was measured. Google may have measured skill at every
one of those points internally. Absence of a published metric is not absence of measurement, and
"never been measured" asserts something we cannot possibly know from a black-box tier.

Second-worst, and likelier to be written by someone else about us:

> *"Google's flood AI is unproven where Africans need it most."*

That is the sentence the Note exists to not say. The bolded caveat in the limits box will not
stop it. What might: never putting a population figure and a skill figure in the same sentence,
and refusing the word "unproven" in every draft.

**Discipline that follows:** the word **measured** does not appear in the title, abstract, or any
headline claim. The word is **published**. Every instance gets checked in the claim-ladder pass.

## 6. What am I claiming that my access tier does not support?

- **Any statement that a person "relies on" a specific forecast point.** We have no usage data.
  Reliance is inferred from the existence of the service plus two documented anticipatory-cash
  programmes. That is rung B at best, and for the ~240,000 lower-confidence points it is rung C.
- **Any statement about the currently serving model.** We measure a 2024 artefact. Gate A's
  conservative frame handles the inventory; it does not handle the version. See disposition.
- **"Never been published"** — we can show a metric is absent from *this* release. We cannot
  survey everything Google has ever published. The claim must be scoped to the named artefacts.
- **Anything about forecast quality at an unevidenced point.** Foreclosed absolutely, and the
  reason the study's central caveat is in bold.

## 7. What did I not look at, that a reader would assume I had?

- **The Flood Hub product itself.** No screenshot, no gauge list, no API call — the API needs
  approval and serves no history. A reader will assume we looked at the thing we are writing
  about. We must say plainly, early, that we did not, and why.
- **v2.** EGUsphere 2026-2283 exists, its review was stopped on a code-archiving breach, and we
  read none of its artefacts because there are none deposited. Say that.
- **`continent_splits` for Africa** — the Africa-held-out cross-validation, which is the cut that
  actually bears on ungauged African basins. Not in the committed cell outputs; recoverable only
  from the Zenodo pickles. A hydrologist will ask for it first. It is now in scope for Q4.
- **The 14.5 GB `model_data.tgz`.** We deliberately did not download it. That is defensible —
  we make no claim requiring hydrographs — but it must be stated as a choice, not left as a gap.
- **Ground truth of any kind.** By design, and the Note says so in its first paragraph.

---

## Disposition

| # | Issue | Fixed / Disclosed / Rejected | Where |
|---|---|---|---|
| 1 | `hybas_*` entries may be ungauged prediction points, not noise — the correction may over-correct in the subject's favour | **CLOSED 2026-08-04 to the unresolved branch, and it was the right worry.** Both readings are dead: 98% disjoint from gauged basins and complementary in geography (so not bookkeeping); 1.6% of Africa's 224,827 level-12 basins (so not the ungauged surface); `provider 23` undocumented in any primary source. **Two denominators reported, no single headline figure** — and the denominator becomes an explicit four-rung ladder. | PROTOCOL §11, Gate H; §4/§5/§8 |
| 2 | Version: we measure a 2024 artefact, the product may serve v2 | **RESOLVED 2026-08-04 — was "disclosed, no action available", now a citable fact.** The developer's own repository (`google-research/flood-forecasting`, commit `affbaaa`) designates the Nature 2024 architecture the **"Former production model"** and Mean-Embedding-Forecast-LSTM the **"Current production model (as of December 2025)"**. The Note states this with the developer's as-of date, and the premise strengthens: the published per-gauge evidence base pertains to a superseded architecture. | PROTOCOL §11, §1 |
| 9 | *(new)* Weights are public — a reader will ask why we stayed black box | **Disclosed as a choice.** White-box access is available and declined: this Note is about published evidence, not about generating new evidence. Stated in §2 so it does not read as ignorance. | PROTOCOL §2 |
| 10 | *(new)* We would have missed a second published metrics artefact | **Fixed.** `pretrained-models/.../test_metrics.csv`, 10,137 basins, NSE/KGE, **zero African** — and unusable as skill evidence anyway by the developer's own warning of in-sample leakage. Both reasons reported. | PROTOCOL §7, §8 |
| 11 | *(new)* "No African basins in the operational training list" is one sentence from a demolishing over-claim | **Fixed by pre-committing the wording.** May say: the operational model's African behaviour **cannot be independently replicated from released artefacts**. May **not** say: the model was not trained on African data. The constraint is redistribution rights — the 2024 work used 741 African GRDC gauges that cannot be redistributed. | PROTOCOL §8 |
| 12 | *(new)* A Note about missing evidence that ignores what *was* published is not a fair account | **Fixed.** Credit for open-sourcing production architectures, releasing weights, and publishing a blunt anti-misuse warning goes near the front, in our own voice. | PROTOCOL §3 |
| 3 | Denominator is a research inventory, not the serving surface | **Disclosed.** Gate A already forces the conservative frame; the abstract must carry it, not just §10. | Gate A, abstract |
| 4 | "Measured" vs "published" | **Fixed.** "Measured" banned from title, abstract and headline claims. Checked in the claim-ladder pass. | §5 above, claim ladder |
| 5 | Historical gauge network as the alternative explanation | **Fixed.** GRDC record length and station density reported in the same figure as the population weighting, and named in the abstract if coverage tracks the network. | PROTOCOL §9 confounders |
| 6 | HydroSHEDS and OSM vintage not pinned | **Fixed.** Both manifested with hashes and extract dates before use; no streaming. | PROTOCOL §7, MANIFEST |
| 7 | We never looked at the product | **Disclosed** early and plainly, with the reason. | Note, first section |
| 8 | Reliance is inferred, not observed | **Disclosed.** Rung B, and rung C for lower-confidence points. Never stated as fact. | Claim ladder |

~~Items 1 and 2 are the two that could still sink this. Item 1 has an action. Item 2 does not, and
the Note has to live inside it.~~

**Updated 2026-08-04, later still.** Item 1 is closed too — to the unresolved branch, which is
the honest disposition rather than a failure to decide. The pre-mortem's headline demolition
scenario ("our headline excluded the exact locations the study is about") is now structurally
impossible: there is no single headline number to be wrong. The denominator ladder replaces it,
and the four questions in Gate G ask the subject the things no amount of our own work can settle.

**The residual risk has moved.** It is no longer a wrong number; it is a reader who takes the
top rung of the ladder — 741 of 224,827 — as the finding, when what it actually measures is the
distance between an evaluation set and a basin inventory. Every rung needs its own sentence
saying what it is and is not.

**Updated 2026-08-04, hours earlier.** Item 2 is resolved — the developer says in their own
repository which model is in production, and it is not the one whose evidence we are mapping.
**Item 1 (Gate H) is now the only unresolved item that can sink this**, which raises rather than
lowers its priority: it is no longer one of two hazards to be balanced against each other, it is
the hazard.

Item 11 is the new one to watch. "No African basins in the operational training list" is true,
verifiable, and one careless sentence away from an assertion we cannot support. The wording is
pre-committed above for exactly that reason.

---

## Pre-mortem — written in week one, not week eight

*It is three months from now and this Note has been publicly demolished. What happened?*

**The most likely story, told plainly.**

We published a number: some millions of Africans in reach of a forecast point with no published
metric. It was picked up as "Google's flood AI unproven in Africa" within a day, which is the
headline the Note explicitly disclaims and which nobody who repeated it had read past.

Then a hydrologist at Google — or, worse, an independent one with no stake — pointed out that the
3,682 `hybas_` entries we stripped from the African denominator are the model's ungauged
prediction points. Our headline had excluded the exact locations the study is about. The
correction moved the number by more than a third. The lab's first published output had a
factual error in its central figure, and the error ran in the direction of our own thesis.

That is the demolition, and note what it is not: it is not a subtle statistical dispute. It is a
denominator, decided in week one, on an inference we had not verified, recorded in a decisions
log that made it *look* verified because it sat among six things that were.

**Second most likely.** Nobody attacks the arithmetic. Instead the response is *"so what — that's
a 2024 supplementary table, our system serves something else entirely, here is the real
coverage."* And they are right, and their number is better than ours, and the Note's contribution
is retrospectively that it embarrassed someone into publishing what we could not compute. That is
a genuinely good outcome for the world and a bad one for us — **so the Note should say in
advance that it would welcome exactly this**, which costs nothing and removes the sting.

**Third.** The population layer does the work. WorldPop error is largest where mapping is
sparsest, and stratum 3 slices on mapping sparsity, so our headline stratum is the one where the
weights are least trustworthy. Somebody re-runs on GHS-POP and gets a materially different
answer, and our confidence intervals — which cover sampling variation and nothing else — look
like false precision. Gate E was written for exactly this and must not be quietly skipped when
GHS-POP turns out to be tedious to acquire.

**Fourth, and the one that would hurt most.** Nothing is wrong with the Note at all. It is
careful, hedged, correct — and it lands as an attack anyway, because "flood forecast" and
"Africa" and "no published accuracy" in one sentence *is* an attack regardless of the
qualifications around it. Three months later the lab is known as the outfit that went after
Google's flood model, the next subject declines to engage, and the right-of-reply process that
makes this work possible becomes harder for every study after it.

**What this changes now, in week one:**

1. **Gate H before anything else touches the denominator.** The `hybas_*` question is settled
   from primary sources, or the Note publishes two denominators and no headline.
2. **The welcome clause.** The Note states explicitly that if the developer publishes coverage
   figures that supersede ours, that is the outcome we wanted. Written into the draft from the
   first paragraph, not added defensively at the end.
3. **Gate E is non-negotiable.** GHS-POP is acquired in the same session as WorldPop, not left
   as a nice-to-have.
4. **The first paragraph does the disclaiming, not the limits box.** By the time a reader
   reaches a limits box they have already formed the view the headline gave them.
5. **Ask two hydrologists to break it before the right of reply, not after.** Costs social
   capital only, and the failure mode above is precisely the kind a domain reader catches in
   ten minutes and a careful non-specialist never does.
