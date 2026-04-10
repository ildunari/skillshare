---
name: forge-agent
description: >-
  Delegate coding, planning, or Apple-platform development tasks to ForgeCode
  via the forge-agent wrapper or raw forge CLI. Use whenever the user mentions
  Forge, forge-agent, "run this in Forge", "send this off", "delegate this",
  "run this in another lane", "have Forge do it", "use Forge as the coder",
  or wants work done by a separate coding agent instead of the current session.
  Also use when asking about available Forge agents, modes, or capabilities. Do
  not use for ordinary edits in the current session unless the user specifically
  wants Forge. For Sage-only investigation, use forge-sage.
metadata:
  author: Codex
  version: 2.2.0
---

# Forge Agent

Delegate work to ForgeCode — a separate AI coding agent with its own context,
tools, and conversation state. Forge runs in the terminal and has full
read/write file access, shell execution, and web fetch.

## Recommended Lanes

For the way you use Forge most often, there are three lanes to reach for first:

| Agent | What it does | When to use |
|---|---|---|
| **forge** (kosta-coder) | Implements code — edits files, runs commands, builds features | "Go build this", "fix this bug", "refactor this module" |
| **muse** | Plans and analyzes implementation work | "Plan this refactor", "what's the best approach", "scope this out" |
| **apple-dev** | Specialized Apple platform engineer for Swift, Xcode, App Store Connect, and Apple UI work | "Fix this SwiftUI bug", "build this macOS feature", "handle ASC release flow" |

If the user specifically wants **Sage** or a read-only investigation lane, use
`forge-sage` instead of routing that through this general skill.

## Quick Reference

**One-shot delegation** (most common):
```bash
forge-agent code "implement the auth middleware"
forge-agent plan "plan the database migration for v2"
forge-agent run --agent apple-dev "fix the SwiftUI navigation bug"
forge-agent check "validate the repo is in good shape"
forge-agent review "review recent changes for bugs and regressions"
```

**With options:**
```bash
forge-agent code --cwd /path/to/repo "fix the failing tests"
forge-agent code --sandbox experiment "try a new caching approach"
forge-agent code --keep "continue where we left off"
forge-agent code --conversation-id <uuid> "now do step 2"
forge-agent run --agent apple-dev --cwd /path/to/repo "implement the macOS settings screen"
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
| User wants coding done | `forge-agent code "..."` | Routes to kosta-coder, the implementation lane |
| User wants a plan first | `forge-agent plan "..."` | Routes to muse — plans without changing files |
| User wants Apple-specific implementation | `forge-agent run --agent apple-dev "..."` | Uses the Apple-focused custom agent instead of the generic coding lane |
| User wants validation | `forge-agent check "..."` | Runs the custom check command against the repo |
| User wants code review | `forge-agent review "..."` | Runs the custom review command |
| User wants Sage investigation | use `forge-sage` | Keeps Sage-only investigation separate from the general router |
| User wants interactive Forge | Launch `forge` directly | Full REPL with /slash commands |
| User wants to continue a session | `forge-agent resume [id]` | Picks up where the last conversation left off |

## Getting Good Results

**Be specific in prompts.** Forge works best with concrete instructions:
- Bad: `forge-agent code "improve the API"`
- Good: `forge-agent code "add rate limiting to POST /api/users — use a sliding window of 100 req/min per IP, return 429 with Retry-After header"`
- Good Apple-specific: `forge-agent run --agent apple-dev --cwd /path/to/app "fix the SwiftUI sheet presentation bug on macOS and verify the build still passes"`

**Use --cwd for repo context.** Forge reads the working directory to understand
the project. Always pass `--cwd` when delegating if you're not already in the
target repo.

**Use muse -> forge for complex work.** For anything non-trivial, run
`forge-agent plan` first, review the plan, then run `forge-agent code` with the
approved plan.

**Use apple-dev when the work is really Apple-specific.** If the task is mostly
about SwiftUI, UIKit, AppKit, Xcode, signing, TestFlight, or App Store Connect,
use `apple-dev` instead of the generic coding lane.

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
  current session. Pass all relevant info in the prompt.
- **Forge can fail.** Check the exit code and output. If it errors on
  provider/model config, run `forge-agent info` to diagnose.

## Raw Forge CLI

When the wrapper isn't enough, use `forge` directly:

```bash
forge --prompt "do the thing"                         # one-shot
forge --agent muse --prompt "plan this"               # planning lane
forge --agent apple-dev --prompt "fix this SwiftUI bug" # Apple lane
forge -C /path --prompt "fix tests"                   # specific directory
forge --conversation-id <uuid> --prompt "step 2"      # continue conversation
forge --sandbox experiment --prompt "try this"        # isolated worktree
cat plan.md | forge                                   # pipe input
```

Interactive commands inside a forge session:
`/forge` `/muse` `/agent` `/model` `/new` `/info` `/usage` `/compact` `/exit`

## Troubleshooting

If Forge says provider/model not configured: `forge-agent info` to check,
then `forge config list` to inspect settings.

If `--keep` picks up wrong context: use `--conversation-id <uuid>` explicitly.

If `forge-agent` isn't found but `forge` is: the wrapper script isn't installed
at `/Users/Kosta/.local/bin/forge-agent`. Fall back to raw `forge` commands.
