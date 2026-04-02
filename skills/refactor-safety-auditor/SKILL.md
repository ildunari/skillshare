---
name: refactor-safety-auditor
description: Use when planning or reviewing refactors/migrations to enforce tiny reversible diffs, behavior preservation, and continuous validation.
---

# Refactor Safety Auditor

## Overview
Ensures refactors are incremental, reversible, and behavior-safe.

## Human Detail Standard
- Treat each step as production-risky until validated.
- Never skip intermediate verification checkpoints for speed.

## When to Use
Use when:
- Multi-file refactor or migration is planned.
- You need confidence that behavior remains unchanged.

## Skill Activation Order
- Load `minidiff-refactor` for incremental migration mechanics.
- Load `testing-protocol` for stepwise verification after each change.
- Load `verification-before-completion` before merge/ship claims.

## Required Behavior
- Split into small mechanical steps.
- Keep old path working while new path is introduced.
- Validate after each step with nearest tests/build checks.
- Track deferred risk explicitly.

## Output Contract
1. Step plan (<=8 steps)
2. Validation per step
3. Behavior-risk notes
4. Remaining cleanup tasks

## Good vs Bad
Good:
- Introduce -> switch callers -> remove old path.
- Frequent compile/test checkpoints.

Bad:
- Big-bang rewrites touching unrelated areas.
- Declares done without behavior validation.

## Test Cases
- Service extraction from monolith module.
- Config migration with backward compatibility window.
