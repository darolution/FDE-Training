"""Redact obvious secrets and identifiers before text leaves your machine.

This is a seatbelt, not a data-loss-prevention system. It catches common
patterns so lab mistakes don't leak; it does not make real data safe to send.
The course rule stands: only synthetic or public data goes to the API.
"""

from __future__ import annotations

import re

_RULES: list[tuple[str, re.Pattern[str], str]] = [
    ("anthropic_key", re.compile(r"sk-ant-[A-Za-z0-9_\-]{10,}"), "[REDACTED_API_KEY]"),
    ("aws_access_key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"), "[REDACTED_AWS_KEY]"),
    ("bearer_token", re.compile(r"(?i)\b(bearer)\s+[A-Za-z0-9._\-~+/]{16,}=*"), r"\1 [REDACTED_TOKEN]"),
    ("splunk_auth", re.compile(r"(?i)\b(splunk)\s+[A-Za-z0-9\-]{20,}"), r"\1 [REDACTED_TOKEN]"),
    (
        "password_kv",
        re.compile(r"(?i)\b(password|passwd|pwd|secret|api[_-]?key|token)\b(\s*[:=]\s*)(\"[^\"]*\"|'[^']*'|\S+)"),
        r"\1\2[REDACTED]",
    ),
    ("card_number", re.compile(r"\b(?:\d[ -]?){13,16}\b"), "[REDACTED_PAN]"),
    ("sin_ca", re.compile(r"\b\d{3}[ -]\d{3}[ -]\d{3}\b"), "[REDACTED_SIN]"),
    ("email", re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"), "[REDACTED_EMAIL]"),
]


def redact(text: str) -> tuple[str, dict[str, int]]:
    """Return (clean_text, counts_by_rule)."""
    counts: dict[str, int] = {}
    for name, pattern, replacement in _RULES:
        text, n = pattern.subn(replacement, text)
        if n:
            counts[name] = n
    return text, counts
