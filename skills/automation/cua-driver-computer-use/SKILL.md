---
name: cua-driver-computer-use
description: >
  Use Cua Driver for local macOS computer-use workflows from Hermes, including
  background native app control, screenshots, accessibility trees, direct shell
  calls, and MCP handoff. Use when the task needs real desktop/app control
  rather than browser-only automation.
version: 0.1.0
author: Hermes Agent
license: MIT
metadata:
  tags: [macos, computer-use, cua-driver, desktop-automation, automation]
---

# Cua Driver Computer Use

## When to use
Use this when Hermes needs to inspect or operate local macOS apps/windows, especially tasks that browser/CDP tools cannot handle: Finder, Preview, Calculator, native app dialogs, Electron apps with poor DOM access, canvas-heavy surfaces, or background UI checks.

Do **not** use this as the default for normal website automation. Prefer Hermes browser tools or `agent-browser` for web pages with DOM/accessibility refs. Cua Driver is the desktop layer.

## Installed tool
Cua Driver is installed on this Mac Studio as:

```bash
/usr/local/bin/cua-driver
/Applications/CuaDriver.app
```

Installed version verified during setup:

```bash
cua-driver --version
# 0.0.7
```

Screenshot fallback helper installed on this Mac Studio:

```bash
~/.local/bin/cua-screenshot --out /tmp/cua-full.png
~/.local/bin/cua-screenshot --window-id <window_id> --out /tmp/cua-window.png
```

Upstream repo/docs:

- https://github.com/trycua/cua
- https://github.com/trycua/cua/tree/main/libs/cua-driver
- https://cua.ai/docs/cua-driver

## Why this repo was chosen
`trycua/cua` is currently the best open-source full computer-use candidate for Hermes: MIT licensed, actively maintained, macOS-native, has a CLI and MCP stdio server, and is designed specifically for Computer-Use Agents. The `cua-driver` component can drive native macOS apps in the background without stealing the user's cursor, focus, or Space.

Browser-only alternatives like `browser-use`, Stagehand, Playwright MCP, and `agent-browser` are better for web workflows, but they do not replace native macOS desktop control.

## Basic commands

```bash
# Version/help
cua-driver --version
cua-driver --help

# Daemon state
cua-driver status
cua-driver diagnose

# Permissions. Most accurate after daemon is launched as CuaDriver.app.
cua-driver check_permissions

# List available MCP-style tools
cua-driver list-tools
cua-driver describe <tool_name>

# MCP stdio server
cua-driver mcp

# MCP client config snippet
cua-driver mcp-config
```

## Starting the daemon
For authoritative macOS TCC permissions, Cua recommends launching the daemon through the app bundle so prompts are attributed to `CuaDriver.app`:

```bash
open -n -g -a CuaDriver --args serve
cua-driver status
cua-driver check_permissions
```

If this is being run from a headless Telegram/launchd session and the daemon does not start, the blocker is probably the missing active GUI desktop. Ask Kosta to log into the Mac Studio desktop via Screen Sharing, then retry.

## Permissions
Cua Driver needs macOS Accessibility and Screen Recording permissions. If `check_permissions` reports missing permissions, open System Settings and grant both to `CuaDriver.app`.

A shell-launched `cua-driver check_permissions` may say permissions are missing because TCC checks the calling process, not the app bundle. Prefer daemon/app-bundle checks before concluding it is broken.

## Direct-call workflow
Use `list-tools` and `describe` before calling tools; tool names and schemas may change because Cua Driver is young.

```bash
cua-driver list-tools
cua-driver describe list_apps
cua-driver call list_apps '{}'
```

For any action that clicks, types, changes files, sends messages, purchases, posts, or changes account state, stop and get explicit user approval unless the user already authorized that exact action.

## MCP workflow
When a Hermes-compatible MCP surface is available, use:

```bash
cua-driver mcp-config
```

Then wire the printed config into the client. The stdio server command is:

