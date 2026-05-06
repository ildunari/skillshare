---
name: claude-code-skill-evolution
description: Run Claude Code as a sandboxed iterative skill-improvement optimizer. Use when Kosta wants to burn Claude subscription quota productively, improve Hermes/Skillshare/Claude skills, run Sonnet/Opus lanes, compare skill variants, collect token/cost stats, detect plateau, or generate reviewable patches without touching live skills.
metadata:
  targets:
    - hermes-default
    - hermes-gpt
    - claude
    - claude-hermes
---

# Claude Code Skill Evolution

Use this when the goal is not just to edit a skill once, but to make Claude Code spend real effort improving it in a controlled, measurable way.

The key idea: Claude Code is the optimizer, not the applier. It works in copied sandboxes, produces candidates, judges them against a rubric, iterates until progress stalls, and leaves reviewable artifacts. Live Skillshare/Hermes files are patched only after review.

## Default stance

Automate aggressively when the action is safe, local, reversible, and predictable. Do not make Kosta nanny routine work. Ask first only for destructive writes, external publication, credential changes, gateway restarts from a live gateway chat, or ambiguous scope decisions that materially change the run.

## When to use

Use this for:

- spending Claude weekly cap on useful improvement work
- improving one or more `SKILL.md` files
- comparing Sonnet-generated variants with Opus or cheaper judges
- discovering stale commands, broken paths, missing verification, unsafe user-confirmation patterns, or voice flattening
- producing patch bundles for manual application

Do not use this for direct live rewrites. If the user asks to apply results, apply only reviewed hunks to canonical Skillshare source, then sync.

## Inputs

Before launching a run, define:

- target skills: canonical source paths, usually under `~/.config/skillshare/skills/`
- wall-clock budget and stop buffer
- max iterations per skill, usually 3–5
- max parallel skills, usually 2–3
- worker model, usually Sonnet
- judge model: Haiku/Sonnet for frequent cheap scoring, Opus for finalist review
- protected clauses: specific lines, sections, user preferences, safety rules, or deliberate voice that must not be removed

If a target is a Hermes/Skillshare skill, prefer canonical Skillshare source over copied live profile files.

## Sandbox layout

Create a timestamped run root:

```text
~/.hermes/evolution-runs/claude-code-skill-evolution/YYYYMMDD-HHMMSS/
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

- Stop after two consecutive rounds with improvement <3 points.
- Stop immediately if the best candidate gets worse twice, starts adding generic bloat, or trips an auto-reject rule.
- Stop 15–20 minutes before quota/reset/window end to collect artifacts and kill stragglers.

## Claude Code invocation

Use Claude Code headless mode. Verify the CLI supports flags before relying on them:

```bash
claude --version
claude --help | grep -E -- '--model|--permission-mode|--print|--output-format|--no-session-persistence'
```

Worker lane pattern:

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

## Stats to collect

After every worker and judge run, parse Claude Code JSON and write `USAGE_SUMMARY.json`:

```json
{
  "skill": "web-research",
  "iteration": 2,
  "variant": "automation",
  "model": "claude-sonnet-4-6",
  "turns": 12,
  "duration_ms": 300000,
  "total_cost_usd": 0.75,
  "input_tokens": 10,
  "cache_creation_input_tokens": 50000,
  "cache_read_input_tokens": 600000,
  "output_tokens": 15000,
  "score": 84,
  "decision": "advance"
}
```

Report both:

- Claude Code cost/token accounting, useful for comparing runs
- total token volume including cache read/write/output, useful for weekly-cap burn intuition

Do not pretend subscription cap maps exactly to `total_cost_usd`; label it as relative accounting.

## Eval prompts

Document-only review is not enough. Add at least two lightweight behavioral eval prompts per skill:

- one happy-path task where the improved skill should make the agent act correctly
- one edge case that should trigger a safety boundary or fallback

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
