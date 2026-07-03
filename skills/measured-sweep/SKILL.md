---
name: measured-sweep
description: Run a read-only, multi-dimension consistency audit where every finding carries measured evidence. Use when asked to "review everything", audit a codebase/artifact set for drift, or verify consistency across files that are supposed to agree (docs vs code, models vs sources, exports vs inputs).
---

# The measured sweep

An audit whose findings are opinions produces argument; an audit whose findings
are measurements produces fixes. This pattern makes every finding carry its own
proof.

## Structure

1. **Partition into dimensions** - independent slices (per-subsystem, per-file-
   class, per-claim-type) that different agents can sweep in parallel without
   overlapping. Assign every file class to exactly one sweeper; a finding that
   straddles two dimensions gets dropped by both unless ownership is explicit.
2. **Read-only, hard rule.** The sweep MEASURES; it never fixes, regenerates,
   or "cleans up while it's in there." Fixes come after synthesis, prioritized.
   State this in every sweep prompt: no writes, no generator runs.
3. **Evidence-required schema.** Every finding must include: severity, the
   exact file/location, the MEASURED numbers that prove it (positions, hashes,
   line numbers, counts - captured with real tools, not read from docs), and a
   concrete fix. A finding without numbers is deleted, not downgraded.
4. **Known-issues list.** Feed each sweeper the already-known findings so they
   do not re-report them. Re-reported knowns bury the new signal.
5. **Passes are summarized, not itemized.** "What passed" goes in a status
   paragraph; findings are only for failures. An audit that lists 200 passing
   checks hides its 12 real problems.
6. **Completeness critic.** After the dimensions return, one agent asks "what
   did this sweep structurally miss?" and RUNS the two cheapest missed checks
   itself. The critic regularly finds the highest-severity item of the whole
   exercise (in one real run: an ops doc that contradicted the manufacturing
   premise, and 37 marketing files with a stale product lineup).

## Anti-patterns

- Findings quoting documentation as evidence. Docs are subjects of the audit,
  never sources of truth for it.
- Severity inflation: reserve the top severity for findings that physically
  break the deliverable.
- Fixing during the sweep: a sweeper that edits invalidates its siblings'
  measurements mid-flight.
- Trusting one measurement style: verify the semantic behind the number too
  (an anchor point may be pad-1, not center; a count may include headers or
  labels; conventions like axis direction and units can flip at tool
  boundaries).
- Acting on a finding without re-deriving it from primary sources: one real
  sweep mis-called a 16mm "offset" that was actually an anchor-convention
  misread, and the "fix" made the artifact worse.

## After the sweep

Synthesize into a ranked action doc, fix in severity order, and re-measure each
fix with the same instrument that found it. The finding's own evidence line
doubles as its acceptance test.
