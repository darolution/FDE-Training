# Costs

*Checked 2026-10-06. Billing details change, so re-check the linked pages.*

## What's free

- The course itself (the site and all the code).
- All of **Launchpad**: Python, Git, GitHub, VS Code and the public API used in L6 are free. (Claude Code in L7 is optional; it needs a paid Claude plan or API credits. The free Claude.ai chat is enough for L7.)
- The optional Splunk lab uses Splunk's own Docker image under its license terms. Check them for your situation.

## What costs money: the Claude API (Phase 1 onwards)

The labs from Phase 1 onwards send requests to Claude through the **Claude API**. That's billed separately from any Claude.ai chat subscription:

- You buy **prepaid usage credits** in the [Claude Console](https://platform.claude.com/). Each request uses a little credit, based on how much text goes in and comes out (counted in *tokens*; see [Week 1](phase-1/week-01.md)).
- Credits **expire one year after purchase** and **aren't refundable**, so buy small amounts.
- **Auto-reload** (automatic top-ups) is optional. Leave it off while you're learning.

**How much?** Running every Phase 1 lab once costs a few US dollars. Iterating on a capstone adds a few more. Expect **tens of dollars across the whole course**, not hundreds. The labs log the cost of every call, so you'll always know where you stand.

## Set a spend limit before your first call

1. In the Console, go to **Settings → Billing → Spend limits** and set a monthly limit you're comfortable with, for example $20.
2. Optional but better: create a **workspace** just for this course, and give it its own spend limit and its own API key. (The default workspace can't have its own limit.)

If a limit is hit, requests fail with an error until the next month or until you raise it. That's annoying, but far better than a surprise bill from a script stuck in a loop.

## Ways to spend less

- Use the **fast** (cheapest) model while you're getting a lab working; switch to bigger models to compare results.
- Run evals on a few cases first (`--only`), then the full set.
- Run `python labs/week01/06_usage_report.py` weekly to see where the money went.

Sources: [How do I pay for my API usage?](https://support.claude.com/en/articles/8977456-how-do-i-pay-for-my-api-usage) · [Rate and spend limits](https://platform.claude.com/docs/en/api/rate-limits) · [Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
