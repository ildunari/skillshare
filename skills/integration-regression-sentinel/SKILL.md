---
name: integration-regression-sentinel
description: Use when a legacy prompt, old workflow, or older skill reference explicitly names `integration-regression-sentinel`; this retired skill exists to redirect that request to `master-orchestrator-agent` for integration and regression gating across multi-track work. Do not select it for new tasks.
---

# Integration Regression Sentinel

## Status
Retired from active routing.

## Why Retired
Integration/regression gating is now owned by `master-orchestrator-agent` so one coordinator can route and verify end-to-end without extra handoff overhead.

## Replacement
Use `master-orchestrator-agent` and include an explicit final integration verification phase in its loop.

## Notes
- Keep this file only as a migration pointer for older references.
- Do not select this skill for new tasks.

## Required Behavior
- Verify symbol/name consistency across changed files.
- Check imports/dependencies and API contract compatibility.
- Ensure tests actually cover touched behavior.
- Flag regression risks with severity.

## Output Contract
1. Files reviewed
2. Findings by severity
3. Exact compatibility risks
4. Suggested minimal remediations
5. Verification command list

## Good vs Bad
Good:
- Focuses on integration risks, not style.
- Produces actionable fixes.

Bad:
- Repeats track-level comments with no cross-track analysis.
- Calls green status without running integration checks.

## Test Cases
- Renamed shared interface not updated in one module.
- Event payload shape changed but tests still shallow.
