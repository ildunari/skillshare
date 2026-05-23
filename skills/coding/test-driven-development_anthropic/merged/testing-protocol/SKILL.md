---
name: testing-protocol
user-invocable: false
description: |
  Protocol for TDD workflow and comprehensive testing including browser-based verification.
  Use when implementing features, fixing bugs, or verifying changes work correctly.
  Triggers: testing, TDD, test first, verify, browser testing, screenshot, console check.
---

# Testing Protocol

## Purpose

Ensure code changes work correctly through:
1. **TDD (Test-Driven Development)** — Write tests before implementation
2. **Automated verification** — Run test suites
3. **Browser verification** — Visual and functional checks for UI changes

## TDD Workflow

### Standard Sequence

```
1. Write failing test   →  Captures expected behavior
2. Run test (red)       →  Confirms test catches the issue
3. Implement change     →  Minimal code to pass
4. Run test (green)     →  Confirms implementation works
5. Run full suite       →  Ensures no regressions
6. Refactor if needed   →  Clean up with test safety net
```

### When to Apply TDD

**Always use TDD for:**
- Bug fixes (test proves the bug, then proves the fix)
- New features (test defines expected behavior)
- Refactors (tests ensure behavior unchanged)
- Edge case handling (test each edge case explicitly)

**TDD optional for:**
- Pure UI styling changes (use browser verification instead)
- Config changes (verify differently)
- Documentation

---

## Test Writing Guidelines

### Bug Fix Test Pattern

```swift
// Swift example
func test_handleSubmit_whenUserIsNil_shouldNotCrash() {
    // Arrange
    let viewModel = SubmitViewModel(user: nil)

    // Act & Assert - should not throw
    XCTAssertNoThrow(viewModel.handleSubmit())
}
```

```typescript
// TypeScript example
it('should not crash when user is undefined', () => {
    const viewModel = new SubmitViewModel(undefined);
    expect(() => viewModel.handleSubmit()).not.toThrow();
});
```

### Feature Test Pattern

```swift
func test_calculateTotal_withDiscountCode_shouldApplyDiscount() {
    // Arrange
    let cart = ShoppingCart(items: [item1, item2])
    let discountCode = "SAVE20"

    // Act
    let total = cart.calculateTotal(discountCode: discountCode)

    // Assert
    XCTAssertEqual(total, expectedDiscountedTotal)
}
```

### Edge Case Test Pattern

```swift
func test_parseInput_withEmptyString_shouldReturnEmptyResult() {
    let result = parser.parse("")
    XCTAssertTrue(result.isEmpty)
}

func test_parseInput_withMalformedData_shouldThrowParseError() {
    XCTAssertThrowsError(try parser.parse("{{invalid}}")) { error in
        XCTAssertTrue(error is ParseError)
    }
}
```

---

## Browser Verification Checklist

When changes affect UI, verify in browser using available tools:

### After Visual Changes

- [ ] **Take screenshot** — Capture the current state
  - Use browser tools to screenshot the affected area
  - Compare with expected design if available

- [ ] **Check multiple states**
  - Loading state
  - Empty state
  - Error state
  - Success state
  - Edge cases (long text, missing images, etc.)

### After Functional Changes

- [ ] **Run through user flows**
  - Complete the primary user journey
  - Test alternate paths
  - Test error paths

- [ ] **Check console for errors**
  - No JavaScript errors
  - No failed network requests
  - No deprecation warnings (unless expected)

- [ ] **Check network tab**
  - Requests completing successfully
  - Response data correct
  - No unexpected requests
  - Appropriate status codes

### Accessibility Checks

- [ ] **Keyboard navigation** — Can complete flow with keyboard only
- [ ] **Screen reader** — Labels and announcements make sense
- [ ] **Color contrast** — Text readable in all themes
- [ ] **Dynamic type** — UI adapts to text size changes (iOS/macOS)

---

## Browser Tool Integration

### Available Browser Tools

Depending on your MCP setup, you may have access to:

```
browsertools MCP server:
- takeScreenshot — Capture current page state
- getConsoleLogs — Retrieve JavaScript console output
- getNetworkLogs — Retrieve network request/response logs
- runSEOAudit — Check accessibility and SEO issues

playwright MCP server:
- browser_navigate — Navigate to URL
- browser_click — Click elements
- browser_type — Enter text
- browser_screenshot — Take screenshots
```

### Screenshot Verification Flow

```
1. Make UI changes
2. Build/refresh the app
3. Navigate to affected screen
4. Take screenshot: mcp__browsertools__takeScreenshot
5. Review screenshot for correctness
6. If issues found, fix and repeat
```

### Console Check Flow

```
1. Navigate to affected page
2. Perform the user action
3. Check console: mcp__browsertools__getConsoleLogs
4. Verify no errors
5. If errors found, investigate and fix
```

### Network Check Flow

```
1. Clear network logs
2. Perform the action that triggers requests
3. Check network: mcp__browsertools__getNetworkLogs
4. Verify:
   - Correct endpoints called
   - Successful status codes
   - Expected response data
```

---

## Test Reporting Format

After running tests, report:

```markdown
## Test Results

### Tests Run
| Test Suite | Tests | Passed | Failed |
|------------|-------|--------|--------|
| Unit Tests | 45 | 45 | 0 |
| Integration | 12 | 11 | 1 |

### Failures
```
test_integration_userFlow_checkout (FAILED)
  Expected: Order confirmation screen
  Actual: Error screen with "Payment failed"

  Stack trace:
  ...
```

### Coverage
- Lines: 85%
- Branches: 72%
- New code: 100%

### Browser Verification
- [x] Screenshot captured — UI matches design
- [x] User flow completed successfully
- [x] No console errors
- [x] Network requests successful
```

---

## Test Commands by Platform

### Swift (Xcode)

```bash
# Run all tests
xcodebuild test -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 15'

# Run specific test
xcodebuild test -scheme MyApp -only-testing:MyAppTests/AuthTests/test_login
```

### JavaScript/TypeScript

```bash
# Jest
npm test
npm test -- --watch
npm test -- path/to/specific.test.ts

# Vitest
npm run test
npm run test:coverage
```

### Python

```bash
# pytest
pytest
pytest -v tests/test_specific.py
pytest --cov=src
```

---

## Common Testing Mistakes

1. **Testing after implementation** — Misses the "red" phase, may write tests that can't fail
2. **Testing implementation, not behavior** — Tests break on refactor
3. **Skipping edge cases** — Happy path only, bugs in edge cases
4. **No browser verification for UI** — "Works in tests" but broken visually
5. **Ignoring flaky tests** — Flaky = bug in test or code
6. **Over-mocking** — Tests pass but real integration fails

---

## Integration with Other Protocols

- **Planning Protocol**: Include test strategy in implementation plan
- **Orchestration Guide**: Spawn test-automator agent for comprehensive test creation
- **Error Handling**: When tests fail, follow error handling protocol (analyze, plan, fix, verify)

---

## Verification Sign-off

Before marking implementation complete:

```markdown
## Verification Complete

- [x] Wrote tests before implementation
- [x] All new tests passing
- [x] Full test suite passing (no regressions)
- [x] Browser verification complete (if UI)
- [x] Edge cases covered
- [x] No console errors
- [x] No network failures
```
