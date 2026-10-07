"""Week 1 · Lab 2 - estimate cost *before* you send.

    python labs/week01/02_count_tokens.py [--copies 1] [--assume-output 400]

Counts the tokens in the support-ticket dataset (token counting is free) and
projects what processing it would cost on each model, per call and at 10,000
calls a day. This is the arithmetic you'll do in every customer scoping
conversation. Use --copies to simulate a bigger batch of tickets in one prompt.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fde_common import llm  # noqa: E402
from fde_common.config import LABS_DIR, models  # noqa: E402
from fde_common.costs import cost_usd, fmt_usd  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--copies", type=int, default=1, help="repeat the ticket set N times")
ap.add_argument("--assume-output", type=int, default=400, help="output tokens to assume per call")
args = ap.parse_args()

tickets_file = LABS_DIR / "data" / "tickets_golden.jsonl"
tickets = [json.loads(line) for line in tickets_file.read_text(encoding="utf-8").splitlines() if line.strip()]
# Only what a real system would send: subject and body, never the expected labels.
ticket_text = "\n".join(json.dumps({"subject": t["subject"], "body": t["body"]}, ensure_ascii=False) for t in tickets)
ticket_text = "\n".join([ticket_text] * args.copies)
prompt = f"Summarise the main themes in these support tickets:\n<tickets>\n{ticket_text}\n</tickets>"

c = llm.client()
m = models()
print(f"{len(tickets) * args.copies} tickets, {len(prompt):,} characters\n")
print(f"{'model':32} {'input tok':>10} {'per call':>12} {'10k calls/day':>15}")
for model in (m.fast, m.default, m.best):
    counted = c.messages.count_tokens(model=model, messages=[{"role": "user", "content": prompt}])
    usage = {"input_tokens": counted.input_tokens, "output_tokens": args.assume_output}
    per_call = cost_usd(model, usage)
    print(f"{model:32} {counted.input_tokens:>10,} {fmt_usd(per_call):>12} {fmt_usd(per_call * 10_000):>15}")

print("\nCharacters per token:", round(len(prompt) / counted.input_tokens, 2))
print("JSON and non-English text use more tokens per character than plain English prose.")
