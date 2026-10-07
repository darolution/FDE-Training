"""Launchpad L7 - a small pricing module with THREE bugs in it.

Your job (see the L7 lesson for the full steps):
  1. Read the docstrings: they describe the correct behaviour.
  2. Write tests in test_my_discount.py that catch each bug (they should FAIL at first).
  3. Fix the bugs here until your tests and `python labs/launchpad/check.py l7` pass.

You may ask Claude or Claude Code to explain the code, but find and fix the bugs yourself first.
"""


def apply_discount(price, percent):
    """Return the price after taking `percent` percent off, rounded to cents.

    apply_discount(200, 10)   ->  180.0
    apply_discount(19.99, 0)  ->  19.99
    `percent` must be between 0 and 100; otherwise raise ValueError.
    """
    if percent < 0 or percent > 100:
        raise ValueError("percent must be between 0 and 100")
    return round(price - percent, 2)


def shipping_cost(order_total, country):
    """Shipping is free for orders of $100 or more. Otherwise $9.99 in "CA" and "US", $24.99 anywhere else."""
    if order_total > 100:
        return 0.0
    if country in ("CA", "US"):
        return 9.99
    return 24.99


def split_bill(total, people):
    """Split a total evenly and round each share to cents.

    split_bill(100, 4)  ->  25.0
    split_bill(10, 3)   ->  3.33
    If `people` is less than 1, raise ValueError (don't crash with ZeroDivisionError).
    """
    return total / people
