---
name: hermes-telegram-gateway
description: >-
  Hermes Agent's Telegram bot gateway — adapter code, Bot API integration,
  DM topics, silent notifications, reactions, polls, forum management, and
  Bot API 9.4+ reference. Use when working on the Hermes Telegram platform
  adapter (gateway/platforms/telegram.py), the telegram_actions tool, DM
  topic setup, silent progress messages, or debugging Telegram delivery
  from the Hermes gateway. NOT for the user-account Telethon `telegram`
  CLI — use the separate `telegram` skill for that.
  Triggers on: hermes telegram gateway, telegram adapter, telegram bot api,
  DM topic, bot api 9.4, telegram_actions tool, disable_notification,
  createForumTopic, PTB, python-telegram-bot, silent progress, set_profile_photo.
tags: [telegram, bot-api, gateway, messaging, hermes-agent]
version: "1.1"
targets: [hermes-default, hermes-gpt]
---

# Hermes Telegram Gateway Skill

This is a Hermes-specific shared skill. Canonical source lives under
`~/.config/skillshare/skills/hermes/` and it should sync only to Hermes targets
via `targets: [hermes-default, hermes-gpt]`. It should not propagate to other
AI CLIs. The skillshare `telegram` skill is a different thing (Telethon
user-account CLI).



## Architecture

- Adapter: `~/.hermes/hermes-agent/gateway/platforms/telegram.py`
- Network fallback: `gateway/platforms/telegram_network.py`
- Base class: `gateway/platforms/base.py` (BasePlatformAdapter)
- Gateway dispatch: `gateway/run.py`
- Config: `~/.hermes/config.yaml` under `platforms.telegram`
- Env: `~/.hermes/.env` (TELEGRAM_BOT_TOKEN, TELEGRAM_ALLOWED_USERS, etc.)
- Reference doc: `~/.hermes/references/telegram-bot-api.md`

## DM Topics (Bot API 9.4+)

Telegram now supports forum topics inside bot DMs (private chats).

### Config (config.yaml)
```yaml
platforms:
  telegram:
    extra:
      dm_topics:
        - chat_id: 5320274083
          topics:
            - name: "General"
              icon_color: 7322096
              thread_id: 1670  # persisted after first creation
```

### Creating topics via API
```bash
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/createForumTopic" \
  -d chat_id=CHAT_ID -d name="Topic Name" | python3 -m json.tool
```

### User settings
- User disabled topic creation (only bot creates topics via BotFather)
- To send to a specific topic: use `message_thread_id` parameter
- Cron delivery format: `telegram:5320274083:thread_id`

## Silent Notifications

Tool progress and reasoning output use `disable_notification=True` so only the final response buzzes the user.

### Config toggles (config.yaml)
```yaml
display:
  tool_progress: compact      # off | new | all | compact | verbose
  reasoning_style: status     # transcript | status | hidden
  progress_cleanup: keep      # keep | replace | delete
  compact_progress_layout: multi_line
  show_reasoning: false
  show_context_status: true
streaming:
  enabled: true
```

### How it works
- `adapter.send(..., silent=True)` passes `disable_notification=True` to Telegram
- Progress messages: sent as silent, edited in place as tools fire
- Reasoning: sent as separate silent message before final response
- Final response: normal notification

## Available Adapter Methods

### Core (existing)
- `send(chat_id, content, reply_to, metadata, silent)` — text with MarkdownV2
- `edit_message(chat_id, message_id, content)` — edit sent message
- `send_image(chat_id, image_url, metadata)` — photo from URL
- `send_image_file(chat_id, file_path, metadata)` — photo from file
- `send_document(chat_id, file_path, metadata)` — file attachment
- `send_video(chat_id, video_path, metadata)` — video
- `send_voice(chat_id, audio_path, metadata)` — voice message (ogg)
- `send_animation(chat_id, url, metadata)` — GIF
- `send_typing(chat_id, metadata)` — typing indicator
- `send_update_prompt(chat_id, prompt, default, session_key)` — inline keyboard

