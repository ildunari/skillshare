# Codex++ Field Guide

This reference summarizes the local read-through of `b-nnett/codex-plusplus` cloned at `/Users/Kosta/LocalDev/codex-plusplus`.

## Project Map

- `README.md`: install, update, writing tweaks, location map, official Codex update warning.
- `docs/ARCHITECTURE.md`: app.asar patch, loader/runtime split, watcher, Sparkle update handling.
- `docs/WRITING-TWEAKS.md`: manifest schema, API surface, lifecycle, update checks, debugging.
- `docs/TROUBLESHOOTING.md`: damaged app/signature recovery, missing Tweaks tab, repair flow.
- `SECURITY.md`: tweaks are local code and should be reviewed before installing or updating.
- `CONTRIBUTING.md`: development commands and release checklist.
- `tweaks/AGENTS.md`: tweak UI style and authoring rules for AI agents.
- `packages/installer/src/cli.ts`: command list and options.
- `packages/installer/src/commands/install.ts`: install sequence.
- `packages/installer/src/commands/update-codex.ts`: macOS official Codex update path.
- `packages/installer/src/commands/self-update.ts`: Codex++ self-update behavior.

## What Codex++ Does

Codex++ patches `Codex.app/Contents/Resources/app.asar` so Electron starts `codex-plusplus-loader.cjs`. The loader points to a runtime under the user data directory. The runtime adds a preload, discovers tweaks, starts main/renderer tweak code, and injects a Tweaks tab into Codex settings.

Most mutable behavior lives outside the app bundle:

- Runtime: `<user-root>/runtime`
- Tweaks: `<user-root>/tweaks`
- Per-tweak data: `<user-root>/tweak-data/<id>`
- Logs: `<user-root>/log`
- State: `<user-root>/state.json`
- Config: `<user-root>/config.json`
- Backup: `<user-root>/backup`

On macOS Kosta's user root is `/Users/Kosta/Library/Application Support/codex-plusplus`.

## Install Sequence

The installer:

1. Locates Codex.
2. Checks bundle writability.
3. Backs up the signed app and original `app.asar`, `Info.plist`, framework binary, and unpacked asar if present.
4. Stages the Codex++ runtime into the user root.
5. Patches `app.asar` package metadata and injects the loader.
6. Updates `ElectronAsarIntegrity` in `Info.plist`.
7. Flips the `EnableEmbeddedAsarIntegrityValidation` Electron fuse off.
8. Re-signs the app ad-hoc on macOS.
9. Installs the launchd watcher.
10. Seeds default tweaks unless `--no-default-tweaks` is used.
11. Writes install state.

For this machine, pass the app explicitly:

```bash
node packages/installer/dist/cli.js install --app "/Applications/Coding/Codex (Beta).app"
```

## Update Paths

Use different commands for different update types:

- `codexplusplus update`: update Codex++ from latest GitHub release, rebuild, and repair the patch.
- `codexplusplus update --ref main`: update Codex++ from development branch when intentionally requested.
- `codexplusplus update-codex`: restore a signed Codex app so Sparkle can update official Codex, then rely on watcher repair after restart.
- `codexplusplus repair`: reapply the patch after Codex updates or when `doctor` detects drift.

Codex++ 0.1.3 also checks hourly for Codex++ releases through the watcher unless auto-update is disabled in the Codex++ Config page.

## Tweak Manifest

Minimum:

```json
{
  "id": "com.you.my-tweak",
  "name": "My Tweak",
  "version": "0.1.0",
  "githubRepo": "you/my-tweak",
  "description": "Does a thing.",
  "scope": "renderer"
}
```

Key fields:

- `id`: reverse-DNS-ish unique id.
- `name`: display name in Tweaks.
- `version`: semver.
- `githubRepo`: owner/repo, required for release checks.
- `scope`: `renderer`, `main`, or `both`; defaults to renderer.
- `main`: custom entry filename.
- `minRuntime`: minimum Codex++ runtime.

Updates are advisory. Codex++ checks GitHub Releases at most once per day and shows an update link. It does not auto-download or replace tweak code.

## Tweak API

Renderer scope commonly uses:

- `api.settings.register({ id, title, description, render })`
- `api.react.waitForElement(selector, timeoutMs?)`
- `api.react.findOwnerByName(node, name)`
- `api.ipc.on/send/invoke`
- `api.fs.read/write/exists`
- `api.storage.get/set/delete/all`
- `api.log.debug/info/warn/error`

Main scope commonly uses:

- `api.ipc.handle`
- `api.fs`
- `api.storage`
- `api.log`

For `scope: "both"`, `start(api)` is called once per process; check `api.process`.

## Tweak UI Rules From AGENTS.md

Use Codex-native styling:

- Prefer Codex tokens over hard-coded colors and dimensions.
- Use grouped cards with `border-token-border`, `divide-token-border`, and `rounded-lg`.
- Use Codex-like rows: `flex items-center justify-between gap-4 p-3`.
- Use Codex-like controls: native toggle switch, Radix-style trigger buttons, link buttons, and danger pills/buttons from `tweaks/AGENTS.md`.
- Do not import React directly.
- Do not ship custom toggle/button styling unless Kosta requested a custom visual direction.
- Do not poll the DOM; wait for elements.
- Do not leave listeners, timers, DOM nodes, or IPC handlers behind after `stop()`.

## Debugging Checklist

- `codexplusplus status`
- `codexplusplus doctor`
- `codexplusplus safe-mode --status`
- `codexplusplus validate-tweak <tweak-dir>`
- `codexplusplus dev <tweak-dir> --replace`
- Logs under `/Users/Kosta/Library/Application Support/codex-plusplus/log`
- DevTools console filtered for `[codex-plusplus]`
- Remote debugging with `CODEXPP_REMOTE_DEBUG=1 open -a "Codex (Beta)"`

If the Tweaks tab does not appear, inspect Settings dialog markup through DevTools or CDP. Tweaks may still load even if settings injection fails.

## Security Notes

Treat tweaks as untrusted local code until reviewed. Main-process tweaks are more powerful than renderer tweaks. Before installing or updating a tweak, review:

- Repository ownership.
- Release notes.
- Changed files.
- Manifest scope and permissions.
- New network or filesystem behavior.

Do not hardcode secrets in tweak code, manifests, scripts, or Skillshare references.

## Local Install Evidence

Successful install on Mac Studio reported:

- App root: `/Applications/Coding/Codex (Beta).app`
- Codex version: `26.429.21146`
- Bundle id: `com.openai.codex.beta`
- Codex++ version: `0.1.3`
- Fuse flipped: `true`
- Re-signed: `true`
- Watcher: `launchd`
- Default tweaks installed: `co.bennett.custom-keyboard-shortcuts`, `co.bennett.ui-improvements`

Validation passed with:

```bash
codexplusplus status
codexplusplus doctor
npm test
```

`npm test` passed 80 tests.
