---
name: hermes-subagent-ios-swift
description: Spawn an iOS/Swift development delegate for app code, Xcode projects,
  TestFlight/App Store workflows, and SwiftUI/UIKit fixes.
version: 0.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags:
    - hermes
    - subagent
    - delegation
    - template
targets:
- hermes-default
- hermes-gpt
---

# hermes-subagent-ios-swift

## Trigger description
Load this skill when the parent Hermes agent should spawn a focused `ios_swift` delegate instead of doing all iOS/Swift development work in the main context.

## When to use
Use for SwiftUI/UIKit bugs, Xcode project config, signing diagnostics, App Store Connect/TestFlight prep, or iOS architecture review.

## Recommended delegate_task toolsets
- Primary: `['terminal', 'file', 'web']`
- Optional: add `browser` only for App Store Connect web UI.
- Add `file` only when the delegate must inspect or write local files.
- Add `terminal` only when shell commands materially improve verification.
- Avoid giving broad `hermes-cli` access unless the task truly needs it.

## Copyable delegate_task prompt template
```python
delegate_task(
    goal="Work on the iOS/Swift task in the given repo. Inspect project structure first, make targeted changes, prefer Swift-native patterns, run available builds/tests only if requested/cheap, and summarize files changed.",
    context="""
User/request: <paste the exact user ask>
Kosta-specific constraints: concise, technical, Telegram-friendly; avoid noisy tables unless fenced.
Known context: <paths, URLs, screenshots, constraints, prior findings, deadlines>
Definition of done: <what the parent needs back>
Do not assume parent conversation history; everything needed is in this context.

Return using the Output Contract below.
""",
    toolsets=['terminal', 'file', 'web']
)
```

## Output contract
Return a compact report with:
1. **Answer/result** — the direct conclusion or completed action.
2. **Evidence/actions** — links, commands, files inspected/changed, or UI steps.
3. **Recommendations/next steps** — only what matters.
4. **Issues/blockers** — uncertainty, missing access, or confirmation needed.

## Safety/confirmation rules
Confirm before changing signing/team IDs, bundle IDs, provisioning, submitting builds, bumping versions, or touching credentials.

## Pitfalls
Assuming Xcode CLI availability; broad project rewrites; ignoring deployment target; editing pbxproj blindly without validation.
