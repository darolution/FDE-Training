"""Launchpad L8 project: an orders report on the command line.

When it's finished:

    python labs/launchpad/l8/orders_report.py labs/launchpad/data/orders.json
    python labs/launchpad/l8/orders_report.py labs/launchpad/data/orders.json --status delivered
    python labs/launchpad/l8/orders_report.py labs/launchpad/data/orders.json --country US --json

prints something like:

    Orders: 8
    Revenue: $2,747.00
    By status: delivered 8
    Top customer: Gus Ito ($775.00)

The spec is in the L8 lesson and in test_l8.py. Build it one function at a
time and run `python labs/launchpad/check.py l8` as you go. You can reuse
code you wrote in L3 and L4.
"""

import argparse  # noqa: F401
import json  # noqa: F401
import sys


def load_orders(path):
    """Read the JSON file and return the list of orders. If the file is missing
    or isn't valid JSON, raise SystemExit with a friendly message instead of a traceback."""
    raise NotImplementedError("Step 1: load_orders()")


def order_total(order):
    """quantity x price for each item, added up."""
    raise NotImplementedError("Step 2: order_total()")


def filter_orders(orders, status=None, country=None):
    """Keep orders matching `status` and/or `country`. None means "don't filter on this"."""
    raise NotImplementedError("Step 3: filter_orders()")


def summarize(orders):
    """Return a dictionary:
        {"orders": <count>,
         "revenue": <total of all order totals, rounded to cents>,
         "by_status": {<status>: <count>, ...},
         "top_customer": <name with the highest combined order value, or None>,
         "top_customer_value": <that value rounded to cents, or 0>}
    """
    raise NotImplementedError("Step 4: summarize()")


def format_report(summary):
    """Turn the summary into the four lines shown at the top of this file.

    Revenue and the top customer's value use a dollar sign, thousands separators
    and 2 decimals ({value:,.2f}). Statuses are listed A-Z as "name count",
    separated by ", ". With no orders, "By status: none" and "Top customer: none".
    """
    raise NotImplementedError("Step 5: format_report()")


def main(argv=None):
    """Parse the command line, then load -> filter -> summarize -> print.

    Arguments: a file path, optional --status, optional --country, and a
    --json flag that prints the summary dictionary as JSON instead of the report.
    Return 0 when everything worked.
    """
    raise NotImplementedError("Step 6: main()")


if __name__ == "__main__":
    sys.exit(main())
