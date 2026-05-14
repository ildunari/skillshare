---
name: self-evolve-skills
description: Run Claude Code as a sandboxed iterative skill-improvement optimizer. Use when Kosta explicitly wants Claude/Sonnet/Opus lanes, wants to burn Claude subscription quota productively, compare Claude-generated variants with other judges, collect Claude Code token/cost stats, detect plateau, or generate reviewable patches without touching live skills. For Hermes-native self-evolve runs, use hermes__hermes-self-evolve-skills instead.
metadata:
  targets:
    - claude
    - claude-hermes
  hermes:
    command_priority: 430
---

# Self-Evolve Skills — Claude Code Lane

Use this when the goal is not just to edit a skill once, but to make Claude Code spend real effort improving it in a controlled, measurable way.

The key idea: Claude Code is the optimizer, not the applier. It works in copied sandboxes, produces candidates, judges them against a rubric, iterates until progress stalls, and leaves reviewable artifacts. Live Skillshare/Hermes files are patched only after review.

For Hermes/GPT-native runs where Kosta did not ask for Claude, use `hermes__hermes-self-evolve-skills` instead. Do not silently route Hermes self-evolution through Claude Code.

## Default stance

Automate aggressively when the action is safe, local, reversible, and predictable. Do not make Kosta nanny routine work. Ask first only for destructive writes, external publication, credential changes, gateway restarts from a live gateway chat, or ambiguous scope decisions that materially change the run.

## When to use

Use this for:

- spending Claude weekly cap on useful improvement work, when explicitly requested
- improving one or more `SKILL.md` files through Claude Code
- comparing Sonnet-generated variants with Opus or cheaper judges
- discovering stale commands, broken paths, missing verification, unsafe user-confirmation patterns, or voice flattening
- producing patch bundles for manual application

Do not use this for direct live rewrites. If the user asks to apply results, apply only reviewed hunks to canonical Skillshare source, then sync.

## Inputs

Before launching a run, define:

- target skills: canonical source paths, usually under `~/.config/skillshare/skills/`
- wall-clock budget and stop buffer
- max iterations per skill: default **10 minimum**, **30 maximum**, unless the user gives a smaller budget; stop earlier only for the plateau rule or an auto-reject/safety/budget condition
- max parallel skills, usually 2–3
- worker model, usually Sonnet
- judge model: Haiku/Sonnet for frequent cheap scoring, Opus for finalist review
- protected clauses: specific lines, sections, user preferences, safety rules, or deliberate voice that must not be removed

If a target is a Hermes/Skillshare skill, prefer canonical Skillshare source over copied live profile files.

## Sandbox layout

Create a timestamped run root:

```text
~/.hermes/evolution-runs/self-evolve-skills/YYYYMMDD-HHMMSS/
```

For each skill:

```text
<run-root>/<skill-name>/
  original/SKILL.md
  protected.md
  rubric.md
  iteration-0/baseline.md
  iteration-1/CANDIDATE_SKILL.md
  iteration-1/PATCH.diff
  iteration-1/JUDGE.json
  iteration-1/REVIEW.md
  iteration-2/...
  FINAL_CANDIDATE.md
  FINAL_PATCH.diff
  FINAL_DECISION.md
```

Never give Claude Code permission to edit outside the skill's run directory. Copy sources in; copy approved patches out later.

## Rubric

Score each candidate 0–100 with these dimensions:

```text
correctness: 0-20
  Fixes stale commands, broken tool names, bad paths, missing prerequisites, and wrong assumptions.

automation_quality: 0-15
  Makes safe predictable steps autonomous instead of forcing user babysitting. Keeps confirmation only for destructive, external, or genuinely ambiguous actions.

specificity_and_verification: 0-15
  Adds exact commands, expected outputs, failure modes, and verification gates.

safety_and_reversibility: 0-15
  Avoids destructive/shared/external writes unless confirmed. Preserves sandboxing and rollback.

voice_and_intent_preservation: 0-15
  Preserves deliberate Kosta-specific voice, operational constraints, and hard-won guidance.

token_efficiency: 0-10
  Removes dead prose and duplication without flattening useful nuance.

evalability: 0-10
  Makes behavior easier to test with prompts, scripts, or clear stop conditions.
```

Auto-reject a candidate if it:

- edits or instructs edits outside the sandbox during the generation phase
- removes protected clauses without explicit justification
- adds autonomous destructive writes to shared files
- invents unavailable tools or model IDs without a verification step
- converts nuanced user-specific guidance into generic corporate prose
- increases length substantially without adding checkable behavior

## Iterative loop

For each skill, run:

1. Snapshot original into `original/SKILL.md`.
2. Write `protected.md`: clauses that must survive, including Kosta preferences and safety boundaries.
3. Write `rubric.md` with scoring dimensions and auto-reject rules.
4. Ask Sonnet to produce candidate variant A focused on correctness and verification.
5. Ask Sonnet to produce candidate variant B focused on safe automation and fewer nanny prompts.
6. Optionally ask Sonnet to produce candidate variant C focused on concision and path/tool reliability.
7. Judge candidates blind with Haiku/Sonnet using `rubric.md` and `protected.md`.
8. Feed only concrete judge failures into the next improvement round.
9. Continue until plateau or budget stop.
10. Run Opus final review only on finalists.

