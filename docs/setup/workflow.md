# Git and publishing

The repo is the source of truth. GitHub Actions builds this site from `docs/` with MkDocs Material, runs the offline tests, and deploys to GitHub Pages on every push to `main`.

**Site:** <https://darolution.github.io/FDT-Training/>

## First push (once)

The repo `darolution/FDT-Training` exists but has no commits yet. From PowerShell:

```powershell
cd "D:\Claude Docs\FDE-Training"
# one-time: put the Pages workflow where GitHub expects it
New-Item -ItemType Directory -Force .github\workflows | Out-Null
Move-Item pages.yml.move-me .github\workflows\pages.yml
git init -b main
git config user.name "Your Name"
git config user.email "you@example.com"     # or your GitHub noreply address
git status                                   # labs\.env must NOT be listed
git add .
git commit -m "Course site and Phase 1 materials"
git remote add origin https://github.com/darolution/FDT-Training.git
git push -u origin main
```

!!! tip "Keep your email private"
    GitHub gives you a noreply address under Settings → Emails. Use it for `user.email` if you'd rather your personal address didn't appear in a public commit history.

## Turn on Pages and protections (once)

In the repo on GitHub:

1. **Settings → Pages → Build and deployment → Source: GitHub Actions.**
2. **Settings → Code security**: turn on secret scanning and **push protection**. Pushes that contain a recognisable key get blocked.
3. Optional: **Settings → Branches**: protect `main` and require the "Publish site" check to pass.

Then open the **Actions** tab. The first run builds and deploys. When it's green, the site URL appears on the run summary.

## Every week

```powershell
.\.venv\Scripts\Activate.ps1
python -m pytest                 # offline tests
pip install -r requirements-docs.txt   # once
mkdocs serve -a 127.0.0.1:8001  # preview (8000 is Splunk Web)
git add .
git commit -m "Week 2: prompt ladder results and notes"
git push
```

`mkdocs build --strict` runs in CI, so a broken internal link fails the build. Run it locally if a push goes red.

## What goes where

| Path | Contents | Committed? |
|---|---|---|
| `docs/` | Lessons, capstone briefs, your write-ups | Yes |
| `labs/` | Lab code, datasets, tests | Yes |
| `labs/.env` | Your keys | **Never** |
| `labs/runs/` | Usage logs, eval results | No (git-ignored). Copy the eval summaries you want to keep into your write-ups |
| `labs/data/out/` | Generated telemetry | No (regenerate any time) |

## Your work vs the course

Write your own notes and capstone write-ups in `docs/notes/` (create it and add pages to `nav` in `mkdocs.yml`). Keep the reference material unchanged so you can tell later what you added.

## Commit messages

Say what changed and why, in the present tense: `Capstone 1: add date-resolution rule to extractor prompt (fixes C-02, C-09)`. Your commit history is part of your portfolio.
