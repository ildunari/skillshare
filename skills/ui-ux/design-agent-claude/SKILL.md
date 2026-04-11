---
name: "Design Agent Claude"
description: "Run a focused UI polish or mockup-to-implementation pass through Claude Code using the custom subagent `design-agent-claude`. Default to Opus 4.6 with high effort; fall back to Sonnet 4.6 when Opus is unavailable or unnecessary."
alwaysAllow: ["Bash"]
---

# Design Agent Claude

Use this when you want Claude Code to handle a visual-first UI pass.

## Preferred agent
On Claude Code, prefer the custom subagent:

- `design-agent-claude`

## Model guidance
- Default: Opus 4.6 with high effort for ambiguous or high-stakes visual work.
- Fallback: Sonnet 4.6 when Opus is unavailable, rate-limited, or more power than the task needs.
- Claude Code treats `model` as preference rather than hard enforcement, so keep the prompt explicit when you really want Opus-first behavior.
- Inspect screenshots or real UI before making design claims.

## Recommended prompt shape
"Use design-agent-claude for a UI polish pass on <surface>. Inspect the current UI or screenshots first, state the design intent, make the smallest high-leverage improvements, then report visual QA findings, interaction QA findings, and remaining weaknesses."

## Output checklist
- Design intent summary
- Top UI/UX issues found
- Concrete changes recommended or applied
- Breakpoint and interaction QA notes
- Remaining risks / next pass
