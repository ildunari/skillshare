# Smart update Telegram DM-topic regression guard — 2026-05-09

Context: a smart update merged upstream into `local/studio-customizations`. The merge completed and many checks passed, but Telegram DM-topic final replies regressed: progress/tool HUD bubbles still appeared in the selected topic while final assistant replies landed in All or were missing from the topic.

Validated cause:

- The merge brought back `direct_messages_topic_id` handling in `gateway/platforms/telegram.py:_thread_kwargs_for_send()`.
- It also allowed stale reply-anchor retry paths to drop `message_thread_id`.
- Existing focused tests did not fully encode the local invariant, so the smart update could pass while losing visible Telegram placement.

Correction applied after the fact:

- Commit: `338a75988 Preserve Telegram DM topic routing after update`
- Focused tests: `92 passed` for Telegram topic/DM/newthread/context/compact-progress coverage.

Smart-update lesson:

- Passing API/miniapp health checks and compact HUD tests is not enough for Telegram topic UX.
- If `gateway/platforms/telegram.py`, `gateway/stream_consumer.py`, or Telegram tests changed/conflicted, inspect the diff for topic kwargs, not just test status.
- Preserve these invariants:
  - Hermes DM/private topic sends use `message_thread_id=<topic>` for visible placement.
  - Do not use `direct_messages_topic_id` for Hermes normal sends unless a future live proof reverses the finding.
  - Private-topic retries must not fall back unthreaded into All.
  - Stale reply-anchor retries may drop `reply_to_message_id`, but must keep `message_thread_id`.

Recommended post-merge grep:

```bash
git diff origin/main...HEAD -- gateway/platforms/telegram.py gateway/stream_consumer.py tests/gateway \
  | grep -nE 'direct_messages_topic_id|message_thread_id|telegram_dm_topic_reply_fallback|reply_to_message_id'
```

Recommended focused test set:

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

If these tests fail because expectations still allow `direct_messages_topic_id` or missing `message_thread_id`, treat the test as stale rather than treating upstream as correct; re-validate against live Telegram Bot API/client placement before changing the invariant.
