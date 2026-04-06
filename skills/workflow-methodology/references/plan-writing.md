# Plan writing

> Adapted from `superpowers/skills/writing-plans`. The granularity calibration, completeness standard, and plan structure are the valuable methodology. Stripped: git commit of plan files, subagent handoff, worktree context, skill invocation syntax.

## Core calibration

Write implementation plans assuming the engineer has zero context for the codebase and questionable taste. Document everything they need to know: which files to touch, actual code (not "add validation"), how to test each step, expected output at each checkpoint.

This calibration applies to self-use too. Future-you in a long conversation has limited context. Past decisions get lost. Explicit plans prevent drift.

## Bite-sized task granularity

Each step is ONE action, roughly 2-5 minutes of work:

```
"Write the failing test"                    -- step
"Run it to make sure it fails"              -- step
"Implement the minimal code to pass"        -- step
"Run the tests and make sure they pass"     -- step
"Verify it renders correctly in the browser" -- step
```

NOT: "Implement the authentication system" -- that's a project, not a step.

## What every plan task must include

| Required element | Bad example | Good example |
|---|---|---|
| Exact file paths | "Update the config" | "Modify `src/config/auth.ts` lines 23-31" |
| Complete code | "Add validation for email" | Full code block with the validation function |
| Verification command | "Test it" | "`npm test src/auth.test.ts -- --grep 'email'` → expect PASS" |
| Expected output | "Should work" | "Returns `{ valid: true }` for `user@example.com`, throws `InvalidEmail` for empty string" |

**Never use placeholders.** If you don't know the exact implementation, that's a sign you need more design work (see `references/design-before-code.md`), not vaguer plan steps.

## Plan structure

For complex multi-step builds, organize the plan with a header and sequenced tasks:

**Header (always):**
- Goal: one sentence describing what this builds
- Architecture: 2-3 sentences about approach
- Tech stack: key technologies/libraries
- Out of scope: what we're explicitly NOT building (YAGNI)

**Tasks (sequenced):**
Each task gets: files involved, step-by-step instructions with code, verification with expected output.

## Principles

- **DRY.** Don't repeat implementation across tasks. Extract shared utilities early.
- **YAGNI.** Don't plan features that aren't needed. If tempted to add "nice to have" tasks, cut them.
- **TDD sequence.** When tests are involved, plan the test FIRST, then the implementation. (See `references/tdd-discipline.md`.)
- **Frequent checkpoints.** Every 2-3 tasks, plan a verification point where the user can review progress.

## Adapting for chat context

In Claude Code, plans are saved as markdown files in the repo. In claude.ai chat, plans live in the conversation (or in a scratchpad artifact for complex work). The granularity and completeness standards are identical -- only the storage location differs.

For complex builds (5+ tasks), consider using a scratchpad artifact to track the plan and check off completed tasks. For simpler builds (2-3 tasks), stating the plan in chat is sufficient.

## When plans go wrong

**Plan gaps discovered mid-execution:** Stop. Update the plan. Don't improvise around the gap.

**Requirements changed:** Revisit the plan from the point of change. Don't just bolt new tasks onto the end if earlier tasks are now invalid.

**Plan is too ambitious:** Better to descope and deliver something complete than attempt everything and deliver nothing working. Propose the cut to the user.
