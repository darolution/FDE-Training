"""Week 2 · Lab 1 - the prompt ladder.

    python labs/week02/01_prompt_ladder.py

Runs the same eight tickets through three system prompts of increasing quality
and shows where each one disagrees with the expected labels. The schema is the
same every time; only the instructions change. Watch which fields improve.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fde_common import llm  # noqa: E402
from fde_common.config import models  # noqa: E402
from week02.tickets import load_tickets, system_prompt, triage  # noqa: E402

PROMPTS = {
    "A bare": "Classify this customer support ticket.",
    "B role+labels": (
        "You triage support tickets for Northwind Outfitters, an online outdoor-gear retailer. "
        "Pick the best category and a priority of low, normal, high or urgent."
    ),
    "C full": system_prompt(),
}
PICK = ["T-001", "T-003", "T-006", "T-008", "T-011", "T-013", "T-017", "T-024"]

m = models()
c = llm.client()
tickets = {t["id"]: t for t in load_tickets()}

score = {name: 0 for name in PROMPTS}
checks = 0
for tid in PICK:
    t = tickets[tid]
    exp = t["expected"]
    print(f"\n{tid}  {t['subject']!r}")
    print(f"   expected: {exp['category']}/{'|'.join(exp['priority'])} human={exp['needs_human']} "
          f"inj={exp['suspicious_instructions_detected']}")
    for name, sys_prompt in PROMPTS.items():
        got, _ = triage(c, m.fast, t, system=sys_prompt, label=f"w2.ladder.{name.split()[0]}")
        ok = [
            got.category.value == exp["category"],
            got.priority.value in exp["priority"],
            got.needs_human == exp["needs_human"],
            got.suspicious_instructions_detected == exp["suspicious_instructions_detected"],
        ]
        score[name] += sum(ok)
        marks = "".join("✓" if x else "✗" for x in ok)
        print(f"   {name:14} {marks}  {got.category.value}/{got.priority.value} human={got.needs_human} "
              f"inj={got.suspicious_instructions_detected}")
    checks += 4

print("\nField checks passed (category, priority, needs_human, injection):")
for name, s in score.items():
    print(f"   {name:14} {s}/{checks}")
