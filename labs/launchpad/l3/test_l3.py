"""Automatic checks for L3. Run with:  python labs/launchpad/check.py l3"""

import json

import pytest

from launchpad._loader import DATA, load

pytestmark = pytest.mark.exercise
ex = load("l3")
ORDERS = json.loads((DATA / "orders.json").read_text(encoding="utf-8"))


def test_1_total():
    assert ex.total([10.0, 5.5, 4.5]) == 20.0
    assert ex.total([]) == 0


def test_2_most_expensive():
    assert ex.most_expensive([19.0, 249.0, 39.0]) == 249.0
    assert ex.most_expensive([]) is None


def test_3_order_total():
    assert ex.order_total({"items": [{"qty": 2, "price": 39.0}, {"qty": 1, "price": 19.0}]}) == 97.0
    assert ex.order_total({"items": []}) == 0


def test_4_priority_label():
    assert ex.priority_label(650) == "high"
    assert ex.priority_label(500) == "high"
    assert ex.priority_label(100) == "medium"
    assert ex.priority_label(99) == "low"


def test_5_only_status():
    shipped = ex.only_status(ORDERS, "shipped")
    assert [o["id"] for o in shipped] == ["A-1003", "A-1011", "A-1014", "A-1018", "A-1020"]
    assert ex.only_status(ORDERS, "lost") == []


def test_6_count_by_status():
    assert ex.count_by_status(ORDERS) == {"cancelled": 3, "processing": 4, "shipped": 5, "delivered": 8}
    assert ex.count_by_status([]) == {}


def test_7_customers_in_country():
    assert ex.customers_in_country(ORDERS, "US") == ["Dev Patel", "Elif Yilmaz", "Gus Ito", "Ivan Petrov"]
    assert ex.customers_in_country(ORDERS, "FR") == []


def test_8_biggest_order():
    assert ex.biggest_order(ORDERS) == "A-1007"
    assert ex.biggest_order([]) is None
