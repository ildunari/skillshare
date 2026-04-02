---
name: discord
description: >
  Interact with Discord — read and send messages, browse servers and channels, search conversations,
  manage DMs, check mentions, and control the Discord desktop app. Use this skill whenever the user
  mentions Discord, asks about messages in a server, wants to send a Discord message, check Discord
  notifications, search Discord conversations, or automate any Discord workflow. Also use when the
  user references specific Discord servers by name (Claude, Brown, Coders, etc.) or asks about
  unread messages/mentions. Triggers on: "check Discord", "send a message on Discord", "what's new
  in the Claude server", "search Discord for", "my Discord DMs", "Discord notifications",
  "post to Discord", or any task involving Discord communication.
requiredSources:
  - discord
---

# Discord

Control Discord via the `discord` CLI. All commands go through Discord's REST API v10 using the user's own auth token, auto-extracted from the running Discord Electron app.

## CLI Location

`/opt/homebrew/bin/discord`

## Usage Pattern

Always use `--json --no-input` flags for programmatic access:

```bash
discord <command> [args] --json --no-input
```

## Common Workflows

### Read recent messages from a channel
```bash
# Find the guild and channel first
discord guilds --json --no-input
discord channels "Claude" --json --no-input
# Then read messages
discord messages <channel_id> --limit 20 --json --no-input
```

### Send a message
```bash
discord send <channel_id> "Message text here" --no-input
```

### Search a server
```bash
discord search "Claude" "API documentation" --json --no-input
```

### Check unread mentions
```bash
discord unread --json --no-input
```

### Send a DM
```bash
discord dm <user_id> "Hey, message here" --no-input
```

## Command Reference

| Command | Args | Description |
|---------|------|-------------|
| `me` | — | Current user info |
| `guilds` | — | List all servers |
| `channels` | `<guild>` | Channels in a guild (name or ID) |
| `messages` | `<channel_id>` | Read messages (use --limit N) |
| `send` | `<channel_id> "text"` | Send a message |
| `reply` | `<msg_id> <ch_id> "text"` | Reply to a message |
| `dm` | `<user_id> "text"` | Send a direct message |
| `dms` | — | List DM channels |
| `search` | `<guild> "query"` | Search messages in guild |
| `react` | `<ch_id> <msg_id> <emoji>` | Add reaction |
| `unread` | — | Show unread mentions |
| `members` | `<guild>` | List guild members |
| `roles` | `<guild>` | List guild roles |
| `pins` | `<channel_id>` | Pinned messages |
| `status` | `[text]` | Get/set custom status |
| `navigate` | `<channel_id>` | Open in Discord app |
| `screenshot` | `[file]` | Screenshot Discord app |

## Guidelines

- Guild and channel arguments accept **partial name matches** (case-insensitive) or snowflake IDs
- Use `--limit N` to control result count (default 25)
- Token is cached in macOS Keychain — auto-refreshes on 401
- If Discord isn't running with CDP, the CLI will try to relaunch it
- For CDP features (navigate, screenshot), Discord must be on port 9224
- Rate limits: ~50 req/s general, ~1 req/s for search
- Parse JSON output with `python3 -c "import json,sys; ..."` or `jq`

## User's Servers

The user (ildunari, ID: 339622137826508802) has 22 servers including:
Claude, Brown Community Discord, Brown University Graduate Students, Google Labs,
Coders, OpenClaw, Perplexity, r/Gemini, ildunari's server (owned), and others.
