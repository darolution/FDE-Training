# Setup

About an hour. Pick your operating system in any tab below and the rest of the site follows your choice. *Checked 2026-10-06.*

!!! tip "Brand new to all this?"
    Launchpad week [L1](../launchpad/l1-terminal.md) walks through the terminal and installing these tools slowly, with explanations. Do that first and come back here for steps 4 and 5.

## 1. Install the tools

You need **Git**, **Python 3.12 or newer**, and **VS Code** (a free code editor).

=== "Windows"

    Open **PowerShell** (Start menu → type "PowerShell") and run:

    ```powershell
    winget install Git.Git
    winget install Python.Python.3.13
    winget install Microsoft.VisualStudioCode
    ```

    Close PowerShell, open a new one, and check:

    ```powershell
    git --version
    py -3.13 --version
    ```

=== "macOS"

    1. Install Git: open **Terminal** (Spotlight → "Terminal") and run `xcode-select --install`. Accept the prompt.
    2. Install Python 3.13 with the official installer from [python.org/downloads](https://www.python.org/downloads/).
    3. Install VS Code from [code.visualstudio.com](https://code.visualstudio.com/).

    Check in a new Terminal window:

    ```bash
    git --version
    python3 --version
    ```

=== "Linux"

    On Ubuntu or Debian:

    ```bash
    sudo apt update
    sudo apt install git python3 python3-venv python3-pip
    ```

    Install VS Code from [code.visualstudio.com](https://code.visualstudio.com/). Check:

    ```bash
    git --version
    python3 --version    # needs to be 3.12 or newer
    ```

You also need a free [GitHub](https://github.com/) account.

## 2. Get the course files

Choose where to keep the course (for example, a `Projects` folder in your home folder), then **clone** it. Cloning downloads a copy you can run.

=== "Windows"

    ```powershell
    cd $HOME
    mkdir Projects -ErrorAction SilentlyContinue
    cd Projects
    git clone https://github.com/darolution/FDE-Training.git
    cd FDE-Training
    ```

=== "macOS"

    ```bash
    mkdir -p ~/Projects && cd ~/Projects
    git clone https://github.com/darolution/FDE-Training.git
    cd FDE-Training
    ```

=== "Linux"

    ```bash
    mkdir -p ~/Projects && cd ~/Projects
    git clone https://github.com/darolution/FDE-Training.git
    cd FDE-Training
    ```

From now on, **"the course folder"** means this `FDE-Training` folder. Run every command from inside it.

!!! note "Want to save your own work to GitHub?"
    Clone is enough to follow the course. If you'd like your own copy on GitHub, for your notes, capstone work and portfolio, [fork it instead](your-own-copy.md).

## 3. Python environment

A **virtual environment** is a private set of Python packages for one project, so the course doesn't clash with anything else on your computer.

=== "Windows"

    ```powershell
    py -3.13 -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    python -m pip install -r labs/requirements.txt
    ```

    If PowerShell refuses to run `Activate.ps1`, allow local scripts for your user once:
    `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then try again.

=== "macOS"

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install -r labs/requirements.txt
    ```

=== "Linux"

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install -r labs/requirements.txt
    ```

Your prompt now starts with `(.venv)`. **Activate the environment every time you open a new terminal** for the course (the second line above). Then check everything installed:

```bash
python -m pytest
```

You should see a line ending in `passed` with some tests `deselected`. No API key is needed for this.

## 4. Claude API key (needed from Phase 1)

Launchpad learners can skip this until Phase 1.

1. Read [Costs](../costs.md), then create an account in the [Claude Console](https://platform.claude.com/) and buy a small amount of credit.
2. Set a **spend limit**, and ideally create a course-only **workspace** with its own key.
3. Create an **API key** and copy it.
4. Make your settings file from the template and open it in VS Code:

    === "Windows"

        ```powershell
        Copy-Item labs/.env.example labs/.env
        code labs/.env
        ```

    === "macOS"

        ```bash
        cp labs/.env.example labs/.env
        code labs/.env
        ```

    === "Linux"

        ```bash
        cp labs/.env.example labs/.env
        code labs/.env
        ```

    (If `code` isn't found, open the file from VS Code's **File → Open** menu.)

5. Paste your key after `ANTHROPIC_API_KEY=` and save.
6. Test it:

    ```bash
    python labs/week01/01_hello.py
    ```

    You should see a short answer, token counts and a cost of a fraction of a cent.

!!! warning "Keep the key in `labs/.env` and nowhere else"
    Not in code, screenshots, chat messages or your terminal history. `labs/.env` is git-ignored, so it never gets uploaded.

## 5. Claude Code (optional in Launchpad L7, needed from Phase 2)

Claude Code is Anthropic's coding assistant that works in your terminal and editor. It needs a paid Claude plan or Console API credits. Install it with the [official guide](https://code.claude.com/docs/en/overview), then check with `claude --version`.

## 6. Optional: security track

If you'd like to do the security-track stretch labs, set up the [Splunk lab](splunk-lab.md) (Docker, about 30 minutes). The main course never requires it.

## Checkpoint

- [ ] `git --version` and `python --version` work (inside the activated environment)
- [ ] `python -m pytest` shows tests passed
- [ ] From Phase 1: `python labs/week01/01_hello.py` prints an answer and a cost, and `git status` doesn't list `labs/.env`
