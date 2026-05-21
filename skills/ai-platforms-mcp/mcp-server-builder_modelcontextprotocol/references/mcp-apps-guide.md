# MCP Apps for Claude.ai: corrected implementation guide

**MCP Apps let a remote MCP server render interactive HTML inline in Claude.ai conversations, bypassing the 1MB tool-result size limit.** Instead of returning base64 images in tool results, the server registers a bundled HTML resource and a linked tool. When Claude invokes the tool, the host fetches the HTML, renders it in a sandboxed iframe, and pipes the tool result to the iframe via postMessage. The image data flows through `structuredContent` (which is delivered to the View, not the model's context window), so it never hits the tool-result payload limit.

The extension (SEP-1865, identifier `io.modelcontextprotocol/ui`) shipped January 26, 2026. Supported hosts as of February 2026: Claude web, Claude Desktop, VS Code Insiders, Goose, ChatGPT, Postman, and MCPJam.

**SDK stack (verified February 11, 2026):**

| Package | Latest version | Role |
|---|---|---|
| `@modelcontextprotocol/sdk` | **1.26.0** | MCP server runtime, transports |
| `@modelcontextprotocol/ext-apps` | **1.0.1** | `registerAppTool`, `registerAppResource`, client `App` class |
| `@mcp-ui/server` | (optional) | `createUIResource` convenience helper with validation |
| `vite` + `vite-plugin-singlefile` | 6.x / 0.13.x | Bundle HTML + JS + CSS into one file |

---

## How the lifecycle works

Three entities: **Server** (your remote Streamable HTTP endpoint), **Host** (Claude.ai), and **View** (sandboxed iframe running your bundled HTML).

```text
Server <── MCP (Streamable HTTP) ──> Host (Claude.ai) <── postMessage (JSON-RPC) ──> View (iframe)
```

**1. Connection and capability negotiation.** Claude sends `initialize`. Check `capabilities.extensions["io.modelcontextprotocol/ui"].mimeTypes` for `"text/html;profile=mcp-app"`. If present, register UI-enabled tools. If absent, fall back to text-only tools.

**2. Tool and resource discovery.** Claude calls `tools/list`. Your server returns tool definitions with `_meta.ui.resourceUri` pointing to a `ui://` URI. Claude calls `resources/read` to fetch the HTML.

**3. Tool invocation.** Claude sends `tools/call`. Your handler returns `content` (small text for the model's context) and `structuredContent` (rich data for the View, hidden from the model).

**4. Iframe rendering and data delivery.** Claude fetches the HTML resource, injects it into a sandboxed iframe, runs a postMessage handshake (`ui/initialize` → host context → `ui/notifications/initialized`), then pushes `ui/notifications/tool-input` and `ui/notifications/tool-result` containing the structuredContent. The View receives the image data and renders it.

**5. Interactive phase.** The iframe can call server tools via `app.callServerTool()`, read resources via `app.request()`, update model context via `app.updateModelContext()`, send messages via `app.sendMessage()`, and request fullscreen via `app.requestDisplayMode()`. All communication is auditable JSON-RPC over postMessage.

---

## How this bypasses the 1MB limit

The 1MB limit is a Claude host constraint on the `content` array of tool results (the text that enters the model's context window). MCP Apps change where image bytes go:

- **Small path (images under ~2-3MB compressed):** Return the base64 in `structuredContent`. This is delivered to the View via postMessage, not through the model's content channel. The model only sees your small text in `content`.

- **Large path (images over ~2-3MB, or you want maximum safety):** Use the **chunked app-only tool** pattern. The primary tool returns an `imageId` in `structuredContent`. The View calls a hidden `read_image_bytes` tool in 500KB chunks via the App Bridge, assembles the chunks into a Blob, and displays it. This is an officially documented pattern in the ext-apps Patterns guide.

For typical AI-generated images (Gemini output compressed to WebP), the small path works. The chunked path is an escape hatch for very large payloads or if you want to guarantee no size issues regardless of image dimensions.

---

## Claude.ai-specific host behaviors

**Sandbox and CSP.** Default CSP is strict:

```text
default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; media-src data:; connect-src 'none'
```

No external network requests unless you declare domains in `_meta.ui.csp`. Data URIs work for images by default (so `structuredContent` → data URI → `<img>` works without CSP changes).

**All server communication is mediated by the host.** The iframe cannot `fetch()` your MCP server directly. Use `app.callServerTool()` or `app.request()` -- the host proxies these over the MCP transport. This is by design for auditability and security.

**CORS domain computation.** Claude assigns each MCP App a stable origin: `${sha256(serverUrl).slice(0,32)}.claudemcpcontent.com`. If your App makes direct external fetches (with CSP declared), compute and set `_meta.ui.domain`.

**Display modes.** Claude supports **inline** (embedded in chat flow) and **fullscreen**. The View can request changes via `app.requestDisplayMode({ mode: "fullscreen" })`.

**Platform support:**

| Platform | Add connectors | Use tools/prompts | Interactive connectors (MCP Apps) |
|---|---|---|---|
| Claude web (claude.ai) | Yes | Yes | Yes |
| Claude Desktop | Yes (via claude.ai settings) | Yes | Yes |
| Claude Mobile (iOS/Android) | No | Yes | No |

Claude.ai supports Streamable HTTP and SSE transports (SSE deprecation planned). Auth-less and OAuth servers both supported.

---

## Server implementation

### Project layout

```text
claude-image-mcp-app/
  package.json
  tsconfig.json
  tsconfig.server.json
  vite.config.ts
  main.ts
  server.ts
  mcp-app.html
  src/
    mcp-app.ts
```

### package.json

```json
{
  "name": "claude-image-mcp-app",
  "private": true,
  "type": "module",
  "scripts": {
    "build": "tsc --noEmit && cross-env INPUT=mcp-app.html vite build",
    "dev": "concurrently 'cross-env NODE_ENV=development INPUT=mcp-app.html vite build --watch' 'tsx watch main.ts'",
    "serve": "tsx main.ts"
  },
  "dependencies": {
    "@modelcontextprotocol/ext-apps": "^1.0.1",
    "@modelcontextprotocol/sdk": "^1.26.0",
    "express": "^4.21.0",
    "cors": "^2.8.5",
    "zod": "^3.24.0"
  },
  "devDependencies": {
    "typescript": "^5.7.0",
    "vite": "^6.0.0",
    "vite-plugin-singlefile": "^0.13.0",
    "tsx": "^4.19.0",
    "concurrently": "^9.0.0",
    "cross-env": "^7.0.3",
    "@types/express": "^5.0.0",
    "@types/cors": "^2.8.0",
    "@types/node": "^22.0.0"
  }
}
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "lib": ["ESNext", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,
    "noEmit": true,
    "strict": true,
    "skipLibCheck": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src", "server.ts", "main.ts"]
}
```

### tsconfig.server.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "declaration": true,
    "emitDeclarationOnly": true,
    "outDir": "./dist",
    "rootDir": ".",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["server.ts", "main.ts"]
}
```

### vite.config.ts

```typescript
import { defineConfig } from "vite";
import { viteSingleFile } from "vite-plugin-singlefile";

const INPUT = process.env.INPUT;
if (!INPUT) throw new Error("INPUT environment variable is not set");

const isDevelopment = process.env.NODE_ENV === "development";

export default defineConfig({
  plugins: [viteSingleFile()],
  build: {
    sourcemap: isDevelopment ? "inline" : undefined,
    cssMinify: !isDevelopment,
    minify: !isDevelopment,
    rollupOptions: { input: INPUT },
    outDir: "dist",
    emptyOutDir: false,
  },
});
```

### server.ts

This uses the **factory pattern** -- `createServer()` returns a new `McpServer` per request. This is required for stateless Streamable HTTP with concurrent users.

Two image delivery strategies are shown: direct `structuredContent` (simpler, works for images under ~2-3MB) and the chunked app-only tool (for larger payloads). Use one or both.

```typescript
import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";
import { z } from "zod";

import {
  registerAppResource,
  registerAppTool,
  RESOURCE_MIME_TYPE,
} from "@modelcontextprotocol/ext-apps/server";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";

const DIST_DIR = path.join(import.meta.dirname, "dist");
const APP_RESOURCE_URI = "ui://image-gen/mcp-app.html";
const MAX_CHUNK_BYTES = 500 * 1024; // 500KB per chunk (safe under host limits after base64 inflation)
const IMAGE_TTL_MS = 15 * 60 * 1000; // 15 minute retention

// --- In-memory image store (swap for Redis/S3 in production) ---

type StoredImage = { mimeType: string; bytes: Buffer; createdAt: number };
const imageStore = new Map<string, StoredImage>();

// Sweep expired images every 5 minutes
setInterval(() => {
  const now = Date.now();
  for (const [id, img] of imageStore) {
    if (now - img.createdAt > IMAGE_TTL_MS) imageStore.delete(id);
  }
}, 5 * 60 * 1000);

function randomId(prefix: string): string {
  return `${prefix}_${crypto.randomBytes(16).toString("hex")}`;
}

// --- Gemini integration (replace with your actual implementation) ---

async function generateWithGemini(prompt: string): Promise<{ mimeType: string; bytes: Buffer }> {
  // Replace this stub with your working Gemini image generation code.
  // Requirements: return image bytes as a Buffer and a mimeType string.
  const fake = Buffer.from(`Stub image for: ${prompt}`);
  return { mimeType: "image/webp", bytes: fake };
}

// --- Server factory ---

export function createServer(): McpServer {
  const server = new McpServer({
    name: "Claude Image MCP App",
    version: "1.0.0",
  });

  // --- UI resource: bundled single-file HTML ---

  registerAppResource(
    server,
    APP_RESOURCE_URI,
    APP_RESOURCE_URI,
    { mimeType: RESOURCE_MIME_TYPE },
    async () => {
      const html = await fs.readFile(path.join(DIST_DIR, "mcp-app.html"), "utf-8");
      return {
        contents: [
          {
            uri: APP_RESOURCE_URI,
            mimeType: RESOURCE_MIME_TYPE,
            text: html,
            // Uncomment and configure if your iframe needs direct external network access:
            // _meta: {
            //   ui: {
            //     csp: {
            //       connectDomains: ["https://api.example.com"],
            //       resourceDomains: ["https://cdn.jsdelivr.net"],
            //     },
            //   },
            // },
          },
        ],
      };
    }
  );

  // --- Tool: generate image (visible to model + app) ---
  //
  // Strategy A (direct structuredContent): For images under ~2-3MB compressed,
  // return the base64 directly in structuredContent. Simpler, fewer round trips.
  //
  // Strategy B (chunked): For larger payloads, return only an imageId and let
  // the View fetch bytes via the read_image_bytes app-only tool. More robust.
  //
  // This implementation uses Strategy B for maximum safety. To use Strategy A,
  // put `imageBase64: bytes.toString("base64")` in structuredContent instead of
  // imageId, and skip the read_image_bytes tool entirely.

  registerAppTool(
    server,
    "generate_image",
    {
      title: "Generate image",
      description:
        "Generate an image from a text prompt and display it inline via an MCP App.",
      inputSchema: {
        prompt: z.string().describe("Image generation prompt"),
      },
      _meta: { ui: { resourceUri: APP_RESOURCE_URI } },
    },
    async ({ prompt }) => {
      const { mimeType, bytes } = await generateWithGemini(prompt);

      const imageId = randomId("img");
      imageStore.set(imageId, { mimeType, bytes, createdAt: Date.now() });

      return {
        // Model-facing content (small text, stays under 1MB easily)
        content: [
          { type: "text", text: `Generated image (${mimeType}, ${bytes.length} bytes) for: "${prompt}"` },
        ],
        // View-facing data (delivered via postMessage, not model context)
        structuredContent: {
          imageId,
          mimeType,
          byteLength: bytes.length,
          prompt,
        },
      };
    }
  );

  // --- App-only tool: read image bytes in chunks (hidden from model) ---

  registerAppTool(
    server,
    "read_image_bytes",
    {
      title: "Read image bytes",
      description: "Load image data in chunks. App-only — not visible to the model.",
      inputSchema: {
        imageId: z.string().describe("Image identifier from generate_image"),
        offset: z.number().min(0).default(0).describe("Byte offset to start reading from"),
        byteCount: z.number().default(MAX_CHUNK_BYTES).describe("Number of bytes to read"),
      },
      outputSchema: z.object({
        bytes: z.string(),
        offset: z.number(),
        byteCount: z.number(),
        totalBytes: z.number(),
        hasMore: z.boolean(),
        mimeType: z.string(),
      }),
      _meta: { ui: { visibility: ["app"] } },
    },
    async ({ imageId, offset = 0, byteCount = MAX_CHUNK_BYTES }) => {
      const stored = imageStore.get(imageId);
      if (!stored) {
        return {
          isError: true,
          content: [{ type: "text", text: `Unknown imageId: ${imageId}` }],
        };
      }

      const total = stored.bytes.length;
      const safeCount = Math.min(byteCount, MAX_CHUNK_BYTES);
      const chunk = stored.bytes.subarray(offset, Math.min(offset + safeCount, total));

      return {
        content: [{ type: "text", text: `${chunk.length} bytes at offset ${offset}` }],
        structuredContent: {
          bytes: chunk.toString("base64"),
          offset,
          byteCount: chunk.length,
          totalBytes: total,
          hasMore: offset + chunk.length < total,
          mimeType: stored.mimeType,
        },
      };
    }
  );

  // --- App-only tool: regenerate image (hidden from model) ---

  registerAppTool(
    server,
    "regenerate_image",
    {
      title: "Regenerate image",
      description: "Regenerate with a modified prompt. App-only.",
      inputSchema: {
        prompt: z.string(),
      },
      _meta: {
        ui: {
          resourceUri: APP_RESOURCE_URI,
          visibility: ["app"],
        },
      },
    },
    async ({ prompt }) => {
      const { mimeType, bytes } = await generateWithGemini(prompt);

      const imageId = randomId("img");
      imageStore.set(imageId, { mimeType, bytes, createdAt: Date.now() });

      return {
        content: [{ type: "text", text: "Regenerated." }],
        structuredContent: { imageId, mimeType, byteLength: bytes.length, prompt },
      };
    }
  );

  return server;
}
```

### main.ts

Uses `createMcpExpressApp` from the SDK (the official Express helper) and creates a **new server per request** for stateless operation.

```typescript
import { createMcpExpressApp } from "@modelcontextprotocol/sdk/server/express.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import cors from "cors";
import type { Request, Response } from "express";
import { createServer } from "./server.js";

const port = parseInt(process.env.PORT ?? "3001", 10);

const app = createMcpExpressApp({ host: "0.0.0.0" });
app.use(cors());

app.all("/mcp", async (req: Request, res: Response) => {
  const server = createServer();
  const transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: undefined, // Stateless mode. Add session management for production.
  });

  res.on("close", () => {
    transport.close().catch(() => {});
    server.close().catch(() => {});
  });

  try {
    await server.connect(transport);
    await transport.handleRequest(req, res, req.body);
  } catch (error) {
    console.error("MCP error:", error);
    if (!res.headersSent) {
      res.status(500).json({
        jsonrpc: "2.0",
        error: { code: -32603, message: "Internal server error" },
        id: null,
      });
    }
  }
});

