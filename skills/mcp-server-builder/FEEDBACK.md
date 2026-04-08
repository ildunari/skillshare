# MCP Server Builder — Skill Feedback Log

<!-- MUST-READ: Claude MUST read this file whenever loading the mcp-server-builder skill. -->
<!-- CATEGORIES: sdk, transport, mcp-apps, structuredContent, csp-cors, chunking, vite-build, claude-host, debugging, patterns, fallback, auth, deployment -->
<!-- CAP: 75 entries. When reached, summarize and compact older entries. -->

## Entries

### 1. [mcp-apps] Do NOT use server.tool() + server.resource() for MCP Apps — use registerAppTool/registerAppResource
**Date:** 2026-04-07
**Category:** mcp-apps
Using raw `server.tool()` with `_meta.ui.resourceUri` and `server.resource()` with manual MIME type strings does NOT trigger inline iframe rendering in Claude Desktop. You MUST use `registerAppTool()` and `registerAppResource()` from `@modelcontextprotocol/ext-apps/server`. These helpers handle the capability negotiation and metadata wiring correctly. Without them, Claude sees the tool but renders raw JSON instead of the interactive iframe.

### 2. [mcp-apps] Tool result must use structuredContent, not just content text
**Date:** 2026-04-07
**Category:** structuredContent
The form schema (or any View-facing data) must go in `structuredContent`, not in `content[].text`. The `content` array is for the model's context window (small text summary). The `structuredContent` is delivered to the iframe View via postMessage and never enters the model's context. Putting the schema in `content` means the View never receives it.

### 3. [vite-build] Set build target to "esnext" when using ext-apps App class
**Date:** 2026-04-07
**Category:** vite-build
The `App` class from `@modelcontextprotocol/ext-apps` uses top-level `await` for `app.connect()`. Vite's default build target (`es2020`) does not support top-level await. Set `build.target: "esnext"` in vite.config.ts. The MCP App iframe runs in a modern browser (Claude Desktop / claude.ai) that supports ESNext features.

### 4. [mcp-apps] HTML JS must be in a separate .ts module for ext-apps import
**Date:** 2026-04-07
**Category:** mcp-apps
Inline `<script>` tags cannot use ES module imports. The `App` class from `@modelcontextprotocol/ext-apps` must be imported via `import { App } from "@modelcontextprotocol/ext-apps"`. Extract all JS into a separate `.ts` file (e.g., `src/mcp-app.ts`) and reference it as `<script type="module" src="./mcp-app.ts"></script>`. Vite + vite-plugin-singlefile will bundle everything into a single HTML file at build time.
