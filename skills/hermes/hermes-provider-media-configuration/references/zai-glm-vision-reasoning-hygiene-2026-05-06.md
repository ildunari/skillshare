# Z.ai GLM vision reasoning hygiene — 2026-05-06

Use this when Hermes routes image/video analysis through Z.ai GLM vision models such as `glm-5v-turbo` and reasoning/thinking text appears in tool output or could leak into the main agent context.

## What happened

BrowserAgent was configured to use:

```yaml
auxiliary:
  vision:
    provider: zai
    model: glm-5v-turbo
    base_url: https://api.z.ai/api/coding/paas/v4
```

A live resolver check confirmed the vision client/model were correct, but Z.ai vision responses could include reasoning tokens / `reasoning_content`. The old `vision_analyze_tool` used `extract_content_or_reasoning(response)`, which meant a reasoning-only response could be treated as the visible image analysis and then injected into tool output, final answers, or the main agent context.

## Correct pattern

Prefer both controls:

1. Ask Z.ai not to think for vision auxiliary calls:

```yaml
auxiliary:
  vision:
    extra_body:
      thinking:
        type: disabled
```

Z.ai docs say GLM thinking can be disabled with `"thinking": {"type": "disabled"}`. This is a provider request, not a sufficient safety boundary.

2. In Hermes vision/video tool code, extract only visible assistant content:

```python
analysis = ((response.choices[0].message.content or "").strip())
```

Do not fall back to `reasoning`, `reasoning_content`, or `reasoning_details` for vision/video tools. If visible content is empty, retry once; if still empty, return the normal fallback message rather than leaking hidden reasoning.

## Verification

- Compile touched files: `python3 -m py_compile tools/vision_tools.py agent/auxiliary_client.py` from `~/.hermes/hermes-agent`.
- Verify profile config loads under the target profile and includes `{'thinking': {'type': 'disabled'}}` for `auxiliary.vision.extra_body`.
- Use a mocked response where `message.content == ''` and `message.reasoning_content == 'SECRET...'`; `vision_analyze_tool` should retry once and must not include the secret reasoning in `analysis`.
- If a live call returns 401, diagnose credentials/env loading separately. A 401 does not prove wrong vision routing.

## Pitfalls

- `display.show_reasoning: false` only affects display of the main gateway stream. It does not protect tool outputs if the tool itself copies `reasoning_content` into JSON.
- `thinking: disabled` can be ignored or fail provider-side. Treat output filtering as the real guardrail.
- `.env` files may not be shell-sourceable if they contain unquoted multiline menu values; Hermes may parse them fine while `source .env` fails. Use Hermes config/env loaders or controlled Python checks instead of raw shell sourcing when possible.
