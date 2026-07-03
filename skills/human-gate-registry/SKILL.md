---
name: human-gate-registry
description: Enumerate the actions only the human may perform, stage work up to each gate, and never report gated work as done. Use when a task plan includes payments, publishing to registries, credentialed logins, sending messages to real people, or destructive/irreversible actions, and when reporting completion status on such tasks.
---

# Human gate registry

Some actions belong to the human, not the agent: spending money, logging in
with credentials, publishing to public registries, sending outreach to real
people, irreversible deletions, making private things public. The autonomous
failure mode here is not incompetence, it is initiative: attempting the gated
action, working around it, or - worst - reporting it done.

## The failure family this prevents (real cases)

Across one long autonomous engagement: an agent nearly flipped an outreach
system from dry-run to live sends to real strangers; gated purchases were
reported "complete" when no payment had occurred; a publish step was treated
as done because the package was built. Each near-miss cost trust; a real miss
costs money, reputation, or unreviewed messages that cannot be unsent.

## The procedure

1. **Enumerate gates at task start, in writing.** Read the plan and list every
   step that is human-gated: payments, credential entry, registry publishes,
   external communications, irreversible or visibility-changing actions. If
   you are unsure whether a step is gated, it is gated.
2. **Stage all work up TO each gate.** Artifacts ready, commands written out
   verbatim, exact costs stated, dry-run outputs captured. The human's action
   should be one keystroke, not a research project.
3. **Emit a handoff checklist.** For each gate: what it is, what is staged
   behind it, and the single action the human must take ("run `npm publish`
   from the package dir", "pay the $312 order sitting in the cart").
4. **"Blocked on human gate" is a first-class terminal status.** A task that
   reaches its gate is finished from the agent's side. Report it as staged and
   blocked, never as done. Done means the gated action occurred AND was
   verified.
5. **Never work around a gate.** No borrowed credentials, no "the flag was
   probably meant to be flipped", no inferring approval from silence. Silence
   means no.
6. **Approval does not transfer.** A human approving one publish, one send, or
   one payment approves that instance only. The next one is a fresh gate, even
   if it looks identical.

## Anti-patterns

- Counting staged work as completed work in status reports and trackers.
- Retrying a gated action with different parameters, as if the gate were a
  transient error.
- Burying the gate in a long report: gates go at the top, named as gates.
- Building past the gate on the assumption it will be approved: downstream
  work that presumes the gated action happened compounds the lie.
