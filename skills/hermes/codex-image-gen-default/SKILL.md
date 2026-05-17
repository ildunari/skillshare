---
name: hermes-codex-image-gen-default
description: Configure, diagnose, and use Hermes Codex/OpenAI GPT Image 2 image generation. Use when Kosta asks about Codex image gen, GPT Image 2, image_gen.provider, default image generation, making Hermes image generation use Codex auth, or improving GPT Image 2 rendering/prompt quality. For actual image creation, route to the /image skill and the bundled GPT Image Craft references.
version: 0.1.0
author: Hermes Agent
license: MIT
targets: [hermes-default, hermes-gpt, claude-hermes]
---

# Hermes Codex image generation default

Use this when setting up or checking Hermes image generation through the bundled `openai-codex` image_gen plugin.

## What this enables

Hermes can route the normal `image_generate` tool to OpenAI **GPT Image 2** through Codex/ChatGPT OAuth. This avoids configuring a separate `OPENAI_API_KEY` when Codex auth is already present.

The relevant bundled plugin is:

```text
~/.hermes/hermes-agent/plugins/image_gen/openai-codex/
```

It registers provider `openai-codex`, calls the Responses `image_generation` tool with `gpt-image-2`, and saves generated PNGs under `$HERMES_HOME/cache/images/`.

## Configure GPT profile default

Edit the active profile config, usually:

```text
~/.hermes/profiles/gpt/config.yaml
```

Set:

```yaml
image_gen:
  provider: openai-codex
  model: gpt-image-2-medium
  openai-codex:
    model: gpt-image-2-medium
```

Available tiers in the current bundled plugin are:

```text
gpt-image-2-low
gpt-image-2-medium
gpt-image-2-high
```

Use `medium` as the default unless Kosta asks for fastest/cheapest iteration or highest fidelity.


## Rendering and prompt-craft lane

If the user asks how to render, make, edit, improve, or debug an image, do not stop at provider configuration. Use the default Hermes `/image` skill (`media-creative__image`) and the bundled GPT Image Craft pack attached here under `references/gpt-image-craft/`. The same pack is also installed as the cross-agent `gpt-image-craft` skill for non-Hermes tools.

For serious image work, choose the relevant reference instead of inventing prompt advice from memory:

- `references/gpt-image-craft/model-and-workflow.md` — GPT Image 2 API/UI choices, size, quality, formats, streaming, limitations.
- `references/gpt-image-craft/prompt-framework.md` — prompt architecture, iteration tactics, text-in-image guidance.
- `references/gpt-image-craft/prompt-recipes.md` — ready-to-adapt templates.
- `references/gpt-image-craft/troubleshooting.md` — fixes for common failure modes.
- `references/gpt-image-craft/styles/` — scientific figures, data graphics, photorealism, UI/marketing, sprites, illustration, print/type, product/editing, and niche aesthetics.

Use `scripts/image_prompt_audit.py` for complex, text-heavy, API-oriented, or constraint-heavy prompts before spending image quota. It is a static checker; it does not call the API.

For reference-conditioned chart/graph cleanup, use `references/codex-chart-redraw.md`. The important lesson is to label this as a model redraw, not factual restoration; use input images with `detail: original`, stream the Codex Responses image_generation call, preserve latest partial output, and verify labels/data geometry visually before delivery.

## Verify without burning an image call

From the Hermes repo:

```bash
cd ~/.hermes/hermes-agent
source .venv/bin/activate
python - <<'PY'
from hermes_cli.config import load_config
from hermes_cli.plugins import _ensure_plugins_discovered
from agent.image_gen_registry import get_provider

cfg = load_config()
print('image_gen config:', cfg.get('image_gen'))
_ensure_plugins_discovered(force=True)
p = get_provider('openai-codex')
print('provider registered:', bool(p))
print('available:', p.is_available() if p else None)
print('default:', p.default_model() if p else None)
PY
```

Expected: provider registered `True`, available `True`, default `gpt-image-2-medium`.

If `available` is false, check Codex auth first:

```bash
hermes --profile gpt auth status
```

or inspect token availability without printing secrets:

```bash
python - <<'PY'
from agent.auxiliary_client import _read_codex_access_token
print(bool(_read_codex_access_token()))
PY
```

Never print or paste OAuth tokens.

## Important behavior

Plugin discovery may show zero providers if you query `agent.image_gen_registry.list_providers()` before forcing plugin discovery. Call `_ensure_plugins_discovered(force=True)` before checking `get_provider('openai-codex')`.

`hermes tools list` only confirms that the `image_gen` toolset is enabled; it does not prove which backend provider `image_generate` will use. The backend is controlled by `image_gen.provider` in the active profile config.

## Safety and cost

A real `image_generate(...)` call may spend image-generation quota/credits. For config validation, prefer the no-generation provider check above. Only run an actual test image when Kosta asks for a generation or explicitly wants an end-to-end smoke test.
