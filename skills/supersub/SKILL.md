---
name: supersub
description: >
  Delegate work to subagents — in parallel or sequentially — across any use case: parallel speed
  (independent low-risk tasks), parallel quality (shared interfaces, higher risk, integration gates),
  multi-domain orchestration (research + code + QA + docs), or implementation plan execution.
  Use whenever a task has 2+ independent tracks, spans multiple files or domains, requires parallel
  investigation, or explicitly calls for subagent delegation, spawning agents, or orchestration.
  Triggers on: "run in parallel," "spawn agents," "delegate," "orchestrate," "multi-track,"
  "do these at the same time," "break into parallel tasks," "use subagents," "implement plan,"
  "run agents concurrently," or any task where independent work streams would benefit from
  parallel execution or specialized delegation.
---

<!-- Merged from: dispatching-parallel-agents, subagent-driven-development, subagent-parallel-quality, subagent-parallel-speed (2026-04-01). Source directories archived. -->

# SuperSub — Subagent Orchestration

Read `FEEDBACK.md` before every use to apply the latest lessons about subagent mapping, model verification, and host-specific tool behavior.

Delegate work to subagents intelligently. Route by task shape, dispatch in parallel when independent, enforce quality gates when risk warrants it, synthesize results into coherent output.

**Core principle:** Classify first, then dispatch. The routing decision matters more than the execution details.

## Routing Decision

Before dispatching, classify the work:

| Shape | Mode | When |
|---|---|---|
| Single simple task | Do it yourself | One file, one concern, <5 tool calls |
| Single complex task | One subagent | Needs isolated context or specialized focus |
| 2+ independent tasks, low risk | **Speed mode** | No shared files, localized changes |
| 2+ independent tasks, higher risk | **Quality mode** | Shared interfaces, public APIs, migrations |
| Multi-domain request | **Dispatch mode** | Research + code + QA + docs spanning domains |
| Implementation plan with tracks | **Development mode** | Structured plan with phases and review gates |

**Upgrade rule:** If you chose Speed mode and discover overlap or integration risk mid-flight, stop new lightweight dispatches and re-route remaining tracks through Quality mode. Never downgrade once risk is confirmed.

## Subagent Types

Pick the most constrained type that fits — less capability means faster, cheaper, and safer.

| Type | Best for | Tools |
|---|---|---|
| `Bash` | Command execution, git ops, builds, terminal tasks | Bash only |
| `Explore` / `explorer` | Fast codebase search, file finding, keyword investigation | Read-only (Read, Glob, Grep, WebSearch) |
| `Plan` | Architecture design, implementation strategy | Read-only |
| `general-purpose` / `worker` | Multi-step implementation, research, reviews | All tools |

Use `Explore` for read-only investigation, `Bash` for command-only work, `general-purpose` when the agent needs to both read and write. Specify thoroughness for Explore agents ("quick", "medium", "very thorough").

## Craft Agent Tool Mapping

When using this skill inside Craft Agent, do **not** assume a generic `Task` tool exists just because the orchestration pattern talks about subagents.

Map the concepts to the tools actually exposed in the current session:

- **True independent agent / parallel worker** → use `spawn_session`
  - Best for real isolation, separate context, separate model selection, and fire-and-forget work.
  - Choose the connection and model explicitly when it matters.
  - Good for long-running research, implementation, or review tracks that do not need to return inline in the same tool call.
- **Fast isolated model-only analysis** → use `call_llm`
  - This is **not** a full tool-using subagent.
  - Use it for critique, summarization, extraction, classification, or focused reasoning over attached files.
  - Use Anthropic/API-key models with `thinking: true` when you specifically want Claude Sonnet/Opus extended reasoning.
- **Do it yourself in the current session** → use normal Read/Bash/Edit/Write/etc.
  - Prefer this for trivial work or when orchestration overhead is not worth it.

**Important:**
- Do not claim a spawned/evaluating model was used unless the actual tool call confirms it.
- Do not describe `call_llm` as a tool-using subagent; it is a single isolated completion.
- Before choosing a subagent path, inspect the currently available tools instead of assuming the environment matches Claude Code or another host.

## Execution Mode: Foreground vs Background

Always use foreground agents for implementation work. Background agents (`run_in_background: true`) have no crash reporting, no health checks, and silently fail without recourse.

| Mode | Use When | Risk |
|---|---|---|
| Foreground (default) | All implementation, reviews, research | Low — errors surface immediately |
| Background | Fire-and-forget tasks where failure is acceptable | High — silent failures, no recovery |

