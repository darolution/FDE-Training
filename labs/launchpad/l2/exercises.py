"""Launchpad L2 exercises: values, variables, text and numbers.

How these work
--------------
Each exercise is a small *function*: a named box of code. You'll learn
functions properly in L3. For now you only need to know two things:

  * The names in brackets (like `name`) are the inputs you're given.
  * You replace the line `raise NotImplementedError(...)` with code that
    ends in `return <your answer>`.

Check your work any time:

    python labs/launchpad/check.py l2

Try each one yourself before looking at labs/launchpad/solutions/l2.py.
"""


def greeting(name):
    """Return a greeting for `name`.

    greeting("Ava")  ->  "Hello, Ava! Welcome to the course."
    Hint: an f-string, f"Hello, {name}! ..."
    """
    raise NotImplementedError("Exercise 1: write greeting()")


def minutes_to_hours(minutes):
    """Convert minutes to hours.

    minutes_to_hours(90)  ->  1.5
    minutes_to_hours(45)  ->  0.75
    """
    raise NotImplementedError("Exercise 2: write minutes_to_hours()")


def total_with_tax(price, tax_rate):
    """Add tax to a price and round to 2 decimal places (cents).

    total_with_tax(100, 0.13)    ->  113.0
    total_with_tax(19.99, 0.05)  ->  20.99
    Hint: round(number, 2)
    """
    raise NotImplementedError("Exercise 3: write total_with_tax()")


def initials(first_name, last_name):
    """Return capitalised initials with dots.

    initials("ava", "chen")  ->  "A.C."
    Hint: first_name[0] is the first letter; .upper() makes it a capital.
    """
    raise NotImplementedError("Exercise 4: write initials()")


def shout(text):
    """Return the text in capitals with an exclamation mark, without spaces at either end.

    shout("  order shipped ")  ->  "ORDER SHIPPED!"
    Hint: .strip() and .upper()
    """
    raise NotImplementedError("Exercise 5: write shout()")


def word_count(sentence):
    """Count the words in a sentence (words are separated by spaces).

    word_count("where is my order")  ->  4
    word_count("")                   ->  0
    Hint: .split() turns text into a list of words; len() counts them.
    """
    raise NotImplementedError("Exercise 6: write word_count()")


def receipt_line(item, quantity, unit_price):
    """Return one line of a receipt, with prices to 2 decimal places.

    receipt_line("Headlamp", 2, 39)  ->  "2 x Headlamp @ $39.00 = $78.00"
    Hint: inside an f-string, {value:.2f} shows a number with 2 decimals.
    """
    raise NotImplementedError("Exercise 7: write receipt_line()")


def is_long_message(text, limit):
    """Return True if the text has more than `limit` characters, otherwise False.

    is_long_message("hello", 3)  ->  True
    is_long_message("hi", 3)     ->  False
    Hint: len(text) gives the number of characters; > compares two numbers.
    """
    raise NotImplementedError("Exercise 8: write is_long_message()")
