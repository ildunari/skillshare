# Telegram DM-topic post-update regression — 2026-05-09

Context: after `/update_smart`, Telegram progress/tool HUD bubbles still appeared in the selected DM topic, but final assistant replies leaked to All / were missing from the topic. Kosta also noticed markdown weirdness, which made the routing problem easier to spot.

Root cause found in `gateway/platforms/telegram.py` after the upstream merge:

- `_thread_kwargs_for_send()` had reintroduced a path where metadata containing `direct_messages_topic_id` produced `direct_messages_topic_id=<topic>` and `message_thread_id=None`.
- Stale reply-anchor retries for text/media could drop `message_thread_id` along with `reply_to_message_id`.
- Live Bot API testing for this setup had already shown `direct_messages_topic_id=<topic>` returns OK but visibly behaves like All, while `message_thread_id=<topic>` returns `is_topic_message=True` and lands in the selected topic.

Fix committed locally:

- `338a75988 Preserve Telegram DM topic routing after update`
- `_thread_kwargs_for_send()` always preserves `message_thread_id` for topic sends when a thread id exists.
- Stale reply-anchor retry removes only the reply anchor, not the topic kwarg.
- Tests in `tests/gateway/test_telegram_thread_fallback.py` now assert that private/DM topic sends, stale reply retries, and media retries keep `message_thread_id` and do not use `direct_messages_topic_id`.

Why the smart update missed it:

- The smart update ran broad Telegram tests, but the merged test expectations still allowed the bad upstream behavior in some cases.
- The post-update regression check did not explicitly assert the invariant “DM topic final replies and retry paths never use `direct_messages_topic_id` and never drop `message_thread_id`.”
- API/miniapp route checks and compact HUD checks are necessary but insufficient; this failure is visible only in Telegram client placement or exact Bot API kwargs.

Future invariant:

- For Hermes-created Telegram DM/private topics, normal text sends, streaming/final sends, inline keyboard sends, and media sends must use `message_thread_id=<topic>` for visible placement.
- Never retry private-topic sends unthreaded into All. If Telegram rejects a topic id, surface the failure rather than leaking the response.
- If a reply anchor is stale/deleted, retry without `reply_to_message_id` but keep `message_thread_id`.

Useful focused checks:

```bash
cd ~/.hermes/hermes-agent
.venv/bin/python -m pytest \
  tests/gateway/test_telegram_thread_fallback.py \
  tests/gateway/test_dm_topics.py \
  tests/gateway/test_newthread_command.py \
  tests/gateway/test_telegram_context_badge_connect.py \
  tests/gateway/test_tool_progress_compact.py \
  tests/cli/test_compact_progress.py -q
```

Expected current result after the fix: `92 passed` for the focused set above.
