"""The L8 project spec as tests. Run with:  python labs/launchpad/check.py l8"""

import json

import pytest

from launchpad._loader import DATA, load

pytestmark = pytest.mark.exercise
app = load("l8")
ORDERS_FILE = DATA / "orders.json"


def test_step1_load_orders():
    orders = app.load_orders(ORDERS_FILE)
    assert len(orders) == 20


def test_step1_missing_file_is_a_friendly_exit(tmp_path):
    with pytest.raises(SystemExit):
        app.load_orders(tmp_path / "nope.json")


def test_step2_order_total():
    assert app.order_total({"items": [{"qty": 2, "price": 39.0}, {"qty": 1, "price": 19.0}]}) == 97.0


def test_step3_filter_orders():
    orders = app.load_orders(ORDERS_FILE)
    assert len(app.filter_orders(orders)) == 20
    assert len(app.filter_orders(orders, status="delivered")) == 8
    assert len(app.filter_orders(orders, country="US")) == 9
    assert len(app.filter_orders(orders, status="cancelled", country="US")) == 2


def test_step4_summarize():
    s = app.summarize(app.load_orders(ORDERS_FILE))
    assert s == {
        "orders": 20,
        "revenue": 5861.0,
        "by_status": {"cancelled": 3, "processing": 4, "shipped": 5, "delivered": 8},
        "top_customer": "Gus Ito",
        "top_customer_value": 1629.0,
    }


def test_step4_summarize_empty():
    assert app.summarize([]) == {"orders": 0, "revenue": 0, "by_status": {}, "top_customer": None,
                                 "top_customer_value": 0}


def test_step5_format_report():
    s = app.summarize(app.filter_orders(app.load_orders(ORDERS_FILE), status="delivered"))
    assert app.format_report(s) == (
        "Orders: 8\nRevenue: $2,747.00\nBy status: delivered 8\nTop customer: Gus Ito ($775.00)"
    )
    empty = app.format_report(app.summarize([]))
    assert "By status: none" in empty and "Top customer: none" in empty


def test_step6_main_prints_report(capsys):
    assert app.main([str(ORDERS_FILE), "--country", "US"]) == 0
    out = capsys.readouterr().out
    assert "Orders: 9" in out and "Revenue: $3,146.00" in out


def test_step6_main_json(capsys):
    assert app.main([str(ORDERS_FILE), "--status", "cancelled", "--country", "US", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["orders"] == 2 and data["revenue"] == 1202.0
