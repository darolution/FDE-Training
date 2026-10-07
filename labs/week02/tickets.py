"""Support-ticket triage with structured outputs - built in Week 2, evaluated in Week 3."""

from __future__ import annotations

import json
from enum import Enum
from pathlib import Path
from typing import Any, Optional

import anthropic
from pydantic import BaseModel, Field

from fde_common import llm
from fde_common.config import LABS_DIR
from fde_common.redact import redact

PROMPT_FILE = Path(__file__).resolve().parent / "prompts" / "ticket_triage_system.md"
GOLDEN_FILE = LABS_DIR / "data" / "tickets_golden.jsonl"
PRIORITY_ORDER = ["low", "normal", "high", "urgent"]


class Category(str, Enum):
    order_status = "order_status"
    return_refund = "return_refund"
    damaged_item = "damaged_item"
    billing = "billing"
    product_question = "product_question"
    account_access = "account_access"
    complaint = "complaint"
    other = "other"


class Priority(str, Enum):
    low = "low"
    normal = "normal"
    high = "high"
    urgent = "urgent"


class Sentiment(str, Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"
    angry = "angry"


class TicketTriage(BaseModel):
    category: Category
    priority: Priority
    sentiment: Sentiment
    language: str = Field(description='"en", "fr" or "other"')
    needs_human: bool
    suspicious_instructions_detected: bool
    order_id: Optional[str] = Field(default=None, description="NW-###### exactly as written, or null")
    summary: str


def load_tickets(path: Path = GOLDEN_FILE) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def system_prompt(path: Path = PROMPT_FILE) -> str:
    return path.read_text(encoding="utf-8")


def render_ticket(ticket: dict[str, Any]) -> str:
    """Only the fields the model needs; never the expected labels. Redacted before sending."""
    visible = {k: ticket[k] for k in ("channel", "customer_tier", "subject", "body") if k in ticket}
    text, _ = redact(json.dumps(visible, ensure_ascii=False, indent=1))
    return f"<ticket>\n{text}\n</ticket>"


def triage(
    c: anthropic.Anthropic,
    model: str,
    ticket: dict[str, Any],
    *,
    system: str | None = None,
    label: str = "w2.ticket_triage",
    max_tokens: int = 1024,
    cache: bool = False,
) -> tuple[TicketTriage, Any]:
    kwargs: dict[str, Any] = dict(
        model=model,
        max_tokens=max_tokens,
        system=system if system is not None else system_prompt(),
        messages=[{"role": "user", "content": render_ticket(ticket)}],
        output_format=TicketTriage,
    )
    if cache:
        # Explicit cache breakpoint on the system prompt: everything up to here is cached.
        kwargs["system"] = [{"type": "text", "text": kwargs["system"], "cache_control": {"type": "ephemeral"}}]
    response = llm.parse(c, label=label, **kwargs)
    if response.parsed_output is None:
        raise ValueError(f"No parsed output (stop_reason={response.stop_reason})")
    return response.parsed_output, response