### New Methods (added)
- `send_reaction(chat_id, message_id, emoji)` → bool — react with emoji
- `send_poll(chat_id, question, options, **kwargs)` → SendResult
- `send_location(chat_id, latitude, longitude, **kwargs)` → SendResult
- `send_venue(chat_id, lat, lon, title, address, **kwargs)` → SendResult
- `send_contact(chat_id, phone_number, first_name, **kwargs)` → SendResult
- `send_sticker(chat_id, sticker, **kwargs)` → SendResult
- `forward_message(chat_id, from_chat_id, message_id)` → SendResult
- `copy_message(chat_id, from_chat_id, message_id)` → SendResult
- `edit_forum_topic(chat_id, thread_id, name, icon_emoji)` → bool
- `close_forum_topic(chat_id, thread_id)` → bool
- `reopen_forum_topic(chat_id, thread_id)` → bool
- `delete_forum_topic(chat_id, thread_id)` → bool
- `set_bot_profile_photo(photo_path)` → bool
- `remove_bot_profile_photo()` → bool
- `attach_context_badge(chat_id, message_id, used, total, details)` → bool — attach an inline-keyboard footer button to an existing message showing context-window usage. Uses `editMessageReplyMarkup` so message text is untouched. Tapping fires a `ctx:` callback that shows a detail alert. See "Inline-keyboard footers" section below.

## Agent Tool: telegram_actions

For in-conversation Telegram-specific actions, the agent has a `telegram_actions` tool (in `tools/telegram_actions_tool.py`, registered in the `messaging` toolset). It's a single multi-action tool like `send_message`.

### Supported actions
`react`, `send_poll`, `send_location`, `send_venue`, `send_contact`, `send_sticker`, `forward`, `copy`, `edit_topic`, `close_topic`, `reopen_topic`, `delete_topic`, `set_profile_photo`, `remove_profile_photo`

### Pattern (matches send_message_tool.py)
- Lazy imports inside handlers (avoid circular imports from gateway/)
- Fresh `Bot(token=...)` instance per call, not the live adapter
- `_run_async` from model_tools bridges sync handler → async Bot methods
- Token from `gateway.config.load_gateway_config().platforms[TELEGRAM].token`
- chat_id defaults from `os.getenv('HERMES_SESSION_CHAT_ID')` when not provided
- Returns JSON strings
- `check_fn` gates on Telegram being configured + enabled

### Adding a new action
1. Write `_handle_<action>(args)` helper
2. Add to `_ACTION_HANDLERS` dispatch dict
3. Add to `enum` in TELEGRAM_ACTIONS_SCHEMA
4. Validate required params before calling API

## Inline-Keyboard Footers on Streamed Messages

Pattern for attaching small status badges, action buttons, or metadata
chips to the **final** message of a streamed agent response, without
disturbing the message text and without touching the abstract base
adapter class. Used by the context-usage badge (`attach_context_badge`)
and reusable for any future "metadata X about this turn" feature.

### Architecture (4 layers, ~140 lines total)

1. **Config gate** in `hermes_cli/config.py` `DEFAULT_CONFIG["display"]`:
   add a bool key like `show_context_status: True`. Read it in
   `gateway/run.py` after the stream task wait.

2. **Stream consumer property** in `gateway/stream_consumer.py`:
   expose `final_message_id` as a `@property` returning `self._message_id`.
   The private `_message_id` already tracks the last edited message;
   the property just makes it public-accessible to gateway/run.py
   without poking through underscores.

3. **Telegram-only adapter method** in `gateway/platforms/telegram.py`:
   add `async def attach_<thing>(self, chat_id, message_id, ...)` that
   builds an `InlineKeyboardMarkup([[InlineKeyboardButton(...)]])` and
   calls `self._bot.edit_message_reply_markup(...)`. This edits ONLY
   the markup, leaving message text untouched — no MarkdownV2
   re-parse risk, no flood-control concerns from re-sending content.
   Wrap the whole thing in try/except and log at DEBUG only — failures
   are common (>48h old messages, deleted messages, flood control)
   and benign.

4. **Wiring in `gateway/run.py`** after `await asyncio.wait_for(stream_task, timeout=5.0)`:
   ```python
   try:
       _display_cfg = user_config.get("display") or {} if isinstance(user_config, dict) else {}
       if _display_cfg.get("show_<feature>", True):
           _sc = stream_consumer_holder[0]
           if _sc and _sc.already_sent and getattr(_sc, "final_message_id", None):
               _adapter = self.adapters.get(source.platform)
               if _adapter is not None and hasattr(_adapter, "attach_<thing>"):
                   try:
                       await _adapter.attach_<thing>(
                           chat_id=source.chat_id,
                           message_id=_sc.final_message_id,
                           ...
                       )
                   except Exception as exc:
                       logger.debug("attach_<thing> failed: %s", exc)
   except Exception:
       logger.debug("attach_<thing> wiring error", exc_info=True)
   ```