const httpServer = app.listen(port, () => {
  console.log(`MCP server listening on http://localhost:${port}/mcp`);
});

const shutdown = () => {
  console.log("\nShutting down...");
  httpServer.close(() => process.exit(0));
};

process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);
```

### mcp-app.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <style>
    :root { font-family: var(--font-sans, system-ui, -apple-system, Segoe UI, Roboto, sans-serif); }
    [data-theme="dark"] { color-scheme: dark; }
    body {
      margin: 0; padding: 16px;
      background: var(--color-background-primary, #fff);
      color: var(--color-text-primary, #111);
    }
    img {
      max-width: 100%;
      border-radius: var(--border-radius-lg, 12px);
      border: 1px solid rgba(128, 128, 128, 0.15);
    }
    #loading { text-align: center; padding: 2rem; opacity: 0.6; }
    #progress-wrap {
      height: 6px; border-radius: 999px; background: rgba(128,128,128,0.12);
      overflow: hidden; display: none; margin-top: 10px;
    }
    #progress-bar { height: 100%; width: 0%; background: rgba(128,128,128,0.4); transition: width 0.2s; }
    #meta {
      margin-top: 10px; white-space: pre-wrap;
      background: rgba(128,128,128,0.06); padding: 10px;
      border-radius: 10px; font-size: 0.85em; display: none;
    }
    button {
      margin-top: 8px; padding: 8px 16px; cursor: pointer;
      border-radius: var(--border-radius-lg, 8px);
      border: 1px solid rgba(128,128,128,0.2);
      background: var(--color-background-primary, #fff);
      color: var(--color-text-primary, #111);
    }
    button:hover { background: rgba(128,128,128,0.08); }
  </style>
</head>
<body>
  <div id="loading">Generating image...</div>
  <div id="progress-wrap"><div id="progress-bar"></div></div>
  <img id="generated-image" style="display:none" alt="Generated image" />
  <p id="prompt-text" style="opacity:0.7; font-size:0.9em;"></p>
  <pre id="meta"></pre>
  <button id="regenerate-btn" style="display:none">Regenerate</button>
  <script type="module" src="./src/mcp-app.ts"></script>
</body>
</html>
```

