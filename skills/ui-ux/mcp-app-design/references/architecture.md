# MCP App Architecture

How to scaffold, declare, and wire up an MCP App that renders interactive HTML inside an MCP host conversation.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Dependencies](#dependencies)
3. [Server: Declaring a Tool with UI](#server-declaring-a-tool-with-ui)
4. [Server: Serving the UI Resource](#server-serving-the-ui-resource)
5. [Server: HTTP Transport](#server-http-transport)
6. [UI: The App Class](#ui-the-app-class)
7. [UI: Host Context and Theming](#ui-host-context-and-theming)
8. [UI: Calling Tools from the UI](#ui-calling-tools-from-the-ui)
9. [Build Configuration](#build-configuration)
10. [CSP and External Resources](#csp-and-external-resources)
11. [Testing](#testing)
12. [Framework Templates](#framework-templates)

---

## Project Structure

```
my-mcp-app/
├── package.json
├── tsconfig.json
├── vite.config.ts
├── server.ts              # MCP server — tool + resource registration
├── mcp-app.html           # UI entry point
└── src/
    ├── mcp-app.ts         # UI logic (App class, tool calls, DOM updates)
    ├── global.css          # Design tokens fallbacks + base styles
    └── mcp-app.css         # Component-specific styles
```

The server and UI are separate concerns. The server registers tools and serves bundled HTML. The UI runs in a sandboxed iframe and communicates back through the App class.

## Dependencies

```bash
# Runtime
npm install @modelcontextprotocol/ext-apps @modelcontextprotocol/sdk

# Dev
npm install -D typescript vite vite-plugin-singlefile express cors @types/express @types/cors tsx
```

- `@modelcontextprotocol/ext-apps` — App class (UI side), registerAppTool/registerAppResource (server side), style utilities
- `@modelcontextprotocol/sdk` — McpServer, StreamableHTTPServerTransport
- `vite-plugin-singlefile` — Bundles CSS/JS into a single HTML file (avoids CSP issues)

## Server: Declaring a Tool with UI

The key difference between a regular MCP tool and an MCP App tool is the `_meta.ui.resourceUri` field in the tool description. This tells the host to fetch and render a UI when the tool is called.

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { registerAppTool } from "@modelcontextprotocol/ext-apps/server";

const server = new McpServer({
  name: "My App Server",
  version: "1.0.0",
});

// ui:// scheme tells hosts this is an MCP App resource
const resourceUri = "ui://my-tool/mcp-app.html";

registerAppTool(
  server,
  "my-tool",             // Tool name
  {
    title: "My Tool",
    description: "Does something and shows results in a UI.",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Search query" },
      },
    },
    _meta: {
      ui: {
        resourceUri,
        // Optional: request additional iframe permissions
        // permissions: ["microphone", "camera"],
        // Optional: whitelist external script origins
        // csp: { "script-src": ["https://cdn.example.com"] },
      },
    },
  },
  async (args) => {
    // Tool logic — runs on the server
    const result = await doSomething(args.query);
    return {
      content: [
        { type: "text", text: JSON.stringify(result) },
      ],
    };
  },
);
```

### How it flows

1. LLM decides to call `my-tool` based on user's message
2. Host sees `_meta.ui.resourceUri` and preloads the UI resource
3. Host calls the tool and gets the result
4. Host renders the UI in a sandboxed iframe
5. Host pushes the tool result to the UI via `app.ontoolresult`

## Server: Serving the UI Resource

The resource handler serves the bundled HTML when the host requests it.

```typescript
import { registerAppResource, RESOURCE_MIME_TYPE } from "@modelcontextprotocol/ext-apps/server";
import fs from "node:fs/promises";
import path from "node:path";

registerAppResource(
  server,
  resourceUri,           // Must match the tool's _meta.ui.resourceUri
  resourceUri,
  { mimeType: RESOURCE_MIME_TYPE },
  async () => {
    const html = await fs.readFile(
      path.join(import.meta.dirname, "dist", "mcp-app.html"),
      "utf-8",
    );
    return {
      contents: [
        { uri: resourceUri, mimeType: RESOURCE_MIME_TYPE, text: html },
      ],
    };
  },
);
```

## Server: HTTP Transport

Expose the MCP server over HTTP using Streamable HTTP transport.

```typescript
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import cors from "cors";
import express from "express";

const expressApp = express();
expressApp.use(cors());
expressApp.use(express.json());

expressApp.post("/mcp", async (req, res) => {
  const transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: undefined,
    enableJsonResponse: true,
  });
  res.on("close", () => transport.close());
  await server.connect(transport);
  await transport.handleRequest(req, res, req.body);
});

expressApp.listen(3001, () => {
  console.log("Server listening on http://localhost:3001/mcp");
});
```

## UI: The App Class

The `App` class handles all communication between your UI and the host.

```typescript
import { App } from "@modelcontextprotocol/ext-apps";

const app = new App({ name: "My App", version: "1.0.0" });

// Establish communication with the host
app.connect();

// Handle the initial tool result pushed by the host
app.ontoolresult = (result) => {
  const data = result.content?.find((c) => c.type === "text")?.text;
  if (data) {
    renderData(JSON.parse(data));
  }
};
```

### Key App methods

| Method | Purpose |
|---|---|
| `app.connect()` | Establish postMessage communication with host. Call once on init. |
| `app.ontoolresult` | Callback: host pushes the initial tool result to your app |
| `app.onhostcontextchanged` | Callback: host pushes theme/style changes |
| `app.getHostContext()` | Get current host context (theme, styles, capabilities) |
| `app.callServerTool(opts)` | Call a tool on your MCP server from the UI |
| `app.callHostTool(opts)` | Call a tool on another MCP server connected to the host |
| `app.log(level, data)` | Send debug logs to the host console |
| `app.sendOpenLink(url)` | Request the host to open a URL in the browser |
| `app.updateContext(data)` | Push structured data to the model's context |

## UI: Host Context and Theming

See `design-tokens.md` for the full token system. The bridging code:

```typescript
import {
  applyDocumentTheme,
  applyHostStyleVariables,
  applyHostFonts,
} from "@modelcontextprotocol/ext-apps";

function applyHostContext(ctx) {
  if (ctx.theme) applyDocumentTheme(ctx.theme);
  if (ctx.styles?.variables) applyHostStyleVariables(ctx.styles.variables);
  if (ctx.styles?.css?.fonts) applyHostFonts(ctx.styles.css.fonts);
}

app.onhostcontextchanged = applyHostContext;
app.connect().then(() => {
  const ctx = app.getHostContext();
  if (ctx) applyHostContext(ctx);
});
```

## UI: Calling Tools from the UI

Users can interact with your UI directly, triggering tool calls without going through the LLM.

```typescript
// Call your own server's tool
const result = await app.callServerTool({
  name: "get-data",
  arguments: { query: "latest metrics" },
});

// Call a tool on another connected MCP server (requires host support)
const result2 = await app.callHostTool({
  name: "search",
  arguments: { q: "something" },
});
```

Each call is a round-trip to the server. Show loading states and handle errors:

```typescript
button.addEventListener("click", async () => {
  button.disabled = true;
  button.textContent = "Loading...";
  try {
    const result = await app.callServerTool({ name: "refresh", arguments: {} });
    updateUI(result);
  } catch (err) {
    showError(err.message);
  } finally {
    button.disabled = false;
    button.textContent = "Refresh";
  }
});
```

## Build Configuration

### package.json

```json
{
  "type": "module",
  "scripts": {
    "build": "INPUT=mcp-app.html vite build",
    "serve": "npx tsx server.ts",
    "dev": "npm run build && npm run serve"
  }
}
```

### vite.config.ts

```typescript
import { defineConfig } from "vite";
import { viteSingleFile } from "vite-plugin-singlefile";

export default defineConfig({
  plugins: [viteSingleFile()],
  build: {
    outDir: "dist",
    rollupOptions: {
      input: process.env.INPUT,
    },
  },
});
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "dist"
  },
  "include": ["*.ts", "src/**/*.ts"]
}
```

## CSP and External Resources

By default, the sandboxed iframe blocks external scripts. If you need CDN resources:

```typescript
registerAppTool(server, "my-tool", {
  // ...
  _meta: {
    ui: {
      resourceUri,
      csp: {
        "script-src": ["https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com"],
        "style-src": ["https://fonts.googleapis.com"],
        "font-src": ["https://fonts.gstatic.com"],
      },
    },
  },
}, handler);
```

Prefer bundling with `vite-plugin-singlefile` to avoid CSP configuration entirely.

## Testing

### Local testing with cloudflared

```bash
# Terminal 1: build and serve
npm run build && npm run serve

# Terminal 2: tunnel to internet
npx cloudflared tunnel --url http://localhost:3001
```

Add the generated URL as a custom connector in Claude (Settings → Connectors → Add custom connector).

### Testing with basic-host

```bash
git clone https://github.com/modelcontextprotocol/ext-apps.git
cd ext-apps/examples/basic-host
npm install
SERVERS='["http://localhost:3001/mcp"]' npm start
```

Navigate to `http://localhost:8080` — select your tool and call it to see the UI render.

## Framework Templates

Official starter templates exist for multiple frameworks. All follow the same pattern (server.ts + UI entry point + vite config):

| Framework | Example path |
|---|---|
| React | `examples/basic-server-react` |
| Vue | `examples/basic-server-vue` |
| Svelte | `examples/basic-server-svelte` |
| Preact | `examples/basic-server-preact` |
| Solid | `examples/basic-server-solid` |
| Vanilla JS | `examples/basic-server-vanillajs` |

All in `https://github.com/modelcontextprotocol/ext-apps/tree/main/examples`.

For MCP App iframes, **Preact is recommended over React** — smaller bundle size (~3KB vs ~40KB), same JSX API, and the iframe loads fresh each time so every KB matters.
