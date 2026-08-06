# Shared helpers

Imported by study harnesses. Keep them small and dependency-free.

| Module | Use |
|---|---|
| `stats.py` | `fmt(k, n)` — renders a proportion with Wilson interval and denominator. No bare proportions. |
| `manifest.py` | Record and verify data provenance. Run `--verify` before every analysis. |
| `freeze.py` | Hash a protocol and print the commands that make its timestamp verifiable. |
| `blind.py` | `require_absent`, `permute`, `blind_name` — structural, permutation and identity blinding. |

```python
import sys; sys.path.insert(0, "../_lib")
from stats import fmt
from blind import require_absent, permute
```
