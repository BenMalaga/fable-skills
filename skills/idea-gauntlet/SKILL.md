---
name: idea-gauntlet
description: Generate ideas through diverse lenses, then adversarially vet each one with real-world checks before any ranking. Use when brainstorming products, research questions, features, or strategies where plausible-but-wrong ideas are expensive - anything that will consume weeks if picked badly.
---

# The idea gauntlet

Brainstorms fail in two ways: everything comes from one angle, and nothing gets
killed. This pattern fixes both: diverse generation, then a skeptic per idea
whose job is execution, not enthusiasm.

## Phase 1 - Generate through lenses

Run N independent generators, each with a DIFFERENT lens (domain, user type,
data source, failure mode - whatever axis suits the space). Each lens gets a
quota and a hard constraint list (budget, tooling, legal lines). Crucially:
generators must GROUND each idea before submitting it - if an idea depends on
a dataset, API, or market fact, the generator verifies it exists (a real web
check, not a memory) before the idea makes the list. Ungroundable ideas cost
the vetting phase real money.

## Phase 2 - Adversarial vetting, one skeptic per idea

Each surviving idea gets its own vetting agent with a default-kill posture:
"your job is to KILL weak candidates." The skeptic performs REAL checks:

- **Novelty/prior art**: search for the thing already existing. A definitive
  precedent kills unless the idea has a genuinely new angle - name it.
- **Load-bearing dependency**: verify the critical resource end to end
  (download the dataset page, confirm the API tier is actually free, check the
  regulation text). "The docs say" is not verification.
- **Feasibility for the actual executor**: the real budget, the real timeline,
  the real skill set - not a hypothetical team.

Verdicts: STRONG / VIABLE / WEAK / KILL, each with the reason. Expect and
accept a meaningful kill rate; a gauntlet that passes 95% of ideas is
decoration.

## Phase 3 - Rank with explicit dimensions

A single director agent scores survivors on named dimensions (impact-if-true,
effort-to-result, dependency solidity, strategic fit, value-of-a-null) and
picks "start first" candidates using queue reality (what fits in the gaps of
current work) - not just the top scores. Time-sensitive ideas (open scoop
windows, expiring data) outrank slightly-better ideas without deadlines.

## Honesty rules

- Vet notes travel with the winners forever; a candidate that survived "with
  homework" carries that homework into its project charter.
- If the requester named target areas, the strongest surviving formulation of
  each MUST appear in the final ranking (marked as mandate slots), even if it
  scored below the cut - the requester decides tradeoffs, not the ranker.
- Killed ideas get one line each in the output: what killed them. Silent kills
  get re-proposed next quarter.
