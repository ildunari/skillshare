# GPT profile Qwopus compression correction — 2026-05-11

## Signal

Kosta noticed a Telegram warning:

> Compression model qwopus-gpu (custom:RTX) context is 131,072 tokens, but the main model gpt-5.5 compression threshold was 270,000 tokens. Auto-lowered this session's threshold...

The GPT profile's main model was already correct, but active compression auxiliary routing was still pinned to Qwopus.

## Correct GPT profile shape

For Hermes GPT, Kosta wants the whole active GPT path to stay GPT/OpenAI Codex unless explicitly changed:

- `model.provider: openai-codex`
- `model.default: gpt-5.5`
- `model.base_url: https://chatgpt.com/backend-api/codex`
- `agent.reasoning_effort: medium`
- `auxiliary.vision.provider/model/base_url`: OpenAI Codex / `gpt-5.5` / Codex URL
- `auxiliary.compression.provider/model/base_url`: OpenAI Codex / `gpt-5.5` / Codex URL
- legacy `compression.summary_provider/model/base_url`: same OpenAI Codex / `gpt-5.5` / Codex URL

Qwopus aliases/custom providers can remain defined for manual use. The important point is that they must not be active GPT compression/vision/chat defaults.

## Pitfall

A stale provider skill note said GamingPC Qwopus should be default for `root/GPT Hermes`. Kosta corrected this: Qwopus belongs in default/root or specialized memory/mem0/auxiliary-memory routing, not GPT's own chat/vision/compression path. Treat any future “root/GPT Qwopus” note as suspect and inspect the active GPT profile before changing it.

## Verification pattern

From the Hermes repo root:

```bash
python - <<'PY'
from pathlib import Path
import yaml
p=Path('/Users/Kosta/.hermes/profiles/gpt/config.yaml')
c=yaml.safe_load(p.read_text())
checks = {
 'main': (c['model']['provider'], c['model']['default'], c['model'].get('base_url'), c['agent'].get('reasoning_effort')),
 'vision': tuple(c['auxiliary']['vision'].get(k) for k in ('provider','model','base_url')),
 'compression_aux': tuple(c['auxiliary']['compression'].get(k) for k in ('provider','model','base_url')),
 'compression_legacy': (c['compression'].get('summary_provider'), c['compression'].get('summary_model'), c['compression'].get('summary_base_url')),
}
for k,v in checks.items(): print(k, v)
PY
hermes --profile gpt status | sed -n '/◆ Environment/,/◆ API Keys/p'
hermes --profile gpt --ignore-rules -z 'Reply with exactly: gpt-profile-ok'
```

Expected one-shot output: `gpt-profile-ok`.
