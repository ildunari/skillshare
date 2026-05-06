---
name: serve-sim
description: Use when Kosta wants to install, run, verify, or integrate Evan Bacon's `serve-sim` for iOS Simulator browser inspection, Codex/browser-agent mobile testing, or remote simulator streaming. Trigger on mentions of `serve-sim`, inspecting iOS app elements in Codex/browser, streaming Apple/iOS Simulator to localhost, or adding simulator preview support to Expo/Metro/dev servers.
targets: [hermes-default, hermes-gpt, claude-hermes]
---

# serve-sim

Use this for Evan Bacon's `serve-sim`: the `npx serve`-style tool for exposing a booted Apple/iOS Simulator in a browser for humans and browser/Codex agents.

Upstream:
- Repo: `https://github.com/EvanBacon/serve-sim`
- npm package: `serve-sim`
- Current verified install on May 5, 2026: `serve-sim` `0.1.13`

## What it does

`serve-sim` captures a booted Simulator framebuffer via a small Swift helper, serves an MJPEG/WebSocket control surface, and opens a browser preview at `http://localhost:3200` by default. It is app-agnostic: works for SwiftUI, UIKit, React Native, Expo, etc. because it talks to the Simulator, not the app internals.

Typical use:

```bash
serve-sim
# Preview at http://localhost:3200
```

Target a specific simulator:

```bash
serve-sim "iPhone 17 Pro"
```

Daemon mode:

```bash
serve-sim --detach
serve-sim --list
serve-sim --kill
```

## Install / verify

Requires macOS, Node.js 18+, and Xcode simulator tooling (`xcrun simctl`). Bun is not required to run the CLI.

```bash
npm install -g serve-sim
command -v serve-sim
serve-sim --help
npm view serve-sim version
xcrun simctl list devices available | sed -n '1,40p'
serve-sim --list || true
```

Expected idle verification:

```text
serve-sim --list -> {"running":false}
```

On Kosta's machines as of May 5, 2026:
- Mac Studio: `/Users/Kosta/.npm-global/bin/serve-sim`, version `0.1.13`, iOS 26.x simulators available.
- MacBook Pro: `/opt/homebrew/bin/serve-sim`, version `0.1.13`, iOS 26.4 simulators available.

## MacBook from Studio

The MacBook is reachable over Tailscale using the service-account-readable key:

```bash
op read 'op://CLI/MacBook Pro SSH Key/private_key' > /tmp/hermes-ssh/macbook_key
chmod 600 /tmp/hermes-ssh/macbook_key
ssh -i /tmp/hermes-ssh/macbook_key \
  -o IdentityAgent=none -o IdentitiesOnly=yes \
  kosta@100.83.186.114 'serve-sim --help'
```

Use `-o IdentityAgent=none`; otherwise the 1Password SSH agent may hijack explicit key auth and fail.

## Common workflows

### Browser/Codex inspection

1. Boot or launch the simulator/app.
2. Run `serve-sim`.
3. Open `http://localhost:3200` in a browser or agent-browser/Codex browser.
4. Inspect/interact with the simulator preview.

If no simulator is booted, either boot one first or pass a device name and let `serve-sim` target it:

```bash
xcrun simctl boot "iPhone 17 Pro" || true
open -a Simulator
serve-sim "iPhone 17 Pro"
```

### Expo / Metro integration

For Expo projects, upstream supports mounting the preview at `/.sim` by adding `serve-sim/middleware` to `metro.config.js`. Check the upstream README before editing because the package is new and APIs may move.

Default pattern from upstream:

```js
const { getDefaultConfig } = require("expo/metro-config");
const connect = require("connect");
const { simMiddleware } = require("serve-sim/middleware");

const config = getDefaultConfig(__dirname);
config.server = config.server || {};
const originalEnhanceMiddleware = config.server.enhanceMiddleware;
config.server.enhanceMiddleware = (metroMiddleware, server) => {
  const middleware = originalEnhanceMiddleware
    ? originalEnhanceMiddleware(metroMiddleware, server)
    : metroMiddleware;
  const app = connect();
  app.use(simMiddleware({ basePath: "/.sim" }));
  app.use(middleware);
  return app;
};
module.exports = config;
```

## Pitfalls

- This is a young package. Check upstream README/current npm version before relying on undocumented flags.
- `serve-sim --list` showing `{"running":false}` is normal when no helper is active; it still verifies the CLI is installed.
- It needs Xcode simulator tooling on the host. On a non-Mac or Mac without Simulator runtimes, install verification can pass while runtime usage fails.
- If remote access is needed, tunnel or port-forward `localhost:3200`; do not expose it publicly without a boundary because it provides simulator interaction.
- If an explicit SSH key fails with `sign_and_send_pubkey` from the 1Password agent, retry with `-o IdentityAgent=none -o IdentitiesOnly=yes`.

## Good handoff

Report:
- installed path and npm version
- simulator availability from `xcrun simctl list devices available`
- idle/running status from `serve-sim --list`
- any machine-specific remote access caveats
