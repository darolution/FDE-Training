"""Automatic checks for L6 (offline). Run with:  python labs/launchpad/check.py l6"""

import json
from pathlib import Path

import pytest

from launchpad._loader import load

pytestmark = pytest.mark.exercise
ex = load("l6")
SAMPLE = json.loads((Path(__file__).parent / "sample_forecast.json").read_text(encoding="utf-8"))


def test_1_build_forecast_url():
    assert ex.build_forecast_url(43.7, -79.42, 3) == (
        "https://api.open-meteo.com/v1/forecast?latitude=43.7&longitude=-79.42"
        "&daily=temperature_2m_max%2Ctemperature_2m_min%2Cprecipitation_sum&timezone=auto&forecast_days=3"
    )


@pytest.mark.parametrize("code,expected", [(200, "success"), (201, "success"), (404, "client error"),
                                           (429, "client error"), (503, "server error"), (302, "other")])
def test_2_describe_status(code, expected):
    assert ex.describe_status(code) == expected


def test_3_summarize_forecast():
    assert ex.summarize_forecast(SAMPLE) == [
        "2026-10-07: 6.1 to 15.2°C, 0.0 mm rain",
        "2026-10-08: 4.0 to 12.8°C, 3.2 mm rain",
        "2026-10-09: 1.5 to 9.4°C, 11.6 mm rain",
    ]


def test_4_wettest_day():
    assert ex.wettest_day(SAMPLE) == "2026-10-09"


def test_5_get_secret(monkeypatch):
    monkeypatch.setenv("FDE_TEST_SECRET", "abc123")
    assert ex.get_secret("FDE_TEST_SECRET") == "abc123"
    monkeypatch.delenv("FDE_TEST_SECRET")
    with pytest.raises(RuntimeError, match="FDE_TEST_SECRET"):
        ex.get_secret("FDE_TEST_SECRET")