**Parallel foreground agents** — dispatch multiple Task/subagent calls in a single message to make them truly concurrent. In Craft Agent specifically, use `spawn_session` for true independent workers, or multiple `call_llm` calls for parallel model-only analysis.

Never use `run_in_background: true` for:
- Agents that write code or create files
- Agents whose results you need before proceeding
- Any work on the critical path

---

## Mode: Speed (Independent, Low Risk)

Use when all are true:
- Tracks are clearly independent with no shared file/interface ownership
- Risk is low and changes are localized
- Speed-first objective; a final global integration verifier is not required

Switch to Quality mode immediately if any of the following appear:
- Any track modifies shared interfaces, exported contracts, or schema surfaces
- Medium/high-risk work, public API behavior, auth/security, or migration logic
- You need per-track review loops or a required final integration verification pass

### Speed Dispatch Pattern

1. **Identify independent domains** — group work by what's broken or needs doing; confirm each domain is independent
2. **Create focused agent tasks** — dispatch all tracks in a **single message** for true concurrency

Each agent gets:
- **Focused scope** — one problem domain (e.g., "Fix agent-tool-abort.test.ts")
- **Self-contained context** — paste all info, don't make them search
- **Output spec** — what exactly to return
- **Constraints** — what NOT to touch

3. **Review and integrate** — read each summary, verify fixes don't conflict, run integration tests

### Speed Mode Example: Parallel Test Debugging

**Scenario:** 6 failures across 3 files after a major refactoring.

| Agent | Scope | Root Cause Found |
|---|---|---|
| Agent 1 | `agent-tool-abort.test.ts` (3 failures) | Replaced arbitrary timeouts with event-based waiting |
| Agent 2 | `batch-completion-behavior.test.ts` (2 failures) | Fixed event structure bug (`threadId` in wrong place) |
| Agent 3 | `tool-approval-race-conditions.test.ts` (1 failure) | Added wait for async tool execution to complete |

All fixes were independent — zero conflicts, full suite green. This pattern applies whenever failures span multiple independent subsystems (different test files, different bugs, different root causes). Do not use it when fixing one issue might cascade and fix others — investigate together first.

### Common Mistakes (Speed Mode)

| Mistake | Fix |
|---|---|
| Too broad scope ("fix all tests") | Specific scope ("fix auth tests in src/auth.test.ts") |
| No context | Paste error messages and test names |
| No constraints | "Do NOT change production code" or "Fix tests only" |
| Vague output | "Return summary of root cause and changes" |

---

## Mode: Quality (Independent, Higher Risk)

Use when any apply:
- Shared interfaces/contracts or potential cross-track integration risk
- Medium/high-risk changes
- Public API, auth/security, migration, or reliability-sensitive behavior
- Requirement for deterministic rework loops and explicit triage routing
- Requirement for a mandatory final integration verifier

### Quality Workflow

**Phase 1: Partition and classify**
1. Parse work into independent tracks.
2. Assign ownership zone per track (files/interfaces).
3. Detect overlaps; auto-serialize overlapping tracks.
4. Assign risk level per track (`low`, `medium`, `high`).

**Phase 2: Parallel implementation dispatch**
1. Spawn implementer agents for non-conflicting tracks (max 4 parallel).
2. Serialize any tracks that share files or exported interfaces.
3. Capture output in a track ledger (see `references/track-ledger-template.md`).

**Phase 3: Adaptive review loop per track**
- `low` risk: combined spec + quality review in one pass
- `medium/high` risk: spec compliance review first, then code quality review

If review fails → triage:
- Quick-fix (≤12 tool calls, single file, no API/schema change): parent applies targeted fix or small fix agent
- Involved-fix: prefer `resume_agent` on original implementer; if not viable, spawn fresh fixer with prior context
- Cap rework loops at 3, then escalate with explicit report

**Phase 4: Final integration verifier (required)**
Spawn one read-only verifier after all tracks are locally green. Verifier checks:
1. Cross-track symbol and naming consistency
2. Import/dependency/interface compatibility
3. Regression risk at integration points
4. Test alignment with touched behavior

**Phase 5: Integration and closeout**
1. Parent performs final integration actions.
2. Run integration test command(s).
3. Close finished agents.
4. Publish summary with residual risks and next actions.

### Reference files for Quality mode
- `references/implementer-prompt.md`
- `references/spec-reviewer-prompt.md`
- `references/quality-reviewer-prompt.md`
- `references/final-verifier-prompt.md`
- `references/triage-matrix.md`
- `references/track-ledger-template.md`

---

## Mode: Dispatch (Multi-Domain, Ad-Hoc)

Use for requests spanning multiple specialist domains or requiring ad-hoc parallel investigation across different concerns (research, code, QA, docs).