### src/mcp-app.ts

```typescript
import { App } from "@modelcontextprotocol/ext-apps";

// --- DOM references ---

const loadingEl = document.getElementById("loading")!;
const imageEl = document.getElementById("generated-image") as HTMLImageElement;
const promptEl = document.getElementById("prompt-text")!;
const metaEl = document.getElementById("meta") as HTMLPreElement;
const regenBtn = document.getElementById("regenerate-btn")!;
const progressWrap = document.getElementById("progress-wrap")!;
const progressBar = document.getElementById("progress-bar")!;

let currentPrompt = "";

// --- Helpers ---

function setProgress(pct: number) {
  progressWrap.style.display = "block";
  progressBar.style.width = `${Math.max(0, Math.min(100, pct))}%`;
}

function hideProgress() {
  progressWrap.style.display = "none";
  progressBar.style.width = "0%";
}

function base64ToBytes(b64: string): Uint8Array {
  const bin = atob(b64);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}

// --- Chunked image loading via app-only tool ---

interface Chunk {
  bytes: string;
  offset: number;
  byteCount: number;
  totalBytes: number;
  hasMore: boolean;
  mimeType: string;
}

async function loadImageChunked(
  app: App,
  imageId: string
): Promise<{ mimeType: string; blob: Blob }> {
  const chunks: Uint8Array[] = [];
  let offset = 0;
  let total = 0;
  let mimeType = "application/octet-stream";
  let hasMore = true;

  while (hasMore) {
    const result = await app.callServerTool({
      name: "read_image_bytes",
      arguments: { imageId, offset, byteCount: 500 * 1024 },
    });

    if (result.isError || !result.structuredContent) {
      throw new Error("Failed to read image bytes");
    }

    const c = result.structuredContent as unknown as Chunk;
    total = c.totalBytes;
    mimeType = c.mimeType;
    hasMore = c.hasMore;

    chunks.push(base64ToBytes(c.bytes));
    offset += c.byteCount;
    setProgress(total > 0 ? (offset / total) * 100 : 0);
  }

  const full = new Uint8Array(total);
  let pos = 0;
  for (const chunk of chunks) {
    full.set(chunk, pos);
    pos += chunk.length;
  }

  return { mimeType, blob: new Blob([full], { type: mimeType }) };
}

// --- Display result ---

async function displayResult(app: App, sc: Record<string, unknown>) {
  const imageId = sc.imageId as string | undefined;
  const prompt = sc.prompt as string | undefined;

  if (prompt) {
    promptEl.textContent = prompt;
    currentPrompt = prompt;
  }

  metaEl.style.display = "block";
  metaEl.textContent = JSON.stringify(sc, null, 2);

  if (!imageId) {
    loadingEl.textContent = "No imageId in tool result.";
    return;
  }

  try {
    loadingEl.textContent = "Loading image...";
    loadingEl.style.display = "block";
    imageEl.style.display = "none";
    hideProgress();

    const { blob } = await loadImageChunked(app, imageId);
    const url = URL.createObjectURL(blob);

    imageEl.src = url;
    imageEl.style.display = "block";
    loadingEl.style.display = "none";
    regenBtn.style.display = "inline-block";
    hideProgress();
  } catch (err: unknown) {
    hideProgress();
    const msg = err instanceof Error ? err.message : String(err);
    loadingEl.textContent = `Error: ${msg}`;
  }
}

// --- App lifecycle ---
// CRITICAL: Register ALL handlers BEFORE calling app.connect().
// If you register after connect(), you will miss the initial tool result.

const app = new App({ name: "Claude Image App", version: "1.0.0" });

// Receive the initial tool result when generate_image completes
app.ontoolresult = (result) => {
  const sc = (result.structuredContent ?? {}) as Record<string, unknown>;
  void displayResult(app, sc);
};

// Stream partial tool input for preview (shows prompt as it's being typed)
app.ontoolinputpartial = (params) => {
  const partial = params.arguments?.prompt as string;
  if (partial) promptEl.textContent = `Generating: ${partial}...`;
};

// Adapt to host theme changes
app.onhostcontextchanged = (ctx) => {
  if (ctx.theme) {
    document.documentElement.setAttribute("data-theme", ctx.theme);
  }
};

// Connect to host (after all handlers are set)
await app.connect();

// Apply initial theme
const ctx = app.getHostContext();
if (ctx?.theme) {
  document.documentElement.setAttribute("data-theme", ctx.theme);
}

// Regenerate button
regenBtn.addEventListener("click", async () => {
  if (!currentPrompt) return;
  loadingEl.textContent = "Regenerating...";
  loadingEl.style.display = "block";
  imageEl.style.display = "none";
  regenBtn.style.display = "none";
  hideProgress();

  try {
    const result = await app.callServerTool({
      name: "regenerate_image",
      arguments: { prompt: currentPrompt },
    });
    const sc = (result.structuredContent ?? {}) as Record<string, unknown>;
    await displayResult(app, sc);
  } catch (err: unknown) {
    const msg = err instanceof Error ? err.message : String(err);
    loadingEl.textContent = `Error: ${msg}`;
  }
});
```

