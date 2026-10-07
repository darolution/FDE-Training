"""Week 1 · Lab 5 - conversation state and why context costs grow.

    python labs/week01/05_multi_turn.py

The API is stateless: you resend the whole conversation every turn. Watch the
input tokens climb. This is why long-running agents need context management.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fde_common import llm  # noqa: E402
from fde_common.config import models  # noqa: E402
from fde_common.costs import cost_usd, fmt_usd  # noqa: E402

m = models()
c = llm.client()
system = ("You are helping a support agent at an online outdoor-gear store handle an escalation. "
          "Be brief (under 120 words per answer).")
questions = [
    "A customer says their order NW-102998 has been delayed three times and wants a full $640 refund today, "
    "or they'll dispute the charge with their bank. What are my first three steps?",
    "The order is stuck at the carrier and can't be recovered this week. Does that change what I should offer?",
    "Draft a short, calm reply to the customer.",
    "Write a two-sentence internal note for the ticket.",
]

history: list[dict] = []
running = 0.0
for i, q in enumerate(questions, 1):
    history.append({"role": "user", "content": q})
    r = llm.call(c, label="w1.multi_turn", model=m.fast, max_tokens=400, system=system, messages=history)
    answer = llm.text_of(r)
    history.append({"role": "assistant", "content": answer})
    cost = cost_usd(m.fast, r.usage)
    running += cost
    print(f"\n--- turn {i}: input tokens {r.usage.input_tokens:,} | this turn {fmt_usd(cost)} | total {fmt_usd(running)}")
    print(answer)
