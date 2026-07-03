---
name: snapshot-before-regenerate
description: Protect approved artifacts before running anything that overwrites its outputs. Use when about to run a generator, exporter, or build step that overwrites existing artifacts, or the moment a human marks an artifact as approved, final, or "locked in."
---

# Snapshot before regenerate

A generator is not a cache. Nothing guarantees that re-running it reproduces
what is on disk: source edits, library upgrades, and environment drift all
change outputs between runs. Treat every tool that writes to an existing
output path as destructive by default.

## The failure this prevents (real case)

A generator script was re-run for an unrelated tweak. Its output path held a
hand-approved binary artifact (a design-locked 3D mesh) that existed nowhere
else - not committed, no snapshot. The script silently overwrote it with a
subtly different version. Nothing errored; the only signal was a human
noticing the artifact looked wrong, days of context later. A full workday was
lost reconstructing the approved state.

## The procedure

1. **Before the run: check the output paths are protected.** For every path
   the tool writes, run `git status --porcelain -- <path>`. Clean and tracked
   means git holds the current version and you may proceed. Untracked or
   modified means the current bytes exist nowhere else: commit them or copy
   them to a snapshot location FIRST.
2. **After the run: diff the protected set.** Hash-compare every locked or
   approved artifact against HEAD (hash the output of `git show HEAD:<path>`
   against the working file's hash). Any mismatch on an artifact that was
   supposed to be untouched gets restored immediately with
   `git checkout -- <path>`, before anything builds on the corrupted version.
3. **Approval is a commit trigger.** The moment a human approves an artifact
   ("lock it in", "that's the one", "final"), commit it before ANY other tool
   runs. An approved artifact that exists only in the working tree is one
   generator run from gone.
4. **Know the blast radius before running.** If you cannot enumerate which
   files a tool writes, run it once in a scratch directory or read its output
   code first. "I think it only writes X" has destroyed Y.

## Anti-patterns

- Assuming the generator is deterministic: the script that produced the
  approved artifact may no longer produce it.
- Snapshotting after trouble starts: a snapshot's entire value is set before
  the overwrite, not after.
- Treating binary artifacts as less commit-worthy than code. The opposite:
  code can be regenerated from thought; an approved binary often cannot.
- Relying on human memory of which artifacts are "the good ones". Mark them:
  a commit, a LOCKED note beside the file, a protected-paths list the
  after-run diff reads.
