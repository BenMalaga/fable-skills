---
name: right-size-new-code
description: Make new code indistinguishable from its siblings and exactly as big as the ask - sample the repo's conventions and helpers before writing, reuse existing dependencies, and ban speculative abstraction, config options, and error handling nobody asked for. Use when creating a net-new file, module, script, or utility in an existing repo, before adding a dependency or helper the repo does not already have, or when the diff has grown several times beyond the stated ask.
---

# Right-size new code

Code written from instinct comes out training-set-average: "production-grade"
scaffolding, a favorite library, generic wrappers. An existing repo does not
want average code; it wants code indistinguishable from what is already there
and exactly as big as the ask. Both are checkable properties, not taste.

## The failure this prevents

Asked for a ~30-line fetch script, an agent shipped 400 lines: a retry
decorator, a config dataclass with six unused fields, a second HTTP client
beside the one the repo had standardized on, and a plugin registry with one
plugin. None of it was wrong, and all of it was cost: review burden, untested
paths, and a parallel idiom that future sessions copy. Over dozens of
delegated tasks this compounds into a repo with three date libraries and no
single way to do anything.

## First moves: sample the neighborhood before writing

1. **Open 1-2 sibling files** doing the closest similar job. Note naming
   style, error-handling idiom, import order, comment density, and where
   their tests live. Before reporting, reread your new code next to one
   sibling: any idiom the sibling does not use (different logger, error
   style, docstring format, import grouping) is a defect to fix. New files
   go where siblings live: list the directory to confirm before creating
   one.
2. **Grep before you build.** Search the repo for keywords plus 2-3 guessed
   function names (`retry`, `http_get`, `slugify`) before implementing any
   utility. Extending an existing helper beats writing a parallel one, even
   when the existing one is slightly awkward.
3. **Check the manifest/lockfile before adding a dependency.** If the repo
   already has a way to do the job (HTTP, dates, CLI parsing, testing), use
   it, even if you prefer another. A genuinely new dependency gets one
   explicit justification line in your report.
4. **Stated rules beat sampled style.** Read the nearest CLAUDE.md /
   CONTRIBUTING / README for locked conventions (banned patterns, formatting
   rules) before inferring conventions from code; the code you sampled may
   itself violate them.

## Scope: one sentence, then trace

Before implementing, write the sentence "the ask is: X". Every block in the
final diff must trace back to that sentence; anything that does not gets
deleted before reporting. A tempting adjacent improvement costs one line in
the report ("could also add X"), never 200 lines of diff.

## Complexity budget

| Rule | Check before reporting |
|---|---|
| Rule of two | No new abstraction (base class, wrapper module, registry, generic helper) until a SECOND concrete caller exists today, in this diff or already in the repo. One caller: inline it. |
| No speculative parameters | A value with exactly one value today is a named constant, not a parameter or config flag. A flag requires an existing second consumer or an explicit request. |
| Error-handling budget | Handle only failures you can name occurring with real inputs, one sentence each. No try/except around code whose failure you cannot name. Unexpected errors surface loudly, never swallowed into log-and-continue. |
| Size gate | Estimate the lines a direct implementation needs. If the actual diff exceeds roughly 2-3x that, justify each extra block in one line or cut it. |

## Risk gate

Before writing, name the one block most likely to be wrong. Before
reporting, show one executed check against that block with real inputs.
Polish on easy parts (docstrings, CLI ergonomics, edge-case flags) does
not count as done until that check exists.

## Formatting and bad conventions

If a formatter or linter config exists, run it instead of hand-styling; never
introduce personal formatting preferences. If the repo's convention is
genuinely bad, follow it anyway for this change and flag the concern in one
report line. Convention changes are their own task, never smuggled into a
feature diff.

## Signature smells

| Smell | Fix |
|---|---|
| Second library for a job the repo already does | Use the incumbent; note the preference in the report if strong |
| try/except commented "just in case" | Delete it; let it raise |
| "While I was in there" refactor inside a feature diff | Revert; propose as one report line |
| New file in a directory with no siblings like it | Re-list where the siblings actually live |
