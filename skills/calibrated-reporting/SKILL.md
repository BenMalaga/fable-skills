---
name: calibrated-reporting
description: Structure completion reports and rollups so the outcome and the worst true thing lead, every load-bearing claim carries its evidence grade, and every number carries provenance. Use BEFORE composing a report that covers multiple work items or relays any subagent's work, whenever anything failed, was skipped, or went untested, or when the reader will decide or spend money based on it. A single fully-verified task does not need the full structure: one outcome line plus its receipt is the whole report.
---

# Calibrated reporting

A report exists to change what the reader does next, not to narrate what you
did. The reader's first three seconds decide whether they see the failure or
build on top of it. Structure is mechanically self-auditable where "be honest"
is not: a fixed section order, a scoreboard that must sum, and wording locked
to evidence grade catch the drift that good intentions miss.

## The failure this prevents

A long session ends. The report opens "All major work complete!" and walks
chronologically through the day; the three failures surface in paragraph six;
a subagent's "all tests pass" is relayed in the reporter's own declarative
voice, laundering hearsay into fact. The reader ships on it. Every rule below
is a mechanical check against one of those moves.

## Line 1

State the resulting state plus the worst true thing: "4/5 boards routed;
board 2 still has 184 unconnected nets." Never activity narration ("I worked
on routing"). If nothing failed, say so plainly and keep the whole report
short; never pad good news to make it look proportional to the effort.

A single-item, fully-MEASURED task stops here: Line 1 plus its receipt is
the entire report. The section order and scoreboard below apply to
multi-item work and rollups.

## Fixed section order (chronological ordering is banned)

| Section | Contents |
|---|---|
| OUTCOME | 1-3 lines: resulting state + worst true thing |
| SCOREBOARD | the counts, see below |
| WHAT CHANGED | artifacts, absolute paths, measured numbers |
| NEEDS-YOU | only actions the reader alone can take |
| RISKS / UNKNOWNS | includes the "expected, unverified" block |
| APPENDIX | everything that fails the next-action test |

## The scoreboard must sum

"N attempted / M succeeded / K failed / J skipped / U untested", where
M + K + J + U = N. The unit is the discrete work item the task decomposed
into (a board, a file, a test target, a subagent assignment); name the unit
in the scoreboard line itself: "5 boards attempted / 3 routed / 1 failed /
0 skipped / 1 untested". If the categories do not sum, the report is not
done: go recount. UNTESTED is a first-class status. A change that was edited
but never run is untested; it is never folded into succeeded.

## Per-failure block (mandatory for every one of the K)

- What was attempted
- The exact trimmed error output
- Root-cause status: found / hypothesized / not investigated
- What was tried
- What was deliberately NOT tried

## Evidence grades lock the wording

| Grade | Meaning | Wording it permits |
|---|---|---|
| MEASURED | ran it this session, output in hand | plain declaratives |
| VERIFIED-ARTIFACT | file/commit/URL checked to exist | "the artifact exists at ..." |
| INFERRED | read the code, never ran it | "the code indicates", "I expect" |
| REPORTED | someone else's claim | name the source + "(unverified)" |
| ASSUMED | taken as true, never checked | its own flagged "assuming ..." line |

Relaying never upgrades a grade: a subagent's claim enters your report as
REPORTED unless you re-measured it yourself (see verify-dont-claim). REPORTED
covers claims too expensive to check this session, not cheap ones: a check
under a minute gets run and the grade upgraded. A rollup that is mostly
REPORTED lines means you stopped orchestrating and started stenographing.

## Banned verbs without a receipt

"works", "fixed", "done", "passes", "deployed", "live", "resolved": each
requires MEASURED grade plus a receipt, meaning the exact command run and its
trimmed output, adjacent to the claim or as a pointer into APPENDIX
("receipt: A2") when the output runs past two lines. Want the verb? Produce
the receipt or change the verb.

## Numbers and softeners

Every number carries its source: the command that produced it, the file path
it came from, or the explicit label "estimate". Softeners ("mostly working",
"minor issues", "should be fine") are banned unless immediately followed by
the enumerated list they summarize.

## Aggregation conservation

A rollup of subagent reports never contains fewer failures than the sum of
its inputs. Carry counts forward verbatim. If you cleared a reported failure,
name the re-verification receipt that cleared it.

## Quarantine predictions

Unmeasured claims about how the delivered work will behave ("should work",
"will pass", "likely fixed") go in an "expected, unverified" block inside
RISKS / UNKNOWNS, so a skimmer cannot mistake a forecast for a measurement.

## Next-action test, per sentence

Does this sentence change what the reader does next? If no: cut it or demote
it to APPENDIX. The top 5 lines must stand alone as a complete report.
Load-bearing statements are full sentences, not arrow-chain fragments.

## No-surprise rule

Any failure that moves a gate, a deadline, or a cost lands in the first three
lines AND in the relevant ops doc in the same session (see doc-truth-refresh),
never only in the chat message.

## Pre-send scan (the stopping condition for report-writing)

Scan the draft for banned verbs, unsourced numbers, and softeners; if the
report has a scoreboard, write the draft to a scratch file first so the scan
is a real grep, not a reread. Hits inside quoted output or in instructions
to the reader do not count; your own declarative claims always do. For each
real hit, attach a receipt or downgrade the wording. The report is done when
the scan is clean and the scoreboard sums, not when the prose feels finished.
