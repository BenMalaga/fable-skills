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
4. **When two heuristics disagree, read the ground truth.** Two different
   inference methods giving opposite answers means neither is trustworthy;
   go read the primary definition (the file format, the datasheet, the source).
5. **Check memory/docs for prior wars.** If the project has notes on this tool,
   read them BEFORE the second retry, not after the fifth. The battle has
   usually been fought before, and the notes contain the exact trap.
6. **After solving, write the postmortem into memory** with the false theories
   listed explicitly as false, so the next session does not re-walk them.

## Signature smells

- Same operation retried with tweaked parameters more than twice: stop, instrument.
- "It works for small inputs" without knowing which PHASE differs: instrument.
- A tool that succeeds interactively but fails headless: suspect exit/save
  paths and non-daemon threads, not the core operation.
- Process killed on timeout leaves no output: the output may only be written
  at graceful exit - the work may be succeeding and getting discarded.
