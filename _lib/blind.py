"""Blinding helpers — the second person you do not have.

Three techniques, increasing in strength:
  require_absent()  structural  — the outcome file must not exist yet
  permute()         permutation — develop against shuffled labels, then freeze and run once
  blind_name()      identity    — grade responses named by hash, join back afterwards
"""
import hashlib
import json
import random
from pathlib import Path


def require_absent(*paths):
    """Fail loudly if an outcome file is present while building strata or covariates.

        require_absent(INTERIM / "metrics")   # in 03-harness/01_build_strata.py

    PASS THE WHOLE OUTCOME TREE, NOT SUBDIRECTORIES INSIDE IT. QL-2026-01 named two specific
    paths — `metrics/return_period_metrics` and `metrics/hydrograph_metrics/per_gauge` —
    and neither was ever extracted, so the guard could not fire, while two *other* metric
    directories sat in the tree unguarded through the entire covariate build (2026-08-04 to
    2026-08-05, found 08-06). An enumeration of forbidden names fails silently the moment a
    name is not the one you guessed. The presence of the directory is the testable thing.

    IMPORT THIS; DO NOT RESTATE IT INLINE. The same study inlined a copy per script, reasoning
    that an inline check could not be disarmed by deleting another file. That reasoning is
    backwards: an inline copy fails OPEN — it silently checks the wrong path and the script
    runs anyway — whereas a missing or renamed import fails CLOSED, raising ImportError so
    the script does not run at all. Fail-closed is the property you want from a guard.
    """
    for p in paths:
        if Path(p).exists():
            raise RuntimeError(
                f"Blinding violation: {p} is present. Strata and covariates must be built "
                f"before outcomes are loaded. Move it out of the tree and re-run."
            )


def permute(values, seed):
    """Shuffled copy of an outcome column, for developing the analysis blind.

    Develop and debug against this. Then freeze the code and run once on real labels.
    A striking result on permuted data means the analysis is broken — found out for free.
    Record the seed in the results file, not just the code.
    """
    out = list(values)
    random.Random(seed).shuffle(out)
    return out


def blind_name(item_id, model, lang, salt):
    """Stable pseudonym for a response file, so grading cannot see model identity.

    Write responses as <blind_name>.json, grade from those, and join back to
    (model, lang) only after every grade is committed.
    """
    key = f"{salt}|{item_id}|{model}|{lang}".encode()
    return hashlib.sha256(key).hexdigest()[:16]


def write_blind_key(path, rows, salt):
    """Write the unblinding key. Commit it, but do not open it until grading is done."""
    key = {blind_name(r["item_id"], r["model"], r["lang"], salt): r for r in rows}
    Path(path).write_text(json.dumps(key, indent=2, sort_keys=True))
    return len(key)
