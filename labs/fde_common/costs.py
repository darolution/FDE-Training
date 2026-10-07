"""Turn API usage into dollars.

Prices are USD per million tokens, from the Claude docs on 2026-10-06:
https://platform.claude.com/docs/en/models/overview
https://platform.claude.com/docs/en/build-with-claude/prompt-caching
Re-check them before you quote a number to anyone. Prices change.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Price:
    input: float          # $ per MTok, uncached input
    output: float         # $ per MTok, output (thinking tokens bill as output)
    cache_read_mult: float = 0.10


PRICES: dict[str, Price] = {
    "claude-fable-5-1": Price(10.00, 50.00, cache_read_mult=0.025),
    "claude-opus-5-5": Price(4.00, 20.00, cache_read_mult=0.05),
    "claude-sonnet-5-5": Price(2.00, 10.00),
    "claude-haiku-4-5-20251001": Price(1.00, 5.00),
    "claude-haiku-4-5": Price(1.00, 5.00),
}

CACHE_WRITE_5M_MULT = 1.25
CACHE_WRITE_1H_MULT = 2.00
PER_MTOK = 1_000_000


def price_for(model: str) -> Price:
    try:
        return PRICES[model]
    except KeyError as exc:
        raise KeyError(f"No price for model {model!r}. Add it to PRICES in fde_common/costs.py.") from exc


def _get(obj: Any, name: str, default: int = 0) -> int:
    """Read a field from an SDK Usage object or a plain dict."""
    if obj is None:
        return default
    value = obj.get(name) if isinstance(obj, dict) else getattr(obj, name, default)
    return int(value or 0)


def cost_usd(model: str, usage: Any) -> float:
    """Cost of one response, including prompt-cache reads and writes.

    `usage` is `response.usage` from the SDK, or a dict with the same keys.
    """
    p = price_for(model)
    uncached_in = _get(usage, "input_tokens")
    out = _get(usage, "output_tokens")
    cache_read = _get(usage, "cache_read_input_tokens")

    creation = usage.get("cache_creation") if isinstance(usage, dict) else getattr(usage, "cache_creation", None)
    if creation is not None:
        write_5m = _get(creation, "ephemeral_5m_input_tokens")
        write_1h = _get(creation, "ephemeral_1h_input_tokens")
    else:  # older responses only report the total; assume the 5-minute TTL
        write_5m = _get(usage, "cache_creation_input_tokens")
        write_1h = 0

    dollars = (
        uncached_in * p.input
        + out * p.output
        + cache_read * p.input * p.cache_read_mult
        + write_5m * p.input * CACHE_WRITE_5M_MULT
        + write_1h * p.input * CACHE_WRITE_1H_MULT
    )
    return dollars / PER_MTOK


def total_input_tokens(usage: Any) -> int:
    return (
        _get(usage, "input_tokens")
        + _get(usage, "cache_read_input_tokens")
        + _get(usage, "cache_creation_input_tokens")
    )


def fmt_usd(amount: float) -> str:
    return f"${amount:,.6f}" if amount < 0.01 else f"${amount:,.4f}"
