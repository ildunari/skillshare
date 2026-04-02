---
name: serena
description: Use when you need symbol-level code navigation or refactoring with Serena instead of plain-text search, especially in larger codebases or when local HTTP-proxied Serena setup may need activation.
source: https://github.com/oraios/serena
---

# Serena

Use Serena when you need IDE-like symbol understanding instead of plain text search.

## What Serena is for

- Finding symbol definitions
- Tracking references across files
- Making precise insertions or refactors at symbol boundaries
- Reducing full-file reads in larger codebases

Prefer Serena over `rg` when symbol semantics matter. Use `rg` when you just need text matching.

## How to use it in Codex

If Serena tools are already available in the session, use them directly.

If they are not available yet, first check which startup model applies:

1. **Local HTTP proxy workflow on this machine**
   Register the repo with the local proxy helper:

```bash
/Users/kosta/.local/bin/serena-proxy-register /path/to/repo
```

This writes a repo-local MCP entry to `.codex/config.toml` pointing at:

```text
http://127.0.0.1:3016/servers/<slug>/mcp
```

It also creates or updates `.serena/project.yml` on first index/create as needed.

Important:
- New MCP entries may require a fresh Codex session rooted in that repo before tools appear.
- The local helper is the preferred path here when Serena is served over HTTP.

2. **Direct Serena MCP workflow**
   Start Serena directly when the proxy helper is unavailable or you need a standalone server:

```bash
uvx --from git+https://github.com/oraios/serena \
  serena start-mcp-server --project-from-cwd --context desktop-app
```

For HTTP transport instead of stdio:

```bash
uvx --from git+https://github.com/oraios/serena \
  serena start-mcp-server --project-from-cwd --context desktop-app \
  --transport streamable-http --host 127.0.0.1 --port 8000
```

Recommended MCP startup sequence once tools are live:

> Call `serena.activate_project`, `serena.check_onboarding_performed`, and `serena.initial_instructions`.

If the project is not initialized yet, create or index it first so Serena can create `.serena/project.yml`.

## Common workflow

1. Activate the project.
2. Run `check_onboarding_performed`; if false, run onboarding.
3. Run `initial_instructions` when the client does not automatically load Serena guidance.
4. Find the relevant symbol.
5. Inspect references before changing behavior.
6. Make the smallest symbol-level edit that solves the problem.

## CLI fallback

If you need to run Serena manually outside the MCP tools, use:

```bash
uvx --from git+https://github.com/oraios/serena serena <command>
```

Useful commands:

- `start-mcp-server`
- `project create /path/to/repo --name <name> [--language <lang>]`
- `project index`
- `project health-check`
- `tools list`

Notes on current CLI behavior:
- Project lifecycle commands now live under `serena project ...`.
- `activate_project`, `check_onboarding_performed`, and `initial_instructions` are MCP tools, not current top-level CLI subcommands.
- `serena project index /path/to/repo --name <name>` auto-creates `.serena/project.yml` if missing.

## Notes

- Serena works best on structured codebases.
- First-time project setup may create `.serena/project.yml`.
- On this machine, the HTTP proxy helper is usually the fastest way to make Serena available to Codex.
- Socket files, generated artifacts, and large vendor trees may slow indexing; trim them with `.serena/project.local.yml` when needed.
