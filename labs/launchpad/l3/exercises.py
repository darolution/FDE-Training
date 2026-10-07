"""Launchpad L3 exercises: lists, dictionaries, loops, decisions and functions.

The data looks like the online-store orders you'll use all through the course.
An order is a dictionary, for example:

    {"id": "A-1001", "customer": "Ava Chen", "country": "CA", "status": "shipped",
     "items": [{"sku": "TENT-2P", "name": "2-person tent", "qty": 1, "price": 249.0}]}

Check your work:   python labs/launchpad/check.py l3
"""


def total(prices):
    """Add up a list of prices with a for loop (don't use sum() for this one).

    total([10.0, 5.5, 4.5])  ->  20.0
    total([])                ->  0
    """
    raise NotImplementedError("Exercise 1: write total()")


def most_expensive(prices):
    """Return the highest price in the list, or None if the list is empty.

    most_expensive([19.0, 249.0, 39.0])  ->  249.0
    most_expensive([])                   ->  None
    """
    raise NotImplementedError("Exercise 2: write most_expensive()")


def order_total(order):
    """Return the order's value: quantity x price for each item, added up.

    {"items": [{"qty": 2, "price": 39.0}, {"qty": 1, "price": 19.0}]}  ->  97.0
    """
    raise NotImplementedError("Exercise 3: write order_total()")


def priority_label(amount):
    """Label an order by value: 500 or more is "high", 100 or more is "medium", anything else "low".

    priority_label(650)  ->  "high"
    priority_label(100)  ->  "medium"
    priority_label(99)   ->  "low"
    Hint: if / elif / else
    """
    raise NotImplementedError("Exercise 4: write priority_label()")


def only_status(orders, status):
    """Return a new list with just the orders whose "status" equals `status`, in the same order."""
    raise NotImplementedError("Exercise 5: write only_status()")


def count_by_status(orders):
    """Count orders per status and return a dictionary.

    [{"status": "shipped"}, {"status": "delivered"}, {"status": "shipped"}]
        ->  {"shipped": 2, "delivered": 1}
    """
    raise NotImplementedError("Exercise 6: write count_by_status()")


def customers_in_country(orders, country):
    """Return the names of customers in `country`, each name once, sorted A-Z.

    Hint: a set removes duplicates; sorted() returns a sorted list.
    """
    raise NotImplementedError("Exercise 7: write customers_in_country()")


def biggest_order(orders):
    """Return the id of the order with the highest order_total(), or None if there are no orders.

    Reuse your order_total() function: calling your own functions is the point of writing them.
    """
    raise NotImplementedError("Exercise 8: write biggest_order()")
