"""Freeze a protocol: hash it, write the .sha256, print the commands that make the
timestamp externally verifiable.

A protocol file on your laptop proves nothing — you can edit it. A pushed public commit
is evidence the protocol existed in this state before the analysis commits did.

    python3 _lib/freeze.py QL-2026-01
"""
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def resolve(study):
    """Accept a short id (QL-2026-01) or the full folder name.

    Handles both layouts — see the note in manifest.py. In a published single-study repo
    `_lib/` is vendored inside the study, so ROOT is the study itself.
    """
    if (ROOT / "00-protocol").is_dir():
        # One study per repo, so the id is a label and the checkout directory name is not
        # matched against it. See the fuller note in manifest.py.
        return ROOT
    d = ROOT / study
    if d.is_dir():
        return d
    hits = sorted(p for p in ROOT.glob(f"{study}*") if p.is_dir())
    if len(hits) == 1:
        return hits[0]
    if not hits:
        raise SystemExit(f"no study folder matching {study!r} under {ROOT}")
    raise SystemExit(f"{study!r} is ambiguous: {[h.name for h in hits]}")


def main(study, version="1.0"):
    base = resolve(study)
    proto = base / "00-protocol" / "PROTOCOL.md"
    if not proto.exists():
        sys.exit(f"no protocol at {proto}")
    digest = hashlib.sha256(proto.read_bytes()).hexdigest()
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    (proto.parent / "PROTOCOL.sha256").write_text(f"{digest}  PROTOCOL.md\n")

    print(f"\nprotocol : {proto.relative_to(ROOT)}")
    print(f"sha256   : {digest}")
    print(f"frozen   : {stamp}\n")
    print("Put that hash in the Note. Then run:\n")
    print(f"  git add {base.name}/00-protocol/")
    print(f'  git commit -m "Freeze protocol {base.name} v{version}"')
    print("  git push")
    print(f'  git tag -a {base.name}-protocol-v{version} -m "Frozen {stamp}"')
    print("  git push --tags\n")
    print(f"Then log the hash in {base.name}/07-admin/DECISIONS.md.")
    print("Amendments are appended to the protocol's amendments table — never edits to")
    print("frozen text. A protocol whose history is editable is not a pre-registration.\n")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "1.0")
