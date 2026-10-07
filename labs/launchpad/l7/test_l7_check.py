"""The course's own checks for discount.py. Run with:  python labs/launchpad/check.py l7"""

import pytest

from launchpad._loader import load

pytestmark = pytest.mark.exercise
ex = load("l7")


def test_discount_is_a_percentage():
    assert ex.apply_discount(200, 10) == 180.0
    assert ex.apply_discount(19.99, 0) == 19.99
    assert ex.apply_discount(50, 100) == 0.0


def test_discount_rejects_out_of_range():
    for bad in (-1, 101):
        with pytest.raises(ValueError):
            ex.apply_discount(100, bad)


def test_free_shipping_starts_at_exactly_100():
    assert ex.shipping_cost(100, "CA") == 0.0
    assert ex.shipping_cost(99.99, "US") == 9.99
    assert ex.shipping_cost(50, "FR") == 24.99


def test_split_bill_rounds_and_validates():
    assert ex.split_bill(100, 4) == 25.0
    assert ex.split_bill(10, 3) == 3.33
    with pytest.raises(ValueError):
        ex.split_bill(10, 0)
