# FDE Training

A 24-week, build-first course in Forward Deployed Engineer skills with Claude: API fundamentals, prompting, evals, tool use, agents, MCP, enterprise architecture and customer delivery. Each phase ends in a capstone for a different fictional customer.

**Read it as a site:** https://darolution.github.io/FDE-Training/

## Quick start (Windows, PowerShell)

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r labs\requirements.txt
python -m pytest                      # offline tests, no key needed
Copy-Item labs\.env.example labs\.env # then add your API key
python labs\week01\01_hello.py
```

Full instructions: [`docs/setup/index.md`](docs/setup/index.md).

## Layout

| Path | What |
|---|---|
| `docs/` | The course site (MkDocs Material) |
| `labs/` | Runnable labs, datasets, capstone starter code and tests |
| `.github/workflows/pages.yml` | Tests, builds and publishes the site to GitHub Pages |

All data is synthetic. Not affiliated with or endorsed by Anthropic or Splunk.
