# Archived skill: hermes-claude-subscription-auth

Original path: `/Users/Kosta/.hermes/profiles/gpt/skills/hermes/hermes-claude-subscription-auth`
Absorbed into umbrella: `hermes-provider-media-configuration` on 2026-04-29.

---

---
name: hermes-claude-subscription-auth
summary: Test and wire Hermes to use Claude Code / Claude Max subscription authentication instead of Anthropic API keys.
description: Diagnose or implement Hermes access to Anthropic Claude through Claude Code subscription auth, Claude Max/Pro setup-token, OpenClaw-style claude-cli reuse, or CLAUDE_CODE_OAUTH_TOKEN. Use whenever the user wants Hermes to use their Claude Max/Pro subscription instead of expensive Anthropic API keys, asks whether OpenClaw Claude auth applies to Hermes, mentions `claude setup-token`, `CLAUDE_CODE_OAUTH_TOKEN`, `claude -p`, or wants a Hermes `claude-cli` provider lane.
---

# Hermes Claude Subscription Auth

Use this when Kosta wants Hermes to use Claude Code / Claude Max subscription auth rather than Anthropic API keys.

## Position

Prefer a `claude-cli` provider lane that shells through authenticated Claude Code (`claude -p`) before trying to make Hermes direct Anthropic API calls with subscription OAuth tokens. That route matches the currently safer OpenClaw-style interpretation: reuse Claude CLI auth, not arbitrary third-party API-key replacement.

Do not steer Kosta toward Anthropic API keys as the default. He considers them too expensive and prefers his Max x20 subscription when possible.

## Fast checks

Confirm Claude Code itself works without Anthropic API env vars:

```bash
env -u ANTHROPIC_API_KEY -u ANTHROPIC_TOKEN -u CLAUDE_CODE_OAUTH_TOKEN \
  claude -p 'Reply with exactly OK' --model sonnet
```

Expected: `OK`. If this works, Claude Code subscription auth is usable on the machine even if Hermes direct Anthropic auth is not.

Check Hermes direct credential visibility:

```bash
cd ~/.hermes/hermes-agent
source .venv/bin/activate
env -u ANTHROPIC_API_KEY -u ANTHROPIC_TOKEN -u CLAUDE_CODE_OAUTH_TOKEN python - <<'PY'
from hermes_cli.auth import get_anthropic_key
key = get_anthropic_key()
print('has_key', bool(key), 'prefix', key[:12] if key else '')
PY
```

If `has_key False`, Hermes does not currently have a native Anthropic credential to test.

## setup-token caveat

`claude setup-token` needs a real raw TTY because Claude Code uses Ink. From Hermes/Telegram/background shell it can fail or hang with:

```text
Raw mode is not supported on the current process.stdin, which Ink uses as input stream by default.
```

Use a real terminal or Screen Sharing session for setup-token. Do not keep retrying from a non-interactive Telegram shell.

## Direct OAuth token test, if token exists

Only run this if Kosta explicitly has a fresh `CLAUDE_CODE_OAUTH_TOKEN` available in the environment. Never print or save the token.

Test both likely header modes with a tiny request, because OpenClaw reports have differed on whether `Authorization: Bearer` or `x-api-key` works for `sk-ant-oat01-*` tokens:

```bash
# Bearer style, similar to many SDK auth_token paths
curl https://api.anthropic.com/v1/messages \
  -H "Authorization: Bearer $CLAUDE_CODE_OAUTH_TOKEN" \
  -H "anthropic-beta: claude-code-20250219,oauth-2025-04-20" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-sonnet-4-5-20250929","max_tokens":16,"messages":[{"role":"user","content":"ok"}]}'

# x-api-key style, reported by OpenClaw issues as working for setup tokens
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $CLAUDE_CODE_OAUTH_TOKEN" \
  -H "anthropic-beta: claude-code-20250219,oauth-2025-04-20" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-sonnet-4-5-20250929","max_tokens":16,"messages":[{"role":"user","content":"ok"}]}'
```

If `x-api-key` works and Bearer fails, patch Hermes `agent/anthropic_adapter.py` and doctor/auth checks so Claude Code OAuth setup tokens are sent with the working header plus the beta headers. Add focused tests around header selection.

If both direct token modes fail but `claude -p` works, implement the `claude-cli` provider lane instead.

## Recommended Hermes implementation path

1. Add a provider/backend named something like `claude-cli`.
2. For non-tool plain turns, call `claude -p <prompt>` with the selected model and capture stdout.
3. Put the prompt before variadic flags like `--add-dir` when using Claude Code print mode.
4. Start with simple non-streaming text turns; tool parity can come later.
5. Add tests that mock subprocess execution and verify env vars do not require Anthropic API keys.
6. Document the tradeoff clearly: this uses Claude Code subscription auth and local Claude CLI behavior, not the Anthropic Messages API.

## Claude Code as a Hermes subagent lane

Do not use `delegate_task(acp_command="claude", acp_args=["--acp", "--stdio"])`. Current Claude Code does **not** expose a native `--acp` flag; `claude --acp --stdio` exits with `unknown option '--acp'` on Claude Code 2.1.119.

For Claude Code work launched by Hermes, prefer a normal subprocess lane:

```bash
claude -p --output-format json --model sonnet \
  --permission-mode plan \
  --append-system-prompt-file .hermes/prompts/claude-planning.md \
  "<task prompt>"
```

Use `--agent <name>` when you want a configured Claude Code agent, for example `--agent design-agent-claude`. Use `--agents '<json>'` for ephemeral session-local agents. Use `--tools` to restrict available tools, and `--allowedTools` only to auto-approve specific tools that are already available. For unattended read-only planning/review, `--permission-mode plan` is the safer default; for controlled implementation, use narrow `--tools` / `--allowedTools` rather than broad bypass mode.

If Hermes truly needs ACP transport to Claude Code, launch a real ACP adapter, not the raw `claude` binary. The current npm package is `@agentclientprotocol/claude-agent-acp` and exposes the `claude-agent-acp` binary, so the Hermes ACP override shape is roughly:

```python
delegate_task(
    goal="...",
    context="...",
    acp_command="npx",
    acp_args=["-y", "@agentclientprotocol/claude-agent-acp"],
)
```

That ACP path should be tested before relying on it; the simpler and more transparent Claude Code lane is still `claude -p` from a terminal subprocess.

## Reporting

When reporting back, distinguish these states:

- `Claude Code subscription auth works` — verified by `claude -p` with Anthropic env vars unset.
- `Hermes native Anthropic OAuth works` — verified by Hermes/curl using a setup token.
- `Hermes can use Claude via CLI bridge` — implemented/tested `claude-cli` provider lane.

Do not collapse those into one vague “Claude auth works” claim.
