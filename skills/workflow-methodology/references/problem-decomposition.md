# Problem decomposition

> Adapted from `superpowers/skills/dispatching-parallel-agents`. Original skill dispatches concurrent subagents -- this adaptation retains the decomposition and scoping methodology for sequential execution in Claude.ai chat.

## When to decompose

```
Multiple problems or failure modes?
  │
  ├─ No → Work on it directly
  │
  └─ Yes → Are they independent?
       │
       ├─ No (related) → Investigate together. Fixing one may fix others.
       │
       └─ Yes → Can they be solved without shared state?
            │
            ├─ No → Sequential with careful ordering. Note dependencies.
            │
            └─ Yes → Decompose into separate focused tasks.
                     Work through each with isolated context.
```

**Decompose when:**

- 3+ failures with different root causes
- Multiple subsystems broken independently
- Each problem can be understood without context from the others
- No shared state between investigations

**Don't decompose when:**

- Failures are related (fixing one might fix others)
- Need to understand full system state before acting
- Tasks would interfere with each other (editing same files, same functions)
- Exploratory debugging where you don't yet know what's broken

## How to scope each sub-task

Every decomposed task gets four properties. If you can't fill all four, the decomposition isn't ready.

| Property | What it means | Bad example | Good example |
|---|---|---|---|
| **Specific scope** | One problem domain | "Fix all the tests" | "Fix the 3 failing tests in auth-flow.test.ts" |
| **Clear goal** | What does "done" look like | "Fix the race condition" | "Make these 3 tests pass without arbitrary timeouts" |
| **Constraints** | What should NOT be touched | (none stated) | "Don't change production code, fix test expectations only" |
| **Expected output** | What to report back | "Fix it" | "Summary of root cause + what changed + verification" |

## Execution pattern (adapted for chat)

Since I can't dispatch parallel agents, I work through decomposed tasks sequentially with focused context per task:

1. **Identify domains.** Group failures by what's broken. Name each domain.
2. **Scope each task.** Fill the four-property table above.
3. **Work one at a time.** Give each task full focused attention. Don't context-switch mid-task.
4. **Report after each.** Summarize root cause and fix before moving to next.
5. **Integration check.** After all tasks, verify fixes don't conflict. Look for cross-cutting concerns.

## Common mistakes

- **Too broad:** "Fix everything" → I get lost in scope. Break it down.
- **No context:** "Fix the race condition" without error messages or file names → I have to go hunting.
- **No constraints:** Without boundaries, I might refactor the world instead of fixing the specific bug.
- **Vague output:** "Fix it" doesn't tell either of us how to verify the fix worked.
- **Forcing decomposition on related problems:** If failures share a root cause, investigating them separately wastes effort. Look for commonality first.

## Real example shape

**Scenario:** 6 test failures across 3 files after a refactor.

**Decomposition:**

| Domain | Files | Root cause hypothesis |
|---|---|---|
| Abort logic | agent-tool-abort.test.ts (3 failures) | Timing / race conditions |
| Batch completion | batch-completion.test.ts (2 failures) | Event structure changed |
| Approval flow | tool-approval.test.ts (1 failure) | Async execution timing |

**Why decomposed:** Each domain is independent -- abort logic doesn't share state with batch completion or approval flow.

**Work through sequentially:** Domain 1 → report → Domain 2 → report → Domain 3 → report → integration check.
