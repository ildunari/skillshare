---
name: mcp-proxy-builder
description: Build, deploy, and troubleshoot MCP servers and MCP Apps behind mcpproxy-go-hosted Claude connectors. Use when working on /mcp connector endpoints, mcpproxy-go upstream routing, Cloudflare tunnel+ingress, initialize/tools/list/tools/call debugging, interactive inline MCP Apps (io.modelcontextprotocol/ui), and fail-closed auth posture.
---

# MCP Proxy Builder

## Overview

Use this skill to build and operate MCP connectors with `mcpproxy-go` as the canonical gateway for web-hosted clients (especially claude.ai), including:

- regular MCP upstream backends routed through one proxy endpoint
- MCP Apps with inline iframe rendering (`io.modelcontextprotocol/ui`)
- hybrid connectors with robust non-UI fallback behavior

This skill is execution-oriented. Follow the workflow in order and fail closed on safety gates.

Primary control-plane docs for this stack:
- `/Users/kosta/.mcpproxy/AGENTS.md`
- `/Users/kosta/.mcpproxy/docs/native-cutover-runbook.md`
- `/Users/kosta/.mcpproxy/scripts/verify-native-cutover.sh`

## Runtime Context and Invariants

- Canonical gateway runtime: `mcpproxy-go`
- Local listener (current snapshot): `http://127.0.0.1:8080/mcp`
- Proxy config: `/Users/kosta/.mcpproxy/mcp_config.json`
- Tunnel config: `/Users/kosta/.cloudflared/config.yml`
- Public endpoint pattern: `https://<hostname>.pluginpapi.dev/mcp`
- Active hostnames in current snapshot:
  - `https://mcp-github.pluginpapi.dev/mcp`
  - `https://mcp.pluginpapi.dev/mcp`

Hard invariants:

1. Use `/mcp` in connector URLs for this stack.
2. Route public traffic as `Claude/Webchat -> Cloudflare Tunnel -> mcpproxy-go -> upstream MCP backend(s)`.
3. Keep one active `github` upstream in `/Users/kosta/.mcpproxy/mcp_config.json` unless explicitly testing migration.
4. Treat auth-off mode as temporary test posture; restore fail-closed mode before production exposure.
5. Validate local + public + initialize + tools/list + tools/call before declaring success.

## Current-System Quick Check (Run First)

Run these exact checks before changing anything:

1. Process health:
- `pgrep -fl "mcpproxy|cloudflared"`
2. Local/public endpoint health:
- `curl -i http://127.0.0.1:8080/mcp`
- `curl -i https://mcp-github.pluginpapi.dev/mcp`
3. End-to-end protocol check:
- `/Users/kosta/.mcpproxy/scripts/verify-native-cutover.sh`

Expected for current system:
- `GET /mcp` returns `405` (not `404`) on local and public.
- `initialize`, `tools/list`, and safe `tools/call` return `200`.

## Secret-Safe Inspection Rules

Never print full config files that may include auth headers or API keys.

Use redacted-safe inspection commands:

- `jq '{listen, data_dir, mcpServers: [.mcpServers[] | {name, url, protocol, enabled}]}' /Users/kosta/.mcpproxy/mcp_config.json`
- `sed -n '1,120p' /Users/kosta/.cloudflared/config.yml`

If you must inspect headers for debugging, print only header keys:

- `jq '.mcpServers[] | {name, header_keys: ((.headers // {}) | keys)}' /Users/kosta/.mcpproxy/mcp_config.json`

## Intake Checklist (Always Confirm First)

