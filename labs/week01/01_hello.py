"""Week 1 · Lab 1 - your first logged API call.

    python labs/week01/01_hello.py

What to look for: the response text, the stop reason, token counts, the cost,
and the request id (quote it if you ever open a support ticket).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fde_common import llm  # noqa: E402
from fde_common.config import models  # noqa: E402
from fde_common.costs import cost_usd, fmt_usd  # noqa: E402

m = models()
c = llm.client()

response = llm.call(
    c,
    label="w1.hello",
    model=m.fast,
    max_tokens=300,
    system="You are a senior SOC analyst. Answer in at most three sentences.",
    messages=[{"role": "user", "content": "In plain terms, what is a SIEM correlation search?"}],
)

print(llm.text_of(response))
print("-" * 60)
print(f"model:        {response.model}")
print(f"stop_reason:  {response.stop_reason}")
print(f"tokens:       in={response.usage.input_tokens} out={response.usage.output_tokens}")
print(f"cost:         {fmt_usd(cost_usd(m.fast, response.usage))}")
print(f"request id:   {getattr(response, '_request_id', None)}")
print(f"logged to:    {llm.USAGE_LOG}")
