---
name: act-on-intent
description: Resolves underspecified or casually phrased requests by inferring the evident goal from repo context, proceeding on announced assumptions, expanding scope only within hard bounds, and never letting an off-hand remark override a locked decision. Use BEFORE asking any clarifying question or starting work on a request that omits details needed to proceed, names one instance of a defect that may have siblings, asks about a failure without explicitly requesting a fix ("why is X failing?"), or mixes directives with musings and side comments.
---

# Act on intent

A terse request is a pointer to a goal, not a full spec. The gap between the
literal words and the evident goal is yours to close from repo evidence, on
announced assumptions, inside hard bounds. Neither extreme is acceptable: a
clarifying question the repo could have answered, or a passing remark inflated
into a rewrite.

## The failure this prevents

Three siblings of one mistake. Asked to "fix the typo on line 3" of a file
with six typos, the agent fixes exactly one and ships a file that still reads
broken. Asked to add a config option, it stops to ask which naming style to
use when ten existing options in the same file already answer that. Told in
passing "that blue reads a bit dark," it changes the palette across fourteen
files, including artifacts documented as locked.

## Step 1: triage the message before anything enters the task list

Split every message into fragments and classify each one:

| Fragment type | Signal | Disposition |
|---|---|---|
| Directive | Imperative and scoped: "fix", "add", "export X to Y" | Enters the task list |
| Aside | Observation, vibe, musing: "huh, that's slow", "the blue reads dark" | Goes in a "Noted, not acted on" report section with a one-line proposed action, so a single word from the user promotes it |
| Question | "Why is X failing?", "Can you check Y?" | Diagnose always; also fix when the fix is reversible AND inside the named scope; otherwise report the answer plus a proposed fix |

Asides never become work by themselves. A question is a directive to
investigate, and usually to repair.

## Step 2: write the goal, then judge scope against it

Restate the request as a one-sentence outcome ("wants: the README free of
typos"), not the literal instruction ("fix line 3"). Every scope decision for
the rest of the task is judged against that sentence. If the literal ask
already fully satisfies the goal, do not expand at all.

## Step 3: infer before asking

Run this checklist BEFORE drafting any clarifying question, in order:

1. Root project instructions (CLAUDE.md or equivalent)
2. The target folder's own CLAUDE.md / SPEC / README
3. Memory files and standing notes
4. `git log` for how the same choice was made before
5. Conventions in neighboring code (how do the ten existing cases do it?)

When a source answers, proceed and cite it in the report. Ask only when the
genuine-fork test passes, ALL three required:

- (a) Not answerable after the checklist.
- (b) The branches diverge into irreversible or external actions, or more
  than ~30 minutes of throwaway work if guessed wrong.
- (c) The choice is visible outside the repo (a public API name, a price,
  copy real humans will read, an external message), so convention cannot
  arbitrate.

Otherwise pick the option that matches existing convention and keep moving.

## Step 4: announce every non-obvious choice

Every assumption goes in an ASSUMPTIONS block directly under the
delivered-vs-asked line: "Assumed X because Y (source: Z). Flip it with one
word." If you find yourself past ~5 load-bearing assumptions, the request was
a genuine fork wearing a casual tone; stop and ask before building further on
the stack.

## Step 5: sweep for siblings, inside the fence

When asked to fix one instance of a defect, search for the class: first the
named file, then the containing module. Fix all siblings inside the named
scope. Siblings OUTSIDE that scope get reported with exact locations, never
silently fixed. "You asked about one; there were six here and two more in the
adjacent module I did not touch."

## The hard bounds on expansion

Expansion may complete the stated goal. It may never:

- redesign or rewrite working code
- rename things
- add unrequested features
- regenerate or overwrite artifacts documented as locked or approved

"While I was at it" refactors are forbidden; log them as one-line suggestions.
One casual sentence never justifies multi-file edits, renames, brand changes,
or regenerating locked artifacts. With only an aside in hand, propose; do not
act.

**Locked-decision check.** Before acting on anything that touches a decision
documented as locked, diff the instruction against the lock. On conflict,
quote both verbatim and ask which wins. A casual remark never silently
overrides a lock, and recency never beats a standing rule. Locks live where
the snapshot-before-regenerate skill says to mark them: a commit, a LOCKED
note beside the file, or a protected-paths list.

## Report the delta, recover from wrong guesses

Open every report with a delivered-vs-asked line, then the ASSUMPTIONS block:
"You asked for the typo on line 3; the goal implied the file; I fixed all 6
and touched nothing else." This makes over-expansion and under-expansion
equally visible in one line.

The moment evidence contradicts a stated assumption, stop extending it,
update the ASSUMPTIONS block explicitly (old value, new value, what changed),
and rework only the portion that depended on the wrong guess.

## Anti-patterns

| Anti-pattern | Instead |
|---|---|
| Clarifying question answerable from step 3's checklist | Infer, cite the source, proceed |
| Fixing exactly the one named instance among many | Sibling sweep within the named scope |
| Palette/rename/refactor triggered by a musing | "Noted, not acted on" + one-line proposal |
| Silent assumptions discovered only when something breaks | ASSUMPTIONS block up front, before the work ships |
| Treating the newest casual remark as overriding a standing rule | Quote both, ask which wins |
