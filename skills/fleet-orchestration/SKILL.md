---
name: fleet-orchestration
description: Patterns for running multiple background agents in parallel without collisions, lost work, or stalled handoffs. Use when delegating work to 2+ concurrent agents, when a background agent's work must continue after it stops, or when coordinating agents that edit files in the same repository.
---

# Fleet orchestration

Parallel agents multiply throughput only if the coordinator prevents three
failure classes: file collisions, detached work, and unverified claims.

## Disjoint ownership

Before launching, partition the file tree: each agent's prompt names the files
it OWNS and explicitly lists the files other agents own that it must not touch.
Two agents editing one file is not a merge problem, it is lost work. If a
shared file is unavoidable (a version constant, a cache-buster), assign it to
exactly one agent and have the other report the needed change instead.

## The detachment trap

A background agent that spawns its OWN background work (sub-agents, disowned
processes) and then stops loses that work: nothing re-invokes the agent when
the detached child finishes, and the child's results often evaporate. Rules:

- Background agents must do their work SYNCHRONOUSLY in their own session.
  Say so in the prompt: "no sub-agents, no background tasks."
- If an agent legitimately must wait on an external process, the COORDINATOR
  owns the wait: arm a monitor yourself, and resume the agent by message when
  the condition fires.
- When an agent reports "waiting for X to notify me," assume nothing will
  notify it. Check what actually happened, then resume it with explicit state.

## Monitors that do not lie

A watcher that greps only for the success marker is silent through crashes,
and silence looks identical to "still running." Cover every terminal state.
Also beware the false-idle race: a poll that checks "is the process running"
can fire during a gap BETWEEN sequential child processes - require the
condition to hold across two samples before acting on it.

## Resuming and redirecting

A stopped background agent can usually be resumed by sending it a message with
its id - it keeps its context. Use this to: deliver new information that
changes its plan mid-flight, correct a wrong assumption before it wastes hours,
and hand it the next phase after its blocking condition clears. Resuming beats
respawning: a fresh agent pays the full context-rebuilding cost.

## Claims flow upward only after verification

Never propagate an agent's completion report to the user or to another agent
without verifying the artifact yourself (see verify-dont-claim). In one real
case an agent reported both sweeps committed; the repository showed zero
commits - its sub-delegated children had silently died.

## Commit discipline

Each agent commits its own files with evidence in the message (measured
numbers, verification performed). The coordinator commits only coordinator
work. Interleaved commits from parallel agents are fine when ownership is
disjoint; a final coordinator pass verifies the tree is clean and nothing
landed in the wrong commit.
