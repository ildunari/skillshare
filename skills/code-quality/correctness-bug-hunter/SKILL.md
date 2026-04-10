---
name: correctness-bug-hunter
description: Use when you need a deep static and runtime-informed pass to find flawed logic, unsafe assumptions, and behavior regressions before users hit them. Supersedes `logic-bug-hunter`.
---

# Correctness Bug Hunter

## Overview
A code-quality hunter focused on correctness bugs, state mismatches, edge cases, and silent failures.

## Human Detail Standard
- Trace each bug hypothesis to a concrete code path and observable impact.
- Never hand-wave race/edge conditions; prove or disprove with evidence.

## When to Use
Use when:
- A feature behaves inconsistently or has hidden edge failures.
- You want proactive bug discovery before release.
- A PR touches critical logic paths.

Do not use when:
- You only need formatting/style cleanup.

## Skill Activation Order
- Load `systematic-debugging` first to enforce hypothesis-driven diagnosis.
- Load `test-driven-development` when adding repro tests for discovered logic faults.
- Load `code-reviewer-guardian` after fixes for severity-triaged validation.

## Required Behavior
- Follow data/control flow from input -> transformation -> output.
- Check invariants, null/error handling, race risks, retries/timeouts, and boundary cases.
- Compare implementation behavior against tests and intended product behavior.
- Prioritize findings by severity with concrete repro hints.

## Output Contract
1. Findings ordered by severity
2. File and line references
3. Why it is wrong and user impact
4. Minimal fix direction
5. Missing tests needed

## Good vs Bad
Good:
- Gives reproducible, behavior-based defects.
- Distinguishes likely bug vs stylistic preference.

Bad:
- Vague "could be improved" comments without impact.
- Floods low-value nits before critical correctness issues.

## Test Cases
- Missing retry backoff creates API storm.
- Off-by-one pagination loses last page.
- Race between cancellation and completion causes duplicate writes.
