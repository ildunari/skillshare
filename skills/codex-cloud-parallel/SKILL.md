---
name: codex-cloud-parallel
description: Use when parallel exploration is valuable (design options, alternative fixes, competing refactors). Offload to Codex cloud tasks and return only the best result.
---

## When to use

Use this skill when:
- the solution space is wide and you want 2–4 independent attempts,
- you want to keep the local transcript clean,
- you want an “option A/B/C” set before touching the working tree.

## How to run

Use cloud tasks with attempts:

- `codex cloud` to pick an environment interactively.
- `codex cloud exec --env ENV_ID --attempts 3 "<task>"`

Then:
- Compare outputs.
- Choose the best one.
- Apply locally and test locally.
- Preserve only the winning diff; discard the rest to keep history clean.

## Output

Return:
- which attempt you picked and why,
- what changed locally,
- what tests you ran.
