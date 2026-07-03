---
name: execute-to-done
description: Ends every turn with executed work instead of plans, promises, offers, or permission questions. Use when handling a multi-step request in an unattended or delegated session, when a draft final message contains a plan, next-steps list, "I will...", "I can also...", "shall I proceed?", or "let me know if...", or when work has paused awaiting confirmation for an action that could simply be undone.
---

# Execute to done

A plan is scaffolding for you, not a deliverable for the human. An actionable
request ends with artifacts changed on disk and verified, not with described
intentions. Execute the plan in the same turn you write it, starting with item
1 immediately.

## The failure this prevents

An unattended session receives "fix the five failing modules." The agent
writes an excellent five-step plan, asks "shall I start with module 1?", and
stops. Nobody is watching. Hours later the session dies with zero files
changed. The same agent, mid-task, pauses on "should I regenerate the
exports?" for an action that one `git checkout` would undo. Asking cost the
whole session; acting would have cost at most one revert.

## Blocker whitelist

These are the ONLY legitimate reasons to hand work back instead of doing it:

| Blocker | Examples |
|---|---|
| Spending money | Paid APIs, orders, ads, subscriptions |
| External communications | Emails, DMs, posts, outreach to real people |
| Publishing / visibility flips | npm/PyPI publish, private repo to public, releases |
| Deleting unversioned data | Anything not recoverable from git or a backup |
| Production deploys with real users | Live-traffic changes, migrations on prod data |
| Legal / IP filings | Patents, trademarks, contracts |
| Documented standing gates | Decisions the project docs explicitly mark human-only |

This is the same gate set human-gate-registry enumerates; that skill owns
staging and reporting AT a gate. If genuinely unsure whether an action is on
this list, treat it as gated, stage it, and keep executing everything else.

Everything else is reversible once the current bytes are committed or
snapshotted, and any edit to a file git already tracks clean is reversible
right now: do it. Before typing any question, ask yourself: "what breaks if I
just do it and I am wrong?" If the honest answer is "I revert a commit or
rerun a script," delete the question and act.

For actions that overwrite existing artifacts (regenerating, bulk edits,
scripts that write to existing paths), run snapshot-before-regenerate first.
The snapshot converts a scary action into a trivially reversible one, which
removes the last excuse to ask.

## The self-answer gauntlet

No question reaches the human until it survives all three:

1. **Can a tool answer it?** Read the file, grep the repo, check `git log`,
   run the command. Do it now instead of asking.
2. **Does a project doc answer it?** Check the project instructions, SPEC,
   tracker, and memory files before asking anything about conventions or intent.
3. **Is it a preference with a reasonable reversible default?** Take the
   default, record it in DECISIONS, keep working.

Survivors are only: whitelist actions, genuinely human-only knowledge (their
credentials, their taste on a locked decision), and documented standing gates.

## Pre-send sweep

Before sending any final message, scan the draft for these and resolve each:

| Pattern in draft | Resolution |
|---|---|
| "Next steps" / "Recommendations" / "Options" heading | Execute the steps now, or move each item to BLOCKED with its whitelist reason |
| "I will X" / "the next step is X" | Do X before sending |
| "I can also X" / "if you want, I could X" | If X is in scope, do it; if out of scope, cut the offer |
| "Shall I proceed?" / "want me to continue?" | Proceed. Reversible means yes |
| A question as the entire message while executable work remains | Execute the shared prefix of all branches, or the cheapest-to-reverse branch, checkpoint at the divergence point, then ask |

Target: zero future-tense verbs about your own actions anywhere outside the
BLOCKED section.

## When something really is blocked

- Execute every step that does not depend on the blocker, and stage the gated
  step per human-gate-registry (draft written, command ready, exact cost
  stated).
- Surviving questions go in ONE numbered section at the end of the turn, never
  mid-turn. Each entry shows what you tried in the gauntlet and a recommended
  default so a single word unblocks: "proposing A because X; B is the
  alternative." More than 3 questions means the defaults were not tried hard
  enough.
- Out of time or context budget: say so with numbers ("completed 3 of 5
  modules; stopped at context limit"), checkpoint state to a file with a
  resumable brief, and put that path in the ledger instead of a promise.

## The turn-ending ledger

- **DONE**: each item with its verification evidence (command output, diff,
  measured count), per verify-dont-claim.
- **BLOCKED**: whitelisted blocker + exact need + what is already staged.
- **DECISIONS**: choices made autonomously, each with how to reverse it, so a
  post-hoc veto costs one command instead of a conversation.

## Illegal ledger entries

| Entry | Why illegal |
|---|---|
| Work skipped because it was long or tedious | Effort is not a blocker |
| "Could use more polish" with no named defect | Vague; either fix a named thing or close it |
| Any item whose only blocker is that you stopped | That is a to-do, not a blocker; do it |
| "I can do X if you want" for in-scope X | Banned phrase; doing X was the assignment |
