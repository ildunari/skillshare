# Track Ledger Template

Use one row per track and keep this updated throughout orchestration.

| Track ID | Objective | Risk | Scope (in/out) | Ownership Zone | Implementer Agent | Review Status | Rework Count | Final Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| T1 | <goal> | low/medium/high | in:<paths> out:<paths> | <interfaces/files> | <agent_id> | pending/pass/fail | 0 | open/done/escalated | <notes> |

## Required states

- `open`
- `in_review`
- `rework`
- `done`
- `escalated`

## Required events to log

1. Implementer spawned and completed
2. Spec review verdict
3. Quality review verdict (if applicable)
4. Any quick/involved fix routing decision
5. Re-validation outcomes
6. Final verifier outcome
