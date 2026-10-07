# L6 · The web and APIs

**Goal:** understand how programs talk over the internet, and call a real web API from Python.
**Time:** about 8 hours.

## How the web works, in one minute

When your browser opens a page, it sends a **request** to a server, and the server sends back a **response**. The rules for that conversation are **HTTP**.

A request has:

- a **method**: `GET` (fetch something) or `POST` (send something), plus a few others,
- a **URL**: `https://api.open-meteo.com/v1/forecast?latitude=43.7&longitude=-79.42`
    - `https://` is the protocol (the `s` means encrypted)
    - `api.open-meteo.com` is the server
    - `/v1/forecast` is the **path**, also called the **endpoint**
    - everything after `?` is the **query string**: `name=value` pairs joined by `&`
- **headers**: extra information, such as an API key,
- sometimes a **body**: data you send, usually JSON.

A response has a **status code**, headers and a body.

| Status | Meaning | What to do |
|---|---|---|
| 200–299 | Success | Use the body |
| 400 | Bad request | Your request is malformed; fix it |
| 401 / 403 | Not authorised / forbidden | Check your key or permissions |
| 404 | Not found | Check the URL |
| 429 | Too many requests | Slow down and retry later |
| 500–599 | Server error | Their problem; retry later |

## APIs

A **web API** is a server built for programs rather than people: you send a request, and it replies with **data**, usually JSON, instead of a web page. The Claude API you'll use from Phase 1 works exactly this way.

Try one in your browser right now. Paste this into the address bar:

```text
https://api.open-meteo.com/v1/forecast?latitude=43.7&longitude=-79.42&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto&forecast_days=3
```

That's a weather forecast as JSON. [Open-Meteo](https://open-meteo.com/) is free for non-commercial use and needs no key. Note the `daily` section: lists that line up by position.

## Calling an API from Python

The `httpx` package (already installed) makes HTTP requests:

```python
import httpx

response = httpx.get("https://api.open-meteo.com/v1/forecast",
                     params={"latitude": 43.7, "longitude": -79.42,
                             "daily": "temperature_2m_max", "timezone": "auto"},
                     timeout=15)
print(response.status_code)        # 200
data = response.json()             # body as Python dictionaries and lists
print(data["daily"]["time"])
```

Habits to build now:

- **Always set a timeout.** Without one, a slow server can make your program wait forever.
- **Check the status code** before using the body.
- **Expect failure.** Networks drop and servers have bad days. Catch `httpx.HTTPError` and give a useful message.

## API keys and environment variables

Most APIs want a **key**: a secret string proving who's calling, so they can bill you or limit you. Two rules:

1. **Never put a key in your code.** Code gets shared, pushed and screenshotted.
2. **Read it from an environment variable** instead: a setting that lives in your terminal session or in a `.env` file that git ignores.

```python
import os
key = os.environ.get("WEATHER_API_KEY")
if not key:
    raise RuntimeError("Missing environment variable: WEATHER_API_KEY")
```

From Phase 1, your Claude API key lives in `labs/.env`, and the course code reads it exactly this way.

## Exercises

To keep them fast and offline, the exercises use a **saved** response in `labs/launchpad/l6/sample_forecast.json`. Testing against saved responses is a standard professional technique.

```bash
python labs/launchpad/check.py l6
```

| # | Exercise | Practises |
|---|---|---|
| 1 | `build_forecast_url` | URLs and query strings |
| 2 | `describe_status` | status-code ranges |
| 3 | `summarize_forecast` | reading nested JSON |
| 4 | `wettest_day` | lists that line up by position |
| 5 | `get_secret` | environment variables and clear errors |

When exercises 1–4 pass, call the **live** API with your own code:

```bash
python labs/launchpad/l6/weather.py
python labs/launchpad/l6/weather.py 51.51 -0.13 5     # London, 5 days
```

??? success "What weather.py prints"
    ```text
    GET https://api.open-meteo.com/v1/forecast?latitude=43.7&longitude=-79.42&daily=...

    Status: 200 (success)
      2026-10-07: 6.1 to 15.2°C, 0.0 mm rain
      2026-10-08: 4.0 to 12.8°C, 3.2 mm rain
      2026-10-09: 1.5 to 9.4°C, 11.6 mm rain

    Wettest day: 2026-10-09
    ```
    (Live numbers will differ.)

**Stretch.** Change `weather.py` to a city you care about, and add the daily `wind_speed_10m_max` to the request and the summary. Read [Open-Meteo's docs](https://open-meteo.com/en/docs) to find the exact name. Reading API docs is half of an FDE's job.

## Checkpoint

- [ ] I can explain a URL's parts and what common status codes mean
- [ ] I can call an API from Python with a timeout and check the result
- [ ] I keep keys in environment variables, never in code
- [ ] `python labs/launchpad/check.py l6` passes, and `weather.py` prints a live forecast
