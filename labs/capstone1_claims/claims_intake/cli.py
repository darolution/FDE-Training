"""Process an inbox of claim emails into a routed work queue.

    python -m claims_intake.cli data/claims_golden.jsonl --model fast        (run from labs/capstone1_claims)

Outputs (under labs/runs/capstone1/):
  queue.jsonl   one record per email: extraction + routing decision
  queue.csv     the same, flattened for the claims team's spreadsheet
  audit.jsonl   who/what/when for every decision - no email text, only ids and outcomes
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))          # capstone1_claims
sys.path.insert(0, str(HERE.parents[1]))      # labs

from fde_common import llm  # noqa: E402
from fde_common.config import models  # noqa: E402

from claims_intake.extractor import extract  # noqa: E402
from claims_intake.rules import route  # noqa: E402

OUT = llm.RUNS_DIR / "capstone1"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("inbox", type=Path, help="jsonl of emails (id, received_at, from_name, subject, body)")
    ap.add_argument("--model", choices=["fast", "default", "best"], default="default")
    args = ap.parse_args(argv)

    model = getattr(models(), args.model)
    c = llm.client()
    emails = [json.loads(x) for x in args.inbox.read_text(encoding="utf-8").splitlines() if x.strip()]
    OUT.mkdir(parents=True, exist_ok=True)

    records = []
    with (OUT / "audit.jsonl").open("a", encoding="utf-8") as audit:
        for e in emails:
            extraction, resp = extract(c, model, e)
            decision = route(extraction, e["received_at"])
            records.append({"id": e["id"], "extraction": extraction.model_dump(mode="json"),
                            "decision": decision.model_dump(mode="json")})
            audit.write(json.dumps({
                "ts": datetime.now(timezone.utc).isoformat(), "email_id": e["id"], "model": model,
                "request_id": getattr(resp, "_request_id", None), "route": decision.route.value,
                "reasons": decision.reasons, "actor": "claims_intake.cli",
            }) + "\n")
            print(f"{e['id']}: {decision.route.value:22} {'; '.join(decision.reasons)}")

    (OUT / "queue.jsonl").write_text("\n".join(json.dumps(r) for r in records) + "\n", encoding="utf-8")
    with (OUT / "queue.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "route", "policy_number", "claim_type", "loss_date", "amount_cad", "injuries",
                    "third_party", "fraud_indicators", "missing_information", "reasons"])
        for r in records:
            x, d = r["extraction"], r["decision"]
            w.writerow([r["id"], d["route"], x["policy_number"], x["claim_type"], x["loss_date"],
                        x["estimated_amount_cad"], x["injuries_reported"], x["third_party_involved"],
                        "|".join(x["fraud_indicators"] + d["code_indicators"]),
                        "|".join(x["missing_information"]), "; ".join(d["reasons"])])
    print(f"\nWrote {len(records)} records to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
