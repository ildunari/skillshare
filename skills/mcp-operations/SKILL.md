---
name: mcp-operations
description: Use when configuring or troubleshooting MCP tools (Context7, OpenAI Developer Docs MCP, Exa, Firecrawl, OAuth logins).
---

## Add MCP servers (CLI)

Preferred: configure with the CLI, then verify in `/mcp`.

Examples:

- Context7 (docs)
  `codex mcp add context7 -- npx -y @upstash/context7-mcp`

- OpenAI Developer Docs MCP (official)
  `codex mcp add openaiDeveloperDocs --url https://developers.openai.com/mcp`

Use the OpenAI Developer Docs MCP whenever you work with OpenAI APIs/SDKs.

After adding:
- `codex mcp list`
- In TUI: `/mcp`

## OAuth for streamable HTTP servers

If the server requires OAuth:
- Use `codex mcp login <name> --scopes scope1,scope2` (only if the server supports OAuth).
- If callbacks fail, set `mcp_oauth_callback_port` in config.

## Troubleshooting checklist

- Confirm the server appears in `/mcp`.
- If it’s configured but not loading, check:
  - the command/path is correct,
  - startup timeout (increase `startup_timeout_sec`),
  - env vars are passed correctly (`env` vs `env_vars`),
  - server tool names aren’t blocked by `disabled_tools`.
