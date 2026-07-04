# Eval Mechanics: verified CLI facts

Verified 2026-07-03 against `claude` CLI 2.1.70 on macOS (darwin). Every
command below was actually run; outputs are quoted or summarized from real
runs. Re-verify this file if the CLI major version changes.

## 1. Headless runs and the model flag

`claude-opus-4-8` is accepted as a full model name. Working probe:

```bash
env -u CLAUDECODE claude -p "reply with exactly: OK" \
  --model claude-opus-4-8 \
  --output-format json \
  --no-session-persistence
```

Observed result: `{"type":"result","subtype":"success","is_error":false,...,"result":"OK",...}`
with `modelUsage` keyed by `claude-opus-4-8`. The alias `opus` was not needed.

Facts that matter for the harness:

- `env -u CLAUDECODE` is REQUIRED when launching from inside another Claude
  Code session, otherwise the CLI refuses with "Claude Code cannot be
  launched inside another Claude Code session."
- `--output-format json` returns a single JSON object with `result` (final
  message text), `is_error`, `num_turns`, `duration_ms`, `total_cost_usd`,
  `usage` (input/output/cache token counts), `modelUsage`, and
  `permission_denials`. The harness records tokens, cost, duration, and
  turns from this object.
- There is NO `--max-turns` flag in 2.1.70. Bounding is done with
  (a) a hard wall-clock timeout on the subprocess and (b) `--max-budget-usd`.
- One probe run hung past 4 minutes and then succeeded in 1.8 s on retry.
  Transient hangs are real; every harness run gets a subprocess timeout and
  a timeout is recorded as a failed run, not a crash.

## 2. Condition isolation (the load-bearing part)

The user's real `~/.claude/skills` ALREADY CONTAINS the 24 fable-skills, so
an un-isolated control arm would be contaminated with the exact treatment.

### What does NOT work

Scratch `CLAUDE_CONFIG_DIR`: a fresh config dir returns
`Not logged in - Please run /login` even after seeding it with a copy of
`.claude.json` (including `oauthAccount` and `hasCompletedOnboarding`).
On macOS the OAuth credential lives in the login Keychain and the lookup is
scoped so a foreign config dir does not see it. Extracting the keychain
secret to disk was rejected as needlessly risky. Do not use this route.

### What DOES work: `--setting-sources project`

With the DEFAULT config dir (auth intact) plus `--setting-sources project`,
user-level skills are not loaded. Probe in an empty dir:

```bash
env -u CLAUDECODE claude -p "List the names of any agent skills available to you, names only, one per line, or the single word NONE" \
  --model claude-opus-4-8 --output-format json --no-session-persistence \
  --strict-mcp-config --setting-sources project
```

Observed result: `keybindings-help`, `simplify`, `claude-api` and nothing
else. Those three are CLI built-ins that ship with Claude Code itself; they
appear identically in BOTH arms, so they are a constant baseline, not a
confound. None of the 24 fable-skills leaked.

Project-level discovery: the same command run in a sandbox containing
`.claude/skills/zebra-dummy-probe/SKILL.md` listed `zebra-dummy-probe` in
addition to the three built-ins. So:

- CONTROL arm  = sandbox with no `.claude/skills` dir.
- TREATMENT arm = identical sandbox plus the 24 skills copied into
  `<sandbox>/.claude/skills/<name>/SKILL.md`.
- Both arms always run with `--setting-sources project --strict-mcp-config`.

`--strict-mcp-config` keeps the user's MCP servers out of both arms.

## 3. Unattended permissions

Working combination, verified end-to-end (agent created a file, ran
`git add` and `git commit` with zero permission denials):

```bash
env -u CLAUDECODE claude -p "<task prompt>" \
  --model claude-opus-4-8 \
  --output-format json \
  --no-session-persistence \
  --strict-mcp-config \
  --setting-sources project \
  --permission-mode acceptEdits \
  --allowedTools "Bash,Edit,Write,Read,Glob,Grep"
```

Observed: `permission_denials: []`, file created, commit landed in the
fixture repo. `--dangerously-skip-permissions` was not needed; the
acceptEdits + allowlist combination is preferred because it keeps the
permission system engaged while never prompting for the tools our tasks
need. Runs execute ONLY inside throwaway fixture dirs under
`eval/sandboxes/`.

## 4. The full harness invocation

```bash
cd <sandbox_fixture_dir>
env -u CLAUDECODE claude -p "$(cat prompt.txt)" \
  --model claude-opus-4-8 \
  --output-format json \
  --no-session-persistence \
  --strict-mcp-config \
  --setting-sources project \
  --permission-mode acceptEdits \
  --allowedTools "Bash,Edit,Write,Read,Glob,Grep" \
  --max-budget-usd 5
# plus a hard subprocess wall-clock timeout in run_eval.py
```
