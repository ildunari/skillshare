---
name: planning-protocol
user-invocable: false
description: |
  Protocol for creating implementation plans before coding. Provides templates for full detailed plans
  (major changes) and quick plans (simple fixes). Use when starting new features, projects, refactors,
  or even quick bug fixes. Triggers: planning, implementation plan, feature spec, how to approach,
  before coding, design document.
---

# Planning Protocol

<!-- Merged from: writing-plans, executing-plans, workflow-protocols (2026-04-05). Legacy material preserved under merged/. -->

## Purpose

Never jump into complex changes without a plan. This skill provides templates and triggers for two planning levels:

1. **Full Detailed Plan** — For major changes, new features, projects
2. **Quick Plan** — For bug fixes, small edits, debugging

## When to Use Each

### Full Detailed Plan Required

**Triggers:**
- New project from scratch
- Major new feature (spans multiple files/modules)
- Significant refactor
- Architectural changes
- Integration with new external system
- User explicitly asks for a plan

### Quick Plan Sufficient

**Triggers:**
- Bug fix (known issue, clear solution)
- Small edit (copy change, config tweak)
- Debugging session
- Test additions
- Minor enhancements (< 50 lines changed)

---

## Full Detailed Plan Template

Use this structure for major work. Write in conversation, not to a file.

```markdown
# Implementation Plan: [Feature/Project Name]

## Overview
[2-3 sentences on what we're building and why]

## Data Models & Relationships

### Entities
- **[Entity1]**: [description]
  - Properties: [list key properties]
  - Relationships: [how it relates to other entities]

- **[Entity2]**: [description]
  - Properties: [list]
  - Relationships: [list]

### Schema Changes
- [Table/collection changes if applicable]
- [Migration requirements]

## API Contracts & Interfaces

### New Functions/Methods
```[language]
// Function signatures with types
func doSomething(param: Type) -> ReturnType
```

### Request/Response Shapes
```[language]
// API request/response structures
struct Request {
    let field: Type
}
```

### Protocol/Interface Definitions
```[language]
protocol SomeProtocol {
    func requiredMethod()
}
```

## Edge Cases

| Edge Case | Handling |
|-----------|----------|
| [Empty input] | [Return empty result / show placeholder] |
| [Network failure] | [Retry with backoff / show error state] |
| [Invalid data] | [Validate and reject / sanitize] |
| [Concurrent access] | [Lock / queue / actor isolation] |
| [User cancellation] | [Clean up resources / restore state] |

## File-by-File Changes

| File | Action | Changes |
|------|--------|---------|
| `path/to/file1.swift` | Modify | Add [X], update [Y] |
| `path/to/file2.swift` | Create | New [component/service] |
| `path/to/file3.swift` | Delete | No longer needed because [reason] |

## Implementation Order

1. **[First step]** — [Why this first]
2. **[Second step]** — [Dependency on step 1]
3. **[Third step]** — [Continue pattern]
4. **Tests** — [What to test]
5. **Verification** — [How to verify it works]

## Intricate Details

### [For UI work]
- Layout: [How elements are arranged]
- Positioning: [Specific constraints, avoiding overlaps]
- States: [Loading, empty, error, success states]
- Animations: [Any transitions or animations]

### [For algorithms]
- Variables: [Key variables and their flow]
- State tracking: [How state is maintained]
- Naming: [Consistent naming conventions to use]
- Data flow: [How data moves through the system]

### [For APIs]
- Auth flow: [How authentication works]
- Error propagation: [How errors bubble up]
- Retry logic: [When and how to retry]
- Rate limiting: [Any throttling needed]

## Open Questions

- [ ] [Any unresolved decisions]
- [ ] [Items needing user input]

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| [Performance concern] | [Caching / lazy loading / pagination] |
| [Breaking change] | [Feature flag / gradual rollout] |
| [External dependency] | [Fallback / timeout handling] |
```

**After presenting the plan:** Wait for user acknowledgment before implementing.

---

## Quick Plan Template

For simple tasks, state briefly in your response (or in thinking for very simple fixes):

```
**Approach:** [1-2 sentences on what you'll do]

**Risks/Assumptions:**
- [Any assumptions being made]
- [Any potential issues]
```

### Examples

**Bug fix:**
```
Approach: Fix null check in handleSubmit() by adding early return when user is undefined.

Risks: None significant — existing tests cover this path.
```

**Config change:**
```
Approach: Update API base URL in config.ts from staging to production endpoint.

Risks: Assuming production endpoint is ready. Will verify with health check after change.
```

**Debug session:**
```
Approach: Add logging to isolate where the state becomes undefined. Check component lifecycle order.

Risks: Logs may be verbose — will remove after debugging.
```

---

## Planning Workflow

### For Full Plans

1. **Identify scope** — What's being built/changed?
2. **Research** — Spawn research agents for unfamiliar APIs (see `research-agent-protocol`)
3. **Draft plan** — Fill out the full template above
4. **Present to user** — Share the complete plan
5. **Wait for acknowledgment** — Don't proceed until user confirms
6. **Implement** — Follow the plan, using sub-agents as needed
7. **Verify** — Run tests, check results against plan

### For Quick Plans

1. **State approach + risks** — Brief statement
2. **Proceed** — Implement the fix
3. **Verify** — Run relevant tests
4. **Report** — What changed and why

---

## Common Mistakes to Avoid

1. **Skipping edge cases** — Always enumerate them, even if handling is "throw error"
2. **Vague file changes** — Be specific about what changes in each file
3. **Missing data flow** — For algorithms, trace how data moves
4. **Assuming API shapes** — Research first, then plan
5. **No implementation order** — Dependencies matter, sequence your steps
6. **Forgetting tests** — Include test strategy in the plan

---

## Integration with Other Protocols

- **Research Protocol**: Complete research before finalizing plan
- **Orchestration Guide**: Plan which sub-agents to use for implementation
- **Testing Protocol**: Include test strategy in the plan
- **Task Tracking**: Create tasks from the implementation order

---

## Asking for Clarification

If the plan requires decisions you can't make:

```
## Clarification Needed

Before finalizing the plan, I need input on:

1. **[Decision 1]**: [Options A vs B, tradeoffs]
2. **[Decision 2]**: [Options, implications]

Which approach would you prefer?
```

Use AskUserQuestion tool for structured choices.
