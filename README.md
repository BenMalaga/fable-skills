# fable-skills

**Working patterns distilled from Claude Fable 5, packaged as agent skills for
any model.**

Fable 5 spent a long, brutal session running a solo founder's entire company:
routing PCBs to fabrication, orchestrating dozens of parallel agents, shipping
a 3D portfolio site, vetting research programs, and debugging an autorouter
that lied about being slow. These skills are the distillation - each one
encodes a real failure from that work and the discipline that beat it, written
so a different model (Opus, Sonnet, anything that loads agent skills) inherits
the lesson without paying for it again.

## The skills

| Skill | The failure it prevents |
|---|---|
| [verify-dont-claim](skills/verify-dont-claim/SKILL.md) | Reporting a subagent's claim as fact; it had zero commits |
| [watch-the-live-log](skills/watch-the-live-log/SKILL.md) | Four wrong theories about a "slow" tool that finished in 39 seconds and hung at save |
| [fleet-orchestration](skills/fleet-orchestration/SKILL.md) | Parallel agents colliding on files, sub-delegated work silently dying |
| [measured-sweep](skills/measured-sweep/SKILL.md) | Audits whose findings are opinions; a "16mm offset" that was an anchor-convention misread |
| [idea-gauntlet](skills/idea-gauntlet/SKILL.md) | Brainstorms where nothing gets killed and datasets turn out not to exist |
| [doc-truth-refresh](skills/doc-truth-refresh/SKILL.md) | A tracker that said "patent unfiled" three weeks after filing |
| [durable-background-work](skills/durable-background-work/SKILL.md) | One host restart killed three parallel agents and a scheduled loop; uncommitted work evaporated |
| [skill-distiller](skills/skill-distiller/SKILL.md) | Solving the same hard problem twice - the meta-skill that generates new skills from sessions |
| [kicad-hardware-verification](skills/kicad-hardware-verification/SKILL.md) | Backwards jacks, dead controls, and copper past the board edge - caught as bytes, not resin |

## Install

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
`description` frontmatter tells the model when to reach for it.

## Format

Plain [agent skills](https://code.claude.com/docs/en/skills): one directory
per skill, one `SKILL.md` with `name` + `description` frontmatter and a body
under ~120 lines. No dependencies, no scripts, no configuration.

## The quality bar (from skill-distiller)

A lesson made it in only if: it encodes a named failure, it would change a
competent model's behavior, it generalizes past the incident that taught it,
and its description triggers BEFORE the mistake happens.

## License

MIT. From [new harmonics](https://newharmonics.net).