1. Confirm target outcome:
- `regular-mcp` (tooling only)
- `mcp-app` (inline interactive iframe)
- `hybrid` (both)
2. Confirm host target:
- claude.ai web connector (public HTTPS required)
- local testing only
3. Confirm auth mode:
- no-auth / API key / OAuth
4. Confirm transport:
- upstream MCP backend exposed through mcpproxy-go `/mcp`
5. Confirm scope:
- public connector via Cloudflare ingress
- local-only via `127.0.0.1`
6. Confirm source-of-truth files:
- `/Users/kosta/.mcpproxy/mcp_config.json`
- `/Users/kosta/.cloudflared/config.yml`
7. Confirm no drift in canonical route:
- both hostname ingress entries route to `http://127.0.0.1:8080`
8. Confirm single-upstream rule for `github` target.

## Decision Tree: Regular MCP vs MCP App vs Hybrid

Choose `regular-mcp` when:
- text-only tool output is sufficient
- no inline custom UI is needed

Choose `mcp-app` when:
- rich rendering is required in chat inline/fullscreen
- payloads include large media or structured results better consumed by UI

Choose `hybrid` when:
- connector must still provide strong text fallbacks for non-app hosts
- you need App features in Claude web while maintaining broad client compatibility

## Workflow A: Regular MCP Server (Implementation-Complete)

0. Create backups before editing:
- `cp /Users/kosta/.mcpproxy/mcp_config.json /Users/kosta/.mcpproxy/artifacts/mcp_config.json.bak.$(date +%Y%m%d-%H%M%S)`
- `cp /Users/kosta/.cloudflared/config.yml /Users/kosta/.cloudflared/config.yml.bak.$(date +%Y%m%d-%H%M%S)`
1. Implement or identify the upstream MCP backend endpoint (`/mcp` preferred).
2. Update proxy routing in:
- `/Users/kosta/.mcpproxy/mcp_config.json`
3. Ensure minimum protocol handling upstream:
- `initialize`
- `notifications/initialized`
- `tools/list`
- `tools/call` (if tools exposed)
4. Confirm Cloudflare ingress maps hostname to local proxy listener `http://127.0.0.1:8080`.
5. Validate local proxy endpoint:
- `curl -i http://127.0.0.1:8080/mcp`
6. Validate public endpoint:
- `curl -i https://<hostname>.pluginpapi.dev/mcp`
7. Run protocol probes:
- `initialize` POST
- `tools/list`
- safe `tools/call`
8. Add connector in Claude using:
- `https://<hostname>.pluginpapi.dev/mcp`
9. Re-run full validator:
- `/Users/kosta/.mcpproxy/scripts/verify-native-cutover.sh`

Required implementation quality for regular servers:

- reject invalid tool inputs with explicit schema errors
- map upstream failures to deterministic, human-readable error messages
- keep tool schemas stable; version rather than breaking argument contracts
- avoid logging secrets and large payloads
- prefer existing runtime conventions in `/Users/kosta/.mcpproxy`

## Workflow B: MCP App Connector (Implementation-Complete)

1. Build app server with `@modelcontextprotocol/sdk` + `@modelcontextprotocol/ext-apps`
2. Register app resource and app tool:
- app resource uses `ui://...` URI
- tool metadata includes `_meta.ui.resourceUri`
3. Keep app bridge lifecycle strict:
- register `ontoolresult`/`ontoolinput` handlers before `app.connect()`
4. Choose delivery strategy:
- Strategy A: signed URL render path in `structuredContent` (default)
- Strategy B: chunked app-only bytes tool (fallback)
- Strategy C: async `jobId` + app-only polling for multi-result/long-running tools
5. Always include meaningful text in `content` as fallback for non-app clients
6. Negotiate capability:
- detect `io.modelcontextprotocol/ui` support and fallback cleanly
7. Publish through mcpproxy-go and Cloudflare with `/mcp` endpoint
8. Test in claude.ai web connector (interactive connectors supported there)

MCP App implementation minimum:

1. Server-side:
- register `ui://` resource
- return `_meta.ui.resourceUri` on UI tool
- return small, useful `content` summary
- return structured data in `structuredContent`
2. View-side:
- bind handlers before `app.connect()`
- process first `tool-result` event immediately
- maintain loading/error/empty states
- keep UI usable if tool result is partial or delayed
3. Compatibility:
- include non-UI fallback text
- avoid assumptions about `structuredContent` fidelity across clients
4. Layout:
- template DOM is optional; full custom UI is valid if app bridge lifecycle/contract stays correct

