# Real Chrome CDP Setup

Connect agent-browser to your actual Chrome browser — with all your existing logins, cookies, passwords, and Google auth sessions. This solves the "Google blocks automated Chromium" problem.

## Why This Exists

Google (and other services) detect Playwright's bundled Chromium as an automated browser and block sign-in. The fix: connect agent-browser to your real Chrome app via Chrome DevTools Protocol (CDP). Your real Chrome has a real fingerprint, real cookies, and real sessions — no bot detection issues.

## The Problem with Default Profile

Chrome **refuses** to enable CDP on its default data directory (`~/Library/Application Support/Google/Chrome/`). You must use a separate `--user-data-dir`. This means you can't directly tap into your existing Chrome sessions via `--user-data-dir`.

## Solution: Dedicated CDP Profile

Create a separate Chrome data directory for agent-browser, sign in once, and reuse it forever.

### One-Time Setup

```bash
# Create the dedicated profile directory
mkdir -p ~/.chrome-cdp

# Kill any running Chrome (required — Chrome can only have one instance per data dir)
pkill -9 -f "Google Chrome" 2>/dev/null; sleep 2

# Launch real Chrome with CDP enabled
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --remote-debugging-port=9222 \
    --remote-debugging-address=127.0.0.1 \
    --user-data-dir="$HOME/.chrome-cdp" \
    >/dev/null 2>&1 &
disown

# Verify CDP is running
sleep 5 && curl -s http://127.0.0.1:9222/json/version | python3 -m json.tool
```

A Chrome window opens. **Sign into Google** (and any other services you need). This is real Chrome — Google auth works normally. Close Chrome when done; the profile persists at `~/.chrome-cdp/`.

### Launch Script

Save this at `~/.agent-browser/launch-chrome-cdp.sh`:

```bash
#!/bin/bash
CDP_PORT="${1:-9222}"
CDP_DIR="$HOME/.chrome-cdp"

if curl -s "http://127.0.0.1:$CDP_PORT/json/version" >/dev/null 2>&1; then
    echo "Chrome CDP already running on port $CDP_PORT"
    exit 0
fi

"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --remote-debugging-port="$CDP_PORT" \
    --remote-debugging-address=127.0.0.1 \
    --user-data-dir="$CDP_DIR" \
    >/dev/null 2>&1 &
disown

echo "Chrome CDP launching on port $CDP_PORT (profile: $CDP_DIR)"
```

### Usage

```bash
# Start the CDP Chrome (idempotent — skips if already running)
~/.agent-browser/launch-chrome-cdp.sh

# Connect agent-browser
agent-browser --cdp 9222 open https://mail.google.com
agent-browser --cdp 9222 snapshot -i

# Or set auto-connect globally
export AGENT_BROWSER_AUTO_CONNECT=1
agent-browser snapshot -i
```

### Environment Variables

Add to `~/.zshrc` for persistent setup:

```bash
export AGENT_BROWSER_AUTO_CONNECT=1
```

### Multiple Profiles

For Brown University or other accounts, create separate profile dirs:

```bash
# Personal Google
~/.chrome-cdp/       # port 9222

# Brown University
~/.chrome-cdp-brown/ # port 9223
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --remote-debugging-port=9223 \
    --user-data-dir="$HOME/.chrome-cdp-brown" &
```

### Your Regular Chrome Is Unaffected

The CDP Chrome uses a completely separate data directory (`~/.chrome-cdp`). Your normal Chrome launched from the Dock stays exactly as-is — different sessions, different windows, no interference.

### Security Notes

- CDP is bound to `127.0.0.1` only — not accessible from the network
- Only local processes can connect to port 9222
- The `~/.chrome-cdp` profile contains session cookies — treat it like a credential store
- Add `~/.chrome-cdp/` to your backup exclusions if desired

### Troubleshooting

**CDP port not responding after launch:**
- Chrome takes 3-5 seconds to bind. Wait and retry: `sleep 5 && curl -s http://127.0.0.1:9222/json/version`
- Check if another Chrome instance owns the port: `lsof -i :9222`

**"non-default data directory" error:**
- You used the default Chrome profile path. Use `~/.chrome-cdp` or any other custom path.

**Google still blocking sign-in:**
- You're probably in agent-browser's built-in Chromium, not real Chrome. Verify with `curl -s http://127.0.0.1:9222/json/version | grep Browser` — it should say `Chrome/`, not `Chromium/`.

**Two Chrome instances conflict:**
- Each `--user-data-dir` can only have one Chrome instance. Kill the old one before launching with a new port.
