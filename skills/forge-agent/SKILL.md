---
name: forge-agent
description: >-
  Route work into the local Forge launcher when the user wants Forge to act as a
  planner, researcher, coder, reviewer, or validator instead of doing the work
  directly in the current agent session. Use whenever the user mentions Forge,
  forge-agent, forge-zsh, "run this in Forge", "send this off", "send this to a
  coding agent", "delegate this", "run this in another lane", "have Forge do
  it", "use Forge as the coder", "what Forge agents are available", or wants
  the exact Forge command to run. Do not use for ordinary direct edits in the
  current session unless the user specifically wants Forge involved.
metadata:
  author: Codex
  version: 1.3.0
---

# Forge Agent

Use this skill to launch or inspect the machine-local Forge workflow through the
`forge-agent` wrapper instead of improvising raw Forge commands.

This skill is most useful when the user wants a second execution lane:
- plan in Forge
- research in Forge
- implement in Forge
- validate or review through Forge
- inspect available Forge agents, tools, commands, or conversations

## When This Skill Should Win

Use this skill when the user:
- explicitly asks to use Forge, `forge-agent`, `forge-zsh`, or the Forge CLI
- wants to hand work off to a coding agent rather than doing it in the current session
- says things like "send this off", "delegate this", "run this in another lane", or "have Forge do it"
- asks what Forge modes, agents, profiles, tools, or commands are available
- wants a reusable or copyable command for launching Forge in the current repo
- wants to continue or inspect a Forge conversation

Prefer the current agent session instead when:
- the user just wants the task done here
- the work is a small direct edit and there is no reason to hand it off
- the user is asking about general shell or coding behavior unrelated to Forge
- the wording is just general implementation intent without any sign they want a second execution lane

## First Checks

Before recommending or launching anything, verify the local surface that is
actually available on the current machine:

```bash
command -v forge-agent
command -v forge
forge-agent info
forge agent list --porcelain
forge cmd list --porcelain
```

If interactive Zsh behavior matters, also verify:

```bash
bash -ic 'type forge-zsh && forge-zsh --version'
```

If `forge-agent` is missing but `forge` exists, explain that the wrapper is not
installed on this machine and either install it or fall back to raw Forge only
if the user wants that.

If neither `forge-agent` nor `forge` exists, say that Forge is not installed on
this machine and switch from launch advice to setup or installation guidance.

## Routing Guide

Choose the lightest Forge path that matches the job.

| User intent | Preferred command | Why |
|---|---|---|
| implement the task | `forge-agent code "..."` | uses the custom `kosta-coder` lane |
| write the plan only | `forge-agent plan "..."` | routes to the planning lane |
| analyze before changing | `forge-agent research "..."` | routes to the research lane |
| validate the current repo | `forge-agent check "..."` | uses the custom validation command |
| review for bugs and regressions | `forge-agent review "..."` | uses the custom review command |
| pick a specific Forge agent | `forge-agent run --agent <id> "..."` | explicit control without raw Forge |
| inspect agents, tools, or providers | `forge-agent list ...` or `forge-agent info` | safer than guessing |
| continue an existing session | `forge-agent resume` or `forge-agent resume <id>` | clear conversation handoff |
| stay inside Forge interactively | `forge-zsh` | launches the Zsh-native Forge shell |

## Safe Defaults

Use these defaults unless the user wants something else:

| Decision | Safe default | Convenience option | Recommendation |
|---|---|---|---|
| conversation start | fresh conversation | `--keep` | start fresh unless the user asks to continue |
| conversation reuse | `--conversation-id <id>` | latest-global reuse | prefer explicit ID when context isolation matters |
| launch style | one-shot `forge-agent ... "prompt"` | interactive `forge-zsh` | use one-shot for handoff, interactive only when the user wants to stay inside Forge |
| launcher surface | `forge-agent` | raw `forge` | prefer the wrapper unless the user explicitly wants raw Forge |

Do not promise per-run `--model` switching through `forge-agent`.
This wrapper rejects per-run `--model`; use Forge config, session commands, or
agent definitions when model selection needs to change.

## Examples

Keep `SKILL.md` focused on routing. For reusable launch recipes and copyable
examples, load [references/examples.md](references/examples.md) when the user
wants concrete command patterns.

## What To Tell The User

When explaining the setup, keep the distinction clear:
- `forge-agent` is the practical launcher for agent-style use
- `forge-zsh` is the interactive shell handoff for the full Zsh-native Forge UX
- `kosta-coder` is the custom implementation agent
- `check`, `code`, `plan-task`, `research`, and `review` are the custom Forge command surfaces

If the user asks which path to use, recommend:
- `forge-agent code` for most "go do the coding" requests
- `forge-agent plan` when they want planning delegated
- `forge-agent review` or `check` after implementation

## Verification

After changing this setup or relying on it heavily, verify with:

```bash
forge --version
forge-agent info
forge agent list --porcelain
forge cmd list --porcelain
forge-agent --print code "smoke test"
bash /Users/kosta/forge/tests/test_forge_agent.sh
```

## Troubleshooting

If Forge says the provider or model is not configured:
- run `forge-agent info`
- inspect `forge config list`
- confirm the expected provider endpoint is active

If `resume` or `--keep` picks up the wrong context:
- use `--conversation-id <id>` instead of the latest-global behavior

If the user wants the custom planning command rather than the built-in planning agent:
- use `forge cmd execute plan-task "..."` directly
