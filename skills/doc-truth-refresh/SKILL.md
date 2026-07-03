---
name: doc-truth-refresh
description: Keep status documents, dashboards, and READMEs synced to measured reality instead of aspirational or stale claims. Use when about to write or update a status claim (a count, a done/deployed/routed/passing state, a blocker, a gate) in any ops doc, tracker, dashboard, or README, or when a doc's status claims predate the most recent work on what they describe.
---

# Doc truth refresh

Status docs rot in a specific direction: toward optimism. "Fab-ready" written
three weeks ago outlives three redesigns. The fix is a measurement discipline,
not a writing style. Anchor incident: a launch tracker still said a patent was
unfiled three weeks after the filing was done; downstream docs inherited the
stale claim because each copied the tracker instead of the filing receipt.

## Rules

1. **Never write a status you did not measure this session.** Before writing
   "routed", "deployed", "passing", run the instrument that proves it and put
   the MEASURED value in the doc ("0 unconnected, re-measured from a fresh
   file load, 2026-07-03"), not the adjective. The verify-dont-claim skill's
   verification-by-artifact-class table is the instrument catalog.
2. **Date every volatile claim.** A number without a date becomes a lie
   silently. "184 unconnected (measured 2026-07-02)" degrades gracefully;
   "184 unconnected" degrades into misinformation.
3. **Single-source counts.** Any number that appears in more than one doc
   (module counts, price, project totals) needs one canonical home; every
   other appearance should be traceable to it. When you change the canonical
   value, grep for the old value across every doc surface - including the
   ones you forgot exist (marketing packs, competition submissions, app
   registries, comments in generators).
4. **Honest blockers over polite vagueness.** State blockers as owner +
   action ("Blocked: needs founder's Stripe keys"), never "in progress". A
   status doc's job is to make the next action obvious to a cold reader.
5. **Claims-vs-artifacts audit direction.** When doc and artifact disagree,
   fix the doc from the artifact, then fix the PROCESS that let it drift -
   usually a human-memory update step that should be a generated value.
6. **Distinguish "done" from "done and verified."** A doc may only use
   completion language for verified items (see verify-dont-claim's
   artifact-class table for how); everything else is "built, unverified" or
   "claimed by agent X, not yet checked."

## The refresh procedure

1. List the doc's factual claims (counts, states, dates, gates).
2. For each: measure the current truth with a real tool.
3. Update, date, and where the drift was embarrassing, add the measurement
   COMMAND next to the claim so the next updater can re-run it, e.g.
   "184 unconnected (measured 2026-07-02, cmd: python check_unconnected.py
   board.file)".
4. Commit with the measurements in the message - the commit log becomes the
   audit trail.