### Why hasattr() duck typing instead of base-class signature changes

The base `BasePlatformAdapter` has 8 concrete subclasses (telegram,
discord, slack, matrix, signal, mattermost, whatsapp, feishu). Adding
a new abstract method or even an optional kwarg to `edit_message`
forces touching all 8. The `hasattr(adapter, "attach_<thing>")` check
in gateway/run.py keeps the new method Telegram-only with zero
collateral and zero risk of breaking other adapters. When you later
want a Discord equivalent, just add a same-named method on
`DiscordAdapter` and the wiring picks it up automatically. No core
changes required.

### Callback handler (`ctx:` pattern)

Tappable badges need a `_handle_callback_query` branch in
`gateway/platforms/telegram.py`. Use a short prefix like `ctx:` so
multiple feature classes can coexist. Two responsibilities:

1. **Always answer the callback query.** If you don't,
   Telegram clients show a perpetual loading spinner on the button.
   Even error paths must call `await query.answer()`.

2. **Pack the popup payload into `callback_data`** instead of looking
   it up in server-side state. callback_data is capped at **64 bytes**
   per Telegram, so use single-letter keys and `json.dumps(..., separators=(",", ":"))`.
   For the context badge: `{"u":12450,"t":200000,"p":14200,"c":1850,"a":8}`
   = ~45 bytes. If your payload would overflow 64 bytes, fall back to
   `<prefix>:noop` so the button still renders without the popup.

3. **`show_alert=True`** gives a modal popup the user must dismiss
   (good for detail you want them to actually read). Without it, the
   answer is a fleeting top-of-screen toast.

### Edit-only-markup vs full edit

`bot.edit_message_reply_markup(chat_id, message_id, reply_markup=...)`
edits ONLY the inline keyboard. It does NOT touch text, parse_mode,
or entities. This is the right primitive for footer badges because:

- No risk of MarkdownV2 re-parse failure on content the bot already
  successfully sent
- Doesn't count against per-message edit content limits
- Same flood-control bucket as edit_message_text but lighter wire
- Original message ID is preserved so reply_to_message_id from prior
  context still works

Use the full `edit_message_text(..., reply_markup=...)` only if you
also need to change content. For passive status, always use
`edit_message_reply_markup`.

### Pitfalls specific to this pattern

1. **Don't attach the badge inside the stream consumer.** It needs to
   happen AFTER `stream_task` is awaited in gateway/run.py, because
   the stream consumer's `_send_or_edit` may still be in flight up
   until the final flush. Attaching from inside the consumer races
   with its own writes.

2. **Skip when `_sc.already_sent` is False.** This means the stream
   was disabled mid-stream (Signal/Email/HA, or flood control killed
   editing). The badge target would be a non-existent message.

3. **Skip when `last_prompt_tokens` is 0 or `context_length` is 0.**
   These can be unset for the very first turn or when the agent
   bypassed the context compressor (e.g. cached agent reuse with no
   new API call). A badge with `0/0` is misleading.

4. **The cached agent's context_compressor IS the persistent state**
   across turns in a session. `last_prompt_tokens` is the last call's
   prompt size, NOT cumulative. `session_prompt_tokens` (on the agent
   itself) is cumulative. Use the right one for each field of your
   detail popup.

5. **Don't use the badge for things that change frequently mid-turn.**
   It only updates when the message finalizes. For "live" status use
   the streaming cursor in `stream_consumer.py` or tool progress
   messages instead.

## Calling Bot API Directly

When the adapter doesn't expose a method, use curl:
```bash
source ~/.hermes/.env
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/METHOD_NAME" \
  -d chat_id=CHAT_ID -d param=value | python3 -m json.tool
```

## Surviving hermes update

The Telegram adapter mods are maintained via the **`hermes-local-patches`** skill — load it for the full pattern. Specific patch files for this feature:

- `~/.hermes/patches/telegram-features.patch` — diff for `gateway/platforms/telegram.py`, `base.py`, `run.py`, `model_tools.py`, `toolsets.py`
- `~/.hermes/patches/telegram_actions_tool.py.new` — full new tool file

