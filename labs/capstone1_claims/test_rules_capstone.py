"""Specification for claims_intake/rules.py.  Run:  python -m pytest -m capstone

These fail until you implement rules.py - that's the point. They are the
claims director's rules written as tests. Don't edit them to make them pass;
if you think a rule is wrong, that's a conversation with the customer.
"""

import pytest

from claims_intake.rules import parse_date, route
from claims_intake.schema import ClaimExtraction, Route

pytestmark = pytest.mark.capstone


def claim(**overrides):
    base = dict(policy_number="LM-1234567", claim_type="auto", loss_date="2026-09-10",
                description="d", estimated_amount_cad=1200.0, injuries_reported=False,
                third_party_involved=False, suspicious_instructions_detected=False, language="en")
    base.update(overrides)
    return ClaimExtraction(**base)


RECEIVED = "2026-09-15"


def test_parse_date():
    assert str(parse_date("2026-09-10")) == "2026-09-10"
    assert parse_date("Sept 10") is None
    assert parse_date(None) is None


def test_clean_small_auto_claim_is_fast_tracked():
    d = route(claim(), RECEIVED)
    assert d.route is Route.fast_track and d.reasons


def test_injury_beats_everything():
    d = route(claim(injuries_reported=True, suspicious_instructions_detected=True, policy_number=None), RECEIVED)
    assert d.route is Route.bodily_injury


def test_injection_goes_to_siu():
    assert route(claim(suspicious_instructions_detected=True), RECEIVED).route is Route.special_investigations


def test_two_model_indicators_go_to_siu():
    d = route(claim(fraud_indicators=["recent_policy_start", "cash_settlement_pressure"]), RECEIVED)
    assert d.route is Route.special_investigations


def test_one_indicator_is_not_enough():
    d = route(claim(fraud_indicators=["unusual_urgency"]), RECEIVED)
    assert d.route is Route.fast_track


def test_future_loss_date_goes_to_siu_with_code_indicator():
    d = route(claim(loss_date="2026-10-03"), RECEIVED)
    assert d.route is Route.special_investigations
    assert "loss_date_after_report" in d.code_indicators


def test_late_report_adds_indicator_and_counts_toward_two():
    d = route(claim(loss_date="2026-07-04"), RECEIVED)
    assert "late_report" in d.code_indicators and d.route is Route.fast_track
    d2 = route(claim(loss_date="2026-07-04", fraud_indicators=["unusual_urgency"]), RECEIVED)
    assert d2.route is Route.special_investigations


@pytest.mark.parametrize("missing", [{"policy_number": None}, {"loss_date": None}, {"loss_date": "last Tuesday"}])
def test_missing_essentials_need_info(missing):
    assert route(claim(**missing), RECEIVED).route is Route.needs_info


@pytest.mark.parametrize("change", [
    {"claim_type": "home"},
    {"estimated_amount_cad": 5000.01},
    {"estimated_amount_cad": None},
    {"third_party_involved": True},
])
def test_not_fast_track_goes_standard(change):
    assert route(claim(**change), RECEIVED).route is Route.standard


def test_fast_track_limit_is_inclusive():
    assert route(claim(estimated_amount_cad=5000.0), RECEIVED).route is Route.fast_track
