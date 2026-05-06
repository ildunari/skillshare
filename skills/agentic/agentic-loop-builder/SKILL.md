---
name: agentic-loop-builder
description: Use when executing phased implementation that needs build verification, testing, and multi-perspective review before each commit. Triggers on multi-phase plans, protocol fixes, platform builds, or any work where sub-agents implement and reviewers gate quality. Not for single-file edits, quick fixes, or tasks that don't require a build step. Supersedes executing-plans and subagent-driven-development when platform-native review is needed alongside general code review.
---

# Agentic Loop Builder

Orchestrate phased implementation using sub-agents for research, testing, coding, and review — with hard gates between phases. The orchestrator delegates, coordinates, and fixes. Sub-agents execute.

## Before Starting

If requirements are unclear — what to build, what "done" looks like, what constraints apply — offer to interview the user first:

> "I can start planning, but I'd get better results with more context. Want me to interview you about [the domain] first? I'll ask detailed questions about requirements, edge cases, and tradeoffs, then write a spec we can plan from."

If they say yes, cover: scope and success criteria, technical constraints (platform, dependencies, performance), error and edge cases, security implications, integration points, and rollback/undo behavior. Write the completed spec to `spec.md` in the project root and use it as phase-planning input.

If requirements are already clear (existing spec, detailed issue, prior conversation context), skip to phase planning.

**Start task tracking immediately.** Use TodoWrite to create one task per phase before beginning. Mark each phase `in_progress` when started, `done` when committed.

## Core Loop

```
RESEARCH → TEST FIRST → IMPLEMENT → [BUILD?] → [TESTS?] → DUAL REVIEW → [CRITICAL?] → COMMIT
                                        ↑ fail       ↑ fail              ↓ yes
                                        └───────────────────── FIX ──────┘
```

Each arrow is a hard gate. No skipping. No "I'll test it later."

## Phase Declaration

Before starting any phase, declare and print:

```
Phase: [name]
Goal: [one sentence — the observable outcome]
Build command: [exact runnable command]
Test command: [exact runnable command]
Native reviewer: [skill name or agent type]
Code reviewer: [skill name or agent type]
Files in scope: [explicit list — additions and modifications]
Files out of scope: [list anything adjacent that must NOT change]
```

**Example:**

```
Phase: Add retry logic to sync client
Goal: SyncClient retries failed requests up to 3 times with exponential backoff
Build command: xcodebuild -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 16' build
Test command: xcodebuild -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 16' test -only-testing:MyAppTests/SyncClientTests
Native reviewer: apple-swift-language-expert
Code reviewer: code-reviewer-guardian
Files in scope: Sources/Sync/SyncClient.swift, Tests/SyncClientTests.swift
Files out of scope: Sources/Network/, Sources/Auth/
```

This prevents scope creep and gives sub-agents unambiguous boundaries.

## Sub-Agent Prompt Contract

Every sub-agent dispatch must include all six:

1. **Task** — one sentence, what to do
2. **Files** — exact paths to read and/or modify
3. **Context** — protocol specs, type definitions, or reference sections needed
4. **Success criterion** — exact observable output (build passes with exit 0, test X fails with error Y, report contains severity ratings)
5. **Constraints** — what NOT to touch (files outside phase scope)
6. **Output format** — what to return (summary, diff, log snippet, severity list) so the orchestrator knows what to read

Omitting any of these produces bad results. 30 seconds writing a complete prompt saves 5 minutes re-dispatching.

**Research output format to request:** File inventory (path, purpose, key types/interfaces), current issues and error messages verbatim, what is missing or needs creation, and any pre-existing test failures (exact names and messages).

## Steps

### 1. Research

Dispatch an `Explore` sub-agent (`subagent_type="Explore"`) to read files in scope. Always run this even when the code seems familiar — sub-agents start with zero context and will guess at types without it.

**Request this specific output from the research agent:**
- List of relevant files with their purpose and key exported types/interfaces
- Any build or test errors that currently exist (verbatim output, not paraphrased)
- Pre-existing failing tests — record these as the baseline; they must not regress but are not required to be fixed in this phase
- Gaps: what's missing that the phase goal requires

