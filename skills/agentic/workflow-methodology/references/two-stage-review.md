# Two-stage self-review

> Adapted from `superpowers/skills/subagent-driven-development` (spec-reviewer-prompt.md, code-quality-reviewer-prompt.md, implementer-prompt.md). Original skill dispatches separate reviewer subagents for each stage. This adaptation internalizes both review stages as a self-review discipline after writing code.

## Core principle

After writing code, review it in two distinct passes with different lenses. Don't conflate "did I build the right thing" with "is it built well."

**Order matters:** Spec compliance first, THEN code quality. There's no point polishing code that doesn't meet requirements.

## Stage 1: Spec compliance review

**The question:** Did I build exactly what was asked? Nothing missing, nothing extra.

### The adversarial lens

The original superpowers prompt says: "The implementer finished suspiciously quickly. Their report may be incomplete, inaccurate, or optimistic. You MUST verify everything independently."

Applied to self-review, this means: don't trust your own sense of completion. Re-read the requirements, then re-read your code, and compare line by line.

### Checklist

**Missing requirements:**

- Did I implement everything that was requested?
- Are there requirements I skipped or missed?
- Did I claim something works but didn't actually implement it?
- Are there edge cases the requirements imply but don't state?

**Extra / unneeded work:**

- Did I build things that weren't requested?
- Did I over-engineer or add unnecessary features?
- Did I add "nice to haves" that weren't in spec?
- Does anything violate YAGNI?

**Misunderstandings:**

- Did I interpret requirements differently than intended?
- Did I solve the wrong problem?
- Did I implement the right feature but the wrong way?

### Verdict

- **Pass:** Everything matches. Move to Stage 2.
- **Fail:** List specifically what's missing or extra. Fix before proceeding.

## Stage 2: Code quality review

**The question:** Assuming it meets spec, is it well-built?

**Only run this after spec compliance passes.** Wrong order = wasted effort polishing wrong code.

### Five-category checklist

| Category | Questions to ask |
|---|---|
| **Code quality** | Clean separation of concerns? Proper error handling? Type safety? DRY principle followed? Edge cases handled? Names clear and accurate? |
| **Architecture** | Sound design decisions? Scalability considerations? Performance implications? Security concerns? |
| **Testing** | Tests actually test logic (not just mocks)? Edge cases covered? Integration tests where needed? All tests passing? |
| **Requirements** | All plan requirements met? (redundant with Stage 1 but a good sanity check) No scope creep? Breaking changes documented? |
| **Production readiness** | Backward compatibility? Documentation? No obvious bugs? Migration strategy if needed? |

### Severity triage

Every issue found gets categorized:

| Severity | Definition | Action |
|---|---|---|
| **Critical** | Bugs, security issues, data loss risks, broken functionality | Must fix before presenting |
| **Important** | Architecture problems, missing error handling, test gaps, poor patterns | Should fix before presenting |
| **Minor** | Code style, optimization opportunities, documentation improvements | Note for later or mention to user |

## Stage 0: Implementer self-review (pre-review)

Before running the two formal stages, do a quick sanity pass. This catches the obvious stuff:

**Completeness:** Did I fully implement everything? Miss any requirements? Unhandled edge cases?

**Quality:** Is this my best work? Are names clear and accurate (describe what things do, not how they work)?

**Discipline:** Did I avoid overbuilding (YAGNI)? Only build what was requested? Follow existing patterns?

**Testing:** Do tests verify actual behavior (not just mock behavior)?

If this pre-review finds issues, fix them now. Don't pass garbage to the formal review stages.

## How to apply in practice

### For substantial code (artifacts, multi-file builds, complex scripts)

Run all three stages explicitly. The output should feel tight and verified.

### For quick code (snippets, one-off helpers, casual responses)

Run Stage 0 (quick sanity) silently. Skip formal stages unless the code is tricky.

### For iterative builds (multiple rounds of feedback)

Run full review on the first pass. On subsequent iterations, focus the review on what changed.

## What this looks like in chat

**Silent review (default):** I run the review internally and present clean output. The user sees the result, not my review process.

**Explicit review (when asked, or when issues found):** I report findings using the structured format from `references/code-review-checklist.md` -- strengths, issues by severity, verdict.

## Verification discipline

> Merged from `superpowers/skills/verification-before-completion`. These rules apply after EVERY change, not just at the end.

**After every fix or implementation:**

- Re-run verification. Don't assume it still works because it worked before the change.
- Verify the fix didn't break adjacent functionality. Check related tests, not just the one you were fixing.
- "Actually run the test" -- not "it should work." Running it takes seconds. Guessing takes hours when you're wrong.
- If you can't verify (no test runner, no browser preview), explicitly state what you couldn't verify and why.

**Before declaring anything complete:**

- Re-read the original requirements one more time
- Compare what was requested to what was built (not what you think you built)
- Run ALL relevant tests, not just the ones you think are affected
- Check for regressions in functionality that was working before

## Red flags

- Skipping spec compliance and jumping straight to code quality
- Trusting my own summary of what I built instead of re-reading the code
- Declaring "looks good" without actually checking each requirement
- Marking everything as Critical (severity inflation)
- Marking nothing as Critical when there are real bugs (severity deflation)
- Skipping review because "it's simple" -- simple code can still miss requirements
- Saying "it should work" instead of actually verifying
- Verifying only the changed code, not adjacent functionality
- Declaring done without re-reading the original requirements
