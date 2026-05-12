# Source Notes

This skill combines four patterns.

## plugin-eval:improve-skill

Use plugin-eval findings as a rewrite brief, then compare before and after. Focus areas:

- reduce trigger and invoke token costs;
- keep `SKILL.md` compact;
- move bulky detail into references or scripts;
- improve trigger descriptions;
- fix broken links and frontmatter issues.

## skill-creator

Treat a skill as context architecture, not documentation. `SKILL.md` should be the routing hub. Put deterministic work in `scripts/`, heavy conditional detail in `references/`, reusable scaffolds in `templates/`, and eval prompts in `evals/`.

Skill improvement should be benchmarked against realistic hero prompts and near-miss prompts. A skill that triggers everywhere is as harmful as one that never triggers.

## gpt-prompt-architect

For GPT/Codex prompt surfaces, use outcome-first structure:

- context;
- task/outcome;
- success criteria;
- constraints;
- evidence and stopping rules;
- output contract.

Avoid generic "be thorough" language. Replace it with concrete evidence thresholds, scope boundaries, and done conditions.

## self-evolve-skills

The Claude/Hermes version contributes the sandbox discipline: copy the target, protect important clauses, score candidates, iterate until plateau, and apply only reviewed hunks back to canonical Skillshare source.

For Codex, prefer Codex-native goals and subagents instead of Claude Code headless workers.

## karpathy/autoresearch

Autoresearch demonstrates the core autonomous loop: one fixed benchmark, one editable file, fixed-time experiments, a TSV log, keep improvements, discard regressions, and repeat. The important transfer is not GPU training; it is the discipline of a narrow editable surface plus an honest metric.

Adaptation for skills:

- `program.md` becomes the Codex goal plus `GOAL.md`.
- `train.py` becomes the candidate skill/prompt/plugin surface.
- `val_bpb` becomes plugin-eval score plus behavioral task metrics.
- `results.tsv` becomes `metrics.jsonl` and `RUNLOG.md`.

## OpenAI Codex Goal And Iteration Docs

Codex `/goal` is for long-running work with a clear objective, validation loop, and verifiable stopping condition. The official pattern is to define the objective, point Codex at files/docs/logs, define proof commands or artifacts, keep a progress log, and pause/resume/clear the goal when done or blocked.

Codex's difficult-problem loop recommends deterministic checks plus judge scoring, machine-readable eval output, artifact inspection, explicit stopping rules, and a running log of scores and changes.
