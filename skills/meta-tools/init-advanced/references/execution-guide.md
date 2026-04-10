# Execution Guide

Use this file when the task needs the full workflow rather than the short dispatcher in
`SKILL.md`.

## Strategy Choice

Choose one path before drafting:

| Condition | Strategy |
|---|---|
| No usable instruction files exist | Fresh create |
| Existing files are stale, generic, or misleading | Rewrite |
| Monorepo packages differ materially in stack or workflow | Layered update |
| Existing files are mostly right and need tightening | Audit + patch |

When rewriting, re-verify every carried-forward command, path, and architectural claim.
For team-policy claims the repo cannot prove, ask the user before preserving them.

## Evidence Gate

Before drafting, try to inspect at least:

- one build or package manifest,
- one CI file or README,
- one representative source file or package-level README.

If one category does not exist, say so explicitly instead of inventing certainty.

## Drafting Rules

### For `AGENTS.md`

- Optimize for Codex/GPT behavior, not Claude behavior.
- Use direct scope limits and explicit approval boundaries.
- Distinguish what is always allowed, approval-gated, and never allowed.
- Prefer durable repo rules over long step-by-step workflows.

### For `CLAUDE.md`

- Keep it concise and practical.
- Prefer conditional guidance with rationale over heavy-handed emphasis.
- Name safer alternatives for hard prohibitions.
- Point to deeper docs instead of inlining long manuals.

## Confidence Labels

Use these labels only for claims that materially affect workflow or safety:

- `[verified]` for facts confirmed directly from the repo or user
- `[inferred]` for strong conclusions supported by multiple signals
- `[assumed]` for gaps that still need confirmation

## Placement Rules

- Single repo: write `AGENTS.md` and `CLAUDE.md` at repo root.
- Monorepo: add package-level files only when a package differs in at least two
  meaningful dimensions such as language, build system, test runner, deployment
  target, CI path, or risk constraints.
- If a package differs only slightly, keep the note in the root file instead.

## Clarifying Threshold

Ask follow-up questions only when:

- the user wants behavior the repo cannot imply,
- multiple contradictory workflows exist,
- existing files conflict with the requested direction,
- approval or destructive-action rules are unclear,
- the scope spans multiple subprojects with different owners.

Otherwise proceed from repo evidence.

## Anti-Patterns

Never:

- duplicate the same prose into both files,
- invent commands from framework stereotypes,
- infer architecture from directory names when files disagree,
- dump every discovered fact into the instruction files,
- turn `SKILL.md` into the full manual when `references/` can hold the detail.
