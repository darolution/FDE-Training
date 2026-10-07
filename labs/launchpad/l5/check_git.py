"""Launchpad L5 - check your git setup.

    python labs/launchpad/l5/check_git.py [path-to-your-practice-repo]

Checks that git is installed and configured, and (if you give it a path)
that your practice repository has commits, a second branch, a remote, and
no .env file committed.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def git(*args: str, cwd: Path | None = None) -> tuple[int, str]:
    try:
        result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    except FileNotFoundError:
        return 127, ""
    return result.returncode, result.stdout.strip()


def check(label: str, ok: bool, hint: str = "") -> bool:
    print(f"  [{'x' if ok else ' '}] {label}" + ("" if ok or not hint else f"\n        -> {hint}"))
    return ok


def main(argv: list[str]) -> int:
    results = []
    print("Git setup")
    code, version = git("--version")
    results.append(check(f"git is installed ({version or 'not found'})", code == 0,
                         "Install git: see Launchpad L1 / the setup page"))
    _, name = git("config", "--global", "user.name")
    results.append(check(f"user.name is set ({name or 'missing'})", bool(name),
                         'git config --global user.name "Your Name"'))
    _, email = git("config", "--global", "user.email")
    results.append(check("user.email is set", bool(email),
                         "git config --global user.email you@example.com  (or your GitHub noreply address)"))

    if argv:
        repo = Path(argv[0]).expanduser().resolve()
        print(f"\nPractice repo: {repo}")
        code, _ = git("rev-parse", "--is-inside-work-tree", cwd=repo)
        results.append(check("it's a git repository", code == 0, "Run `git init` inside it, or clone it"))
        if code == 0:
            _, count = git("rev-list", "--count", "HEAD", cwd=repo)
            results.append(check(f"has at least 3 commits ({count or 0})", count.isdigit() and int(count) >= 3,
                                 "Make small changes and commit each one"))
            _, branches = git("branch", "--list", "--all", cwd=repo)
            n_local = len([b for b in branches.splitlines() if "remotes/" not in b])
            results.append(check("has at least 2 branches", n_local >= 2, "git switch -c my-feature"))
            _, remotes = git("remote", cwd=repo)
            results.append(check("is connected to GitHub (has a remote)", bool(remotes),
                                 "Create a repo on GitHub, then: git remote add origin <url>"))
            _, tracked = git("ls-files", cwd=repo)
            leaked = [f for f in tracked.splitlines() if Path(f).name == ".env"]
            results.append(check("no .env file is committed", not leaked,
                                 "Remove it with `git rm --cached .env`, add .env to .gitignore, "
                                 "and treat any key that was inside as leaked"))

    print(f"\n{sum(results)} of {len(results)} checks pass.")
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
