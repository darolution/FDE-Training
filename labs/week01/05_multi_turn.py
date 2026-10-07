"""Week 1 · Lab 5 - conversation state and why context costs grow.

    python labs/week01/05_multi_turn.py

The API is stateless: you resend the whole conversation every turn. Watch
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
system = "You are helping a SIEM engineer investigate an alert. Be brief (under 120 words per answer)."
questions = [
    "An alert fired: 40 failed VPN logins for one user from 203.0.113.45, then a success. First three checks?",
    "The source IP geolocates to Romania; the user is based in Toronto. Does that change your priority?",
    "Write the SPL to list every event from that IP in the last 24 hours, newest first.",
    "Draft a two-sentence update for the incident ticket.",
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
