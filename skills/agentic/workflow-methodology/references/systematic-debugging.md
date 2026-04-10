# Systematic debugging

> Adapted from `superpowers/skills/systematic-debugging` (SKILL.md, root-cause-tracing.md, defense-in-depth.md, condition-based-waiting.md). The most methodology-dense skill in the repo. Nearly everything is portable; only shell script paths and git-specific instrumentation stripped.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes. This is not optional. This is not flexible. "Quick fix first, investigate later" is the single most common failure mode.

## When to use this

Use for ANY technical issue: test failures, bugs, unexpected behavior, performance problems, build failures, integration issues.

Use this ESPECIALLY when under time pressure, when "just one quick fix" seems obvious, when you've already tried multiple fixes, or when you don't fully understand the issue.

## The four phases

Complete each phase before proceeding to the next.

### Phase 1: Root cause investigation

BEFORE attempting ANY fix:

**Read error messages carefully.** Don't skip past errors or warnings. They often contain the exact solution. Read stack traces completely. Note line numbers, file paths, error codes.

**Reproduce consistently.** Can you trigger it reliably? What are the exact steps? If not reproducible, gather more data -- don't guess.

**Check recent changes.** What changed that could cause this? Recent code, new dependencies, config changes, environmental differences.

**Gather evidence in multi-component systems.** When the system has multiple components (API → service → database, build → compile → bundle), add diagnostic instrumentation at each component boundary BEFORE proposing fixes. Log what enters and exits each component. Run once to gather evidence showing WHERE it breaks. THEN analyze evidence to identify the failing component. THEN investigate that specific component.

**Trace data flow backward.** When an error happens deep in execution: find where the bad value originates. What called this with the bad value? Keep tracing up the call chain until you find the source. Fix at the source, not at the symptom.

Root cause tracing example chain:
```
Error: git init failed in /Users/jesse/project/packages/core
  ← gitInit(directory) called with cwd = '' (empty string!)
    ← WorktreeManager.createSessionWorktree(projectDir='', sessionId)
      ← Session.initializeWorkspace()
        ← Session.create()
          ← test accessed context.tempDir before beforeEach populated it
Root cause: top-level variable initialization accessing empty value
```

Fix at the source (the test setup), not at the symptom (the git init call).

### Phase 2: Pattern analysis

**Find working examples.** Locate similar working code in the same codebase. What works that's similar to what's broken?

**Compare against references.** If implementing a pattern, read the reference implementation COMPLETELY. Don't skim. Understand the pattern fully before applying.

**Identify differences.** What's different between working and broken? List every difference, however small. Don't assume "that can't matter."

### Phase 3: Hypothesis and testing

**Form a single hypothesis.** State clearly: "I think X is the root cause because Y." Be specific, not vague.

**Test minimally.** Make the SMALLEST possible change to test the hypothesis. One variable at a time. Don't fix multiple things at once.

**Verify.** Did it work? Yes → Phase 4. Didn't work? Form NEW hypothesis. DON'T add more fixes on top.

### Phase 4: Implementation

**Create a failing test case.** Simplest possible reproduction. Automated if possible. MUST have before fixing.

**Implement a single fix.** Address the root cause identified. ONE change at a time. No "while I'm here" improvements. No bundled refactoring.

**Verify the fix.** Test passes now? No other tests broken? Issue actually resolved?

### The 3-fix escalation rule

**If 3+ fixes have failed: STOP fixing and question the architecture.**

Pattern indicating architectural problem:
- Each fix reveals new shared state / coupling / problem in a different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere

This is NOT a failed hypothesis. This is a wrong architecture. Discuss with the user before attempting more fixes.

## Defense-in-depth validation

When you fix a bug caused by invalid data, adding validation at one place feels sufficient. But that single check can be bypassed by different code paths, refactoring, or mocks.

**Principle:** Validate at EVERY layer data passes through. Make the bug structurally impossible.

| Layer | Purpose | Example |
|---|---|---|
| Entry point validation | Reject obviously invalid input at API boundary | `if (!dir) throw new Error('dir required')` |
| Business logic validation | Ensure data makes sense for this operation | Validate constraints before processing |
| Environment guards | Prevent dangerous operations in specific contexts | Refuse destructive ops outside test/temp dirs |
| Debug instrumentation | Capture context for forensics | Log + stack trace before risky operations |

Single validation: "We fixed the bug." Four layers: "We made the bug impossible."

## Condition-based waiting

Flaky behavior often comes from guessing at timing with arbitrary delays.

**Principle:** Wait for the actual condition you care about, not a guess about how long it takes.

```
Bad:  await sleep(500); const result = getResult();
Good: await waitFor(() => getResult() !== undefined);
```

| Scenario | Pattern |
|---|---|
| Wait for event | `waitFor(() => events.find(e => e.type === 'DONE'))` |
| Wait for state | `waitFor(() => state === 'ready')` |
| Wait for count | `waitFor(() => items.length >= 5)` |
| Complex condition | `waitFor(() => obj.ready && obj.value > 10)` |

Arbitrary timeout is ONLY correct when testing actual timing behavior (debounce, throttle). Always document WHY.

## Red flags -- STOP and return to Phase 1

If you catch yourself thinking any of these:

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- Proposing solutions before tracing data flow
- "One more fix attempt" (when already tried 2+)
- Each fix reveals a new problem in a different place

ALL of these mean: STOP. Return to Phase 1.

## Common rationalizations

| Excuse | Reality |
|---|---|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I see the problem, let me fix it" | Seeing symptoms does not equal understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question pattern, don't fix again. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
