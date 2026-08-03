# Run log — QL-2026-01

**Append only.** One row per execution of anything in `03-harness/` or `04-analysis/`.

`blind?` — `blind` (outcome absent or permuted) or `UNBLINDED`.
The unblinding row is the important one: it records the single authorised run against real
outcomes. A re-run after a post-unblinding bug fix gets its own row with the reason.

| UTC | Script | Git SHA | Inputs (sha256 prefix) | blind? | Outputs | Notes |
|---|---|---|---|---|---|---|
| 2026-08-03T20:02:01Z | `03-harness/00_day1_join_check.py` | c88d5c6 (script uncommitted at run time; committed this session, file sha256 `5d464eedf9b1`) | metrics.tgz `237559b9abbe` · metadata.tgz `59c6b8310d17` · gauge_groups_for_paper.tgz `a72a2b777ef3` | blind | stdout only — no file written | Day-1 feasibility. Reads gauge identifiers and coordinates only; opens no metric file and reads no skill value. Result: 5,678/5,678 joinable globally, 741/741 Africa. |

## Unblinding record

- **Date (UTC):**
- **Frozen analysis SHA:**
- **Protocol hash at time of run:**
- **Authorised by:**
- **Post-unblinding changes:** *(none, or each with date, reason and new SHA)*
