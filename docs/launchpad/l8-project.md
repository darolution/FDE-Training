# L8 · Launchpad project

**Goal:** build a small, tested command-line tool from a spec, publish it on GitHub, and start thinking like an FDE.
**Time:** about 10 hours. This is also the [skip test](index.md#skip-test) for people who already code.

## The brief

> A small online outdoor-gear store exports its orders as JSON. The owner wants a quick way to answer questions like *"How much did US customers order?"* or *"Who's our biggest customer among delivered orders?"* without opening a spreadsheet. Build a command-line tool that reads the export and prints a short report.

**When it's done**, these commands work:

```bash
python labs/launchpad/l8/orders_report.py labs/launchpad/data/orders.json
python labs/launchpad/l8/orders_report.py labs/launchpad/data/orders.json --status delivered
python labs/launchpad/l8/orders_report.py labs/launchpad/data/orders.json --country US --json
```

and the second one prints:

```text
Orders: 8
Revenue: $2,747.00
By status: delivered 8
Top customer: Gus Ito ($775.00)
```

## The spec

`labs/launchpad/l8/orders_report.py` has six empty functions, built in order. Their docstrings are the spec, and `labs/launchpad/l8/test_l8.py` turns the spec into tests.

| Step | Function | Does |
|---|---|---|
| 1 | `load_orders(path)` | Reads the JSON file. A missing or broken file exits with a friendly message, not a traceback |
| 2 | `order_total(order)` | Quantity × price for each item, added up |
| 3 | `filter_orders(orders, status, country)` | Keeps matching orders; `None` means "don't filter" |
| 4 | `summarize(orders)` | Count, revenue, counts by status, top customer and their total |
| 5 | `format_report(summary)` | The four-line report shown above |
| 6 | `main(argv)` | Command-line arguments (`argparse`), then load → filter → summarise → print |

```bash
python labs/launchpad/check.py l8
```

??? tip "Hints"
    - Steps 1–3 are close to L3 and L4 exercises you've already solved. Reuse your thinking.
    - **Step 4:** keep two dictionaries while you loop: one counting statuses, one adding up value per customer. Then `max(per_customer, key=per_customer.get)` finds the top customer.
    - **Step 5:** `f"${value:,.2f}"` gives `$2,747.00`. `sorted(by_status.items())` puts statuses in A–Z order.
    - **Step 6:** [argparse](https://docs.python.org/3/library/argparse.html) handles command-line options. Look for `add_argument("path")`, `add_argument("--status")` and `action="store_true"` for `--json`.
    - Missing file: `raise SystemExit("File not found: ...")` exits with a message.

## Publish it

Put the project in its own GitHub repository, so it can stand on its own as a portfolio piece:

1. Make a new folder outside the course (for example `~/Projects/orders-report`) and copy in `orders_report.py`, `test_l8.py` and `orders.json`. In the copied `test_l8.py`, replace the import and setup lines at the top with:

    ```python
    from pathlib import Path
    import json
    import pytest
    import orders_report as app

    ORDERS_FILE = Path(__file__).parent / "orders.json"
    ```

    Give the new folder its own virtual environment (`python -m venv .venv`, activate it, `python -m pip install pytest`) and check that `python -m pytest` passes there.

2. Add a `README.md` covering: what it does, how to run it, an example, and how to run the tests.
3. `git init`, commit in small steps, create the repo on GitHub, and push, just like L5.

## Think like an FDE

Write a short note (half a page) in your README or in `my-notes`:

1. **Who is the user, and what decision does this report help them make?**
2. **What would you ask the store owner before building version 2?** (For example: Should cancelled orders count as revenue? Which currency? How often is the export made?)
3. **What could go wrong with real data that the sample doesn't show?** (Missing fields, refunds, very large files…)

Those three questions (who's it for, what don't I know yet, what breaks in the real world) are the heart of a Forward Deployed Engineer's job. You'll ask them in every capstone from Phase 1 on.

## Launchpad complete

When all L8 checks pass and your project is on GitHub, you have the foundation the rest of the course builds on. Next:

1. Do **step 4 of the [setup](../setup/index.md#4-claude-api-key-needed-from-phase-1)**: a Claude API key with a spend limit. Read [Costs](../costs.md) first.
2. Start **[Phase 1 · Week 1](../phase-1/week-01.md)**.

## Checkpoint

- [ ] `python labs/launchpad/check.py l8` passes all checks
- [ ] The project is in its own GitHub repo, with a README
- [ ] I've written the three "think like an FDE" answers
