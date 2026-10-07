# FDE Training

A free, build-first course that takes you from your first line of code to the skills of a **Forward Deployed Engineer** (FDE): the engineer who works with a customer to build AI systems that fit their world, proves those systems work, and hands them over.

**Read the course:** https://darolution.github.io/FDE-Training/

- **New to coding?** Start with the 8-week **Launchpad**: terminal, Python, Git, web APIs, testing.
- **Already code?** Do the setup and start at **Phase 1**: Claude API, prompting, evals, and your first capstone.
- Phases 2–5 (agents, MCP, architecture, a residency simulation) are outlined and being written.

All customers are fictional and all data is synthetic. Works on Windows, macOS and Linux.

## Quick start

```bash
git clone https://github.com/darolution/FDE-Training.git
cd FDE-Training
python3 -m venv .venv            # Windows: py -3.13 -m venv .venv
source .venv/bin/activate        # Windows: .\.venv\Scripts\Activate.ps1
python -m pip install -r labs/requirements.txt
python -m pytest                 # offline tests; no API key needed
```

Full instructions, including the API key you'll need from Phase 1: [Setup](https://darolution.github.io/FDE-Training/setup/).

## What's in the repo

| Path | What |
|---|---|
| `docs/` | The course website (MkDocs Material) |
| `labs/` | Runnable labs, exercises with automatic checks, datasets, capstone starter code |
| `.github/workflows/` | Tests the labs on Windows and Linux, builds the site, publishes it to GitHub Pages |

## Found a mistake?

Please [open an issue](https://github.com/darolution/FDE-Training/issues/new/choose). Pull requests aren't expected; issues are the best way to report problems or suggest improvements.

## License

- Code (everything outside `docs/`): [MIT](LICENSE)
- Lesson text in `docs/`: [CC BY 4.0](LICENSE-docs.md)

Independent course: not affiliated with or endorsed by Anthropic or any other company named in it.
