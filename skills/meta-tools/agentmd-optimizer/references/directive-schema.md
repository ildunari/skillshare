# Directive Schema

The optimizer should reason about files at the level of **discrete directives**, not just token counts.

## Concept

A directive is one actionable behavioral instruction, preference, or prohibition.

Examples:
- "Before creating files, check whether a similar file already exists."
- "Prefer CLI over SSH over MCP wrappers."
- "Do not store secrets in memory."

## Suggested fields

```json
{
  "directive_id": "d-014",
  "file": "/path/to/CLAUDE.md",
  "runtime": "claude-code",
  "scope": "project-local",
  "category": "workflow",
  "strength": "conditional",
  "text": "Before creating files, check whether a similar file already exists."
}
```

## Why this matters

Directive-level analysis enables:
- instruction-count estimates
- duplicate policy detection
- contradiction detection
- extraction candidates
- better estimates for the 150–200 instruction attention ceiling

## Categories to use

Suggested first-pass categories:
- workflow
- validation
- tools
- response-style
- security
- git
- general

## Strength levels

Suggested first-pass strength labels:
- **hard** — MUST / NEVER / ALWAYS / CRITICAL style rules
- **conditional** — When X, do Y / Prefer X / Avoid Y
- **normal** — neutral guidance without strong emphasis
