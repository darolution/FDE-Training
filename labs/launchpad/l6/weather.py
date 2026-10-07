"""Launchpad L6 - call a real API.

    python labs/launchpad/l6/weather.py [latitude] [longitude] [days]
    python labs/launchpad/l6/weather.py 51.51 -0.13 5      # London, 5 days

Uses YOUR functions from exercises.py, so finish exercises 1-4 first.
Default location: Toronto. Find coordinates for your city by searching
"<city> latitude longitude".
"""

import importlib.util
import sys
from pathlib import Path

import httpx

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("l6_exercises", HERE / "exercises.py")
ex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ex)

lat = float(sys.argv[1]) if len(sys.argv) > 1 else 43.7
lon = float(sys.argv[2]) if len(sys.argv) > 2 else -79.42
days = int(sys.argv[3]) if len(sys.argv) > 3 else 3

url = ex.build_forecast_url(lat, lon, days)
print(f"GET {url}\n")

try:
    response = httpx.get(url, timeout=15)
except httpx.HTTPError as e:
    sys.exit(f"Couldn't reach the API: {e}. Check your internet connection and try again.")

print(f"Status: {response.status_code} ({ex.describe_status(response.status_code)})")
if response.status_code != 200:
    sys.exit(f"The API said: {response.text[:300]}")

data = response.json()
for line in ex.summarize_forecast(data):
    print(" ", line)
print(f"\nWettest day: {ex.wettest_day(data)}")
