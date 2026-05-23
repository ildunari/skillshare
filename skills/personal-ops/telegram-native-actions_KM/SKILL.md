---
name: telegram-native-actions_KM
description: >-
  Use this whenever Kosta is chatting through Telegram and asks for richer Telegram behavior, bot UX ideas, polls, reactions, stickers, topic management, forum/group workflows, or asks whether/when Hermes should use Telegram-specific actions. Also use proactively when a Telegram-native action would be better than plain text: reacting to a message, making a quick poll, sending a location/contact/sticker, copying/forwarding a message, or managing Telegram forum topics.
---
# Telegram Native Actions

Hermes can use `telegram_actions` in Telegram sessions for native Bot API actions that plain `send_message` cannot do. Treat these as UX affordances, not gimmicks: use them when they make the conversation easier to scan, easier to decide on, or more Telegram-native.

## Available actions

Use `telegram_actions` for:

- `react` — add an emoji reaction to a specific message when a reaction is clearer than a text reply.
- `send_poll` — make a quick decision, preference check, vote, or lightweight async check-in.
- `send_location` / `send_venue` — share a place as a native Telegram card.
- `send_contact` — share a phone/contact card.
- `send_sticker` — send a sticker by file ID or URL when the user asks for playful Telegram behavior.
- `forward` / `copy` — move a message between chats when explicitly requested.
- `create_topic`, `edit_topic`, `close_topic`, `reopen_topic`, `delete_topic` — manage Telegram forum topics in groups.
- `set_profile_photo`, `remove_profile_photo` — change the bot’s profile photo when explicitly requested.

Use `send_message` for normal text/media delivery. Do not use `telegram_actions` to send ordinary text.

## Good defaults for Kosta

Prefer these patterns:

- If Kosta asks a yes/no or choose-between-options question in Telegram and a real decision from humans is needed, offer or create a poll instead of a long text thread.
- If Kosta sends a short acknowledgement-worthy message and no substantive reply is needed, react instead of cluttering the chat.
- In topic-enabled supergroups, create or rename topics for durable project lanes, audits, incidents, launches, or recurring workflows when Kosta asks for organization.
- For group/chat operations, use native Telegram affordances to keep work where the conversation is happening: summaries, polls, topic routing, onboarding/rules reminders, and admin-facing drafts.
- Keep destructive or identity-changing actions explicit: deleting topics, forwarding/copying between chats, changing bot profile photos, sending contacts/locations, or doing anything that affects other people’s chat experience.

## What to ask before acting

Ask one sharp question only when required data is missing:

- Reaction needs `message_id` unless the platform context exposes the replied-to message ID.
- Poll needs the question and 2–10 options. Choose sensible options if Kosta’s wording already contains them.
- Topic actions need target chat and topic/thread info unless the current chat/topic is obvious.
- Forward/copy needs source chat, destination chat, and message ID.
- Profile photo change needs a specific image path/URL and explicit confirmation because it is user-visible branding.

For reversible, low-risk actions in the current chat — reactions and simple polls — act when the intent is clear.

## Telegram AI-bot UX ideas from research

Observed common high-value patterns for Telegram AI bots:

- FAQ / repeated-answer relief: answer common questions immediately so core humans stop repeating themselves.
- Thread catch-up: summarize long group discussions for late arrivals or returning members.
- Multilingual bridge: answer in a member’s preferred language and help admins understand cross-language messages.
- Writing/research in-place: draft announcements, review wording, list trade-offs, and summarize research without leaving Telegram.
- Moderation support: explain rules, draft neutral reminders, flag possible violations for human review, and welcome/onboard new members.
- Community workflow: use polls for lightweight decisions, event planning, rosters, and preference checks.

The useful principle: do not just “chat like a website in Telegram.” Use Telegram’s native surfaces — reactions, polls, topics, and message actions — to reduce noise and make group decisions legible.

## Safety and etiquette

- Do not spam reactions or stickers. Use them sparingly when they reduce text clutter.
- Do not change bot profile photos, delete topics, forward messages, or share contacts/locations unless Kosta explicitly asks.
- In groups, assume actions are visible to others. Keep tone neutral and avoid playful actions in serious/debugging/incident contexts.
- Polls should be short and actionable. If a decision needs nuance, send a short framing message first, then the poll.
- Topic creation should produce clear, durable names, not clever labels.

## Verification

After enabling or changing Telegram action behavior, verify:

```bash
hermes --profile gpt plugins list | grep -A3 -B1 'telegram-actions'
hermes --profile default plugins list | grep -A3 -B1 'telegram-actions'
cd ~/.hermes/hermes-agent && python -m pytest tests/tools/test_telegram_actions_tool.py tests/gateway/test_tool_progress_compact.py tests/gateway/test_telegram_context_badge_connect.py tests/cli/test_compact_progress.py -q
```

Runtime health checks should show protected gateway routes healthy:

```bash
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8643/health
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8643/api/model-info  # 401 is expected without auth
```
