# GPT profile vision routed through Codex

Session note:
- The GPT profile's vision path is controlled by `auxiliary.vision`, not `image_gen`.
- Working config on this machine:
  - `auxiliary.vision.provider: openai-codex` (or `codex`; the alias normalizes to `openai-codex`)
  - `auxiliary.vision.model: gpt-5.5`
  - `auxiliary.vision.base_url: ''`
- Do **not** set `auxiliary.vision.base_url: https://chatgpt.com/backend-api/codex`. In `resolve_vision_provider_client()`, any explicit `base_url` takes the direct-endpoint branch and can turn the request into a generic `custom` OpenAI client instead of the native `CodexAuxiliaryClient`, causing HTML/error-page failures from `vision_analyze`.
- `image_gen.provider: openai-codex` was already correct and should be left alone when only vision routing is being fixed.

Verification:
- `hermes --profile gpt config path`
- `HERMES_HOME=~/.hermes/profiles/gpt python - <<'PY' ... load_config(); resolve_vision_provider_client(...) ... PY`
- Good resolution for this profile is `openai-codex / gpt-5.5 / CodexAuxiliaryClient`; if it resolves as `custom / OpenAI`, clear `auxiliary.vision.base_url` and retry.
- Smoke test with a local cached image via `vision_analyze_tool(...)`, not only config inspection.

Pitfall:
- Don't assume a user asking for 'vision' means image generation. In Hermes, vision analysis and image generation are separate settings and can have different providers.