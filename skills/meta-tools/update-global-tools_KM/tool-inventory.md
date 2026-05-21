# Tool Inventory

> Auto-maintained by the update-global-tools skill. Last full scan: 2026-05-07.

## Homebrew Formulae (Key Tools)

### asc
- **Version**: 0.47.0
- **Repo**: steipete/asc
- **Update**: `brew upgrade asc`
- **Last Update Notes**: Minor bump from 0.46.2

### bird (@steipete/bird)
- **Version**: 0.8.0
- **Repo**: steipete/bird
- **Update**: `npm update -g @steipete/bird`
- **Last Update Notes**: ⚠️ npm deprecation warning as of 2026-05-03: "Package no longer supported." Monitor for replacement.

### bun
- **Version**: 1.3.11
- **Repo**: oven-sh/bun
- **Update**: `brew upgrade bun`
- **Last Update Notes**: Patch from 1.3.10

### cloudflared
- **Version**: 2026.3.0
- **Repo**: cloudflare/cloudflared
- **Update**: `brew upgrade cloudflared`
- **Last Update Notes**: Monthly release bump

### deno
- **Version**: 2.7.9
- **Repo**: denoland/deno
- **Update**: `brew upgrade deno`
- **Last Update Notes**: Patch from 2.7.8

### fd
- **Version**: 10.4.2
- **Repo**: sharkdp/fd
- **Update**: `brew upgrade fd`
- **Last Update Notes**: Minor bump from 10.3.0

### fzf
- **Version**: 0.70.0
- **Repo**: junegunn/fzf
- **Update**: `brew upgrade fzf`
- **Last Update Notes**: Bumped from 0.68.0

### gh (GitHub CLI)
- **Version**: 2.89.0
- **Repo**: cli/cli
- **Update**: `brew upgrade gh`
- **Last Update Notes**: Minor bump from 2.88.1

### gogcli (gog)
- **Version**: 0.15.0
- **Repo**: steipete/gogcli
- **Update**: `brew upgrade gogcli`
- **Last Update Notes**: 0.14.0 → 0.15.0. Raw export subcommand on all services (docs/sheets/drive/gmail/calendar etc). Drive storage auditing (`tree`, `du`, `inventory`). Contact deduplication preview (JSON plan, no writes). Agent-safe Gmail reads (`--safe`/`--sanitize-content`). Google Docs font/color/tab management. Sheets table + conditional-format. Docker images + bundled `gog` skill.

### llvm
- **Version**: 22.1.1
- **Repo**: llvm/llvm-project
- **Update**: `brew upgrade llvm`
- **Last Update Notes**: Major version bump from 21.x

### maestro
- **Version**: 2.3.0 (CLI), cask 0.15.2 (app)
- **Repo**: mobile-dev-inc/maestro
- **Update**: `brew upgrade maestro` (formula); `brew upgrade --cask maestro` (app)
- **Last Update Notes**: Cask bumped 0.14.5 → 0.15.2; CLI unchanged at 2.3.0

### ffmpeg
- **Version**: 8.1.1
- **Repo**: FFmpeg/FFmpeg
- **Update**: `brew upgrade ffmpeg`
- **Last Update Notes**: Patch from 8.1_1

### mas
- **Version**: 7.0.0
- **Repo**: mas-cli/mas
- **Update**: `brew upgrade mas`
- **Last Update Notes**: Major bump from 6.0.1. JSON output (`--json` flag) added to `config`, `list`, `lookup`/`info`, `outdated`, `search` commands — now pipe-friendly with jq. Improved tabular display. Bug fix: unrecognized IDs in `uninstall` no longer repeat error. No breaking changes vs 6.x — safe to upgrade from 6.0.1.

### node
- **Version**: 25.8.2
- **Repo**: nodejs/node
- **Update**: `brew upgrade node`
- **Last Update Notes**: Patch from 25.8.1

### ollama
- **Version**: 0.18.2 (standalone app, not brew-managed)
- **Repo**: ollama/ollama
- **Update**: App auto-updates; not installed via brew formula/cask
- **Last Update Notes**: Bumped from 0.18.1; confirmed not in brew

### repomix
- **Version**: 1.13.1
- **Repo**: yamadashy/repomix
- **Update**: `brew upgrade repomix`
- **Last Update Notes**: Patch from 1.13.0

### ruby
- **Version**: 4.0.2
- **Repo**: ruby/ruby
- **Update**: `brew upgrade ruby`
- **Last Update Notes**: Patch from 4.0.1

