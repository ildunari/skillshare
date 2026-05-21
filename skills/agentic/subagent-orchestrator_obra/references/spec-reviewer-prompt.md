## Task

Validate one completed implementation track against its track spec.

## Inputs

- Track task text
- Scope and ownership zone
- Implementer output report
- Files changed by implementer

## Review checks

1. Spec compliance: all required deliverables present
2. Scope compliance: no writes outside ownership zone
3. Regression scan: obvious behavioral regressions from implementation
4. Verification fidelity: required checks were run and relevant

## Decision

Return one:
- `pass`
- `fail_quick_fix`
- `fail_involved_fix`

## Output

1. Verdict
2. Findings by severity (`critical`, `important`, `minor`)
3. Exact fixes required
4. Fix class recommendation (`quick_fix` or `involved_fix`)
5. `agent_id`
