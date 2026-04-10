---
name: forge-reviewer
description: >-
  Use when the user specifically wants Forge to review, audit, sanity-check, or
  validate code instead of implementing it. Trigger on requests like "have Forge
  review this", "run this through Forge reviewer", "use Forge to check for
  bugs", "delegate the review", "have the coding agent review the change", or
  when the primary task is post-implementation review rather than planning or
  coding. Do not use for general Forge routing when the task is not primarily a
  review or validation task; use forge-agent for that.
metadata:
  author: Codex
  version: 1.0.0
---

# Forge Reviewer

Use this skill when the main goal is to send review or validation work into
Forge, not to plan or implement changes.

## When This Skill Should Win

Use this skill when the user:
- explicitly asks Forge to review, audit, or check code
- wants a second lane focused on bugs, regressions, or validation
- says things like "have Forge review this", "run a Forge review", or "delegate the review"
- wants a copyable review or validation command for the current repo

Prefer `forge-agent` instead when:
- the user needs general Forge routing
- the task is mainly planning, coding, or research
- the user is exploring Forge capabilities rather than specifically asking for review

## First Checks

Before recommending or launching review work, verify the local Forge surface:

```bash
command -v forge-agent
command -v forge
forge-agent info
forge agent list --porcelain
forge cmd list --porcelain
```

If `forge-agent` is missing but `forge` exists, explain that the wrapper is not
installed on this machine and either install it or fall back to raw Forge only
if the user wants that.

If neither `forge-agent` nor `forge` exists, switch from review advice to setup
or installation guidance.

## Preferred Commands

| Review need | Preferred command | Why |
|---|---|---|
| bug and regression review | `forge-agent review "..."` | purpose-built review lane |
| project validation | `forge-agent check "..."` | purpose-built validation lane |
| inspect review-related capabilities | `forge-agent list agents` or `forge-agent info` | confirms what exists before recommending |

## Safe Defaults

| Decision | Safe default | Recommendation |
|---|---|---|
| review session reuse | fresh conversation | use `--conversation-id <id>` only when the user wants explicit continuity |
| review launch style | one-shot `forge-agent review` or `check` | prefer one-shot review handoff over interactive Forge shells |
| launcher surface | `forge-agent` | prefer the wrapper over raw `forge` |

Treat `--keep` as convenience only. It reuses the latest global Forge
conversation and is not repo-scoped.

## Examples

For copyable examples, load [references/examples.md](references/examples.md).

## What To Tell The User

When explaining the setup:
- `forge-agent review` is the review lane for bugs and regressions
- `forge-agent check` is the validation lane for running the right project checks
- `forge-reviewer` should win only when review is the primary task
- `forge-agent` remains the broader router for planning, coding, research, and general Forge use

## Verification

After changing or relying on this setup, verify with:

```bash
forge-agent info
forge cmd list --porcelain
forge-agent --print review "review the latest change"
forge-agent --print check "run validation"
```

## Troubleshooting

If Forge review picks up the wrong prior context:
- use `--conversation-id <id>` instead of relying on the latest-global behavior

If the user wants a broader Forge handoff rather than review-only routing:
- switch back to `forge-agent`
