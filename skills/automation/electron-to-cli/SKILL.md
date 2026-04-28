---
name: electron-to-cli
description: >
  Use when turning an Electron or Chromium desktop app into a programmable CLI, MCP server, API
  wrapper, or direct automation harness. Also use for requests to automate apps like Slack,
  Discord, VS Code, Notion, Figma, Obsidian, or Spotify via CDP, internal API discovery, token
  extraction, or agent-browser control.
---

# Electron App → CLI/MCP/API Converter

A structured methodology for converting any Electron desktop app into a fully programmable
CLI tool, MCP server, or API wrapper. This process has been validated on Discord and applies
to any Chromium-based desktop application.

## Overview

Every Electron app is a Chromium browser with Node.js access. This means every Electron app
exposes the Chrome DevTools Protocol (CDP) when launched with `--remote-debugging-port=NNNN`.
Through CDP you can: snapshot the UI, execute JavaScript in the app's renderer context,
intercept network requests, extract auth tokens, and discover internal APIs.

The goal is to move **away** from UI automation (slow, fragile, token-expensive) and toward
**direct API calls** (fast, reliable, token-cheap) wherever possible. CDP is the
reconnaissance tool, not the production interface.

## Phase 1: Reconnaissance

### Step 1.1 — Identify the App

```bash
# Find the app
ls /Applications/ | grep -i "<app_name>"
# Or search for running processes
pgrep -fl "<app_name>"
# Get app details
plutil -convert json -o - "/Applications/<App>.app/Contents/Info.plist" | python3 -c "
import json, sys; d = json.load(sys.stdin)
print(f'Version: {d.get(\"CFBundleShortVersionString\", \"?\")}')"
```

Record: app path, version, Electron version, bundle ID.

### Step 1.2 — Launch with CDP

Quit any running instance first, then relaunch with remote debugging:

```bash
osascript -e 'tell application "<App Name>" to quit' 2>/dev/null || true
sleep 2
open -a "<App Name>" --args --remote-debugging-port=<PORT>
sleep 5
# Verify CDP is active
curl -s http://127.0.0.1:<PORT>/json/version
```

**Port assignment convention** (avoid conflicts):
| Port | App |
|------|-----|
| 9222 | Slack |
| 9223 | VS Code |
| 9224 | Discord |
| 9225 | Figma |
| 9226 | Notion |
| 9227 | Spotify |
| 9228 | Telegram |
| 9229 | Signal |
| 9230+ | Others |

### Step 1.3 — Enumerate CDP Targets

```bash
curl -s http://127.0.0.1:<PORT>/json/list | python3 -c "
import json, sys
for i, t in enumerate(json.load(sys.stdin)):
    print(f'[{i}] type={t.get(\"type\")} title={t.get(\"title\",\"\")[:50]} url={t.get(\"url\",\"\")[:60]}')"
```

