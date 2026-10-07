import sys
from pathlib import Path

LABS = Path(__file__).resolve().parent
for p in (LABS, LABS / "capstone1_claims"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
