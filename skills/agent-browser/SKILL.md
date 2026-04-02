---
name: agent-browser
description: >
  Browser automation CLI for AI agents using agent-browser (Vercel, Rust).
  Use when the user needs to interact with websites — navigating pages,
  filling forms, clicking buttons, taking screenshots, extracting data,
  testing web apps, scraping content, or automating any browser task.
  Triggers on: "open a website", "fill out a form", "take a screenshot",
  "scrape data", "test this web app", "login to a site", "automate browser",
  "browse to", "check this page", "download from site", "web automation",
  or any task requiring programmatic web interaction. Also use when the user
  needs to access authenticated pages using their real Chrome sessions via CDP.
  Do not use for simple curl/wget fetches of public URLs or API calls.
targets: [claude, codex, cursor, windsurf]
allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*)
---

# Browser Automation with agent-browser

Rust CLI for browser automation via Chrome DevTools Protocol. Install: `npm i -g agent-browser` or `brew install agent-browser`. Version: v0.23.x+.

## Core Workflow

Every browser task follows this loop:

```bash
agent-browser open <url>           # 1. Navigate
agent-browser snapshot -i          # 2. Get element refs (@e1, @e2...)
agent-browser click @e3            # 3. Interact using refs
agent-browser snapshot -i          # 4. Re-snapshot after DOM changes
```

Refs (`@e1`, `@e2`) are invalidated on navigation or DOM changes. Always re-snapshot after clicks, form submissions, or dynamic content loads.

## Authentication — Choosing the Right Approach

| Scenario | Approach | Detail |
|----------|----------|--------|
| Need user's existing Google/SSO logins | **CDP to real Chrome** | `--cdp 9222` — see [references/real-chrome-cdp.md](references/real-chrome-cdp.md) |
| Recurring automation on one site | **Persistent profile** | `--profile ~/.myapp` |
| One-off authenticated task | **Session name** | `--session-name myapp` (auto-saves cookies) |
| Stored credentials | **Auth vault** | `auth save name --url ... --username ... --password-stdin` |
| Export/import from browser | **State file** | `state save auth.json` / `state load auth.json` |

**Google auth blocks Playwright Chromium.** If you need Google login, use CDP to real Chrome (see reference). For other sites, persistent profile or session-name works.

See [references/authentication.md](references/authentication.md) for OAuth, 2FA, and token refresh patterns.

## Essential Commands

```bash
# Navigation
agent-browser open <url>                  # Navigate (aliases: goto, navigate)
agent-browser back / forward / reload     # History navigation
agent-browser close [--all]               # Close session(s)

# Snapshot (primary way to discover elements)
agent-browser snapshot -i                 # Interactive elements with refs
agent-browser snapshot -s "#selector"     # Scoped to CSS selector

# Interaction (use @refs from snapshot)
agent-browser click @e1                   # Click element
agent-browser fill @e2 "text"             # Clear and type
agent-browser type @e2 "text"             # Type without clearing
agent-browser select @e1 "option"         # Select dropdown
agent-browser check @e1 / uncheck @e1    # Checkbox
agent-browser press Enter                 # Press key
agent-browser keyboard type "text"        # Type at current focus
agent-browser scroll down 500             # Scroll page

# Get information
agent-browser get text @e1                # Element text
agent-browser get url / title             # Page URL or title

# Wait
agent-browser wait @e1                    # Wait for element
agent-browser wait --load networkidle     # Wait for network idle
agent-browser wait --url "**/dashboard"   # Wait for URL pattern
agent-browser wait --text "Welcome"       # Wait for text
agent-browser wait 2000                   # Wait milliseconds

# Capture
agent-browser screenshot                  # Screenshot to temp dir
agent-browser screenshot --full           # Full page
agent-browser screenshot --annotate       # With numbered element labels
agent-browser pdf output.pdf              # Save as PDF

# Downloads
agent-browser download @e1 ./file.pdf     # Click to download
agent-browser wait --download ./out.zip   # Wait for download

# JavaScript
agent-browser eval 'document.title'       # Simple expression
agent-browser eval --stdin <<'EOF'        # Complex JS (avoids shell quoting)
JSON.stringify(Array.from(document.querySelectorAll("a")).map(a => a.href))
EOF
```

## Command Chaining

Chain with `&&` when you don't need intermediate output:

```bash
agent-browser open https://example.com && agent-browser wait --load networkidle && agent-browser snapshot -i
```

Run separately when you need to parse refs between steps.

## CDP Connection (Real Chrome)

Connect to a running Chrome instance to reuse existing sessions:

```bash
# Auto-discover running Chrome
agent-browser --auto-connect snapshot

# Explicit CDP port
agent-browser --cdp 9222 snapshot

# Launch Chrome with CDP (requires separate data dir)
~/.agent-browser/launch-chrome-cdp.sh
agent-browser --cdp 9222 open https://mail.google.com
```

Full setup guide: [references/real-chrome-cdp.md](references/real-chrome-cdp.md)

## Parallel Sessions

```bash
agent-browser --session site1 open https://site-a.com
agent-browser --session site2 open https://site-b.com
agent-browser session list
```

