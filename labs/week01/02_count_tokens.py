"""Week 1 · Lab 2 - estimate cost *before* you send.

    python labs/week01/02_count_tokens.py [--lines 200]

Counts the tokens in a slice of the synthetic log (token counting is free)
and projects what analysing it would cost on each model, per call and at
10,000 calls a day. This is the arithmetic you'll do in every customer scoping
conversation.
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
ap.add_argument("--lines", type=int, default=200)
ap.add_argument("--assume-output", type=int, default=400, help="output tokens to assume per call")
args = ap.parse_args()

events_file = LABS_DIR / "data" / "out" / "events.jsonl"
if not events_file.exists():
    sys.exit("Run `python labs/data/generate_events.py` first.")

lines = events_file.read_text(encoding="utf-8").splitlines()[: args.lines]
log_text = "\n".join(json.dumps(json.loads(line)["event"]) for line in lines)
prompt = f"Summarise notable security activity in these events:\n<events>\n{log_text}\n</events>"

c = llm.client()
m = models()
print(f"{len(lines)} events, {len(log_text):,} characters\n")
print(f"{'model':32} {'input tok':>10} {'per call':>12} {'10k calls/day':>15}")
for model in (m.fast, m.default, m.best):
    counted = c.messages.count_tokens(model=model, messages=[{"role": "user", "content": prompt}])
    usage = {"input_tokens": counted.input_tokens, "output_tokens": args.assume_output}
    per_call = cost_usd(model, usage)
    print(f"{model:32} {counted.input_tokens:>10,} {fmt_usd(per_call):>12} {fmt_usd(per_call * 10_000):>15}")

print("\nRule of thumb check: characters / tokens =", round(len(prompt) / counted.input_tokens, 2))
print("JSON logs tokenise worse than prose - that's why the ratio is low. Trim fields before you send.")
