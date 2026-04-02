## Task

Perform code-quality review for one track that already passed spec compliance.

## Inputs

- Implementer report
- Spec-review verdict and findings
- Changed files list

## Review checks

1. Code clarity and maintainability
2. Error handling and edge-case handling
3. Test quality/coverage adequacy for touched behavior
4. Performance or reliability risk introduced

## Decision

Return one:
- `pass`
- `fail_quick_fix`
- `fail_involved_fix`

## Output

1. Verdict
2. Findings by severity (`critical`, `important`, `minor`)
3. Suggested minimal fixes
4. Fix class recommendation (`quick_fix` or `involved_fix`)
5. `agent_id`
