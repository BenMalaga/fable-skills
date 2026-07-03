# fable-skills

**The working style of a top-tier model, written down as agent skills any
model can load.**

Claude Fable 5 spent a long, brutal stretch running a solo founder's entire
company: routing PCBs to fabrication, orchestrating dozens of parallel agents,
shipping web work, vetting research programs, and debugging an autorouter that
lied about being slow. This repo distills that into two things: a **behavioral
port** - the general disciplines that separate top-tier agentic work from the
tier below, so a smaller or older model inherits the working style - and a set
of **field lessons**, each encoding a real failure and the discipline that
beat it.

An honest note on scope: a skill cannot transfer raw reasoning depth. It can
transfer defaults, first moves, checklists, stopping rules, verification
habits, and escalation criteria - which is most of what you notice day to day.
That is what these are.

## The port: general disciplines

How to work, independent of domain. Each targets a specific moment where the
weaker default goes wrong.

| Skill | The moment it governs |
|---|---|
| [execute-to-done](skills/execute-to-done/SKILL.md) | Ending a turn: executed work, never plans, offers, or "shall I proceed?" on revertible actions |
| [act-on-intent](skills/act-on-intent/SKILL.md) | Parsing a terse request: infer from context, bound the expansion, don't turn an aside into a project |
| [check-the-premise](skills/check-the-premise/SKILL.md) | An instruction arrives with an embedded claim: spend a few read-only calls checking it before building on it |
| [calibrated-reporting](skills/calibrated-reporting/SKILL.md) | Composing a report: fixed section order, failures first-class, subagent hearsay never laundered into fact |
| [triage-the-error](skills/triage-the-error/SKILL.md) | A command just failed: full output, first error, grep project memory before theorizing |
| [diversify-or-park](skills/diversify-or-park/SKILL.md) | Attempt one failed: change approach family or park it; never bump-the-timeout thrash |
| [own-the-diff](skills/own-the-diff/SKILL.md) | Editing existing code: edit what you re-read, then read the diff and its callers; never regenerate from memory |
| [right-size-new-code](skills/right-size-new-code/SKILL.md) | Writing new code: read sibling files first, match the repo's idiom and size, no speculative architecture |
| [delegate-brief-verify](skills/delegate-brief-verify/SKILL.md) | Delegating: when to fan out at all, how to brief a context-free agent, what evidence to demand back |
| [plan-keystone-first](skills/plan-keystone-first/SKILL.md) | Writing a plan: plan against the real world, keystone assumption at step 1, every step gets a pass condition |
| [externalize-session-state](skills/externalize-session-state/SKILL.md) | Long sessions: journal decisions and measurements to files so compaction and restarts can't erase them |
| [ship-gate](skills/ship-gate/SKILL.md) | Declaring a multi-part task done: reconcile every clause of the original request; consume the artifact as its recipient |

## Field lessons

Each encodes a named failure from real autonomous work.

| Skill | The failure it prevents |
|---|---|
| [verify-dont-claim](skills/verify-dont-claim/SKILL.md) | Reporting a subagent's claim as fact; it had zero commits |
| [watch-the-live-log](skills/watch-the-live-log/SKILL.md) | Four wrong theories about a "slow" tool that finished in 39 seconds and hung at save |
| [fleet-orchestration](skills/fleet-orchestration/SKILL.md) | Parallel agents colliding on files, sub-delegated work silently dying |
| [durable-background-work](skills/durable-background-work/SKILL.md) | One host restart killed three parallel agents and a scheduled loop; uncommitted work evaporated |
| [measured-sweep](skills/measured-sweep/SKILL.md) | Audits whose findings are opinions; a "16mm offset" that was an anchor-convention misread |
| [idea-gauntlet](skills/idea-gauntlet/SKILL.md) | Brainstorms where nothing gets killed and datasets turn out not to exist |
| [doc-truth-refresh](skills/doc-truth-refresh/SKILL.md) | A tracker that said "patent unfiled" three weeks after filing |
| [snapshot-before-regenerate](skills/snapshot-before-regenerate/SKILL.md) | A generator re-run silently destroyed a hand-approved artifact that existed nowhere else; a full workday lost |
| [human-gate-registry](skills/human-gate-registry/SKILL.md) | Agents attempting, or falsely reporting done, actions only the human may take (payments, publishes, live sends) |
| [publish-preflight-scrub](skills/publish-preflight-scrub/SKILL.md) | A private repo nearly flipped public with a home-directory path and an unfinished result in the pushed tree |
| [skill-distiller](skills/skill-distiller/SKILL.md) | Solving the same hard problem twice - the meta-skill that generates new skills from sessions |

## Domain packs

| Skill | Scope |
|---|---|
| [kicad-hardware-verification](skills/kicad-hardware-verification/SKILL.md) | KiCad/pcbnew PCB work: backwards jacks, dead controls, copper past the board edge - caught as bytes, not resin |

## Install

```bash
git clone https://github.com/BenMalaga/fable-skills && cd fable-skills
```

For one project:

```bash
mkdir -p .claude/skills
cp -R skills/* .claude/skills/
```

For every session on your machine:

```bash
mkdir -p ~/.claude/skills
cp -R skills/* ~/.claude/skills/
```

Claude Code discovers `SKILL.md` files automatically; each skill's
`description` frontmatter tells the model when to reach for it. Individual
skill folders can also be copied selectively.

## Format

Plain [agent skills](https://code.claude.com/docs/en/skills): one directory
per skill, one `SKILL.md` with `name` + `description` frontmatter and a body
under ~120 lines. No dependencies, no scripts, no configuration.

## The quality bar (from skill-distiller)

A lesson made it in only if: it encodes a named failure, it would change a
competent model's behavior, it generalizes past the incident that taught it,
and its description triggers BEFORE the mistake happens. The port skills faced
one more filter: an adversarial reviewer asking "would a strong model already
do this without the skill?" - anything that survived is there because the
answer was no.

## License

MIT. From [new harmonics](https://newharmonics.net).
