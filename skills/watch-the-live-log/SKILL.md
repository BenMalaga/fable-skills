---
name: watch-the-live-log
description: Debugging discipline for long-running or hanging processes. Use when a process seems slow, stuck, or times out repeatedly; when you are about to form a theory about WHY something is slow; or when you have already retried the same operation twice with different parameters.
---

# Watch the live log

If a process "takes forever," you do not have a performance problem - you have
an observability problem. Fix the observability first. Theories formed without
watching the process's own output are usually wrong, and each wrong theory
costs a full retry cycle.

## The failure this prevents (real case)

An autorouter "timed out" at 40 minutes across a dozen runs. Four successive
theories (pass budget too high, CPU contention, dirty input state, edge
clearance violations) each triggered fixes and 40-minute retries. When someone
finally ran the tool with its stdout visible, the log showed the entire job
completing in 39 SECONDS - followed by an internal thread hang that prevented
the result from ever being written. Hours of retries, and the answer was in
the first minute of the first log.

## The discipline

1. **Instrument before theorizing.** Run the tool directly with stdout/stderr
   to a file you can tail. If a wrapper captures the output, bypass the wrapper
   for one diagnostic run.
2. **CPU% and elapsed time are not evidence.** 100% CPU can be a busy-loop
   doing nothing; 0% CPU can be a completed job waiting on a broken join.
   Only the process's own output tells you which phase it is in.
3. **One cheap kill-experiment per theory.** Before a fix that costs a long
   retry, design a test that falsifies the theory in under 5 minutes (e.g.
   delete the suspect element from a COPY of the input and run briefly).
4. **Check project notes before the second retry, and record false theories
   after.** If the project has notes on this tool, read them before retry two,
   not after retry five. After solving, write the false theories down
   explicitly as false (see skill-distiller) so the next session does not
   re-walk them.

## Signature smells

| Smell | Response |
|---|---|
| Same operation retried with tweaked parameters more than twice | Stop, instrument |
| "Works for small inputs" without knowing which phase differs | Instrument before scaling theories |
| Succeeds interactively, fails headless | Suspect exit/save paths and non-daemon threads, not the core operation |
| Killed-on-timeout run leaves no output | Output may only be written at graceful exit; the work may be succeeding and getting discarded |
