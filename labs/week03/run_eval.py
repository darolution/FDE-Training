"""Week 3 · Lab 1 - run the ticket-triage eval.

    python labs/week03/run_eval.py --model fast
    python labs/week03/run_eval.py --model default --repeats 3 --min-accuracy 0.8

Prints per-field accuracy, critical misses, cost and latency, and saves a full
result file under labs/runs/. Exits with code 1 if the run falls below the gate
(--min-accuracy on exact match, or any critical miss when --no-critical is set).
That exit code is what lets you put this eval in CI later.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fde_common import llm  # noqa: E402
from fde_common.config import models  # noqa: E402
from fde_common.costs import cost_usd, fmt_usd  # noqa: E402
from week02.tickets import PROMPT_FILE, load_tickets, triage  # noqa: E402
from week03.graders import consistency, grade_ticket, percentile, summarize  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", choices=["fast", "default", "best"], default="fast")
    ap.add_argument("--repeats", type=int, default=1, help="run each case N times to measure stability")
    ap.add_argument("--min-accuracy", type=float, default=0.0, help="gate on all-fields-correct rate")
    ap.add_argument("--no-critical", action="store_true", help="fail the run on any critical miss")
    ap.add_argument("--only", nargs="*", help="ticket ids to run (default: all)")
    args = ap.parse_args(argv)

    model = getattr(models(), args.model)
    c = llm.client()
    tickets = [t for t in load_tickets() if not args.only or t["id"] in args.only]

    runs: list[list[dict]] = []
    graded_all, cases, latencies, spend = [], [], [], 0.0
    for rep in range(args.repeats):
        outputs = []
        for t in tickets:
            started = time.perf_counter()
            result, resp = triage(c, model, t, label=f"w3.eval.{args.model}")
            latencies.append(time.perf_counter() - started)
            spend += cost_usd(model, resp.usage)
            got = result.model_dump(mode="json")
            g = grade_ticket(t["expected"], got)
            graded_all.append(g)
            outputs.append(got)
            if rep == 0:
                cases.append({"id": t["id"], "got": got, "grade": g})
        runs.append(outputs)

    s = summarize(graded_all)
    print(f"\nModel {model}  |  {len(tickets)} cases x {args.repeats} repeat(s)")
    print(f"All fields correct: {s['all_fields_correct']:.0%}")
    for f, acc in s["field_accuracy"].items():
        print(f"   {f:12} {acc:6.0%}")
    print(f"Critical misses: {s['critical_total']} {s['critical_misses'] or ''}")
    if args.repeats > 1:
        print(f"Stability (same category every repeat): {consistency(runs, 'category'):.0%}")
        print(f"Stability (same priority every repeat): {consistency(runs, 'priority'):.0%}")
    print(f"Latency p50 {percentile(latencies, 50):.2f}s  p95 {percentile(latencies, 95):.2f}s  |  cost {fmt_usd(spend)}")

    print("\nFailures (first repeat):")
    for case in cases:
        if not case["grade"]["passed"]:
            bad = [f for f, ok in case["grade"]["checks"].items() if not ok]
            print(f"   {case['id']}: wrong {bad} {case['grade']['critical'] or ''}")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = llm.RUNS_DIR / f"eval_tickets_{args.model}_{stamp}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "model": model, "prompt_file": PROMPT_FILE.name, "repeats": args.repeats,
        "summary": s, "cost_usd": spend, "cases": cases,
    }, indent=2), encoding="utf-8")
    print(f"\nSaved {out}")

    failed = s["all_fields_correct"] < args.min_accuracy or (args.no_critical and s["critical_total"] > 0)
    if failed:
        print("GATE FAILED")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
