# MCP Apps patterns reference

Catalog of official patterns from the `@modelcontextprotocol/ext-apps` documentation. Each pattern includes server-side and client-side code where applicable.

Source: https://modelcontextprotocol.github.io/ext-apps/api/documents/Patterns.html

## Table of contents

- App-only tools (hidden from model)
- Chunked binary loading
- Capability negotiation and fallback
- Host theme adaptation
- Streaming partial tool input
- Fullscreen toggle
- Model context updates from View
- Large follow-up messages
- View state persistence
- Pausing heavy views when offscreen
- CSP and CORS configuration

---

## App-only tools (hidden from model)

Tools that only the iframe View can call. The model never sees them in `tools/list`, so they don't consume context window and can't be invoked by the model. Use for: regenerate buttons, pagination, chunk loading, View-specific actions.

### Server

```typescript
import { registerAppTool } from "@modelcontextprotocol/ext-apps/server";

registerAppTool(
  server,
  "regenerate_image",
  {
    title: "Regenerate",
    description: "Regenerate the image. App-only — not visible to the model.",
    inputSchema: {
      prompt: z.string(),
      style: z.enum(["photo", "illustration", "abstract"]).optional(),
    },
    _meta: {
      ui: {
        resourceUri: APP_RESOURCE_URI,
        visibility: ["app"],  // This is the key — hides from model
      },
    },
  },
  async ({ prompt, style }) => {
    const result = await generateImage(prompt, style);
    return {
      content: [{ type: "text", text: "Regenerated." }],
      structuredContent: { imageId: result.id, mimeType: result.mimeType },
    };
  }
);
```

### Client (calling from iframe)

```typescript
const result = await app.callServerTool({
  name: "regenerate_image",
  arguments: { prompt: currentPrompt, style: "illustration" },
});

const sc = result.structuredContent as { imageId: string; mimeType: string };
```

---

## Chunked binary loading

The officially documented pattern for delivering large binary data (images, PDFs, audio) to the View without hitting size limits. The primary tool returns an ID; the View fetches bytes in 500KB chunks via an app-only tool through the App Bridge.

### Server — primary tool

```typescript
registerAppTool(
  server,
  "generate_image",
  {
    title: "Generate image",
    description: "Generate an image from a text prompt.",
    inputSchema: {
      prompt: z.string().describe("Image generation prompt"),
    },
    _meta: { ui: { resourceUri: APP_RESOURCE_URI } },
  },
  async ({ prompt }) => {
    const { mimeType, bytes } = await generateImage(prompt);

    // Store bytes server-side with TTL
    const imageId = randomId("img");
    imageStore.set(imageId, { mimeType, bytes, createdAt: Date.now() });

    return {
      content: [
        { type: "text", text: `Generated image (${mimeType}, ${bytes.length} bytes)` },
      ],
      structuredContent: {
        imageId,
        mimeType,
        byteLength: bytes.length,
        prompt,
      },
    };
  }
);
```

### Server — chunk reader (app-only)

```typescript
const MAX_CHUNK_BYTES = 500 * 1024; // 500KB per chunk

registerAppTool(
  server,
  "read_image_bytes",
  {
    title: "Read image bytes",
    description: "Load image data in chunks. App-only.",
    inputSchema: {
      imageId: z.string(),
      offset: z.number().min(0).default(0),
      byteCount: z.number().default(MAX_CHUNK_BYTES),
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
```

### Client — chunk assembler

```typescript
function base64ToBytes(b64: string): Uint8Array {
  const bin = atob(b64);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}

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
  imageId: string,
  onProgress?: (pct: number) => void
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
    onProgress?.(total > 0 ? (offset / total) * 100 : 0);
  }

  // Assemble into a single typed array
  const full = new Uint8Array(total);
  let pos = 0;
  for (const chunk of chunks) {
    full.set(chunk, pos);
    pos += chunk.length;
  }

  return { mimeType, blob: new Blob([full], { type: mimeType }) };
}

// Usage in ontoolresult handler:
app.ontoolresult = async (result) => {
  const sc = result.structuredContent as { imageId: string };
  if (!sc?.imageId) return;

  const { blob } = await loadImageChunked(app, sc.imageId, (pct) => {
    progressBar.style.width = `${pct}%`;
  });

  const url = URL.createObjectURL(blob);
  imageEl.src = url;
  imageEl.style.display = "block";
};
```

