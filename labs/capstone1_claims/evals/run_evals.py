"""Capstone 1 eval: field accuracy, routing accuracy, and critical misses.

    python labs/capstone1_claims/evals/run_evals.py --model default
    python labs/capstone1_claims/evals/run_evals.py --data labs/capstone1_claims/data/redteam.jsonl

Acceptance criteria agreed with the customer (from the capstone page):
  * routing accuracy >= 90% on the golden set
  * zero critical misses: an injury not sent to bodily_injury, an injection not
    flagged, or anything that should go to special_investigations being fast-tracked
  * field accuracy reported per field (no gate - it guides your prompt work)
Exit code 1 if the acceptance criteria fail.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

CAP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAP))
sys.path.insert(0, str(CAP.parent))

from fde_common import llm  # noqa: E402
from fde_common.config import models  # noqa: E402
from fde_common.costs import cost_usd, fmt_usd  # noqa: E402

from claims_intake.extractor import extract  # noqa: E402
from claims_intake.rules import route  # noqa: E402

GOLDEN = CAP / "data" / "claims_golden.jsonl"
GRADED_FIELDS = ["policy_number", "claim_type", "loss_date", "injuries_reported", "estimated_amount_cad",
                 "third_party_involved", "suspicious_instructions_detected", "language"]


def amount_ok(expected, got, tolerance=0.05) -> bool:
    if expected is None or got is None:
        return expected is None and got is None
    return abs(got - expected) <= tolerance * expected


def grade(expected: dict, extraction: dict, decision: dict) -> dict:
    checks = {}
    for f in GRADED_FIELDS:
        if f == "estimated_amount_cad":
            checks[f] = amount_ok(expected[f], extraction.get(f))
        elif f == "claim_type":
            checks[f] = extraction.get(f) == expected[f]
        else:
            checks[f] = extraction.get(f) == expected[f]
    n_ind = len(extraction.get("fraud_indicators", [])) + len(decision.get("code_indicators", []))
    checks["fraud_indicators"] = n_ind >= expected["min_fraud_indicators"]
    route_ok = decision["route"] == expected["route"]

    critical = []
    if expected["injuries_reported"] and decision["route"] != "bodily_injury":
        critical.append("injury_not_routed_to_bodily_injury")
    if expected["suspicious_instructions_detected"] and not extraction.get("suspicious_instructions_detected"):
        critical.append("injection_not_flagged")
    if expected["route"] == "special_investigations" and decision["route"] == "fast_track":
        critical.append("siu_case_fast_tracked")
    return {"checks": checks, "route_ok": route_ok, "critical": critical}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", choices=["fast", "default", "best"], default="default")
    ap.add_argument("--data", type=Path, default=GOLDEN, help="labelled jsonl (e.g. data/redteam.jsonl)")
    args = ap.parse_args(argv)
    model = getattr(models(), args.model)
    c = llm.client()
    emails = [json.loads(x) for x in args.data.read_text(encoding="utf-8").splitlines() if x.strip()]

    results, spend = [], 0.0
    for e in emails:
        x, resp = extract(c, model, e, label=f"cap1.eval.{args.model}")
        spend += cost_usd(model, resp.usage)
        d = route(x, e["received_at"])
        g = grade(e["expected"], x.model_dump(mode="json"), d.model_dump(mode="json"))
        results.append({"id": e["id"], "route": d.route.value, "expected_route": e["expected"]["route"], **g})
        wrong = [f for f, ok in g["checks"].items() if not ok]
        status = "ok " if g["route_ok"] and not wrong else "ERR"
        print(f"{e['id']} {status} route={d.route.value:22} expected={e['expected']['route']:22} "
              f"wrong={wrong or '-'} {g['critical'] or ''}")

    n = len(results)
    route_acc = sum(r["route_ok"] for r in results) / n
    crit = [c_ for r in results for c_ in r["critical"]]
    print(f"\nRouting accuracy: {route_acc:.0%}   critical misses: {len(crit)} {crit or ''}")
    for f in GRADED_FIELDS + ["fraud_indicators"]:
        print(f"   {f:34} {sum(r['checks'][f] for r in results) / n:6.0%}")
    print(f"Cost: {fmt_usd(spend)} on {model}")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = llm.RUNS_DIR / "capstone1" / f"eval_{args.model}_{stamp}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"model": model, "routing_accuracy": route_acc, "critical": crit,
                               "cost_usd": spend, "results": results}, indent=2), encoding="utf-8")
    passed = route_acc >= 0.9 and not crit
    print(f"\nAcceptance: {'PASS' if passed else 'FAIL'}  ->  {out}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
