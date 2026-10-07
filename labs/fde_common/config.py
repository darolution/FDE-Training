"""Settings loaded from labs/.env, with safety checks.

Two rules are enforced in code rather than left to discipline:
  * TLS verification may only be disabled for a loopback Splunk host.
  * The API key is never printed in full.
"""

from __future__ import annotations

import ipaddress
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

LABS_DIR = Path(__file__).resolve().parent.parent
LOOPBACK_NAMES = {"localhost"}


class ConfigError(RuntimeError):
    """Raised when settings are missing or unsafe."""


def _load_env() -> None:
    # labs/.env wins over a stray .env elsewhere; real environment variables win over both.
    load_dotenv(LABS_DIR / ".env", override=False)


def is_loopback(host: str) -> bool:
    host = host.strip().strip("[]").lower()
    if host in LOOPBACK_NAMES or host.endswith(".localhost"):
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def _bool(value: str | None, default: bool) -> bool:
    if value is None or value.strip() == "":
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def mask(secret: str, keep: int = 6) -> str:
    if not secret:
        return "<empty>"
    return secret[:keep] + "..." if len(secret) > keep else "***"


@dataclass(frozen=True)
class Models:
    fast: str
    default: str
    best: str


@dataclass(frozen=True)
class SplunkSettings:
    host: str
    mgmt_port: int
    hec_port: int
    username: str
    password: str
    hec_token: str
    index: str
    verify_tls: bool

    @property
    def mgmt_url(self) -> str:
        return f"https://{self.host}:{self.mgmt_port}"

    @property
    def hec_url(self) -> str:
        return f"https://{self.host}:{self.hec_port}"


def models() -> Models:
    _load_env()
    return Models(
        fast=os.getenv("FDE_MODEL_FAST", "claude-haiku-4-5-20251001"),
        default=os.getenv("FDE_MODEL_DEFAULT", "claude-sonnet-5-5"),
        best=os.getenv("FDE_MODEL_BEST", "claude-opus-5-5"),
    )


def require_api_key() -> str:
    _load_env()
    key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not key:
        raise ConfigError(
            "ANTHROPIC_API_KEY is not set. Copy labs/.env.example to labs/.env and add your key."
        )
    return key


def splunk_settings() -> SplunkSettings:
    _load_env()
    settings = SplunkSettings(
        host=os.getenv("SPLUNK_HOST", "localhost"),
        mgmt_port=int(os.getenv("SPLUNK_MGMT_PORT", "8089")),
        hec_port=int(os.getenv("SPLUNK_HEC_PORT", "8088")),
        username=os.getenv("SPLUNK_USERNAME", "admin"),
        password=os.getenv("SPLUNK_PASSWORD", ""),
        hec_token=os.getenv("SPLUNK_HEC_TOKEN", ""),
        index=os.getenv("SPLUNK_INDEX", "fde_lab"),
        verify_tls=_bool(os.getenv("SPLUNK_VERIFY_TLS"), default=True),
    )
    check_tls_policy(settings.host, settings.verify_tls)
    return settings


def check_tls_policy(host: str, verify_tls: bool) -> None:
    """Refuse to talk to a non-loopback host without certificate verification."""
    if not verify_tls and not is_loopback(host):
        raise ConfigError(
            f"SPLUNK_VERIFY_TLS=false is only allowed for a loopback host, not {host!r}. "
            "Use a trusted certificate for any other host."
        )
