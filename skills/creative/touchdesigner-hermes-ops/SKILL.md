---
name: touchdesigner-hermes-ops
targets: [hermes-default, hermes-gpt, claude, claude-hermes]
description: >-
  Operate the Mac Studio TouchDesigner + twozero MCP setup for Hermes. Use this whenever the user wants Hermes to create TouchDesigner visuals, check whether the TouchDesigner MCP gateway is ready, finish the GUI setup, troubleshoot port 40404, install or reason about a launch agent, or produce a fallback TouchDesigner-style artifact when the GUI session is unavailable.
version: 1.0.0
---

# TouchDesigner Hermes Ops

This skill is the local runbook for using the TouchDesigner creative-coding setup from Hermes on Kosta's Mac Studio.

Load `creative__touchdesigner-mcp` for the actual TD operator/MCP tool reference. Use this skill for the surrounding operational workflow: app install, twozero gateway readiness, launch-agent handling, GUI-session constraints, and fallback artifact creation.

## Current architecture

```text
Hermes Telegram/Discord/CLI session
  -> Hermes MCP client config: twozero_td
  -> http://localhost:40404/mcp
  -> twozero.tox running inside TouchDesigner
  -> TouchDesigner Python/operator network
```

Known local paths:

- TouchDesigner app: `/Applications/TouchDesigner.app`
- twozero tox: `~/Downloads/twozero.tox`
- Default Hermes skill: `~/.hermes/skills/creative__touchdesigner-mcp/`
- GPT Hermes skill: `~/.hermes/profiles/gpt/skills/creative__touchdesigner-mcp/`
- Hermes MCP config key: `mcp_servers.twozero_td`
- MCP endpoint: `http://localhost:40404/mcp`

## First checks

Run these before claiming TouchDesigner/Hermes is ready:

```bash
stat -f '%Su' /dev/console
brew list --cask touchdesigner >/dev/null && brew info --cask touchdesigner | sed -n '1,8p'
ls -lh ~/Downloads/twozero.tox
hermes mcp list
HERMES_PROFILE=gpt hermes mcp list
nc -z 127.0.0.1 40404 && echo 'twozero MCP: READY' || echo 'twozero MCP: NOT READY'
```

Interpretation:

- `twozero_td` listed in `hermes mcp list` means Hermes knows about the server.
- Port `40404` open means TouchDesigner is running with twozero MCP enabled.
- If the console user is not `Kosta`, do not expect GUI app launch or drag/drop setup to work from a background Telegram/Discord session.

## GUI-session rule

TouchDesigner is a macOS GUI app. Hermes can install files and edit config while running in the background, but it cannot reliably launch or operate the app when another user owns the console session.

If `stat -f '%Su' /dev/console` is not `Kosta`, stop before trying to drive the UI and tell Kosta the remaining manual step is GUI-bound.

Manual finish when signed in as Kosta:

1. Open TouchDesigner.
2. Drag `~/Downloads/twozero.tox` into the TouchDesigner network editor.
3. Click Install.
4. Enable `twozero icon -> Settings -> mcp -> auto start MCP -> Yes`.
5. Verify: `nc -z 127.0.0.1 40404 && echo READY`.

## Setup / repair commands

Use the flat Skillshare-managed paths, not the upstream nested path:

```bash
HERMES_HOME="$HOME/.hermes" \
  bash "$HOME/.hermes/skills/creative__touchdesigner-mcp/scripts/setup.sh"

HERMES_HOME="$HOME/.hermes/profiles/gpt" \
  bash "$HOME/.hermes/profiles/gpt/skills/creative__touchdesigner-mcp/scripts/setup.sh"
```

If TouchDesigner is missing:

```bash
brew install --cask touchdesigner
```

TouchDesigner Non-Commercial is free for personal/non-commercial learning use, capped at 1280x1280 output. Paid licensing is needed for commercial work and some pro/export features.

## Optional launch agent

Use a launch agent only after the manual twozero setup is complete. The launch agent can open TouchDesigner when Kosta logs into the GUI session; it cannot complete the `.tox` install or click settings inside TouchDesigner.

Install from this skill with:

```bash
bash ~/.hermes/profiles/gpt/skills/creative__touchdesigner-hermes-ops/scripts/install_launch_agent.sh
```

The script writes `~/Library/LaunchAgents/com.kosta.touchdesigner.twozero.plist`. It loads it only if the current console user is Kosta; otherwise it leaves the plist ready for the next Kosta GUI login.

Remove it with:

```bash
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.kosta.touchdesigner.twozero.plist 2>/dev/null || true
rm -f ~/Library/LaunchAgents/com.kosta.touchdesigner.twozero.plist
```

## When asked to make a visual

If port 40404 is ready, use the MCP tools from `creative__touchdesigner-mcp`: discover parameters first, create the network, verify errors/perf, capture screenshot/video.

If port 40404 is not ready because the GUI session is unavailable, still make something useful: produce a TouchDesigner-style preview artifact using local Python/ffmpeg and, when helpful, also write a TouchDesigner Python scene script that can be pasted or executed once twozero is live.

Use `/tmp/hermes-touchdesigner-artifacts/` for generated previews unless the user asks for a project path.

## Reporting

Keep the report short:

- Say whether Hermes MCP config is present.
- Say whether the live twozero port is ready.
- Say exactly what is blocked by GUI login, if anything.
- Attach the generated preview if the user asked for something visual.
