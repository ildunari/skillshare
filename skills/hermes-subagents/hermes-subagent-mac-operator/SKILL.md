---
name: hermes-subagent-mac-operator
description: Spawn a macOS local-operations delegate for files, processes, apps, launch
  agents, cron, logs, and setup checks.
version: 0.4.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags:
    - hermes
    - subagent
    - delegation
    - template
targets:
- hermes-default
- hermes-gpt
- claude-hermes
---

# hermes-subagent-mac-operator

## Trigger description
Load this skill when the parent Hermes agent should spawn a focused `mac_operator` delegate instead of doing all macOS operation/admin work in the main context.

## When to use
Use for Mac troubleshooting, automation, app/process checks, launchd/cron, paths, logs, Homebrew, Tailscale, Syncthing-aware file work.

## Recommended delegate_task toolsets
- Primary: `['terminal', 'file']`
- Add `web` for official docs lookup only.
- Avoid giving broad `hermes-cli` access unless the task truly needs it.

## Copyable delegate_task prompt template
```python
delegate_task(
    goal="Operate on this Mac. Inspect state first, use native CLIs, act on safe reversible tasks without asking, and report exact commands/results. Workspace root is /Users/Kosta unless narrowed.",
    context="""
User/request: <paste the exact user ask>
Kosta-specific constraints: concise, technical, Telegram-friendly; avoid noisy tables unless fenced.
Known context: <paths, URLs, screenshots, constraints, prior findings, deadlines>
Definition of done: <what the parent needs back>
PATH note: source /opt/homebrew/bin if brew is needed and PATH may not include it. Use full paths (/opt/homebrew/bin/brew, /usr/bin/defaults) when uncertain.
Do not assume parent conversation history; everything needed is in this context.

Return using the Output Contract below.
""",
    toolsets=['terminal', 'file']
)
```

## Prerequisite checks

Run these checks before the relevant command class; skip if already verified this session:

| Before using… | Check |
|---|---|
| `brew` | `command -v brew 2>/dev/null \|\| { test -x /opt/homebrew/bin/brew && echo /opt/homebrew/bin/brew; } \|\| { test -x /usr/local/bin/brew && echo /usr/local/bin/brew; }` |
| `launchctl` domain commands | `sw_vers -productVersion` — Ventura 13+ uses `gui/$(id -u)/<label>` domain format |
| Tailscale CLI | `command -v tailscale 2>/dev/null` |
| Writing to any `~/` directory | Check if Syncthing-tracked: `grep -Frl "<exact-path>" ~/Library/Application\ Support/Syncthing/config.xml 2>/dev/null` |
| `mas` (App Store CLI) | `command -v mas 2>/dev/null` |
| Any file path | `test -e "<path>" && echo exists \|\| echo missing` before operating |

If a prerequisite is missing and the task requires it, report "prerequisite missing: `<tool>`" in Issues/blockers and stop; do not attempt workarounds.

## Automation posture

**Proceed without asking** for any of these:
- Read/inspect/list operations (files, processes, logs, system state)
- `brew info`, `brew list`, `brew install <named-pkg>`, `brew upgrade <named-pkg>` (single explicit package only)
- `launchctl list`, `launchctl print gui/$(id -u)/<label>`, reading plist files
- Creating new files in non-synced, non-shared directories
- Restarting a named user-level LaunchAgent that is not a gateway service
- `pkill`/`kill` for a clearly non-critical named process (not `hermes`, not `telegram`, not system daemons)
- Running diagnostics: `lsof`, `ps`, `top -l1`, `df`, `netstat`, `ping`, `traceroute`
- `defaults read` (reading only), `plutil -p`

**Stop and confirm** before:
- Deleting any file or directory (`rm`, `rmdir`, `trash`)
- Writing into `~/.hermes/`, `~/.config/hermes-state/`, `~/Library/LaunchAgents/` or any Syncthing-tracked path
- Killing or restarting `hermes`, `telegram`, or any active gateway process
- `defaults write` or `defaults delete` (system preference changes)
- Installing a new LaunchAgent or modifying an existing one
- Any action using `--force`, `-rf`, or that is not easily reversed
- Accessing, printing, or modifying credentials, tokens, or API keys

**After each action, verify with an exact command** and include the output (trimmed if long):

| Action | Verification command |
|---|---|
| File created/modified | `ls -la <path>` |
| Process started/stopped | `pgrep -fl <name>` |
| LaunchAgent loaded | `launchctl list \| grep <label>` |
| LaunchAgent unloaded | `launchctl list \| grep <label>` (expect no output) |
| Homebrew install | `brew list <pkg> && brew info <pkg> \| head -3` |
| App Store install | `mas list \| grep <app-id>` |
| Network/service reachable | `curl -sf --max-time 5 <endpoint>` or `ping -c1 <host>` |

**On failure — run exactly one diagnostic step** before stopping:

| Failed action | First diagnostic |
|---|---|
| `brew install` | `brew doctor 2>&1 \| tail -20` |
| `launchctl load` | `launchctl print gui/$(id -u)/<label> 2>&1 \| tail -20` then `plutil -p <plist-path>` |
| `launchctl unload` | `launchctl list \| grep <label>` to confirm current state |
| Service/process won't start | `log show --last 5m --predicate 'process == "<name>"' --info 2>/dev/null \| tail -30` |
| File operation fails | `ls -la <parent-dir>` and check `echo $?` from the failed command |
| Network unreachable | `ping -c2 8.8.8.8` to distinguish host vs internet issue |

Report raw diagnostic output verbatim; do not paraphrase error messages.

## macOS version notes

- **launchctl domain format**: macOS Ventura (13+) requires `gui/$(id -u)/<label>` for per-user agents. Use `launchctl print gui/$(id -u)/<label>` not `launchctl print <label>`. The `launchctl error <code>` subcommand is unreliable on modern macOS — use `launchctl print gui/$(id -u)/<label>` to read service state.
- **Homebrew prefix**: Apple Silicon = `/opt/homebrew`, Intel = `/usr/local`. Detect with `$(brew --prefix)` or check `uname -m` (`arm64` = Apple Silicon). Delegate shells may not have `/opt/homebrew/bin` in PATH — use full path or run `eval "$(/opt/homebrew/bin/brew shellenv)"` first.
- **System log**: `log show` (unified logging) is preferred over `tail /var/log/system.log` on Ventura+. Use `--info` flag to capture service startup messages that default level misses.
- **Syncthing config**: default location is `~/Library/Application Support/Syncthing/config.xml`. Use `-F` (fixed-string) with `grep` when matching literal paths to avoid regex metacharacter issues.

## Output contract
Return a compact report with:
1. **Answer/result** — the direct conclusion or completed action.
2. **Evidence/actions** — exact commands run and their output (trimmed if long).
3. **Recommendations/next steps** — only what matters.
4. **Issues/blockers** — uncertainty, missing access, prerequisites missing, or confirmation needed.

## Pitfalls
Assuming Linux paths; using sudo casually; modifying synced folders without checking Syncthing config first; starting duplicate gateways; treating every action as requiring user confirmation when it is clearly read-only or reversible; using legacy `launchctl` domain syntax on Ventura+; running `brew` without verifying PATH includes `/opt/homebrew/bin`; using `launchctl error <code>` which is unreliable on modern macOS.
