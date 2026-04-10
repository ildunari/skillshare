---
name: word-mcp-bridge
description: Operate the Word MCP Bridge stack — live Word taskpane sessions via local HTTPS bridge plus stdio MCP server. Use for reading live Word context, listing sessions, calling bridge tools, VFS helpers, running privileged Office.js, CLI debugging, session inspection, watch-selection, or troubleshooting bridge connectivity. Triggers on word mcp bridge, office-bridge, bridge MCP, call_bridge_tool, list_sessions, localhost 4017, mcp-serve, bridge serve, watch-selection, live Word selection/context, or troubleshooting "no bridge sessions" / add-in not connected.
---

# Word MCP Bridge

Operate the **Word MCP Bridge** stack after the bridge package and Word add-in are installed. The stack has two complementary interfaces — MCP tools (structured, from within an MCP host) and the `office-bridge` CLI (terminal-first, scripts, streaming). Pick the right one for the job.

## When to use MCP vs CLI

**Prefer MCP tools** when you're inside an MCP-capable host (Claude Code, Claude Desktop, Cursor, Codex) and want structured tool calls: session discovery, snapshots, live context, recent events, `call_bridge_tool`, VFS read/write, or gated `run_unsafe_office_js`. Implementation lives in `packages/bridge/src/mcp.ts`.

**Prefer the CLI** (`office-bridge` command, `packages/bridge/src/cli.ts`) for terminal-first workflows, shell scripts, CI, long-running streams, or features not exposed as MCP tools: `watch-selection`, `watch-context`, `poll`, `screenshot`, `dom`, `assert`, `bench`, `vfs pull`/`push` to local disk paths, `reset`, etc.

## Two processes (do not skip)

1. **`office-bridge serve`** — local HTTPS/WebSocket bridge the Word taskpane connects to (default `https://localhost:4017`).
2. **`office-bridge mcp-serve`** — MCP host launches this; it talks to the bridge URL (often `--url https://localhost:4017`).

From the repo: `pnpm bridge:serve` starts the server; `pnpm bridge:mcp` runs `pnpm exec office-bridge mcp-serve`. Hosted-add-in users still run `serve` locally per `README.md`.

## MCP tools (stdio server)

Registered in `packages/bridge/src/mcp.ts`:

| Tool | Role |
|------|------|
| `list_sessions` | List connected bridge sessions. |
| `get_session_snapshot` | Refresh and return full session snapshot (state, capabilities, gateway context). Optional `session` selector. |
| `get_live_context` | Live context slice (e.g. selection) via `refresh_session`. Optional `session`. |
| `get_recent_events` | Recent events; `limit` 1-200, default 20. Optional `session`. |
| `call_bridge_tool` | Run a named bridge tool with `args`. Optional `session`. Respect session capability boundaries. |
| `run_unsafe_office_js` | Privileged Office.js **only** if the session exposes `unsafe_office_js`. `code` required; `explanation` optional. |
| `vfs_list` | List VFS paths; optional `prefix`. |
| `vfs_read` | Read VFS file; `path`; `encoding` `text` or `base64`. |
| `vfs_write` | Write VFS file; `path`; `text` and/or `dataBase64`. |
| `vfs_delete` | Delete VFS path. |

**Session selector:** If exactly one session exists, `session` can be omitted. If multiple sessions exist, pass an unambiguous selector.

## CLI command reference

| Goal | Command |
|------|---------|
| See if anything is connected | `office-bridge list` |
| One-line human status | `office-bridge summary word` |
| Full session snapshot | `office-bridge snapshot word` / `--compact` / `--fields key1,key2` |
| Recent bridge events | `office-bridge events word --limit 20` |
| Stream live selection | `office-bridge watch-selection word` |
| Bridge server / CLI self-check | `office-bridge status` |
| Start bridge | `office-bridge serve` |
| MCP stdio for hosts | `office-bridge mcp-serve [--url URL]` |
| Rich state dump | `office-bridge state word --compact` |
| Event stream / polling | `office-bridge poll word` |

Global output shaping: `--compact`, `--fields`, `--max-tokens` (events); `--url` for non-default bridge base.

## Setup

**Local dev (repo):** `pnpm install`, `pnpm setup:word`, `pnpm bridge:serve`, `pnpm dev-server:word`, `pnpm start:word`, open the Word MCP Bridge taskpane; then `office-bridge list`, `summary word`, `snapshot word`, etc.

**MCP host config:** Copy-paste patterns in `packages/bridge/README.md` for Claude Desktop JSON, Cursor `mcp.json`, `claude mcp add`, `codex mcp add`, `~/.codex/config.toml`.

**Auth:** Default token path usually works when bridge and MCP run as the same user; otherwise set `OFFICE_BRIDGE_TOKEN` per `packages/bridge/README.md`.

## Troubleshooting

- **Empty `list` / "No bridge sessions" / MCP tools fail** — Confirm `office-bridge serve` is up, Word taskpane is open, and add-in shows a connected bridge.
- **Wrong bridge** — Pass `--url` consistently on CLI subcommands and `mcp-serve`.
- **TLS / localhost** — Bridge TLS is localhost-oriented.
- **`run_unsafe_office_js` unavailable** — Session must advertise the capability; prefer `call_bridge_tool` with documented tool names when possible.
- **Auth / HTTPS issues** — Ensure MCP `--url` matches the running bridge. Set `OFFICE_BRIDGE_TOKEN` if needed.
- **More CLI commands** (`inspect`, `tool`, `exec`, `vfs`, `diag`, `dom`, ...): see usage in `packages/bridge/src/cli.ts`.

## Reference files

- `README.md` — Repo overview, dev commands, hosted add-in mode, bundle output.
- `packages/bridge/README.md` — Install modes, CLI cheat sheet, MCP host snippets, `OFFICE_BRIDGE_TOKEN`.
- `packages/bridge/src/mcp.ts` — MCP tool registry and behavior.
- `packages/bridge/src/cli.ts` — Full CLI surface and usage text.
