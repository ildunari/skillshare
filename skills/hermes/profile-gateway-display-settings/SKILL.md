---
name: hermes-profile-gateway-display-settings
description: Configure and verify Hermes gateway display/tool-progress behavior across the default profile and named profiles like gpt, including reasoning status, compact tool HUD, and process sanity checks.
targets: [hermes-default, hermes-gpt]
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

```bash
pkill -f '/Users/Kosta/.hermes/hermes-agent/.venv/bin/python -m hermes_cli.main gateway run --replace'
pkill -f '/Users/Kosta/.hermes/hermes-agent/.venv/bin/python -m hermes_cli.main --profile gpt gateway run --replace'

sleep 2

nohup /Users/Kosta/.hermes/hermes-agent/.venv/bin/python -m hermes_cli.main gateway run --replace >/tmp/hermes-default-gateway.log 2>&1 &
nohup /Users/Kosta/.hermes/hermes-agent/.venv/bin/python -m hermes_cli.main --profile gpt gateway run --replace >/tmp/hermes-gpt-gateway.log 2>&1 &

sleep 2

ps aux | egrep 'hermes_cli.main( --profile gpt)? gateway run --replace' | grep -v egrep
```

## Pitfalls

- Don’t assume changing the default profile config affects `gpt`.
- Don’t assume multiple gateway processes are wrong without checking whether they are different profiles.
- Don’t trust stale file reads alone when debugging live Python behavior; inspect the imported module source to see what the running code path actually is.
