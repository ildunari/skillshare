---
name: hermes-self-evolve-skills
description: Run Hermes-native sandboxed skill-evolution loops using the active Hermes profile/model, not Claude Code. Use when Kosta asks Hermes/GPT to self-evolve, improve Skillshare skills, build benchmark suites, track progress metrics, compare candidates, sync verified improvements, or visualize skill improvement runs. Claude/Sonnet/Opus lanes belong to agentic__self-evolve-skills unless explicitly requested here as a cross-model comparison.
metadata:
  targets:
    - hermes-default
    - hermes-gpt
    - claude-hermes
  hermes:
    command_priority: 431
---

# Hermes Self-Evolve Skills

Use this for Hermes-native skill improvement. The worker/judge is the current Hermes profile and model unless Kosta explicitly asks for another provider. Do not silently switch to Claude Code just because the older self-evolve workflow exists.

There is no dedicated upstream `hermes self-evolve` CLI subcommand right now. The official Hermes-native process is this Skillshare workflow: copy the target skill into a sandbox, run iterative Hermes `-z`/agent-tool loops against a rubric and benchmark, then apply only reviewed patches back to canonical Skillshare source.

## Default stance

- Reversible local sandbox work: act autonomously.
- Live canonical Skillshare writes: apply only reviewed hunks after benchmark evidence.
- Destructive/shared/external actions: ask first.
- If a worker hangs or returns partial output, keep the artifacts, label the run honestly, and judge only what can be verified.

## Model/provider rules

- Default worker: active Hermes profile/model.
- Default judge: active Hermes profile/model, or the same model with a stricter judge prompt.
- Use Claude Code only if Kosta says Claude/Sonnet/Opus, wants Claude quota burn, or specifically asks for the Claude self-evolve lane.
- Record `provider`, `model`, `profile`, and exact command/tool path per loop. Unknown token/cost values stay null; never synthesize them.

## Sandbox layout

Create a timestamped run root:

```text
~/.hermes/evolution-runs/<skill-name>/YYYYMMDD-HHMMSS/
```

Recommended structure:

```text
<run-root>/
  original/                  # copied canonical source
  workspace/                 # mutable sandbox candidate
  benchmark/                 # eval fixtures, scripts, expected outputs
  iteration-01/
    PROMPT.md
    RESPONSE.md
    PATCH.diff
    JUDGE.json
    VERIFY.json
  ...
  SUMMARY.json
  SUMMARY.md
  dashboard/                 # optional HTML/PNG progress views
```

Never let a worker edit outside `workspace/` during generation. Apply to canonical only after review.

## Loop contract

For a substantial run, default to **minimum 10 loops, maximum 30 loops**, or stop after **4 consecutive plateau loops** with no material improvement. If Kosta gives a different budget, follow it.

Each loop should:

1. Run the current benchmark and capture baseline metrics.
2. Ask the worker to improve either the skill or the benchmark, not both blindly.
3. Reject generic bloat, unsafe autonomy, stale commands, unverifiable claims, or live-vault writes outside an explicit sandbox.
4. Run verification after the candidate edit.
5. Score against the rubric and update plateau state.
6. Make the next benchmark harder if the current one has become too easy.

## Rubric dimensions

Score 0–100, with per-dimension sub-scores:

- correctness
- retrieval/search quality
- breadcrumb/context-following quality
- routing/storage quality
- spec/frontmatter/API compliance
- output/format quality
- safety and idempotency
- verification strength
- token/context efficiency
- evalability and benchmark realism

Auto-reject if the candidate invents tools, removes protected user-specific rules, overwrites shared files without confirmation, edits live data during a benchmark, or inflates prose without checkable behavior.

## Metrics to track

Track these per loop and per candidate when available:

- wall-clock duration
- provider, model, profile
- turns / API calls / tool calls
- exit reason and errors
- input, cache creation, cache read, output, and total token volume
- relative cost, labeled as provider accounting when available
- context chars/tokens loaded
- files scanned/opened/changed
- lines/bytes changed
- benchmark cases passed/total
- score and score delta vs previous best
- plateau counter
- false positives / rejected candidates
- time-to-first-hit and time-to-correct-answer for retrieval evals
- breadcrumb hops and backlinks inspected for graph evals
- verification commands and exit codes
- sync success and installed-copy verification

## Applying results

1. Diff `original/` vs `workspace/` and inspect the actual hunks.
2. Apply only approved changes to canonical Skillshare source under `~/.config/skillshare/skills/`.
3. Run relevant compile/lint/benchmark commands.
4. Run `git diff --check`.
5. Run `skillshare sync -g --json`.
6. Verify Hermes default and Hermes GPT installed copies, then load with `skill_view`.
7. Commit canonical source if the source repo is git-backed.

## Dashboard expectation

For benchmark-driven runs, create a compact visual report under `<run-root>/dashboard/` when useful. Include score over time, benchmark breadth, loop durations, files/lines changed, rubric heatmap, plateau markers, and an honesty panel for missing/partial metrics.

For Telegram, prefer attached PNG or a self-contained HTML path plus a screenshot. Do not rely on wide markdown tables.
