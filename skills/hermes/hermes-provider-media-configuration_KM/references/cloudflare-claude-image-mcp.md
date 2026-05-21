# Archived skill: cloudflare-claude-image-mcp

Original path: `/Users/Kosta/.hermes/profiles/gpt/skills/automation/cloudflare-claude-image-mcp`
Absorbed into umbrella: `hermes-provider-media-configuration` on 2026-04-29.

---

---
name: cloudflare-claude-image-mcp
description: Build and deploy a fully-online Cloudflare remote MCP server for Claude.ai that exposes image generation with OpenAI GPT Image 2. Use when the user asks for Claude.ai custom connectors, Cloudflare MCP/Workers, Image 2/GPT Image 2 image generation, or wants to make local Codex/Hermes image generation available online. Includes the important course-correction that Codex/ChatGPT OAuth should not be reused as a Cloudflare server credential; use an OpenAI API key in Worker secrets instead.
---

# Cloudflare Claude.ai GPT Image 2 MCP

Use this when creating a remote MCP connector for Claude.ai that generates images through GPT Image 2 and runs fully online on Cloudflare Workers.

## Core judgement

Do **not** copy or reuse Codex/ChatGPT OAuth credentials in Cloudflare.

Codex OAuth / `~/.codex/auth.json` is local, password-equivalent, undocumented for arbitrary server-side Images API calls, and brittle. Treat it as unsuitable for a public or semi-public remote MCP service. The supportable online architecture is:

```text
Claude.ai custom connector
  -> Cloudflare Worker remote MCP endpoint
  -> OpenAI Images API using OPENAI_API_KEY Worker secret
  -> Cloudflare-hosted image URL returned to Claude (R2 preferred; Workers KV is a workable fallback if R2 is not enabled)
```

If the user specifically wants to spend Codex subscription/image quota, keep that path local through Hermes/Codex tooling. For a fully-online Claude.ai connector, use OpenAI API billing.

## Research checks before coding

Verify current docs before implementation because all three surfaces move:

- Claude.ai remote MCP/custom connector docs: confirm Streamable HTTP support and current connector-add flow.
- Cloudflare Agents/Workers MCP docs: confirm `createMcpHandler` signature and the current stateless per-request `McpServer` pattern.
- OpenAI image-generation docs: confirm `gpt-image-2` endpoint, params, and whether org verification/API key is required.

Freshness receipts that mattered in the original build:

- Cloudflare Agents remote MCP docs: remote MCP supports Streamable HTTP; `createMcpHandler()` is the lightweight stateless option.
- Cloudflare `createMcpHandler` docs: with newer MCP SDKs, create a fresh `McpServer` per request to avoid cross-client leakage.
- Claude.ai remote MCP docs: Free/Pro/Max users can add custom connectors from Settings → Connectors → Add custom connector.
- OpenAI image docs: Image API supports `gpt-image-2` through `/v1/images/generations` using `Authorization: Bearer $OPENAI_API_KEY`.

## Recommended implementation

Create a small TypeScript Cloudflare Worker project:

```bash
mkdir -p ~/LocalDev/cloudflare-image2-mcp/src
cd ~/LocalDev/cloudflare-image2-mcp
git init
npm init -y
npm pkg set type=module \
  scripts.dev='wrangler dev' \
  scripts.deploy='wrangler deploy' \
  scripts.typecheck='tsc --noEmit' \
  scripts.test='npm run typecheck'
npm install @cloudflare/workers-types @modelcontextprotocol/sdk agents zod typescript wrangler vitest --save-dev
```

Use a Worker shaped like:

- `/mcp/<CONNECTOR_SECRET>`: MCP endpoint.
- `/image/<id>`: serves generated images from Cloudflare storage.
- Tool: `generate_image(prompt, size?, quality?, format?)`.
- OpenAI call: `POST https://api.openai.com/v1/images/generations` with `model: "gpt-image-2"`.
- Return a URL, not base64, because Claude tool-result payloads can get too large.
- Prefer storing decoded image bytes in R2. If R2 is not enabled on the Cloudflare account, use Workers KV as a fallback by storing the OpenAI `b64_json` string plus metadata, then decoding it in `/image/<id>`.

Bind an R2 bucket in `wrangler.toml` when R2 is available:

```toml
name = "image2-mcp"
main = "src/index.ts"
compatibility_date = "2026-04-25"
compatibility_flags = ["nodejs_compat"]

[[r2_buckets]]
binding = "IMAGES"
bucket_name = "image2-mcp-images"
```

If R2 creation/deploy fails with Cloudflare API code `10042` (`Please enable R2 through the Cloudflare Dashboard`), switch to Workers KV instead:

```bash
npx wrangler kv namespace create IMAGES --preview false
```

Then bind it in `wrangler.toml`:

```toml
[[kv_namespaces]]
binding = "IMAGES"
id = "<namespace id from wrangler>"
```

For KV storage, do not store a `Uint8Array` directly. Store the OpenAI `b64_json` string and metadata:

```ts
await env.IMAGES.put(id, base64, {
  metadata: { contentType, model: "gpt-image-2", size, quality, format, createdAt: new Date().toISOString() },
});
```

Then serve it by decoding and copying into a plain `ArrayBuffer` for TypeScript/Workers compatibility:

```ts
const object = await env.IMAGES.getWithMetadata<{ contentType?: string }>(id);
if (!object.value) return notFound();
const bytes = decodeBase64(object.value);
const body = new ArrayBuffer(bytes.byteLength);
new Uint8Array(body).set(bytes);
return new Response(body, { headers });
```

Use secrets, not committed env files:

```bash
npx wrangler secret put OPENAI_API_KEY
npx wrangler secret put CONNECTOR_SECRET
```

Generate the connector secret locally:

```bash
python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(32))
PY
```

## OpenAI key gotcha

On this Mac Studio, the `OpenAI API Key` 1Password item may be stale/invalid for this use. The known working key during the original build was `op://CLI/OpenAI Photon API/password`. If image generation returns `Incorrect API key provided`, retry with that item before debugging Worker code.

## Local verification pattern

Keep `.dev.vars` ignored and put dummy values back after tests. Do not leave real API keys in local files.

Start local dev with a temporary real key only long enough to test:

```bash
printf 'CONNECTOR_SECRET=test-secret\nOPENAI_API_KEY=%s\n' "$(op read 'op://CLI/OpenAI Photon API/password')" > .dev.vars
npx wrangler dev --local --port 8790
```

In another terminal, verify the root and MCP tool listing. A minimal MCP SDK client can connect to:

```text
http://localhost:8790/mcp/test-secret
```

Then run one cheap real image generation, e.g. low quality, simple prompt, and verify the returned image URL serves a valid PNG:

```bash
python3 - <<'PY'
import urllib.request
url='http://localhost:8790/image/<id>.png'
resp=urllib.request.urlopen(url, timeout=10)
data=resp.read(16)
print(resp.status, resp.headers.get('content-type'), data[:8].hex())
PY
```

Expected PNG signature: `89504e470d0a1a0a`.

After testing:

```bash
printf 'CONNECTOR_SECRET=test-secret\nOPENAI_API_KEY=dummy\n' > .dev.vars
```

## Deployment flow

1. Authenticate Wrangler on the machine with a real browser session:

   ```bash
   cd ~/LocalDev/cloudflare-image2-mcp
   npx wrangler login
   ```

   If Google passkey verification appears, the user must complete it in the real desktop browser. Browser automation may not be able to complete the passkey challenge. If the user pastes the `localhost:8976/oauth/callback?...` URL back into chat while the same `wrangler login` process is still running, first check `npx wrangler whoami`; the callback may already have completed successfully even if manually replaying the URL returns 403.

2. Create storage:

   ```bash
   npx wrangler r2 bucket create image2-mcp-images
   ```

3. Set secrets:

   ```bash
   npx wrangler secret put OPENAI_API_KEY
   npx wrangler secret put CONNECTOR_SECRET
   ```

4. Deploy:

   ```bash
   npx wrangler deploy
   ```

5. Verify remote root and MCP with an MCP SDK client or MCP Inspector.

6. Add to Claude.ai:

   Settings → Connectors → Add custom connector → URL:

   ```text
   https://<worker-host>/mcp/<CONNECTOR_SECRET>
   ```

## Browser/Claude.ai setup notes

Use agent-browser or browser tools for Claude.ai connector setup only after the Worker is deployed and verified. Claude.ai custom connectors are user-visible/external configuration, so be careful not to expose the secret path in chat logs beyond what is necessary.

