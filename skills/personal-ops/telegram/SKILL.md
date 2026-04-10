---
name: telegram
description: >
  Interact with Telegram — read and send messages, browse chats, search conversations,
  manage contacts, check unread messages, and control the Telegram desktop app.
  Uses your real Telegram account via Telethon — full access to all chats, DMs, groups,
  and channels. No bot needed. Use this skill whenever the user mentions Telegram,
  asks about messages in a Telegram chat, wants to send a Telegram message, check
  Telegram notifications, search Telegram conversations, or automate any Telegram
  workflow. Triggers on: "check Telegram", "send a Telegram message", "what's new on
  Telegram", "search Telegram", "my Telegram chats", "Telegram notifications",
  "post to Telegram", or any task involving Telegram communication.
requiredSources:
  - telegram
---

# Telegram

Control Telegram via the `telegram` CLI. Uses Telethon to connect as your real user account — full access to all chats, groups, channels, and contacts. No bot needed.

## CLI Location

`/opt/homebrew/bin/telegram`

## First-Time Setup

If not yet logged in, run:
```bash
telegram login
# Enter phone number → verification code → optional 2FA password → done
```

Session persists permanently. Check with `telegram status`.

## Usage Pattern

Always use `--json --no-input` for programmatic access:

```bash
telegram <command> [args] --json --no-input
```

## Common Workflows

### List all chats
```bash
telegram chats --limit 30 --json --no-input
```

### Read messages from a chat
```bash
telegram messages "Saved Messages" --limit 20 --json --no-input
telegram messages @durov --limit 10 --json --no-input
```

### Send a message
```bash
telegram send "My Group" "Hello everyone!" --no-input
telegram send @username "Hey!" --no-input
```

### Search messages
```bash
telegram search "meeting notes" --json --no-input
telegram search "budget" "Work Group" --json --no-input
```

### Check unread
```bash
telegram unread --json --no-input
```

## Command Reference

| Command | Args | Description |
|---------|------|-------------|
| `login` | — | One-time phone verification |
| `status` | — | Check connection status |
| `me` | — | Your user info |
| `chats` | — | List all chats (--limit N) |
| `messages` | `<chat>` | Read messages (name, @user, or ID) |
| `send` | `<chat> "text"` | Send a message |
| `reply` | `<chat> <msg_id> "text"` | Reply |
| `search` | `"query" [chat]` | Search messages |
| `contacts` | — | List contacts |
| `unread` | — | Show unread chats |
| `forward` | `<from> <msg_id> <to>` | Forward a message |
| `pin` | `<chat> <msg_id>` | Pin a message |
| `media` | `<chat>` | List media files |
| `navigate` | `<user_or_chat>` | Open in Telegram app |
| `screenshot` | `[file]` | Screenshot Telegram window |

## Guidelines

- Chat args accept **partial name matches**, **@usernames**, or numeric IDs
- Uses your REAL user account — full access, same as the app
- Session is permanent at `~/.telegram-cli/telegram.session`
- Parse JSON output with `python3 -c "import json,sys; ..."` or `jq`
