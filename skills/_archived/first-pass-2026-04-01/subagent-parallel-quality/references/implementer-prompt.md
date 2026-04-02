## Task

<concise track task>

## Scope

- In scope: <explicit files/areas>
- Out of scope: <explicit exclusions>
- Ownership zone: <paths/interfaces this track owns>

## Constraints

- Do not spawn subagents.
- Do not call any MCP `delegate_*` tools.
- Keep diffs minimal and reversible.
- Do not commit changes.

## Required checks

- <test/lint/typecheck commands for this track>

## Output contract

1. Files read
2. Files changed (with rationale)
3. Tests/checks run + results
4. Blockers/open questions
5. Risks/integration notes
6. Recommended next actions
7. `agent_id`
