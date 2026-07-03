---
name: delegate-brief-verify
description: The delegation lifecycle around any subagent spawn - a priced decision on whether to delegate at all, a cold-reader brief template for context-free subagents, and an adversarial cross-check before acting on a high-stakes delegated finding. Use BEFORE spawning a subagent, when you catch yourself grinding a 15+-file sweep inline, when writing any subagent brief, or when a subagent's absence claim ("no issues found", "nothing matches") or diagnosis is about to drive an irreversible or expensive action.
---

# Delegate, brief, verify

A subagent is a contractor with amnesia: it knows nothing you did not write
down, and its report is a claim you have not yet checked. Three decisions
bracket every delegation - whether to delegate, what goes in the brief, and
whether to act on the result - and each has a mechanical test.
fleet-orchestration (in this collection) governs running the fleet; this
skill governs the moments before and after.

## The failures this prevents

- Delegating a 2-minute lookup (the brief costs more than the task), while
  grinding a 50-file sweep inline until the context window is spent on bulk
  reading instead of integration and decisions.
- Writing "fix the bug we discussed" to an agent that was not in the
  discussion; it fixes a different bug, confidently.
- Routing real money, a deletion, or a public flip on the first confident
  "nothing found" without ever asking what was actually searched.

## Part 1: Delegate or do

Writing a brief plus reading a report costs 2-4 tool calls. Price against that:

| Situation | Call |
|---|---|
| Finishable in under ~5 tool calls and the output will not flood your context with bulk reading | Inline, always |
| Sweep over ~15+ files | Delegate |
| 3+ independent workstreams, each requiring heavy reading | Delegate, fan out |
| Well-specified transformation with a checkable acceptance test; bulk read-and-summarize; defined-schema search | Delegate |
| Irreversible actions (and first check whether the action is the human's to take at all); choosing between options; final integration of parallel outputs; work governed by non-negotiable constraints the human has set | Inline, never delegate |

Granularity: one agent per independently verifiable deliverable.

**Self-catch:** on file 12 of 40 of an inline grind, stop. Split the
remainder into briefs and fan out.

**Context-transfer test:** if the task depends on session discoveries you
cannot write down in ~10 lines, either keep it inline or first externalize
those discoveries to a file the subagent will read.

## Part 2: The brief

All six parts are mandatory in every brief:

1. **Objective** - one sentence with a testable done-condition, phrased as a
   command the agent runs and pastes.
2. **Paths** - exact absolute paths for every input and every output.
3. **Constraints** - applicable standing constraints restated verbatim, never
   referenced ("see the style rules" resolves to nothing for a cold reader).
4. **Gotchas** - session-discovered traps: commands that hang, generators
   that must not be re-run, files that look editable but are locked.
5. **Scope fence** - what the agent owns and what it must NOT touch.
6. **Output contract** - required evidence: pasted command output, not prose.

Also include: an effort budget line ("if this exceeds N steps or M minutes,
checkpoint and report"), a blocked-path instruction (write findings to a
named file and stop; do not improvise new scope), and an explicit read-only
flag on lookups and audits. If the work could outlive the host process,
durable-background-work (in this collection) adds the durability layer: the
brief written to disk at dispatch, checkpoint commits per verified unit.

**Cold-reader pass before sending:** reread the brief pretending you have
zero history; every referent must resolve. Deixis grep: replace every "this",
"that", "as discussed", and "the current" with a concrete noun, path, or
value; any "it" whose referent is not named earlier in the same brief gets
the same treatment.

**No shadow work.** After delegating, monitor or message, but never start the
same work yourself. Takeover protocol if the agent is stuck: stop it, harvest
partial output, then continue alone. Before editing any file, check your
delegation notes for in-flight ownership.

## Part 3: Accepting results

Positive completion claims (done, deployed, committed, routed) are
verify-dont-claim territory (in this collection): check the artifact with
your own tools. This section covers what an artifact check cannot reach:
absence claims, judgment findings, and causal diagnoses.

**Absence claims get zero default trust.** "No other occurrences", "no
issues", "nothing matches" must arrive with coverage evidence: the exact
commands run and the exact file set searched. If it is missing, demand it or
rerun one search yourself before accepting.

**High-stakes findings** - anything that drives an order, a public flip, a
deletion, or a product kill - get one independent-path cross-check before you
act. Either spot-check the riskiest sub-claim with your own tools, or spawn a
second agent briefed adversarially: "assume this conclusion is wrong; find
the counterexample." The cross-check must travel a different path than the
original; re-running the same command is not independence. Never present the
first conclusion as established fact.

**Root-cause diagnoses:** a real cause predicts something checkable ("if X
causes Y, removing X removes Y"). State the prediction, check it, then
accept. When two agents conflict, identify the single discriminating
observable and measure it yourself.

**Cost cap:** the gate should cost under ~20% of the original task. If a
proper cross-check is too expensive, downgrade the downstream action to a
reversible form (stage instead of ship, draft instead of send) until it can
be checked. Record "finding X, cross-checked via Y, result Z" next to the
decision it fed.

## Anti-patterns

| Smell | Response |
|---|---|
| Brief contains "the bug", "as discussed", "the usual way" | Failed the cold-reader pass; rewrite with concrete nouns and paths |
| Redoing delegated work yourself "just to be sure" while the agent runs | Shadow work wastes both contexts; monitor, or take over cleanly |
| Accepting "clean" from an audit with no command list | Demand the coverage evidence before it feeds any decision |
| Blaming the agent for wrong work | Diff the failure against the brief first; most misdirection traces to a missing brief line. Fix the brief, then re-dispatch |
| Cross-checking by asking the same agent "are you sure?" | Same path, same blind spots; use your own tools or an adversarial second agent |
