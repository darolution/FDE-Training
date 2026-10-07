"""Offline checks that the datasets are well-formed and the graders behave."""

import ipaddress
import json

import pytest

from claims_intake.schema import ClaimExtraction, Route
from data.generate_events import generate
from week02.tickets import Category, Priority, load_tickets, render_ticket
from week03.graders import consistency, grade_ticket, percentile, summarize
from fde_common.config import LABS_DIR


# --- ticket golden set ---------------------------------------------------------
def test_ticket_labels_are_valid_enums():
    tickets = load_tickets()
    assert len(tickets) >= 20
    assert len({t["id"] for t in tickets}) == len(tickets)
    for t in tickets:
        e = t["expected"]
        Category(e["category"])
        assert e["priority"] and all(Priority(p) for p in e["priority"])
        assert e["language"] in {"en", "fr", "other"}


def test_rendered_ticket_never_leaks_expected_labels():
    for t in load_tickets():
        rendered = render_ticket(t)
        assert "expected" not in rendered and "needs_human" not in rendered


def test_golden_set_covers_hard_cases():
    tickets = load_tickets()
    assert sum(t["expected"]["suspicious_instructions_detected"] for t in tickets) >= 2
    assert sum(t["expected"]["language"] == "fr" for t in tickets) >= 2
    assert sum("urgent" in t["expected"]["priority"] for t in tickets) >= 3


# --- graders ------------------------------------------------------------------
EXP = {"category": "damaged_item", "priority": ["urgent"], "language": "en", "needs_human": True,
       "suspicious_instructions_detected": False, "order_id": "NW-103377", "sentiment": ["negative", "angry"]}


def test_perfect_answer_passes():
    got = {"category": "damaged_item", "priority": "urgent", "language": "en", "needs_human": True,
           "suspicious_instructions_detected": False, "order_id": "nw-103377 ", "sentiment": "angry"}
    g = grade_ticket(EXP, got)
    assert g["passed"] and g["critical"] == []


def test_missed_escalation_and_underrated_urgent_are_critical():
    got = {"category": "damaged_item", "priority": "normal", "language": "en", "needs_human": False,
           "suspicious_instructions_detected": False, "order_id": "NW-103377", "sentiment": "negative"}
    g = grade_ticket(EXP, got)
    assert not g["passed"]
    assert set(g["critical"]) == {"missed_escalation", "underrated_urgent"}


def test_summary_and_consistency():
    ok = {"checks": {"category": True, "priority": True}, "passed": True, "critical": []}
    bad = {"checks": {"category": False, "priority": True}, "passed": False, "critical": ["missed_injection"]}
    s = summarize([ok, bad])
    assert s["all_fields_correct"] == 0.5 and s["field_accuracy"]["category"] == 0.5
    assert s["critical_total"] == 1
    runs = [[{"category": "a"}, {"category": "b"}], [{"category": "a"}, {"category": "c"}]]
    assert consistency(runs) == 0.5
    assert percentile([1, 2, 3, 4, 5], 50) == 3


# --- synthetic security telemetry ------------------------------------------------
def test_generator_is_deterministic_and_plants_incidents():
    ev1, truth1 = generate(seed=42, hours=24)
    ev2, truth2 = generate(seed=42, hours=24)
    assert len(ev1) == len(ev2) and [t["id"] for t in truth1] == [t["id"] for t in truth2]
    assert {t["type"] for t in truth1} >= {"brute_force_success", "password_spray", "impossible_travel",
                                           "suspicious_process", "possible_exfiltration", "prompt_injection_bait"}
    assert all(e["index"] == "fde_lab" and e["sourcetype"] == "_json" for e in ev1)


def test_generator_uses_only_non_routable_or_documentation_addresses():
    events, _ = generate(seed=1, hours=6)
    for e in events:
        ip = ipaddress.ip_address(e["event"].get("src", "10.0.0.1"))
        assert ip.is_private or ip in ipaddress.ip_network("203.0.113.0/24") \
            or ip in ipaddress.ip_network("198.51.100.0/24") or ip in ipaddress.ip_network("192.0.2.0/24")


# --- capstone 1 golden set -------------------------------------------------------
def test_claims_golden_is_well_formed():
    path = LABS_DIR / "capstone1_claims" / "data" / "claims_golden.jsonl"
    rows = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(rows) >= 10
    for r in rows:
        Route(r["expected"]["route"])
        assert r["received_at"][:4] == "2026"
    assert {r["expected"]["route"] for r in rows} == {x.value for x in Route}


def test_claim_schema_accepts_minimal_extraction():
    x = ClaimExtraction(claim_type="auto", description="d", injuries_reported=False, third_party_involved=False,
                        suspicious_instructions_detected=False, language="en")
    assert x.policy_number is None and x.fraud_indicators == []


@pytest.mark.parametrize("field", ["policy_number", "loss_date", "estimated_amount_cad"])
def test_claim_schema_fields_are_nullable(field):
    assert ClaimExtraction.model_fields[field].default is None
