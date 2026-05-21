# Default profile vision fallback

Use this when the default Hermes profile runs a text-only main model but still needs image understanding.

## Trigger

The default profile may use DeepSeek v4 (`model.provider: deepseek`, `model.default: deepseek-v4-pro`). DeepSeek's text chat model is not a vision model, so leaving `auxiliary.vision.provider: auto` can route image work poorly or fail depending on provider/model capability lookup.

## Known-good Mac Studio configuration

Set the default profile vision auxiliary explicitly:

```bash
cp ~/.hermes/config.yaml ~/.hermes/backups/config-default-before-vision-$(date +%Y%m%d-%H%M%S).yaml
hermes --profile default config set auxiliary.vision.provider zai
hermes --profile default config set auxiliary.vision.model glm-5v-turbo
hermes --profile default config set auxiliary.vision.base_url https://api.z.ai/api/coding/paas/v4
```

Expected YAML under `~/.hermes/config.yaml`:

```yaml
auxiliary:
  vision:
    provider: zai
    model: glm-5v-turbo
    base_url: https://api.z.ai/api/coding/paas/v4
```

## Verification

Run from the Hermes checkout:

```bash
cd ~/.hermes/hermes-agent
HERMES_HOME="$HOME/.hermes" .venv/bin/python - <<'PY'
from agent.auxiliary_client import resolve_vision_provider_client
provider, client, model = resolve_vision_provider_client()
print({'provider': provider, 'model': model, 'client': client is not None})
PY
```

A usable result observed on Mac Studio was:

```text
{'provider': 'custom', 'model': 'glm-5v-turbo', 'client': True}
```

`provider: custom` here is acceptable because the resolver treats an explicit `base_url` override as a custom OpenAI-compatible endpoint while preserving the configured model.

## Pitfalls

- Do not infer that `fallback_model` covers vision. Vision uses `auxiliary.vision` resolution.
- Do not configure this under the GPT profile if the user asked about regular/default Hermes. Use `hermes --profile default config ...` or edit `~/.hermes/config.yaml`.
- Do not promise successful image analysis from resolver-only verification; for a shipped fix, run a real image prompt or image-routing test when available.
