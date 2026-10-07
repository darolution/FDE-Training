"""Minimal Splunk REST + HEC client for the local lab.

Endpoints used (Splunk Enterprise 10.x):
  POST /services/search/parser            - validate SPL without running it (400 on error)
  POST /services/search/v2/jobs/export    - run a search and stream results
  POST /services/data/indexes             - create an index
  POST /services/collector/event          - HTTP Event Collector (port 8088)
  GET  /services/collector/health         - HEC health check
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import Any

import httpx

from .config import SplunkSettings, splunk_settings


@dataclass
class ParseResult:
    ok: bool
    messages: list[str]


def normalize_spl(spl: str) -> str:
    """The REST API needs an explicit leading command: `search ...` or `| tstats ...`."""
    spl = spl.strip()
    if spl.startswith("|") or spl.lower().startswith("search "):
        return spl
    return "search " + spl


class SplunkClient:
    def __init__(self, settings: SplunkSettings | None = None, timeout: float = 60.0):
        self.s = settings or splunk_settings()
        self._mgmt = httpx.Client(
            base_url=self.s.mgmt_url,
            auth=(self.s.username, self.s.password),
            verify=self.s.verify_tls,
            timeout=timeout,
        )
        self._hec = httpx.Client(
            base_url=self.s.hec_url,
            headers={"Authorization": f"Splunk {self.s.hec_token}"},
            verify=self.s.verify_tls,
            timeout=timeout,
        )

    def close(self) -> None:
        self._mgmt.close()
        self._hec.close()

    def __enter__(self) -> "SplunkClient":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    # --- management API -------------------------------------------------
    def server_version(self) -> str:
        r = self._mgmt.get("/services/server/info", params={"output_mode": "json"})
        r.raise_for_status()
        return r.json()["entry"][0]["content"]["version"]

    def ensure_index(self, name: str) -> bool:
        """Create the index if missing. Returns True if it was created."""
        r = self._mgmt.post("/services/data/indexes", data={"name": name, "output_mode": "json"})
        if r.status_code == 409:
            return False
        r.raise_for_status()
        return True

    def parse(self, spl: str) -> ParseResult:
        r = self._mgmt.post(
            "/services/search/parser",
            data={"q": normalize_spl(spl), "output_mode": "json"},
        )
        if r.status_code == 200:
            return ParseResult(ok=True, messages=[])
        try:
            msgs = [m.get("text", "") for m in r.json().get("messages", [])]
        except ValueError:
            msgs = [r.text[:500]]
        return ParseResult(ok=False, messages=msgs or [f"HTTP {r.status_code}"])

    def search(
        self,
        spl: str,
        earliest: str = "-24h",
        latest: str = "now",
        max_results: int = 1000,
    ) -> list[dict[str, Any]]:
        """Run a blocking export search and return result rows."""
        rows: list[dict[str, Any]] = []
        with self._mgmt.stream(
            "POST",
            "/services/search/v2/jobs/export",
            data={
                "search": normalize_spl(spl),
                "earliest_time": earliest,
                "latest_time": latest,
                "output_mode": "json",
                "count": str(max_results),
            },
        ) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if not line.strip():
                    continue
                obj = json.loads(line)
                if "result" in obj:
                    rows.append(obj["result"])
                    if len(rows) >= max_results:
                        break
        return rows

    # --- HEC ------------------------------------------------------------
    def hec_healthy(self) -> bool:
        r = self._hec.get("/services/collector/health")
        return r.status_code == 200

    def hec_send(self, events: Iterable[dict[str, Any]], batch_size: int = 500) -> int:
        """Send HEC envelopes ({time, host, source, sourcetype, index, event}). Returns count sent."""
        sent = 0
        for batch in _batched(events, batch_size):
            body = "\n".join(json.dumps(e) for e in batch)
            r = self._hec.post("/services/collector/event", content=body)
            r.raise_for_status()
            sent += len(batch)
        return sent


def _batched(items: Iterable[dict[str, Any]], size: int) -> Iterator[list[dict[str, Any]]]:
    batch: list[dict[str, Any]] = []
    for item in items:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch
