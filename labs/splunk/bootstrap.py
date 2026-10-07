"""Check the local Splunk lab and create the lab index.

    python labs/splunk/bootstrap.py

Exits non-zero with a hint if something is wrong.
"""

from __future__ import annotations

import sys
from pathlib import Path

LABS_DIR = Path(__file__).resolve().parent.parent
if str(LABS_DIR) not in sys.path:
    sys.path.insert(0, str(LABS_DIR))

import httpx  # noqa: E402

from fde_common.config import ConfigError, splunk_settings  # noqa: E402
from fde_common.splunk import SplunkClient  # noqa: E402


def main() -> int:
    try:
        s = splunk_settings()
    except ConfigError as e:
        print(f"Config problem: {e}")
        return 1
    if not s.password or not s.hec_token:
        print("Set SPLUNK_PASSWORD and SPLUNK_HEC_TOKEN in labs/.env (see docs/setup/splunk-lab.md).")
        return 1

    try:
        with SplunkClient(s) as sc:
            print(f"Splunk version: {sc.server_version()}")
            created = sc.ensure_index(s.index)
            print(f"Index {s.index!r}: {'created' if created else 'already exists'}")
            print(f"HEC healthy: {sc.hec_healthy()}")
            check = sc.parse("index=fde_lab | stats count")
            print(f"SPL parser reachable: {check.ok}")
    except httpx.ConnectError:
        print("Can't reach Splunk. Is the container running?  docker ps --filter name=fde-splunk")
        return 1
    except httpx.HTTPStatusError as e:
        print(f"Splunk returned {e.response.status_code} for {e.request.url.path}. Check username/password.")
        return 1
    print("Lab ready. Next: python labs/data/generate_events.py --hec")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
