---
name: orchestration-guide
user-invocable: false
description: |
  Guide for orchestrating sub-agents effectively. Includes decision matrix for when to spawn agents,
  prompt templates, report format requirements, and context management best practices.
  Use when coordinating multi-file changes, delegating specialized work, or managing context.
  Triggers: sub-agent, delegate, spawn agent, orchestrate, context management, multi-file.
---

# Orchestration Guide

## Purpose

You are an **orchestrator-first agent**. Your primary value is coordination, planning, and high-level reasoning. Delegate execution to specialized sub-agents to:

1. Preserve your context for important decisions
2. Leverage specialist expertise
3. Enable parallel execution
4. Reduce token costs on repetitive operations

## Decision Matrix: When to Spawn Sub-Agents

| Situation | Action | Agent Type |
|-----------|--------|------------|
| **3+ files to modify** | Spawn per module/domain | Specialist or general-purpose |
| **Web research needed** | Spawn research agent | search-specialist |
| **Find files/variables in codebase** | Spawn exploration agent | Explore |
| **Bug investigation** | Spawn debugger | debugger |
| **Security review** | Spawn security specialist | security-auditor |
| **Performance issue** | Spawn performance specialist | performance-engineer |
| **iOS/Swift work** | Spawn iOS specialist | ios-developer |
| **Code review needed** | Spawn reviewer | code-reviewer |
| **Large file to analyze** | Spawn reader agent | Explore or general-purpose |
| **Phase complete, context heavy** | Summarize, spawn fresh agent | Any appropriate type |
| **Parallel-capable independent tasks** | Spawn multiple concurrent agents | Various |

## When NOT to Spawn

- Single file, simple change (< 30 lines)
- Information already in context
- Quick verification you can do directly
- User explicitly wants you to do it yourself

---

## Sub-Agent Prompt Template

**Every sub-agent prompt MUST include these four sections:**

```markdown
## Task: [Descriptive Name]

### Deliverables
[Be explicit about what you expect back]

- Specific output 1: [format/structure]
- Specific output 2: [format/structure]
- Required format: [JSON/markdown/code/etc.]

### Scope

**Include:**
- Files/directories: [specific paths]
- Functionality: [what to examine/modify]
- Depth: [surface scan vs deep dive]

**Exclude:**
- [What to ignore]
- [Out of bounds areas]
- [Time/complexity limits]

### Context

**Main goal:** [What the user is trying to achieve]

**Why this sub-task:** [How this fits into the larger picture]

**Decisions already made:**
- [Relevant decision 1]
- [Relevant decision 2]

**Constraints:**
- [Any limitations]
- [Technology choices already made]

### Report Format

Return your findings as:

## Sub-Agent Report: [Task Name]

### Summary
[2-3 sentence overview of what was done/found]

### Files Changed
| File | Change Type | Description |
|------|-------------|-------------|
| path/to/file | Modified | [What changed] |

### Key Diffs
```[language]
// Most important code changes
```

### Tests Run
| Test | Result | Notes |
|------|--------|-------|
| [test name] | Pass/Fail | [any notes] |

### Open Questions
- [ ] [Anything unresolved]
- [ ] [Decisions needed from main agent]

### Blockers
- [Any blocking issues encountered]

### Recommendations
- [Suggestions for main agent]
- [Follow-up work needed]
```

---

## Sub-Agent Report Requirements

Every sub-agent report MUST include:

1. **Files changed with diffs** — What was modified and the key changes
2. **Tests executed with results** — What was tested, pass/fail
3. **Open questions/blockers** — What couldn't be resolved
4. **Recommendations** — Suggestions for the orchestrator

If a sub-agent returns without these, request completion:

```
Your report is missing [section]. Please provide:
- [Specific information needed]
```

---

## Context Management Strategies

### Proactive Context Preservation

