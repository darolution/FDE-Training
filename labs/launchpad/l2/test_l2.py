"""Automatic checks for L2. Run with:  python labs/launchpad/check.py l2"""

import pytest

from launchpad._loader import load

pytestmark = pytest.mark.exercise
ex = load("l2")


def test_1_greeting():
    assert ex.greeting("Ava") == "Hello, Ava! Welcome to the course."
    assert ex.greeting("Kofi") == "Hello, Kofi! Welcome to the course."


def test_2_minutes_to_hours():
    assert ex.minutes_to_hours(90) == 1.5
    assert ex.minutes_to_hours(45) == 0.75
    assert ex.minutes_to_hours(0) == 0


def test_3_total_with_tax():
    assert ex.total_with_tax(100, 0.13) == 113.0
    assert ex.total_with_tax(19.99, 0.05) == 20.99


def test_4_initials():
    assert ex.initials("ava", "chen") == "A.C."
    assert ex.initials("Kofi", "adeyemi") == "K.A."


def test_5_shout():
    assert ex.shout("  order shipped ") == "ORDER SHIPPED!"
    assert ex.shout("hi") == "HI!"


def test_6_word_count():
    assert ex.word_count("where is my order") == 4
    assert ex.word_count("") == 0
    assert ex.word_count("  extra   spaces  here ") == 3


def test_7_receipt_line():
    assert ex.receipt_line("Headlamp", 2, 39) == "2 x Headlamp @ $39.00 = $78.00"
    assert ex.receipt_line("Tent", 1, 249.5) == "1 x Tent @ $249.50 = $249.50"


def test_8_is_long_message():
    assert ex.is_long_message("hello", 3) is True
    assert ex.is_long_message("hi", 3) is False
    assert ex.is_long_message("abc", 3) is False