### rust / rustup
- **Version**: rust 1.94.0, rustup 1.29.0
- **Repo**: rust-lang/rust
- **Update**: `brew upgrade rust rustup`
- **Last Update Notes**: rust 1.93.1 -> 1.94.0, rustup 1.28.2 -> 1.29.0

### sqlite
- **Version**: 3.51.3
- **Repo**: sqlite/sqlite
- **Update**: `brew upgrade sqlite`
- **Last Update Notes**: Patch from 3.51.2

### swiftformat
- **Version**: 0.60.1
- **Repo**: nicklockwood/SwiftFormat
- **Update**: `brew upgrade swiftformat`
- **Last Update Notes**: Patch from 0.60.0

### tailscale
- **Version**: 1.96.4
- **Repo**: tailscale/tailscale
- **Update**: `brew upgrade tailscale`
- **Last Update Notes**: Patch from 1.96.3

### uv
- **Version**: 0.11.11
- **Repo**: astral-sh/uv
- **Update**: `brew upgrade uv`
- **Last Update Notes**: Patch from 0.11.10

### xcodebuildmcp
- **Version**: 2.3.2
- **Repo**: nicklockwood/xcodebuildmcp
- **Update**: `brew upgrade xcodebuildmcp` (also npm global `xcodebuildmcp@2.3.2`)
- **Last Update Notes**: Patch from 2.3.1

### xcodegen
- **Version**: 2.45.3
- **Repo**: yonaskolb/XcodeGen
- **Update**: `brew upgrade xcodegen`
- **Last Update Notes**: Bumped from 2.44.1

### yt-dlp
- **Version**: 2026.3.17
- **Repo**: yt-dlp/yt-dlp
- **Update**: `brew upgrade yt-dlp`
- **Last Update Notes**: Bi-weekly release from 2026.3.13

## Homebrew Casks (Apps)

### 1password-cli
- **Version**: 2.33.1
- **Update**: `brew upgrade --cask 1password-cli`
- **Last Update Notes**: Patch from 2.33.0

### codexbar
- **Version**: 0.24
- **Repo**: steipete/codexbar
- **Update**: `brew reinstall --cask codexbar` (app sometimes not in /Applications)
- **Last Update Notes**: Bumped from 0.23

### discord
- **Version**: 0.0.389
- **Update**: `brew upgrade --cask discord`
- **Last Update Notes**: Patch from 0.0.388

### droid (cask)
- **Version**: 0.120.1
- **Repo**: nicklabs/droid
- **Update**: `brew upgrade --cask droid`
- **Last Update Notes**: Minor bump from 0.119.0

### flutter
- **Version**: 3.41.6
- **Repo**: flutter/flutter
- **Update**: `brew upgrade --cask flutter`
- **Last Update Notes**: Patch from 3.41.5

### tuist
- **Version**: 4.191.8
- **Repo**: tuist/tuist
- **Update**: `brew upgrade --cask tuist`
- **Last Update Notes**: Patch from 4.191.7

## npm Global Packages

### @microsoft/inshellisense
- **Version**: 0.0.1
- **Repo**: microsoft/inshellisense
- **Update**: `npm update -g @microsoft/inshellisense`
- **Last Update Notes**: Added to inventory 2026-03-27. IDE-style terminal autocomplete.

### @factory/cli
- **Version**: 0.120.1
- **Update**: `npm update -g @factory/cli`
- **Last Update Notes**: Minor bump from 0.119.0

### @google/gemini-cli
- **Version**: 0.41.2
- **Repo**: google/gemini-cli
- **Update**: `npm update -g @google/gemini-cli`
- **Last Update Notes**: Patch from 0.41.1

### @openai/codex
- **Version**: 0.128.0
- **Repo**: openai/codex
- **Update**: `npm update -g @openai/codex`
- **Last Update Notes**: 0.117.0 → 0.128.0. Realtime voice v2 (WebRTC, media controls). Plugin marketplace (`codex marketplace add`). Amazon Bedrock built-in provider. MCP resource reads + parallel calls. `Ctrl+R` history search, `/side` conversations, `codex update` self-update. Hooks now stable (configurable in `config.toml`). Persistent `/goal` workflows + MultiAgent v2.

### agent-browser
- **Version**: 0.26.0
- **Repo**: nicklabs/agent-browser
- **Update**: `npm update -g agent-browser`
- **Last Update Notes**: Bumped from 0.23.0

