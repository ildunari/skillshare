# xAI Grok default-profile auth and fallback pitfall — 2026-05-17

When switching the root/default Hermes profile to `xai-oauth` / `grok-4.3`, do not stop at `model.default`, `model.provider`, and `agent.reasoning_effort`.

Observed failure pattern:

- `hermes status --profile default` can show `Model: grok-4.3` and `Provider: xAI Grok OAuth` from config alone.
- A real one-shot can still fail with `No xAI OAuth credentials stored` if root `~/.hermes/auth.json` lacks the `xai-oauth` provider/token, even when the GPT profile has working xAI OAuth in `~/.hermes/profiles/gpt/auth.json`.
- The default profile may also have `fallback_model` still pointing at `openai-codex` / `gpt-5.3-codex-spark`, which makes Hermes appear to be “on Spark” after primary provider/auth trouble.

Reliable fix/verification sequence:

1. Read the actual default config: `hermes --profile default config path`, then inspect `model.*`, `agent.reasoning_effort`, and `fallback_model`.
2. Set root/default to:
   - `model.default: grok-4.3`
   - `model.provider: xai-oauth`
   - `model.base_url: https://api.x.ai/v1`
   - `agent.reasoning_effort: medium`
3. Change `fallback_model` to xAI/Grok too if the user wants the default Hermes not to route through Spark on fallback.
4. Verify root auth has xAI OAuth credentials, not just the GPT profile: `hermes auth list` and/or inspect root `~/.hermes/auth.json` for `providers.xai-oauth` plus a credential-pool entry.
5. If GPT has a valid xAI OAuth token and root does not, copy the `xai-oauth` provider and credential-pool entries from GPT auth into root auth with a timestamped backup of root `auth.json` first.
6. Final proof is a real one-shot: `hermes --profile default -z 'Reply with exactly: OK grok-4.3 medium'`.

Do not claim the provider switch is done from `hermes status` alone; status may reflect config while runtime auth is still missing.