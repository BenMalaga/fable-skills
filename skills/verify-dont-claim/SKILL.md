---
name: verify-dont-claim
description: Before reporting any work as done (yours or a subagent's), verify it with your own tools against the real artifact. Use whenever accepting a completion report from a subagent, before telling the user something is fixed/deployed/routed/built, and before making a decision based on another agent's findings.
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
| File changed/committed | `git log -1` + `git diff --quiet HEAD -- <path>`; read the actual hunk |
| Build passes | Run the build yourself; read the exit code, not the summary |
| Web UI works | Load it fresh (cleared storage), read the DOM/console, screenshot; a synthetic probe that returns all-false while the screenshot shows content means YOUR PROBE is broken - reconcile before concluding |
| Binary/geometry artifact | Hash it (md5) against the expected source of truth; compare counts (faces, rows, bytes) against the committed version |
| Long process finished | Check the OUTPUT artifact exists, not that the process exited; exit 0 with no output file is a failure |
| Locked/protected files untouched | MD5 every one against git HEAD after ANY operation that could touch them, every time, even when "obviously" safe |
| Deployed | Fetch the live URL and compare content hash to local; a passing build does not mean the deploy served it (prebuilt-output dirs can silently override builds) |
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
unverified overwrite. The check is never the expensive part.
