# Z.AI hidden/plan-gated model validation

## Symptom

`/model glm-5v-turbo` in a gateway chat switched to `glm-5-turbo` with a warning like:

```text
Auto-corrected `glm-5v-turbo` → `glm-5-turbo`
```

The user may still have access. Z.AI coding-plan `/models` can omit plan-gated or hidden models even when direct chat-completions calls to that model succeed.

## Diagnosis pattern

1. Resolve Z.AI runtime credentials/base URL for the active profile.
2. Check Hermes model validation result for the requested model.
3. Run a direct OpenAI-compatible smoke call against the same Z.AI endpoint:

```python
from hermes_cli.runtime_provider import resolve_runtime_provider
from openai import OpenAI

rt = resolve_runtime_provider(requested="zai", target_model="glm-5v-turbo")
client = OpenAI(api_key=rt["api_key"], base_url=rt["base_url"])
resp = client.chat.completions.create(
    model="glm-5v-turbo",
    messages=[{"role": "user", "content": "Reply with exactly: ok"}],
    max_tokens=10,
    extra_body={"thinking": {"type": "disabled"}},
)
print(resp.choices[0].message.content)
```

If this returns `ok`, access is real and Hermes should not auto-correct the requested exact model ID.

## Durable fix

In `hermes_cli.models.validate_requested_model()`, when a provider `/models` response does not include the requested model, check exact membership in Hermes' curated provider catalog before close-match auto-correction. This preserves known hidden models such as `glm-5v-turbo` while keeping typo correction for actual mistakes like `glm-5-tubbo` → `glm-5-turbo`.

Add tests for both paths:

- curated hidden model is accepted without `corrected_model`
- real typo still auto-corrects
