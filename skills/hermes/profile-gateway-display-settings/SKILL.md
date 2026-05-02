---
name: hermes-profile-gateway-display-settings
description: Configure and verify Hermes gateway display/tool-progress behavior across the default profile and named profiles like gpt, including reasoning status, compact tool HUD, and process sanity checks.
targets: [hermes-default, hermes-gpt, claude-hermes]
---

# Hermes profile gateway display settings

Use this when a user wants Telegram/Discord gateway display behavior changed — especially tool progress, reasoning visibility, or per-profile differences between `default` and `gpt`.

## Core findings

- Hermes profiles are **fully isolated**. `~/.hermes/config.yaml` and `~/.hermes/profiles/<name>/config.yaml` must be configured separately.
- It is valid to run **one default gateway** and **one `gpt` gateway** at the same time. That is not inherently a bug.
- A real process problem is:
  - more than one gateway for the same profile, or
  - two profiles using the same platform token and colliding.
- If display changes are only config changes, a restart is enough. If message-rendering code changed, restart is also required so the gateway reloads the code.

## Display settings that mattered here

For compact progress with no full reasoning transcript:

```yaml
display:
  show_reasoning: false
  reasoning_style: status
  tool_progress: compact
  progress_cleanup: keep
  compact_progress_layout: multi_line
```

What this means:
- `show_reasoning: false` prevents transcript-style reasoning.
- `reasoning_style: status` is the intended mode for a short “thinking” status instead of full reasoning text.
- `tool_progress: compact` enables the compact tool HUD.
- `progress_cleanup: keep` leaves the status message visible after completion.
- `compact_progress_layout: multi_line` is the right shape for one-line-per-activity rendering.

## Verification workflow

1. Read both configs:
   - `~/.hermes/config.yaml`
   - `~/.hermes/profiles/gpt/config.yaml`
2. Check the live imported gateway code, not just the file text:
   - `python - <<'PY'`
   - `import importlib, inspect, gateway.run as gr`
   - `importlib.reload(gr)`
   - `print(inspect.getsource(gr._render_compact_tool_progress))`
   - `PY`
3. Check running gateway processes:
   - `ps aux | egrep 'hermes_cli.main( --profile gpt)? gateway run --replace' | grep -v egrep`
4. If behavior still seems wrong after restart, verify which profile/process is actually handling the platform message.

## Safe restart pattern for one default + one gpt gateway

Prefer the managed background LaunchAgent restart. On this Mac Studio, Hermes gateways are loaded in the `user/<uid>` launchd domain with `LimitLoadToSessionType=Background`; do **not** use `gui/<uid>` from Telegram/Discord/background shells.

```bash
uid=$(id -u)
launchctl kickstart -k user/$uid/ai.hermes.gateway
launchctl kickstart -k user/$uid/ai.hermes.gateway-gpt
```

If this is triggered from a live Telegram/Discord/Hermes gateway command, do not run it inline inside the receiving gateway process. Queue a detached helper that replies first, sleeps briefly so the reply flushes, runs the two `launchctl kickstart -k user/$uid/...` commands, logs to `~/.hermes/logs/restart-surfaces.log`, then verifies the managed services.

The local implementation for that helper is:

```text
hermes_cli/restart_surfaces.py
/restart-gateways
/restart-hermes
/restart-gateways --dry-run
/restart-hermes --dry-run
```

Only fall back to killing and launching direct `gateway run --replace` processes when launchd is broken or unloaded and the dual-gateway recovery skill says to use the headless fallback. Direct `pkill`/`nohup` restarts are no longer the normal first choice because they can leave orphaned gateway pollers outside launchd.

## Pitfalls

- Don’t assume changing the default profile config affects `gpt`.
- Don’t assume multiple gateway processes are wrong without checking whether they are different profiles.
- Don’t trust stale file reads alone when debugging live Python behavior; inspect the imported module source to see what the running code path actually is.