**Why this pattern exists:** The App Bridge (postMessage) carries the chunks inside JSON-RPC messages, staying entirely within the MCP protocol. No CSP exceptions needed, no CORS headers on image endpoints, no separate HTTP image server. Everything stays auditable and sandboxed.

---

## Capability negotiation and fallback

Check whether the connected client supports MCP Apps before registering UI tools. Non-App hosts (Claude Code, Cursor, generic MCP clients) won't render iframes — give them useful text output instead.

```typescript
import {
  getUiCapability,
  RESOURCE_MIME_TYPE,
  registerAppTool,
  registerAppResource,
} from "@modelcontextprotocol/ext-apps/server";

export function createServer(clientCapabilities?: Record<string, unknown>): McpServer {
  const server = new McpServer({ name: "My Server", version: "1.0.0" });

  const uiCap = getUiCapability(clientCapabilities);
  const hasApps = !!uiCap?.mimeTypes?.includes(RESOURCE_MIME_TYPE);

  if (hasApps) {
    // Register UI-enabled tools with resourceUri + iframe HTML
    registerAppResource(server, /* ... */);
    registerAppTool(server, "generate_image", {
      _meta: { ui: { resourceUri: "ui://my-app/view.html" } },
      /* ... */
    }, handler);
  } else {
    // Register text-only fallback
    server.tool("generate_image", { /* ... */ }, async ({ prompt }) => {
      const url = await generateImageAndGetUrl(prompt);
      return {
        content: [
          { type: "text", text: `Generated image: ${url}` },
          { type: "image", data: smallThumbnailBase64, mimeType: "image/webp" },
        ],
      };
    });
  }

  return server;
}
```

**Simpler approach:** Even without capability negotiation, your App tool's `content` text serves as a natural fallback. Non-App hosts display the text and ignore `_meta.ui`. Only add explicit branching if you need meaningfully different behavior (e.g., returning a thumbnail in the non-App path).

---

## Host theme adaptation

Claude provides theme info and CSS variables. Match them to feel native.

### CSS (in your bundled HTML)

```css
:root {
  font-family: var(--font-sans, system-ui, -apple-system, Segoe UI, Roboto, sans-serif);
  background: var(--color-background-primary, #fff);
  color: var(--color-text-primary, #111);
}

[data-theme="dark"] {
  color-scheme: dark;
}

/* Use host spacing and rounding */
.card {
  padding: var(--spacing-md, 12px);
  border-radius: var(--border-radius-lg, 12px);
  border: 1px solid var(--color-border-primary, rgba(0,0,0,0.1));
}

button {
  background: var(--color-background-secondary, #f5f5f5);
  color: var(--color-text-primary, #111);
  border: 1px solid var(--color-border-primary, rgba(0,0,0,0.1));
  border-radius: var(--border-radius-md, 8px);
}
```

### JavaScript

```typescript
// Set BEFORE connect
app.onhostcontextchanged = (ctx) => {
  if (ctx.theme) {
    document.documentElement.setAttribute("data-theme", ctx.theme);
  }
  if (ctx.safeAreaInsets) {
    // Adjust for notches/toolbars on mobile
    document.body.style.paddingTop = `${ctx.safeAreaInsets.top}px`;
  }
};

await app.connect();

// Apply initial theme
const ctx = app.getHostContext();
if (ctx?.theme) {
  document.documentElement.setAttribute("data-theme", ctx.theme);
}
```

---

## Streaming partial tool input

Preview what the model is typing before the tool call completes. Useful for showing the prompt as it's being generated.

```typescript
app.ontoolinputpartial = (params) => {
  const partial = params.arguments?.prompt as string;
  if (partial) {
    previewEl.textContent = `Generating: ${partial}...`;
    previewEl.style.display = "block";
  }
};

// Full input arrives when the tool is actually called
app.ontoolinput = (params) => {
  const prompt = params.arguments?.prompt as string;
  previewEl.textContent = prompt;
};
```

---

## Fullscreen toggle

Let the View switch between inline (in chat flow) and fullscreen (takes over window).

```typescript
const fullscreenBtn = document.getElementById("fullscreen-btn")!;

fullscreenBtn.addEventListener("click", async () => {
  const ctx = app.getHostContext();
  const current = ctx?.displayMode ?? "inline";
  const next = current === "inline" ? "fullscreen" : "inline";

  const available = ctx?.availableDisplayModes ?? [];
  if (available.includes(next)) {
    await app.requestDisplayMode({ mode: next });
  }
});

// React to mode changes
app.onhostcontextchanged = (ctx) => {
  if (ctx.displayMode === "fullscreen") {
    document.body.classList.add("fullscreen");
    fullscreenBtn.textContent = "Exit Fullscreen";
  } else {
    document.body.classList.remove("fullscreen");
    fullscreenBtn.textContent = "Fullscreen";
  }
};
```

