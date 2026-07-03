---
name: doc-truth-refresh
description: Keep status documents, dashboards, and READMEs synced to measured reality instead of aspirational or stale claims. Use when updating any ops doc, status tracker, or README; when a doc's claims are older than the work they describe; or after any milestone that changes project state.
---

# Doc truth refresh

Status docs rot in a specific direction: toward optimism. "Fab-ready" written
three weeks ago outlives three redesigns. The fix is a measurement discipline,
not a writing style.

## Rules

1. **Never write a status you did not measure this session.** Before writing
   "routed", "deployed", "passing", run the instrument that proves it and put
   the MEASURED value in the doc ("0 unconnected, fresh-load verified
   2026-07-03"), not the adjective.
2. **Date every volatile claim.** A number without a date becomes a lie
   silently. "184 unconnected (measured 2026-07-02)" degrades gracefully;
   "184 unconnected" degrades into misinformation.
3. **Single-source counts.** Any number that appears in more than one doc
   (module counts, price, project totals) needs one canonical home; every
   other appearance should be traceable to it. When you change the canonical
   value, grep for the old value across every doc surface - including the
   ones you forgot exist (marketing packs, competition submissions, app
   registries, comments in generators).
4. **Honest blockers over polite vagueness.** "Blocked: needs founder's
   Stripe keys" is actionable; "in progress" is not. A status doc's job is to
   make the next action obvious to a cold reader.
5. **Claims-vs-artifacts audit direction.** When doc and artifact disagree,
   the artifact wins, always - then ask WHY the doc drifted and fix the
   process (usually: a human-memory update step that should be a generated
   value).
6. **Distinguish "done" from "done and verified."** A doc may only use
   completion language for verified items; everything else is "built,
   unverified" or "claimed by agent X, not yet checked."

## The refresh procedure

1. List the doc's factual claims (counts, states, dates, gates).
2. For each: measure the current truth with a real tool.
3. Update, date, and where the drift was embarrassing, add the measurement
   COMMAND next to the claim so the next updater can re-run it.
4. Commit with the measurements in the message - the commit log becomes the
   audit trail.
