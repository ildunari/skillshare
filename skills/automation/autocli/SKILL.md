---
name: autocli
description: >-
  Use when the user wants data fetched from a website, a site turned into a
  CLI, existing browser login state reused through Chrome, or a supported local
  CLI/desktop app accessed through AutoCLI. Prefer this before heavier browser
  automation when AutoCLI likely covers the target. Read this skill before using
  `autocli`.
targets: [hermes-default, hermes-gpt, claude-hermes]
---

# AutoCLI

Use this when a site or supported app already has an AutoCLI adapter, or when the user wants “turn this website into a command” behavior without a whole browser-driving session.

## What it does

AutoCLI is a fast Rust CLI that turns websites and some local tools/apps into command-line interfaces. It can:
- fetch structured data from supported sites
- reuse Chrome login state through its extension for browser-backed commands
- search for existing community adapters
- generate adapters for new sites via `autocli.ai`
- wrap a few local CLIs like `gh`, `docker`, `kubectl`, and Google Workspace helpers

Think of it as: “try a purpose-built website/app CLI first, then fall back to browser automation if needed.”

## Environment notes

- Expect the `autocli` binary to be available on `PATH`.
- Keep auth tokens in the machine's normal secure secret store or local AutoCLI auth flow.
- If a team already has a standard token-retrieval workflow, use that instead of inventing a new one.

Do not paste tokens into files, skills, or committed config.

## First checks

1. Confirm the binary exists:
   - `autocli --version`
2. If AI generation/search features need auth, run:
   - `autocli auth`
3. If browser-backed commands matter, make sure Chrome is open and the AutoCLI extension is installed.

## Default workflow

1. Check whether the target already has a command:
   - `autocli --help`
   - or `autocli search <url>`
2. If a matching adapter exists, use it directly.
3. If not, and the user wants extraction from a new site, try:
   - `autocli generate <url> --goal '<plain-English goal>' --ai`
4. If the task needs full arbitrary page interaction, rich login flows, or UI testing, switch to browser automation instead of forcing AutoCLI.

## Good fits

- “Get structured data from this website.”
- “Can you pull this page into JSON/CSV/markdown?”
- “Is there already an adapter for this site?”
- “Turn this site into a reusable CLI command.”
- “Use the site I’m already logged into in Chrome.”

## Poor fits

- Multi-step UI testing
- Complex forms or flows with lots of clicks
- Sites with no useful adapter path where browser automation is clearly simpler
- Tasks where raw browser screenshots/DOM interaction matter more than structured output

## Quick commands

```bash
autocli --version
autocli search https://example.com
autocli generate https://example.com --goal 'list the latest posts' --ai
autocli hackernews top --format json
autocli gh repo view cli/cli --format json
```

## Notes

- Public commands can work without browser auth.
- AI generation/auth features use `autocli.ai` and store local config in `~/.autocli/config.json`.
- If auth is needed again, prefer the machine's existing secure secret workflow instead of asking the user to retype a token that is already managed locally.
