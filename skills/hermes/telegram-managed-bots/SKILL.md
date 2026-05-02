---
name: telegram-managed-bots
description: >-
  Create and wire Telegram Managed Bots from an existing Hermes Telegram manager bot. Use this whenever Kosta asks to create a new Telegram bot, use Telegram Bot Management Mode, fetch a managed bot token, avoid BotFather GUI automation, or wire a per-bot Claude/Hermes Telegram surface. This skill is especially important when BotFather automation is flaky: use the managed-bot deep-link plus getManagedBotToken flow instead.
targets: [hermes-default, hermes-gpt, claude-hermes]
---

# Telegram Managed Bots for Hermes

Use Telegram Managed Bots when the existing Hermes Telegram bot has `can_manage_bots: true`. This avoids unreliable BotFather GUI automation, but still requires Kosta to confirm the creation screen in Telegram once.

## Fast path

1. Load the manager bot token from the active Hermes env without printing it:
   - `~/.hermes/profiles/gpt/.env` usually wins for Hermes GPT.
   - fallback: `~/.hermes/.env`.
   - key: `TELEGRAM_BOT_TOKEN`.
2. Verify manager mode:
   ```bash
   python3.12 - <<'PY'
   import json, os, urllib.request
   token = os.environ['TELEGRAM_BOT_TOKEN']
   r = json.load(urllib.request.urlopen(f'https://api.telegram.org/bot{token}/getMe'))['result']
   print({'username': r.get('username'), 'can_manage_bots': r.get('can_manage_bots')})
   PY
   ```
   Do not continue unless `can_manage_bots` is true.
3. Before sending Kosta the creation link, prime/capture `managed_bot` updates. Call `getUpdates` with `allowed_updates=["managed_bot"]`, or start a short watcher that polls for the update. This matters because existing gateway code may not preserve unknown update types.
4. Give Kosta a deep link:
   ```text
   https://t.me/newbot/{manager_bot_username}/{suggested_bot_username}?name={urlencoded_display_name}
   ```
5. After Kosta confirms, capture the `managed_bot` update. It contains the managed bot user object; use its `id` as `user_id` for token calls.
6. Fetch the token without printing it:
   ```text
   POST https://api.telegram.org/bot<MANAGER_TOKEN>/getManagedBotToken
   body: user_id=<managed_bot_user_id>
   ```
7. Store the returned token only in the target service env, e.g.:
   ```text
   ~/.hermes/claude-telegram/.env
   ```
   with `chmod 600`. Never paste the token in chat, logs, skills, README files, or shell command arguments.
8. Validate the new token with `getMe`, printing only `{ok, id, username, first_name}`.

## If the creation update was missed

If Kosta already clicked the link before a watcher was running, the `managed_bot` update may be gone. Bot API does not provide a list-managed-bots endpoint. In that case:

- First try to resolve the bot user id via a logged-in Telegram user client, if available.
- If that is not available, make a second managed-bot link with a new username and run the watcher before Kosta taps confirm.
- Do not keep retrying BotFather GUI automation; it is slower and less reliable.

## Watcher pattern

Use a short Python watcher that:

- loads manager `TELEGRAM_BOT_TOKEN` from env files,
- polls `getUpdates` with `allowed_updates=["managed_bot"]`,
- when an update arrives, calls `getManagedBotToken(user_id=<managed_bot.id>)`,
- writes the token directly to the destination `.env`,
- validates the token with `getMe`,
- records only redacted metadata: managed bot id, username, first name, and creation timestamp.

Keep the watcher single-purpose. Do not modify or restart the active Hermes Telegram gateway from a Telegram-origin conversation.

## Claude Telegram bridge notes

For the Claude Code Telegram channel plugin, keep a separate bot token from the Hermes gateway token. Telegram long polling only supports one active consumer per bot token.

Do not pipe Claude Code through `tee` from the launch script. Claude treats piped stdout as non-interactive and can exit with `Input must be provided either through stdin or as a prompt argument`. Start Claude directly in tmux, then use `tmux pipe-pane` for logging.

Use the absolute Claude binary path in launchd/tmux scripts, e.g. `/Users/Kosta/.local/bin/claude`; launchd may not inherit the interactive shell `PATH`. Include `/Users/Kosta/.bun/bin` in the tmux command `PATH` too, because the official Telegram channel plugin starts through `bun`; if Bun is missing from PATH, Claude shows “Listening for channel messages” but the Telegram MCP server silently fails and the bot never polls.

If Remote Control is globally enabled in Claude settings, keep Telegram and Remote Control in separate Claude Code processes. Give the Telegram channel session a settings file with `remoteControlAtStartup: false`, add explicit permission allows for the Telegram plugin tools (`mcp__plugin_telegram_telegram__reply`, `react`, `edit_message`, `download_attachment`, and `telegram`), and run a separate Remote Control tmux session with `claude --remote-control --name Hermes`. Without the reply allow, Claude can receive Telegram messages but auto-mode may deny outbound replies as “posting under the user's identity.”

If exposing Claude Code slash commands in Telegram’s bot command menu, remember Telegram command names cannot contain hyphens. Store menu commands with underscores (for example `/add_dir`) and patch the Telegram plugin to normalize underscore aliases back to Claude’s real hyphenated commands before `handleInbound` (`/add_dir` → `/add-dir`). Use `setMyCommands`/`getMyCommands` with the child bot token and verify the reported command count.

For LaunchAgents on this Mac Studio, bootstrap into the GUI domain (`gui/$(id -u Kosta)`) rather than the user domain when `launchctl bootstrap user/...` returns `Bootstrap failed: 5: Input/output error`.

Recommended local layout:

```text
~/.hermes/claude-telegram/.env
~/.hermes/claude-telegram/start.sh
~/.hermes/claude-telegram/status.sh
~/.hermes/claude-telegram/logs/
~/.hermes/claude-telegram/state/
```

Start Claude from `~/.hermes` so Hermes-local Claude instructions are loaded. Keep the session in tmux for persistence.

## Safety

- Treat any visible token as compromised.
- Never include tokens in final responses.
- Prefer `POST` bodies or env files over command arguments.
- `chmod 600` env files containing bot tokens.
- DM-only is the right first deployment; groups/topics can come later after session routing is designed.
