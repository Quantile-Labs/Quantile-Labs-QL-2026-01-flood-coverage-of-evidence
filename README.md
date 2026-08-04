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

## Progress

- [x] Feasibility check — **passed 2026-08-03.** Per-gauge metrics join to coordinates and a
      country for 5,678/5,678 gauges globally and 741/741 in Africa.
- [x] Protocol frozen and published — **v1.0, 2026-08-04**, sha256
      `52ed62354fe58577c77661de5d20dc92a2991db84ad126d92c375e245efb71da`, tag
      `QL-2026-01-protocol-v1.0`. Frozen before any metric value was read.
- [ ] Data acquired and manifested
- [ ] Analysis
- [ ] Draft
- [ ] Right of reply — 21 days minimum
- [ ] Published
