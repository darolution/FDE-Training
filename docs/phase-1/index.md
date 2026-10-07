# Phase 1 · Foundations

**Weeks 1–4 · about 50 hours.** By the end you can call Claude reliably and cheaply, write prompts that hold up on messy input, prove quality with an eval, and deliver a small system to a customer with the paperwork to match.

## Skip-ahead checkpoint

If you can do all of these without looking anything up, skim Weeks 1–2, do the Week 3 eval lab properly, and go straight to the capstone.

- [ ] Explain what `stop_reason: "max_tokens"` means and what your code should do about it
- [ ] Estimate the monthly cost of 10,000 calls a day for a given prompt on two different models
- [ ] Get a response that's guaranteed to match a JSON schema
- [ ] Say why `temperature=0` returns a 400 on current models, and what to use instead to get consistent outputs
- [ ] Cache a long system prompt and show the saving in the usage fields
- [ ] Build a golden set, grade it in code, and fail a CI run on a regression

## The weeks

1. [Claude API essentials](week-01.md)
2. [Prompting for real work](week-02.md)
3. [Evals](week-03.md)
4. [Capstone 1: Claims intake for Lakeshore Mutual](week-04-capstone.md)

## Lab layout

```text
labs/
├── fde_common/        shared helpers: config, logged API calls, costs, redaction, Splunk client
├── data/              datasets: tickets_golden.jsonl, synthetic security telemetry generator
├── week01/ … week03/  one script per lab, run from the repo root
├── capstone1_claims/  the capstone: starter code, golden set, eval harness, spec tests
└── tests/             offline tests (python -m pytest)
```

Run every lab from the **repo root** with the venv active, for example `python labs\week01\01_hello.py`.

## Budget

Running every Phase 1 lab once costs a few dollars. Iterating on the capstone prompt with the default model adds a few more. Check `python labs\week01\06_usage_report.py` at the end of each week.
