"""Week 3 · Lab 2 - diff two eval runs to find regressions.

    python labs/week03/compare_runs.py labs/runs/eval_tickets_fast_A.json labs/runs/eval_tickets_fast_B.json

Use it after every prompt change: which cases got fixed, which broke?
"""

import json
import sys
from pathlib import Path

if len(sys.argv) != 3:
    sys.exit(__doc__)

a, b = (json.loads(Path(p).read_text(encoding="utf-8")) for p in sys.argv[1:])
by_id_a = {c["id"]: c for c in a["cases"]}
by_id_b = {c["id"]: c for c in b["cases"]}

print(f"A: {a['model']} exact={a['summary']['all_fields_correct']:.0%} critical={a['summary']['critical_total']}")
print(f"B: {b['model']} exact={b['summary']['all_fields_correct']:.0%} critical={b['summary']['critical_total']}\n")

for cid in sorted(by_id_a.keys() & by_id_b.keys()):
    pa, pb = by_id_a[cid]["grade"]["passed"], by_id_b[cid]["grade"]["passed"]
    if pa and not pb:
        bad = [f for f, ok in by_id_b[cid]["grade"]["checks"].items() if not ok]
        print(f"REGRESSED {cid}: now wrong on {bad}")
    elif pb and not pa:
        print(f"FIXED     {cid}")
