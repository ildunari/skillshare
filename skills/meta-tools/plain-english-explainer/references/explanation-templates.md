# Explanation Templates

Pre-built structures for common scenarios. Pick the template that matches the situation, then fill it in using the translation rules from SKILL.md.

## Template 1: Bug Fix

```markdown
## Plain English Summary

### What just happened
I found and fixed a bug in [specific file/feature]. The issue was [one-sentence plain description].

### What was going wrong
[Analogy-based explanation of the bug. Use a real-world comparison.]

Think of it like this: [extended analogy that makes the mechanism click].

### What I changed
- In [filename]: [what the change does in plain English, not what the code says]
- [Additional changes if any]

### The situation right now
[What works now that didn't before. What the user can go test.]

### Things to keep in mind
[Any related fragility, edge cases, or "this might come back if..." warnings]
```

## Template 2: New Feature / Code Addition

```markdown
## Plain English Summary

### What just happened
I added [feature name] to the app. Here's what it does and how it fits in.

### How it works (the simple version)
[Walk through what happens from the user's perspective, step by step.]

1. When the user [action]...
2. The app [response]...
3. Behind the scenes, [what the code does, in analogy terms]...
4. The result: [what appears/changes on screen]

### Where it lives
- [filename] — this is the [what it does, not what it is]
- [filename] — this handles [responsibility in plain terms]

### What I recommend testing
[Specific things to click/try to verify it works]

### What this doesn't handle (yet)
[Scope boundaries — what's deliberately left out and why]
```

## Template 3: Error / Something Broke

```markdown
## Plain English Summary

### What's happening
[Plain description of the symptom — what the user sees or experiences]

### Why it's happening
[Root cause in analogy terms. Start with the simplest accurate explanation.]

Imagine [analogy]. That's essentially what's happening here: [connect analogy to the actual problem].

### What our options are

**Option A: [Name the approach]**
[What we'd do, what it fixes, what the tradeoff is]
- Upside: [benefit in user-facing terms]
- Downside: [cost in user-facing terms]
- Time: [rough estimate]

**Option B: [Name the approach]**
[Same structure]

**Option C: [Name the approach, if applicable]**
[Same structure]

### What I recommend
I'd go with **Option [X]** because [reason tied to the user's specific situation, not abstract best practices].

[If applicable: "Before I proceed, I need you to [decision/approval/info]."]
```

## Template 4: Architecture / Pipeline Explanation

```markdown
## Plain English Summary

### The big picture
[One paragraph explaining what this system does and why it exists. Frame it as a problem being solved.]

### How the pieces fit together
Think of it like [overarching analogy]:

1. **[Component name] → [What it does]**
   This is like the [analogy role]. It takes [input in plain terms] and produces [output in plain terms].

2. **[Component name] → [What it does]**
   [Same pattern. Keep the analogy family consistent.]

3. **[Continue for each major piece]**

### Where our issue is
The problem is in step [N] — the [component name]. Specifically: [plain description of what's going wrong in that piece].

### What this means for the app
[Connect the technical issue to user-facing impact: speed, reliability, correctness, cost]
```

## Template 5: "What Should We Do Next?" (Decision Point)

```markdown
## Plain English Summary

### Where we are
[Current state of the project/feature. What's done, what's not.]

### The decision we need to make
[Frame the fork in the road clearly]

### The options

| Approach | What it means | Best for | Risk |
|---|---|---|---|
| [Option A] | [Plain description] | [When this is the right call] | [What could go wrong] |
| [Option B] | [Plain description] | [When this is the right call] | [What could go wrong] |
| [Option C] | [Plain description] | [When this is the right call] | [What could go wrong] |

### My recommendation
[Pick one. Say why. Be specific to the user's situation.]

### What I need from you to proceed
[Clear, actionable ask — a decision, a file, access to something, a preference]
```

## Template 6: Quick Fix (Minimal)

For trivial changes that don't need a full writeup.

```markdown
## Quick Summary
[1-2 sentences: what was wrong, what I did, it's fixed now. Done.]
```

## Choosing the Right Template

| Situation | Template |
|---|---|
| Fixed a bug | Bug Fix |
| Added new functionality | New Feature |
| Something is broken and we need to decide how to fix it | Error / Something Broke |
| User asks "what does this system/pipeline/flow do?" | Architecture / Pipeline |
| We've hit a fork and need user input | Decision Point |
| Typo fix, config tweak, one-liner | Quick Fix |
| Multiple situations at once | Combine relevant sections from multiple templates |
