"""Week 2 · Lab 2 - structured triage over the whole ticket set.

    python labs/week02/02_structured_triage.py [--model fast|default|best]

Structured outputs guarantee the response parses into TicketTriage. They do NOT
guarantee the values are right - that's what next week's evals are for.
Results go to labs/runs/w2_triage_<model>.jsonl.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fde_common import llm  # noqa: E402
from fde_common.config import models  # noqa: E402
from fde_common.costs import cost_usd, fmt_usd  # noqa: E402
from week02.tickets import load_tickets, triage  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--model", choices=["fast", "default", "best"], default="fast")
args = ap.parse_args()
model = getattr(models(), args.model)

c = llm.client()
out = llm.RUNS_DIR / f"w2_triage_{args.model}.jsonl"
out.parent.mkdir(parents=True, exist_ok=True)
total = 0.0

with out.open("w", encoding="utf-8") as fh:
    for t in load_tickets():
        result, resp = triage(c, model, t)
        total += cost_usd(model, resp.usage)
        flag = "⚠" if result.suspicious_instructions_detected else " "
        print(f"{t['id']} {flag} {result.category.value:17} {result.priority.value:7} {result.sentiment.value:8} "
              f"{result.language:3} human={str(result.needs_human):5} {result.order_id or '-':10} | {result.summary[:70]}")
        fh.write(json.dumps({"id": t["id"], "result": result.model_dump(mode="json")}) + "\n")

print(f"\n{model}: cost {fmt_usd(total)} -> {out}")
