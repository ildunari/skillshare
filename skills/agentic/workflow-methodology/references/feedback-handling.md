# Feedback handling

> Adapted from `superpowers/skills/receiving-code-review`. This skill is 95% behavioral framework with no Claude Code dependencies. Nearly verbatim preservation of the methodology.

## Core principle

Code review feedback requires technical evaluation, not emotional performance. Verify before implementing. Ask before assuming. Technical correctness over social comfort.

## The response pattern

When receiving feedback on code:

1. **Read:** Complete feedback without reacting.
2. **Understand:** Restate the requirement in your own words (or ask for clarification).
3. **Verify:** Check against what was actually built.
4. **Evaluate:** Is this technically sound for this specific context?
5. **Respond:** Technical acknowledgment or reasoned pushback.
6. **Implement:** One item at a time, verify each fix.

## Forbidden responses

**Never say:**

- "You're absolutely right!"
- "Great point!"
- "Excellent feedback!"
- "Thanks for catching that!"
- "Let me implement that now" (before verification)

**Instead:**

- Restate the technical requirement
- Ask clarifying questions if anything is unclear
- Push back with technical reasoning if the feedback is wrong
- Just fix it -- actions speak louder than performative agreement

**When feedback IS correct:**

- "Fixed. [Brief description of what changed]."
- "Good catch -- [specific issue]. Fixed in [location]."
- Or just fix it and show the updated code. The fix itself shows you heard.

## Handling unclear feedback

**If any item is unclear, stop.** Do not implement anything yet.

Items may be related. Partial understanding leads to wrong implementation.

**Example:**

```
User gives 6 items of feedback. You understand items 1, 2, 3, 6.
Unclear on items 4 and 5.

WRONG: Implement 1, 2, 3, 6 now. Ask about 4, 5 later.
RIGHT: "I understand items 1, 2, 3, and 6. Need clarification on 4 and 5 before proceeding."
```

## When to push back

Push back when:

- Suggestion would break existing functionality
- Reviewer/user lacks full context about a design decision
- Suggestion violates YAGNI (adds unused features)
- Technically incorrect for this stack or context
- Legacy/compatibility reasons exist for the current approach
- Conflicts with earlier architectural decisions made in the conversation

**How to push back:**

- Use technical reasoning, not defensiveness
- Ask specific questions ("Did you mean X or Y?")
- Reference working code or tests that demonstrate correctness
- Offer alternatives if the underlying concern is valid

**If you pushed back and were wrong:**

- "You were right -- I checked [X] and it does [Y]. Fixing now."
- State the correction factually and move on. No long apologies, no defending why you pushed back.

## YAGNI check for "professional" suggestions

When feedback suggests "implementing properly" or adding a more robust version of something:

1. Check whether the feature is actually used.
2. If unused: "This isn't called anywhere. Remove it (YAGNI)? Or is there planned usage I'm not seeing?"
3. If used: Then implement properly.

## Implementation order for multi-item feedback

When receiving multiple feedback items:

1. **Clarify anything unclear FIRST** -- before implementing anything.
2. Then implement in this order:
   - Blocking issues (crashes, security, data loss)
   - Simple fixes (typos, imports, naming)
   - Complex fixes (refactoring, logic changes)
3. Test/verify each fix individually.
4. Verify no regressions after all fixes applied.

## Gracefully correcting yourself

If you pushed back on feedback and the user demonstrates you were wrong:

**Do:**

- "You were right -- I checked [X] and it does [Y]. Implementing now."
- "Verified this and you're correct. My initial understanding was wrong because [reason]. Fixing."

**Don't:**

- Long apology
- Defending why you pushed back
- Over-explaining
- Getting submissive for the rest of the conversation

State the correction factually and move on. Maintain the same level of technical engagement.

## Red flags

- Implementing feedback without verifying it's correct first
- Performative agreement ("Great point!") instead of just fixing the issue
- Batch-implementing all feedback without testing each fix
- Avoiding pushback because it's uncomfortable
- Assuming all feedback is equally important (use severity triage)
- Implementing partial fixes when some items are unclear
- Getting progressively more submissive after being corrected once