---

## Registering as a connector in Claude.ai

Claude.ai requires a public HTTPS URL. For local development, use Cloudflare Tunnel:

```bash
npx cloudflared tunnel --url http://localhost:3001
# Produces: https://abc123.trycloudflare.com
# Connector URL: https://abc123.trycloudflare.com/mcp
```

**Pro/Max (individual):**

1. Go to **Settings → Connectors** at `claude.ai/settings/connectors`
2. Click **"Add custom connector"**
3. Paste your server URL (e.g., `https://abc123.trycloudflare.com/mcp`)
4. If using OAuth, expand **"Advanced settings"** and enter client ID/secret
5. Click **"Add"**

**Team/Enterprise:** An org owner adds the connector in **Admin Settings → Connectors**, then members connect individually.

**Per-conversation:** Click **"+"** in the chat composer, select **"Connectors"**, toggle your connector on.

---

## Choosing an image delivery strategy

| Strategy | When to use | Pros | Cons |
|---|---|---|---|
| **A: Direct structuredContent** | Images under ~2-3MB (WebP-compressed Gemini output) | Simpler code, one round trip, no server-side storage | Untested at the exact boundary; may hit undocumented limits |
| **B: Chunked app-only tool** | Large images, or you want maximum robustness | Officially documented pattern, no size concerns, works for any binary | More code, multiple round trips, requires server-side image store |
| **A+B: Both with fallback** | Production systems | Best of both: try direct first, fall back to chunked | Most complex to implement |

