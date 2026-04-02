---
name: research-agent-protocol
user-invocable: false
description: |
  Protocol for spawning research sub-agents to verify API/SDK/library information before coding.
  Use when you need to check current versions, breaking changes, API signatures, or migration notes.
  Triggers: API lookup, SDK verification, library research, documentation check, version compatibility.
---

# Research Agent Protocol

## Purpose

Spawn research sub-agents to verify technical information while preserving main context. Research tasks consume significant tokens (web fetches, doc parsing, multiple sources). Offloading to a sub-agent keeps the main orchestrator lean.

## When to Use

- Before using any API you haven't verified this session
- When integrating a new library or SDK
- When unsure if your knowledge of an API is current
- When the user mentions a specific version
- When encountering unexpected API behavior

## Research Agent Prompt Template

Use this template when spawning a research sub-agent:

```
## Task: Research [Library/API Name]

### Deliverables
1. Current stable version number
2. API signatures for: [specific functions/methods needed]
3. Any breaking changes from version [X] to current
4. Migration notes if applicable
5. Official documentation links

### Scope
- Primary source: Official documentation
- Secondary: Release notes, changelogs
- Tertiary: Official GitHub repo issues/discussions
- Out of scope: Blog posts, Stack Overflow, tutorials

### Context
I need to use [specific functionality] in a [project type] project.
Current assumption: [what you think the API looks like]
Need to verify: [specific concerns]

### Report Format
Return findings as:

## Research Report: [Library/API]

### Version
Current stable: X.Y.Z
Verified from: [source link]

### API Signatures
```[language]
// Verified signatures for requested functions
```

### Breaking Changes
- [List any relevant breaking changes]
- [Or "None found since version X"]

### Migration Notes
[Any relevant migration guidance]

### Sources
- [Link 1]: [what was found there]
- [Link 2]: [what was found there]

### Confidence Level
[High/Medium/Low] — [reasoning]
```

## Handling Research Results

### If API is current (matches your understanding)
Proceed with implementation. No need to note changes.

### If API has changed
1. Update your approach to use current API
2. Explicitly note in your response:
   ```
   Note: Updated to current API. Previous approach used [old method],
   now using [new method] per [source].
   ```

### If research is inconclusive
1. Note the uncertainty
2. Use most recent reliable source
3. Flag in plan: "API info from [date], may need verification"
4. Consider asking user for clarification

## Sub-Agent Type

Use `subagent_type: "search-specialist"` or `subagent_type: "Explore"` depending on whether you need web search or codebase exploration.

For web research:
```
Task tool with subagent_type: "search-specialist"
```

For finding usage examples in codebase:
```
Task tool with subagent_type: "Explore"
```

## Example Usage

### Scenario: Need to use SwiftUI NavigationStack

**Spawn research agent:**
```
## Task: Research SwiftUI NavigationStack API

### Deliverables
1. Current API for NavigationStack in iOS 17/18
2. NavigationPath usage and initialization
3. navigationDestination modifier signatures
4. Any changes from iOS 16 to iOS 17/18

### Scope
- Primary: Apple Developer Documentation
- Secondary: WWDC session notes
- Out of scope: Third-party tutorials

### Context
Building navigation for iOS app. Need programmatic navigation with type-safe destinations.
Current assumption: NavigationStack takes a path binding and uses navigationDestination(for:destination:)
Need to verify: Exact signatures, any iOS 17+ changes

### Report Format
[Use standard report format above]
```

**Handle result:**
If research shows API changed, update approach and note:
```
Note: NavigationStack API verified for iOS 17. Using NavigationPath
with navigationDestination(for:destination:) as confirmed in Apple docs.
```

## Cost-Benefit Threshold

**Spawn research agent when:**
- Unfamiliar API (haven't used in 3+ months)
- User specified a version number
- API is known to change frequently
- High-stakes code (production, security-sensitive)

**Skip research when:**
- Just verified this session
- Very stable/unchanging API (e.g., basic Foundation types)
- User explicitly says "use version X" with confidence
- Simple, well-known patterns

## Integration with Planning

Research should happen during the **planning phase**, before writing the detailed plan:

```
1. Identify APIs/libraries needed
2. Spawn research agents for unfamiliar ones
3. Incorporate findings into plan
4. Present plan to user
5. Implement with verified information
```
