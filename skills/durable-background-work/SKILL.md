---
name: durable-background-work
description: Make delegated background work survive host restarts, and recover correctly after one. Use when launching background agents or long-running tasks that could outlive the current process, when a session resumes after a crash or restart, or when a notification reports a background task died with its state lost.
---

# Durable background work

A running background agent is not a checkpoint. It is RAM. In one real case a
single host-process restart killed three parallel agents and a scheduled loop
at once: two agents had committed nothing, so hours of their work evaporated
completely, and the third left a half-built scaffold that a blind relaunch
would have duplicated or clobbered. (For collision and detachment failures
while the host is alive, see fleet-orchestration.)

## Launch so a stranger can relaunch

- **Write the brief for the replacement, not the agent.** The prompt must let
  a fresh process with zero memory of your conversation execute it: full
  state, exact paths, acceptance checks. Its replacement WILL have zero
  memory.
- **Keep your own durable copy of the brief.** The conversation that produced
  it may be summarized or truncated before the agent dies; if the brief lives
  only in chat history, the relaunch starts from guesswork. Write the brief to
  a file on disk (a briefs/ dir, the task folder, or a scratchpad file) at
  dispatch time, not after trouble starts.
- **Require checkpoint commits.** Instruct agents to commit each completed,
  verified unit of work with the evidence in the message. An agent that
  commits only at the end has an all-or-nothing failure mode; its death costs
  everything instead of one unit.

## Recovery protocol (after any restart or kill notification)

1. **Never relaunch blind.** For each dead task, audit the ARTIFACTS first:
   commits since dispatch, working-tree status, target-folder inventory,
   output files with sizes.
2. **Classify, then act.**

   | Artifact audit shows | Action |
   |---|---|
   | Landed | Verify it with your own tools (or the verify-dont-claim skill from this repo, if installed), mark done, do not relaunch |
   | Partial | Adjust the brief: state exactly what already exists so the relaunch builds on it instead of redoing or overwriting it |
   | Nothing | Relaunch the original brief unchanged |

3. **Re-arm process-owned timers.** In-process scheduled jobs, polling loops,
   and monitors die with the host process, silently; OS or platform schedulers
   (cron, CI schedules) usually survive it. Audit which timers were owned by
   the dead process, re-create only those, and verify the survivors are still
   armed - re-creating a timer that survived makes it fire twice.

## Rules of thumb

- "Launched" is not a state of progress. Only committed, verifiable artifacts
  count as progress.
- Uncommitted work is a bet that the process outlives the task. Long tasks
  lose that bet regularly.
- When the platform says "process exited, in-process state lost," believe the
  artifacts, not the agent's last optimistic status message.
