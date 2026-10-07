"""Week 1 · Lab 3 - stream a response.

    python labs/week01/03_streaming.py

Streaming changes perceived latency, not total latency. Watch time-to-first-token
versus total time. Use streaming for anything a human waits on.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fde_common import llm  # noqa: E402
from fde_common.config import models  # noqa: E402
from fde_common.costs import cost_usd, fmt_usd  # noqa: E402

m = models()
c = llm.client()

started = time.perf_counter()
first_token_at = None
with c.messages.stream(
    model=m.default,
    max_tokens=800,
    messages=[{
        "role": "user",
        "content": "Write a short runbook (6 numbered steps) for triaging a password-spray alert in Splunk.",
    }],
) as stream:
    for text in stream.text_stream:
        if first_token_at is None:
            first_token_at = time.perf_counter()
        print(text, end="", flush=True)
    final = stream.get_final_message()

total = time.perf_counter() - started
print("\n" + "-" * 60)
print(f"time to first token: {first_token_at - started:.2f}s   total: {total:.2f}s")
print(f"tokens: in={final.usage.input_tokens} out={final.usage.output_tokens}  "
      f"cost: {fmt_usd(cost_usd(m.default, final.usage))}")
