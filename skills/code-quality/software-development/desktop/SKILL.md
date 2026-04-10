---
name: desktop
description: Run a multi-agent review-readiness pass on a nearly finished change before commit; fan out exactly three parallel review agents across rules/docs conformance, type safety/source-of-truth, and simplification, then synthesize and apply the worthwhile fixes.
---

# Desktop

Use this skill after a change is functionally correct and before commit, merge, or handoff.

This is a final review-readiness pass, not initial implementation. The goal is to leave the smallest clear diff that still solves the issue.

## Goals

- Run three focused review passes in parallel instead of relying on one vague final read.
- Preserve behavior while improving correctness, readability, type safety, and alignment with repo rules.
- Apply only the clearly worthwhile fixes that stay in scope.
- Leave PR, commit, and handoff text describing the final code state rather than an earlier draft.

## Required review vectors

Launch exactly 3 parallel subagents. Give all three the same context bundle, but assign each one a different review vector.

1. Rules and documentation conformance
   - Review against nearest `AGENTS.md`, repo docs, plans, specs, and design notes.
   - Look for drift from documented patterns, ownership boundaries, or architecture rules.

2. Type safety and source of truth
   - Review for canonical types, inference flow, unsafe casts, duplicated type definitions, widened unions, stray `any`, and trust-boundary validation mistakes.
   - Ask whether mistakes could slip to runtime or deploy time instead of failing earlier.

3. Overengineering and simplification
   - Review for helpers, wrappers, factories, defensive code, or indirection that do not pay for themselves.
   - Ask whether the same result can be expressed more directly without widening scope.

## Required context bundle

Before delegating, gather the exact paths and context the reviewers need.

Include:
- repo root path
- root `AGENTS.md`
- nested `AGENTS.md` files for changed areas
- relevant `docs/...`, `README`, plans, specs, or design docs
- changed files plus enough nearby context to review them properly
- current task summary and any important user constraints not captured in files
- current git diff context when relevant

If the work follows a written plan or spec, include that explicitly. Do not make reviewers guess intent from diffs alone.

## Delegation protocol

1. Read the context bundle yourself first so the delegation is precise.
2. Spawn the 3 review agents immediately with `delegate_task(tasks=[...])` so they work in parallel.
3. While they run, inspect your own diff (`git status`, `git diff --stat`, targeted file reads) and run the narrowest relevant local checks.
4. Require each reviewer to return findings ordered by severity, with file references and concrete reasoning.
5. Wait for all three reviews.
6. Synthesize the responses into one balanced report with headings like:
   - Must fix
   - Should fix
   - Maybe / follow-up
   - Rejected / ignored
   - Proof of work
7. Prefer balanced synthesis over any one reviewer’s hottest take.

## Reviewer prompt contract

Each delegated reviewer should get:
- the same exact context bundle
- one assigned review vector only
- explicit in-scope / out-of-scope limits
- instruction to return findings first, not code changes
- instruction to cite files and call out uncertainty plainly

Suggested reviewer return format:
- Summary
- Must fix
- Should fix
- Maybe
- Passed / no issues
- Uncertainty or missing context

## What to fix automatically

Apply feedback immediately when it is clearly correct, local, and in scope.

Prioritize:
- type drift, unsafe casts, duplicated type definitions
- violations of documented repo boundaries or design rules
- dead helpers, dead code, debug leftovers, placeholder text
- unnecessary wrappers or indirection removable without widening scope
- incorrect or stale PR / commit / worklog wording after code changes

Do not auto-apply feedback that is:
- speculative
- conflicting across reviewers
- mostly stylistic without clear payoff
- a material scope increase
- a stealth refactor outside the changed area

## Steps

1. Gather the context bundle.
2. Launch the 3 required review agents in parallel.
3. While they run, inspect your own diff and run narrow validation.
4. Wait for all responses and synthesize them.
5. Apply the worthwhile fixes that are clearly in scope.
6. Re-run the narrowest affected validation immediately.
7. Update worklog, commit text, and PR-facing text to match the final code state.
8. Stop.

## Stop rules

- Do not turn this into an unrelated refactor.
- Do not churn stable code outside the changed area just to make it prettier.
- If a cleanup is subjective and not clearly better, leave it alone.
- Do not blindly apply every subagent suggestion.
- If the change is still functionally broken, do not use this skill yet; finish implementation/debugging first.

## Hermes-specific notes

- `delegate_task` supports exactly the 3 parallel lanes this workflow wants.
- Subagents cannot ask follow-up questions, so the context bundle must be complete.
- Use this skill after implementation, not instead of implementation.
- Pair well with `requesting-code-review`, `subagent-driven-development`, and verification gates.