---

## Model context updates from View

The View can send text that appears in the model's context as if it were a tool result. Use for: user selections, form submissions, interactive results that the model should know about.

```typescript
// User picks a color in the iframe
colorPicker.addEventListener("change", async () => {
  const color = colorPicker.value;
  await app.updateModelContext({
    content: [
      { type: "text", text: `User selected color: ${color}` },
    ],
  });
});

// User submits a form in the iframe
submitBtn.addEventListener("click", async () => {
  const formData = gatherFormData();
  await app.updateModelContext({
    content: [
      { type: "text", text: `User submitted: ${JSON.stringify(formData)}` },
    ],
  });
});
```

---

## Large follow-up messages

If the View generates a large result that should appear as a user or assistant message (not model context), use `app.sendMessage()`:

```typescript
await app.sendMessage({
  content: "Here is the analysis result: ...",
});
```

This adds a message to the conversation, visible to the user. Use sparingly — it's interruptive.

---

## View state persistence

MCP App iframes are ephemeral — they're destroyed when scrolled out of view and recreated when scrolled back. Use `_meta.viewUUID` to persist state:

```typescript
const viewId = app.getHostContext()?.viewUUID;
if (viewId) {
  // Save state
  const state = { selectedTab: "preview", zoom: 1.5 };
  localStorage.setItem(`mcp-app-${viewId}`, JSON.stringify(state));

  // Restore on re-render
  const saved = localStorage.getItem(`mcp-app-${viewId}`);
  if (saved) {
    const restored = JSON.parse(saved);
    applyState(restored);
  }
}
```

**Note:** `localStorage` works inside the MCP App iframe sandbox (it's scoped to the computed origin, not the parent). This is different from Claude's artifact iframe, where `localStorage` is blocked. Don't confuse the two contexts.

---

## Pausing heavy views when offscreen

If your View runs animations, timers, or heavy computation, pause when offscreen:

```typescript
document.addEventListener("visibilitychange", () => {
  if (document.hidden) {
    pauseAnimation();
    clearInterval(pollingInterval);
  } else {
    resumeAnimation();
    pollingInterval = setInterval(pollData, 5000);
  }
});
```

---

## CSP and CORS configuration

### When you need CSP exceptions

You need CSP exceptions only if your iframe HTML makes direct HTTP requests to external services. This is rare — prefer the App Bridge (`app.callServerTool()`) for all server communication.

If you must make direct requests (e.g., loading a CDN library, calling a third-party API):

```typescript
// In registerAppResource handler, set _meta.ui.csp on the content:
contents: [{
  uri: resourceUri,
  mimeType: RESOURCE_MIME_TYPE,
  text: html,
  _meta: {
    ui: {
      csp: {
        connectDomains: ["https://api.mapbox.com"],     // fetch, XHR, WebSocket
        resourceDomains: ["https://cdn.jsdelivr.net"],   // script src, img src, font src
      },
    },
  },
}]
```

### CORS for direct iframe requests

If your iframe fetches from your own API server (not through the App Bridge), you need CORS headers on that API:

```typescript
// On your API server (separate from MCP server)
import { computeAppDomainForClaude } from "./utils.js";

const allowedOrigin = computeAppDomainForClaude("https://your-mcp-server.com/mcp");

app.use(cors({
  origin: `https://${allowedOrigin}`,
  methods: ["GET", "POST"],
}));
```

**Strong recommendation:** Avoid this complexity. Use the App Bridge for all server communication. The chunked loading pattern proves you can deliver even large binary data entirely through the App Bridge without any CSP or CORS configuration.

---

## Image store with TTL

Server-side pattern for temporarily storing generated images. Used by the chunked loading pattern.

```typescript
type StoredImage = { mimeType: string; bytes: Buffer; createdAt: number };
const imageStore = new Map<string, StoredImage>();

const IMAGE_TTL_MS = 15 * 60 * 1000; // 15 minutes

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
```

**15-minute TTL rationale:** Long enough for iframe rendering and brief scrollback. Short enough to avoid memory accumulation. Iframes aren't persisted across Claude sessions, so 24h retention is wasteful. For production with many users, swap the `Map` for Redis or S3 with lifecycle rules.
