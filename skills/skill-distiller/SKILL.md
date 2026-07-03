---
name: skill-distiller
description: Mine a work session, postmortem, or memory file for hard-won lessons and emit them as new reusable skills. Use when the user asks to "create skills from this session", after any debugging war or multi-day project with non-obvious lessons, or on a recurring cadence to compound an agent's capabilities.
---

# The skill distiller

An agent that solves a hard problem and writes nothing down solves it again
next month at full price. This skill turns session experience into new SKILL.md
files - the compounding loop.

## What qualifies as a skill (the quality bar)

A lesson becomes a skill only if ALL four hold:

1. **It encodes a failure.** The skill must name the concrete mistake it
   prevents, ideally the real incident. "Be careful with X" is not a skill;
   "X's exit path never fires when Y, so always Z" is.
2. **It changes behavior.** A competent agent reading it would act DIFFERENTLY
   next time - different first move, different check, different default. If
   the skill restates what any strong model already does, delete it.
3. **It generalizes past the incident.** Strip the project-specific nouns and
   the advice must still bite. Keep ONE anonymized real example as the anchor;
   drop the rest of the war story.
4. **It has a trigger.** The description must let a model recognize the
   situation BEFORE the mistake: "use when a process seems stuck", not "about
   processes".

## The distillation procedure

1. **Harvest candidates** from: memory files (especially entries with
   "gotcha", "lesson", "never", "always"), moments where a hypothesis was
   falsified, any task retried 3+ times, anything the user corrected, and
   anything you verified that contradicted a report.
2. **Cluster into single-responsibility skills.** One failure family per
   skill. A skill covering five topics triggers on none of them.
3. **Write each as SKILL.md**: frontmatter `name` (kebab-case) +
   `description` (the trigger conditions - this is what activates the skill,
   write it as "Use when..."), then a body under ~120 lines: the principle,
   the failure it prevents, the procedure, the anti-patterns. Tables for
   lookup content, prose for judgment content.
4. **Adversarial pass**: for each draft, ask "would a strong model without
   this skill already do this?" If yes, cut or sharpen until the answer is no.
5. **Install and ship**: place in the skills directory the target agent loads
   (project `.claude/skills/<name>/SKILL.md` or user-level `~/.claude/skills/`),
   and version-control the collection so other agents and people can adopt it.

## Anti-patterns

- Diary skills: narrating what happened instead of what to DO next time.
- Kitchen-sink skills: merging unrelated lessons because they share a session.
- Secret leakage: skills get published and shared - strip credentials, private
  paths, personal data, and unreleased business specifics before they leave
  the machine.
- Skipping the trigger: a brilliant body with a vague description never fires.
