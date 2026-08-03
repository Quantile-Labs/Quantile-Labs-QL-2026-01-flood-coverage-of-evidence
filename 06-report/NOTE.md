---
title: "<Title — a claim you can defend, not a question>"
study: QL-2026-NN
type: Note            # Note | Review | Finding
date: <YYYY-MM-DD>
access_tier: black box
protocol_hash: <sha256>
protocol_url: <url>
doi: <reserved DOI>
licence: CC BY 4.0
---

# <Title>

**Access tier:** black box — <what this forecloses, in one clause>.
**System and version:** <exact identifier, and the window in which it was queried>.
**Protocol:** frozen <date>, sha256 `<hash>`, published at <url>.
**Data and code:** <DOI>.
**Conflicts:** <one line, or "None declared" — see CONFLICTS.md>.

> ### Limits of this claim
>
> *Write this box first, before the results section. What this Note cannot establish, stated
> plainly enough that a reader cannot mistake it. Include what the confidence intervals do not
> cover.*

## What was asked

*The question, stated so it could have been answered the other way.*

## What was measured

*Data, sources with retrieval dates, unit of analysis, primary metric, how uncertainty was
computed. Enough that a stranger could rebuild it.*

## Results

*Every figure: interval, denominator, version, date. Only rung A claims in the headline
sentences. Machine-readable results file behind every chart.*

## What this does not establish

*Separate from the limits box: the specific inferences a reader might make that the data does
not support.*

## Reproduction

```bash
git clone <repo> && cd <study>
conda env create -f environment.yml && conda activate <env>
make all
```

*Inputs and checksums: `02-data/manifests/MANIFEST.csv`. Red team: `RED-TEAM.md`.*

## Right of reply

*Who was contacted, when, the window given, and their reply in full and unedited — or a
statement that no reply was received within the window.*

## Corrections

*None to date. Corrections are published as prominently as the original.*