```bash
/usr/local/bin/cua-driver mcp
```

## Safety defaults
- Prefer read-only operations first: status, diagnose, list tools, screenshots, window/app inspection.
- Do not enter secrets into GUI apps unless Kosta explicitly authorizes the site/app and action.
- Do not click destructive/account-changing buttons without confirmation.
- For browser-only tasks, use Hermes browser tools or `agent-browser` first; use Cua when DOM/browser control is insufficient.

## Skillshare verification
This skill is canonical in Skillshare source at:

```bash
~/.config/skillshare/skills/automation/cua-driver-computer-use/SKILL.md
```

It is shared broadly across configured agents and syncs with the flattened live skill name:

```text
automation__cua-driver-computer-use
```

After edits, sync globally:

```bash
cd ~/.config/skillshare
skillshare sync -g --json
```

Hermes targets are include-filtered from `hermes-allowlist.yaml`; because this skill is in that allowlist as `automation/cua-driver-computer-use`, it appears in both Hermes default and Hermes GPT as `automation__cua-driver-computer-use` too.

## Troubleshooting
If Cua Driver looks installed but unusable:

```bash
which cua-driver
cua-driver --version
cua-driver status
cua-driver diagnose
cua-driver check_permissions
cua-driver list-tools
```

Common blockers:

- No active macOS GUI session: `open -a CuaDriver` may fail silently from background launchd/Telegram.
- TCC permissions missing: grant Accessibility and Screen Recording to `CuaDriver.app`.
- Wrong process granted permissions: grant the app bundle, not only Terminal or a symlinked binary.
- Screenshot can still fail even with green TCC. Observed on Mac Studio with Cua Driver 0.0.7: `cua-driver call screenshot '{}'` returned `Screenshot failed: no main display found`, and window screenshot returned `Failed to start stream due to audio/video capture failure`, while native `screencapture -x /tmp/native-screen.png` worked. Treat this as a Cua Driver/ScreenCaptureKit issue, not a global macOS permission failure. Use `~/.local/bin/cua-screenshot` as the working fallback for full screenshots and window crops.
- Moving upstream: re-check docs before relying on exact tool schemas.
- Severe memory leak observed on Mac Studio with Cua Driver 0.0.7 after ~19h runtime: `cua-driver serve` reached ~35.1 GB physical footprint, 75.8 GB peak, and ~34.8 GB malloc allocation. `sample` pointed at the visual agent cursor overlay path: `AgentCursorView.body -> AgentCursorRenderer.tick(now:) -> SwiftUI CanvasDisplayList/update/render/ObservationRegistrar`. Upstream code in `libs/cua-driver/Sources/CuaDriverCore/Cursor/AgentCursorView.swift` uses `TimelineView(.animation(minimumInterval: 1/120))` + `Canvas`, and `AgentCursorRenderer.tick` mutates observable state from the render loop. Immediate mitigation: disable the overlay with `cua-driver call set_agent_cursor_enabled '{"enabled":false}'`; this persists in `~/Library/Application Support/Cua Driver/config.json` as `agent_cursor.enabled=false` and keeps the daemon/tooling usable. If using Cua long-running, add a watchdog to restart `cua-driver serve` when RSS exceeds ~1.5–2 GB or physical footprint exceeds ~3–4 GB.

## Install / update notes
Initial install used the official macOS installer with updater disabled:

```bash
curl -fsSL https://raw.githubusercontent.com/trycua/cua/main/libs/cua-driver/scripts/install.sh -o /tmp/cua-driver-install.sh
CUA_DRIVER_NO_UPDATER=1 /bin/bash /tmp/cua-driver-install.sh
```

The installer places the app in `/Applications/CuaDriver.app` and symlinks `/usr/local/bin/cua-driver` to the app binary. It may also add a Claude Code skill symlink under `~/.claude/skills/cua-driver`; Agents use the shared Skillshare skill at `automation/cua-driver-computer-use`.