For Strategy A, the server returns `imageBase64: bytes.toString("base64")` in `structuredContent` and the View renders it as `data:${mimeType};base64,${imageBase64}`. No `read_image_bytes` tool needed.

For Strategy B (what the code above implements), the server stores bytes and returns an `imageId`. The View fetches chunks via the App Bridge.

**Recommendation:** Start with Strategy B (chunked). It's only ~30 more lines of code, it's the officially documented pattern for binaries, and you'll never have to wonder if you're hitting size limits.

---

## Capability negotiation and fallback

For non-App hosts (Claude Code, other MCP clients), your tool still runs but no iframe renders. Use `getUiCapability()` to detect support and provide a text-only fallback:

```typescript
import { getUiCapability, RESOURCE_MIME_TYPE } from "@modelcontextprotocol/ext-apps/server";

// Inside your createServer function, after server initialization:
const uiCap = getUiCapability(clientCapabilities);
if (uiCap?.mimeTypes?.includes(RESOURCE_MIME_TYPE)) {
  // Register UI-enabled tools with _meta.ui.resourceUri
} else {
  // Register text-only fallback tools (return image URL or description)
}
```

Even without capability negotiation, your tool's `content` text serves as a natural fallback -- non-App hosts display it as normal tool output. The `_meta.ui` metadata is simply ignored.

