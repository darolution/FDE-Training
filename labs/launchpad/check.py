"""Check your Launchpad exercises.

    python labs/launchpad/check.py l3

Runs the automatic checks for one week and tells you how many pass.
It's normal for most checks to fail before you start: each one turns
green as you finish the matching exercise.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
WEEKS = ["l2", "l3", "l4", "l6", "l7", "l8"]


class _Counter:
    def __init__(self) -> None:
        self.passed = 0
        self.failed = 0

    def pytest_runtest_logreport(self, report):  # noqa: D401 - pytest hook
        if report.when == "call":
            if report.passed:
                self.passed += 1
            elif report.failed:
                self.failed += 1


def main(argv: list[str]) -> int:
    if len(argv) != 1 or argv[0].lower() not in WEEKS:
        print(f"Usage: python labs/launchpad/check.py <week>   where <week> is one of: {', '.join(WEEKS)}")
        return 2
    week = argv[0].lower()
    os.chdir(REPO_ROOT)
    counter = _Counter()
    args = [str(HERE / week), "-m", "exercise", "-q", "--no-header", "-p", "no:cacheprovider", "--tb=line"]
    code = pytest.main(args, plugins=[counter])
    total = counter.passed + counter.failed
    print()
    if total and counter.failed == 0:
        print(f"All {total} checks pass for {week.upper()}. Well done!")
    elif total:
        print(f"{counter.passed} of {total} checks pass for {week.upper()}. "
              "Read the first failure above, fix that exercise, and run this again.")
    return int(code)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
