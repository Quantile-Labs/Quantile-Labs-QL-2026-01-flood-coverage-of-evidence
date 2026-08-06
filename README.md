# QL-2026-01 — Coverage of evidence: Google Flood Hub

**Type:** Note · **Access tier:** black box · **Status:** pre-registered

## Question

How many people live in reach of a river forecast whose accuracy has never been published?

A reanalysis of the developer's own released per-gauge metrics, weighted by population
exposed and stratified by settlement mapping density.

**This study makes no claim about the model's accuracy anywhere.** Absence of a published
metric is not evidence of poor skill.

## Sources

| Source | Licence |
|---|---|
| Zenodo `10.5281/zenodo.10397664` — per-gauge metrics and metadata | CC BY 4.0 |
| WorldPop, 100 m | CC BY 4.0 |
| OpenStreetMap, via Geofabrik | ODbL |
| GADM / geoBoundaries | free |

## Verifying the pre-registration yourself

The claim that matters is that the protocol was fixed **before** any metric value was read.
You do not have to take that on trust.

```sh
# The protocol as first frozen, 2026-08-04, before any metric value existed:
git show QL-2026-01-protocol-v1.0:00-protocol/PROTOCOL.md | shasum -a 256
# -> 52ed62354fe58577c77661de5d20dc92a2991db84ad126d92c375e245efb71da

# The current protocol — same frozen text, with amendments appended to §11:
shasum -a 256 00-protocol/PROTOCOL.md && cat 00-protocol/PROTOCOL.sha256
# -> ea0a1ac42f31fd0919f01a82d358e6dda152e79f79fe16f250599b9799664e95

# What changed between any two versions, and when:
git diff QL-2026-01-protocol-v1.0 QL-2026-01-protocol-v1.8 -- 00-protocol/PROTOCOL.md
```

Amendments are **appended** to §11 and the frozen text above it is never edited, so every
version remains verifiable at its own tag. `07-admin/RUNLOG.md` records every execution and
`07-admin/DECISIONS.md` every judgement call, both append-only. Where the record is weaker
than it looks — a reconstructed run-log row, a safeguard that turned out to be inert — it
says so at the point where it is weaker.

## Reproducing

Data is not in this repository: raw inputs are ~700 MB and interim products are larger.
Every input is re-fetchable from the URL and sha256 recorded in
`02-data/manifests/MANIFEST.csv`, which is the published artefact. Verify what you have with:

```sh
python3 _lib/manifest.py QL-2026-01 --verify
```

`_lib/` is vendored into this repository so a plain clone runs. Rows marked `transient` were
hashed on arrival and then deleted by design — the streaming harness never holds more than
about a gigabyte at once — so they verify as absent rather than as missing.

## Progress

- [x] Feasibility check — **passed 2026-08-03.** Per-gauge metrics join to coordinates and a
      country for 5,678/5,678 gauges globally and 741/741 in Africa.
- [x] Protocol frozen — **v1.0, 2026-08-04**, sha256 `52ed6235…`, tag
      `QL-2026-01-protocol-v1.0`. Frozen before any metric value was read. Now at **v1.8**,
      sha256 `ea0a1ac4…`; all eight versions are tagged.
- [x] Data acquired and manifested — Zenodo release, HydroBASINS, geoBoundaries, WorldPop,
      GHS-POP and 51 Geofabrik extracts.
- [x] Strata frame built **blind** — 230,028 African level-12 basins; all five strata that do
      not require a metric value are populated.
- [ ] Analysis — **not started. No metric value has been read.**
- [ ] Draft
- [ ] Right of reply — 21 days minimum
- [ ] Published
