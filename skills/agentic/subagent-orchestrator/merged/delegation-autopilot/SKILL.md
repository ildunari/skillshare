---
name: delegation-autopilot
description: Use when working in Codex interactive mode and the task can be split into independent tracks, especially for parallel implementation, review, testing, or other subagent work using the native agent tools. Do not use for tiny single-track edits or explanation-only tasks.
delegator_exclude: true
---

# Native Parallel Subagent Orchestration (parent-agent only)

This skill is for the parent Codex agent in interactive mode.

## Why this exists

The previous MCP delegation workflow (`delegate_autopilot` / `delegate_run` / `delegate_resume`) is replaced with native subagent orchestration for reliable parallel track control.

## Native Tools

Use these tools only:

- `spawn_agent`
- `send_input`
- `wait`
- `resume_agent`
- `close_agent`

## Reality Model

- One track = one spawned subagent.
- True parallelism = spawn N independent track agents, then grouped `wait(ids=[...])`.
- Parent orchestrator performs decomposition, synchronization, and integration.

## When to Use

Use native subagents before direct edits when at least one is true:

- Work can be split into independent tracks.
- Request spans multiple files/modules.
- Request includes implementation plus tests/docs/review.
- User explicitly asks for delegation/subagents.

Do not use for tiny single-file edits, strict sequential chains, or pure explanations.

## Deterministic Orchestration Rubric

1. Tiny/sequential/local task -> no delegation.
2. Single non-trivial track -> one `spawn_agent`.
3. Independent tracks A/B/C -> one `spawn_agent` per track, then grouped `wait`.
4. Strict track -> one dedicated `worker` with explicit constraints and parent checkpoints.

Exception: when explicitly following `/Users/kosta/.codex/superpowers/skills/subagent-driven-development/SKILL.md`, keep implementation subagents sequential for that workflow's staged review loop.

## Default Native Profile

Role defaults:

- Research/review/audit -> `agent_type: "explorer"`
- Implementation -> `agent_type: "worker"`
- Final verifier -> `agent_type: "explorer"` (or `default`)

Parallel defaults:

- Spawn all independent track agents up front.
- Wait on all IDs together.
- Keep a parent ledger of `track -> agent_id -> status`.
- Treat `agent_id` as the durable persistence key (replacing old MCP `run_dir` references) for resume, verifier context, and recovery.

## Mandatory Constraints in Every Subagent Prompt

- Do not spawn subagents.
- Do not call MCP `delegate_*` tools.
- Keep scope bounded to assigned files and outcomes.
- Return the required report contract exactly.

## Mandatory Report Contract (native)

Every subagent must report:

1. `agent_id`
2. Files read
3. Files changed (if any) + rationale
4. Tests/checks run + pass/fail
5. Blockers/open questions
6. Risks/integration notes
7. Recommendations/next actions

## Final Verifier Loop (required)

After implementation tracks complete:

1. Spawn one final verifier subagent.
2. Provide changed-file list + track summaries.
3. Verify cross-track consistency and regression risk.
4. Integrate only after verifier report is reviewed.

## Timeout and Recovery

If one or more agents are incomplete:

1. Re-run `wait` with explicit IDs and higher timeout.
2. Send corrective guidance via `send_input`.
3. Use `resume_agent` for interrupted threads.
4. `close_agent` completed tracks to keep orchestration clean.

## Long-Session Anti-Drift Rule

Every 3-5 turns in long delegated sessions, restate:

- no subagent recursion
- parent-orchestrated one-agent-per-track model
- grouped wait for true parallel completion
- mandatory final verifier gate

## MCP -> Native Translation Table

- `delegate_autopilot(task, ...)` -> split task into tracks + `spawn_agent` per track + grouped `wait`
- `delegate_run(...)` -> strict single-track `spawn_agent` with deterministic prompt
- `delegate_resume(thread_id, ...)` -> `resume_agent(id)`
- MCP aggregate/run metadata -> parent-maintained ledger keyed by `agent_id`
- `max_agents`/`max_parallel` knobs -> explicit track decomposition + spawn count

## Parent Orchestrator Pseudocode

```text
1) Build tracks: T1, T2, T3 (independent)
2) id1 = spawn_agent({agent_type:"worker", message:"<T1 prompt>"})
3) id2 = spawn_agent({agent_type:"worker", message:"<T2 prompt>"})
4) id3 = spawn_agent({agent_type:"explorer", message:"<T3 prompt>"})
5) wait({ids:[id1,id2,id3], timeout_ms:120000})
6) If needed, send_input({id:id2, interrupt:false, message:"<follow-up>"})
7) wait({ids:[id2], timeout_ms:120000})
8) verifier = spawn_agent({agent_type:"explorer", message:"<final verifier prompt>"})
9) wait({ids:[verifier], timeout_ms:120000})
10) close_agent for all completed agents
```

## Prompt Template: Implementation Track

```md
## Task
<concise track task>

<scope>
- In scope: <files/areas>
- Out of scope: <explicit exclusions>
</scope>

<constraints>
- Do not spawn subagents.
- Do not call MCP `delegate_*` tools.
- Keep edits minimal and reversible.
- Run appropriate tests/checks; if skipped, explain why.
</constraints>

<deliverable>
1. agent_id
2. Files read
3. Files changed + why
4. Tests/checks + results
5. Blockers/open questions
6. Risks/integration notes
7. Next actions
</deliverable>
```

## Prompt Template: Final Verifier

```md
## Task
Final integration verification for all completed tracks.

<inputs>
- Changed files by track
- Track outputs and assumptions
</inputs>

<checks>
1. Cross-file naming/reference consistency
2. Import/dependency/interface compatibility
3. Test alignment with touched behavior
4. Obvious regressions/conflicts
</checks>

<constraints>
- Do not spawn subagents.
- Do not call MCP `delegate_*` tools.
- Read-only unless explicitly asked to patch.
</constraints>

<report>
1. agent_id
2. Files reviewed
3. Findings by severity
4. Suggested minimal fixes
5. Verification commands
</report>
```

## Safety

- Never expose secrets from local config.
- Keep prompts scoped and explicit.
- Parent agent retains final integration ownership.
