# TDD discipline

> Adapted from `superpowers/skills/test-driven-development`. The red-green-refactor cycle, anti-patterns, and rationalizations table are the valuable methodology. Stripped: git commit per cycle, npm-specific commands (generalized), skill invocation syntax.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

If you didn't watch the test fail, you don't know if it tests the right thing.

**Wrote code before the test?** Delete it. Start over. Not "keep as reference." Not "adapt while writing tests." Delete means delete.

## Red-green-refactor

### RED -- Write failing test

Write one minimal test showing what should happen.

**Good test:** Clear name describing behavior, tests real code (not mocks), tests ONE thing.

```
test('rejects empty email with descriptive error', async () => {
  const result = await submitForm({ email: '' });
  expect(result.error).toBe('Email required');
});
```

**Bad test:** Vague name, tests mock behavior, tests multiple things.

```
test('form works', async () => {
  // Tests mock, not real code
  // Name tells you nothing
  // Multiple assertions testing different behaviors
});
```

### VERIFY RED -- Watch it fail

**Mandatory. Never skip.** Confirm: test FAILS (not errors), failure message is what you expect, fails because the feature is missing (not because of typos).

Test passes immediately? You're testing existing behavior. Fix the test.

### GREEN -- Minimal code

Write the SIMPLEST code to make the test pass. Don't add features, don't refactor other code, don't "improve" beyond what the test requires.

### VERIFY GREEN -- Watch it pass

**Mandatory.** Confirm: test passes, other tests still pass, no warnings or errors.

### REFACTOR -- Clean up (only after green)

Remove duplication, improve names, extract helpers. Keep tests green throughout. Don't add behavior during refactoring.

### Repeat

Next failing test for the next behavior.

## Testing anti-patterns

| Anti-pattern | Why it's bad | What to do instead |
|---|---|---|
| Testing mock behavior instead of real behavior | Proves mocks work, not your code | Use real implementations; mock only external services (network, database) |
| Writing code before tests | Test passes immediately, proving nothing | Delete the code. Write the test first. |
| Not watching the test fail | No proof the test catches the bug | Always run and see the failure before implementing |
| Vague test names (`test1`, `it works`) | Can't understand what's tested without reading the body | Name describes the specific behavior: "rejects empty email with error message" |
| "and" in test name | Testing multiple things = unclear what broke | Split into separate tests, one behavior each |
| Test setup larger than the test | Complexity hides what's actually being tested | Extract helpers. If still complex, the design needs simplifying. |
| Mocking everything | Tests prove nothing about real behavior | Dependency injection for external services only |
| Testing implementation details | Tests break on refactoring even when behavior is unchanged | Test public interface and observable behavior, not internal state |

## Common rationalizations

| Excuse | Reality |
|---|---|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after ask "what does this do?" Tests-first ask "what SHOULD this do?" |
| "Already manually tested" | Ad-hoc is not systematic. No record, can't re-run. |
| "Deleting X hours of work is wasteful" | Sunk cost fallacy. Keeping unverified code is tech debt. |
| "Keep as reference, write tests first" | You'll adapt it. That's testing after in disguise. Delete means delete. |
| "Need to explore first" | Fine. Throw away the exploration. Start fresh with TDD. |
| "Test hard = skip test" | Hard to test = hard to use. Listen to the test -- simplify the design. |
| "TDD will slow me down" | TDD is faster than debugging. First-time fix rate: ~95% vs ~40%. |
| "This is different because..." | No it isn't. |

## When to apply in chat context

**Full TDD cycle:** When building artifacts with logic, React components with state management, utilities, data processing code. Write the test (or describe the expected behavior), then implement.

**TDD-informed thinking:** When writing any code, mentally ask "how would I test this?" If the answer is "I can't easily," the design needs rethinking.

**Skip TDD when:** Throwaway prototypes, pure UI styling changes, configuration, or when the user explicitly says to skip it. But even then, apply the anti-patterns awareness.

## Debugging integration

Bug found? Write a failing test that reproduces it. Follow the TDD cycle. The test proves the fix works AND prevents regression.

Never fix bugs without a test.
