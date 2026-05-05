---
name: non-hermes-update-audit
description: Audit and update non-Hermes local apps/tools on the Mac Studio, especially when the user says apps are behind, asks whether the update job catches everything, or wants GUI apps/direct installs/Homebrew casks/App Store/npm/git update coverage verified. Use this before claiming the machine is fully updated because normal `brew outdated` misses greedy casks and direct-installed apps.
targets: [hermes-default, hermes-gpt, claude-hermes]
---

# Non-Hermes Update Audit

Use this when Kosta asks to update local tools/apps outside the Hermes repo, or asks whether the update cron/report catches all outdated software.

## Core idea

Do not trust a single updater. On this machine, important apps can be Homebrew casks, greedy casks, direct `.app` bundles, App Store apps, npm globals, or git checkouts. A clean `brew outdated` result is not enough.

## Workflow

1. Inspect the existing audit job/report first.
   - Check `~/.hermes/profiles/gpt/scripts/non_hermes_update_audit.py`.
   - Check the latest report under `~/.hermes/profiles/gpt/cron/non-hermes-updates/latest.json` if present.
   - If the report omits a class of updates the user cares about, patch the audit script rather than only doing a one-off manual update.

2. Use broad update discovery.
   - Homebrew: use `brew outdated --cask --greedy --json=v2`, not plain `brew outdated`, when checking GUI casks. Greedy casks can catch apps like Discord/Maestro that normal checks miss.
   - Direct apps: scan `.app` bundles in `/Applications`, `/Applications/AI`, `/Applications/Coding`, and `~/Applications` and compare against known release sources when possible.
   - App Store: use `mas outdated` if `mas` is installed.
   - Include npm globals and git checkout status if the audit script already tracks them.
   - Keep routine media/tooling formulae such as `ffmpeg` in the auto-safe formula allowlist once verified, so minor patch bumps do not churn as report-only classification work.

3. Update safely by install class.
   - For normal Homebrew casks, prefer `brew upgrade --cask ...`; if an appdir mismatch or stale state blocks it, use a targeted `brew reinstall --cask --force ... --appdir=<actual app dir>` rather than broad cleanup.
   - For direct apps from GitHub/Electron releases, fetch release metadata, download the official artifact, verify the published checksum when available, mount/copy/install, and keep a temporary backup until verification passes.
   - If Homebrew’s cask checksum is stale or wrong but the official release metadata verifies, install from the official upstream artifact directly instead of bypassing checksum verification blindly.

4. Verify each updated app before reporting success.
   - Read the installed app version from `Info.plist` or the tool’s CLI.
   - For macOS apps, run `codesign --verify --deep --strict <App.app>` when practical.
   - Rerun the audit script and confirm the relevant outdated counts are zero or explicitly list what remains manual-gated.

5. Keep Hermes repo updates separate.
   - If the user also asked for a Hermes smart update, use the Hermes local update/merge workflow for `~/.hermes/hermes-agent`; do not mix app updater logic with Hermes git merge logic.

## Common pitfalls

- Plain `brew outdated` can miss greedy casks; use `--greedy --json=v2` for cask audit coverage.
- Some apps are installed outside `/Applications`; include `/Applications/AI`, `/Applications/Coding`, and `~/Applications`.
- Do not bypass a bad cask checksum just to get unstuck. Prefer official release metadata checksum verification and direct app install.
- Do not call the update job comprehensive until the script itself captures the classes you manually checked.
- Duplicate app bundle IDs across scan roots are a real problem: Factory, CraftCodex, InjectionIII, and Codex Beta all had copies in multiple `/Applications` subdirectories with different versions. The audit script now reports `duplicate_bundle_ids`. When you see duplicates, recommend keeping the newer copy and removing the older one, but do not delete app bundles without explicit confirmation.
- Hermes WebUI update failures can be false negatives after a successful fast-forward: if `ai.hermes.webui` is present as `~/Library/LaunchAgents/ai.hermes.webui.plist` but unloaded, `launchctl kickstart user/$(id -u)/ai.hermes.webui` returns “Could not find service.” Bootstrap the plist into `user/$(id -u)` first, then kickstart, and poll `/health` for a few seconds before declaring failure.
- DMG automation can fail if you parse `hdiutil attach -plist` as a non-seekable stream; fall back to `hdiutil info` or plain `hdiutil attach` output parsing when needed.

## Good handoff

Report app names and installed versions, what audit coverage changed, the fresh audit result, and any unrelated smoke-test failures separately from update status.
