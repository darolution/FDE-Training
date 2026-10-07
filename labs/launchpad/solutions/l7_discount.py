"""Reference solution for Launchpad L7 (discount.py with the three bugs fixed)."""


def apply_discount(price, percent):
    if percent < 0 or percent > 100:
        raise ValueError("percent must be between 0 and 100")
    return round(price * (1 - percent / 100), 2)   # bug 1: subtracted the percent as dollars


def shipping_cost(order_total, country):
    if order_total >= 100:                           # bug 2: > excluded exactly $100
        return 0.0
    if country in ("CA", "US"):
        return 9.99
    return 24.99


def split_bill(total, people):
    if people < 1:                                   # bug 3: no check, crashed on 0
        raise ValueError("people must be at least 1")
    return round(total / people, 2)                  # and no rounding to cents
