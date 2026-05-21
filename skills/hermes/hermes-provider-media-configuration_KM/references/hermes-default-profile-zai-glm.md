# Switching the non-GPT default Hermes profile to Z.AI GLM

Session lesson: when the current runtime is the GPT profile, `hermes config path` may resolve to `~/.hermes/profiles/gpt/config.yaml` because `HERMES_HOME` is set to the GPT profile. If Kosta asks for the "non-GPT" or "default" Hermes profile, scope commands explicitly to the root Hermes home.

Known-good flow on Mac Studio:

```bash
HERMES_HOME=/Users/Kosta/.hermes hermes config path
HERMES_HOME=/Users/Kosta/.hermes hermes config set model.default glm-5.1
HERMES_HOME=/Users/Kosta/.hermes hermes config set model.provider zai
HERMES_HOME=/Users/Kosta/.hermes hermes config set model.base_url https://api.z.ai/api/coding/paas/v4
HERMES_HOME=/Users/Kosta/.hermes hermes status
HERMES_HOME=/Users/Kosta/.hermes hermes --ignore-rules -z 'Reply with exactly: ok'
```

Expected verification:

- Config path prints `/Users/Kosta/.hermes/config.yaml`, not `/Users/Kosta/.hermes/profiles/gpt/config.yaml`.
- `hermes status` shows `Model: glm-5.1` and `Provider: Z.AI / GLM`.
- Z.AI/GLM API key is configured, usually sourced from `GLM_API_KEY` / auth pool.
- A one-shot returns `ok`.

Pitfall: setting only `model.default=glm-5.1` while leaving `provider=openai-codex` causes Codex/ChatGPT backend errors because GLM is not supported by the Codex provider. Always set model, provider, and base URL together.
