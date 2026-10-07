"""Reference solutions for Launchpad L4. Try the exercises yourself first!"""

import csv
import json


def load_orders(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_summary(path, summary):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)


def read_products(path):
    products = []
    with open(path, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            row["price"] = float(row["price"])
            row["stock"] = int(row["stock"])
            products.append(row)
    return products


def low_stock(products, threshold):
    return sorted(p["name"] for p in products if p["stock"] < threshold)


def safe_load_orders(path):
    try:
        return load_orders(path)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def parse_jsonl(text):
    records, bad = [], 0
    for line in text.splitlines():
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            bad += 1
    return records, bad
