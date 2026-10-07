"""Week 1 · Lab 4 - break things on purpose.

    python labs/week01/04_errors.py

Production code meets every one of these. Learn what each looks like now.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import anthropic  # noqa: E402

from fde_common import llm  # noqa: E402
from fde_common.config import models  # noqa: E402

m = models()
c = llm.client()
msg = [{"role": "user", "content": "List ten common reasons an online order arrives late, one per line."}]


def attempt(title, fn):
    print(f"\n== {title}")
    try:
        result = fn()
        print(f"   no exception. stop_reason={result.stop_reason!r}")
        print(f"   text: {llm.text_of(result)[:120]!r}")
    except anthropic.AuthenticationError as e:
        print(f"   AuthenticationError (401) - bad or revoked key. request_id={e.request_id}")
    except anthropic.NotFoundError as e:
        print(f"   NotFoundError (404) - usually a wrong model id. {e.message[:120]}")
    except anthropic.BadRequestError as e:
        print(f"   BadRequestError (400) - the request itself is invalid. {e.message[:160]}")
    except anthropic.RateLimitError:
        print("   RateLimitError (429) - the SDK already retried; back off or queue work.")
    except anthropic.APITimeoutError:
        print("   APITimeoutError - your timeout fired before the response arrived.")
    except anthropic.APIConnectionError:
        print("   APIConnectionError - network/proxy problem; nothing reached the API.")


# 1. Output cut short: not an exception! You must check stop_reason yourself.
attempt("max_tokens too small", lambda: c.messages.create(model=m.fast, max_tokens=15, messages=msg))

# 2. A model id that doesn't exist.
attempt("wrong model id", lambda: c.messages.create(model="claude-sonnet-4-6-20250417", max_tokens=50, messages=msg))

# 3. A parameter newer models reject. Since Opus 4.6, temperature other than 1.0 returns 400.
attempt("temperature on a current model",
        lambda: c.messages.create(model=m.default, max_tokens=50, temperature=0.0, messages=msg))

# 4. Bad key - a separate client so we don't disturb the real one.
bad = anthropic.Anthropic(api_key="sk-ant-not-a-real-key", max_retries=0)
attempt("invalid API key", lambda: bad.messages.create(model=m.fast, max_tokens=50, messages=msg))

# 5. A timeout far too short to succeed, with retries off so it fails fast.
impatient = c.with_options(timeout=0.01, max_retries=0)
attempt("timeout", lambda: impatient.messages.create(model=m.fast, max_tokens=50, messages=msg))

print("\nTakeaways: check stop_reason on every response; let the SDK retry 429/5xx (max_retries);"
      " never retry 400/401/404 - fix the request instead.")
