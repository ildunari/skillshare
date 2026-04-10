# Code review checklist

> Adapted from `superpowers/skills/requesting-code-review/code-reviewer.md`. Original template is used by reviewer subagents comparing git diffs. This adaptation is a structured rubric for reviewing code in Claude.ai chat -- either the user's code or my own output.

## When to use this checklist

- User pastes code and asks for review
- User asks "what's wrong with this"
- I'm reviewing my own output on a complex build (per two-stage review)
- Before presenting a substantial artifact or code file
- User asks for feedback on architecture or approach

## The review rubric

### Code quality

- Clean separation of concerns?
- Proper error handling? (not just happy path)
- Type safety where applicable?
- DRY principle followed? (but not over-abstracted)
- Edge cases handled?
- Names are clear and describe *what things do*, not *how they work*?

### Architecture

- Sound design decisions for the scale of the problem?
- Scalability considerations (if relevant)?
- Performance implications? (O(n^2) loops, unnecessary re-renders, etc.)
- Security concerns? (injection, XSS, auth bypasses, secrets in code)

### Testing

- Tests actually verify behavior, not just mock behavior?
- Edge cases covered?
- Integration tests where needed?
- All tests passing?
- Tests are readable and serve as documentation?

### Requirements

- All stated requirements met?
- Implementation matches spec?
- No scope creep (extra features nobody asked for)?
- Breaking changes documented?

### Production readiness

- Backward compatibility considered?
- Documentation where needed?
- No obvious bugs?
- Migration strategy if schema/API changes?
- Error messages are helpful to the end user?

## Output format

When presenting a code review (explicit review, not silent self-review), use this structure:

```
### Strengths
[What's well done -- be specific, cite locations]

### Issues

#### Critical (must fix)
[Bugs, security issues, data loss risks, broken functionality]
Each: what's wrong, why it matters, how to fix

#### Important (should fix)
[Architecture problems, missing features, poor error handling, test gaps]
Each: what's wrong, why it matters, how to fix

#### Minor (nice to have)
[Code style, optimization opportunities, documentation]

### Assessment
Ready to use? [Yes / No / With fixes]
Reasoning: [1-2 sentences]
```

## Severity calibration

Getting severity right matters. Inflation ("everything is Critical") desensitizes. Deflation ("nothing is Critical") misses real problems.

| Severity | Threshold | Examples |
|---|---|---|
| **Critical** | Will cause incorrect behavior, data loss, security vulnerability, or crash in normal use | Unhandled null that crashes on valid input; SQL injection; auth bypass; infinite loop; data corruption |
| **Important** | Will cause problems under likely conditions or makes the code significantly harder to maintain | Missing error handling on API calls; no input validation; O(n^2) on large datasets; no tests for core logic; tight coupling |
| **Minor** | Cosmetic, stylistic, or optimization that doesn't affect correctness | Inconsistent naming; could use a constant instead of magic number; missing JSDoc; unused import |

## Rules for giving review

**Do:**

- Categorize by actual severity (not everything is Critical)
- Be specific -- cite locations, not vague concerns
- Explain WHY issues matter (not just what's wrong)
- Acknowledge strengths (what's done well)
- Give a clear verdict

**Don't:**

- Say "looks good" without checking
- Mark nitpicks as Critical
- Give feedback on code you didn't actually read
- Be vague ("improve error handling" -- where? how?)
- Avoid giving a clear verdict
- Pile on Minor issues when there are Critical ones to address

## Adapting for context

**Quick review (user asks "does this look right"):** Scan for Critical/Important only. Skip Minor unless pattern is pervasive. Keep it concise.

**Deep review (user asks for thorough review):** Full rubric, all severity levels, specific references, detailed suggestions.

**Self-review (internal, before presenting output):** Focus on Critical and Important. Fix before presenting. Don't report Minor issues to the user unless they asked for a review.