Update routing for app backends through mcpproxy-go:
- upstream app backend stays independent
- mcpproxy-go remains the public connector entrypoint

## Host Rendering Contract (Claude + ChatGPT)

Build app tools so they degrade gracefully across hosts:

1. Always return all three channels in tool results when possible:
- `content` (human-readable fallback summary)
- `structuredContent` (machine/app payload)
- `_meta.ui.resourceUri` (UI render target for app-capable hosts)
2. Never rely on UI-only output for critical user meaning.
3. Keep fallback `content` actionable even when iframe/app rendering is unavailable.
4. Keep payload contracts stable:
- additive schema evolution only
- avoid renaming/removing required fields without versioning
5. Treat host UI capability as negotiated, not guaranteed:
- if host lacks `io.modelcontextprotocol/ui`, return strong text fallback and continue.

### Claude.ai Verification

For Claude connector deployments, verify:

1. Connector URL uses public Cloudflare `/mcp` endpoint.
2. `tools/list` shows app tool and `_meta.ui.resourceUri`.
3. Tool call renders app UI in chat when UI capability is available.
4. Tool call still returns useful text fallback when UI is unavailable/interrupted.

### ChatGPT Verification

For ChatGPT-facing integrations, verify:

1. Host/client path can consume MCP app metadata for rendering.
2. Same tool call returns useful fallback `content` if rich UI is not rendered.
3. No critical data is trapped in host-specific UI-only fields.
4. Core user journey succeeds with text-only fallback path.

## Required MCP App Data Delivery Patterns

Pattern A: signed URL render (default)
- Return `signedUrl` + metadata in `structuredContent`.
- Keep model-facing `content` short and useful.

Pattern B: chunked app-only tool retrieval (fallback)
- Primary tool returns object ID + metadata.
- View calls hidden app-only bytes tool in fixed chunks.
- View assembles bytes and renders Blob/object URL.

Pattern C: async job/polling for multi-result workloads
- Primary tool returns quickly with `jobId` and summary metadata.
- View polls hidden app-only status tool (for example `get_*_job`).
- Terminal states must be explicit (`ready`, `error`, `cancelled`, `expired`).

Pattern selection rule:
- default to Pattern A for remote media rendering
- use Pattern B only when signed URL path is blocked/failing by host/CSP constraints
- use Pattern C when results arrive progressively or generation time is long

## Mandatory Safety Gates (Non-Negotiable)

1. Use `/mcp`, not `/sse`, for this Streamable HTTP deployment.
2. Never hardcode secrets in scripts or docs; use env files excluded from git.
3. Keep Cloudflare ingress pointed at active proxy listener (`127.0.0.1:8080` unless intentionally changed).
4. Keep one active upstream per logical connector target unless running a migration test.
5. Avoid startup interactivity and blocking auth prompts in backend startup.
6. Keep control-plane topology fixed:
- public clients never connect directly to upstream MCP backend URLs
- all public traffic enters through Cloudflare hostnames and `mcpproxy-go`

## App Lifecycle Sequencing Rules (Do Not Violate)

1. Define `ontoolresult` and other handlers first.
2. Call `app.connect()` second.
3. Read host context (theme/display) after connect.
4. Render initial UI state before waiting on async fetches.
5. Handle subsequent tool calls without replacing core listeners.

Breaking this order causes blank app states and missed initial result events.

## Do This / Not That

