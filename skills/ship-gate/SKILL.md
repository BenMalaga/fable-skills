---
name: ship-gate
description: Gate every multi-deliverable handoff behind a clause-by-clause reconciliation of the original request (done, blocked, or descoped, never silently dropped) plus a consume-the-artifact-as-its-recipient pass with mechanical placeholder scans. Use when finishing a task with 3+ deliverables or embedded constraints, before the final handoff message on such a task, or when a long session tempts wrapping up with items still open.
---

# Ship gate

Finishing is a checked state, not a feeling. The gate has two halves: prove the
SET of claims is complete (every clause of the original request accounted for),
and prove the artifact is consumable (opened, run, or read exactly as its
recipient will consume it). verify-dont-claim checks that each individual claim
is true; this skill checks that nothing was silently dropped and nothing ships
unopened.

## The failure shape this prevents

A five-part request comes back with the headline ask polished and delivered.
The "also update the changelog" clause is gone. The "without changing the
public API" constraint was never checked against the diff. The report still
contains [PROJECT_NAME]. The generated export was never opened; its second
section is empty. The final message says "Done." Each omission is small; the
recipient discovers them one at a time, and trust in every future "done" is
gone.

## Part 1: the ledger (written BEFORE the work)

First move on any task with 3+ deliverables: open a ledger, one line per
deliverable, before starting the work. Use the harness task/todo tool when the
work is single-session; write the ledger to a file when the work spans
sessions, subagents, or compaction risk, because the file, not the
conversation, survives compaction. Include the implied deliverables:

- tests for changed behavior
- regeneration of downstream artifacts (exports, builds, renders)
- doc, status, and tracker updates the change makes stale
- version, cache, or manifest bumps
- the commit or handoff itself, if one was requested

Newly discovered subtasks are appended the moment they are found, never held in
working memory. A mid-task amendment from the user ("also make sure X") is a
permanent ledger clause: it does not expire when the immediate fix lands.

## Part 2: the gate (AFTER the work, BEFORE the final message)

Never skipped, including under time pressure. Session length and context
pressure are not stopping conditions: checkpoint the ledger and keep working.

1. **Re-open the original request verbatim.** Scroll back to the actual message
   or re-read the brief file. Never gate against your memory of what was asked;
   memory is where secondary clauses go to die.
2. **Decompose into atomic clauses.** Explicit deliverables, embedded negative
   constraints ("without X", "keep Y", "preserve Z"), format and length asks,
   quality bars, and standing rules that apply to this output type.
3. **Assign every clause exactly one state.** There is no fourth state and no
   silent omission. Do not deliver while any clause is unaccounted for.

| State | Requires |
|---|---|
| DONE | A pointer to a specific artifact: file path, diff hunk, or command output |
| BLOCKED | The named external blocker plus exactly what is needed to unblock |
| DESCOPED | A one-line reason, surfaced in the final message, never buried |

4. **Check negative constraints against the diff, not against your intent.**
   "Don't change X" is verified by reading the actual hunks touching X, or
   confirming none do, not by recalling that you meant to leave it alone.
   Negative constraints are the most commonly dropped clause type.
5. **Count, then speak.** "Done", "complete", and "finished" may appear only
   when open ledger items equal zero. Otherwise report counts: "9 done, 2
   blocked (named), 1 descoped (reason)". Never "mostly done".

One pass: the gate takes minutes and catches shipping defects. Fix what it
finds, do not re-litigate design decisions, then ship.

## Part 3: consume the artifact as its recipient

Rule zero: a deliverable you have not consumed in its final form is a draft.
For build, deploy, web, and process claims, use verify-dont-claim's
artifact-class table; the rows below cover only the recipient-posture
consumption it does not.

| Artifact | Consume it by |
|---|---|
| Script / pipeline | Run it top to bottom in a clean shell and read the output |
| CLI tool | Invoke it with the exact command the README documents |
| Document / report | Read it start to finish as a first-time reader |

**Mechanical scan pack** (run these exact greps on the deliverable, do not
eyeball):

- Work markers: `grep -rnE 'TODO|FIXME|XXX|TBD'`
- Unresolved templates: `grep -rnE '\[[A-Z][A-Z0-9_]+\]|\{\{[^}]+\}\}|\$[A-Z_]{3,}'`
- Filler: `grep -rniE 'lorem'`
- Project-forbidden patterns: one grep per banned character or phrase from the
  standing rules for this output type, run verbatim

**Internal-consistency pass:** the title matches the content; the stated
section list matches the actual sections; grep each headline number and
confirm all occurrences agree; every referenced local path passes `ls`; every
URL is fetched, or explicitly labeled unverified in the handoff.

**Recipient-context strip:** remove or rewrite anything that assumes context
the recipient lacks: "as discussed above" in a standalone doc, machine-local
absolute paths, scratchpad links, references to agents or tools the recipient
never saw.

**Long-report rule:** front-load a 3-5 line summary with the key finding and
the recommended action. If the summary cannot be written in five lines, the
work is not finished; go back. Deviations (blocked and descoped clauses with
reasons) go in the first lines, never in a footnote.

## Anti-patterns

| Smell | What it actually means |
|---|---|
| Gating from memory of the request | The dropped clause is invisible by construction |
| "The generator ran clean" | Nobody opened the output |
| "Done (see caveats below)" | The deviations are buried; move them to line one |
| Wrapping up because the session is long | The ledger has open items; checkpoint and continue |
| "I was careful not to touch X" | Intent, not evidence; read the diff |
