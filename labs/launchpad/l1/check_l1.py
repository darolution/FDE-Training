"""Launchpad L1 - check your terminal treasure hunt.

    python labs/launchpad/l1/check_l1.py
"""

from pathlib import Path

HERE = Path(__file__).resolve().parent
ok = True


def read_text_any(path: Path) -> str:
    """Read text saved by any terminal (Windows PowerShell 5 writes UTF-16 with `>`)."""
    raw = path.read_bytes()
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw.decode("utf-16", errors="ignore")
    return raw.decode("utf-8-sig", errors="ignore")


answers = HERE / "answers.txt"
if not answers.exists():
    print("[ ] answers.txt not found in labs/launchpad/l1/ - create it with the secret phrase")
    ok = False
elif "FORWARD-DEPLOYED-ENGINEER" not in read_text_any(answers).upper():
    print("[ ] answers.txt is there, but the phrase isn't right yet. Three parts, joined with dashes, in order")
    ok = False
else:
    print("[x] Secret phrase found")

note = HERE / "my-notes" / "first-note.txt"
if note.exists() and read_text_any(note).strip():
    print("[x] my-notes/first-note.txt exists and has something in it")
else:
    print("[ ] Create a folder my-notes inside labs/launchpad/l1, and a file first-note.txt in it with one line of text")
    ok = False

print("\nL1 complete. You can find your way around a computer from the terminal!" if ok else "\nNot done yet - keep going.")
