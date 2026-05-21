# fal.ai image generation provider (2026-05-06)

Session context: Kosta supplied a fal.ai key and asked to integrate fal.ai into Hermes image generation. Hermes already had image-generation registry behavior and OpenAI/OpenAI-Codex providers, but no bundled fal provider plugin.

## Implementation pattern

Add fal.ai as a normal Hermes `image_gen` plugin, not as a shim through the OpenAI Codex provider.

Relevant files in `~/.hermes/hermes-agent`:

- `plugins/image_gen/fal/plugin.yaml` — provider metadata and registration.
- `plugins/image_gen/fal/__init__.py` — `FalImageGenProvider` implementation.
- `tests/plugins/image_gen/test_fal_provider.py` — provider metadata, availability, and plugin registration tests.
- `agent/image_gen_provider.py` — provider interface.
- `agent/image_gen_registry.py` — active provider registry.

The provider should expose:

- provider id: `fal`
- display name: `fal.ai`
- default model: `fal-ai/flux/schnell`
- additional model: `fal-ai/flux/dev`
- auth env: `FAL_KEY`

Use the official `fal-client`. It reads `FAL_KEY` from environment. Verify current fal docs before expanding beyond simple generation because queue APIs and return payload shapes can move.

## Config pattern

Set both default Hermes and GPT profile when Kosta asks for “both”:

```yaml
image_gen:
  provider: fal
  model: fal-ai/flux/schnell
  fal:
    model: fal-ai/flux/schnell
```

Keep any previous `openai-codex` image settings as fallback/reference unless Kosta explicitly asks to remove them.

Store `FAL_KEY` only in local env files with restrictive permissions:

```bash
chmod 600 ~/.hermes/.env ~/.hermes/profiles/gpt/.env
```

Do not echo, summarize, or preserve the raw key in logs/handoffs.

## Verification without spending credits

Use a registry/config smoke test before a paid generation call:

- load Hermes config for the intended profile
- confirm plugin discovery registers `fal`
- confirm `fal.available == True`
- confirm active provider resolves to `fal`
- confirm model catalog includes `fal-ai/flux/schnell` and `fal-ai/flux/dev`

Run targeted tests:

```bash
cd ~/.hermes/hermes-agent
pytest -q tests/plugins/image_gen/test_fal_provider.py \
  tests/agent/test_image_gen_registry.py \
  tests/tools/test_image_generation_plugin_dispatch.py
```

Only run a live `image_generate` smoke test after Kosta agrees, because it spends fal credits.

## Pitfalls

- A fallback entry in the registry is not the same as a bundled provider plugin. Check plugin discovery and active-provider resolution.
- Do not source `.env` blindly if it may contain shell-incompatible lines; parse or load the specific key safely.
- Do not put the raw `FAL_KEY` into transcripts, summaries, commits, or skill references.
- If generation fails after registration, inspect fal return payload shape before assuming the model is unavailable.
