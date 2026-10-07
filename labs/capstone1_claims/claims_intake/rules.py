"""Routing rules for Lakeshore Mutual claims.  >>> YOU IMPLEMENT THIS <<<

The customer's claims director agreed these rules in discovery (see the capstone
page). Implement `route()` so that `pytest -m capstone labs` passes.

Rules, in priority order - the first that applies wins:

  1. bodily_injury           if injuries_reported is true.
  2. special_investigations  if ANY of:
        - suspicious_instructions_detected is true
        - the loss date is AFTER the date the email was received   (add code indicator "loss_date_after_report")
        - 2 or more fraud indicators in total (model + code indicators)
  3. needs_info              if policy_number or loss_date is missing.
  4. fast_track              if claim_type is auto AND estimated_amount_cad is known AND <= 5000
                             AND third_party_involved is false.
  5. standard                otherwise.

Code-derived indicators (computed here, never by the model):
  - "loss_date_after_report": loss_date > received_at
  - "late_report":           loss_date more than 30 days before received_at

Every decision must list human-readable `reasons` (adjusters read them).
Dates arrive as "YYYY-MM-DD" strings; a malformed loss_date counts as missing.
"""

from __future__ import annotations

from datetime import date

from .schema import ClaimExtraction, Route, RoutingDecision  # noqa: F401

FAST_TRACK_LIMIT_CAD = 5000.0
LATE_REPORT_DAYS = 30


def parse_date(value: str | None) -> date | None:
    """Return a date for a valid YYYY-MM-DD string, else None."""
    raise NotImplementedError("TODO: implement parse_date")


def route(extraction: ClaimExtraction, received_at: str) -> RoutingDecision:
    """Apply the rules above and return the decision with reasons."""
    raise NotImplementedError("TODO: implement route")
