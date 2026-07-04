#!/usr/bin/env python3
"""A/B eval runner: does loading the fable-skills change Opus agent behavior?

For each task x condition x trial:
  1. build a fresh git fixture via tasks/<task>/setup.sh
  2. skills_on only: copy the repo's 24 skills into <fixture>/.claude/skills/
  3. run headless claude (flags verified in MECHANICS.md), capture the full
     stream-json transcript and the final result object
  4. run the task's mechanical grader against the fixture's final state
  5. append one row to results/results.csv

Usage:
  python3 run_eval.py --tasks premise_trap,permission_stall --trials 2
  python3 run_eval.py --tasks all --trials 3 --timeout 900

Runs happen ONLY inside throwaway dirs under eval/sandboxes/.
"""
import argparse
import csv
import json
import os
import shutil
import subprocess
import sys
import time

EVAL_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(EVAL_DIR)
SKILLS_SRC = os.path.join(REPO_DIR, "skills")
TASKS_DIR = os.path.join(EVAL_DIR, "tasks")
SANDBOXES = os.path.join(EVAL_DIR, "sandboxes")
RESULTS_CSV = os.path.join(EVAL_DIR, "results", "results.csv")

ALL_TASKS = [
    "premise_trap",
    "false_done",
    "permission_stall",
    "clobber_trap",
    "scope_fidelity",
    "error_triage",
]
CONDITIONS = ["skills_on", "skills_off"]

CSV_FIELDS = [
    "timestamp",
    "task",
    "condition",
    "trial",
    "model",
    "score",
    "passed_checks",
    "failed_checks",
    "num_turns",
    "duration_ms",
    "total_cost_usd",
    "input_tokens",
    "output_tokens",
    "cache_creation_tokens",
    "cache_read_tokens",
    "is_error",
    "timed_out",
    "notes",
    "run_dir",
]


def build_fixture(task, run_dir):
    fixture = os.path.join(run_dir, "fixture")
    setup = os.path.join(TASKS_DIR, task, "setup.sh")
    subprocess.run(["bash", setup, fixture], check=True, capture_output=True)
    return fixture


def install_skills(fixture):
    dest = os.path.join(fixture, ".claude", "skills")
    shutil.copytree(SKILLS_SRC, dest)
    return len(os.listdir(dest))


def run_agent(fixture, prompt, model, timeout, budget):
    """Run headless claude in the fixture. Returns (result_obj, transcript_lines, timed_out)."""
    cmd = [
        "claude",
        "-p",
        prompt,
        "--model",
        model,
        "--output-format",
        "stream-json",
        "--verbose",
        "--no-session-persistence",
        "--strict-mcp-config",
        "--setting-sources",
        "project",
        "--permission-mode",
        "acceptEdits",
        "--allowedTools",
        "Bash,Edit,Write,Read,Glob,Grep",
        "--max-budget-usd",
        str(budget),
    ]
    env = dict(os.environ)
    env.pop("CLAUDECODE", None)  # the CLI refuses to nest otherwise
    try:
        proc = subprocess.run(
            cmd, cwd=fixture, env=env, capture_output=True, text=True, timeout=timeout
        )
        raw = proc.stdout
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        raw = exc.stdout or ""
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8", errors="replace")
        timed_out = True

    lines = [ln for ln in raw.splitlines() if ln.strip()]
    result_obj = None
    for ln in reversed(lines):
        try:
            obj = json.loads(ln)
        except ValueError:
            continue
        if obj.get("type") == "result":
            result_obj = obj
            break
    return result_obj, lines, timed_out


def grade(task, fixture, run_dir):
    grader = os.path.join(TASKS_DIR, task, "grade.py")
    final_msg = os.path.join(run_dir, "final_message.txt")
    transcript = os.path.join(run_dir, "transcript.jsonl")
    proc = subprocess.run(
        ["python3", grader, fixture, final_msg, transcript],
        capture_output=True,
        text=True,
        timeout=300,
    )
    if proc.returncode != 0:
        return {
            "task": task,
            "passed_checks": [],
            "failed_checks": [],
            "score": 0.0,
            "notes": "GRADER ERROR: {0}".format(proc.stderr.strip()[:300]),
        }
    return json.loads(proc.stdout.strip().splitlines()[-1])


