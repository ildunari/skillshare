---
name: plik
description: How to send Kosta files via the Plik MCP — when, how, where credentials live, and how to verify the backend is healthy. Read this once per session before the first upload.
targets: [hermes-default, hermes-gpt, claude-hermes]
machines: [mac-studio]
---

# Plik file sharing

Plik (root-gg/plik 1.4.2) is the self-hosted "send Kosta a file via short link" backend. It runs in Docker on the Mac Studio, exposed via Tailscale Funnel. The official Plik CLI ships an MCP server (`plik --mcp`) that is wired into every Hermes profile and the Claude Hermes hybrid.

## When to use it

Use **native Telegram attach** (the platform reply tool with `files=[…]`) for:
- Images under 10MB (PNG/JPG/WebP — render as inline photos).
- Audio under 10MB (OGG — sends as voice bubble).
- Short videos under 10MB (MP4 — plays inline).
- Small PDFs and Office files Kosta opens in the moment.

Use **`plik upload_file` / `upload_files` / `upload_text`** for:
- Any file > 10MB (Telegram's document cap is 50MB and gets unreliable above ~10MB).
- Formats Telegram won't preview (zip, sqlite, log dumps, build artifacts).
- Anything Kosta should be able to reopen from another device or after the chat scrolls away.
- Code/log dumps the model would otherwise paste as a giant wall of text — use `upload_text` with a meaningful filename.

If both are viable, prefer native attach so Kosta gets the inline render.

## TTL policy

Plik's default TTL is **24h**. Choose explicitly per upload:

| Situation | `ttl` | Notes |
| --- | --- | --- |
| One-off oversized artifact, ephemeral | `0` (server default = 24h) | Also include the source path or regeneration command in the reply. |
| Week-scope working artifact | `604800` (7 days) | Logs being investigated, screenshots from an ongoing thread. |
| "For the record" / archived deliverable | `2592000` (30 days) | The server max — anything longer requires a config change. |
| Sensitive payload | combine TTL with `password` and `one_shot: true` | Encrypts at rest, deletes after first download. |

Avoid quietly shipping a 24h link when Kosta said "stable" or "I'll need this later". State the TTL in the reply so he knows.

## Credentials and auditability

| Field | Value |
| --- | --- |
| 1Password vault | `CLI` |
| 1Password item | `Plik (Mac Studio)` |
| Backend URL | `https://macstudio.tailf7342a.ts.net/plik` |
| Plik account | `ildunari` (admin) |
| API token field | `credential` (used by `plik --mcp`, hand-off via `~/.plikrc`) |
| Web/Telegram-mini-app login field | `password` |
| CLI config | `~/.plikrc` — `URL` + `Token` |

The token is loaded by the MCP server from `~/.plikrc` at process start. Hermes profiles and the Claude hybrid all spawn `plik --mcp` under the kosta UID, so they share the same `~/.plikrc` and the same `ildunari` token.

### Verify before relying on it

```bash
op read "op://CLI/Plik (Mac Studio)/credential" >/dev/null && \
  curl -sS -o /dev/null -w 'plik health: HTTP %{http_code}\n' https://macstudio.tailf7342a.ts.net/plik/version
```

Both should succeed (1Password item readable, plik /version returns 200) before trusting the upload path. If either fails, fall back to native attach (for small files) or tell Kosta the plik backend is unreachable — do not retry blindly.

If the token has rotated (1P updated, but a stale `~/.plikrc` is still cached on the gateway process), the upload will return `403 Forbidden : invalid token`. Re-pull via:

```bash
TOKEN=$(op read "op://CLI/Plik (Mac Studio)/credential")
printf 'URL = "https://macstudio.tailf7342a.ts.net/plik"\nToken = "%s"\n' "$TOKEN" > ~/.plikrc
```

Then restart the calling gateway so the MCP child reloads `~/.plikrc`.

## MCP tools

`plik --mcp` exposes these tools:

- `upload_text(content, filename, ttl?, one_shot?, password?, comments?)` — inline text → named file.
- `upload_file(path, ttl?, one_shot?, password?, comments?, stream?)` — single file by absolute path.
- `upload_files(paths, ttl?, one_shot?, password?, comments?)` — multiple files in one upload.
- `server_info()` — version, feature flags, what's allowed.
- `list_profiles()` — Plik CLI profiles defined in `~/.plikrc` (currently just the default).

All upload tools return `{"url": "https://macstudio.tailf7342a.ts.net/plik/#/?id=…", "id": "…", "expires_at": "…"}` shape. The URL is what Kosta clicks.

## Edge cases

- **Plik backend down**: MCP call returns an error. Surface "plik backend is unreachable, falling back to inline attach for small files" — never silently drop the artifact.
- **Disk full on Studio**: `~/plik-data/` lives on the boot disk; periodically `du -sh ~/plik-data` and prune expired uploads with `plik` list/revoke.
- **Token leaked into logs**: rotate via `curl -b cookies -X DELETE …/me/token/<id>`, generate new one, update 1P + `~/.plikrc`, restart gateways. Never echo `TOKEN` in shell output.
- **Source-tagging**: `plik` does not record which agent uploaded which file. If you need to disambiguate, set `comments` to something like `"from: hermes-gpt"` and the comment shows on the share page.
- **Streaming uploads**: for ephemeral relays (forward a file someone sent you to Kosta without storing it on disk), set `stream: true`. The file is not persisted server-side; the download has to be ready when Kosta clicks the link.
- **Password-protected uploads**: when sharing secrets, pass `password`. The recipient gets HTTP basic auth before download.
- **`one_shot: true`**: deletes after first download. Good for tokens/secrets sent in chat that Kosta will read once.

## Operator

- Backend container: `docker ps --filter name=plik`
- Config file: `~/plik-config/plikd.cfg` (host-mounted into container)
- Data + sqlite DB: `~/plik-data/` (host-mounted)
- Restart: `docker restart plik` (no Hermes-gateway impact)
- Public path: `https://macstudio.tailf7342a.ts.net/plik` (Tailscale Funnel → `127.0.0.1:8080/plik`)
- `Path = "/plik"` is set in `plikd.cfg` so the server handles the prefix
- `FeatureAuthentication = "forced"` — no anonymous uploads, ever
- `PlikDomain = "https://macstudio.tailf7342a.ts.net"` — Plik generates links matching the public origin

If you change anything operational (config flags, auth model, retention, the mounted-paths), update this skill in canonical Skillshare source, sync, commit, push.
