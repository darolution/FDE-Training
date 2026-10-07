"""YOUR tests for discount.py. Run them with:  python labs/launchpad/check.py l7

One example test is written for you. Add at least one test per function,
including the edge cases in the docstrings. A good test fails on the buggy
code and passes once the bug is fixed.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from discount import apply_discount, shipping_cost, split_bill  # noqa: E402,F401

pytestmark = pytest.mark.exercise


def test_apply_discount_rejects_negative_percent():
    with pytest.raises(ValueError):
        apply_discount(100, -5)


# TODO: test_apply_discount_takes_a_percentage
#       e.g. assert apply_discount(200, 10) == 180.0


# TODO: test_free_shipping_at_exactly_100


# TODO: test_split_bill_rounds_to_cents and test_split_bill_rejects_zero_people
