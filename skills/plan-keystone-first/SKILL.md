---
name: plan-keystone-first
description: "Plan discipline for risky multi-step work: survey work already in flight, name the single assumption that could kill the plan and probe it with a throwaway test before any scaffolding, then attach a tool-checkable done-when to every step with a stop-on-pass rule. Use before writing a plan whose success depends on an unverified assumption (an external API or data source, a tool or credential never exercised on this machine, an integration between components, a constraint at real scale), and whenever planning in a workspace with recent commits, running background tasks, or half-done branches."
---

# Plan the keystone first

A plan is only as good as its worst assumption and its blindest spot. The
default failure is to plan against an empty world (rebuilding what a
background agent shipped yesterday), order steps by convenience (easy
scaffolding first, the hard integration last), and write steps with no pass
condition, so nothing ever says stop. Plan the other way around: inventory
first, keystone probed first, every step gated.

## The failure shape

The generic shape, not a single incident: a six-step plan puts folder
structure, models, and CRUD at steps 1-5 and "wire to the external API" at
step 6. Step 6 reveals the API does not return the field the whole feature
needs. Steps 1-5 are now rework, and the diff also contains a parallel copy
of a module another agent finished yesterday. One curl at minute zero would
have killed the plan before it cost anything.

## Before writing the plan: rebuild the in-flight inventory

In any non-fresh workspace, run these BEFORE drafting a single step. After a
context compaction or restart, rebuild this from tools; never inherit a
remembered inventory (recovering the dead tasks themselves is
durable-background-work territory).

1. `git status` plus the last ~10 commits in every repo the task touches.
2. List running and recently finished background tasks and monitors.
3. Grep the ops/status docs for the task's keywords.
4. Glance at scratchpad dirs and worktrees for half-done artifacts in the area.

The plan's FIRST section is an in-flight table:

| Item | Observed state | Stance |
|---|---|---|
| (artifact, task, branch) | done / in progress / stale / conflicting | REUSE / EXTEND / SUPERSEDE / WAIT |

- REUSE: use as-is. EXTEND: finish it rather than starting fresh.
- SUPERSEDE: replace it, but snapshot it first (the snapshot-before-regenerate
  skill covers the procedure) and state the reason in the plan.
- WAIT: blocked on it; name what unblocks it.
- Conflicts get resolved here, in the plan, not at impact time.

Search-before-build corollary: before creating any new file, module, or
script, spend 2 minutes searching for an existing artifact that does 80% of
the job. Extending beats creating a parallel near-duplicate.

## Name and probe the keystone

Write down the answer to: which single step, if it fails, makes the rest of
this plan worthless? Common shapes: the API actually returns the needed data;
the tool runs on this machine; the credential exists; two components actually
integrate; a constraint (latency, memory, board space) holds at real scale.
A plan without a named keystone is not ready to execute.

Then probe it with the cheapest throwaway test: a 10-line script, one curl, a
one-file spike, a dry run on one record. Rules:

- Hard cap: no plan step other than the probe's own setup executes before the
  probe passes. If you notice scaffolding, models, or folder structure
  landing before probe output exists, stop and run the probe.
- Record the probe command and its actual output in the plan.
- If the probe fails: stop executing the remaining steps immediately and
  replan at the top level. No "meanwhile" work on other steps - they were
  justified by the assumption that just died.
- Multiple risky assumptions: list them, rank by (likelihood of failure x
  cost of discovering it late), probe in that order, and reorder the TODO
  list to match. A TODO list ordered by file layout or convenience is an
  anti-pattern to catch and fix.
- When delegating, the subagent brief names the keystone and the relevant
  slice of the in-flight inventory, and requires the probe result before the
  subagent proceeds past it.

## Every step gets a done-when

Write each step as: `Step: <action>. Done when: <command or observation>
yields <expected result>.`

- Checks must be tool-executable: "exit code 0", "endpoint returns 200 with
  field X", "grep finds 0 remaining matches". "Looks good" and "should work"
  are banned check language.
- Cannot state a check? Either split the step, or convert it into a discovery
  step whose output IS the next step's check.
- Every edit step carries the companion check: the diff contains the intended
  change and nothing else.
- Stop-on-pass: the moment a step's check passes, stop working on that step.
  Further improvement requires a NEW step with its own check and a one-line
  justification tied to the task goal. This is the gold-plating brake.
- A step whose check fails twice gets instrumented and structurally
  rethought: different approach, different tool, or park the step (for slow
  or hanging processes, the watch-the-live-log skill covers the
  instrumentation). Never a third attempt with tweaked parameters.
- The keystone, probe results, and per-step checks live in a durable plan
  artifact (a plan file or the task tracker's descriptions), never only in
  working memory, so they survive compaction and restarts.

## Signature smells

| Smell in a draft plan | Fix |
|---|---|
| Step 1 is "create folder structure" or "set up scaffolding" | Move the keystone probe to step 1 |
| The hard integration sits in the back half of the list | Reorder by failure-likelihood x cost-of-late-discovery |
| A step reads "improve X" or "polish Y" with no check | Attach a measurable done-when or delete the step |
| A new module's name mirrors an existing one | Run the 2-minute search; extend the existing artifact |
| Plan written from memory after a compaction or restart | Rebuild the inventory from git, task lists, and docs |
| "Meanwhile" progress continues after a probe failure | Halt everything; replan at the top level |
| A step keeps absorbing work after its check passed | Stop-on-pass; new work means a new step with a new check |
