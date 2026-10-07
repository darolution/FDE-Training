# Workstation setup

About an hour on Windows 11 with PowerShell. Checked 2026-10-06.

## 1. Tools

Skip anything you already have.

```powershell
winget install Git.Git
winget install Python.Python.3.13
winget install GitHub.cli          # optional, handy for repo settings
```

Close and reopen PowerShell, then check:

```powershell
git --version
py -3.13 --version
```

**Claude Code.** Check with `claude --version`. If you don't have it, follow the [official install guide](https://code.claude.com/docs/en/overview). The native installer auto-updates; WinGet installs don't (`winget upgrade Anthropic.ClaudeCode`).

## 2. The repo

The course lives in `D:\Claude Docs\FDE-Training` and publishes to `github.com/darolution/FDT-Training`. First-time git and publishing steps are in [Git and publishing](workflow.md).

## 3. Python environment

From the repo root:

```powershell
cd "D:\Claude Docs\FDE-Training"
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r labs\requirements.txt
python -m pytest
```

The last command runs the offline test suite (no key needed). Expect all tests to pass, with the capstone tests deselected.

??? tip "PowerShell won't run Activate.ps1?"
    Allow local scripts for your user only:
    `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## 4. API key with a spend limit

1. In the [Claude Console](https://platform.claude.com/), create a **workspace** just for this course.
2. Set a **monthly spend limit** on it. Around $25 is plenty for Phase 1.
3. Create an API key in that workspace.
4. Copy the template and add the key:

```powershell
Copy-Item labs\.env.example labs\.env
notepad labs\.env
```

Check it:

```powershell
python labs\week01\01_hello.py
```

You should see a three-sentence answer, the token counts and a cost of a fraction of a cent.

!!! warning "Keep the key out of everything else"
    Don't put it in PowerShell history (`$env:ANTHROPIC_API_KEY = ...` gets saved), screenshots or prompts. `labs\.env` is git-ignored, so keep it there.

## 5. Optional: security track

To do the security-track stretch labs, set up the [Splunk lab](splunk-lab.md) (Docker Desktop, about 30 minutes).

## Checkpoint

- [ ] `python -m pytest` is green
- [ ] `01_hello.py` prints an answer and a cost
- [ ] `labs\.env` exists and `git status` doesn't list it
