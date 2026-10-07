"""Loads either your exercise file or the reference solution, so the same tests check both.

You don't need to read this file. The course's automatic build sets
FDE_LAUNCHPAD_TARGET=solutions to prove the reference solutions pass the tests;
on your computer the tests check *your* files.
"""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
from types import ModuleType

HERE = Path(__file__).resolve().parent

EXERCISES = {
    "l2": "l2/exercises.py",
    "l3": "l3/exercises.py",
    "l4": "l4/exercises.py",
    "l6": "l6/exercises.py",
    "l7": "l7/discount.py",
    "l8": "l8/orders_report.py",
}
SOLUTIONS = {
    "l2": "solutions/l2.py",
    "l3": "solutions/l3.py",
    "l4": "solutions/l4.py",
    "l6": "solutions/l6.py",
    "l7": "solutions/l7_discount.py",
    "l8": "solutions/l8_orders_report.py",
}
DATA = HERE / "data"


def using_solutions() -> bool:
    return os.environ.get("FDE_LAUNCHPAD_TARGET") == "solutions"


def load(week: str) -> ModuleType:
    rel = (SOLUTIONS if using_solutions() else EXERCISES)[week]
    path = HERE / rel
    name = f"launchpad_{week}_{'solution' if using_solutions() else 'exercise'}"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module
