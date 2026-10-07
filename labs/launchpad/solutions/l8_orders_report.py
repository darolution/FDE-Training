"""Reference solution for the Launchpad L8 project. Build yours first!"""

import argparse
import json
import sys


def load_orders(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise SystemExit(f"File not found: {path}")
    except json.JSONDecodeError:
        raise SystemExit(f"Not valid JSON: {path}")


def order_total(order):
    return sum(item["qty"] * item["price"] for item in order["items"])


def filter_orders(orders, status=None, country=None):
    result = []
    for order in orders:
        if status is not None and order["status"] != status:
            continue
        if country is not None and order["country"] != country:
            continue
        result.append(order)
    return result


def summarize(orders):
    by_status = {}
    per_customer = {}
    revenue = 0.0
    for order in orders:
        value = order_total(order)
        revenue += value
        by_status[order["status"]] = by_status.get(order["status"], 0) + 1
        per_customer[order["customer"]] = per_customer.get(order["customer"], 0) + value
    top = max(per_customer, key=per_customer.get) if per_customer else None
    return {
        "orders": len(orders),
        "revenue": round(revenue, 2),
        "by_status": by_status,
        "top_customer": top,
        "top_customer_value": round(per_customer[top], 2) if top else 0,
    }


def format_report(summary):
    statuses = ", ".join(f"{name} {count}" for name, count in sorted(summary["by_status"].items())) or "none"
    top = (f"{summary['top_customer']} (${summary['top_customer_value']:,.2f})"
           if summary["top_customer"] else "none")
    return "\n".join([
        f"Orders: {summary['orders']}",
        f"Revenue: ${summary['revenue']:,.2f}",
        f"By status: {statuses}",
        f"Top customer: {top}",
    ])


def main(argv=None):
    parser = argparse.ArgumentParser(description="Summarise an orders JSON file.")
    parser.add_argument("path", help="path to orders.json")
    parser.add_argument("--status", help="only orders with this status")
    parser.add_argument("--country", help="only orders from this country code")
    parser.add_argument("--json", action="store_true", help="print the summary as JSON")
    args = parser.parse_args(argv)

    orders = filter_orders(load_orders(args.path), status=args.status, country=args.country)
    summary = summarize(orders)
    print(json.dumps(summary, indent=2) if args.json else format_report(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
