---
name: context-control
description: Use when the session is long or tool output is huge. Keep context lean with compaction, focused logs, and clean handoffs.
---

## Tools to use selectively

- Use `/compact` only when context feels too heavy; do not auto‑compact.
- `/fork` to explore alternatives without polluting the main thread.
- `/status` to confirm token usage, model, and writable roots.
- Tune `tool_output_token_limit` if you keep hitting “missing logs” vs “too much noise”.

## Output discipline

- Prefer targeted outputs: grep, tail, file+line references.
- If a log is large, summarize and point to the exact command/file/line that matters.
- Keep a short “state of play” paragraph in the transcript when the task spans multiple turns.

## Hand-off

When stopping mid-task, leave:
- current status,
- what’s already verified,
- the next single command to run.
