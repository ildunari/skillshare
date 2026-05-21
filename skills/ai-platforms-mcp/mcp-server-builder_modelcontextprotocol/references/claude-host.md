# Claude.ai host behaviors and constraints

Claude-specific details for MCP servers and MCP Apps running as connectors in Claude.ai.

## Table of contents

- Platform support matrix
- Transport requirements
- Connector registration
- Sandbox and CSP (MCP Apps)
- CORS domain computation
- Display modes
- Known limitations
- Debugging on Claude

---

## Platform support

| Platform | Add connectors | Use tools/prompts/resources | Interactive connectors (MCP Apps) |
|---|---|---|---|
| Claude web (claude.ai) | Yes | Yes | Yes |
| Claude Desktop | Yes (via claude.ai settings) | Yes | Yes |
| Claude Mobile (iOS/Android) | No | Yes | No |

Interactive connectors (MCP Apps with inline iframe UI) require Claude web or Claude Desktop. Mobile can use standard tools but will not render App iframes.

---

## Transport requirements

Claude.ai supports:
- **Streamable HTTP** (recommended, long-term support)
- **SSE** (supported but deprecation is planned)

Both auth-less and OAuth servers are supported. For public connectors, OAuth is recommended.

Your server must be accessible over **HTTPS**. For local development, use Cloudflare Tunnel:

```bash
npx cloudflared tunnel --url http://localhost:3001
# Connector URL: https://<random>.trycloudflare.com/mcp
```

---

## Connector registration

### Individual (Pro/Max)

1. Go to **Settings → Connectors** at `claude.ai/settings/connectors`
2. Click **"Add custom connector"**
3. Paste your HTTPS server URL (e.g., `https://abc123.trycloudflare.com/mcp`)
4. If using OAuth, expand **"Advanced settings"** and enter client ID/secret
5. Click **"Add"**

### Team/Enterprise

An Organization Owner adds the connector in **Admin Settings → Connectors**. Members then connect individually from their Settings page.

### Enabling per conversation

Click the **"+"** button in the chat composer → select **"Connectors"** → toggle your connector on. Claude will then have access to your server's tools.

---

## Sandbox and CSP (MCP Apps)

All MCP App Views run in sandboxed iframes. The sandbox blocks:
- Access to the parent DOM
- Host cookies
- `localStorage` and `sessionStorage`
- Parent navigation
- Popups

### Default CSP

```text
default-src 'none';
script-src 'unsafe-inline';
style-src 'unsafe-inline';
img-src data:;
media-src data:;
connect-src 'none'
```

This means:
- Inline scripts and styles work (bundled via vite-plugin-singlefile)
- Data URIs work for images and media (so base64 via structuredContent works)
- **No external network requests** unless you declare domains in `_meta.ui.csp`
- **No fetch/XHR** to any URL unless declared in `connectDomains`

### Declaring CSP exceptions

Set `_meta.ui.csp` in the resource `contents[]` array (not in `registerAppResource` config):

```typescript
contents: [{
  uri: resourceUri,
  mimeType: RESOURCE_MIME_TYPE,
  text: html,
  _meta: {
    ui: {
      csp: {
        connectDomains: ["https://api.example.com"],    // fetch/XHR/WebSocket
        resourceDomains: ["https://cdn.jsdelivr.net"],   // scripts, images, fonts
      },
    },
  },
}]
```

**Best practice:** Avoid needing CSP exceptions. Bundle everything into one HTML file and use the App Bridge (`app.callServerTool()`) for all server communication. This eliminates CSP and CORS headaches entirely.

---

## CORS domain computation

Claude assigns each MCP App a stable origin derived from the server URL:

```text
${sha256(serverUrl).slice(0,32)}.claudemcpcontent.com
```

Compute it server-side:

```typescript
import crypto from "node:crypto";

function computeAppDomainForClaude(mcpServerUrl: string): string {
  return crypto
    .createHash("sha256")
    .update(mcpServerUrl)
    .digest("hex")
    .slice(0, 32) + ".claudemcpcontent.com";
}
```