### Regenerating after local edits
The patch file is the union of ALL local mods (the name "telegram-features"
is historical — it now also carries the gateway env-var fix, the approval.py
silent-deny logger fix, the context-badge config default, etc.). Always
regenerate against the full set, not just the file you touched:

```bash
cd ~/.hermes/hermes-agent
cp ~/.hermes/patches/telegram-features.patch \
   ~/.hermes/patches/telegram-features.patch.bak.$(date +%Y%m%d-%H%M%S)
git --no-pager diff \
    agent/prompt_builder.py \
    gateway/platforms/api_server.py \
    gateway/platforms/base.py \
    gateway/platforms/telegram.py \
    gateway/run.py \
    hermes_cli/commands.py \
    hermes_cli/config.py \
    hermes_cli/gateway.py \
    model_tools.py \
    plugins/memory/__init__.py \
    tools/approval.py \
    toolsets.py \
    > ~/.hermes/patches/telegram-features.patch
cp tools/telegram_actions_tool.py ~/.hermes/patches/telegram_actions_tool.py.new
wc -l ~/.hermes/patches/telegram-features.patch  # sanity check
```

Use `git status --short` first to see what's actually modified — if
new files appear in the modified list (e.g. someone added a hook in
another file), include them too. The file list above is the snapshot
as of April 2026 ~1700 lines; expect it to grow.

The post-merge hook at `~/.hermes/hermes-agent/.git/hooks/post-merge` auto-applies these after every `hermes update`. See the `hermes-local-patches` skill for hook details, troubleshooting, and the broader pattern.

## Bot API Changelog (Recent)

### 9.6 (Apr 3, 2026) — Managed Bots, Polls overhaul
### 9.5 (Mar 1, 2026) — date_time entities, member tags, sendMessageDraft
### 9.4 (Feb 9, 2026) — DM topics, custom emoji buttons, bot profile photos

Full reference: `~/.hermes/references/telegram-bot-api.md`

## Pitfalls

1. MarkdownV2 requires escaping special chars — adapter handles this in format_message()
2. Telegram flood control: edits throttled to 1.5s minimum between edits
3. Message length limit: 4096 chars, auto-chunked by truncate_message()
4. Forum thread_id is different from reply_to_message_id — don't confuse them
5. Gateway restart from inside Telegram chat interrupts the session — run gateway control from local shell (`launchctl kickstart -k gui/$(id -u)/ai.hermes.gateway` on Studio)
6. python-telegram-bot may lag behind Bot API — newer methods may need raw HTTP fallback via `self._bot._post()`

### PTB 22.7+ API Gotchas (verified April 2026)

These caught a code review. Check your PTB version with:
```python
import telegram; print(telegram.__version__)
```

- **`set_my_profile_photo` requires `InputProfilePhotoStatic` wrapper**, NOT raw `InputFile`. On PTB 22.7+:
  ```python
  from telegram import InputFile, InputProfilePhotoStatic
  await bot.set_my_profile_photo(photo=InputProfilePhotoStatic(photo=InputFile(f)))
  ```
  Passing a raw `InputFile` raises TypeError. Catch `ImportError` on `InputProfilePhotoStatic` to support older versions.

- **Method is `remove_my_profile_photo`, not `delete_my_profile_photo`.** The underlying API endpoint is `removeMyProfilePhoto`. Do NOT use `deleteMyProfilePhoto` in `_post()` fallbacks — that endpoint doesn't exist.

- **`set_message_reaction` expects a Python list, not a JSON string.** In raw `_post()` fallbacks: `data={"reaction": [{"type": "emoji", "emoji": "👍"}]}`. Don't `json.dumps()` it — PTB's `_post` serializes nested structures automatically. Double-encoding causes the API to reject it.

- **Exception types for fallback branches**: Use `ImportError` for missing wrapper classes (compile-time absence), `AttributeError` for missing methods (runtime absence). Don't conflate them.

### Review-driven lesson

When implementing wrappers around python-telegram-bot, always:
1. Probe the actual installed version: `hasattr(Bot, 'method_name')`, `from telegram import ClassName`
2. Read PTB's source for the exact signature — the Bot API docs describe the HTTP API, not the library's Python signatures
3. Run a code review subagent after writing adapter/tool code — it catches signature mismatches humans miss
4. The adapter methods and the tool handlers are two separate code paths; fix bugs in BOTH

## Command Scope Gotcha (silent command hiding)