| Do this | Not that |
|---|---|
| Use `https://<host>/mcp` in Claude connector config | Use `/sse` for this stack |
| Route Cloudflare ingress directly to `http://127.0.0.1:8080` | Route public traffic through retired supergateway/contextforge runtimes |
| Keep secrets in env files excluded from git | Hardcode keys in repo or pass as command args |
| Return strong `content` fallback text in tool results | Assume all clients consume `structuredContent` correctly |
| Register app event handlers before `app.connect()` | Register handlers after connect and miss initial tool result |
| Validate DNS + ingress together | Debug auth first when hostname routing is broken |
| Verify local/public/initialize/tools flow after each routing change | Declare success after only one ping |
| Use signed URL render as primary media path | Push large base64 payloads into model-facing content |
| Use chunked app-only bytes retrieval only as fallback | Assume chunking is always required |
| Use async `jobId` + app-only polling for multi-result tools | Block tool call until all results are finished |
| Keep app HTML bundled and self-contained | Depend on undeclared external assets that CSP blocks |

## Verification Gates Before Declaring Success

Pass all:

1. `curl -i http://127.0.0.1:8080/mcp` returns expected non-POST behavior (typically `405`).
2. `curl -i https://<hostname>.pluginpapi.dev/mcp` returns expected non-POST behavior (typically `405`).
3. `initialize` POST returns `200` with valid MCP initialize payload.
4. `tools/list` returns `200` with expected schema.
5. Safe `tools/call` returns `200`.
6. `dig +short <hostname>.pluginpapi.dev` resolves to expected Cloudflare target.
7. For MCP Apps: claude.ai renders iframe, receives tool-result data, and fallback text remains useful.
8. For MCP Apps with media: signed URL renders successfully; if fallback enabled, chunk retrieval completes with no monotonic memory/process growth.
9. `GET /mcp` never returns `404` on active local/public routes.
10. `tools/list` exposes `_meta.ui.resourceUri`; debug uses active URI for `resources/read`.
11. `/Users/kosta/.mcpproxy/scripts/verify-native-cutover.sh` passes.
12. Runtime logs show no immediate route/proxy failures:
- `/Users/kosta/.mcpproxy/runtime/logs/mcpproxy-serve.log`
- `/Users/kosta/.mcpproxy/runtime/logs/cloudflared.log`
13. Host compatibility checks pass:
- Claude: inline app render works and fallback text remains useful.
- ChatGPT path: rendering metadata is present, and text fallback still completes task.

## Rollback Procedure (Required Before Risky Changes)

If checks fail after a route/config change:

1. Restore last known-good config backup:
- `cp /Users/kosta/.mcpproxy/artifacts/mcp_config.json.bak.<timestamp> /Users/kosta/.mcpproxy/mcp_config.json`
- `cp /Users/kosta/.cloudflared/config.yml.bak.<timestamp> /Users/kosta/.cloudflared/config.yml`
2. Restart affected runtime/processes by current host standard.
3. Re-run:
- `/Users/kosta/.mcpproxy/scripts/verify-native-cutover.sh`
4. Stop only when local/public initialize + tools flow are healthy again.

## Stop Conditions

Stop and fix before proceeding if:

- endpoint configured as `/sse` in this stack
- DNS exists but ingress rule points wrong local port
- local listener is not `mcpproxy-go` as intended
- mcp_config contains duplicate/conflicting upstreams for same target
- App tool lacks `_meta.ui.resourceUri`
- UI handlers are attached after `app.connect()`
- connector works locally but public `/mcp` host does not resolve cleanly
- app view depends on blocked external resources under host CSP
- auth is disabled and deployment is being treated as production

## Required Reference Files for This Workflow

- `/Users/kosta/.mcpproxy/AGENTS.md`
- `/Users/kosta/.mcpproxy/docs/native-cutover-runbook.md`
- `/Users/kosta/.mcpproxy/scripts/verify-native-cutover.sh`

## Quick Trigger Examples

- "Create a new public MCP connector on mcpproxy-go for claude.ai and validate end-to-end."
- "Build an MCP App connector with inline image rendering and chunked binary delivery."
- "Diagnose why this connector fails with URL/auth error and confirm DNS/ingress/tunnel/proxy safety."
