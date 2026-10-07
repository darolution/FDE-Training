"""Reference solutions for Launchpad L2. Try the exercises yourself first!"""


def greeting(name):
    return f"Hello, {name}! Welcome to the course."


def minutes_to_hours(minutes):
    return minutes / 60


def total_with_tax(price, tax_rate):
    return round(price * (1 + tax_rate), 2)


def initials(first_name, last_name):
    return f"{first_name[0].upper()}.{last_name[0].upper()}."


def shout(text):
    return text.strip().upper() + "!"


def word_count(sentence):
    return len(sentence.split())


def receipt_line(item, quantity, unit_price):
    return f"{quantity} x {item} @ ${unit_price:.2f} = ${quantity * unit_price:.2f}"


def is_long_message(text, limit):
    return len(text) > limit
