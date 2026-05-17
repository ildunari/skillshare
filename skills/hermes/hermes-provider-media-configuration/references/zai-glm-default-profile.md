# Z.AI GLM as Hermes default-profile main model

Use this when Kosta asks to switch the non-GPT/default Hermes profile to GLM or asks whether GLM needs reasoning effort enabled.

## Target the correct profile

Discord/Telegram gateway sessions often run with `HERMES_HOME=/Users/Kosta/.hermes/profiles/gpt`, so plain `hermes config ...` may edit the GPT profile even when Kosta says "the non-GPT/default profile". Explicitly target the default global profile:

```bash
HERMES_HOME=/Users/Kosta/.hermes hermes config path
HERMES_HOME=/Users/Kosta/.hermes hermes config set model.default glm-5.1
HERMES_HOME=/Users/Kosta/.hermes hermes config set model.provider zai
HERMES_HOME=/Users/Kosta/.hermes hermes config set model.base_url https://api.z.ai/api/coding/paas/v4
HERMES_HOME=/Users/Kosta/.hermes hermes status
```

A known-good status check shows `Model: glm-5.1`, `Provider: Z.AI / GLM`, and `Z.AI/GLM` API key configured.

## Verification

A minimal smoke test that avoids profile/rules ambiguity:

```bash
HERMES_HOME=/Users/Kosta/.hermes hermes --ignore-rules -z 'Reply with exactly: ok'
```

Expected output: `ok`.

## Reasoning / thinking behavior

Z.AI GLM-5.1 does not use the same primary knob as OpenAI/OpenRouter-style `reasoning_effort`. Z.AI docs describe deep thinking as:

```json
"thinking": { "type": "enabled" }
```

Their GLM-5.1 docs say deep thinking is supported and enabled by default; `thinking.type` can be set to `enabled` for compulsory thinking or `disabled` for quick direct answers. Responses may include `reasoning_content`.

In Hermes, `agent.reasoning_effort` may still be present in config (often `medium`), but direct `zai`/`api.z.ai` routes are not OpenRouter reasoning routes and Hermes currently gates OpenAI-style `extra_body.reasoning` away for non-supported direct providers. Do not assume `agent.reasoning_effort` forces GLM thinking.

Default recommendation: leave GLM-5.1 on its default thinking behavior unless Kosta reports shallow answers or missing reasoning. If forcing is needed, implement/send the Z.AI-specific `thinking: {type: "enabled"}` payload rather than changing only `agent.reasoning_effort`.

## GLM-5V-Turbo visual backup

When Kosta asks to add GLM-5V-Turbo as a visual/coding backup, use the Coding Plan endpoint, not the general endpoint:

```bash
HERMES_HOME=/Users/Kosta/.hermes hermes config set fallback_model.provider zai
HERMES_HOME=/Users/Kosta/.hermes hermes config set fallback_model.model glm-5v-turbo
HERMES_HOME=/Users/Kosta/.hermes hermes config set fallback_model.base_url https://api.z.ai/api/coding/paas/v4
```

Verify with `hermes config check`, inspect `fallback_model` in `/Users/Kosta/.hermes/config.yaml`, and smoke-test the model directly against `https://api.z.ai/api/coding/paas/v4/chat/completions` with `model: "glm-5v-turbo"` if Hermes does not expose a direct fallback smoke command.

## Common pitfall

If you set `model.default=glm-5.1` but leave `provider=openai-codex`, Hermes will call the ChatGPT Codex backend with a GLM model and fail with a 400 like: `The 'glm-5.1' model is not supported when using Codex with a ChatGPT account.` Always change provider and base_url together.
