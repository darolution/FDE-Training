# Splunk lab (optional, security track)

A disposable Splunk Enterprise in Docker, reachable only from your own machine, loaded with synthetic telemetry that has six planted incidents. Used by the security-track stretch labs and, in Phase 3, as the observability backend for your agents.

Checked against the [docker-splunk](https://github.com/splunk/docker-splunk) README on 2026-10-06.

## 1. Docker Desktop

```powershell
winget install Docker.DockerDesktop
```

Start Docker Desktop once, accept its terms, and make sure `docker version` works.

## 2. Run Splunk

Pick a password of at least 8 characters for the local admin account and a random HEC token:

```powershell
$hec = [guid]::NewGuid().ToString()
$hec   # copy this into labs\.env as SPLUNK_HEC_TOKEN
docker run -d --name fde-splunk `
  -p 127.0.0.1:8000:8000 -p 127.0.0.1:8089:8089 -p 127.0.0.1:8088:8088 `
  -e SPLUNK_START_ARGS=--accept-license `
  -e SPLUNK_GENERAL_TERMS=--accept-sgt-current-at-splunk-com `
  -e "SPLUNK_PASSWORD=<choose-a-password>" `
  -e "SPLUNK_HEC_TOKEN=$hec" `
  splunk/splunk:latest
```

Why these flags:

- `127.0.0.1:` on every port keeps Splunk off your network. Without it, Docker listens on all interfaces.
- Splunk 10.x images **won't start** unless you pass both `SPLUNK_START_ARGS=--accept-license` and `SPLUNK_GENERAL_TERMS=--accept-sgt-current-at-splunk-com`. Running them means you accept Splunk's license and General Terms, so read them first.
- `SPLUNK_HEC_TOKEN` makes the image create an HTTP Event Collector token for you.

Startup takes a few minutes. Run `docker ps --filter name=fde-splunk` until the status shows `(healthy)`, then open <http://localhost:8000>.

## 3. Configure the labs

In `labs\.env` set `SPLUNK_PASSWORD` and `SPLUNK_HEC_TOKEN`. Leave `SPLUNK_HOST=localhost` and `SPLUNK_VERIFY_TLS=false`.

!!! note "About `SPLUNK_VERIFY_TLS=false`"
    The container uses a self-signed certificate, so verification can't pass. `fde_common/config.py` only allows switching it off for a loopback host and raises an error for anything else. Real deployments use a certificate from a CA you trust.

## 4. Create the index and load data

```powershell
python labs\splunk\bootstrap.py
python labs\data\generate_events.py --hec
```

Then in Splunk Web:

```spl
index=fde_lab | stats count by source
```

You should see `fde:auth`, `fde:proxy` and `fde:endpoint`. The planted incidents and their answers are in `labs\data\out\ground_truth.json`. **Try to find all six with SPL before you open it.**

## Data dictionary

All events use `sourcetype=_json`, so fields extract automatically.

| source | Key fields |
|---|---|
| `fde:auth` | `action` (success/failure), `user`, `src`, `src_country`, `src_city`, `dest`, `app` (sso/vpn/windows), `reason` |
| `fde:proxy` | `action`, `user`, `src`, `url`, `url_domain`, `http_method`, `status`, `bytes_out`, `bytes_in`, `category`, `http_user_agent` |
| `fde:endpoint` | `user`, `dest`, `process_name`, `process` (command line), `parent_process_name` |

## Reset

```powershell
docker rm -f fde-splunk     # deletes the container and its data
```

Re-run step 2 for a clean instance. Events are timestamped relative to now, so regenerate them if they've aged out of your search window.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Container exits right away | Check `docker logs fde-splunk`. Usually a missing terms flag or a password that's too short. |
| `bootstrap.py` can't connect | The container is still starting. Wait until `docker ps` shows `(healthy)`. |
| HEC returns 403 | The token in `.env` doesn't match the container's. Compare with `docker inspect fde-splunk`. |
| HEC returns "Incorrect index" | Run `bootstrap.py` first so `fde_lab` exists. |
| A search returns nothing | Widen the time picker, or regenerate events if they're older than your window. |
