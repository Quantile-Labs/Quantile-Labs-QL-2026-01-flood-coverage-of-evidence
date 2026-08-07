---
title: "<Title, a claim you can defend, not a question>"
study: QL-2026-01
type: Note            # Note | Review | Finding
date: <YYYY-MM-DD>
access_tier: black box
protocol_hash: b05c0b932ddb9c6db2f192ff5804570197470175e50ed21ce7520839321d2248
protocol_url: https://github.com/Quantile-Labs/Quantile-Labs-QL-2026-01-flood-coverage-of-evidence
doi: 10.5281/zenodo.21822781          # this version; concept DOI 10.5281/zenodo.21822780
licence: CC BY 4.0
# Anchors, and the limit of what they establish. The protocol hash above is stamped into the
# Bitcoin blockchain (00-protocol/PROTOCOL.md.ots) and the repository is archived at Software
# Heritage as swh:1:snp:5918a1abf7ffa5d946009a89a9c8a6be4fa1eed5. All three anchors were made
# on 2026-08-06, so that is the externally verifiable date, and the 2026-08-04 freeze recorded
# against protocol v1.0 is our own record rather than an attested fact. Say so in the Note.
---

# <Title>

**Access tier:** black box, <what this forecloses, in one clause>.
**System and version:** <exact identifier, and the window in which it was queried>.
**Protocol:** frozen <date>, sha256 `<hash>`, published at <url>.
**Data and code:** <DOI>.
**Conflicts:** <one line, or "None declared", see CONFLICTS.md>.

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

*Who was contacted, when, the window given, and their reply in full and unedited, or a
statement that no reply was received within the window.*

## Corrections

*None to date. Corrections are published as prominently as the original.*
