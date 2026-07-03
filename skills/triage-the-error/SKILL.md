---
name: triage-the-error
description: Extract the complete failure record and search project memory for prior encounters before forming any theory, anchoring every hypothesis to a quoted error line. Use when a command, build, test, script, or deploy fails with an error message or stack trace whose cause you cannot immediately quote from the output, before proposing a cause, before editing code in response to a failure, and before accepting a subagent's paraphrase of an error.
---

# Triage the error

An error message is evidence, not a prompt to start typing. The expensive
failure mode is the ten seconds after a command fails: reading only the last
line, pattern-matching the exception type, and editing code based on a guess -
or re-deriving from scratch a landmine the project already documented. Both are
prevented by the same two mechanical moves: capture everything, then search
before you theorize.

## The failure this prevents (real case)

A build was "fixed" three times by patching the last error in the output; the
first error, 400 lines up, was a missing generated file that caused all the
rest. Separately, sessions repeatedly re-fought a tool failure that a project
note written weeks earlier had already solved in one line: a 30-second grep
would have found it. (The hang variant of that incident belongs to
watch-the-live-log; the search discipline below applies either way.)

## Step 0: capture the complete record

- Redirect the failing command's FULL stdout+stderr to a scratch file
  (`cmd > "$SCRATCH/err.log" 2>&1`), re-running once if the original output
  was truncated by the tool harness or scrollback. Triage from the file,
  never from memory of what scrolled past.
- Never triage a subagent's paraphrase. "It failed with an import error" is
  not an error record. Demand the raw text or reproduce it yourself.
- Note the exit code. Exit 0 with error text, or nonzero exit with clean
  output, is itself a finding.

## Step 1: search for prior encounters (budget: at most 6 search commands)

**Fast path:** if the failure is fresh fallout from an edit you made this
session AND you can already pass the Step 3 gate (quote the exact line that
implicates your change), skip the search and go straight to Step 3. The
search order below is for failures whose cause you cannot yet quote.

Otherwise, before writing ANY hypothesis, run this search order. Stop at the
first hit or when the budget (6 search commands total across the four rows)
is spent - do not loop on search.

| Order | Where | How |
|---|---|---|
| 1 | Auto-memory files + every CLAUDE.md from repo root down to the failing component | grep for the error's distinctive tokens |
| 2 | docs/, ops trackers, HANDOFF / postmortem / agent-report directories | same grep |
| 3 | Git history | `git log --all --grep "<2-3 keywords>"` plus `git log --oneline -- <failing file>` |
| 4 | Filesystem near the component | look for `fix_*` / `workaround_*` scripts; their existence is evidence of a prior fight, read them |

**Query construction:** grep the CONSTANT parts of the error - identifiers,
error codes, function names, tool + subsystem names. Never the variable parts:
paths, PIDs, addresses, timestamps, line numbers.

**On a hit:** apply the documented resolution FIRST and verify it still
applies before inventing anything new. If the note turns out stale, update
that same note with the date and why it no longer works - do not leave a trap
for the next session.

**On no hit:** the budget is spent, you proceed to normal triage. Six search
commands are cheap; re-fighting a documented bug costs hours.

## Step 2: triage the FIRST error, not the last

1. **Find the first error chronologically.** Search the capture file top-down
   for the earliest failure; later errors are usually cascade fallout from
   it. Open the deepest frame in code you control and read it before stating
   any cause. Fixing the last error in a cascade is a banned move.
2. **Check the secondary channels every time:** "caused by" chains, exit
   codes, warnings in the 10 lines BEFORE the first error, and log lines
   sharing its timestamp. The real cause often prints as a warning.

## Step 3: the hypothesis gate

Before proposing a cause or touching code, write one sentence stating the
cause AND quote the exact error text (with file:line) that implicates it.

- No quotable line that implicates your cause = you have a guess, not a
  hypothesis. Gather evidence instead of editing: a verbose/debug flag, one
  added print at the suspect site, one inspection command.
- Fixing based on the exception TYPE alone ("that error name usually means
  install the missing package") is a banned move. The type narrows the search;
  the quoted line closes it.

## Step 4: reproduce, then fix

Find the minimal deterministic command that triggers the error and record it
in your notes before changing anything. That exact command is the mandatory
post-fix verification - run it and read its output yourself (see
verify-dont-claim). Re-running the original command "to see if it happens
again" is allowed exactly once, with output captured; more than once without
new instrumentation is thrashing.

## Write-back on close

Any bug that consumed more than 30 minutes, crossed a session boundary, or
involved a version/platform quirk gets ONE grep-able line at resolution,
placed where Step 1's search order would find it (memory file, component
CLAUDE.md, or ops doc): the verbatim error string, the root cause in one
clause, the exact fix command, and the date. Skill-worthy lessons get flagged
for skill-distiller, not expanded inline.

## Boundaries

| Situation | Hand off to |
|---|---|
| Process is slow or hung with NO error output | watch-the-live-log |
| Two or more fix attempts have already failed | stop and instrument (watch-the-live-log covers the retried-twice rule) |
| Confirming the fix actually worked | verify-dont-claim |
