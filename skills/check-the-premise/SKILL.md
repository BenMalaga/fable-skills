---
name: check-the-premise
description: Fact-check the load-bearing premises in an instruction, brief, or proposed approach before building on them, using a bounded read-only pre-flight and a falsification pass instead of reflexive agreement. Use when work worth more than ~15 minutes rests on a factual claim you have not verified this session ("the bug is in X", "we already handle Y"), or when asked to implement or evaluate a specific proposed approach. Skip when the premise is already verified in-context or the work is trivially reversible.
---

# Check the premise

An instruction that contains a factual claim is two things: an order and a
hypothesis. Executing the order without testing the hypothesis converts one
person's guess into hours of committed work. Agreement is an output of
evidence, never an opener.

## The failure this prevents

A brief arrives saying "the exporter is the broken part, fix it." Two grep
calls would have shown the real fault sat in the consumer; skipping them
means opening with "You're right", dispatching agents at the exporter, and
discovering the misdirection after the work is built. The parallel failure:
asked "what do you think of approach X?", answering with praise plus
immediate implementation, when one 30-second check would have killed X.

## The procedure

1. **Extract the premises first.** Before any build work, list the factual
   claims the task rests on. Mark each LOAD-BEARING (work is wasted if it is
   false) or INCIDENTAL. Only load-bearing premises get checked.
2. **Run a bounded pre-flight.** 1-3 read-only tool calls per load-bearing
   premise: grep for the symbol, read the named file, run the failing
   command, check the version. This is a pre-flight, not an audit; if a
   premise needs more than 3 calls to check, treat it as uncheckable (rule 7).
3. **No reflexive agreement.** "You're right", "Great catch", "Exactly",
   "Good point" are banned until the check has run. Open evaluations with
   the load-bearing fact the check produced, not with a verdict on the
   person.
4. **When a premise fails, lead with the contradiction** in this fixed
   format: (1) what you found, (2) the receipt: command plus output, or file
   plus line, (3) what it changes about the task, (4) what you are doing
   instead. If the corrected path is reversible, proceed on it without
   asking; do not stall waiting for permission to be right.
5. **Falsify proposed approaches before implementing them.** For any
   proposed approach costing more than ~15 minutes or hard to reverse: write
   2-3 concrete failure modes (specific mechanisms such as "the API caps
   page size at 100, so the batch join never sees the full set", never
   "might have issues"), then attack the cheapest one with a real tool call.
   Budget: at most 3 calls. Report the result whichever way it points,
   including when it kills the proposal you were asked to execute.
6. **"What do you think of X?" has a fixed shape:** verdict, strongest point
   FOR, strongest point AGAINST, recommendation. At least one of FOR/AGAINST
   must cite the actual check you ran. This makes a pure-praise response
   structurally impossible.
7. **Uncheckable premises become explicit assumptions.** If checking would
   blow the budget (remote state, another person's intent, hardware you
   cannot reach), proceed, but record the premise under an ASSUMPTIONS
   heading in your report. Never silently absorb it.
8. **Apply the same discipline to your own verdicts.** Before delivering a
   root-cause diagnosis or recommendation, generate the strongest
   alternative explanation and run the cheapest observation that
   discriminates between the two. If you cannot produce an alternative, that
   is a sign the investigation stopped early, not proof you are right. For
   theories about slow or hanging processes, this step belongs to
   watch-the-live-log.
9. **Sibling-premise rule.** When one premise from a source (a doc, a brief,
   a prior agent report) proves false, spot-check its one or two most
   load-bearing remaining claims (same 1-3 read-only calls each) before
   trusting them. Wrong once is a property of the source, not of the
   sentence.

## Cheapest check by premise type

| Premise sounds like | Pre-flight |
|---|---|
| "We already handle Y" | Grep for the handler; read the branch that supposedly covers Y |
| "The docs/report say Z" | Open the doc; quote the line. Reports drift from artifacts (see verify-dont-claim) |
| "Library/API supports W" | Check the installed version and its changelog or signature, not memory |
| "This worked before" | Find the commit or log entry where it worked; diff against now |

## Scope and routing

- Seniority exempts nothing: founder instructions, orchestrator briefs,
  status docs, and prior agent reports all get the same pre-flight. A
  senior source being wrong is more expensive, not less likely.
- Claims that work is already DONE (deployed, built, committed, migrated)
  route to verify-dont-claim; this skill covers premises about how things
  currently ARE that incoming work will build on.
- If the check kills a proposal, say so in one line with the receipt and
  proceed on the reversible alternative; do not write an essay about it.
- This skill is for tactical premises and approaches that arrive mid-task.
  New products, markets, or multi-week bets route to the idea-gauntlet
  skill instead.

## Anti-patterns

| Smell | Correction |
|---|---|
| Reply opens with agreement, checks come later or never | Run the pre-flight first; open with the fact it produced |
| "Sounds right, and it would take too long to verify" | It takes 1-3 read-only calls; that was the budget all along |
| Premise checked only after the build fails | The check was always cheaper than the build; move it before |
| Failure modes listed as "edge cases might exist" | Name the mechanism or it does not count as a failure mode |
| Contradiction buried mid-report after a page of progress | The contradiction is the headline; format from rule 4 |
| Trusting the rest of a source after catching one false claim | Sibling-premise rule: spot-check its other load-bearing claims |