**Verify:** The research report names specific files and types, not just "the networking layer." If it's vague, re-dispatch with a narrower scope question.

### 2. Test First

Dispatch an agent to write failing tests BEFORE implementation. The agent receives: research findings, test file location, test framework name, and phase goal.

For protocol/networking: test exact wire format, mock expected server responses, cover error cases.
For UI: test state transitions, view hierarchy expectations, accessibility.
For logic: test boundary conditions and the specific bug or feature being addressed.

**Verify tests fail correctly:**
1. Run the test command yourself (Bash tool, not sub-agent report).
2. Check exit code is non-zero.
3. Read the failure output — it must fail with a *logic* or *missing implementation* error, not a compilation error. A compilation error means the test itself is broken.
4. If tests pass immediately, either the behavior already exists (skip implementation) or the tests are wrong — do not proceed until resolved.

### 3. Implement

Dispatch an agent to write minimal code making the tests pass. The agent receives: failing test file paths, allowed file scope, any protocol/API reference, and the build command.

Instruct the agent to: run the build command, fix until exit 0, then run the test command, fix until all target tests pass, then return the test output verbatim.

### 4. Build Gate

Run the build command yourself using the Bash tool. Check exit code — 0 is pass, anything else is fail.

```bash
# Example — adapt the command from your Phase Declaration
xcodebuild -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 16' build 2>&1 | tail -20
```

If it fails: send the exact error lines (not the full log) back to the implement agent. Build failures in files that are out of scope and predate this phase can be noted and skipped *only if* they don't affect the phase scope — document them.

### 5. Test Gate

Run the test command yourself using the Bash tool. All phase tests must pass. Pre-existing failures (recorded in step 1) are acceptable if and only if they existed before this phase.

```bash
# Example — adapt from Phase Declaration
xcodebuild -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 16' test -only-testing:MyAppTests/SyncClientTests 2>&1 | grep -E '(PASS|FAIL|error:)'
```

If failures occur: send the exact failure output (test name + error message) back to the implement agent. Never send the full log — extract only the failing test names and their error messages.

### 6. Native Review

Dispatch a platform-specialist review agent (read-only). Choose based on domain:

| Domain | Reviewer |
|--------|----------|
| iOS/Swift | `apple-swift-language-expert`, `apple-swiftui-mastery`, `apple-networking-apis` |
| macOS | `apple-macos-ux-full`, `apple-architecture-patterns` |
| Web frontend | `design-maestro`, `nextjs-app-router-architecture` |
| General | `code-reviewer-guardian` |

The reviewer receives: phase goal, diff of changed files, spec/protocol reference, and the severity scale below. Instruct the reviewer to prefer findings in the format `[P0/P1/P2/P3] filename:line — description` when a line-specific finding exists. For architectural or cross-cutting findings, allow a short section-level location instead of forcing a fake line number.

### 7. Code Review

Dispatch a general code quality reviewer in parallel with step 6. This agent checks correctness, error handling, memory management, thread safety, security. Same severity system and output format. Read-only — if it proposes code changes, discard and re-request findings only.

**Severity scale (P0–P3):**
- **P0 Critical** — crashes, security holes, data loss, protocol violations
- **P1 High** — concurrency bugs, retain cycles, architectural boundary breaks, missing error handling on failure paths
- **P2 Medium** — maintainability, test gaps, style deviations, missing UI states
- **P3 Low** — naming, minor improvements, polish

### 8. Fix

Read both review reports. Fix all P0 and P1 findings yourself — do not re-delegate fixes. Only the orchestrator has seen both reports and the full phase context. After fixing, loop back to step 4 (build gate).

P2 and P3 findings: collect them in a `phase-[name]-deferred.md` note for the next cleanup pass. Do not fix them now.

**Fix cycle limit:** After 3 fix cycles on the same phase without clearing all P0/P1 issues, the phase scope is too large. See Phase Splitting below.

### 9. Commit

Preconditions — all must be true:
- Build exits 0
- All phase tests pass
- No P0 or P1 findings remain

Commit with: `git commit -m "[phase name]: [one-line summary of what changed and why]"`

Do not push unless the user explicitly asked for it. Update task tracking (mark phase `done` in TodoWrite). Move to next phase.

