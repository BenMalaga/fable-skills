---
name: verify-dont-claim
description: Verify claims against the real artifact before repeating them. Use when accepting a completion report from a subagent or background process, before reporting any state you did not directly observe this session (deployed, built, migrated, data changed), and before making a decision based on another agent's findings.
---

# Verify, don't claim

A completion report is a claim, not a fact. Between the claim and the truth sit:
stale caches, detached processes, silent failures, optimistic summarization, and
work that happened on the wrong copy of a file. Verify with YOUR tools before
the claim leaves your mouth.

## The rule

Never report state you did not measure this session. "The agent says X" is a
different sentence from "X". If you must relay an unverified claim, label it as
a claim.

## Verification by artifact class

| Claimed | Verify with |
|---|---|
| File changed/committed | `git log -1 -- <path>` (must show the claimed commit) + `git status --porcelain -- <path>` (must be empty) + `git show HEAD:<path>` to read the actual committed hunk. `git diff --quiet HEAD` passes for untracked files - it cannot prove a commit exists |
| Build passes | Run the build yourself; read the exit code, not the summary |
| Web UI works | Load it fresh (cleared storage), read the DOM/console, screenshot; if probe and screenshot disagree, see below |
| Binary/geometry artifact | Hash it against the expected source of truth; compare counts (faces, rows, bytes) against the committed version |
| Long process finished | Check the OUTPUT artifact exists, not that the process exited; exit 0 with no output file is a failure |
| Locked/protected files untouched | Hash the output of `git show HEAD:<path>` (`md5` on macOS, `md5sum` on Linux) and compare to the working file's hash, after ANY operation that could touch them, even when "obviously" safe |
| Deployed | Fetch the live URL and confirm the specific change is present (a marker string or version stamp you added); compare content hashes only when the pipeline serves files byte-identical. A passing build does not mean the deploy served it (prebuilt-output dirs can silently override builds) |
| Counts/positions/measurements | Re-measure from the primary artifact (board file, database, DOM), never from a doc or a previous report |

## When two sources disagree

When your verification contradicts the claim, the claim is wrong until proven
otherwise - but ALSO check your own probe. In one real case a DOM probe
reported a page empty while the screenshot showed content: the probe had
attached to a dead browser context. Reconcile the instruments before ruling.

## The economics

Verification is almost always under 60 seconds. An unverified false "done"
costs hours: the user builds on it, downstream agents build on it, and the
eventual unwind is public. One project logged a full workday lost to a single
unverified overwrite (the snapshot-before-regenerate skill in this collection
encodes the preventive side of that incident). The check is never the
expensive part.
