"""A thin, observable wrapper around the Anthropic client.

Every call made through `call()` appends one JSON line to labs/runs/usage_log.jsonl
with the model, token counts, cost, latency and stop reason. You will reuse this
log in later weeks (it is the seed of the observability work in Phase 3).
"""

from __future__ import annotations

import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import anthropic

from .config import LABS_DIR, require_api_key
from .costs import cost_usd

RUNS_DIR = LABS_DIR / "runs"
USAGE_LOG = RUNS_DIR / "usage_log.jsonl"


def client(max_retries: int = 3, timeout: float = 60.0) -> anthropic.Anthropic:
    """Create a client. The SDK already retries 429/5xx with backoff; we set the count explicitly."""
    return anthropic.Anthropic(api_key=require_api_key(), max_retries=max_retries, timeout=timeout)


def text_of(response: Any) -> str:
    """Join the text blocks of a response (ignores thinking and tool-use blocks)."""
    return "".join(block.text for block in response.content if getattr(block, "type", None) == "text")


def log_usage(record: dict[str, Any], path: Path = USAGE_LOG) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")


def usage_record(label: str, model: str, response: Any, latency_ms: int | None) -> dict[str, Any]:
    u = response.usage
    return {
        "ts": datetime.now(timezone.utc).isoformat(),
        "trace_id": uuid.uuid4().hex[:12],
        "label": label,
        "model": response.model,
        "requested_model": model,
        "input_tokens": u.input_tokens,
        "output_tokens": u.output_tokens,
        "cache_read_input_tokens": u.cache_read_input_tokens or 0,
        "cache_creation_input_tokens": u.cache_creation_input_tokens or 0,
        "cost_usd": round(cost_usd(model, u), 8),
        "latency_ms": latency_ms,
        "stop_reason": response.stop_reason,
        "request_id": getattr(response, "_request_id", None),
    }


def _timed(fn: Any, label: str, kwargs: dict[str, Any]) -> Any:
    started = time.perf_counter()
    response = fn(**kwargs)
    elapsed_ms = round((time.perf_counter() - started) * 1000)
    log_usage(usage_record(label, kwargs["model"], response, elapsed_ms))
    return response


def call(c: anthropic.Anthropic, *, label: str, **kwargs: Any) -> Any:
    """`c.messages.create(**kwargs)` plus a usage-log line. Never logs prompt or response text."""
    return _timed(c.messages.create, label, kwargs)


def parse(c: anthropic.Anthropic, *, label: str, **kwargs: Any) -> Any:
    """`c.messages.parse(**kwargs)` (structured outputs) plus a usage-log line."""
    return _timed(c.messages.parse, label, kwargs)
