---
name: forge-agent
description: >-
  Delegate coding, planning, or research tasks to the ForgeCode AI agent via
  the forge-agent wrapper or raw forge CLI. Use whenever the user mentions Forge,
  forge-agent, "run this in Forge", "send this off", "delegate this", "run this
  in another lane", "have Forge do it", "use Forge as the coder", or wants work
  done by a separate coding agent instead of the current session. Also use when
  asking about available Forge agents, modes, or capabilities. Do not use for
  ordinary edits in the current session unless the user specifically wants Forge.
metadata:
  author: Codex
  version: 2.0.0
---

# Forge Agent

Delegate work to ForgeCode — a separate AI coding agent with its own context,
tools, and conversation state. Forge runs in the terminal and has full
read/write file access, shell execution, and web fetch.

## Three Agents

Forge has three specialized agents. Pick the right one for the job:

| Agent | What it does | When to use |
|---|---|---|
| **forge** (kosta-coder) | Implements code — edits files, runs commands, builds features | "Go build this", "fix this bug", "refactor this module" |
| **muse** | Plans and analyzes — produces implementation plans, scopes work | "Plan this refactor", "what's the best approach", "scope this out" |
| **sage** | Investigates read-only — traces bugs, maps architecture, answers questions | "How does this work", "trace this bug", "explain the auth flow" |

The natural workflow is **muse -> forge**: plan first, then implement.
Sage is also used internally by the other two when they need to research.

## Quick Reference

**One-shot delegation** (most common from Hermes):
```bash
forge-agent code "implement the auth middleware"
forge-agent plan "plan the database migration for v2"
forge-agent research "trace how errors propagate through the pipeline"
forge-agent check "validate the repo is in good shape"
forge-agent review "review recent changes for bugs and regressions"
```

**With options:**
```bash
forge-agent code --cwd /path/to/repo "fix the failing tests"
forge-agent code --sandbox experiment "try a new caching approach"
forge-agent code --keep "continue where we left off"
forge-agent code --conversation-id <uuid> "now do step 2"
forge-agent run --agent <custom-id> "use a specific agent"
```

**Inspection:**
```bash
forge-agent info                    # current model, provider, conversation
forge-agent list agents             # available agents
forge-agent list models             # available models
forge-agent list tools [agent]      # tools available to an agent
```

## How to Choose

| Situation | Command | Why |
|---|---|---|
| User wants coding done | `forge-agent code "..."` | Routes to kosta-coder, the implementation agent |
| User wants a plan first | `forge-agent plan "..."` | Routes to muse — produces a plan without changing files |
| User wants investigation | `forge-agent research "..."` | Routes to sage — read-only, won't modify anything |
| User wants validation | `forge-agent check "..."` | Runs the custom check command against the repo |
| User wants code review | `forge-agent review "..."` | Runs the custom review command |
| User wants interactive Forge | Launch `forge` directly | Full REPL with /slash commands |
| User wants to continue a session | `forge-agent resume [id]` | Picks up where the last conversation left off |

## Getting Good Results

**Be specific in prompts.** Forge works best with concrete instructions:
- Bad: `forge-agent code "improve the API"`
- Good: `forge-agent code "add rate limiting to POST /api/users — use a sliding window of 100 req/min per IP, return 429 with Retry-After header"`

**Use --cwd for repo context.** Forge reads the working directory to understand
the project. Always pass `--cwd` when delegating from Hermes if you're not
already in the target repo.

**Use plan -> code flow for complex work.** For anything non-trivial, run
`forge-agent plan` first, review the plan with the user, then run
`forge-agent code` with the approved plan. Muse's plans are thorough and
save implementation time.

**Use --sandbox for risky experiments.** This creates an isolated git worktree
so Forge can experiment without touching the main branch. Requires a git repo.

**Use --keep or --conversation-id for multi-step work.** By default each
invocation starts a fresh conversation. If the task needs multiple steps,
use `--keep` to continue the latest conversation, or `--conversation-id <uuid>`
for a specific one.

## What to Expect

- **One-shot runs** execute the prompt and exit. Output goes to stdout.
  The agent will read files, make edits, run commands, and report results.
- **Interactive runs** (no prompt given) open a REPL. The user types prompts
  and gets responses. Exit with `/exit` or Ctrl+D.
- **Forge has its own context window.** It doesn't share context with the
  current Hermes session. Pass all relevant info in the prompt.
- **Forge can fail.** Check the exit code and output. If it errors on
  provider/model config, run `forge-agent info` to diagnose.

## Raw Forge CLI

When the wrapper isn't enough, use `forge` directly:

```bash
forge --prompt "do the thing"                    # one-shot
forge --agent muse --prompt "plan this"          # specific agent
forge -C /path --prompt "fix tests"              # specific directory
forge --conversation-id <uuid> --prompt "step 2" # continue conversation
forge --sandbox experiment --prompt "try this"   # isolated worktree
cat plan.md | forge                              # pipe input
```

Interactive commands inside a forge session:
`/forge` `/muse` `/agent` `/model` `/new` `/info` `/usage` `/compact` `/exit`

## Troubleshooting

If Forge says provider/model not configured: `forge-agent info` to check,
then `forge config list` to inspect settings.

If `--keep` picks up wrong context: use `--conversation-id <uuid>` explicitly.

If `forge-agent` isn't found but `forge` is: the wrapper script isn't installed
at `/Users/Kosta/.local/bin/forge-agent`. Fall back to raw `forge` commands.