### npm
- **Version**: 11.14.0
- **Update**: `npm update -g npm`
- **Last Update Notes**: Minor bump from 11.13.0

### pnpm
- **Version**: 11.0.8
- **Repo**: pnpm/pnpm
- **Update**: `npm update -g pnpm`
- **Last Update Notes**: MAJOR: 10.33.4 → 11.0.8. Node 22+ required (drops 18–21). Now pure ESM. Config split: non-auth `.npmrc` settings must move to `pnpm-workspace.yaml` (use `pnpm_config_*` env vars, not `npm_config_*`). `allowBuilds` replaces all old build-permission fields (`onlyBuiltDependencies`, etc.). Supply-chain protection on by default (24h hold on new packages, `strictDepBuilds=true`). SQLite-backed store (v11), `undici` HTTP stack. New commands: `pnpm ci`, `pnpm clean`, `pnpm sbom`. Run `pnpm setup` after upgrade.

### remodex
- **Version**: (removed)
- **Update**: Was `npm update -g remodex`
- **Last Update Notes**: No longer installed globally as of 2026-05-04

### supergateway
- **Version**: (removed)
- **Update**: Was `npm update -g supergateway`
- **Last Update Notes**: No longer installed globally as of 2026-03-28

### serve-sim
- **Version**: 0.1.16
- **Update**: `npm update -g serve-sim`
- **Last Update Notes**: Patch from 0.1.14

### uipro-cli
- **Version**: 2.2.3
- **Update**: `npm update -g uipro-cli`
- **Last Update Notes**: Current

### yarn
- **Version**: 1.22.22
- **Update**: `npm update -g yarn`
- **Last Update Notes**: Current

## uv-managed Tools

### zotero-mcp-server
- **Version**: 0.3.0
- **Repo**: zotero-mcp/zotero-mcp-server (PyPI)
- **Update**: `uv tool upgrade zotero-mcp-server`
- **Last Update Notes**: 0.1.3 → 0.3.0 (significant pre-1.0 bump). MCP server for Zotero reference manager (also configured as a Craft Agent source).

### hf (HuggingFace CLI)
- **Version**: 1.8.0
- **Repo**: huggingface/huggingface_hub
- **Update**: `brew upgrade hf`
- **Last Update Notes**: Added to inventory 2026-03-28. CLI for HuggingFace Hub (model/dataset downloads).

### atuin
- **Version**: 18.13.6
- **Repo**: atuinsh/atuin
- **Update**: `brew upgrade atuin`
- **Last Update Notes**: Added to inventory 2026-03-28. Shell history sync/search.

## npm Global Packages (MCP)

### @_davideast/stitch-mcp
- **Version**: 0.5.5
- **Repo**: davideast/stitch-mcp
- **Update**: `npm update -g @_davideast/stitch-mcp`
- **Last Update Notes**: Patch bumps from 0.5.1

## uv-managed Tools (MCP)

### mcp-proxy
- **Version**: 0.11.0
- **Repo**: mcp-proxy (PyPI)
- **Update**: `uv tool upgrade mcp-proxy`
- **Last Update Notes**: Added to inventory 2026-03-28. MCP proxy/bridge server.

### notebooklm-py
- **Version**: 0.3.4
- **Repo**: notebooklm-py (PyPI)
- **Update**: `uv tool upgrade notebooklm-py`
- **Last Update Notes**: Added to inventory 2026-03-28. CLI for Google NotebookLM.

## Standalone Binaries (~/.local/bin)

### pencil-mcp
- **Version**: unversioned (shell script)
- **Location**: ~/.local/bin/pencil-mcp (also ~/.local/bin/pencil wrapper)
- **Update**: Manual — check source for updates
- **Last Update Notes**: Added to inventory 2026-03-27. MCP server for Pencil.app.

### rtk
- **Version**: 0.39.0
- **Repo**: rtk-ai/rtk
- **Update**: `brew upgrade rtk`
- **Last Update Notes**: Minor bump from 0.38.0

### claude (Claude Code)
- **Version**: 2.1.132
- **Location**: ~/.local/share/claude/versions/2.1.132
- **Update**: `claude update` (self-updating)
- **Last Update Notes**: Auto-updated from 2.1.131