Find the main page target (type=page with the app's URL). Note the `webSocketDebuggerUrl`.

### Step 1.4 — Snapshot the UI

```bash
# Use --cdp flag (not connect) for Electron apps — avoids about:blank issues
agent-browser --cdp <PORT> snapshot -i
```

**Key insight from Discord**: `agent-browser connect <PORT>` creates a new blank page.
Use `agent-browser --cdp <PORT> <command>` instead — this attaches to the existing app page.

### Step 1.5 — Discover Internal APIs

Every Electron app has internal JavaScript APIs accessible via CDP eval. Check for:

```bash
# Check for app-specific native bridge
agent-browser --cdp <PORT> eval --stdin <<'EOF'
(function() {
  var results = {};
  // Common Electron app patterns
  results.hasWebpack = typeof webpackChunkdiscord_app !== 'undefined'
    || typeof webpackChunk_N_E !== 'undefined'
    || typeof __webpack_require__ !== 'undefined';
  // App-specific native bridges
  var bridges = ['DiscordNative', 'SlackNative', 'electron', 'require'];
  bridges.forEach(function(b) {
    results['has_' + b] = typeof window[b] !== 'undefined';
    if (typeof window[b] !== 'undefined' && typeof window[b] === 'object') {
      results[b + '_keys'] = Object.keys(window[b]);
    }
  });
  // Check localStorage for tokens/state
  try {
    var iframe = document.createElement('iframe');
    iframe.style.display = 'none';
    document.body.appendChild(iframe);
    var ls = iframe.contentWindow.localStorage;
    var tokenKeys = [];
    for (var i = 0; i < ls.length; i++) {
      var key = ls.key(i);
      if (key.toLowerCase().includes('token') || key.toLowerCase().includes('auth')
          || key.toLowerCase().includes('session')) {
        tokenKeys.push({key: key, length: (ls.getItem(key) || '').length});
      }
    }
    document.body.removeChild(iframe);
    results.authKeys = tokenKeys;
  } catch(e) { results.localStorageError = e.message; }
  return JSON.stringify(results, null, 2);
})();
EOF
```

### Step 1.6 — Probe for Local Servers

Many Electron apps expose local HTTP/WebSocket/IPC servers:

```bash
# Check common local ports
for port in 6463 6464 6465 8080 8081 3000 5000 9090; do
  resp=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:$port" 2>/dev/null)
  [[ "$resp" != "000" ]] && echo "Port $port: HTTP $resp"
done

# Check for Unix domain sockets (IPC)
find "$TMPDIR" /tmp -maxdepth 2 -name "*<app_name>*" 2>/dev/null
ls -la "$TMPDIR" 2>/dev/null | grep -i "<app_name>"
```

### Step 1.7 — Extract Auth Token

Three approaches, in order of preference:

**Method A: Fetch interceptor (most reliable)**
```bash
# Install interceptor
agent-browser --cdp <PORT> eval --stdin <<'EOF'
(function() {
  var origFetch = window.fetch;
  window.__capturedToken = null;
  window.fetch = function() {
    if (arguments[1] && arguments[1].headers) {
      var h = arguments[1].headers;
      if (h.Authorization) window.__capturedToken = h.Authorization;
    }
    return origFetch.apply(this, arguments);
  };
  return 'Interceptor installed';
})();
EOF

# Trigger an API call (click something in the UI)
agent-browser --cdp <PORT> snapshot -i
agent-browser --cdp <PORT> click @e<N>  # click a navigation element
sleep 2

# Retrieve captured token
agent-browser --cdp <PORT> eval 'window.__capturedToken'
```

**Method B: localStorage/sessionStorage**
```bash
agent-browser --cdp <PORT> eval --stdin <<'EOF'
(function() {
  var iframe = document.createElement('iframe');
  iframe.style.display = 'none';
  document.body.appendChild(iframe);
  var token = iframe.contentWindow.localStorage.getItem('token');
  document.body.removeChild(iframe);
  return token;
})();
EOF
```

Note: Many apps now encrypt localStorage tokens via OS keychain (e.g., Discord's
`safeStorage`). If the token appears encrypted (has a non-standard prefix like
`dQw4w9WgXcQ:`), fall back to Method A.

**Method C: Network interception via CDP**
Use Chrome DevTools Protocol directly to intercept network requests — useful when
agent-browser eval isn't working. Connect via WebSocket to the CDP endpoint and
enable Network domain monitoring.

### Step 1.8 — Test the Service's REST API

Once you have a token, test it against the service's known REST API:

```bash
# Test from within the app's context (avoids CORS)
agent-browser --cdp <PORT> eval --stdin <<'EOF'
(function() {
  var token = window.__capturedToken;
  return fetch('https://api.service.com/v1/me', {
    headers: {'Authorization': token}
  }).then(function(r) { return r.json(); }).then(function(d) {
    return JSON.stringify(d, null, 2);
  });
})();
EOF

# Or test directly via curl (if API allows it)
curl -s -H "Authorization: <TOKEN>" https://api.service.com/v1/me
```

### Step 1.9 — Multi-App Simultaneous Automation

When you need to automate or compare multiple Electron apps at the same time, use named sessions to keep them isolated:

```bash
# Connect to multiple apps simultaneously
agent-browser --session slack connect 9222
agent-browser --session vscode connect 9223
agent-browser --session discord connect 9224

# Interact with each independently
agent-browser --session slack snapshot -i
agent-browser --session vscode snapshot -i
agent-browser --session discord snapshot -i

# Screenshots per-app
agent-browser --session slack screenshot slack-state.png
agent-browser --session vscode screenshot vscode-state.png
```

Named sessions persist until the agent-browser process exits. Use descriptive session names matching the app's common identifier.

**Color scheme note:** agent-browser overrides color scheme to `light` by default via CDP. Preserve dark mode with:

```bash
agent-browser --session slack --color-scheme dark snapshot -i
# Or globally:
AGENT_BROWSER_COLOR_SCHEME=dark agent-browser --session slack connect 9222
```

**Tab management in Electron apps:**

Electron apps often expose multiple windows or webviews. Use `tab` commands to list and switch:

```bash
agent-browser --session slack tab          # list all targets
agent-browser --session slack tab 2        # switch by index
agent-browser --session slack tab --url "*settings*"  # switch by URL pattern
```

## Phase 2: Architecture Decision

Based on reconnaissance, choose the optimal architecture:

### Decision Matrix

| Factor | CLI (Bash+curl) | Node.js CLI | MCP Server | Browser Wrapper |
|--------|----------------|-------------|------------|-----------------|
| REST API available | Best choice | Good | Good | Overkill |
| No REST API | N/A | N/A | N/A | Only option |
| WebSocket needed | Poor | Best | Good | Poor |
| Token efficiency | Excellent | Good | Medium | Poor |
| Speed | Fast | Fast | Medium | Slow |
| Dependencies | None (curl) | Node.js | Node.js | agent-browser |
| Composability | Excellent (pipes) | Good | Limited | Poor |
| Real-time events | No | Yes | Yes | No |

### When to Use Each

**CLI (Bash + HTTP client)** — Default choice when a REST API exists. Matches existing patterns
(bird, gog), zero dependencies, excellent token efficiency, pipe-friendly.

**Node.js CLI** — When WebSocket features are needed (real-time events, streaming),
or when the API client library is significantly better than raw curl.

**MCP Server** — When the tool needs to be consumed by other AI agents, or when
the interaction pattern is request-response with tool schemas.

**Browser Wrapper (CDP)** — Last resort. Only when there's no API and all functionality
is UI-only. Token-expensive, slow, fragile. Use sparingly for specific operations
that have no API equivalent (e.g., navigating to a specific view, screenshots).

### Hybrid Pattern (Recommended)

Most apps benefit from a **hybrid** approach:
- **Primary**: REST API via CLI (fast, reliable, cheap)
- **Secondary**: CDP via agent-browser (UI-only operations)

This is what the Discord CLI does: REST API for all data operations, CDP only for
`navigate` and `screenshot`.

## Phase 3: Build the CLI

### Step 3.1 — Scaffold

Use this template for a shell CLI backed by an HTTP client:

```bash
#!/usr/bin/env bash
set -euo pipefail

# ── Config ──
API_BASE="https://api.service.com/v1"
KEYCHAIN_SERVICE="<app>-cli-token"
KEYCHAIN_ACCOUNT="<app>-user"
CDP_PORT=<PORT>
APP_PATH="/Applications/<App>.app"
JSON_OUTPUT=false
LIMIT=25

# ── Parse global flags ──
args=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --json) JSON_OUTPUT=true; shift ;;
    --limit) LIMIT="$2"; shift 2 ;;
    *) args+=("$1"); shift ;;
  esac
done
set -- "${args[@]+"${args[@]}"}"
COMMAND="${1:-help}"; shift || true

# ── Token management ──
get_cached_token() {
  security find-generic-password -s "$KEYCHAIN_SERVICE" -a "$KEYCHAIN_ACCOUNT" -w 2>/dev/null || echo ""
}
cache_token() {
  security delete-generic-password -s "$KEYCHAIN_SERVICE" -a "$KEYCHAIN_ACCOUNT" 2>/dev/null || true
  security add-generic-password -s "$KEYCHAIN_SERVICE" -a "$KEYCHAIN_ACCOUNT" -w "$1"
}
# ... (see Discord CLI for full token extraction via CDP)

# ── API helper ──
api() {
  local method="$1" endpoint="$2"; shift 2
  local token=$(get_token)
  http_request "$method" "$API_BASE/$endpoint" "$token" "$@"
}

# ── Commands ──
# ... one function per command

# ── Dispatch ──
case "$COMMAND" in
  help) cmd_help ;;
  # ... map commands to functions
  *) die "Unknown: $COMMAND" ;;
esac
```

### Step 3.2 — Command Design Principles

1. **Match the service's domain language** — If the API calls them "workspaces", the CLI
   should too. Don't rename concepts.

2. **Support name resolution** — Accept human-readable names, not just IDs.
   Do fuzzy matching internally.

3. **Always support --json** — Machine-readable output for scripting and AI consumption.

4. **Always support --no-input** — Non-interactive mode for automation.

5. **Default to human-readable** — Without --json, show formatted text output.

6. **Token caching in Keychain** — Never store tokens in plaintext files. Use macOS
   Keychain (`security` CLI) or equivalent OS credential store.

7. **Auto-refresh on 401** — When a cached token expires, transparently re-extract
   and retry the request.

### Step 3.3 — Install and Link

```bash
chmod +x /path/to/cli-script
ln -sf /path/to/cli-script /opt/homebrew/bin/<app-name>
```

## Phase 4: Create Craft Agent Integration

### Step 4.1 — Source (config.json + guide.md + permissions.json)

Create in `~/.craft-agent/workspaces/<ws>/sources/<app>/`:

- **config.json** — type: "local", point to the source directory
- **guide.md** — CLI reference, command table, flags, guidelines, user context
- **permissions.json** — Allow read-only CLI commands in Explore mode

### Step 4.2 — Skill (SKILL.md)

Create in `~/.craft-agent/workspaces/<ws>/skills/<app>/`:

- Include `requiredSources: [<app>]` to auto-enable the source
- Document the CLI commands with examples
- Include the user's specific context (accounts, servers, workspaces)

### Step 4.3 — Validate

```bash
# Validate the skill
mcp__session__skill_validate({ skillSlug: "<app>" })
# Test the source
mcp__session__source_test({ sourceSlug: "<app>" })
```

## Troubleshooting Reference

### CDP Connection Issues

| Problem | Cause | Fix |
|---------|-------|-----|
| "Connection refused" | App not launched with CDP flag | Quit and relaunch with --remote-debugging-port |
| Snapshot shows "about:blank" | `connect` created new page | Use `--cdp <PORT>` flag instead of `connect` |
| eval returns wrong context | Multiple webviews | Use `tab` to list targets, select the right one |
| Elements not in snapshot | Lazy-loaded content | Navigate first to trigger loading, then re-snapshot |

### Token Extraction Issues

| Problem | Cause | Fix |
|---------|-------|-----|
| localStorage token encrypted | OS keychain encryption | Use fetch interceptor (Method A) instead |
| Interceptor captures nothing | App uses custom HTTP client | Click a navigation element to force API calls |
| Token works in-app but not curl | CORS or cookie-based auth | Make API calls from within app context via eval |
| 401 with extracted token | Token format wrong | Check if prefix needs stripping (e.g., "Bearer ") |

### Webpack Module Discovery

Many Electron apps use webpack. The module cache may be sparse due to lazy loading.
When store/module discovery returns few results:
- Navigate to different views in the app to trigger module loading
- Search for `webpackChunk*` global variables (app-specific names)
- Check `window.__NEXT_DATA__` for Next.js-based apps
- Look for Flux/Redux stores via dispatcher patterns

## Known App Patterns

| App | Native Bridge | API Base | Token Location | IPC Socket |
|-----|--------------|----------|----------------|------------|
| Discord | `DiscordNative` | discord.com/api/v10 | localStorage (encrypted) | $TMPDIR/discord-ipc-0 |
| Slack | `SlackNative` | api.slack.com | localStorage | — |
| VS Code | `vscode` | — (local only) | — | — |
| Notion | — | api.notion.com | Cookie-based | — |
| Spotify | — | api.spotify.com | OAuth token | — |
| Figma | — | api.figma.com | localStorage | — |
| Telegram | — | — (MTProto) | tdlib session | — |
| Signal | — | — (Signal Protocol) | SQLCipher DB | — |

## Architectural Lessons Learned

1. **CDP is for reconnaissance, not production** — Use it to discover APIs and extract
   tokens, then build the CLI against the REST API directly.

2. **`--cdp <PORT>` not `connect`** — For Electron apps, `agent-browser connect` opens a
   new blank page. Always use the `--cdp` flag on each command instead.

3. **Encrypted tokens are common now** — Discord, Slack, and others encrypt localStorage
   tokens via `safeStorage`/OS keychain. The fetch interceptor pattern (install a hook on
   `window.fetch`, trigger a navigation, read the captured Authorization header) is the
   most reliable extraction method.

4. **Lazy-loaded webpack modules** — Don't expect to find all stores/modules on first scan.
   Navigate around the app to trigger lazy loading before enumerating.

5. **The iframe trick for localStorage** — `iframe.contentWindow.localStorage` bypasses
   some apps' CSP restrictions on direct localStorage access.

6. **Token caching beats re-extraction** — Extracting a token via CDP takes 5-10 seconds
   and requires the app to be running. Cache in macOS Keychain and only re-extract on 401.

7. **Hybrid architecture wins** — REST API for speed/reliability, CDP for UI-only operations.
   This gives the best of both worlds.

8. **Match existing CLI patterns** — If the user already has CLIs (bird, gog), match their
   flag conventions (--json, --no-input, --limit) for consistency.
