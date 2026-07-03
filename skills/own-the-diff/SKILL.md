---
name: own-the-diff
description: Make the smallest diff that fulfills the ask, then review the actual diff hunk-by-hunk as a hostile reviewer - existing features preserved, blast radius traced through untouched callers, siblings of fixed bugs swept, construction debris scrubbed. Use before using Write on a file that already exists, when a change alters a function signature, export, config key, or other contract with callers you never opened, and as the last step before committing or reporting a code change done.
---

# Own the diff

The deliverable is the diff, not your intent. Two adjacent moments lose work:
writing the change from a partial mental model of the file (regenerating the
whole thing and silently dropping features you never re-read), and declaring
done from memory of what you wrote instead of the diff that actually landed.
Both are prevented by the same habit: read before you cut, read what you cut.

## The failure this prevents (real cases)

A "small fix" delivered as a whole-file rewrite dropped features the author
never re-read; the user found them missing days later. Separately, a one-line
signature change compiled cleanly and shipped while call sites in files the
author never opened kept passing the old arguments. In both cases the diff
itself contained the evidence, and nobody read it.

## Before editing

1. Grep every symbol your edit touches within the target file and Read each
   hit, plus the file's imports block. You cannot preserve what you have not
   seen.
2. Default tool is Edit with a minimal unique old_string. Use Write on an
   existing file ONLY when the user explicitly asked for a rewrite, or the
   file is a generated artifact being regenerated from source - and then
   snapshot or commit the old version first (the snapshot-before-regenerate
   skill in this collection owns the generator-overwrite procedure).
3. Proportionality gate: a one-behavior change is a diff measured in tens of
   lines. If `git diff HEAD --stat` reports several times more changed lines
   than the ask implies, stop, revert, and redo it as a point edit.

## After editing: read the REAL diff

Run `git diff HEAD --stat` for the shape, `git diff HEAD` for the hunks, and
`git status --porcelain` for what the diff cannot show (new untracked files -
open each one). Plain `git diff` hides staged changes; never review from
memory.

- Every deleted line is either (a) targeted by the ask or (b) has a specific,
  nameable reason. Any other deletion gets restored before you report.
- If a file was regenerated rather than patched: diff old vs new
  feature-by-feature. List everything present before and absent now, then
  restore each item or explicitly justify its removal in the report.
- No drive-by refactors outside the required hunks: no renames, import
  reordering, or formatting fixes in code you were not asked to touch. Revert
  formatting-only hunks. Log the cleanup idea as one line in your report
  instead of doing it.

## Blast radius: changed symbols have users you never opened

For every changed contract, find its users, open each one, and verify it
still matches. Report counts: "N call sites found, N verified." A contract
change is not done until every caller is updated or confirmed compatible.

| You changed | Find users with |
|---|---|
| Function/method signature or behavior | grep the name, or LSP find-references |
| Class, export, module path | grep imports of it across the repo |
| Config key, env var, schema field | grep the literal key in code AND config files |
| CSS class, component prop | grep templates, markup, style sheets |
| CLI flag, API route, event name | grep the string, including docs and tests |

Then run the narrowest command that exercises the NEIGHBORS, not just the
changed file: the module's tests, the full build, the page that renders the
component. Capture the actual output. "It compiles" ranks below "the caller's
test passes."

## Sibling sweep on bug fixes

A bug you can grep for is rarely alone. After fixing one instance, grep for
the same pattern or idiom elsewhere in the repo; fix the siblings or list
them explicitly in the report. Never silently fix exactly one instance of a
copy-pasted bug.

## Debris scrub before commit

| Debris | Action |
|---|---|
| Commented-out code | Delete; version control remembers |
| Session-narration comments ("changed this to fix...") | Delete; keep only WHY comments |
| Debug prints or temporary logging you added | Delete |
| TODO/FIXME markers you introduced | Convert to a real tracked task or remove |
| _v2 / _new / _backup / .bak files | Delete or merge; never commit |
| Untracked files in `git status` | Each one justified in the report or removed |

## Stopping rule

Report done only after all three:

1. Hunks read, every deletion accounted for.
2. All discovered call sites are verified against the new contract, with
   counts in the report.
3. One neighbor-exercising command ran, with its output captured in the
   report.