### droid (CLI binary)
- **Version**: 0.120.1
- **Location**: ~/.local/bin/droid → /opt/homebrew/bin/droid (Homebrew-managed)
- **Update**: `brew upgrade --cask droid`
- **Last Update Notes**: Minor bump from 0.119.0; matches cask version

### factoryd
- **Version**: 0.25.0
- **Location**: ~/.local/bin/factoryd
- **Update**: Self-updating on launch
- **Last Update Notes**: Auto-updated from previous version

## Other Runtimes (Homebrew-managed)

### python
- **Version**: 3.14.3
- **Update**: `brew upgrade python@3.14`
- **Last Update Notes**: Current

### ruby
- **Version**: 4.0.2
- **Update**: `brew upgrade ruby`
- **Last Update Notes**: Patch

### rust
- **Version**: 1.94.0
- **Update**: `brew upgrade rust`
- **Last Update Notes**: Bumped from 1.93.1

## Developer Utilities (Homebrew)

Tracked but don't need changelog notes — just version bumps.

### bat
- **Version**: 0.26.1
- **Update**: `brew upgrade bat`
- **Last Update Notes**: Added 2026-05-03. `cat` replacement with syntax highlighting.

### btop
- **Version**: 1.4.7
- **Update**: `brew upgrade btop`
- **Last Update Notes**: Added 2026-05-03. System resource monitor (htop alternative).

### eza
- **Version**: 0.23.4
- **Update**: `brew upgrade eza`
- **Last Update Notes**: Added 2026-05-03. Modern `ls` replacement.

### fastlane
- **Version**: 2.233.1
- **Update**: `brew upgrade fastlane`
- **Last Update Notes**: Added 2026-05-03. iOS/Android CI automation.

### git
- **Version**: 2.54.0
- **Update**: `brew upgrade git`
- **Last Update Notes**: Added 2026-05-03. Homebrew-managed git.

### jq
- **Version**: 1.8.1
- **Update**: `brew upgrade jq`
- **Last Update Notes**: Added 2026-05-03. JSON processor.

### ripgrep (rg)
- **Version**: 15.1.0
- **Update**: `brew upgrade ripgrep`
- **Last Update Notes**: Added 2026-05-03. Fast grep replacement.

### skillshare
- **Version**: 0.19.7
- **Update**: `brew upgrade skillshare`
- **Last Update Notes**: Patch from 0.19.5

### swiftlint
- **Version**: 0.63.2
- **Update**: `brew upgrade swiftlint`
- **Last Update Notes**: Added 2026-05-03. Swift linter.

### tmux
- **Version**: 3.6a
- **Update**: `brew upgrade tmux`
- **Last Update Notes**: Added 2026-05-03. Terminal multiplexer.

### zoxide
- **Version**: 0.9.9
- **Update**: `brew upgrade zoxide`
- **Last Update Notes**: Added 2026-05-03. Smart `cd` with frecency tracking.

### pipx
- **Version**: 1.11.2
- **Update**: `brew upgrade pipx`
- **Last Update Notes**: Patch from 1.11.1

## npm Global Packages (New)

### firecrawl-cli
- **Version**: 1.16.2
- **Update**: `npm update -g firecrawl-cli`
- **Last Update Notes**: Patch from 1.16.1

### wrangler
- **Version**: 4.88.0
- **Update**: `npm update -g wrangler`
- **Last Update Notes**: Patch from 4.87.0

## Standalone Binaries (New)

### cursor-agent
- **Version**: 2026.04.08-a41fba1
- **Location**: ~/.local/bin/cursor-agent
- **Update**: Manual — check Cursor release notes
- **Last Update Notes**: Added 2026-05-03. Cursor AI agent binary.

### forge
- **Version**: 2.9.8
- **Location**: ~/.local/bin/forge (31MB binary)
- **Update**: Manual — self-update or reinstall
- **Last Update Notes**: Added 2026-05-03. ForgeMax agent binary.

### hermes
- **Version**: v0.12.0 (rolling — 226 commits pulled 2026-05-07)
- **Location**: ~/.local/bin/hermes
- **Update**: `hermes update`
- **Last Update Notes**: Rolling update (226 commits since last sync). linear skill updated; 2 user-modified skills preserved. grpcio/google-cloud-pubsub deps added. Version tag still v0.12.0.

## uv-managed Tools (New)

### mcp2cli
- **Version**: 3.0.2
- **Update**: `uv tool upgrade mcp2cli`
- **Last Update Notes**: Added 2026-05-03. MCP-to-CLI bridge.

