# L7 · Working with AI tools

**Goal:** use AI assistants to learn faster and code better, without handing over your thinking. And learn to write tests, the skill that makes AI-assisted code trustworthy.
**Time:** about 8 hours.

FDEs build with AI tools every day. The skill isn't getting an assistant to produce code; it's knowing **what to ask, how to check the answer, and when not to trust it**.

## Two kinds of AI tool

| Tool | What it is | Cost |
|---|---|---|
| **Claude** chat ([claude.ai](https://claude.ai/) or the Claude app) | Conversation: explain, review, brainstorm. It sees only what you paste in | Has a free plan |
| **Claude Code** | Works inside your project: reads files, runs commands, edits code, with your permission | Needs a paid Claude plan or Console API credits. **Optional in Launchpad** |

Everything in this lesson works with the free chat. Where Claude Code is mentioned, you can paste code into the chat instead.

## Using an assistant while you're learning

Ask for **understanding**, not just answers:

| Instead of… | Try… |
|---|---|
| "Fix my code" | "Explain this error to a beginner and tell me which line to look at. Don't fix it for me." |
| "Write a function that…" | "I wrote this function. What cases might it get wrong? Give hints, not code." |
| "What's wrong?" (no context) | Paste the code, the exact command, and the full error message |

And three rules:

1. **Never paste secrets** (API keys, passwords) or other people's personal data into any AI tool.
2. **Verify everything.** Assistants can be confidently wrong, including about which functions exist. Run the code; read the docs it cites.
3. **You own the result.** If you can't explain a line, don't keep it.

## Claude Code basics (optional)

If you have access, install it with the [official guide](https://code.claude.com/docs/en/overview) and start it **in the course folder**:

```bash
claude
```

- It asks **permission** before editing files or running commands. Read what it wants to do before you approve.
- Good first prompts: *"Explain what labs/launchpad/check.py does, step by step."* or *"Read labs/launchpad/l7/discount.py and tell me which functions look risky, without changing anything."*
- After it changes files, review with `git diff`, exactly as you would a teammate's work.
- Type `/help` to see commands, and `/exit` to leave.

In Phase 2 you'll use Claude Code as a professional delivery tool: project instructions (`CLAUDE.md`), custom skills and guardrail hooks.

## Testing with pytest

AI tools make writing code fast. Tests make it **safe**: they prove the code does what it should, and they keep proving it every time anything changes.

A test is a function whose name starts with `test_` and that uses `assert`:

```python
from discount import apply_discount

def test_ten_percent_off():
    assert apply_discount(200, 10) == 180.0
```

- `assert` checks something is true; if not, the test **fails** and shows both values.
- To check that something raises an error:

    ```python
    import pytest

    def test_rejects_negative():
        with pytest.raises(ValueError):
            apply_discount(100, -5)
    ```

- **pytest** finds files named `test_*.py` and runs every `test_*` function in them.

The professional loop is **red → green**: write a test that fails because of a bug (red), fix the code until it passes (green), and keep the test so the bug can never sneak back.

## Lab: three bugs

`labs/launchpad/l7/discount.py` holds three small pricing functions. Their docstrings describe the correct behaviour, and **each function has a bug**.

1. Read `discount.py`. Work out from the docstrings what each function *should* do.
2. Open `labs/launchpad/l7/test_my_discount.py`. One test is written for you. Add tests that **catch each bug**: they should fail on the current code.
3. Run your tests together with the course's checks:

    ```bash
    python labs/launchpad/check.py l7
    ```

    Watch your new tests fail. That's red.

4. Fix the bugs in `discount.py`, one at a time, re-running after each fix, until everything passes. That's green.
5. Use an assistant **as a reviewer**: paste your tests and ask *"What edge cases are my tests missing?"* Add any good ones.

??? tip "Hints (open one at a time)"
    - `apply_discount`: "10 percent off 200" should be 180. What does the code actually subtract?
    - `shipping_cost`: what happens at **exactly** $100?
    - `split_bill`: what if `people` is 0? And is `10 / 3` "rounded to cents"?

## Exercises

1. **Core.** Complete the lab: all checks green, with at least one test of your own per function.
2. **Core.** Ask an assistant to explain one function from `labs/launchpad/check.py` that you don't understand. Then explain it back in your own words in `labs/launchpad/l1/my-notes/`.
3. **Stretch.** Ask an assistant to write a function `parse_price("$1,249.00") -> 1249.0`. Before using it, write three tests, including a tricky input, and see whether its code passes.

## Checkpoint

- [ ] I ask AI tools for explanations and reviews, and I verify what they say
- [ ] I never paste secrets or personal data into AI tools
- [ ] I can write pytest tests, including for expected errors
- [ ] `python labs/launchpad/check.py l7` passes, including my own tests
