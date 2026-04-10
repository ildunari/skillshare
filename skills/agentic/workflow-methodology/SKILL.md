---
name: workflow-methodology
description: Software development methodology adapted from obra/superpowers for structured planning, execution, self-review, debugging, and feedback handling. Use this skill whenever building multi-step code, planning a substantial implementation, debugging complex multi-failure problems, or applying a disciplined self-review loop. It no longer owns specialist code-review routing; use `code-reviewer-guardian` for dedicated review work. Supersedes `superpowers-methodology`.
---

# Workflow Methodology

> Software development thinking framework adapted from [obra/superpowers](https://github.com/obra/superpowers) for Claude.ai chat. Stripped of Claude Code tooling (subagents, git worktrees, hooks), retaining the methodology that makes the work good.

## Always-on rules

1. **Verify before declaring done.** After writing code, re-read your own output with adversarial eyes. Did you actually build what was asked? Did you miss anything? Did you add anything that wasn't requested?
2. **Ask before guessing.** When blocked, unclear, or uncertain -- stop and ask. Never barrel through ambiguity.
3. **No performative agreement.** Never say "You're absolutely right!" or "Great point!" when receiving feedback. Verify the concern, then either fix it silently or push back with reasoning.
4. **YAGNI.** Don't build what wasn't requested. If reviewing code and tempted to suggest "implement properly," check whether the feature is actually used first.
5. **Severity matters.** Not every issue is critical. Triage into Critical (must fix) / Important (should fix) / Minor (nice to have). Don't cry wolf.
6. **Batch and checkpoint.** On multi-step work, batch ~3 tasks, report progress, get feedback, then continue. Don't try to do everything at once.

## Commands

| Command | What it triggers |
|---|---|
| `/plan` | Full plan mode. Load `references/design-before-code.md` → `references/plan-writing.md`. Clarify requirements first (2-3 approaches with tradeoffs, section-by-section approval), then produce a bite-sized implementation plan with exact file paths, complete code per step, and verification commands. Present the plan for approval before executing. |
| `/review` | Code review mode. Load `references/code-review-checklist.md`. Review the provided code using the full rubric (quality, architecture, testing, requirements, production readiness). Output: Strengths → Issues by severity → Assessment (Ready? Yes/No/With fixes). |
| `/debug` | Systematic debugging mode. Load `references/systematic-debugging.md` + `references/problem-decomposition.md`. Follow the 4-phase process: root cause investigation → pattern analysis → hypothesis testing → implementation. No fixes without diagnosis first. |

## Routing table

Read the relevant reference files based on what you're doing. Multiple files may apply.

| Task type | Load these references |
|---|---|
| **Non-trivial feature request (before building)** | `references/design-before-code.md` |
| **Planning a multi-step build** | `references/plan-writing.md` |
| **Multi-failure debugging or complex problem** | `references/systematic-debugging.md` + `references/problem-decomposition.md` |
| **Executing a multi-step plan or building a feature** | `references/plan-execution.md` |
| **Writing tests or test-driven work** | `references/tdd-discipline.md` |
| **After writing any code (self-review)** | `references/two-stage-review.md` |
| **Reviewing someone else's code** | `references/code-review-checklist.md` |
| **Receiving feedback on code you wrote** | `references/feedback-handling.md` |
| **Full implementation cycle** | `references/design-before-code.md` → `references/plan-writing.md` → `references/plan-execution.md` → `references/two-stage-review.md` |

## How the phases connect

For a full implementation cycle, the phases flow in order. For targeted tasks, jump to the relevant phase.

```
Problem / feature request arrives
       │
       ▼
┌─────────────────────┐
│ 0. DESIGN           │  Clarify requirements. Propose 2-3 approaches.
│    (if non-trivial)  │  Get approval per section before building.
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ 1. DECOMPOSE        │  Is this multiple independent problems?
│    (if complex)      │  Scope each one. Work sequentially with focus.
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ 2. PLAN             │  Write bite-sized tasks with exact file paths,
│    (if multi-step)   │  complete code, and verification per step.
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ 3. EXECUTE          │  Batch ~3 tasks. Build. Report. Get feedback.
│    (TDD when testable)│  Repeat until complete.
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ 4. SELF-REVIEW      │  Spec compliance: did I build what was asked?
│    (always)          │  Code quality: is it well-built?
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ 5. PRESENT          │  Strengths, issues by severity, clear verdict.
│    (always)          │
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ 6. HANDLE FEEDBACK  │  Verify concern → fix or push back.
│    (when feedback)   │  No performative agreement. YAGNI check.
└─────────────────────┘

  ↕ DEBUGGING can interrupt any phase.
    See references/systematic-debugging.md
```

## When NOT to use this skill

- Simple factual questions or casual conversation
- Single-line code fixes where the answer is obvious
- Creative writing or non-code tasks
- Tasks where the user explicitly says "just do it, skip the process"

## Feedback loop

When this skill is active, detect opportunities to improve it:

1. **Detect:** Notice when a methodology step helped or failed during the conversation.
2. **Search:** Check `FEEDBACK.md` for existing related entries.
3. **Scope:** Keep the feedback entry to one actionable observation.
4. **Draft and ask:** Propose the feedback entry to the user before writing.
5. **Write on approval:** Append to `FEEDBACK.md` with date and category tag.
6. **Compact at 75:** When entries reach 75, merge duplicates, promote patterns to reference files, archive resolved items. Reset to ~30 entries.