---

## Debugging and failure modes

**"The UI never appears."** Most common causes: (1) Claude mobile (doesn't support interactive connectors), (2) tool definition missing `_meta.ui.resourceUri`, (3) `ui://` resource not registered or unreadable, (4) server unreachable (network/TLS/CORS), (5) server not speaking Streamable HTTP correctly. Use MCP Inspector or the `ext-apps/examples/basic-host` to validate outside Claude.

**"Iframe renders but shows nothing."** Two root causes: (1) `app.connect()` was never called, (2) event handlers registered *after* `app.connect()` so the initial `tool-result` was missed. **Always set `ontoolresult`, `ontoolinput`, and `ontoolinputpartial` before calling `connect()`.**

**"Iframe has zero height."** The iframe starts empty. If your root element has no content at render time, it collapses. Set a minimum height or show a loading state.

**CSP blocking (silent failures).** If your HTML tries to fetch external resources without declaring them in `_meta.ui.csp`, requests silently fail. On **Claude Desktop**: enable Developer Mode via **Help → Troubleshooting → Enable Developer Mode**, then `Cmd+Option+I` for DevTools. On **Claude.ai web**: you can't access the iframe's console; bundle everything into one file to avoid CSP issues entirely.

**`structuredContent` cross-client bugs (known as of Feb 2026):**

| Client | Bug |
|---|---|
| VS Code | Ignores `content` when `structuredContent` is present; sends only stringified structured content to model |
| OpenAI Codex | Drops image blocks from `content` when `structuredContent` exists |
| LangChain MCP adapters | Ignores `structuredContent` entirely |

**Always provide meaningful `content` text as a fallback.** Test on your target clients.

**npm install fails with version conflicts (ext-apps issue #367).** Use `--legacy-peer-deps` if resolution fails, or pin versions explicitly.

**Handler overwrite (ext-apps issue #225).** `app.onhostcontextchanged` is a property, not an event emitter. Assigning it twice silently overwrites the first handler. Compose logic into a single function.

**Working directory undefined on macOS (Claude Desktop).** Always use absolute paths (`import.meta.dirname` for ES modules) and specify env vars explicitly in `claude_desktop_config.json`.

**Base64 inflation math.** Base64 adds ~33% overhead. A 750KB image becomes ~1MB after encoding. With MCP Apps, this only matters for the chunked tool path (keep chunks under 500KB raw = ~667KB base64, well under 1MB).

---

## How `@mcp-ui/server` relates to `@modelcontextprotocol/ext-apps`

These packages are **complementary, not competing**. MCP-UI (by Ido Salomon and Liad Yosef) pioneered interactive UI over MCP and influenced the MCP Apps spec.

- **`@modelcontextprotocol/ext-apps/server`** — `registerAppTool()` and `registerAppResource()`. Core registration layer. This is all you need.
- **`@mcp-ui/server`** — `createUIResource()`. Convenience helper with validation, base64 encoding support, and cross-platform metadata (also handles ChatGPT's Apps SDK format).

Use `@mcp-ui/server` if you want its validation and cross-platform adapters. Skip it if you prefer fewer dependencies.

---

## Sources

**Official MCP Apps (authoritative):**
- Spec + SDK: https://modelcontextprotocol.io/docs/extensions/apps
- Blog announcement: https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/
- API docs: https://modelcontextprotocol.github.io/ext-apps/api/documents/Overview.html
- Quickstart: https://modelcontextprotocol.github.io/ext-apps/api/documents/Quickstart.html
- Patterns: https://modelcontextprotocol.github.io/ext-apps/api/documents/Patterns.html
- GitHub: https://github.com/modelcontextprotocol/ext-apps

**Claude connector docs:**
- Custom connectors: https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp
- Building connectors: https://support.claude.com/en/articles/11503834-building-custom-connectors-via-remote-mcp-servers
- Interactive connectors: https://support.claude.com/en/articles/13454812-using-interactive-connectors-in-claude
- Connector submission: https://support.claude.com/en/articles/12922490-remote-mcp-server-submission-guide

**npm packages (verified Feb 11, 2026):**
- `@modelcontextprotocol/sdk` v1.26.0: https://www.npmjs.com/package/@modelcontextprotocol/sdk
- `@modelcontextprotocol/ext-apps` v1.0.1: https://www.npmjs.com/package/@modelcontextprotocol/ext-apps

**Reference implementation:**
- AnassKartit/nano-banana-mcp-app: https://github.com/AnassKartit/nano-banana-mcp-app

**MCP-UI (complementary):**
- https://mcpui.dev/
- https://github.com/MCP-UI-Org/mcp-ui