**Before reading large files:**
```
Instead of: Read tool on 2000-line file
Do: Spawn Explore agent to analyze and summarize relevant parts
```

**After completing a phase:**
```
Summarize:
- What was accomplished
- Key decisions made
- Current state
- Next steps

Then spawn fresh agent for next phase if needed.
```

**For research tasks:**
```
Web research is token-heavy. Always spawn:
- search-specialist for web lookups
- Explore for codebase searches
```

### Context Budget Guidelines

| Context Level | Action |
|---------------|--------|
| < 40% | Work directly, spawn for parallelism only |
| 40-60% | Consider spawning for large operations |
| 60-80% | Proactively spawn, summarize completed work |
| > 80% | Must spawn, avoid large reads/fetches |

---

## Parallel Execution Patterns

### Independent Tasks

When tasks don't depend on each other, spawn multiple agents in a single message:

```
Use Task tool multiple times in one response:
- Agent 1: Research API documentation
- Agent 2: Explore codebase for existing patterns
- Agent 3: Analyze test coverage
```

### Sequential with Handoff

When tasks depend on previous results:

```
1. Spawn Agent A for research
2. Wait for report
3. Use findings to spawn Agent B for implementation
4. Wait for report
5. Spawn Agent C for testing
```

### Fan-out / Fan-in

For multi-module changes:

```
1. Create plan for all modules
2. Spawn agents per module (parallel)
3. Collect all reports
4. Review for cross-module issues
5. Final integration pass
```

---

## Specialist Agent Reference

| Agent | Best For | Model |
|-------|----------|-------|
| `debugger` | Root cause analysis, error investigation | sonnet |
| `security-auditor` | Vulnerability analysis, OWASP compliance | opus |
| `performance-engineer` | Profiling, optimization | opus |
| `ios-developer` | Swift/SwiftUI implementation | sonnet |
| `frontend-developer` | React, UI components | sonnet |
| `backend-architect` | API design, system architecture | sonnet |
| `test-automator` | Test suite creation | sonnet |
| `code-reviewer` | Code quality analysis | sonnet |
| `search-specialist` | Web research, documentation lookup | sonnet |
| `Explore` | Codebase navigation, file finding | (built-in) |
| `general-purpose` | Flexible tasks | (built-in) |

---

## Common Orchestration Mistakes

1. **Vague prompts** — "Look at the code" vs "Find all usages of UserService in src/services/"
2. **Missing context** — Agent doesn't know why they're doing this
3. **No report format** — Agent returns unstructured text
4. **Over-spawning** — Simple tasks don't need agents
5. **Under-spawning** — Trying to do everything yourself, exhausting context
6. **Ignoring reports** — Not acting on open questions/blockers
7. **Sequential when parallel possible** — Missing efficiency gains

---

## Example: Multi-File Feature Implementation

**Scenario:** Add user authentication to an app

**Orchestration plan:**

```markdown
## Phase 1: Research (Parallel)
- Agent A (search-specialist): Research current JWT best practices
- Agent B (Explore): Find existing auth patterns in codebase

## Phase 2: Plan
- Synthesize research findings
- Create full implementation plan
- Present to user for approval

## Phase 3: Implementation (Parallel by module)
- Agent C (backend-architect): Implement auth service
- Agent D (frontend-developer): Implement login UI
- Agent E (ios-developer): Implement iOS auth flow (if applicable)

## Phase 4: Integration
- Review all agent reports
- Handle cross-cutting concerns
- Resolve any conflicts

## Phase 5: Testing
- Agent F (test-automator): Create auth test suite
- Run integration tests

## Phase 6: Security Review
- Agent G (security-auditor): Review auth implementation
```

---

## Integration with Other Protocols

- **Research Protocol**: Spawn research agents per that skill's templates
- **Planning Protocol**: Plan orchestration as part of implementation plan
- **Testing Protocol**: Include test agent in orchestration plan
- **Task Tracking**: Create tasks for each agent's work
