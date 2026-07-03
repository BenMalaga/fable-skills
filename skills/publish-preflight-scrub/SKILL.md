---
name: publish-preflight-scrub
description: Audit the tree that will actually be served, including its history, before flipping anything public. Use when making any repo, deploy, or doc public, transferring visibility, or publishing artifacts that were developed privately.
---

# Publish preflight scrub

What goes public is the pushed tree and its full history, not your local
working copy. A repo can look immaculate on your machine and still leak from
the remote.

## The failure this prevents (real case)

A private research repo was queued to flip public. The local checkout looked
clean. The PUSHED tree contained an absolute home-directory path (naming the
machine's user) and an unfinished result that, once public, would have read as
a published finding. It was caught at the flip and held. The lesson: the local
copy was never the artifact being published.

## The procedure

1. **Audit what will be served.** Clone fresh into a temp dir, or inspect the
   remote tree directly, and run every check against THAT - never against your
   working copy.
2. **Grep the full tree AND the history** for each leak class:
   - absolute home paths (`/Users/`, `/home/`, `C:\Users`)
   - credentials, tokens, keys, connection strings
   - internal-notes folders (`_internal`, scratch dirs, private planning docs)
   - personal data: emails, phone numbers, names not meant for release
   - TODO / FIXME / placeholder text in user-facing surfaces
   - results framed as findings that are not final

   For history: `git grep <pattern> $(git rev-list --all)`. A clean tip with a
   dirty history still leaks - every old commit becomes browsable at flip
   time.
3. **Check .gitignore did its job retroactively.** Ignoring a file today does
   not remove it from commits made before the rule existed. Search history for
   currently-ignored patterns.
4. **Vet every claim that becomes public.** An unfinished analysis in a
   private repo is a draft; the same file in a public repo is a publication.
   Anything not final gets removed, clearly marked as preliminary, or the flip
   waits.
5. **Scrub at the moment of flipping, not the moment of writing.** Hygiene
   while writing helps but never substitutes: files accumulate between the
   last scrub and the flip, and the flip is the only moment that matters.

## Anti-patterns

- Auditing the working copy and calling the remote clean by extension.
- Grepping only the tip commit: history is published too.
- Fixing a leak with a new commit on top: the leaked bytes remain reachable in
  history; rewrite history or publish from a clean tree if the leak is
  sensitive.
- Treating a "private for now" repo as a safe place for secrets: visibility is
  one setting change away, often made in a hurry.
