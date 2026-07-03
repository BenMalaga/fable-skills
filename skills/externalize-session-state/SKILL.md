---
name: externalize-session-state
description: Write decisions, measured facts, todos, and standing constraints to files the moment they are established, and rebuild working state from artifacts, never from a compaction summary or memory, before any further mutating action on resume. Use when starting a session expected to run long, span multiple work streams, or dispatch subagents; within such a session, the moment any decision, measurement, todo, or user correction occurs; and whenever you can no longer quote your own earlier command outputs verbatim.
---

# Externalize session state

Conversation memory is not durable state. Compaction silently replaces your
past with a paraphrase, and a paraphrase of a measurement is not a
measurement. Anything that exists only in the conversation is one compaction
away from gone; anything in a file survives.

## The failure this prevents

Two moments. Mid-session: a decision or number lands and stays in
conversation, where compaction later destroys or distorts it. Post-compaction:
the session resumes confidently from the summary, repeating steps already
completed, quoting paraphrased numbers as if freshly measured, and violating
standing rules stated in hour one (banned characters, frozen directories,
naming rules) that the summary dropped. In one real case a hard formatting ban
held for hours, then reappeared in every artifact written after compaction,
because the rule lived nowhere but the lost turns.

## First move

If the session is expected to exceed about an hour, span more than one work
stream, or dispatch subagents, create or open `LEDGER.md` and
`CONSTRAINTS.md` in a canonical spot: a repo `_ops/` dir, preferred, since it
survives session replacement; the scratchpad only if work cannot touch the
repo (scratchpads are compaction-safe but usually die with the session). If
either file already exists, read it fully before doing anything else. This
costs one minute and is the entire insurance premium.

## The ledger

Fixed sections, append-only, entries telegraphic (one line each). When a
section passes ~40 lines, move completed items to a dated ARCHIVE block.

| Section | Holds |
|---|---|
| NOW | The single action currently in progress |
| DECISIONS | Dated, with a one-line rationale |
| FACTS | Dated, with HOW it was measured (command or file) |
| TODOS | Open items; completed ones move to ARCHIVE |
| BLOCKED-ON | What is stuck and on whom/what |

**Write-immediately triggers.** Each is a write at that moment, never batched
to session end: a decision made; a measurement obtained; a nonobvious fact
discovered (paths, versions, flags, gotchas); the plan revised; a todo created
or completed; a blocker hit; a user correction or new standing rule stated.

**A todo that exists only in conversation does not exist.** The moment you
write "later", "next", or "TODO" in a reply, it enters the TODOS section in
the same turn. A harness todo tool counts only if its state provably survives
compaction; when unsure, mirror items into the ledger.

**Grep before rederiving.** Before recomputing any count, measurement, or
config fact, grep the ledger. Found, and nothing has modified the measured
artifact since the fact's date (check mtime or git log on the artifact):
reuse it. Otherwise: re-measure and append the new dated value beside the
old one.

## The constraints card

Every hard rule from project instructions, memory files, and user messages,
numbered, verbatim where possible, max ~12 items. Tag each one GREPPABLE
(banned characters, banned terms, forbidden paths - things a command can
check) or JUDGMENT (things only you can check). Soft preferences stay out: a
card too long to actually re-read protects nothing. Mid-session corrections
are constraints until explicitly revoked; append them to the card before
resuming the task.

**Re-read checkpoints.** Mechanical, no reasoning about whether you still
remember it: before writing any user-facing artifact; before any commit;
immediately after suspected compaction; before every subagent dispatch (paste
the card verbatim into the brief - the subagent has none of your context); and
at every phase boundary.

**Enforcement pass.** Before shipping text or code, actually run the
GREPPABLE checks on the artifacts produced, and name which checks ran in your
report. If one violation is found: fix it, then grep every other artifact from
this session for the same violation. Drift never leaks into just one output.

## Compaction detection

Any of these means your context has been rewritten:

| Trigger | Meaning |
|---|---|
| A summary block stands in for earlier turns | Compaction happened |
| Asked to restate an earlier measured number, you would be paraphrasing rather than quoting a line you can point to | Details are already lost |
| A memory contradicts what a file says | The file wins; your memory is a paraphrase |

**Hard stopping rule.** After any trigger, no mutating action - no edits,
commits, deploys, subagent dispatches, or status claims - until reconciliation
completes.

## Reconciliation checklist

1. Read the ledger and the constraints card, fully.
2. `git status` and `git log` back to the last commit you can verify.
3. List files modified in the session window (`git diff --stat` or `find -newer`).
4. Verify each in-flight task's claimed state with one direct command. The
   verify-dont-claim skill's artifact-class table is the instrument catalog;
   post-compaction, treat your own memory as just another agent's unverified
   claim.
5. Classify every remembered item: VERIFIED (an artifact confirms it), STALE
   (an artifact contradicts it; the artifact wins, always), or UNKNOWN (no
   artifact; treat as not done).

Then write a dated RESUMED entry recording the reconciled state. That entry,
not the summary, is the baseline for everything that follows. Remembered
numbers may only be restated after re-measuring or locating the exact source
line. Before redoing a step, check whether its output artifact already exists;
before skipping a step marked done, check the same thing.

## Keep it proportionate

A short gap with a clean ledger costs two file reads and one git command, not
a full audit. Escalate to per-item verification only for state you are about
to build on. Boundaries: doc-truth-refresh governs polished status docs; this
ledger is private working state, and the two must not be conflated.
durable-background-work governs background agents surviving restarts; this
skill covers the orchestrator's own thread surviving its own memory loss.
