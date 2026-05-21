# Default Grok + Codex mini compression context

Session lesson from 2026-05-17 on the Mac Studio.

## Default/root Grok switch checklist

When Kosta asks to make default Hermes use xAI/Grok, do not stop at `model.default`.

Check and align:

- `~/.hermes/config.yaml`
  - `model.default: grok-4.3`
  - `model.provider: xai-oauth`
  - `model.base_url: https://api.x.ai/v1`
  - `agent.reasoning_effort: medium`
  - `fallback_model` or `fallback_providers` must not still point at Codex/Spark unless Kosta explicitly wants Spark fallback.
- Root auth store: `~/.hermes/auth.json` must contain usable `xai-oauth` provider credentials and a credential-pool entry. A working `~/.hermes/profiles/gpt/auth.json` credential does not automatically cover root/default.
- Gateway sessions may carry `model_override`/`reasoning_override` in `sessions/sessions.json`; inspect if UI/status disagrees with config.

Verification pattern:

```bash
python - <<'PY'
import yaml
p='/Users/Kosta/.hermes/config.yaml'
c=yaml.safe_load(open(p))
print(c['model'])
print(c['agent'].get('reasoning_effort'))
print(c.get('fallback_model'))
PY
hermes --profile default -z 'Reply with exactly: OK grok-4.3 medium'
```

## Codex mini compression context

Kosta corrected that the Codex mini compression model has a larger context window than Hermes had cached/detected. Current local preference: set the auxiliary compression context override to 400,000 for all local Hermes profiles.

Apply to root/default and profiles such as `gpt`, `browser-agent`, `coding`, and `research`:

```yaml
auxiliary:
  compression:
    provider: openai-codex
    model: gpt-5.4-mini
    context_length: 400000
```

Also seed each profile's `context_length_cache.yaml` for both Codex base URL spellings when needed:

```yaml
context_lengths:
  gpt-5.4-mini@https://chatgpt.com/backend-api/codex: 400000
  gpt-5.4-mini@https://chatgpt.com/backend-api/codex/: 400000
```

This fixes warnings like: compression model `gpt-5.4-mini (openai-codex)` context is 272,000 but main `grok-4.3` threshold is 294,000. Do not lower the global compression threshold just to silence that warning unless Kosta asks for lower compression timing.

Smoke test root/default and GPT with Grok override and verify no compression warning is printed:

```bash
hermes --profile default --provider xai-oauth -m grok-4.3 -z 'Reply exactly: OK'
hermes --profile gpt --provider xai-oauth -m grok-4.3 -z 'Reply exactly: OK'
```

## RTX provider naming

The multiple RTX provider entries are not just cosmetic duplicates: they represent different OpenAI-compatible services/ports on the same GamingPC with different model, timeout, and context behavior. Prefer keeping separate provider records plus clean `model_aliases` unless Hermes deliberately adds one provider that supports per-model `base_url` routing.
