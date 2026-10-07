"""Week 1 · Lab 6 - read your own usage log.

    python labs/week01/06_usage_report.py

Summarises labs/runs/usage_log.jsonl by label and model. Later you'll ship this
same log to Splunk and build a dashboard from it.
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fde_common.costs import fmt_usd  # noqa: E402
from fde_common.llm import USAGE_LOG  # noqa: E402

if not USAGE_LOG.exists():
    sys.exit("No usage log yet - run another lab first.")

rows = [json.loads(line) for line in USAGE_LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
agg = defaultdict(lambda: {"calls": 0, "in": 0, "out": 0, "cost": 0.0, "ms": 0})
for r in rows:
    a = agg[(r["label"], r["requested_model"])]
    a["calls"] += 1
    a["in"] += r["input_tokens"] + r.get("cache_read_input_tokens", 0) + r.get("cache_creation_input_tokens", 0)
    a["out"] += r["output_tokens"]
    a["cost"] += r["cost_usd"]
    a["ms"] += r["latency_ms"]

print(f"{'label':22} {'model':28} {'calls':>5} {'in tok':>9} {'out tok':>8} {'avg ms':>7} {'cost':>11}")
for (label, model), a in sorted(agg.items()):
    print(f"{label:22} {model:28} {a['calls']:>5} {a['in']:>9,} {a['out']:>8,} {a['ms'] // a['calls']:>7} "
          f"{fmt_usd(a['cost']):>11}")
print(f"\nTotal spend logged: {fmt_usd(sum(a['cost'] for a in agg.values()))} across {len(rows)} calls")
