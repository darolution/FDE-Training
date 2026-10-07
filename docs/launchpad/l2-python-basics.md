# L2 · Python 1: values and variables

**Goal:** write and run Python scripts that work with text and numbers.
**Time:** about 8 hours.

Open the course folder in VS Code, open its terminal, and activate the environment (see [L1](l1-terminal.md#get-the-course-files)).

## Two ways to run Python

**1. Interactively.** Type `python` and press Enter. The prompt changes to `>>>`, and Python answers each line straight away:

```python
>>> 2 + 3
5
>>> "outdoor" + " gear"
'outdoor gear'
>>> exit()
```

Great for trying things out.

**2. As a script.** Save code in a `.py` file and run it with `python path/to/file.py`. Scripts are how real programs work. Try the one waiting for you:

```bash
python labs/launchpad/l2/hello.py
```

Answer its questions, then open `labs/launchpad/l2/hello.py` in VS Code and read it. Change the message, save (Ctrl+S / ⌘S), and run it again.

## Values and types

Every value in Python has a **type**:

| Type | Examples | Used for |
|---|---|---|
| `int` (integer) | `3`, `-12`, `2026` | Whole numbers |
| `float` | `39.99`, `0.13`, `1.5` | Numbers with decimals |
| `str` (string) | `"Ava"`, `'order shipped'` | Text, inside quotes |
| `bool` (Boolean) | `True`, `False` | Yes/no answers |

Check any value's type with `type(39.99)`.

## Variables

A **variable** is a name for a value. `=` means "store the value on the right under the name on the left".

```python
price = 39.0
quantity = 2
total = price * quantity
print(total)        # 78.0
```

- Names use lowercase letters, digits and underscores: `unit_price`, `order_count`. They can't start with a digit.
- Choose names that say what something *is*. `t` is a puzzle for the next reader; `total` isn't.
- Lines starting with `#` are **comments**: notes for humans, ignored by Python.

## Numbers

```python
10 + 3     # 13   add
10 - 3     # 7    subtract
10 * 3     # 30   multiply
10 / 4     # 2.5  divide (always gives a float)
10 // 4    # 2    whole-number division
10 % 4     # 2    remainder
2 ** 3     # 8    power
round(2.678, 2)   # 2.68
```

## Text (strings)

```python
name = "  ava chen "
name.strip()          # "ava chen"    remove spaces at both ends
name.strip().title()  # "Ava Chen"
"shipped".upper()     # "SHIPPED"
len("hello")          # 5            number of characters
"where is my order".split()   # ["where", "is", "my", "order"]
name.strip()[0]       # "a"          first character (counting starts at 0!)
```

**f-strings** put values inside text. Put an `f` before the quotes and the value in `{}`:

```python
item = "Headlamp"
price = 39
print(f"{item} costs ${price:.2f}")   # Headlamp costs $39.00
```

`:.2f` means "show as a number with 2 decimal places".

## Input and output

```python
name = input("Your name? ")          # always returns text (a str)
hours = float(input("Hours a week? "))   # convert text to a number
print("Hi", name)
```

`int("3")` and `float("3.5")` turn text into numbers; `str(3)` turns a number into text.

## Comparisons give Booleans

```python
5 > 3           # True
len("hi") > 3   # False
"a" == "a"      # True    == compares; = stores
```

## Exercises

Open `labs/launchpad/l2/exercises.py`. It has eight small exercises written as **functions**. You'll learn functions properly in L3; for now, replace each `raise NotImplementedError(...)` line with code that ends in `return <your answer>`. For example, a finished exercise looks like:

```python
def double(number):
    return number * 2
```

Check your work as often as you like:

```bash
python labs/launchpad/check.py l2
```

??? success "What the checker shows"
    Before you start, all 8 fail with `NotImplementedError`. That's expected. As you finish each exercise, its check passes:
    ```text
    3 of 8 checks pass for L2. Read the first failure above, fix that exercise, and run this again.
    ```
    and finally `All 8 checks pass for L2. Well done!`

??? failure "Reading a failed check"
    A line like `AssertionError: assert '2 x Headlamp @ $39 = $78' == '2 x Headlamp @ $39.00 = $78.00'` shows **what your code returned** (left) and **what was expected** (right). Compare them character by character: here, the decimals are missing.

| # | Exercise | Practises |
|---|---|---|
| 1 | `greeting` | f-strings |
| 2 | `minutes_to_hours` | division |
| 3 | `total_with_tax` | arithmetic, `round` |
| 4 | `initials` | indexing, `.upper()` |
| 5 | `shout` | string methods |
| 6 | `word_count` | `.split()`, `len` |
| 7 | `receipt_line` | number formatting |
| 8 | `is_long_message` | comparisons, Booleans |

**Stretch.** Write a script `labs/launchpad/l2/tip.py` that asks for a bill amount and a tip percentage, then prints the tip and the total, both to 2 decimals.

## Checkpoint

- [ ] I can run Python interactively and as a script
- [ ] I know the four basic types and can convert between text and numbers
- [ ] I can format numbers in f-strings
- [ ] `python labs/launchpad/check.py l2` passes all 8 checks
