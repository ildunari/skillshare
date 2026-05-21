# Codex account routing by Hermes profile (2026-05-15)

Use this when Kosta asks for Codex/OpenAI account selection to differ by Hermes profile, especially when `/codex` or `codex_app_server` should not inherit the same ChatGPT account everywhere.

## Durable pattern

Codex has two separate auth surfaces in this setup:

- Hermes OpenAI/Codex provider auth: `~/.hermes/auth.json` and per-profile `~/.hermes/profiles/<profile>/auth.json`.
- Codex CLI/app-server auth: `auth.json` under the `CODEX_HOME` used by the spawned `codex app-server` process.

For profile-specific account routing, update both surfaces. If Hermes direct OpenAI/Codex requests use one account but app-server still uses `~/.codex`, `/codex` will silently run under the wrong account.

## Known-good Mac Studio split

- GPT profile: keep Kosta's personal/pro account in `~/.hermes/profiles/gpt/auth.json` and Codex home `~/.codex`.
- Default/root and other profiles: use the alternate account in `~/.hermes/auth.json` or their per-profile auth store, and point Codex app-server at a separate home such as `~/.codex-photongaming`.

The separate Codex home can be lightweight: copy `config.toml`, model/catalog files, hooks, and `AGENTS.md`; symlink heavy shared non-secret directories such as `plugins/`, `skills/`, `agents/`, and `cache/`; write a separate `auth.json` with the desired account tokens.

## Hermes implementation pitfall

The Codex app-server adapter accepts `codex_home`, `codex_profile`, `codex_bin`, and config overrides, but profile config only matters if `run_agent.py` passes `model.codex_app_server.*` into `CodexAppServerSession`. If account routing appears ignored, inspect the session construction path before assuming Codex cannot do it.

Suggested config shape:

```yaml
model:
  codex_app_server:
    codex_home: /Users/Kosta/.codex-photongaming
```

Use `/Users/Kosta/.codex` in the GPT profile when GPT should use kosta963, and the alternate Codex home in default/root or non-GPT profiles.

## Verification

- Parse each edited `config.yaml` and confirm `model.codex_app_server.codex_home` resolves as intended.
- Check safe auth metadata only: `account_id`/label/email, never print tokens.
- Smoke both app-server homes with `CodexAppServerClient(codex_home=...).initialize()` and verify returned `codexHome`.
- Compile or run the narrow Hermes test for app-server session changes after touching `run_agent.py`.
- Restart/reload long-running gateway processes before expecting Telegram/Discord sessions to inherit code/config changes.
