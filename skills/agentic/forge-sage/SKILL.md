---
name: forge-sage
description: >-
  Use when the user wants Forge Sage to investigate, review, audit,
  sanity-check, or validate code instead of implementing it. Trigger on requests
  like "use sage", "forge sage", "have sage look at this", "run this through
  Forge Sage", "have Forge review this", "delegate the review", "audit this
  change", or when the primary task is read-only investigation, post-change
  review, or validation. Do not use for implementation work; use forge-agent for
  broader Forge routing and coding handoffs.
metadata:
  author: Codex
  version: 2.0.0
---

# Forge Sage

Use this skill when the main goal is to send **read-heavy investigation, review, or validation work** into Forge with a strong brief.

The value here is not just remembering that Forge has `review`, `check`, or Sage-style investigation lanes. The value is packaging the task well enough that Forge starts with the right context, reads the right files, and returns a useful answer instead of a generic pass.

## When This Skill Should Win

Use this skill when the user:
- explicitly says **sage**, **Forge Sage**, or asks for a second read-only lane
- wants Forge to review, audit, sanity-check, or validate recent changes
- wants investigation rather than implementation
- wants a copyable, high-context Forge handoff for the current repo
- wants bug hunting, regression review, architectural tracing, or validation without changing files

Prefer `forge-agent` instead when:
- the user needs general Forge routing
- the task is mainly planning or implementation
- the user is exploring Forge capabilities rather than asking for a Sage-style investigation or review handoff

## First Checks

Before recommending or launching Sage work, verify the local Forge surface:

```bash
command -v forge-agent
command -v forge
forge-agent info
forge agent list --porcelain
forge cmd list --porcelain
```

If `forge-agent` is missing but `forge` exists, explain that the wrapper is not installed on this machine and either install it or fall back to raw Forge only if the user wants that.

If neither `forge-agent` nor `forge` exists, switch from Sage/review advice to setup or installation guidance.

## Pick the Right Forge Lane

| Need | Preferred command | Why |
|---|---|---|
| read-only investigation | `forge-agent research "..."` | routes to Sage's investigation lane |
| bug / regression review | `forge-agent review "..."` | purpose-built review lane |
| project validation | `forge-agent check "..."` | purpose-built validation lane |
| inspect available capabilities | `forge-agent list agents` or `forge-agent info` | confirms what exists before recommending |

Important nuance: users may say **"use Sage"** or **"Forge Sage"** even though some wrapper commands still use the verb `research`. Match the user's intent, then choose the correct Forge command.

## What A Good Sage Handoff Includes

Small prompts are fine for tiny, obvious tasks. But for repo investigation or code review, Forge does better with **dense, relevant context**.

A strong handoff usually includes:
- **Context** — what this repo or subsystem is
- **Scope** — what changed or what question needs answering
- **Read first** — files, docs, tests, or diffs that matter most
- **Focus** — bugs, regressions, architecture, performance, security, etc.
- **Ignore** — style nits, speculative refactors, unrelated cleanup
- **Output** — severity order, file references, concise vs exhaustive format

Do **not** pad the prompt with generic filler. Long is not the goal. Relevant context is the goal.

## Default Brief Template

Use this structure when drafting a Forge Sage handoff:

```text
Context:
- What this project or subsystem is
- What changed or what question is being investigated

Scope:
- Exactly what Sage should answer or review
- What is in bounds vs out of bounds

Read first:
- Specific files, folders, docs, tests, or diffs

Focus:
- The kinds of issues to look for

Ignore:
- What not to spend time on

Output:
- How findings should be formatted
- Whether to say "no substantive issues found" when clean
```

## Safe Defaults

| Decision | Safe default | Recommendation |
|---|---|---|
| conversation reuse | fresh conversation | use `--conversation-id <id>` only when the user wants explicit continuity |
| launch style | one-shot `research`, `review`, or `check` | prefer one-shot handoffs over interactive Forge shells |
| launcher surface | `forge-agent` | prefer the wrapper over raw `forge` |
| prompt style | detailed but scoped | include project context, scope boundaries, and output format |

Treat `--keep` as convenience only. It reuses the latest global Forge conversation and is not repo-scoped.

## Bad vs Good Prompting

Bad:

```bash
forge-agent review "review the latest change"
```

Better:

```bash
forge-agent review --cwd /path/to/repo "
Review the latest uncommitted change.

Context:
- This repo is a desktop agent app with workspace-scoped skills.
- The recent change touches Forge delegation guidance.

Read first:
- git diff --stat
- full git diff
- the affected SKILL.md files

Focus:
- incorrect guidance
- missing context that would cause weak delegated reviews
- broken references caused by renaming

Ignore:
- wording nits
- unrelated refactors

Output:
- list only substantive issues
- rank by severity
- include concrete replacement suggestions when useful
- say \"no substantive issues found\" if clean
"
```

## Examples

For copyable examples, load [references/examples.md](references/examples.md).

## What To Tell The User

When explaining the setup:
- `forge-agent research` is the Sage-style investigation lane
- `forge-agent review` is the review lane for bugs and regressions
- `forge-agent check` is the validation lane for project checks
- `forge-sage` should win when the user wants Sage/investigation/review behavior
- `forge-agent` remains the broader router for planning, coding, and general Forge use

## Verification

After changing or relying on this setup, verify with:

```bash
forge-agent info
forge cmd list --porcelain
forge-agent --print research "trace the bug without making changes"
forge-agent --print review "review the latest change for regressions"
forge-agent --print check "run validation for this project"
```

## Troubleshooting

If Forge picks up the wrong prior context:
- use `--conversation-id <id>` instead of relying on the latest-global behavior

If the user wants a broader Forge handoff rather than Sage/review-only routing:
- switch back to `forge-agent`
