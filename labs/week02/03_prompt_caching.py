"""Week 2 · Lab 3 - prompt caching.

    python labs/week02/03_prompt_caching.py

Same long system prompt, several tickets in a row. The first call writes the
cache (costs 1.25x on those tokens); later calls within 5 minutes read it
(0.1x). Minimum cacheable length is model-specific: 512 tokens on Sonnet 5.5 and
Opus 5.5, 4,096 on Haiku 4.5 - so this lab uses the default (Sonnet) model.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fde_common import llm  # noqa: E402
from fde_common.config import models  # noqa: E402
from fde_common.costs import cost_usd, fmt_usd  # noqa: E402
from week02.tickets import load_tickets, system_prompt, triage  # noqa: E402

m = models()
c = llm.client()

# A realistic deployment pads the system prompt with policy text. We do the same so
# the prefix clears the minimum cacheable length.
policy_appendix = "\n\n<return_policy>\n" + (
    "Items may be returned within 60 days in original condition. Footwear must be unworn outdoors. "
    "Refunds go to the original payment method within 5-10 business days of receipt. "
    "Damaged or defective items are replaced or refunded at no cost, including return shipping. "
) * 12 + "\n</return_policy>"
system = system_prompt() + policy_appendix

counted = c.messages.count_tokens(model=m.default, system=system, messages=[{"role": "user", "content": "x"}])
print(f"System prompt is about {counted.input_tokens:,} tokens (needs >= 512 on {m.default} to cache)\n")

with_cache = 0.0
for t in load_tickets()[:4]:
    _, r = triage(c, m.default, t, system=system, cache=True, label="w2.caching")
    u = r.usage
    cost = cost_usd(m.default, u)
    with_cache += cost
    print(f"{t['id']}: write={u.cache_creation_input_tokens or 0:>5}  read={u.cache_read_input_tokens or 0:>5}  "
          f"uncached={u.input_tokens:>4}  cost={fmt_usd(cost)}")

# What the same four calls would have cost with no caching at all
no_cache = 0.0
for t in load_tickets()[:4]:
    _, r = triage(c, m.default, t, system=system, cache=False, label="w2.no_cache")
    no_cache += cost_usd(m.default, r.usage)

print(f"\nwith cache: {fmt_usd(with_cache)}   without: {fmt_usd(no_cache)}")
print("Savings grow with every call that reuses the prefix. Order matters: stable content first, variable content last.")
