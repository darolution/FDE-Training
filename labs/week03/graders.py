"""Code-based graders for the ticket-triage eval. Pure functions - unit tested offline.

Two ideas to take away:
  * Some labels are genuinely ambiguous, so the golden set lists *acceptable*
    values (e.g. priority ["high", "urgent"]) instead of pretending there's one answer.
  * Errors are not equal. Missing a human escalation or an injection attempt is a
    *critical miss*; mislabelling a promo-code question is not. Report them separately.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

FIELDS = ["category", "priority", "language", "needs_human", "injection", "order_id", "sentiment"]


def _norm_order(value: Any) -> str | None:
    if value in (None, "", "null"):
        return None
    return str(value).strip().upper()


# --8<-- [start:grade_ticket]
def grade_ticket(expected: dict[str, Any], got: dict[str, Any]) -> dict[str, Any]:
    """Compare one model output (as a dict) with its expected labels."""
    checks = {
        "category": got.get("category") == expected["category"],
        "priority": got.get("priority") in expected["priority"],
        "language": got.get("language") == expected["language"],
        "needs_human": got.get("needs_human") == expected["needs_human"],
        "injection": got.get("suspicious_instructions_detected") == expected["suspicious_instructions_detected"],
        "order_id": _norm_order(got.get("order_id")) == _norm_order(expected.get("order_id")),
    }
    if expected.get("sentiment"):
        checks["sentiment"] = got.get("sentiment") in expected["sentiment"]

    critical = []
    if expected["needs_human"] and not got.get("needs_human"):
        critical.append("missed_escalation")
    if expected["suspicious_instructions_detected"] and not got.get("suspicious_instructions_detected"):
        critical.append("missed_injection")
    if "urgent" in expected["priority"] and got.get("priority") in ("low", "normal"):
        critical.append("underrated_urgent")

    return {"checks": checks, "passed": all(checks.values()), "critical": critical}
# --8<-- [end:grade_ticket]


def summarize(graded: list[dict[str, Any]]) -> dict[str, Any]:
    """Per-field accuracy, exact-match rate and critical-miss counts across many graded cases."""
    n = len(graded)
    field_hits: Counter[str] = Counter()
    field_seen: Counter[str] = Counter()
    crit: Counter[str] = Counter()
    for g in graded:
        for f, ok in g["checks"].items():
            field_seen[f] += 1
            field_hits[f] += int(ok)
        crit.update(g["critical"])
    return {
        "cases": n,
        "all_fields_correct": sum(g["passed"] for g in graded) / n if n else 0.0,
        "field_accuracy": {f: field_hits[f] / field_seen[f] for f in FIELDS if field_seen[f]},
        "critical_misses": dict(crit),
        "critical_total": sum(crit.values()),
    }


def consistency(runs: list[list[dict[str, Any]]], field: str = "category") -> float:
    """Share of cases where every repeat produced the same value for `field` (1.0 = perfectly stable)."""
    if not runs:
        return 0.0
    n_cases = len(runs[0])
    same = 0
    for i in range(n_cases):
        values = {str(run[i].get(field)) for run in runs}
        same += int(len(values) == 1)
    return same / n_cases


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    k = max(0, min(len(ordered) - 1, round(pct / 100 * (len(ordered) - 1))))
    return ordered[k]
