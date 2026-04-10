---
name: mcp-server-builder
description: Build production-quality MCP servers — both standard tool servers and MCP App servers with inline interactive UI (iframes in Claude.ai). Use this skill whenever the user wants to create an MCP server, build a connector for Claude, make a remote MCP tool, add interactive UI to an MCP server, bypass the 1MB tool-result size limit with MCP Apps, or work with the ext-apps SDK. Also triggers on "MCP App", "interactive connector", "inline iframe", "structuredContent", "registerAppTool", "ui:// resource", "Streamable HTTP server", or any task involving the @modelcontextprotocol/sdk or @modelcontextprotocol/ext-apps packages. Always use this skill even for modifications to existing MCP servers, debugging MCP transport issues, or adding MCP Apps UI to a server that currently only returns text/data.
---

# MCP Server Builder

<!-- Merged from: mcp-proxy-builder, mcp-operations (2026-04-05). Legacy material preserved under merged/. -->

> Build standard MCP tool servers and MCP App servers (with inline interactive UI) for Claude.ai, Claude Desktop, and other MCP hosts. Covers both Streamable HTTP remote servers and stdio local servers.

## Feedback Loop

When the user gives feedback on outputs from this skill (corrections, bugs, missing patterns, new gotchas), log it:

1. **Detect**: User says something went wrong, a pattern didn't work, or suggests improvement.
2. **Search**: Check `FEEDBACK.md` for duplicates.
3. **Scope**: Determine category and whether it affects SKILL.md or a reference file.
4. **Draft and ask**: Propose the feedback entry to the user for approval.
5. **Write on approval**: Append to `FEEDBACK.md` with category tag.
6. **Compact at 75**: When entries hit 75, summarize older entries and fold insights into the skill/reference files.

---

## Decision: standard server vs MCP App

Before writing code, determine which type the user needs:

| Need | Server type | Key difference |
|---|---|---|
| Tools that return text, JSON, structured data | **Standard MCP server** | Tools return `content` array with text/images |
| Tools that render interactive UI inline in chat | **MCP App server** | Tools declare `_meta.ui.resourceUri`, HTML renders in sandboxed iframe |
| Tools that return large binary data (images, PDFs) | **MCP App server** | Bypasses 1MB tool-result limit via `structuredContent` + iframe |
| Tools that need user interaction after invocation | **MCP App server** | Iframe can call back to server, update model context, send messages |

If the user's server needs to return images, render charts, display interactive content, or bypass the 1MB limit, it's an MCP App. Otherwise, a standard server is simpler.

---

## Quick reference: verified SDK versions (February 2026)

| Package | Version | Role |
|---|---|---|
| `@modelcontextprotocol/sdk` | **1.26.0** | Server runtime, transports, protocol types |
| `@modelcontextprotocol/ext-apps` | **1.0.1** | MCP Apps: `registerAppTool`, `registerAppResource`, client `App` class |
| `vite` + `vite-plugin-singlefile` | 6.x / 0.13.x | Bundle App HTML into single file |

Always verify these against npm before starting — the SDK iterates fast.

---

## Standard MCP server

### Architecture

A standard MCP server exposes tools, resources, and prompts over a transport (Streamable HTTP for remote, stdio for local). Claude discovers tools via `tools/list` and calls them via `tools/call`.

### Key patterns

**Factory pattern (required for Streamable HTTP).** Create a new `McpServer` instance per request for stateless operation. A shared singleton causes state collisions with concurrent users.

```typescript
// server.ts
export function createServer(): McpServer {
  const server = new McpServer({ name: "My Server", version: "1.0.0" });
  // register tools here
  return server;
}

// main.ts — new server per request
app.all("/mcp", async (req, res) => {
  const server = createServer();
  const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined });
  res.on("close", () => { transport.close().catch(() => {}); server.close().catch(() => {}); });
  await server.connect(transport);
  await transport.handleRequest(req, res, req.body);
});
```

**Use `createMcpExpressApp`** from `@modelcontextprotocol/sdk/server/express.js` instead of raw Express. It sets up correct defaults.

**Zod for input schemas.** The SDK accepts Zod schemas directly — use them consistently.

**`structuredContent` for rich data.** Even in standard servers, `structuredContent` lets you return typed data alongside text `content`. Clients that understand it get structured access; others fall back to the text.

**Tool annotations.** Always include `readOnlyHint`, `destructiveHint`, `idempotentHint` for each tool. Helps hosts make safe decisions about automatic tool calling.

**For complete standard server patterns, read:** `references/standard-server.md`

---

## MCP App server

MCP Apps extend a standard server with interactive UI. A tool declares a `ui://` resource; when Claude calls the tool, the host renders the HTML in a sandboxed iframe and pipes the tool result to the iframe via postMessage.

### When to use MCP Apps

- Displaying images, charts, maps, or any visual content inline in Claude
- Bypassing the 1MB tool-result size limit (images, PDFs, large data)
- Adding interactive controls (regenerate buttons, parameter sliders, pagination)
- Streaming partial results with live preview
- Any tool where "seeing" the output matters more than reading text about it

### Core architecture

```text
Server <── MCP (Streamable HTTP) ──> Host (Claude.ai) <── postMessage (JSON-RPC) ──> View (iframe)
```

Two registration calls link tool to UI:

1. `registerAppTool(server, name, config, handler)` — tool with `_meta.ui.resourceUri`
2. `registerAppResource(server, name, uri, options, handler)` — serves the bundled HTML

