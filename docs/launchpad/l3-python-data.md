# L3 · Python 2: lists, loops, decisions and functions

**Goal:** work with collections of data, the way you'll handle customer orders, tickets and API responses all course.
**Time:** about 10 hours. This is the most important Launchpad week, so don't rush it.

## Lists

A **list** is an ordered collection in square brackets:

```python
prices = [249.0, 39.0, 19.0]
prices[0]          # 249.0   first item (positions start at 0)
prices[-1]         # 19.0    last item
len(prices)        # 3
prices.append(89.0)            # add to the end
prices                         # [249.0, 39.0, 19.0, 89.0]
max(prices), min(prices), sum(prices)
```

## Dictionaries

A **dictionary** maps **keys** to **values**, in curly brackets. Real-world records look like this:

```python
order = {"id": "A-1001", "customer": "Ava Chen", "status": "shipped", "total": 278.0}
order["customer"]            # "Ava Chen"
order["status"] = "delivered"   # change a value
order.get("discount", 0)     # 0: .get() gives a default if the key is missing
order.keys(), order.values()
```

Lists and dictionaries nest: an order can hold a list of item dictionaries. Open `labs/launchpad/data/orders.json` in VS Code to see 20 real-looking orders. That's the data you'll practise on.

## Loops

A `for` loop runs the same code for each item:

```python
for price in prices:
    print(price)
```

The **indented** lines (4 spaces) belong to the loop. Indentation isn't decoration in Python: it's how Python knows what's inside what.

A common pattern is to start a total and add to it:

```python
running = 0
for price in prices:
    running = running + price     # or: running += price
print(running)
```

Loop over orders and reach inside each one:

```python
for order in orders:
    print(order["id"], order["status"])
```

## Decisions

```python
if total >= 500:
    label = "high"
elif total >= 100:
    label = "medium"
else:
    label = "low"
```

Combine conditions with `and`, `or` and `not`: `if order["status"] == "shipped" and order["country"] == "CA":`

## Functions

A **function** is a named, reusable piece of code. It takes **parameters** (inputs) and **returns** a result:

```python
def order_value(quantity, unit_price):
    """Return the value of one order line."""
    return quantity * unit_price

order_value(2, 39.0)   # 78.0
```

- `def` starts the function; the indented block is its **body**.
- `return` hands back the result and ends the function.
- The text in triple quotes is a **docstring**: it explains what the function does.

Why bother? Write once, use everywhere, test separately, and give a name to an idea. Each exercise is a function so the checker can test it.

## Two handy shortcuts

**List comprehensions** build a list in one line:

```python
shipped = [o for o in orders if o["status"] == "shipped"]
names = [o["customer"] for o in orders]
```

**Sets** hold unique values: `set(["a", "b", "a"])` gives `{"a", "b"}`. `sorted(...)` returns a sorted list.

## Exercises

Open `labs/launchpad/l3/exercises.py`, read each docstring, and complete the eight functions. Several use the real `orders.json` data.

```bash
python labs/launchpad/check.py l3
```

| # | Exercise | Practises |
|---|---|---|
| 1 | `total` | `for` loops, running totals |
| 2 | `most_expensive` | empty lists, `max` |
| 3 | `order_total` | nested lists and dictionaries |
| 4 | `priority_label` | `if` / `elif` / `else` |
| 5 | `only_status` | filtering a list |
| 6 | `count_by_status` | building a dictionary of counts |
| 7 | `customers_in_country` | sets and sorting |
| 8 | `biggest_order` | calling your own function |

!!! tip "Try it in small pieces"
    Before writing a whole function, try parts of it interactively. Run `python`, paste a few orders from the file as a list, and experiment. You can also add a `print(...)` inside your function to see what's happening; remove it when done.

**Stretch.** Write `average_order_value(orders)` in the same file and test it yourself on `orders.json` (you'll need L4's file reading, or paste a few orders).

## Checkpoint

- [ ] I can create, read and change lists and dictionaries
- [ ] I can write a `for` loop with a running total, and filter with `if`
- [ ] I can write a function with parameters and a return value
- [ ] `python labs/launchpad/check.py l3` passes all 8 checks