### Decision Matrix

| Situation | Action | Agent Type |
|---|---|---|
| 3+ files to modify | Spawn per module/domain | Specialist or general-purpose |
| Web research needed | Spawn research agent | search-specialist |
| Find files/variables in codebase | Spawn exploration agent | Explore |
| Bug investigation | Spawn debugger | debugger |
| Security review | Spawn security specialist | security-auditor |
| Code review needed | Spawn reviewer | code-reviewer |
| Large file to analyze | Spawn reader agent | Explore |
| Phase complete, context heavy | Summarize, spawn fresh agent | Any appropriate type |
| Parallel-capable independent tasks | Spawn multiple concurrent agents | Various |

When NOT to spawn: single file simple change (<30 lines), information already in context, quick verification you can do directly.

### Dispatch Pattern

1. Parse request into objectives with ownership boundaries
2. Dispatch specialists in parallel where independent
3. Collect and synthesize intermediate results
4. Re-dispatch only for unresolved gaps
5. Final verification pass before responding

**Bounded recursion:** Max depth 2. You (depth 0) → specialists (depth 1) → workers (depth 2, leaf only). Depth-2 agents do not spawn further agents.

### Context Budget Guidelines

| Context Level | Action |
|---|---|
| < 40% | Work directly, spawn for parallelism only |
| 40-60% | Consider spawning for large operations |
| 60-80% | Proactively spawn, summarize completed work |
| > 80% | Must spawn, avoid large reads/fetches |

---

## Mode: Development (Implementation Plan Execution)

Use when executing a structured implementation plan where tasks proceed through staged review loops.

### Development Workflow

1. **Partition plan into tracks** — parse the plan into independent implementation tracks
2. **Dispatch implementers** — spawn one implementer per track (parallel where independent; sequential where tightly coupled)
3. **Per-track review loop:**
   - Implementer completes task, self-reviews, reports back
   - Spec review agent verifies: built what was requested, nothing more, nothing less
   - Code quality review agent verifies: clean, tested, maintainable
   - Fix loop: reviewer finds issue → implementer fixes → re-review
   - Move to next task only when current passes both reviews
4. **Spec compliance before code quality** — wrong order wastes review cycles
5. **Final integration verifier** — after all tracks pass, spawn one read-only verifier

This mode keeps implementation sequential when tasks are tightly coupled, parallel when they are independent.

---

## Writing Subagent Prompts

Good prompts are self-contained, scoped, output-specified, and constrained. Use this template:

```
You are [role] working on [scope].

## Task
[Full description — paste it, don't reference external files]

## Context
[Where this fits, dependencies, architecture notes]

## Your Job
[Numbered steps]

## Constraints
- Do not spawn subagents.
- Do not call MCP delegate_* tools.
- Keep scope bounded to assigned files and outcomes.
[What to avoid, what not to touch]

## Report Format
1. Files read
2. Files changed + rationale
3. Checks/tests run + results
4. Blockers/open questions
5. Risks/integration notes
6. Recommended next actions
```

Paste full task text into the prompt. Subagents should never need to read plan files or hunt for context — provide everything upfront.

---

## Recovery from Agent Failures

If a foreground agent returns an error or incomplete result:
1. Check the error — often a simple fix (wrong path, missing dep, env issue)
2. Resume the agent with its ID if possible, passing corrective context
3. If unrecoverable, do the work yourself — don't re-dispatch for the same task

If a `wait` times out (when using native subagent tools):
1. Re-run `wait` with longer timeout
2. Send corrective `send_input` to stalled track
3. Keep healthy tracks moving
4. Escalate after repeated timeout on same track

If a track exceeds 3 failed re-validation loops: stop automatic retry, surface explicit escalation report.

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Parallel agents editing same files | Serialize conflicting tracks |
| Vague scope ("fix all tests") | Specific scope ("fix auth tests in src/auth.test.ts") |
| Skipping integration verification | Run full suite after parallel work completes |
| Subagents for trivial tasks | Do simple things yourself (<5 tool calls) |
| Unspecified output format | Agents return inconsistent, hard-to-synthesize summaries |
| Quality review before spec compliance | Spec first, quality second (for medium/high risk) |
| Unlimited rework loops | Cap at 3, then escalate with explicit report |
| Agents spawning more agents | Enforce max depth 2 — leaf workers cannot delegate |
| Background agents for critical work | Always foreground — background = fire-and-forget only |
| Not verifying agent output immediately | Check results right after return; don't assume success |
| Dispatching >4 parallel agents | Diminishing returns; 2-4 is the sweet spot |
