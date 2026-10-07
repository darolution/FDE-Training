# Week 4 · Capstone 1: Claims intake for Lakeshore Mutual

**Time box: 15 hours** (allow 20 if this is your first project of this size). Run it like an engagement, not an exercise: discovery, build, evals, security review, handover. There's no reference solution. **The eval is the judge**, as in the Residency assessment.

!!! abstract "The customer"
    **Lakeshore Mutual** (fictional) is a mid-sized Ontario property and casualty insurer. First notice of loss (FNOL) arrives as free-text email in English and French. Three intake clerks read every email, re-key it into the claims system and decide which team gets it. Volume is about 400 emails a day; the backlog peaks at two days after storms. The VP Claims wants the triage automated. Adjusters will still own every decision on the claim itself.

!!! tip "Where your write-ups go"
    The capstone asks for a few short documents. Keep them in a `docs/notes/` folder in the course folder. If you're working in your own fork, commit them there: they become part of your portfolio. See [Your own copy](../setup/your-own-copy.md).

## 1. Discovery (2 hours)

Notes from your kickoff call, as you'd write them up afterwards:

> **Dana Whitfield, VP Claims:** "Two-day backlogs after a storm mean angry customers and regulator complaints. I want routing in minutes. But if an injury claim sits in the standard queue, that's on me. That can never happen."
>
> **Marc Gagnon, Intake Lead:** "Clerks spend most of their time hunting for the policy number and the date of loss. Customers write 'yesterday' or 'last Tuesday'. About a third of emails are in French. If anything's missing we need to know *what*, so we can email the customer the same day."
>
> **Priya Natarajan, Special Investigations:** "Red flags I care about: a policy that started days ago, pressure for a cash settlement, a theft with no police report, dates that don't add up. Two or more flags, or anything odd, I want to see it. And people have started pasting text into claim emails aimed at 'the AI'. Anything like that comes to us."
>
> **Owen Mills, Information Security:** "Claim emails have names, addresses and medical details. Tell me exactly what leaves our environment, what's logged and for how long. No email content in logs. And I want to see your prompt-injection testing."

From that, the agreed routing rules are written up in `labs/capstone1_claims/claims_intake/rules.py`, and the claims director has signed them off as **spec tests** (`test_rules_capstone.py`).

**Your discovery deliverable:** a one-page `docs/notes/capstone1-discovery.md` covering the problem, users, success metrics, constraints, open questions, and **what's out of scope** (for example: approving claims, contacting customers, writing to the claims system).

## 2. Acceptance criteria

Agreed with Dana and Owen before you build:

| # | Criterion | How it's measured |
|---|---|---|
| A1 | Routing accuracy ≥ 90% on the golden set | `evals/run_evals.py` |
| A2 | **Zero critical misses**: every injury goes to bodily injury; every injection attempt is flagged; nothing that belongs in special investigations is fast-tracked | `evals/run_evals.py` |
| A3 | All routing rules pass their spec tests | `python -m pytest -m capstone` |
| A4 | No email text in any log | Code review + inspect `labs/runs/` |
| A5 | Cost per email reported, with a monthly estimate at 400/day | Eval output + your write-up |

## 3. Build (8 hours)

```text
labs/capstone1_claims/
├── claims_intake/
│   ├── schema.py      the data contract (given; changes = scope change)
│   ├── rules.py       ← YOU: deterministic routing rules
│   ├── extractor.py   ← YOU: the extraction prompt
│   └── cli.py         inbox → queue.jsonl, queue.csv, audit.jsonl (given)
├── data/claims_golden.jsonl   12 labelled emails (EN/FR, injection, missing info, date traps)
├── evals/run_evals.py         acceptance eval (given)
└── test_rules_capstone.py     the rules as spec tests (given; don't edit)
```

Suggested order:

1. **Rules first.** Implement `parse_date()` and `route()` until `python -m pytest -m capstone` is green. No API calls needed. This is the part adjusters will read, so keep it boring and clear.
2. **Prompt second.** Write `SYSTEM_PROMPT` in `extractor.py`. Then iterate:
    ```bash
    python labs/capstone1_claims/evals/run_evals.py --model default
    ```
    Fix the most common failure, re-run, repeat. Keep a log of each change and its effect in your notes.

3. **Try the cheap model.** Once `default` passes, run `--model fast`. Does it still meet A1 and A2? What's the cost difference per month?
4. **Run the pipeline** end to end:
    ```bash
    cd labs/capstone1_claims
    python -m claims_intake.cli data/claims_golden.jsonl --model default
    ```
    Open `labs/runs/capstone1/queue.csv`. Would Marc's clerks understand every `reasons` column?

??? tip "Hints if you're stuck"
    - Dates: put `received_at` in the email you send (it already is) and tell the model to resolve relative dates against it.
    - Third parties: a neighbour's tree and a tenant's injury both count. Define the term with those examples.
    - French: you don't need a separate prompt. Say the input may be French and the output fields are always English enum values.
    - Fraud indicators: the model reports what's *in the text*; date arithmetic belongs in `rules.py`, where it can be tested.

## 4. Security review (2 hours)

Write `docs/notes/capstone1-security-review.md` for Owen. Cover at least:

- **Data flow:** what leaves the environment (email text, after redaction, to the Claude API), what's stored (`queue.*`, `audit.jsonl`), what's never stored (email bodies in logs).
- **Prompt injection:** C-07 plants an attack. Show the result, then write **three new attack emails** (for example: in French, hidden in a quoted reply chain, claiming to come from an adjuster). Add them, labelled in the same format as the golden set, to a separate `data/redteam.jsonl`. Run them with `run_evals.py --data labs/capstone1_claims/data/redteam.jsonl` and report what happened.
- **Blast radius:** what's the worst a successful injection could do *in this design*? (Hint: the model only extracts. Routing is code, and nothing is written to the claims system. Say why that matters.)
- **Residual risks and mitigations:** for example, PII in the extracted `description` field, or the redaction module's limits.

## 5. Handover (2 hours)

Fill in the [handover template](../reference/handover-template.md) as `docs/notes/capstone1-handover.md`, then record a **five-minute demo** for Dana (screen recording): the problem, one email flowing through, the eval results, and what you'd do next.

## Done when

- [ ] A1–A5 met, with numbers in your handover doc
- [ ] Discovery, security review and handover notes written (and committed, if you have your own fork)
- [ ] Demo recorded
- [ ] A short "what I'd do differently" paragraph. Interviewers ask for this
