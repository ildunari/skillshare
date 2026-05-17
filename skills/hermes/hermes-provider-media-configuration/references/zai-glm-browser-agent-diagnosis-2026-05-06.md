# Z.ai GLM browser-benchmark false-positive provider diagnosis — 2026-05-06

## Situation

Ralph/GLM BrowserAgent benchmark runs appeared to fail with:

```text
API call failed after 3 retries: HTTP 429: The service may be temporarily overloaded, please try again later
missing_result_file=...
```

Initial direct Z.ai checks showed the provider was healthy:

- `GET /models` succeeded on `https://api.z.ai/api/coding/paas/v4`.
- Tiny `glm-5.1` calls succeeded.
- A ~44k-token prompt with tools succeeded repeatedly.
- Streaming succeeded.
- `glm-5-turbo` worked and was faster on tiny calls.

Z.ai docs confirm HTTP 429 can mean concurrency/frequency/usage/model-traffic throttling, but in this case the trigger was not ordinary prompt size or credentials.

## Actual cause

The Ralph/browser benchmark had a browser backend config conflict:

```text
BROWSER_CDP_URL=http://localhost:9222
AGENT_BROWSER_AUTO_CONNECT=1
```

Browser tool calls failed with:

```text
Cannot use --auto-connect and --cdp together
```

The model then fell back to terminal `curl`, which injected large raw HTML tool outputs into the conversation. Request dumps showed the failed path had large bodies and repeated tool errors, e.g. ~143k JSON chars and ~50k terminal-output chars. The later 429 was a secondary symptom of an unnecessarily heavy broken loop.

## Z.ai-specific notes

GLM-5.1 defaults to emitting `reasoning_content`; small-output-budget calls may spend the entire response on hidden thinking and return empty visible content. Direct probe result from this session:

- default GLM-5.1 tiny call: visible `ok`, ~148 total tokens, 136 reasoning tokens.
- `thinking: {"type":"disabled"}`: visible `ok`, ~11 total tokens, 0 reasoning tokens, faster.
- `glm-5-turbo` with thinking disabled: also worked and was faster.

Hermes currently documents that Z.ai thinking uses top-level `thinking.type`, not OpenAI/OpenRouter `reasoning_effort`. Do not assume `agent.reasoning_effort: high` forces or optimizes Z.ai thinking.

## Diagnostic order for future sessions

When Z.ai/GLM fails only in an agentic browser run but works in normal Hermes/default prompts:

1. Smoke-test the exact profile with a tiny prompt.
2. Direct-probe Z.ai `/models` and a tiny completion without printing keys.
3. Check failed request dumps under the profile `sessions/request_dump_*.json` for tool errors, request size, and repeated terminal/screenshot/HTML outputs.
4. Check browser env conflicts (`BROWSER_CDP_URL`, `AGENT_BROWSER_AUTO_CONNECT`) before blaming Z.ai context limits.
5. If GLM is used as a review lane rather than an operator, consider `glm-5-turbo` or `thinking.disabled` to reduce token burn.

## Good verification commands

```bash
hermes --profile browser-agent-ralph -z 'Reply exactly ok'

env -u BROWSER_CDP_URL -u AGENT_BROWSER_AUTO_CONNECT \
  hermes --profile browser-agent -t browser \
  -z 'Use the browser tool to open http://127.0.0.1:8766/ and reply exactly opened if it opened.'
```