The host fetches the HTML, renders it in a sandboxed iframe, and delivers the tool result via the App Bridge (postMessage JSON-RPC).

### Image delivery strategies

| Strategy | When | How |
|---|---|---|
| **Direct structuredContent** | Images under ~2-3MB | Return base64 in `structuredContent`; View renders as data URI |
| **Chunked app-only tool** | Large images, maximum safety | Return `imageId`; View calls `read_image_bytes` in 500KB chunks via App Bridge |

The chunked pattern is officially documented and recommended for binaries. It avoids all size limit concerns.

### Critical rules (the top 3 bugs)

1. **Register ALL event handlers BEFORE calling `app.connect()`.** If you register `ontoolresult` after `connect()`, you miss the initial tool result. This is the single most common MCP App bug.

2. **Bundle everything into one HTML file.** The iframe runs under deny-by-default CSP. Separate JS/CSS files require CSP declarations and are nearly impossible to debug on Claude.ai web. Use `vite-plugin-singlefile`.

3. **Separate `content` from `structuredContent`.** `content` is small text for the model's context window. `structuredContent` is rich data for the View, hidden from the model. This separation is what bypasses the 1MB limit.

### Complete MCP App implementation guide

**Read `references/mcp-apps-guide.md` for:**
- Full lifecycle walkthrough (5 phases)
- Complete server code with factory pattern, image store, TTL cleanup
- Complete client code with chunked loading, progress bar, theme adaptation
- Vite build setup with dual tsconfigs
- Capability negotiation and fallback for non-App hosts
- CSP, CORS, and `_meta.ui.domain` configuration
- Platform support matrix
- All debugging techniques and known cross-client bugs

### Claude.ai-specific behaviors

**Read `references/claude-host.md` for:**
- Default CSP string
- Sandbox restrictions
- CORS domain computation (`sha256(serverUrl).slice(0,32).claudemcpcontent.com`)
- Display modes (inline, fullscreen)
- Platform support (web, desktop, mobile)
- Transport requirements (Streamable HTTP + SSE)

### MCP Apps patterns (from official ext-apps docs)

**Read `references/mcp-apps-patterns.md` for:**
- App-only tools (hidden from model)
- Chunked binary loading (the full pattern with server + client code)
- Binary blob resources
- CSP and CORS configuration with examples
- Host theme adaptation (CSS variables, fonts, safe areas)
- Fullscreen toggle
- Model context updates from the View
- Large follow-up messages
- View state persistence
- Pausing heavy views when offscreen
- Streaming partial tool input for preview

---

## Project setup checklist

### Standard server

```text
my-mcp-server/
├── package.json        (type: module, @modelcontextprotocol/sdk ^1.26.0)
├── tsconfig.json
├── server.ts           (createServer factory, tool registrations)
└── main.ts             (createMcpExpressApp, transport, shutdown)
```

### MCP App server

```text
my-mcp-app/
├── package.json        (+ @modelcontextprotocol/ext-apps ^1.0.1, vite, vite-plugin-singlefile)
├── tsconfig.json       (DOM libs for client code)
├── tsconfig.server.json (NodeNext for server code)
├── vite.config.ts      (viteSingleFile plugin)
├── server.ts           (createServer factory, registerAppTool, registerAppResource)
├── main.ts             (createMcpExpressApp, transport, shutdown)
├── mcp-app.html        (entry point for View)
└── src/
    └── mcp-app.ts      (App class, ontoolresult, callServerTool)
```

---

## Connector registration (Claude.ai)

Claude.ai requires a public HTTPS URL. For local dev:

```bash
npx cloudflared tunnel --url http://localhost:3001
# Connector URL: https://<random>.trycloudflare.com/mcp
```

1. **Settings → Connectors → Add custom connector**
2. Paste your public URL
3. Enable per-conversation via **"+" → Connectors** in the chat composer

Team/Enterprise: Org owner adds in Admin Settings first.

---

## Testing and debugging

**MCP Inspector:** `npx @modelcontextprotocol/inspector` — validate tools/resources outside Claude.

**ext-apps basic-host:** Clone `github.com/modelcontextprotocol/ext-apps`, run `examples/basic-host` — renders MCP App iframes with browser DevTools access.

**Claude Desktop DevTools:** Help → Troubleshooting → Enable Developer Mode → `Cmd+Option+I`. Navigate DOM tree to find the inner iframe.

**Claude.ai web:** No iframe DevTools access. Bundle everything into one file and test with the basic-host first.

---

## Common mistakes

| Mistake | Fix |
|---|---|
| SDK version `^1.0.0` | Use `^1.26.0` — the SDK has iterated heavily |
| Shared `McpServer` singleton | Factory pattern: `createServer()` per request |
| `app.post("/mcp")` | `app.all("/mcp")` — Streamable HTTP uses multiple methods |
| Handlers registered after `connect()` | Set `ontoolresult`, `ontoolinput`, `ontoolinputpartial` BEFORE `app.connect()` |
| Separate JS/CSS files in App HTML | Bundle with `vite-plugin-singlefile` — CSP blocks external assets |
| `enableJsonResponse: true` in transport | Omit — not in official docs, may cause unexpected behavior |
| Large base64 in `content` array | Use `structuredContent` for View data, keep `content` small for model |
| No `content` text fallback | Always include meaningful text — non-App hosts only see `content` |
| `localStorage` in Claude artifacts | Blocked in sandbox. Use `window.storage` (Anthropic API) or in-memory state |
| No image TTL / cleanup | Add `setInterval` to sweep expired images from your store |
