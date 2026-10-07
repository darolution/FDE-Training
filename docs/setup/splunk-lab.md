# Splunk lab (optional security track)

**Who this is for:** anyone curious about security operations or observability. Security teams are common FDE customers, and Splunk is one of the most widely used tools for searching logs. **The main course never requires this lab.**

You'll run a disposable Splunk Enterprise on your own computer, reachable only from your machine, and load it with synthetic security logs that hide six planted incidents. The security-track stretch labs and, later, the observability work in Phase 3 can use it.

*Checked against the [docker-splunk](https://github.com/splunk/docker-splunk) README on 2026-10-06.*

## 1. Install Docker Desktop

**Docker** runs software in an isolated, throw-away *container*.

=== "Windows"

    ```powershell
    winget install Docker.DockerDesktop
    ```

=== "macOS"

    Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop/) and install it.

=== "Linux"

    Follow Docker's instructions for your distribution at [docs.docker.com/engine/install](https://docs.docker.com/engine/install/).

Start Docker once, accept its terms, and check that `docker version` works. Splunk needs about 4 GB of free memory.

## 2. Run Splunk

Make up a password of at least 8 characters for the local admin account, and generate a random token for sending data in:

=== "Windows"

    ```powershell
    $hec = [guid]::NewGuid().ToString()
    $hec   # copy this value; you'll need it in step 3
    docker run -d --name fde-splunk `
      -p 127.0.0.1:8000:8000 -p 127.0.0.1:8089:8089 -p 127.0.0.1:8088:8088 `
      -e SPLUNK_START_ARGS=--accept-license `
      -e SPLUNK_GENERAL_TERMS=--accept-sgt-current-at-splunk-com `
      -e "SPLUNK_PASSWORD=<choose-a-password>" `
      -e "SPLUNK_HEC_TOKEN=$hec" `
      splunk/splunk:latest
    ```

=== "macOS"

    ```bash
    HEC=$(uuidgen); echo $HEC   # copy this value; you'll need it in step 3
    docker run -d --name fde-splunk \
      -p 127.0.0.1:8000:8000 -p 127.0.0.1:8089:8089 -p 127.0.0.1:8088:8088 \
      -e SPLUNK_START_ARGS=--accept-license \
      -e SPLUNK_GENERAL_TERMS=--accept-sgt-current-at-splunk-com \
      -e "SPLUNK_PASSWORD=<choose-a-password>" \
      -e "SPLUNK_HEC_TOKEN=$HEC" \
      splunk/splunk:latest
    ```

=== "Linux"

    ```bash
    HEC=$(cat /proc/sys/kernel/random/uuid); echo $HEC   # copy this value; you'll need it in step 3
    docker run -d --name fde-splunk \
      -p 127.0.0.1:8000:8000 -p 127.0.0.1:8089:8089 -p 127.0.0.1:8088:8088 \
      -e SPLUNK_START_ARGS=--accept-license \
      -e SPLUNK_GENERAL_TERMS=--accept-sgt-current-at-splunk-com \
      -e "SPLUNK_PASSWORD=<choose-a-password>" \
      -e "SPLUNK_HEC_TOKEN=$HEC" \
      splunk/splunk:latest
    ```

Why these settings:

- `127.0.0.1:` on every port keeps Splunk off your network. Without it, Docker makes it reachable from other machines.
- Splunk 10.x images **won't start** without both `SPLUNK_START_ARGS=--accept-license` and `SPLUNK_GENERAL_TERMS=--accept-sgt-current-at-splunk-com`. Running them means you accept Splunk's license and General Terms, so read them first.
- `SPLUNK_HEC_TOKEN` creates a token for Splunk's HTTP Event Collector, the way the labs send data in.

Startup takes a few minutes. Run `docker ps --filter name=fde-splunk` until the status shows `(healthy)`, then open <http://localhost:8000> and sign in as `admin` with your password.

## 3. Configure the labs

In `labs/.env` (create it from `labs/.env.example` if you haven't), set `SPLUNK_PASSWORD` and `SPLUNK_HEC_TOKEN`. Leave `SPLUNK_HOST=localhost` and `SPLUNK_VERIFY_TLS=false`.

!!! note "Why `SPLUNK_VERIFY_TLS=false` is OK here, and only here"
    The container uses a self-signed certificate, so normal certificate checks can't pass. The lab code allows switching the check off **only** for your own computer (`localhost`) and refuses for anything else. Real deployments use proper certificates.

## 4. Create the index and load data

With your virtual environment active, from the course folder:

```bash
python labs/splunk/bootstrap.py
python labs/data/generate_events.py --hec
```

Then search in Splunk Web:

```spl
index=fde_lab | stats count by source
```

You should see `fde:auth`, `fde:proxy` and `fde:endpoint`. The planted incidents and their answers are in `labs/data/out/ground_truth.json`. **Try to find all six with searches before you open it.** New to Splunk's search language? Splunk's free [Search Tutorial](https://help.splunk.com/en/splunk-enterprise/get-started/search-tutorial/10.2/introduction) is a good start.

## Data dictionary

All events use `sourcetype=_json`, so fields are extracted automatically.

| source | Key fields |
|---|---|
| `fde:auth` | `action` (success/failure), `user`, `src`, `src_country`, `src_city`, `dest`, `app` (sso/vpn/windows), `reason` |
| `fde:proxy` | `action`, `user`, `src`, `url`, `url_domain`, `http_method`, `status`, `bytes_out`, `bytes_in`, `category`, `http_user_agent` |
| `fde:endpoint` | `user`, `dest`, `process_name`, `process` (command line), `parent_process_name` |

## Reset

```bash
docker rm -f fde-splunk     # deletes the container and its data
```

Run step 2 again for a clean instance. Events are timestamped relative to when you generated them, so regenerate if they've aged out of your search window.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Container exits right away | Check `docker logs fde-splunk`. Usually a missing terms setting or a password that's too short |
| `bootstrap.py` can't connect | The container is still starting. Wait until `docker ps` shows `(healthy)` |
| HEC returns 403 | The token in `labs/.env` doesn't match the container's. Compare with `docker inspect fde-splunk` |
| HEC returns "Incorrect index" | Run `bootstrap.py` first so the `fde_lab` index exists |
| A search returns nothing | Widen the time picker, or regenerate events if they're older than your window |
