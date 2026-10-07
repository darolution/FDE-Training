# L4 · Python 3: files, JSON, errors and packages

**Goal:** read and write real data files, handle things going wrong, and understand packages and virtual environments.
**Time:** about 9 hours.

## Reading and writing files

```python
with open("labs/launchpad/data/products.csv", encoding="utf-8") as f:
    text = f.read()
print(text)
```

- `open(path)` opens a file; `encoding="utf-8"` makes accented letters (é, ü) work on every computer.
- `with` closes the file for you when the block ends, even if something fails.
- Open with `"w"` to **write** (this replaces the file) or `"a"` to **append**:

```python
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("First line\n")      # \n is a new line
```

## JSON

**JSON** is the most common data format on the web. It looks like Python lists and dictionaries, and the `json` module converts between the two:

```python
import json

with open("labs/launchpad/data/orders.json", encoding="utf-8") as f:
    orders = json.load(f)          # file -> Python list of dictionaries

print(orders[0]["customer"])

summary = {"orders": len(orders)}
with open("summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)   # Python -> file, nicely indented
```

`json.loads(text)` and `json.dumps(value)` do the same with text instead of files.

**JSON Lines** (`.jsonl`) puts one JSON object on each line. It's common for logs and datasets, including the support tickets you'll use in Phase 1.

## CSV

**CSV** files are spreadsheets as plain text. The `csv` module reads each row as a dictionary:

```python
import csv

with open("labs/launchpad/data/products.csv", encoding="utf-8", newline="") as f:
    for row in csv.DictReader(f):
        print(row["name"], row["price"])
```

Everything in a CSV is text: `row["price"]` is `"39.00"`, not `39.0`. Convert with `float(...)` or `int(...)`.

## When things go wrong: exceptions

When Python can't do something, it **raises an exception** and stops:

```text
FileNotFoundError: [Errno 2] No such file or directory: 'ordres.json'
```

Read error messages from the **bottom up**: the last line says what happened, the lines above (the *traceback*) say where.

You can **catch** exceptions you expect and handle them:

```python
try:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Can't find {path}")
    data = []
except json.JSONDecodeError:
    print(f"{path} isn't valid JSON")
    data = []
```

Only catch errors you know how to handle. A bare `except:` that hides every problem makes bugs much harder to find.

## Modules, packages and pip

- A **module** is a Python file you can `import`. `json`, `csv` and `math` come with Python (the *standard library*).
- A **package** is code other people publish, installed with **pip**. The course needs a few: `anthropic`, `httpx`, `pydantic`, `pytest`, `python-dotenv`.
- `labs/requirements.txt` lists them with **exact versions**, so everyone gets the same setup:

```bash
python -m pip install -r labs/requirements.txt
python -m pip list            # what's installed in this environment
```

## Virtual environments, properly

You created `.venv` in L1. Here's why it matters:

- Different projects need different packages and versions. Installed globally, they'd clash.
- A virtual environment is a folder (`.venv`) holding a private copy of Python's package list for **one** project.
- **Activating** it points `python` and `pip` at that folder. That's why your prompt shows `(.venv)`.
- It's disposable: if it breaks, delete `.venv` and recreate it with the setup commands.
- It's never uploaded to GitHub (`.gitignore` excludes it). `requirements.txt` is what you share.

Try it: run `deactivate`, then `python -m pip list`. You'll see a different list (or an error). Activate again and run it once more.

## Exercises

Open `labs/launchpad/l4/exercises.py`. The data files are in `labs/launchpad/data/`.

```bash
python labs/launchpad/check.py l4
```

| # | Exercise | Practises |
|---|---|---|
| 1 | `load_orders` | reading JSON |
| 2 | `save_summary` | writing JSON |
| 3 | `read_products` | CSV and type conversion |
| 4 | `low_stock` | filtering and sorting |
| 5 | `safe_load_orders` | catching exceptions |
| 6 | `parse_jsonl` | line-by-line parsing that survives bad data |

!!! info "Why exercise 6 matters"
    Real data is messy. A system that crashes on one bad line out of a million is a system the customer can't use. Counting and skipping bad records, then reporting how many were skipped, is a pattern you'll use constantly.

**Stretch.** Write a script that reads `orders.json` and writes `labs/launchpad/l4/report.json` with the number of orders per country, using your functions from L3 and L4.

## Checkpoint

- [ ] I can read and write text, JSON and CSV files
- [ ] I can read a traceback and catch an expected exception
- [ ] I can explain what a virtual environment is for, and recreate one
- [ ] `python labs/launchpad/check.py l4` passes all 6 checks
