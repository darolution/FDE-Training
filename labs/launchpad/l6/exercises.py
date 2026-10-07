"""Launchpad L6 exercises: web APIs, JSON responses, status codes and secrets.

We use Open-Meteo, a free weather API that needs no key for non-commercial use.
These exercises work on a *saved* response (sample_forecast.json), so they run
offline. weather.py then uses your functions on live data.

Check your work:   python labs/launchpad/check.py l6
"""

import os  # noqa: F401  (you'll use it)
from urllib.parse import urlencode  # noqa: F401

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def build_forecast_url(latitude, longitude, days):
    """Build the full request URL for a daily forecast.

    Query parameters, in this order:
        latitude, longitude,
        daily=temperature_2m_max,temperature_2m_min,precipitation_sum
        timezone=auto
        forecast_days=<days>

    build_forecast_url(43.7, -79.42, 3) ->
      "https://api.open-meteo.com/v1/forecast?latitude=43.7&longitude=-79.42&daily=temperature_2m_max%2Ctemperature_2m_min%2Cprecipitation_sum&timezone=auto&forecast_days=3"

    Hint: urlencode({...}) builds the part after the "?" (and turns "," into "%2C").
    """
    raise NotImplementedError("Exercise 1: write build_forecast_url()")


def describe_status(code):
    """Describe an HTTP status code by its range.

    200-299 -> "success", 400-499 -> "client error" (your request is wrong),
    500-599 -> "server error" (their side), anything else -> "other".
    """
    raise NotImplementedError("Exercise 2: write describe_status()")


def summarize_forecast(data):
    """Turn a forecast response (a dictionary) into one line of text per day.

    data["daily"] has lists that line up by position: "time",
    "temperature_2m_max", "temperature_2m_min", "precipitation_sum".

    Return a list like:
        ["2026-10-07: 6.1 to 15.2°C, 0.0 mm rain", ...]
    Hint: for i in range(len(daily["time"])): ...
    """
    raise NotImplementedError("Exercise 3: write summarize_forecast()")


def wettest_day(data):
    """Return the date (string) with the most precipitation. If several tie, the first one."""
    raise NotImplementedError("Exercise 4: write wettest_day()")


def get_secret(name):
    """Return the value of the environment variable `name`.

    If it's missing or empty, raise RuntimeError with a message that says which
    variable is missing, e.g. "Missing environment variable: WEATHER_API_KEY".
    Never print or return a made-up value. Hint: os.environ.get(name)
    """
    raise NotImplementedError("Exercise 5: write get_secret()")
