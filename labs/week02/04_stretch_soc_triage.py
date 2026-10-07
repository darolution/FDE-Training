"""Week 2 · Stretch (security track) - triage SIEM alerts built from the synthetic logs.

    python labs/data/generate_events.py        # once, to create events + ground truth
    python labs/week02/04_stretch_soc_triage.py

Each planted incident becomes an "alert" with a neutral name and a handful of
sample events. Compare the model's category and severity with ground_truth.json.
No Splunk needed - it reads the generated files directly.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fde_common import llm  # noqa: E402
from fde_common.config import LABS_DIR, models  # noqa: E402
from week02.soc_triage import classify  # noqa: E402

out_dir = LABS_DIR / "data" / "out"
if not (out_dir / "ground_truth.json").exists():
    sys.exit("Run `python labs/data/generate_events.py` first.")

truth = json.loads((out_dir / "ground_truth.json").read_text(encoding="utf-8"))
events = [json.loads(line)["event"] for line in (out_dir / "events.jsonl").read_text(encoding="utf-8").splitlines()]


def matches(ev, t):
    keys = [k for k in ("user", "src", "url_domain", "dest") if k in t]
    return all(ev.get(k) == t[k] for k in keys)


m = models()
c = llm.client()
for t in truth:
    sample = [e for e in events if matches(e, t)]
    alert = {"alert_name": "Detection rule fired", "count": len(sample), "sample_events": sample[:6]}
    got, _ = classify(c, m.fast, alert)
    print(f"{t['id']} expected {t['type']:24} {t['severity']:8} | got {got.category.value:22} {got.severity.value:8} "
          f"inj={got.suspicious_instructions_detected}")
    print(f"        {got.summary}")
