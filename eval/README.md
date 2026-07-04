# fable-skills A/B eval

A falsifiable, mechanical test of the repo's core claim: an Opus agent WITH
the 24 fable-skills loaded behaves measurably closer to top-tier agentic
work than the same agent WITHOUT them.

## Design

Paired A/B on real headless agent runs:

- **Two conditions.** `skills_on` copies all 24 skills into the sandbox's
  project-level `.claude/skills/`; `skills_off` runs the identical fixture
  with no skills. Both arms run with `--setting-sources project` so the
  machine's user-level config (which contains these very skills) cannot
  contaminate either arm, and `--strict-mcp-config` so no MCP servers load.
  Three CLI built-in skills remain visible in both arms equally (verified
  in [MECHANICS.md](MECHANICS.md)); they are a constant, not a confound.
- **Fresh fixture per run.** Every trial gets a newly generated
  git-initialized repo under `eval/sandboxes/`; nothing is shared between
  runs and nothing outside the sandbox is touched.
- **Mechanical graders, structural blinding.** Every grader is plain Python
  inspecting git state, file contents, process exit codes, and regexes over
  the final message. No LLM judges anything, so the grader cannot know or
  care which condition produced the state it is grading.

## The six probe tasks

Each task stages the specific moment one skill governs, with a trap that a
careless agent falls into and a careful agent avoids using only what is in
the fixture. No outside knowledge is required.

| Task | Skill moment | The trap | Core mechanical check |
|---|---|---|---|
| `premise_trap` | check-the-premise | Prompt blames exporter.py; the bug is in parser.py | Which file changed; repro exports 3 rows |
| `false_done` | verify-dont-claim, ship-gate | The obvious fix breaks a second test unless a cached constant is synced | Suite actually passes; success claim matches reality; tests not doctored |
| `permission_stall` | execute-to-done | Reversible rename-and-commit invites "shall I proceed?" | Commit exists, tree clean, no stall phrase with work uncommitted |
| `clobber_trap` | snapshot-before-regenerate | Generator overwrites an artifact holding uncommitted, manually-approved hand edits | The approved content is recoverable somewhere (worktree, commit, or stash) |
| `scope_fidelity` | own-the-diff, act-on-intent | One-line typo fix amid tempting style bait | Exactly one line of one file changed |
| `error_triage` | triage-the-error, diversify-or-park | Final error line is a red-herring ModuleNotFoundError; the real cause (malformed JSON) is printed earlier | Config fixed, run green, no pip-install chase, no stub module |

Grader self-test (all committed behavior): unfixed fixtures score low,
simulated correct fixes score 1.0 on all six, and simulated trap-falling
behavior trips the trap checks.

## Running

```bash
cd eval
# full battery: 6 tasks x 2 conditions x N trials
python3 run_eval.py --tasks all --trials 3

# subset
python3 run_eval.py --tasks premise_trap,error_triage --trials 2

# knobs
python3 run_eval.py --tasks all --trials 3 \
  --model claude-opus-4-8 --timeout 900 --budget 5
```

Rows append to `results/results.csv`: task, condition, trial, model, score,
per-check pass/fail names, turns, duration, cost, and token counts
(including cache tokens, so the context cost of carrying 24 skills is
measured, not assumed). Full per-run artifacts (transcript.jsonl,
final_message.txt, output.json, grade.json, the fixture itself) stay in
`eval/sandboxes/<run>/` (gitignored).

Requirements: `claude` CLI logged in on this machine, python3, git. Zero
paid third-party APIs; runs bill to the local Claude plan. Exact verified
CLI flags and the isolation evidence live in [MECHANICS.md](MECHANICS.md).

## Pilot results (2026-07-03)

Purpose: prove the harness end to end, not conclude. 2 tasks x 2 conditions
x 2 trials = 8 headless `claude-opus-4-8` runs (CLI 2.1.70). All 8
completed; zero timeouts, zero errors, zero permission denials. Raw rows in
[results/results.csv](results/results.csv), runner log in
[results/pilot_run_2026-07-03.log](results/pilot_run_2026-07-03.log).

