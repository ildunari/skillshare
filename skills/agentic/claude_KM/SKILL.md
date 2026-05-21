---
description: Use when Kosta invokes /claude from Hermes/Telegram and wants a Claude Code helper lane. Launch Claude Code with an interactive prefilled prompt when appropriate, rather than answering as Hermes directly.
metadata:
    targets:
        - antigravity
name: claude_KM---
# Claude Code Lane Shortcut

Use this skill as the short Telegram command `/claude` for Claude Code work.

Default behavior: if the user included a task after `/claude`, start or prepare a Claude Code helper lane for that task. Prefer the interactive prefill path because it keeps Claude Code on subscription/interactive auth instead of unnecessary `-p` / Agent SDK usage.

## Preferred launch pattern

Create a task prompt file, then launch Claude Code in a PTY/interactive session:

```bash
cat > /tmp/claude-task.md <<'EOF'
<task here>
EOF
claude --permission-mode auto --prefill "$(cat /tmp/claude-task.md)"
```

When launching through Hermes terminal tooling, use `pty=true`; for long lanes, use `background=true` and monitor with `process.poll` / `process.log`.

## When not to launch

Do not launch Claude Code if the request can be answered directly in one or two normal Hermes tool calls. Use Claude when the user explicitly asks for Claude/Claude Code or the task benefits from a separate coding lane, repo review, or long-running implementation.

Use `claude -p` / `--print` only for unattended scripts, CI, or required machine-readable JSON/stream-json capture.

## Response shape

If you launch a lane, report the session id and the exact task you gave Claude. If you only prepare the command because launching is unsafe or missing context, give the command and the reason briefly.
