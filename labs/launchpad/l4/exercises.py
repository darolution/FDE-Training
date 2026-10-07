"""Launchpad L4 exercises: files, JSON, CSV and handling errors.

Files you'll read are in labs/launchpad/data/:
    orders.json         a list of orders (JSON)
    products.csv        the product catalogue (CSV: sku,name,category,price,stock)
    messy_orders.jsonl  one JSON object per line, with some broken lines

Check your work:   python labs/launchpad/check.py l4
"""

import csv  # noqa: F401  (you'll use these)
import json  # noqa: F401


def load_orders(path):
    """Read a JSON file and return what's in it (here: a list of orders).

    Hint:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    """
    raise NotImplementedError("Exercise 1: write load_orders()")


def save_summary(path, summary):
    """Write the dictionary `summary` to `path` as JSON, indented by 2 spaces so people can read it.

    Hint: open the file with "w" (write) mode and use json.dump(summary, f, indent=2).
    """
    raise NotImplementedError("Exercise 2: write save_summary()")


def read_products(path):
    """Read the products CSV and return a list of dictionaries.

    CSV files hold everything as text, so convert: "price" to a float and "stock" to an int.
    Example item: {"sku": "LAMP-400", "name": "Headlamp 400", "category": "lighting", "price": 39.0, "stock": 40}
    Hint: csv.DictReader(f) gives you one dictionary per row.
    """
    raise NotImplementedError("Exercise 3: write read_products()")


def low_stock(products, threshold):
    """Return the names of products with stock below `threshold`, sorted A-Z."""
    raise NotImplementedError("Exercise 4: write low_stock()")


def safe_load_orders(path):
    """Like load_orders(), but return an empty list instead of crashing when
    the file doesn't exist or doesn't contain valid JSON.

    Hint: try / except FileNotFoundError / except json.JSONDecodeError
    """
    raise NotImplementedError("Exercise 5: write safe_load_orders()")


def parse_jsonl(text):
    """Parse text with one JSON object per line.

    Skip blank lines. Count lines that aren't valid JSON instead of crashing.
    Return a tuple: (list_of_records, number_of_bad_lines)

    parse_jsonl('{"a": 1}\\n\\nnot json\\n{"a": 2}')  ->  ([{"a": 1}, {"a": 2}], 1)
    """
    raise NotImplementedError("Exercise 6: write parse_jsonl()")
