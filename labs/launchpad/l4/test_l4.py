"""Automatic checks for L4. Run with:  python labs/launchpad/check.py l4"""

import json

import pytest

from launchpad._loader import DATA, load

pytestmark = pytest.mark.exercise
ex = load("l4")


def test_1_load_orders():
    orders = ex.load_orders(DATA / "orders.json")
    assert isinstance(orders, list) and len(orders) == 20
    assert orders[0]["id"] == "A-1001"


def test_2_save_summary(tmp_path):
    out = tmp_path / "summary.json"
    ex.save_summary(out, {"orders": 20, "status": "ok"})
    text = out.read_text(encoding="utf-8")
    assert json.loads(text) == {"orders": 20, "status": "ok"}
    assert "\n  " in text, "Use indent=2 so the file is readable"


def test_3_read_products():
    products = ex.read_products(DATA / "products.csv")
    assert len(products) == 10
    lamp = next(p for p in products if p["sku"] == "LAMP-400")
    assert lamp == {"sku": "LAMP-400", "name": "Headlamp 400", "category": "lighting", "price": 39.0, "stock": 40}


def test_4_low_stock():
    products = ex.read_products(DATA / "products.csv")
    assert ex.low_stock(products, 5) == ["Camp stove", "Rain jacket", "Sleeping bag -10C"]
    assert ex.low_stock(products, 0) == []


def test_5_safe_load_orders(tmp_path):
    assert ex.safe_load_orders(tmp_path / "does-not-exist.json") == []
    broken = tmp_path / "broken.json"
    broken.write_text("{ this is not valid json", encoding="utf-8")
    assert ex.safe_load_orders(broken) == []
    assert len(ex.safe_load_orders(DATA / "orders.json")) == 20


def test_6_parse_jsonl():
    assert ex.parse_jsonl('{"a": 1}\n\nnot json\n{"a": 2}') == ([{"a": 1}, {"a": 2}], 1)
    records, bad = ex.parse_jsonl((DATA / "messy_orders.jsonl").read_text(encoding="utf-8"))
    assert [r["id"] for r in records] == ["B-2001", "B-2002", "B-2004"]
    assert bad == 2