If Claude.ai is logged in but `generate_image` is missing, first check the connector URL in Settings → Connectors. In the original `structured-input` setup, the existing **Structured Output** connector pointed at the safe public `/mcp` endpoint, so Claude correctly saw only `collect_structured_input`. Do not debug the Worker implementation until you confirm whether Claude is using the protected `/mcp/<CONNECTOR_SECRET>` route.

For a safe Claude.ai test flow:

1. Verify protected `tools/list` remotely before touching Claude:
   ```bash
   URL='https://<worker-host>/mcp/<CONNECTOR_SECRET>'
   curl -sS -H 'content-type: application/json' \
     -H 'accept: application/json, text/event-stream' \
     --data '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
     "$URL"
   ```
   The response should include both `collect_structured_input` and `generate_image`.
2. In Claude.ai, add a separate custom connector for the protected route, e.g. **Structured Image**, instead of replacing the safe public connector unless the user explicitly wants that.
3. Set `generate_image` permission to Always allow for frictionless testing. Leave other tools at Needs approval if appropriate.
4. Start a fresh chat and explicitly ask Claude to use the named protected connector: “Use the Structured Image connector's `generate_image` tool…”.
5. Verify Claude shows a `Structured Image generate_image` tool call, the request/response panel includes the image URL and the “interactive widget rendered” message, and an iframe appears in the chat above the final text.

Claude.ai/browser automation quirks from the original test:

- The normal browser click/type helpers can time out or report “blocked by overlay” even when the element is usable. If that happens, use CDP `Runtime.evaluate` to focus/click buttons or insert text into `[data-testid="chat-input"]`.
- Narrow viewports can hide connector controls offscreen; set a wider viewport before managing connectors.
- The MCP app iframe may appear as an OOPIF whose direct DOM is just Claude’s proxy shell (`MCP-UI Proxy`) and not expose useful body text/images to automation. Treat the Claude tool-call transcript plus visible iframe dimensions as the reliable non-screenshot verification path.
- Raw one-shot `tools/call` requests can return `403 Forbidden` because the Cloudflare/Agents MCP transport expects a proper initialized session, even when `tools/list` works and Claude can call the tool. Do not mistake that isolated 403 for a broken connector.
- If you put the protected URL on the clipboard or in a temp file for browser setup, clear both when done.

If a site hits passkey/human verification, stop and ask Kosta to complete that specific prompt on the Studio. Do not repeatedly retry automation against Cloudflare/Google passkey flows.

## Security and spend-control defaults

- Do not deploy a public unauthenticated image-generation MCP endpoint. It can burn money.
- Prefer an unguessable secret path at minimum for personal use.
- For a shared/team connector, replace the secret path with proper OAuth/Cloudflare Access.
- Store OpenAI API keys only as Worker secrets.
- Store generated images in R2 and return URLs, not base64 payloads.
- Consider signed/expiring URLs if generated images may be sensitive.
- Add an app-side monthly budget cap for any cost-incurring image tool, even if the user also sets an OpenAI billing cap. The Worker can only cap usage through this connector; it cannot see other usage of the same OpenAI API key.
- Confirm before enabling or wiring any write/action tools beyond image generation.

For a simple personal cap, add a Worker variable such as `IMAGE_MONTHLY_BUDGET_USD = "10"`, estimate each request from the current OpenAI GPT Image 2 pricing table, and track usage in KV/R2 under a monthly key like `usage:YYYY-MM`. Check the budget before calling OpenAI and record spend only after a successful image response. Return the estimated cost and monthly cap in the tool response so Claude can surface it.

Example cost table from the original build, checked against OpenAI image-generation docs on 2026-04-25:

```ts
const COST_MICRODOLLARS = {
  low: { "1024x1024": 6_000, "1024x1536": 5_000, "1536x1024": 5_000 },
  medium: { "1024x1024": 53_000, "1024x1536": 41_000, "1536x1024": 41_000 },
  high: { "1024x1024": 211_000, "1024x1536": 165_000, "1536x1024": 165_000 },
};
```

Default-medium at 1024×1024 is about `$0.053` per image, so a `$10` cap allows roughly 188 successful default generations. This is a guardrail, not a billing guarantee: text/input-image costs, pricing changes, race conditions between concurrent requests, and external API-key usage can make final account billing differ slightly.