## Common Patterns

### Form Submission
```bash
agent-browser open https://example.com/signup
agent-browser snapshot -i
agent-browser fill @e1 "Jane Doe" && agent-browser fill @e2 "jane@example.com"
agent-browser select @e3 "California"
agent-browser check @e4 && agent-browser click @e5
agent-browser wait --load networkidle
```

### Data Extraction
```bash
agent-browser open https://example.com/products
agent-browser snapshot -i
agent-browser get text @e5                    # Specific element
agent-browser get text body > page.txt        # Full page text
agent-browser snapshot -i --json              # Structured JSON output
```

### Visual Diff
```bash
agent-browser snapshot -i                     # Baseline
agent-browser click @e2                       # Action
agent-browser diff snapshot                   # See what changed
```

### Responsive Testing
```bash
agent-browser set viewport 1920 1080 && agent-browser screenshot desktop.png
agent-browser set viewport 375 812 && agent-browser screenshot mobile.png
agent-browser set device "iPhone 14" && agent-browser screenshot device.png
```

### Batch Execution
```bash
echo '[["open","https://example.com"],["snapshot","-i"],["screenshot","out.png"]]' \
  | agent-browser batch --json
```

## Security

All opt-in. Default: no restrictions.

```bash
# Content boundaries (recommended for AI agents)
export AGENT_BROWSER_CONTENT_BOUNDARIES=1

# Domain allowlist
export AGENT_BROWSER_ALLOWED_DOMAINS="example.com,*.example.com"

# Output limit (prevent context flooding)
export AGENT_BROWSER_MAX_OUTPUT=50000

# Action policy
export AGENT_BROWSER_ACTION_POLICY=./policy.json
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `AGENT_BROWSER_AUTO_CONNECT` | Auto-discover running Chrome |
| `AGENT_BROWSER_HEADED` | Show browser window |
| `AGENT_BROWSER_COLOR_SCHEME` | `dark` or `light` |
| `AGENT_BROWSER_CONTENT_BOUNDARIES` | Wrap output in markers |
| `AGENT_BROWSER_MAX_OUTPUT` | Truncate output at N chars |
| `AGENT_BROWSER_ALLOWED_DOMAINS` | Restrict navigation |
| `AGENT_BROWSER_DEFAULT_TIMEOUT` | Default timeout in ms |
| `AGENT_BROWSER_IDLE_TIMEOUT_MS` | Auto-shutdown daemon |
| `AGENT_BROWSER_ENCRYPTION_KEY` | 64-char hex key for state encryption |
| `AGENT_BROWSER_ENGINE` | `chrome` (default) or `lightpanda` |
| `AGENT_BROWSER_SESSION` | Default session name |
| `AGENT_BROWSER_SESSION_NAME` | Auto-save/restore state by name |
| `AGENT_BROWSER_STREAM_PORT` | Live WebSocket preview port |

## Iframes

Refs inside iframes work directly — no frame switching needed:

```bash
agent-browser snapshot -i
# @e3 [input] "Card number" (inside iframe)
agent-browser fill @e3 "4111111111111111"    # Just works
```

## Dialogs

JS dialogs (alert/confirm/prompt) block all commands:

```bash
agent-browser dialog status                   # Check if dialog is pending
agent-browser dialog accept                   # Accept
agent-browser dialog accept "input text"      # Accept with input
agent-browser dialog dismiss                  # Cancel
```

## Cleanup

Always close when done:

```bash
agent-browser close                           # Close default session
agent-browser --session name close            # Close specific session
agent-browser close --all                     # Close everything
```

## Deep-Dive References

| Reference | When to read |
|-----------|-------------|
| [references/real-chrome-cdp.md](references/real-chrome-cdp.md) | Setting up CDP with real Chrome for Google auth and existing sessions |
| [references/authentication.md](references/authentication.md) | OAuth, 2FA, cookie-based auth, token refresh |
| [references/commands.md](references/commands.md) | Full command reference with all options and flags |
| [references/snapshot-refs.md](references/snapshot-refs.md) | Ref lifecycle, invalidation rules, troubleshooting |
| [references/session-management.md](references/session-management.md) | Parallel sessions, state persistence |
| [references/video-recording.md](references/video-recording.md) | Recording workflows for debugging |
| [references/profiling.md](references/profiling.md) | Chrome DevTools profiling |
| [references/proxy-support.md](references/proxy-support.md) | Proxy configuration, rotating proxies |

## iOS Simulator

```bash
agent-browser device list
agent-browser -p ios --device "iPhone 16 Pro" open https://example.com
agent-browser -p ios snapshot -i
agent-browser -p ios tap @e1
agent-browser -p ios swipe up
agent-browser -p ios close
```

Requires macOS + Xcode + Appium (`npm install -g appium && appium driver install xcuitest`).

## Browser Engines

```bash
agent-browser --engine chrome open example.com      # Default
agent-browser --engine lightpanda open example.com  # 10x faster, 10x less memory
```

Lightpanda doesn't support `--profile`, `--state`, or `--extension`.
