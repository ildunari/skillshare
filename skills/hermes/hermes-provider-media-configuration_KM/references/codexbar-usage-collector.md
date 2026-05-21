# Archived skill: codexbar-usage-collector

Original path: `/Users/Kosta/.hermes/profiles/gpt/skills/hermes/codexbar-usage-collector`
Absorbed into umbrella: `hermes-provider-media-configuration` on 2026-04-29.

---

---
name: codexbar-usage-collector
description: Use when the user asks about adding a Telegram/Hermes usage tab, subscription quota dashboard, Codex/Claude/Copilot usage monitoring, or whether CodexMonitor/CodexBar is installed. Prefer checking and integrating the local CodexBarCLI collector before building custom provider scrapers or reaching for unrelated CodexMonitor repos.
targets: [hermes-default, hermes-gpt]
---

# CodexBar Usage Collector

Use this skill when designing or debugging a Hermes/Telegram usage page for AI subscription limits, or when Kosta asks whether Codex Monitor is already installed.

## Key local finding on Mac Studio

Kosta has **CodexBar** installed via Homebrew cask, not necessarily the Dimillian `CodexMonitor` repo.

Known installed app path:

```bash
/Applications/Coding/CodexBar.app
```

Useful CLI path:

```bash
/Applications/Coding/CodexBar.app/Contents/Helpers/CodexBarCLI
```

Homebrew may report the cask as `codexbar`; the helper symlink may not always be at `/Applications/CodexBar.app/...` because this machine stores the app under `/Applications/Coding/`.

## Discovery commands

Check the live machine before answering from memory:

```bash
brew info codexbar
search_files path=/Applications pattern='*CodexBar*' target=files
ps aux | grep -i '[c]odexbar' || true
/Applications/Coding/CodexBar.app/Contents/Helpers/CodexBarCLI --help
```

Avoid slow Spotlight-only discovery as the first step; `mdfind` can hang or time out.

## Usage collection command

CodexBarCLI can emit normalized JSON across providers:

```bash
/Applications/Coding/CodexBar.app/Contents/Helpers/CodexBarCLI usage \
  --provider all \
  --format json \
  --pretty \
  --no-color
```

For one provider:

```bash
/Applications/Coding/CodexBar.app/Contents/Helpers/CodexBarCLI usage \
  --provider codex \
  --format json \
  --pretty \
  --no-color
```

Supported providers shown by `--help` include Codex, Claude, Cursor, OpenCode, Factory, Gemini, Copilot, OpenRouter, Perplexity, and others. Provider support depends on local app/browser/session credentials.

## Interpretation pattern

Treat CodexBarCLI as the backend collector for a Hermes Telegram Mini App usage tab:

1. Run CodexBarCLI and parse the JSON.
2. Keep successful provider snapshots and surface provider errors separately.
3. Expose a Hermes API route such as `/api/subscription-usage` or `/api/usage/subscriptions`.
4. Render a web dashboard or Telegram Mini App route such as `/usage`.
5. Open it from Telegram via the bot menu web app or an inline `Usage` button.

Do not make Telegram do quota calculations. Telegram should be the front door; Hermes/API server should normalize and serve usage data.

### Mini app implementation lessons

Hermes profile gateways can serve a profile-specific mini app, not the root one. For GPT profile, check and patch:

```bash
~/.hermes/profiles/gpt/miniapp/index.html
```

Do not assume `~/.hermes/miniapp/index.html` is the live file for every profile. In code, `api_server.py` resolves miniapp from `get_hermes_home() / 'miniapp'`, so the active path depends on the running profile.

For the Usage tab, prefer one backend call:

```js
api('/api/subscription-usage?provider=all')
```

Avoid firing separate requests for a hardcoded list like `codex`, `claude`, and `copilot`. That is slower, can leave Telegram stuck on “Fetching provider usage from CodexBar...”, and misses active subscriptions like Gemini. After fetching `provider=all`, render all providers with `usage` first, then show actionable errors such as expired tokens or missing sessions. Hide non-actionable CodexBar inventory noise such as “No available fetch strategy”, “not detected”, and “Install a JetBrains IDE” unless the user explicitly wants a full provider diagnostics dump.

## Auth and error caveats

CodexBar may be installed and the CLI may work while individual providers fail because their auth expired or the app/browser session is missing.

Example observed failure for Codex:

```text
Provided authentication token is expired. Please try signing in again.
```

In that case, the right conclusion is not “CodexBar is missing”; it is “CodexBar is installed, but the Codex/ChatGPT session needs re-auth.”

Example successful providers observed in one check: Claude and Copilot returned usage snapshots, while Codex returned an expired-token error.

## Recommendation default

When building the Hermes/Telegram usage page, start with CodexBarCLI rather than vendoring Dimillian CodexMonitor or writing custom scrapers. CodexBar already normalizes multiple subscription sources, which is exactly what the usage tab needs.
