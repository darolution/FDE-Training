"""Offline tests for the shared lab helpers. No API key or Splunk needed."""

import json
from types import SimpleNamespace

import pytest

from fde_common import llm
from fde_common.config import ConfigError, check_tls_policy, is_loopback, mask
from fde_common.costs import cost_usd, total_input_tokens
from fde_common.redact import redact
from fde_common.splunk import normalize_spl


# --- costs ---------------------------------------------------------------
def test_plain_cost_haiku():
    # 1M in at $1 + 1M out at $5
    assert cost_usd("claude-haiku-4-5-20251001", {"input_tokens": 1_000_000, "output_tokens": 1_000_000}) == pytest.approx(6.0)


def test_cache_read_and_write_multipliers_sonnet():
    usage = {"input_tokens": 0, "output_tokens": 0, "cache_read_input_tokens": 1_000_000,
             "cache_creation": {"ephemeral_5m_input_tokens": 1_000_000, "ephemeral_1h_input_tokens": 1_000_000}}
    # read 0.1 x $2 + write5m 1.25 x $2 + write1h 2 x $2
    assert cost_usd("claude-sonnet-5-5", usage) == pytest.approx(0.2 + 2.5 + 4.0)


def test_opus_cache_read_is_cheaper():
    usage = {"input_tokens": 0, "output_tokens": 0, "cache_read_input_tokens": 1_000_000}
    assert cost_usd("claude-opus-5-5", usage) == pytest.approx(0.20)


def test_unknown_model_raises():
    with pytest.raises(KeyError):
        cost_usd("claude-sonnet-4-6-20250417", {"input_tokens": 1, "output_tokens": 1})


def test_total_input_tokens():
    assert total_input_tokens({"input_tokens": 5, "cache_read_input_tokens": 100, "cache_creation_input_tokens": 20}) == 125


# --- config --------------------------------------------------------------
@pytest.mark.parametrize("host", ["localhost", "127.0.0.1", "::1", "[::1]", "splunk.localhost"])
def test_loopback_hosts(host):
    assert is_loopback(host)


@pytest.mark.parametrize("host", ["splunk.corp.example", "10.0.0.5", "192.168.1.20"])
def test_non_loopback_hosts(host):
    assert not is_loopback(host)


def test_tls_off_refused_for_remote_host():
    with pytest.raises(ConfigError):
        check_tls_policy("splunk.corp.example", verify_tls=False)
    check_tls_policy("localhost", verify_tls=False)  # allowed
    check_tls_policy("splunk.corp.example", verify_tls=True)  # allowed


def test_mask_never_reveals_full_secret():
    assert mask("sk-ant-abcdefghijklmnop") == "sk-ant..."
    assert mask("") == "<empty>"


# --- redaction -------------------------------------------------------------
def test_redacts_secrets_and_identifiers():
    raw = ("key sk-ant-api03-ABCDEFGHIJKLMNOP password=hunter2 card 4111 1111 1111 1111 "
           "SIN 046 454 286 mail jo@example.com Authorization: Bearer abcdefghijklmnopqrstuvwxyz")
    clean, counts = redact(raw)
    for secret in ["sk-ant-api03", "hunter2", "4111 1111", "046 454 286", "jo@example.com", "abcdefghijklmnopqrst"]:
        assert secret not in clean
    assert counts["anthropic_key"] == 1 and counts["email"] == 1


def test_redaction_leaves_order_ids_alone():
    clean, counts = redact("order NW-104233 for $189.99")
    assert clean == "order NW-104233 for $189.99" and counts == {}


# --- splunk helpers ----------------------------------------------------------
@pytest.mark.parametrize("spl,expected", [
    ("index=fde_lab | stats count", "search index=fde_lab | stats count"),
    ("search index=fde_lab", "search index=fde_lab"),
    ("| tstats count where index=fde_lab", "| tstats count where index=fde_lab"),
])
def test_normalize_spl(spl, expected):
    assert normalize_spl(spl) == expected


# --- llm wrapper (fake client, no network) -----------------------------------
def test_call_logs_usage_without_content(tmp_path, monkeypatch):
    log = tmp_path / "usage.jsonl"
    monkeypatch.setattr(llm, "USAGE_LOG", log)
    monkeypatch.setattr(llm, "log_usage", lambda rec, path=log: path.open("a").write(json.dumps(rec) + "\n"))

    usage = SimpleNamespace(input_tokens=100, output_tokens=50, cache_read_input_tokens=0,
                            cache_creation_input_tokens=0, cache_creation=None)
    response = SimpleNamespace(model="claude-haiku-4-5-20251001", usage=usage, stop_reason="end_turn",
                               content=[SimpleNamespace(type="text", text="secret answer")])
    fake = SimpleNamespace(messages=SimpleNamespace(create=lambda **kw: response))

    r = llm.call(fake, label="test", model="claude-haiku-4-5-20251001", max_tokens=10,
                 messages=[{"role": "user", "content": "secret prompt"}])
    assert llm.text_of(r) == "secret answer"
    rec = json.loads(log.read_text().strip())
    assert rec["input_tokens"] == 100 and rec["label"] == "test"
    assert rec["cost_usd"] == pytest.approx((100 * 1 + 50 * 5) / 1_000_000)
    assert "secret" not in log.read_text()  # prompts and answers are never logged


def test_ticket_triage_plumbing_with_fake_client(tmp_path, monkeypatch):
    """triage() sends a redacted, tagged ticket and returns the parsed object; caching wraps the system prompt."""
    from week02.tickets import TicketTriage, load_tickets, triage

    monkeypatch.setattr(llm, "log_usage", lambda rec, path=None: None)
    parsed = TicketTriage(category="order_status", priority="normal", sentiment="neutral", language="en",
                          needs_human=False, suspicious_instructions_detected=False, order_id="NW-104233", summary="s")
    seen = {}

    def fake_parse(**kw):
        seen.update(kw)
        usage = SimpleNamespace(input_tokens=10, output_tokens=5, cache_read_input_tokens=0,
                                cache_creation_input_tokens=0, cache_creation=None)
        return SimpleNamespace(model=kw["model"], usage=usage, stop_reason="end_turn", parsed_output=parsed)

    fake = SimpleNamespace(messages=SimpleNamespace(parse=fake_parse))
    result, _ = triage(fake, "claude-haiku-4-5-20251001", load_tickets()[0], cache=True)
    assert result.order_id == "NW-104233"
    assert seen["output_format"] is TicketTriage
    assert seen["messages"][0]["content"].startswith("<ticket>")
    assert seen["system"][0]["cache_control"] == {"type": "ephemeral"}
