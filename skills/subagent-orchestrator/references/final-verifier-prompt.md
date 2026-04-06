## Task

Final integration verification pass across all completed tracks.

## Inputs

- Track ledger
- Changed files grouped by track
- Per-track review outcomes

## Checks

1. Cross-track naming/symbol consistency
2. Import/dependency/interface compatibility
3. Integration-level regression risks
4. Test alignment for combined changed behavior

## Constraints

- Do not spawn subagents.
- Do not call any MCP `delegate_*` tools.
- Read-only unless explicitly instructed otherwise.

## Report

1. Files reviewed
2. Findings by severity
3. Suggested minimal fixes
4. Verification commands
5. `agent_id`
