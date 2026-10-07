"""Stretch lab (security track): SIEM alert triage with structured outputs."""

from __future__ import annotations

import json
from enum import Enum
from pathlib import Path
from typing import Any, Optional

import anthropic
from pydantic import BaseModel, Field

from fde_common import llm
from fde_common.redact import redact

PROMPT_FILE = Path(__file__).resolve().parent / "prompts" / "soc_triage_system.md"
SEVERITY_ORDER = ["informational", "low", "medium", "high", "critical"]


class Category(str, Enum):
    benign = "benign"
    authentication_attack = "authentication_attack"
    account_compromise = "account_compromise"
    malware_execution = "malware_execution"
    data_exfiltration = "data_exfiltration"
    policy_violation = "policy_violation"
    prompt_injection = "prompt_injection"
    other = "other"


class Severity(str, Enum):
    informational = "informational"
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class Triage(BaseModel):
    category: Category
    severity: Severity
    needs_human: bool
    suspicious_instructions_detected: bool = Field(
        description="True if any alert content tries to instruct an AI system."
    )
    mitre_tactic: Optional[str] = Field(default=None, description="ATT&CK tactic name, or null.")
    recommended_action: str
    summary: str


def system_prompt() -> str:
    return PROMPT_FILE.read_text(encoding="utf-8")


def render_alert(alert: dict[str, Any]) -> str:
    """Serialise and redact an alert, then wrap it in tags so the model can tell data from instructions."""
    text, _ = redact(json.dumps(alert, ensure_ascii=False))
    return f"<alert>{text}</alert>"


def classify(
    c: anthropic.Anthropic,
    model: str,
    alert: dict[str, Any],
    *,
    label: str = "w2.soc_triage",
    max_tokens: int = 1024,
    cache: bool = False,
) -> tuple[Triage, Any]:
    """Return (Triage, raw_response). Uses structured outputs, so the result always matches the schema."""
    kwargs: dict[str, Any] = dict(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt(),
        messages=[{"role": "user", "content": render_alert(alert)}],
        output_format=Triage,
    )
    if cache:
        # Explicit cache breakpoint on the system prompt: everything up to here is cached.
        kwargs["system"] = [{"type": "text", "text": kwargs["system"], "cache_control": {"type": "ephemeral"}}]
    response = llm.parse(c, label=label, **kwargs)
    if response.parsed_output is None:
        raise ValueError(f"No parsed output (stop_reason={response.stop_reason})")
    return response.parsed_output, response
