---
name: forge-sage
description: >-
  Use when the user specifically wants Sage, Forge Sage, or a read-only Forge
  investigation lane. Trigger on requests like "use sage", "forge sage",
  "have sage look at this", "trace this bug", "map this codepath", or "explain
  how this works in Forge". This skill is for Sage-only investigation and
  analysis, not implementation, review, or validation. Use forge-agent for the
  broader Forge router.
metadata:
  author: Codex
  version: 2.1.0
---

# Forge Sage

Use this skill when the main goal is to send **read-only investigation work**
into Forge's Sage lane.

This skill is intentionally narrow. It is for tracing behavior, mapping a
system, understanding architecture, isolating likely root causes, and answering
technical questions without making changes.

If the user wants implementation, planning, review, or validation, use
`forge-agent` instead.

## When This Skill Should Win

Use this skill when the user:
- explicitly says **sage** or **Forge Sage**
- wants a read-only investigation lane
- wants a codepath traced or a system explained
- wants likely root cause analysis before deciding on a fix
- wants a copyable Sage handoff for the current repo

Prefer `forge-agent` instead when:
- the task is mainly implementation
- the user wants a plan first
- the task is mainly code review or project validation
- the user wants general Forge routing rather than Sage specifically

## First Checks

Before recommending or launching Sage work, verify the local Forge surface:

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

If neither `forge-agent` nor `forge` exists, switch from Sage advice to setup
or installation guidance.

## Preferred Command

| Need | Preferred command | Why |
|---|---|---|
| read-only investigation | `forge-agent research "..."` | routes to Sage's investigation lane |
| inspect available capabilities | `forge-agent list agents` or `forge-agent info` | confirms what exists before recommending |

Important nuance: users may say **"use Sage"** or **"Forge Sage"** even though
the wrapper command still uses the verb `research`. Match the user's intent,
then use the command that reaches Sage.

## What A Good Sage Handoff Includes

Small prompts are fine for tiny, obvious questions. But for repo investigation,
Sage does better with **dense, relevant context**.

A strong handoff usually includes:
- **Context** — what this repo or subsystem is
- **Question** — what Sage needs to explain or trace
- **Read first** — files, docs, tests, or diffs that matter most
- **Focus** — the exact behavior, bug, or uncertainty to investigate
- **Output** — root cause, codepath map, architectural summary, file references

Do **not** pad the prompt with generic filler. Long is not the goal. Relevant
context is the goal.

## Default Brief Template

Use this structure when drafting a Forge Sage handoff:

```text
Context:
- What this project or subsystem is
- What behavior or bug is being investigated

Question:
- Exactly what Sage should explain, trace, or determine

Read first:
- Specific files, folders, docs, tests, or diffs

Focus:
- The exact path, state transition, or failure mode to investigate

Output:
- How findings should be formatted
- Whether to include likely root cause, open questions, and file references
```

## Safe Defaults

| Decision | Safe default | Recommendation |
|---|---|---|
| conversation reuse | fresh conversation | use `--conversation-id <id>` only when the user wants explicit continuity |
| launch style | one-shot `research` | prefer one-shot Sage handoffs over interactive Forge shells |
| launcher surface | `forge-agent` | prefer the wrapper over raw `forge` |
| prompt style | detailed but scoped | include project context, read-first files, and the exact investigation question |

Treat `--keep` as convenience only. It reuses the latest global Forge
conversation and is not repo-scoped.

## Bad vs Good Prompting

Bad:

```bash
forge-agent research "look into this"
```

Better:

```bash
forge-agent research --cwd /path/to/repo "
Trace the auth failure without making changes.

Context:
- This repo is a multi-service app with a web client and API backend.
- Users can sign in, but some requests fail after login.

Question:
- Where is auth state created, forwarded, and lost?

Read first:
- auth middleware
- route handlers
- the latest auth-related diff

Output:
- concise trace of the failure path
- likely root cause
- file references for each important finding
"
```

## Examples

For copyable examples, load [references/examples.md](references/examples.md).

## What To Tell The User

When explaining the setup:
- `forge-agent research` is the command that reaches Sage
- `forge-sage` should win only when the user wants Sage specifically
- `forge-agent` remains the broader router for planning, coding, Apple work,
  review, and validation

## Verification

After changing or relying on this setup, verify with:

```bash
forge-agent info
forge cmd list --porcelain
forge-agent --print research "trace the bug without making changes"
```

## Troubleshooting

If Forge picks up the wrong prior context:
- use `--conversation-id <id>` instead of relying on the latest-global behavior

If the user wants a broader Forge handoff rather than Sage-only investigation:
- switch back to `forge-agent`
