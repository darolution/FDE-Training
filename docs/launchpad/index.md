# Launchpad

**8 weeks · about 8–10 hours a week · no prior experience needed · free** (Claude Code in L7 is optional and needs a paid plan).

Launchpad takes you from "I've never used a terminal" to writing tested Python programs that read data, call web APIs and live on GitHub. Those are the everyday skills Phase 1 builds on.

## How each week works

- **Lesson:** short explanations with examples to type in yourself. Typing beats copy-pasting while you're learning.
- **Exercises:** small functions in `labs/launchpad/lN/` for you to complete. Each has an **automatic checker**:

    ```bash
    python labs/launchpad/check.py l3
    ```

    It tells you how many exercises pass. It's normal for everything to fail at first: each check turns green as you finish an exercise.

- **Solutions** are in `labs/launchpad/solutions/`. Use them **after** you've tried, to compare approaches.
- **Checkpoint:** a list of things you can now do. Tick them off before moving on.

| Week | Topic | You'll be able to |
|---|---|---|
| [L1](l1-terminal.md) | Your computer as a workshop | Use a terminal, move around folders, install tools, use VS Code |
| [L2](l2-python-basics.md) | Python 1 | Write and run scripts with variables, text and numbers |
| [L3](l3-python-data.md) | Python 2 | Use lists, dictionaries, loops, `if` and functions |
| [L4](l4-python-files.md) | Python 3 | Read and write files, JSON and CSV; handle errors; manage packages |
| [L5](l5-git.md) | Git and GitHub | Save versions of your work, branch, push to GitHub, keep secrets out |
| [L6](l6-apis.md) | The web and APIs | Call a web API from Python and handle what comes back |
| [L7](l7-ai-tools.md) | Working with AI tools | Use Claude and Claude Code as a coding partner, and write tests with pytest |
| [L8](l8-project.md) | Launchpad project | Build, test and publish a small command-line tool |

## When you get stuck

Getting stuck is normal; it's most of programming. In order:

1. **Read the error message from the bottom up.** The last line says what went wrong; the lines above say where.
2. **Check the basics:** Is your virtual environment active? Are you in the course folder? Did you save the file?
3. **Search the exact error text** (leave out your own file names).
4. **Ask an AI assistant to explain the error, not to write the answer.** For example: *"Explain this Python error to a beginner and tell me where to look. Don't give me the fixed code."* L7 covers this properly.
5. Still stuck? Look at the solution, then close it and write your own version from memory.

## Skip test

Already code a bit? The **[L8 project](l8-project.md)** is the skip test. Do the [setup](../setup/index.md), then try to finish L8 without the lessons:

```bash
python labs/launchpad/check.py l8
```

- **All checks pass within about 3 hours:** skip Launchpad and go to [Phase 1](../phase-1/index.md). Skim [L7](l7-ai-tools.md) for the Claude Code basics.
- **Some pass:** do the Launchpad weeks that cover what you struggled with.
- **Not sure where to begin:** start at L1. You'll move fast through what you know.