Telegram has per-scope command lists with precedence:
`CHAT > CHAT_ADMINS > ALL_CHAT_ADMINS > ALL_GROUP_CHATS > ALL_PRIVATE_CHATS > DEFAULT`

The more-specific scope wins. Hermes only writes commands to **DEFAULT scope**. If anything ever set a narrower scope (BotFather, an old one-off script, manual API call), Telegram persists it forever and silently hides the DEFAULT list in the affected chat type.

**Symptom:** user sees only N commands in their bot DM despite Hermes registering 100.

**Diagnose:**
```python
from telegram import Bot, BotCommandScopeAllPrivateChats
bot = Bot(token=...)
cmds = await bot.get_my_commands(scope=BotCommandScopeAllPrivateChats())
# If non-empty, that's the override hiding the DEFAULT list
```

**Fix:**
```python
await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
```

After clearing, the Telegram client aggressively caches the per-chat command list. Force-quit and reopen the Telegram app, or tap `/` in the chat to refresh.

**Prevention idea (not yet implemented):** add a startup check in `TelegramAdapter._initialize` that calls `get_my_commands` for each narrower scope (`AllPrivateChats`, `AllGroupChats`, `AllChatAdministrators`) and clears any non-empty conflicting list. Belt-and-suspenders against future drift.

## Streaming Reasoning Architecture (dual stream consumer)

When `display.show_reasoning: true` and `streaming.enabled: true`, the gateway creates **two** `GatewayStreamConsumer` instances per turn — one for the answer, one for reasoning.

### Why two consumers
The naive approach (gate streaming when reasoning is enabled) makes the answer arrive as a single blob and breaks the live UX. Worse, post-run reasoning send-after-answer is the wrong order — reasoning shows up *below* the answer instead of above, and gets read after the user already read the answer.

### Layout
- `gateway/stream_consumer.py` — `StreamConsumerConfig` has new fields:
  - `silent: bool = False` → passes `disable_notification=True` on first send
  - `header_prefix: str = ""` → prepended to every edit (e.g. `"💭 Reasoning:\n"`)
- `gateway/run.py` — when `show_reasoning` is on:
  1. Create answer consumer (existing) wired to `agent.stream_delta_callback`
  2. Create reasoning consumer with `silent=True, header_prefix="💭 Reasoning:\n"` wired to `agent.reasoning_callback`
  3. Start `reasoning_task` alongside `stream_task`
  4. Both `finish()` after the agent loop completes
  5. Both awaited in the `finally` block
- `gateway/platforms/base.py` — post-send hook checks `adapter._pending_reasoning_deletes[chat_id]` and calls `adapter.delete_message()` after the final answer is delivered, so the reasoning bubble auto-vanishes
- `gateway/platforms/telegram.py` — `delete_message(chat_id, message_id)` adapter method wrapping `bot.delete_message()`. Failures are non-fatal (48h API window limit)

### Cross-method state passing
The post-run one-shot reasoning fallback (`run.py:~2993`) needs to know whether streaming already delivered the reasoning, to suppress double-sending. The flag is passed via `agent_result["reasoning_streamed"]` rather than a closure variable, because the post-run block runs in a different scope from where the streaming bool is set.

### Auto-delete stash
On the streaming path, the reasoning consumer's `final_message_id` is captured immediately after `await reasoning_task` and either:
- Deleted inline (if the answer is already on screen)
- Stashed in `adapter._pending_reasoning_deletes[chat_id]` for the post-send hook to clean up after the answer lands

### Pitfalls specific to dual-consumer
1. **Don't share a consumer between answer and reasoning streams.** They have different message IDs, different silent flags, different header prefixes. One consumer per stream.
2. **`reasoning_callback` must be set BEFORE the agent starts running**, same as `stream_delta_callback`. Set both in the same code block.
3. **Both tasks must be awaited in `finally`**, not just on the happy path. Otherwise a mid-turn exception leaks the reasoning task.
4. **The `reasoning_streamed` flag must be set on `agent_result`**, not as a local variable. The fallback runs in a method that doesn't see locals from the streaming setup.
5. **Auto-delete races:** if the answer fails to send, leave the reasoning visible (debugging value). Only delete on successful answer delivery.
6. **Providers that don't emit reasoning deltas** (some models, some providers) fall back to the post-run one-shot send. The `reasoning_streamed` check makes this transparent.