Plateau rule:

- Kosta's default substantial-run expectation is **minimum 10 loops**, **maximum 30 loops**, or stop when the plateau rule below fires. Do not stop after a couple of tidy edits just because the obvious patch landed; design harder evals and keep improving until the run has real signal.
- Stop after **four consecutive runs/loops** with no material improvement, or improvement below the run's configured significance threshold.
- Stop immediately if the best candidate gets worse twice, starts adding generic bloat, or trips an auto-reject rule.
- Stop 15–20 minutes before quota/reset/window end to collect artifacts and kill stragglers.

## Claude Code invocation

Prefer the Hermes-native self-evolve lane unless Kosta explicitly asks to burn Claude Code. For Claude Code self-evolve runs after the June 15, 2026 Agent SDK credit split, prefer interactive/PTY workers launched with `--prefill` when a controller can submit and monitor them; reserve `claude --print` for unattended JSON-producing workers where the runner must parse machine output.

Verify the CLI supports the relevant flags before relying on them:

```bash
claude --version
claude --help | grep -E -- '--model|--permission-mode|--print|--output-format|--no-session-persistence' || true
python - <<'PY'
import subprocess, time
p = subprocess.Popen(['claude','--prefill','prefill smoke'], cwd='/tmp')
time.sleep(2)
print('prefill_accepted_started_interactive=', p.poll() is None)
p.terminate()
PY
```

Interactive worker lane pattern:

```bash
claude \
  --model claude-sonnet-4-6 \
  --permission-mode acceptEdits \
  --prefill "$(cat /tmp/worker-prompt.md)"
```

Unattended JSON fallback pattern:

```bash
claude --print \
  --input-format text \
  --output-format json \
  --model claude-sonnet-4-6 \
  --permission-mode acceptEdits \
  --no-session-persistence
```

Use a working directory inside the iteration folder. `acceptEdits` is acceptable only because the CWD is a copied sandbox. For stricter runs, use `--permission-mode default` and require candidates to be written through explicit tool calls.

## Background process pattern in Hermes

Run long batches as Hermes-tracked background processes, not shell-disowned jobs, so they can be polled and auto-notify on completion.

Preferred launch from Hermes tooling:

```text
terminal(background=true, notify_on_complete=true)
```

After launch, verify Claude Code is actually running, not just the Python wrapper:

```bash
pgrep -P <runner-pid> -fl claude
ps -axo pid,ppid,command | grep 'claude --print' | grep -v grep
```

A harmless `stty: stdin isn't a terminal` warning can appear in background Claude Code runs. Treat it as noise if the process exits 0 and artifacts are written.

If a headless Claude worker edits the sandbox but hangs without returning JSON, do not let it run indefinitely. Kill it after the configured per-iteration timeout, then inspect the sandbox diff, run the benchmark/verification locally, and either reject or promote the candidate based on evidence. In the final report, label this honestly as a recovered/stuck worker rather than a clean Claude iteration; synthesize loop metrics only from artifacts you actually have.

## Stats to collect

After every worker and judge run, parse Claude Code JSON and write `USAGE_SUMMARY.json`. Track enough metrics to explain both quality and operating cost:

- wall-clock duration per loop and per worker/judge call
- model, turns, tool/API calls, exit reason, and errors
- input, cache-creation, cache-read, output, and total token volume
- estimated context loaded into each run, plus any benchmark-specific context/token estimate
- relative `total_cost_usd` when available, labeled as relative accounting under subscription plans
- candidate score, score delta vs previous best, pass/fail counts, and plateau counter
- files changed, bytes/lines changed, verification commands, and whether target sync/installed-copy verification passed

Report both Claude Code cost/token accounting and total token volume including cache read/write/output. Do not pretend subscription cap maps exactly to `total_cost_usd`; label it as relative accounting.

## Eval prompts

Document-only review is not enough. Add **hard, complex behavioral eval prompts** per skill, not just easy happy paths. Include at least:

- one realistic happy-path task where the improved skill should make the agent act correctly
- one hard-to-track or ambiguous retrieval/debugging task that requires following breadcrumbs, checking prior context, or reconciling conflicting files
- one edge case that should trigger a safety boundary, fallback, idempotency rule, or explicit clarification
- one regression test for a failure mode observed in the session that motivated the skill update

The judge should answer: would the candidate skill cause a future agent to behave better on these prompts than the original? Require concrete evidence from the text.

## Applying results

After Opus final review:

1. Apply only approved hunks to canonical Skillshare source.
2. Preserve backups in the run folder.
3. Validate frontmatter for every edited `SKILL.md`.
4. Run `git diff --check` on patched files.
5. Run `skillshare sync --json`.
6. Verify at least one target profile received the changed skill.
7. Write a short applied-run reference under the relevant maintenance skill if the workflow taught a reusable lesson.

## Final report

Keep the final report short, but include:

- which skills changed
- which candidates were rejected and why
- iteration count and plateau reason per skill
- token/cost stats
- validation commands and results
- run root path for audit
