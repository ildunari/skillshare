# Telegram Native Actions — Research Notes

Sources checked 2026-05-08:

- Telegram Bot API docs: https://core.telegram.org/bots/api
- Qualtir, “5 Use Cases for an AI Assistant in Telegram Group Chats”: https://qualtir.com/es/blog/ai-assistant-telegram-group-use-cases/
- FlowHunt, “Telegram Bot: Ultimate Guide”: https://www.flowhunt.io/blog/telegram-bot-the-ultimate-guide/
- Search snippets for Telegram Bot API / chatbot builder / n8n bot examples.

## Useful patterns

Telegram AI assistants are most useful when they reduce group/admin load and keep workflows inside the chat:

1. FAQ / repeated-answer relief — answer common product/community questions without core members repeating themselves.
2. Long-thread catch-up — summarize recent discussions for late arrivals, returning users, or busy team members.
3. Multilingual bridge — answer users in their preferred language and help admins understand cross-language messages.
4. Writing/research in-place — draft announcements, review wording, list tradeoffs, explain concepts, and summarize research without context switching.
5. Moderation support — explain rules, draft polite reminders, flag possible violations for human review, and onboard new members.
6. Community workflow — polls for event planning, team rosters, preference checks, and lightweight decisions.

## Design principle

A Telegram bot should not behave like a web chat transplanted into Telegram. It should use native Telegram surfaces when they reduce friction: reactions for acknowledgements, polls for decisions, forum topics for durable work lanes, copy/forward for message routing, and native cards for locations/contacts.

## Safety notes

Bots cannot initiate conversations with users who have not interacted with them. Group actions are visible and social; use native actions sparingly. Destructive/admin actions should be explicit, especially deleting topics, forwarding/copying across chats, and changing bot profile photos.