Set this in `_meta.ui.domain` if your App iframe needs to make direct fetch requests to an API that allowlists specific origins. If you use the App Bridge for all communication, you don't need this.

---

## Display modes

Claude supports:

| Mode | Behavior |
|---|---|
| **inline** | Embedded in chat flow (default) |
| **fullscreen** | Takes over the window, composer still accessible |

The View can request mode changes:

```typescript
const ctx = app.getHostContext();
if (ctx?.availableDisplayModes?.includes("fullscreen")) {
  await app.requestDisplayMode({ mode: "fullscreen" });
}
```

Listen for mode changes:

```typescript
app.onhostcontextchanged = (ctx) => {
  if (ctx.displayMode === "fullscreen") {
    container.style.borderRadius = "0";
  }
};
```

Picture-in-picture is spec-defined but not confirmed for Claude.ai as of February 2026.

---

## The 1MB tool-result limit

Claude enforces a **1MB limit on the `content` array** of tool results. This is a host-side constraint, not a protocol limit.

**What counts toward 1MB:** The `content` array (text blocks, image blocks — what enters the model's context window).

**What does NOT count:** `structuredContent` is delivered to the View via postMessage, not through the model content channel. This is the architectural insight that lets MCP Apps bypass the limit.

**Cost consideration:** 1MB of tool output ≈ $1 per request in API billing, and it's billed in every follow-up message. Even without the hard limit, keeping `content` small is economically important.

---

## Known limitations

### No iframe DevTools on Claude.ai web

You cannot access the iframe's console or network tab on claude.ai. CSP violations fail silently. **Always test with the ext-apps basic-host first** (gives you full browser DevTools), then deploy to Claude.ai.

### Claude Desktop DevTools

Enable via **Help → Troubleshooting → Enable Developer Mode**, then press `Cmd+Option+I` (macOS) or `Ctrl+Shift+I` (Windows/Linux). Navigate the DOM tree to find the inner iframe containing your App.

### Working directory undefined (macOS)

Claude Desktop may launch servers with an undefined working directory. Always use absolute paths:

```typescript
const DIST_DIR = path.join(import.meta.dirname, "dist");
```

Specify environment variables explicitly in `claude_desktop_config.json`.

### structuredContent cross-client bugs (February 2026)

| Client | Bug |
|---|---|
| VS Code | Ignores `content` when `structuredContent` is present; sends only stringified structured content to model |
| OpenAI Codex | Drops image blocks from `content` when `structuredContent` exists |
| LangChain MCP adapters | Ignores `structuredContent` entirely |

**Mitigation:** Always include meaningful text in `content` as a standalone fallback. Never assume `structuredContent` will be delivered — it's an enhancement, not a replacement.

### ext-apps SDK issues

- **Issue #367:** npm install fails with peer dependency conflicts. Use `--legacy-peer-deps` or pin versions.
- **Issue #225:** `app.onhostcontextchanged` is a property assignment, not `addEventListener`. Assigning it twice silently overwrites the first handler. Compose all logic into a single function.

---

## Host theme adaptation

Claude provides CSS variables and theme info via the host context. Use them to match Claude's look and feel:

```css
:root {
  font-family: var(--font-sans, system-ui, -apple-system, sans-serif);
  background: var(--color-background-primary, #fff);
  color: var(--color-text-primary, #111);
}

[data-theme="dark"] {
  color-scheme: dark;
}
```

```typescript
app.onhostcontextchanged = (ctx) => {
  if (ctx.theme) {
    document.documentElement.setAttribute("data-theme", ctx.theme);
  }
};

// Apply initial theme after connect
await app.connect();
const ctx = app.getHostContext();
if (ctx?.theme) {
  document.documentElement.setAttribute("data-theme", ctx.theme);
}
```

See the ext-apps Patterns doc for the full list of CSS variables (`McpUiStyleVariableKey`).
