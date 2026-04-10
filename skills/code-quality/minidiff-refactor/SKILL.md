---
name: minidiff-refactor
description: Use when a refactor, migration, rename, or other structural multi-file change should be executed in tiny reversible steps with compile or test checks between steps instead of one big patch. Also use when behavior must stay stable during staged cutovers, compatibility shims, or careful cleanup across several files.
---

## Rules of engagement

- Split work into mechanical steps that keep the project running between each step.
- Prefer “introduce new path, then switch callers, then delete old path” over a big-bang rewrite.
- Keep diffs reviewable: small patches, isolated concerns.
- Avoid mixed concerns; one refactor axis per step.

## Checklist

- Compile/build after each step (or run the closest equivalent).
- Run unit tests for touched areas.
- Use `/diff` and `/review` before considering the work “done.”
- If there is no test coverage, add a minimal smoke test or runnable check.

## Output

Summarize:
- steps performed,
- key diffs,
- tests run,
- any follow-ups you intentionally deferred.