## Developer Utilities (Homebrew, Newly Discovered)

### cmake
- **Version**: 4.3.2
- **Update**: `brew upgrade cmake`
- **Last Update Notes**: Added 2026-05-05. Build system generator.

### cocoapods
- **Version**: 1.16.2
- **Update**: `brew upgrade cocoapods`
- **Last Update Notes**: Added 2026-05-05. iOS/macOS dependency manager (`pod` CLI).

### direnv
- **Version**: 2.37.1
- **Update**: `brew upgrade direnv`
- **Last Update Notes**: Added 2026-05-05. Per-directory shell environment switcher.

### ios-deploy
- **Version**: 1.12.2
- **Update**: `brew upgrade ios-deploy`
- **Last Update Notes**: Added 2026-05-05. Deploy iOS apps to devices without Xcode.

### syncthing
- **Version**: 2.0.16
- **Update**: `brew upgrade syncthing`
- **Last Update Notes**: Added 2026-05-05. Continuous file sync daemon.

### xcbeautify
- **Version**: 3.2.1
- **Update**: `brew upgrade xcbeautify`
- **Last Update Notes**: Added 2026-05-05. Formatter for xcodebuild output.

### yq
- **Version**: 4.53.2
- **Update**: `brew upgrade yq`
- **Last Update Notes**: Added 2026-05-05. YAML/JSON/XML processor (like jq for YAML).

## Standalone Binaries (~/.local/bin, Newly Discovered)

### officecli
- **Version**: 1.0.69
- **Location**: ~/.local/bin/officecli (Mach-O binary)
- **Update**: Manual — part of office-cli Craft Agent source
- **Last Update Notes**: Added 2026-05-05. AI-friendly CLI for .docx/.xlsx/.pptx — backs the office-cli Craft Agent source.

### serena-mcp-router
- **Version**: unversioned (Python scripts)
- **Location**: ~/.local/bin/serena* (cluster of 5 scripts)
- **Update**: Manual — oraios/serena on GitHub
- **Last Update Notes**: Added 2026-05-05. MCP proxy router for Serena coding assistant; manages project-scoped MCP instances.

### go-llm-proxy (VibeProxy)
- **Version**: dev
- **Location**: ~/.local/bin/go-llm-proxy
- **Update**: Manual — rebuild from source
- **Last Update Notes**: Added 2026-05-06. LLM API proxy/router (VibeProxy) — routes Droid/Codex through alternative models (z.ai GLM, etc.) via OpenAI-compatible protocol. Per-request SQLite metrics, multi-user API key config.

### a11yfix
- **Version**: 0.1.0
- **Location**: ~/.local/bin/a11yfix
- **Update**: Manual (Kosta's own tool)
- **Last Update Notes**: Added 2026-05-06. Detects and fixes accessibility issues in .docx and .pptx files using Claude SDK. Has `--report-only` mode and rollup/status subcommands.

### chrome-cdp
- **Version**: unversioned (shell script)
- **Location**: ~/.local/bin/chrome-cdp
- **Update**: Manual
- **Last Update Notes**: Added 2026-05-07. Bash script wrapper for Chrome DevTools Protocol — `start|stop|status` subcommands. Likely part of browser automation infrastructure (autocli source or similar).

## Libraries (Homebrew, auto-updated)

These are dependencies that get pulled in by `brew upgrade`. No manual tracking needed:
ada-url, freetype, giflib, glib, harfbuzz, libiconv, libngtcp2, libunistring, libuv, mosh, protobuf, simdjson, tree, mlx, mlx-c

---

## Removed Tools (DO NOT reinstall — assume user removed them on purpose)

When a tracked tool is no longer found on the system after the recursive `/Applications` + binary scan, it gets moved here instead of being reinstalled. Future runs read this list and skip it during discovery. To bring something back, the user must remove its line here AND reinstall it manually.

<!-- Format: - **tool** — last seen vX.Y.Z, removed YYYY-MM-DD. Reason: not found on system. -->

(none yet)

---

## Blocklist (DO NOT install, track, or re-add)

These tools were explicitly removed by the user. Never reinstall, re-track, or add them back to the inventory.

- **osaurus** — removed 2026-03-23. User does not want this tool.

---

## Quick Update Commands

```bash
# Update everything at once:
brew update && brew upgrade && brew upgrade --cask --greedy
npm update -g
# Ollama (restart after brew upgrade):
brew services restart ollama
# Claude Code:
claude update
```
