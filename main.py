#!/usr/bin/env python3
"""Make the AI Judge Laugh — one office-life line, written to /output/entry.txt.

The line won an internal tournament of seven candidates, scored 1-5 on
specificity / surprise / freshness. The winner scored 5/4/5: a folder
naming habit every office worker recognises, with the punch landing on
the nested folder name itself. Nothing here needs the network or any
third-party package; the standard library is all it uses.
"""

import argparse
import sys
from pathlib import Path

ENTRY = (
    "Our team's shared drive has a folder called FINAL_v2_REAL, "
    "and inside it, a folder called FINAL_v2_REAL_USE_THIS_ONE."
)

GATE_MIN = 1
GATE_MAX = 200

# Tournament record (specificity / surprise / freshness, each 1-5):
# 1. IT reset my password to 'Password123!' + 40-page policy — 5/4/4 = 13
# 2. Office plant has a name, a schedule, more job security — 4/4/4 = 12
# 3. Finance rejected my $4 coffee, approved a $40,000 synergy workshop — 5/5/4 = 14
# 4. Calendar blocked focus time, manager booked it as a quick sync — 5/4/4 = 13
# 5. FINAL_v2_REAL folder, inside it FINAL_v2_REAL_USE_THIS_ONE — 5/4/5 = 14 WINNER
# 6. HR condolence email for the dead plant, replaced it with plastic — 4/4/5 = 13
# 7. Intern fixed the bug, we promoted the bug to a feature — 5/4/4 = 13
# Tie at 14 between 3 and 5; 5 won: the nested folder name is the fresher
# surprise and reads cleanly aloud in one breath.


def check_entry(text: str) -> list[str]:
    """Return a list of gate failures; empty means the line is valid."""
    problems: list[str] = []
    if not text.strip():
        problems.append("entry is only white space")
    if len(text) < GATE_MIN:
        problems.append(f"entry is {len(text)} chars, below the {GATE_MIN} minimum")
    if len(text) > GATE_MAX:
        problems.append(f"entry is {len(text)} chars, above the {GATE_MAX} maximum")
    if "\n" in text.strip():
        problems.append("entry must be a single line")
    return problems


def write_entry(destination: Path) -> int:
    """Write the line to destination, creating parent dirs, return bytes."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    data = (ENTRY + "\n").encode("utf-8")
    destination.write_bytes(data)
    return len(data)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write the judge-laugh entry line.")
    parser.add_argument(
        "--output",
        default="/output/entry.txt",
        help="where to write the entry (default: /output/entry.txt)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate the line against the gate and print its size",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="write to a temp file and verify the bytes read back",
    )
    args = parser.parse_args(argv)

    problems = check_entry(ENTRY)
    if args.check:
        print(f"entry: {ENTRY}")
        print(f"chars: {len(ENTRY)}  bytes: {len(ENTRY.encode('utf-8'))}")
        print("tournament winner: FINAL_v2_REAL nesting, 5/4/5 (7 candidates)")
        if problems:
            for problem in problems:
                print(f"FAIL: {problem}")
            return 1
        print("check: ok")
        return 0

    if args.self_test:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "entry.txt"
            written = write_entry(target)
            back = target.read_bytes()
            if back != (ENTRY + "\n").encode("utf-8"):
                print("FAIL: self-test round-trip mismatch", file=sys.stderr)
                return 1
            print(f"self-test: ok ({written} bytes round-trip identical)")
            return 0

    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1

    written = write_entry(Path(args.output))
    print(f"wrote {written} bytes to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