## Integrating Image 2 into an existing MCP app Worker

If the user asks to add Image 2 into an already-hosted MCP app, first inspect the existing Worker/server split instead of creating another repo. The reusable pattern from `~/LocalDev/mcp-apps/structured-input` was:

- Keep the original public MCP route unchanged for safe/basic tools.
- Add a protected secret route, e.g. `/mcp/<CONNECTOR_SECRET>`, that includes the cost-incurring `generate_image` tool.
- Keep generated images served from the same Worker origin at `/image/<id>` so Claude gets a normal URL.
- Reuse the same Worker secrets: `OPENAI_API_KEY` and `CONNECTOR_SECRET`.
- Reuse the same KV/R2 storage binding if appropriate, but verify the binding in that project’s `wrangler.jsonc`/`wrangler.toml`.

For TypeScript MCP apps that have a pure `createServer()` function, make image generation optional so local stdio/basic mode does not require Cloudflare env secrets.

If the app should render the generated image inline, register `generate_image` as an MCP App tool with the same UI resource, not as a plain `server.tool`. Return normal model-facing text plus `structuredContent` that the iframe can understand:

```ts
export type CreateServerOptions = {
  generateImage?: (args: GenerateImageArgs) => Promise<GenerateImageResult>;
};

export function createServer(appHtml: string, options: CreateServerOptions = {}): McpServer {
  // register normal app resources/tools first
  if (options.generateImage) {
    registerAppTool(
      server,
      "generate_image",
      {
        title: "Generate image",
        description: "Generate an image with GPT Image 2 and render it inline in the MCP App.",
        inputSchema: {
          prompt: z.string().min(1).max(8000),
          size: z.enum(["1024x1024", "1024x1536", "1536x1024", "auto"]).optional(),
          quality: z.enum(["low", "medium", "high", "auto"]).optional(),
          format: z.enum(["png", "jpeg", "webp"]).optional(),
        },
        _meta: { ui: { resourceUri: APP_RESOURCE_URI } },
      },
      async (args) => {
        const result = await options.generateImage!(args);
        return {
          content: [{ type: "text", text: `Generated image with GPT Image 2.\n\nURL: ${result.url}` }],
          structuredContent: {
            kind: "image-result",
            title: "GPT Image 2 result",
            ...result,
          },
        };
      }
    );
  }
  return server;
}
```

In the iframe app, branch on `structuredContent.kind === "image-result"` inside `app.ontoolresult`, clear the form body, and render an `<img src=result.url>` plus prompt/metadata/actions. Keep the existing `schema.fields` branch for normal structured-input forms. This is the key difference between “Claude gets an image URL” and “the MCP app renders the generated image inline.”

Then in the Worker:

```ts
if (url.pathname.startsWith("/mcp/")) {
  if (!secretPath(url.pathname, env.CONNECTOR_SECRET)) {
    return json({ error: "unauthorized" }, 401);
  }

  const server = createServer(APP_HTML, {
    generateImage: (args) => generateImage(args, env, request),
  });
  return createMcpHandler(server, { route: url.pathname })(request, env, ctx);
}

const server = createServer(APP_HTML); // public/basic route
return createMcpHandler(server)(request, env, ctx);
```

In the original `structured-input` integration, the deployed behavior was intentionally:

- `https://structured-input.kosta963.workers.dev/mcp` lists only `collect_structured_input`.
- `https://structured-input.kosta963.workers.dev/mcp/<CONNECTOR_SECRET>` lists `collect_structured_input` and `generate_image`.

This split avoids accidentally exposing a public image-spend endpoint while preserving the existing app’s basic public behavior.

## Completion checks

Before calling it done, run:

```bash
npm run typecheck
# or, for repos that define build instead of typecheck:
npm run build
npx wrangler deploy --dry-run
```

After deploy, verify:

- Worker root responds.
- Public/basic MCP route still lists only the intended safe tools.
- Protected `/mcp/<secret>` lists `generate_image` in MCP Inspector or SDK client.
- A low-cost real generation returns a Cloudflare image URL.
- The image URL returns `200` with expected image content type, e.g. PNG signature `89504e470d0a1a0a`.
- Claude.ai connector can be added using the protected URL and the tool appears in a conversation.