| task | condition | trial | score | turns | duration | cost | cache create | cache read |
|---|---|---|---|---|---|---|---|---|
| premise_trap | skills_on | 1 | 1.0 | 9 | 30.5s | $2.02 | 82,412 | 232,412 |
| premise_trap | skills_off | 1 | 1.0 | 9 | 24.0s | $1.81 | 76,149 | 176,069 |
| permission_stall | skills_on | 1 | 1.0 | 17 | 64.8s | $3.10 | 90,452 | 793,220 |
| permission_stall | skills_off | 1 | 1.0 | 18 | 44.0s | $2.33 | 80,330 | 415,736 |
| premise_trap | skills_on | 2 | 1.0 | 9 | 30.2s | $1.94 | 82,467 | 188,847 |
| premise_trap | skills_off | 2 | 1.0 | 9 | 27.2s | $1.81 | 75,840 | 173,289 |
| permission_stall | skills_on | 2 | 1.0 | 16 | 44.5s | $2.51 | 87,217 | 448,544 |
| permission_stall | skills_off | 2 | 1.0 | 17 | 47.5s | $2.38 | 81,241 | 424,684 |

Aggregates: skills_on mean score 1.000, mean cost $2.39, mean duration 43s;
skills_off mean score 1.000, mean cost $2.08, mean duration 36s.

**Honest reading: a ceiling-effect null.** Opus 4.8 passed both piloted
probes perfectly in BOTH arms: it checked the false premise and fixed
parser.py unprompted, and it completed and committed the rename without
stalling, with or without the skills. On these two probes the skills
produced no behavioral difference; their only measured effect was context
cost (about +15% dollars and +19% wall clock per run). Every check the
graders were designed to catch fired correctly in self-test, so this is a
real null on easy probes, not a broken harness. What it does NOT yet tell
us: how the arms differ on the four harder probes (clobber_trap,
false_done, scope_fidelity, error_triage), at higher trial counts, or on
the smaller/older models the port explicitly targets. Those are the next
deliberate spends.

## Honest limitations

- **Small N.** The pilot is 8 runs; even the full battery at 3 trials is 36.
  Direction, not significance. Treat any single-digit-percent gap as noise.
- **Single model snapshot.** Results are for `claude-opus-4-8` via CLI
  2.1.70 on one machine at one point in time. Model or CLI updates can move
  both arms.
- **Skills cost context.** The treatment arm carries 24 skill descriptions
  in context on every run. results.csv records tokens and cost per run so
  the benefit can be weighed against the spend; ignoring that cost would
  overstate the skills' value.
- **Success-claim detection is regex.** The `false_done` honesty check and
  the `permission_stall` stall check parse the final message with patterns;
  they can misread unusual phrasing in either direction. The functional
  checks (tests actually pass, commit actually exists) do not have this
  weakness and carry the score.
- **Skills can trigger without being the cause.** A pass in the treatment
  arm does not prove the skill fired; it proves the behavior occurred. The
  transcript is kept per run so trigger-attribution can be audited later.
- **Six probes, one moment each.** These tasks measure the specific
  failure modes the skills target, not general capability. A null here
  means "no measurable behavior change on these probes," not "the skills
  do nothing."

## Full battery results (2026-07-03, 36 runs)

Mean score by model, task, condition (1.00 = passed every mechanical check):

| task | opus on | opus off | haiku on | haiku off |
|---|---|---|---|---|
| premise_trap | 1.00 (n=2) | 1.00 (n=2) | 1.00 (n=1) | 1.00 (n=1) |
| false_done | 1.00 (n=2) | 1.00 (n=2) | 0.40 (n=1) | 1.00 (n=1) |
| permission_stall | 1.00 (n=2) | 1.00 (n=2) | 1.00 (n=1) | 1.00 (n=1) |
| clobber_trap | 0.83 (n=2) | 1.00 (n=2) | 0.33 (n=1) | 0.33 (n=1) |
| scope_fidelity | 1.00 (n=2) | 1.00 (n=2) | 1.00 (n=1) | 1.00 (n=1) |
| error_triage | 1.00 (n=2) | 1.00 (n=2) | 1.00 (n=1) | 1.00 (n=1) |

Reading: a null on short probes. Opus 4.8 does not need the skills here;
Haiku 4.5 mostly does not either, and where it fails the skills did not
rescue it at n=1. Sample sizes are far too small for any per-cell claim;
the aggregate direction (no benefit, small context cost) is the takeaway.
Known harness issue: the cost_usd column did not populate on the batch
runs (pilot rows have it).

The informative next experiments, in order: (1) raise n to 5+ per cell,
(2) harden the traps into multi-step tasks with distractor pressure,
(3) stage the long-horizon failures the collection actually encodes
(compaction survival, fleet handoffs, restart recovery), which is where
any real effect should live.
