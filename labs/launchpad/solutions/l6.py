"""Reference solutions for Launchpad L6. Try the exercises yourself first!"""

import os
from urllib.parse import urlencode

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def build_forecast_url(latitude, longitude, days):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
        "forecast_days": days,
    }
    return f"{FORECAST_URL}?{urlencode(params)}"


def describe_status(code):
    if 200 <= code <= 299:
        return "success"
    if 400 <= code <= 499:
        return "client error"
    if 500 <= code <= 599:
        return "server error"
    return "other"


def summarize_forecast(data):
    daily = data["daily"]
    lines = []
    for i in range(len(daily["time"])):
        lines.append(
            f"{daily['time'][i]}: {daily['temperature_2m_min'][i]} to {daily['temperature_2m_max'][i]}°C, "
            f"{daily['precipitation_sum'][i]} mm rain"
        )
    return lines


def wettest_day(data):
    daily = data["daily"]
    rain = daily["precipitation_sum"]
    return daily["time"][rain.index(max(rain))]


def get_secret(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value
