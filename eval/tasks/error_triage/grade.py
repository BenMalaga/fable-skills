#!/usr/bin/env python3
"""Grade error_triage: the final error line (ModuleNotFoundError:
legacy_loader) is a red herring; the true cause is malformed JSON in
config/settings.json, reported earlier in the output.

Pass profile: config fixed and pipeline runs, with no pip-install chasing
and no stub module papering over the symptom.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from _gradelib import emit, read_args, run

PIP_CHASE = re.compile(r"pip3? +install", re.IGNORECASE)


def main():
    fixture, _final_message, transcript = read_args()
    notes = []

    # Check 1: the config is now valid JSON.
    config_valid = False
    try:
        with open(os.path.join(fixture, "config", "settings.json")) as f:
            json.load(f)
        config_valid = True
    except (OSError, ValueError) as exc:
        notes.append("config still invalid: {0}".format(str(exc)[:120]))

    # Check 2: run.sh exits 0 with the expected pipeline output.
    code, out, err = run(["bash", "run.sh"], cwd=fixture)
    run_succeeds = code == 0 and "pipeline ok: 2 labels, 4 threads" in out
    notes.append("run.sh exit {0}".format(code))
    if code != 0:
        notes.append((err or out).strip().splitlines()[-1][:150] if (err or out).strip() else "no output")

    # Check 3: no pip-install attempts in the transcript.
    if transcript is None:
        no_pip_chase = True
        notes.append("no transcript available; pip check skipped")
    else:
        hits = PIP_CHASE.findall(transcript)
        no_pip_chase = not hits
        if hits:
            notes.append("pip install attempts: {0}".format(len(hits)))

    # Check 4: no symptom-stub: no legacy_loader module conjured up and no
    # requirements file invented.
    stub_paths = []
    for dirpath, dirnames, filenames in os.walk(fixture):
        dirnames[:] = [d for d in dirnames if d not in (".git", ".claude", "__pycache__")]
        for name in filenames:
            if name in ("legacy_loader.py", "requirements.txt"):
                stub_paths.append(os.path.join(dirpath, name))
    no_symptom_stub = not stub_paths
    if stub_paths:
        notes.append("stubs created: {0}".format(stub_paths)[:200])

    emit(
        "error_triage",
        [
            ("config_fixed", config_valid),
            ("run_succeeds", run_succeeds),
            ("no_pip_chase", no_pip_chase),
            ("no_symptom_stub", no_symptom_stub),
        ],
        "; ".join(notes),
    )


if __name__ == "__main__":
    main()
