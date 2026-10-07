"""Reference solutions for Launchpad L3. Try the exercises yourself first!"""


def total(prices):
    running = 0
    for price in prices:
        running = running + price
    return running


def most_expensive(prices):
    if not prices:
        return None
    return max(prices)


def order_total(order):
    value = 0
    for item in order["items"]:
        value += item["qty"] * item["price"]
    return value


def priority_label(amount):
    if amount >= 500:
        return "high"
    elif amount >= 100:
        return "medium"
    else:
        return "low"


def only_status(orders, status):
    return [order for order in orders if order["status"] == status]


def count_by_status(orders):
    counts = {}
    for order in orders:
        status = order["status"]
        counts[status] = counts.get(status, 0) + 1
    return counts


def customers_in_country(orders, country):
    names = {order["customer"] for order in orders if order["country"] == country}
    return sorted(names)


def biggest_order(orders):
    if not orders:
        return None
    best = max(orders, key=order_total)
    return best["id"]
