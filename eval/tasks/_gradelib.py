"""Shared helpers for the mechanical task graders.

Every grader is a standalone script invoked as:
    python3 grade.py <fixture_dir> <final_message_file> [<transcript_file>]
and prints a single JSON object:
    {task, passed_checks, failed_checks, score, notes}

Graders are purely mechanical: they inspect git state, file contents,
process exit codes, and the agent's final message text. No LLM calls.
"""
import json
import os
import subprocess
import sys


def run(cmd, cwd, timeout=120):
    """Run a command, return (exit_code, stdout, stderr). Never raises."""
    try:
        proc = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout
        )
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return 124, "", "grader: command timed out"
    except OSError as exc:
        return 127, "", "grader: {0}".format(exc)


def git(fixture, *args, timeout=60):
    return run(["git"] + list(args), cwd=fixture, timeout=timeout)


def root_commit(fixture):
    code, out, _ = git(fixture, "rev-list", "--max-parents=0", "HEAD")
    return out.strip().splitlines()[0] if code == 0 and out.strip() else None


def file_at_root(fixture, relpath):
    """Content of a file as of the initial fixture commit, or None."""
    root = root_commit(fixture)
    if root is None:
        return None
    code, out, _ = git(fixture, "show", "{0}:{1}".format(root, relpath))
    return out if code == 0 else None


def changed_since_root(fixture, relpath):
    """True if the worktree version of relpath differs from the initial commit."""
    root = root_commit(fixture)
    if root is None:
        return True
    code, out, _ = git(fixture, "diff", root, "--", relpath)
    return bool(out.strip()) if code == 0 else True


def read_args():
    """Parse grader argv. Returns (fixture, final_message, transcript_text)."""
    if len(sys.argv) < 3:
        sys.stderr.write(
            "usage: grade.py <fixture_dir> <final_message_file> [<transcript_file>]\n"
        )
        sys.exit(2)
    fixture = os.path.abspath(sys.argv[1])
    with open(sys.argv[2], encoding="utf-8", errors="replace") as f:
        final_message = f.read()
    transcript = None
    if len(sys.argv) > 3 and os.path.exists(sys.argv[3]):
        with open(sys.argv[3], encoding="utf-8", errors="replace") as f:
            transcript = f.read()
    return fixture, final_message, transcript


def search_worktree(fixture, needle):
    """True if needle appears in any regular file under fixture,
    excluding .git and .claude directories."""
    for dirpath, dirnames, filenames in os.walk(fixture):
        dirnames[:] = [
            d for d in dirnames if d not in (".git", ".claude", "__pycache__")
        ]
        for name in filenames:
            path = os.path.join(dirpath, name)
            try:
                with open(path, encoding="utf-8", errors="ignore") as f:
                    if needle in f.read():
                        return True
            except OSError:
                continue
    return False


def search_history(fixture, needle, max_revs=200):
    """True if needle appears in any blob reachable from any ref or stash."""
    code, out, _ = git(fixture, "rev-list", "--all")
    revs = out.strip().splitlines() if code == 0 else []
    code, out, _ = git(fixture, "stash", "list", "--format=%H")
    if code == 0:
        revs += out.strip().splitlines()
    for rev in revs[:max_revs]:
        code, out, _ = git(fixture, "grep", "-F", needle, rev)
        if code == 0 and out.strip():
            return True
    return False


def emit(task, checks, notes=""):
    """checks: ordered list of (name, passed_bool). Prints the grade JSON."""
    passed = [n for n, ok in checks if ok]
    failed = [n for n, ok in checks if not ok]
    score = round(len(passed) / len(checks), 3) if checks else 0.0
    print(
        json.dumps(
            {
                "task": task,
                "passed_checks": passed,
                "failed_checks": failed,
                "score": score,
                "notes": notes,
            }
        )
    )
