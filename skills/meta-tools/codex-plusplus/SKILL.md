---
name: codex-plusplus
description: Use when working with Codex++ / codex-plusplus, the b-nnett/codex-plusplus tweak system for the Codex desktop app. Trigger for installing, repairing, updating Codex++, updating the official Codex app while Codex++ is installed, authoring or validating local tweaks, debugging the Tweaks settings tab, or making Kosta-specific Codex UI tweaks. Always use this before modifying /Applications/Coding/Codex (Beta).app, ~/.codex-plusplus, or ~/Library/Application Support/codex-plusplus.
---

# Codex++ Operating Skill

Codex++ patches the local Codex desktop app so it loads a user-directory runtime and local tweaks. Treat it like bundle surgery: inspect state first, keep backups, run the official CLI, and verify with `status` and `doctor` before calling the job done.

## Source Of Truth

- Upstream repo: `https://github.com/b-nnett/codex-plusplus`
- Local clone on Kosta's Mac Studio: `/Users/Kosta/LocalDev/codex-plusplus`
- Installed Codex app on this machine: `/Applications/Coding/Codex (Beta).app`
- Codex++ user root: `/Users/Kosta/Library/Application Support/codex-plusplus`
- Tweaks directory: `/Users/Kosta/Library/Application Support/codex-plusplus/tweaks`
- CLI names: `codexplusplus` preferred, `codex-plusplus` alias

Read `references/codex-plusplus-field-guide.md` before changing install/update behavior. It condenses the repository README, architecture docs, security policy, troubleshooting notes, and `tweaks/AGENTS.md`.

Use `scripts/codexpp-health.sh` for a quick local status snapshot.

## Standard Workflow

1. Check the local clone and installed state:

```bash
cd /Users/Kosta/LocalDev/codex-plusplus
git status --short --branch
git fetch --prune
codexplusplus status
codexplusplus doctor
```

2. If the local clone is behind upstream, pull it, rebuild, and test:

```bash
git pull --ff-only
npm ci --workspaces --include-workspace-root --ignore-scripts
npm run build
npm test
```

3. For Codex++ runtime/CLI updates, use:

```bash
codexplusplus update
```

Use `codexplusplus update --ref main` only when Kosta explicitly wants current development branch behavior instead of the latest release.

4. For official Codex app updates on macOS, use:

```bash
codexplusplus update-codex
```

This restores a Developer ID signed Codex app for Sparkle, then lets the watcher reapply Codex++ after Codex restarts. Do not tell Sparkle to update a patched ad-hoc-signed app directly.

5. If Codex updated and Codex++ did not return, run:

```bash
codexplusplus repair
codexplusplus doctor
```

## Mac Studio Install Notes

The Codex Beta app lives at `/Applications/Coding/Codex (Beta).app`, which upstream auto-detection does not scan. Pass the app explicitly when installing from the clone:

```bash
cd /Users/Kosta/LocalDev/codex-plusplus
npm ci --workspaces --include-workspace-root --ignore-scripts
npm run build
node packages/installer/dist/cli.js install --app "/Applications/Coding/Codex (Beta).app"
```

If install fails during Info.plist writing or codesign because the app bundle has root-owned metadata files, normalize ownership and rerun the install:

```bash
sudo -n chown -R Kosta:staff "/Applications/Coding/Codex (Beta).app"
node packages/installer/dist/cli.js install --app "/Applications/Coding/Codex (Beta).app"
codexplusplus doctor
```

Only use `sudo` for this narrow ownership repair after confirming the target path is the Codex app bundle.

## Tweak Authoring Rules

When creating or editing files under a Codex++ tweak folder, also read `/Users/Kosta/LocalDev/codex-plusplus/tweaks/AGENTS.md`.

Important defaults from that file:

- Match Codex's existing UI patterns unless Kosta asks for a custom look.
- Use Codex Tailwind tokens such as `text-token-*`, `bg-token-*`, `border-token-border`, `px-row-x`, `py-row-y`, `p-panel`, and `h-toolbar`.
- A tweak folder contains `manifest.json` and `index.js` or an explicit `main`.
- Use `module.exports = { start(api), stop() {} }` or `defineTweak`.
- Include `githubRepo` in `owner/repo` form so update checks work.
- Do not import Codex's React directly; use `api.react.*` or vanilla DOM.
- Do not poll the DOM; use `api.react.waitForElement`.
- Make `stop()` idempotent and clean up DOM nodes, IPC listeners, and timers.

## Debugging Tweaks

For live DOM inspection, relaunch Codex with Codex++ remote debugging enabled:

```bash
CODEXPP_REMOTE_DEBUG=1 open -a "Codex (Beta)"
curl -s http://localhost:9222/json | jq '.[] | {id, type, url}'
```

Use the `page` target whose URL starts with `app://-/index.html`. Prefer small probe scripts under `/tmp/probe-codexpp-*.mjs` for repeatable DOM inspection.

Common checks:

```bash
codexplusplus validate-tweak "/path/to/tweak"
codexplusplus dev "/path/to/tweak" --replace
codexplusplus safe-mode --status
tail -n 120 "$HOME/Library/Application Support/codex-plusplus/log/loader.log"
```

## Verification Gate

Before reporting success:

- Run `codexplusplus status`.
- Run `codexplusplus doctor`.
- For repo changes, run `npm test` from `/Users/Kosta/LocalDev/codex-plusplus`.
- For tweak changes, run `codexplusplus validate-tweak <tweak-dir>`.
- If the work affects UI, verify the running Codex app or capture evidence from DevTools/CDP.

Report the exact app path, user root, tweaks dir, and whether doctor passed.
