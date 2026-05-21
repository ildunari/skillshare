# Codex mini compression context override

Session lesson from 2026-05-17: after switching root/default Hermes to Grok, startup emitted a compression warning because the auxiliary compression model `gpt-5.4-mini` was resolved as 272K while Grok 4.3’s compression threshold was 294K.

Kosta corrected the assumption: the local mini definition should be treated as 400K for Hermes compression.

## Fix pattern

For every active profile config (`~/.hermes/config.yaml` plus `~/.hermes/profiles/*/config.yaml`) set:

```yaml
auxiliary:
  compression:
    context_length: 400000
```

Also seed or update each profile’s `context_length_cache.yaml`:

```yaml
context_lengths:
  gpt-5.4-mini@https://chatgpt.com/backend-api/codex: 400000
  gpt-5.4-mini@https://chatgpt.com/backend-api/codex/: 400000
```

## Verification

Run a one-shot for the affected profile/model and confirm the compression warning is gone. Example:

```bash
hermes --profile default --provider xai-oauth -m grok-4.3 -z 'Reply exactly: OK'
```

A successful fix returns the response without the `Compression model ... context is 272,000 tokens` status card.
