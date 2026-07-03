---
name: durable-background-work
description: Make delegated background work survive host restarts, and recover correctly after one. Use when launching background agents or long-running tasks that could outlive the current process, when a session resumes after a crash or restart, or when a notification reports a background task died with its state lost.
---

# Durable background work

A running background agent is not a checkpoint. It is RAM. In one real case a
single host-process restart killed three parallel agents and a scheduled loop
at once: two agents had committed nothing, so hours of their work evaporated
completely, and the third left a half-built scaffold that a blind relaunch
would have duplicated or clobbered.

## Launch so a stranger can relaunch

- **Self-contained briefs.** Write each agent's prompt as if its replacement
  will run it with zero memory of your conversation - full state, exact paths,
  constraints, acceptance checks. Its replacement WILL have zero memory.
- **Keep your own durable copy of the brief.** The conversation that produced
  it may be summarized or truncated before the agent dies; if the brief lives
  only in chat history, the relaunch starts from guesswork.
- **Require checkpoint commits.** Instruct agents to commit each completed,
  verified unit of work with the evidence in the message. An agent that
  commits only at the end has an all-or-nothing failure mode; its death costs
  everything instead of one unit.

## Recovery protocol (after any restart or kill notification)

1. **Never relaunch blind.** For each dead task, audit the ARTIFACTS first:
   commits since dispatch, working-tree status, target-folder inventory,
   output files with sizes.
2. **Classify, then act.**
   - Landed: verify it (see verify-dont-claim), mark done, do not relaunch.
   - Partial: adjust the brief - state exactly what already exists so the
     relaunch builds on it instead of redoing or overwriting it.
   - Nothing: relaunch the original brief unchanged.
3. **Re-arm the timers.** Scheduled jobs, polling loops, and monitors die with
   the process too, silently. Nothing will fire on its own; re-create each one
   explicitly or its task simply never happens again.

## Rules of thumb

- "Launched" is not a state of progress. Only committed, verifiable artifacts
  count as progress.
- Uncommitted work is a bet that the process outlives the task. Long tasks
  lose that bet regularly.
- When the platform says "process exited, in-process state lost," believe the
  artifacts, not the agent's last optimistic status message.