## Phase Splitting

When error recovery step 5 triggers (3 fix cycles, no resolution), split the current phase:

1. Identify the smallest self-contained behavior from the phase goal that can pass build + test independently.
2. Scope a new Phase A to just that behavior. Move the rest to Phase B.
3. Update the TodoWrite task list to reflect the split.
4. Re-run from step 1 (research) for Phase A — do not reuse the old research report across a scope change.

Example: "Add retry logic with exponential backoff and circuit breaker" → split into Phase A: "Add retry logic (fixed attempts)" and Phase B: "Add circuit breaker on top of retry."

## Error Recovery

If a sub-agent fails (context overflow, can't fix build, returns vague text without specifics):

1. Read its partial output — it often contains useful diagnostics even if incomplete
2. Reduce scope: split the step to cover fewer files or a single file at a time
3. Re-dispatch with a more constrained prompt: provide explicit type signatures, concrete examples, fewer responsibilities per dispatch
4. After 2 failed dispatches on the same step, do it yourself — debugging the sub-agent now costs more than direct implementation
5. After 3 fix cycles at the same gate, the phase scope is too large — split it (see Phase Splitting above)

**Signs a sub-agent returned garbage:** no file paths named, no specific types or method signatures referenced, claims "build succeeded" without showing any output, proposes changes outside the declared scope.

## Parallel vs Sequential

- Steps 1–5 are sequential (each depends on the previous)
- Steps 6–7 run in parallel (independent review perspectives)
- Phases are sequential (each builds on the previous)

## Review Dimensions

Both reviewers should cover relevant dimensions. Not every dimension applies to every phase — pick what's relevant.

**Code dimensions:**

| Dimension | What to check |
|-----------|---------------|
| Correctness | Logic errors, protocol mismatches, wrong behavior |
| Security | Credential handling, injection, auth bypass |
| Concurrency | Data races, actor isolation, Sendable compliance |
| Performance | N+1 queries, unnecessary allocations, blocking main thread |
| Error handling | Missing catches, silent failures, crash paths |
| Platform idioms | Native patterns vs fighting the framework |

**UI/Design dimensions** (when phase touches views or styling):

| Dimension | What to check |
|-----------|---------------|
| Visual hierarchy | Focal points, information flow, heading/body/meta distinction |
| Interaction states | Default, hover, active, focus, disabled all present |
| Accessibility | VoiceOver labels, touch targets (44pt min), WCAG AA contrast, dynamic type |
| Responsiveness | Phone/tablet layouts, safe areas, keyboard handling |
| Loading/empty/error | Every async view has all three states, not just the happy path |
| Design token usage | Colors from theme, not hardcoded hex; spacing from scale, not magic numbers |

## Red Flags — Stop

- Skipping tests because "this is just a config change"
- Skipping native review because "it's just networking"
- Fixing P2 issues before moving on (scope creep)
- Sub-agent says "build succeeded" without showing output — verify yourself before accepting
- Review agent proposing code changes instead of reporting findings — reviewers are read-only
- More than 3 fix cycles on the same phase without P0/P1 clearing — phase scope is too large, split it
- Orchestrator writing implementation code instead of delegating — you coordinate, sub-agents execute
- Reusing stale research output from a previous phase for a different scope

## Adapting to Your Project

| Parameter | iOS (xcodebuild) | iOS (SPM) | Web | Python |
|-----------|------------------|-----------|-----|--------|
| Build | `xcodebuild -scheme X -destination 'platform=iOS Simulator,name=iPhone 16' build` | `swift build` | `npm run build` | `ruff check . && mypy .` |
| Test | `xcodebuild -scheme X -destination 'platform=iOS Simulator,name=iPhone 16' test` | `swift test` | `npm test` | `pytest -x` |
| Native reviewer | `apple-swift-language-expert` | `apple-swift-language-expert` | `design-maestro` | — |
| Code reviewer | `code-reviewer-guardian` | `code-reviewer-guardian` | `code-reviewer-guardian` | `code-reviewer-guardian` |

Always run `xcodebuild -list` or `swift package describe` first to confirm the correct scheme and target names before populating the Phase Declaration.