def append_row(row):
    os.makedirs(os.path.dirname(RESULTS_CSV), exist_ok=True)
    new_file = not os.path.exists(RESULTS_CSV)
    with open(RESULTS_CSV, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerow(row)


def run_one(task, condition, trial, model, timeout, budget):
    stamp = time.strftime("%Y%m%d-%H%M%S")
    run_dir = os.path.join(
        SANDBOXES, "{0}__{1}__t{2}__{3}".format(task, condition, trial, stamp)
    )
    os.makedirs(run_dir, exist_ok=True)
    fixture = build_fixture(task, run_dir)

    if condition == "skills_on":
        n = install_skills(fixture)
        print("  installed {0} skills".format(n))

    with open(os.path.join(TASKS_DIR, task, "prompt.txt")) as f:
        prompt = f.read().strip()

    t0 = time.time()
    result_obj, lines, timed_out = run_agent(fixture, prompt, model, timeout, budget)
    wall = time.time() - t0

    with open(os.path.join(run_dir, "transcript.jsonl"), "w") as f:
        f.write("\n".join(lines) + "\n")
    final_message = (result_obj or {}).get("result", "") or ""
    with open(os.path.join(run_dir, "final_message.txt"), "w") as f:
        f.write(final_message)
    with open(os.path.join(run_dir, "output.json"), "w") as f:
        json.dump(result_obj or {"error": "no result object"}, f, indent=2)

    g = grade(task, fixture, run_dir)
    with open(os.path.join(run_dir, "grade.json"), "w") as f:
        json.dump(g, f, indent=2)

    usage = (result_obj or {}).get("usage", {})
    notes = g.get("notes", "")
    if timed_out:
        notes = "TIMED OUT after {0}s; ".format(int(wall)) + notes
    row = {
        "timestamp": stamp,
        "task": task,
        "condition": condition,
        "trial": trial,
        "model": model,
        "score": g.get("score", 0.0),
        "passed_checks": ";".join(g.get("passed_checks", [])),
        "failed_checks": ";".join(g.get("failed_checks", [])),
        "num_turns": (result_obj or {}).get("num_turns", ""),
        "duration_ms": (result_obj or {}).get("duration_ms", int(wall * 1000)),
        "total_cost_usd": (result_obj or {}).get("total_cost_usd", ""),
        "input_tokens": usage.get("input_tokens", ""),
        "output_tokens": usage.get("output_tokens", ""),
        "cache_creation_tokens": usage.get("cache_creation_input_tokens", ""),
        "cache_read_tokens": usage.get("cache_read_input_tokens", ""),
        "is_error": (result_obj or {}).get("is_error", True),
        "timed_out": timed_out,
        "notes": notes,
        "run_dir": os.path.relpath(run_dir, EVAL_DIR),
    }
    append_row(row)
    print(
        "  score={0} passed=[{1}] failed=[{2}]{3}".format(
            row["score"],
            row["passed_checks"],
            row["failed_checks"],
            " TIMED OUT" if timed_out else "",
        )
    )
    return row


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tasks", default="all", help="comma list or 'all'")
    ap.add_argument("--conditions", default="skills_on,skills_off")
    ap.add_argument("--trials", type=int, default=1)
    ap.add_argument("--model", default="claude-opus-4-8")
    ap.add_argument("--timeout", type=int, default=900, help="per-run wall clock (s)")
    ap.add_argument("--budget", type=float, default=5.0, help="per-run --max-budget-usd")
    args = ap.parse_args()

    tasks = ALL_TASKS if args.tasks == "all" else args.tasks.split(",")
    conditions = args.conditions.split(",")
    for t in tasks:
        if t not in ALL_TASKS:
            sys.exit("unknown task: {0}".format(t))
    for c in conditions:
        if c not in CONDITIONS:
            sys.exit("unknown condition: {0}".format(c))

    total = len(tasks) * len(conditions) * args.trials
    done = 0
    for trial in range(1, args.trials + 1):
        for task in tasks:
            for condition in conditions:
                done += 1
                print(
                    "[{0}/{1}] {2} x {3} trial {4}".format(
                        done, total, task, condition, trial
                    )
                )
                try:
                    run_one(
                        task, condition, trial, args.model, args.timeout, args.budget
                    )
                except Exception as exc:
                    print("  RUN FAILED: {0}".format(exc))
                    append_row(
                        {
                            "timestamp": time.strftime("%Y%m%d-%H%M%S"),
                            "task": task,
                            "condition": condition,
                            "trial": trial,
                            "model": args.model,
                            "score": "",
                            "passed_checks": "",
                            "failed_checks": "",
                            "num_turns": "",
                            "duration_ms": "",
                            "total_cost_usd": "",
                            "input_tokens": "",
                            "output_tokens": "",
                            "cache_creation_tokens": "",
                            "cache_read_tokens": "",
                            "is_error": True,
                            "timed_out": False,
                            "notes": "HARNESS ERROR: {0}".format(str(exc)[:300]),
                            "run_dir": "",
                        }
                    )
    print("done: {0} runs -> {1}".format(total, os.path.relpath(RESULTS_CSV, EVAL_DIR)))


if __name__ == "__main__":
    main()
