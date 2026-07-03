---
name: diversify-or-park
description: "Debugging discipline that runs fix attempts as single-variable ledger experiments with pre-committed kill criteria: two strikes per hypothesis family, structurally different pivots instead of parameter tweaks, cheap discriminating tests before expensive fixes, and a parking protocol so one stuck item never ends the turn. Use the moment a first fix attempt fails and before launching the second, when the next attempt would differ from the last only in parameters, or when a fix under consideration is slow, destructive, or chosen while multiple causes still fit the evidence. Routine iteration where each run is fast and each change is driven by new output does not need this until the same error survives two informed fixes."
---

# Diversify or park

A first failed fix is normal. What separates a debugging session from a
debugging spiral is the move after: every attempt is either an experiment that
eliminates something, or noise that costs a retry cycle. Run attempts as
single-variable experiments with written predictions, kill a hypothesis family
after two misses, and park the item after three dead families instead of
letting it end the turn.

## The failure this prevents

Attempt one fails and the reflex takes over: bump the timeout 30 to 60 to 120
(three runs, one hypothesis, zero information), or shotgun-edit three files at
once so the outcome teaches nothing, or reach for the big familiar fix -
reinstall, rewrite from scratch - on a theory nothing has confirmed. Each move
burns a full retry cycle without narrowing the cause. The alternative costs
one written line and a 30-second test.

## The ledger

The moment a second attempt begins, open a debug ledger file in your
scratchpad. One row per attempt:

| # | Hypothesis | Exact change | Predicted outcome | Actual result |
|---|---|---|---|---|

- The prediction is written BEFORE the run. A run without a written
  prediction eliminates nothing but still consumes an attempt from the
  family budget; noise is not free, so never launch one.
- A missed prediction is data. Record what it eliminates before writing the
  next row.
- One variable per attempt. Revert every failed attempt (git stash, checkout,
  or explicit undo) before the next. Never stack failed fixes: three
  unexplained changes plus the original bug is strictly worse than the bug.

## The retry ladder

| Situation | Allowed next move |
|---|---|
| First failure, plausibly transient cause (network, rate limit, file lock, race) | ONE unchanged retry, maximum |
| Exact same error text after a changed attempt | Change approach FAMILY; a flag, timeout, or path change does not count |
| Two misses within one family ("it's a timeout", "it's the version") | Family is dead; a third parameter tweak is banned. Mandatory next move: gather evidence - add instrumentation, minimize the repro, or bisect |
| Three distinct families dead | Park it (protocol below) |

Changing family means a structurally different move: a different tool,
decomposing the operation into separately verifiable pieces, checking for a
missing dependency, or searching the exact error string.

## Cheap test before expensive fix

Before any fix that (a) takes over 5 minutes, (b) is destructive or hard to
reverse, or (c) was chosen while 2+ causes still fit the evidence:

1. Write the top 2-3 hypotheses. ALWAYS include the boring one - typo, wrong
   path, stale cache, wrong venv, wrong directory - and check it first.
2. For each, name the cheapest observation that discriminates it from the
   others.
3. Run the cheapest first. Prefer the test whose failure would KILL your
   favorite hypothesis, not the one that would flatter it.
4. If the test costs as much as the fix, it is not a test.

Bisection is the default discriminating test on any ordered space: `git
bisect` for "it worked before", halve the input for data-dependent failures,
disable half the config or pipeline for setup failures. State the expected
log2(N) step count before starting so you do not abandon it midway.

## Tripwires

Before starting any approach expected to cost more than 10 minutes or more
than one attempt, pre-commit in the plan file: a time-box, a max attempt
count (default 2 substantive attempts), and the specific evidence that would
prove the approach wrong. Sunk cost never justifies attempt N+1; only new
information does, and you must name that information in the ledger. A ledger
result that contradicts a plan assumption marks that assumption DEAD in the
plan file and forces re-derivation of the remaining steps before the next
row is written.

When a tripwire fires: STOP. Write a 3-line postmortem (what was assumed /
what was observed / why this approach cannot close the gap). Generate at least
2 structurally different alternatives before choosing one. Salvage
transferable artifacts (repro script, instrumentation, partial data) so the
pivot starts warm.

## Parking protocol

After 3 distinct families fail, write a failure record and move on:

- Record the goal, families tried, exact error text, best remaining
  hypothesis, and recommended next approach.
- Append it to a "do not retry" list that later sessions and subagents read
  before touching the item.
- Parked is a status, not a deletion. One stuck item never ends the turn while
  independent work remains.

## When the bug disappears

- Write the mechanism in one sentence. Check it explains ALL observed
  symptoms; an unexplained symptom means possibly masked, not fixed - say so
  in the report.
- Check cause vs symptom: did you fix what produced the error, or what
  displayed it?
- Grep for siblings of the same defect before closing; the pattern that
  produced one instance usually produced others.

## Boundary

Both this skill and watch-the-live-log fire once the same operation has been
retried with tweaked parameters. Split on output: a failure that RETURNS an
error or a wrong result runs this ladder; a process that is slow, hung, or
silent goes to watch-the-live-log first, because there instrumentation
replaces hypotheses entirely. The two-misses row above deliberately lands on
the same move as that skill: instrument before theory three.
