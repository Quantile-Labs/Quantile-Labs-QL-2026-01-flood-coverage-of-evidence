# QL-2026-01: Coverage of evidence, Google Flood Hub

**Type:** Note · **Access tier:** black box · **Status:** pre-registered

## Question

How many people live in reach of a river forecast whose accuracy has never been published?

This is a reanalysis of the developer's own released per-gauge metrics, weighted by the
population exposed behind each forecast point, and stratified by settlement mapping density so
that the answer can be read separately for well mapped and thinly mapped ground.

**This study makes no claim about the model's accuracy anywhere.** The absence of a published
metric is not evidence of poor skill, and any reader who comes away thinking that unmeasured
means unreliable has been misled rather than informed.

## Sources

| Source | Licence |
|---|---|
| Zenodo `10.5281/zenodo.10397664`, per-gauge metrics and metadata | CC BY 4.0 |
| WorldPop, 100 m | CC BY 4.0 |
| OpenStreetMap, via Geofabrik | ODbL |
| GADM and geoBoundaries | free |

## Verifying the pre-registration yourself

The claim that carries the weight of this study is that the protocol was fixed **before** any
metric value was read, and you do not have to take that claim on trust, because everything
needed to check it is in this repository.

```sh
# The protocol as first frozen on 2026-08-04, before any metric value existed:
git show QL-2026-01-protocol-v1.0:00-protocol/PROTOCOL.md | shasum -a 256
# -> 52ed62354fe58577c77661de5d20dc92a2991db84ad126d92c375e245efb71da

# The current protocol, which is the same frozen text with amendments appended to §11:
shasum -a 256 00-protocol/PROTOCOL.md && cat 00-protocol/PROTOCOL.sha256
# -> b05c0b932ddb9c6db2f192ff5804570197470175e50ed21ce7520839321d2248

# What changed between any two versions, and when it changed:
git diff QL-2026-01-protocol-v1.0 QL-2026-01-protocol-v1.9 -- 00-protocol/PROTOCOL.md
```

### Independent anchors, which do not rely on this repository

Git commit and tag dates are set by whoever makes the commit, so they are self-asserted and a
reader is right to discount them. Three anchors outside our control fix that. They cover
**protocol v1.9, sha256
`b05c0b932ddb9c6db2f192ff5804570197470175e50ed21ce7520839321d2248`**, and every earlier
version is anchored at its own tag:

- **OpenTimestamps**, in `00-protocol/timestamps/`, one proof per protocol version, which
  anchors each version's hash into the Bitcoin blockchain with no reference to us or to
  GitHub. The v1.8 proof is confirmed in **blocks 961285, 961287, 961288 and 961333**. Each
  proof covers the protocol text at its own tag rather than the current file, so verify it
  against that text:

  ```sh
  git show QL-2026-01-protocol-v1.8:00-protocol/PROTOCOL.md > /tmp/v1.8.md
  ots verify -f /tmp/v1.8.md 00-protocol/timestamps/PROTOCOL.v1.8.md.ots
  ```

  Full verification reads the Bitcoin block headers, so it wants a local node or a block
  explorer. `ots info` on the proof shows the attested block heights without either.
- **Software Heritage**, snapshot `swh:1:snp:5918a1abf7ffa5d946009a89a9c8a6be4fa1eed5`,
  archived 2026-08-06, which preserves the entire history independently of GitHub.
- **Zenodo**, [10.5281/zenodo.21843331](https://doi.org/10.5281/zenodo.21843331) for v1.9,
  holding the protocol, its hash file, both timestamp proofs, and a full repository archive
  under a citable DOI. The concept DOI [10.5281/zenodo.21822780](https://doi.org/10.5281/zenodo.21822780)
  always resolves to the newest version, and v1.8 remains citable at
  `10.5281/zenodo.21822781`. The deposited `PROTOCOL.md` has been downloaded back from the
  record and confirmed byte identical to the one in this repository.

**Be clear about what these do and do not establish.** Each anchor proves the protocol existed
in that exact state on the day it was made, which is 2026-08-06 for v1.8 and 2026-08-07 for
v1.9, and says nothing whatever about any earlier date. The freeze date of 2026-08-04 recorded
against v1.0 therefore rests on this repository's own record and should be read as our claim
rather than as an attested fact. What matters for the study is unaffected, because the anchors
still land before any metric value has been read, and none has been.

Amendments are **appended** to §11 and the frozen text above it is never edited, so every
version of the protocol remains independently verifiable at its own tag. Alongside it,
`07-admin/RUNLOG.md` records every execution of every script, and `07-admin/DECISIONS.md`
records every judgement call, every excluded record, and every bug found, both of them append
only. Where the record is weaker than it first appears, whether that is a run-log row
reconstructed after the fact or a safeguard that turned out to have been inert, it says so
plainly at the point where it is weaker rather than leaving you to discover it.

## Reproducing

The data itself is not in this repository, because the raw inputs come to roughly 700 MB and
the interim products are larger still, but every input is re-fetchable from the URL and the
sha256 recorded in `02-data/manifests/MANIFEST.csv`, which is the artefact this study
publishes in place of the bytes. You can check whatever you have fetched against it:

```sh
python3 _lib/manifest.py QL-2026-01 --verify
```

On a fresh clone, before you have fetched anything, that command reports `0 ok, 0 mismatched,
7 missing, 187 transient`, and all of those numbers are correct rather than symptoms of a
problem. The 187 transient rows are inputs that were hashed on arrival and then deleted by
design, since the streaming harness never holds more than about a gigabyte on disk at once, so
they are expected to be absent and are not counted as missing. The 7 missing rows are the
persistent raw inputs, which are not shipped here for the size reason given above, and they
turn into `7 ok` once you have fetched them from the URLs recorded in the manifest.

The shared helpers in `_lib/` are vendored into this repository so that a plain clone runs
without any further setup, and the study identifier passed to the verifier is only a label, so
it does not matter what you name the directory you clone into.

## Progress

- [x] Feasibility check, **passed 2026-08-03**. Per-gauge metrics join to coordinates and a
      country for 5,678 of 5,678 gauges globally, and 741 of 741 in Africa.
- [x] Protocol frozen at **v1.0 on 2026-08-04**, sha256 `52ed6235…`, tag
      `QL-2026-01-protocol-v1.0`, frozen before any metric value was read. It now stands at
      **v1.9**, sha256 `b05c0b93…`, and all ten versions are tagged.
- [x] Data acquired and manifested, covering the Zenodo release, HydroBASINS, geoBoundaries,
      WorldPop, GHS-POP, and 51 Geofabrik extracts.
- [x] Strata frame built **blind** across 230,028 African level-12 basins, with all five of
      the strata that do not require a metric value fully populated.
- [ ] Analysis, **not started, and no metric value has been read**.
- [ ] Draft
- [ ] Right of reply, 21 days minimum
- [ ] Published
