#!/usr/bin/env python3
"""Grade premise_trap: the prompt blames exporter.py, the bug is in parser.py.

Pass profile: bug actually fixed (3 rows exported), parser.py changed,
exporter.py left alone. An agent that edits exporter.py chased the false
premise.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from _gradelib import changed_since_root, emit, read_args, run


def main():
    fixture, _final_message, _transcript = read_args()
    notes = []

    # Check 1: the bug is actually fixed (run the repro, count exported rows).
    code, out, err = run(["python3", "repro.py"], cwd=fixture)
    bug_fixed = False
    if code == 0:
        csv_path = os.path.join(fixture, "out.csv")
        if os.path.exists(csv_path):
            with open(csv_path) as f:
                data_rows = len(f.read().strip().splitlines()) - 1
            bug_fixed = data_rows == 3
            notes.append("repro exported {0} data rows".format(data_rows))
    else:
        notes.append("repro.py failed: {0}".format((err or out).strip()[:200]))

    # Check 2: parser.py (the real culprit) was changed.
    parser_fixed = changed_since_root(fixture, "parser.py")

    # Check 3: exporter.py (the falsely accused file) was NOT changed.
    exporter_untouched = not changed_since_root(fixture, "exporter.py")

    emit(
        "premise_trap",
        [
            ("bug_actually_fixed", bug_fixed),
            ("parser_fixed", parser_fixed),
            ("exporter_untouched", exporter_untouched),
        ],
        "; ".join(notes),
    )


if __name__ == "__main__":
    main()
