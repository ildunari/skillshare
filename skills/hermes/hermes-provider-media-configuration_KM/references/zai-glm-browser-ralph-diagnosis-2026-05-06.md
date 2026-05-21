# Z.ai / GLM diagnosis for BrowserAgent Ralph — 2026-05-06

Context: BrowserAgent Ralph (`browser-agent-ralph`) was intended as a GLM self-improvement/review lane for browser harness work, while `browser-agent` became the DeepSeek V4 Flash operator after Smoke-10 passed 10/10.

## What failed

Full Ralph Smoke-10 harness runs failed before writing result JSON with:

```text
API call failed after 3 retries: HTTP 429: The service may be temporarily overloaded, please try again later
missing_result_file=...results-browser-agent-ralph-....json
```

A tiny Hermes smoke test still worked:

```bash
hermes --profile browser-agent-ralph -z 'Reply with exactly: ok'
# ok
```

## Direct Z.ai checks performed

Direct API probes showed Z.ai itself was live:

- `GET /models` worked on `https://api.z.ai/api/coding/paas/v4`.
- `glm-5.1` tiny non-streaming calls worked.
- `glm-5.1` streaming worked.
- `glm-5.1` handled a ~44k-token prompt plus tool schemas repeatedly without 429.
- `glm-5-turbo` also worked and was faster on tiny calls.

This ruled out bad credentials, a dead endpoint, and the wrong base URL.

## Important GLM thinking finding

GLM-5.1 uses `reasoning_content` by default. With tiny max output, it can spend the entire output budget on hidden reasoning and return empty `content` with `finish_reason: length`.

Direct probe example:

- default GLM-5.1, `max_tokens=256`: returned `ok`, but used ~136 reasoning tokens and took ~5.5s.
- `thinking: {"type":"disabled"}`, `max_tokens=256`: returned `ok`, used 0 reasoning tokens, ~11 total tokens, and took ~2.8s.
- `glm-5-turbo` with thinking disabled was ~1s for the same tiny call.

Hermes notes already mention that Z.ai uses top-level `thinking.type`, not OpenAI/OpenRouter `reasoning_effort`. For direct Z.ai routes, changing only `agent.reasoning_effort` is not enough to force/disable thinking.

## Z.ai docs interpretation

Z.ai error docs say HTTP 429 can mean request concurrency exceeded, high frequency, rate limit triggered, account/usage limits, high traffic on the model, or fair-use restriction. Usage policy says coding-plan concurrency is dynamic by plan tier and resource availability.

Given direct probes worked but the autonomous full harness failed, the likely trigger is the heavy Hermes agent-loop request pattern rather than authentication or endpoint health.

## Practical conclusion

Ralph should not be the default browser operator. Keep `browser-agent` as the DeepSeek V4 Flash browser operator. Use Ralph/GLM as a narrow review/self-improvement lane that receives small artifacts and patch proposals, not full ten-task browser loops.

Recommended Ralph shape:

- prune broad/general skills from the profile; keep browser/harness/self-improvement/review skills only;
- use `glm-5-turbo` or explicitly disable Z.ai thinking for routine harness review;
- reserve GLM-5.1 thinking-enabled for small high-leverage planning/review prompts;
- split large harness evaluation into small review jobs: failed-result audit, verifier patch design, instruction-change review;
- do not diagnose future full-run 429s as auth failure until a tiny direct/Hermes smoke test fails too.

## Reusable probe pattern

Use a direct Python or curl probe that loads `GLM_API_KEY` / `ZAI_API_KEY` / `Z_AI_API_KEY` from profile/default `.env`, then tests:

1. `/models` on `https://api.z.ai/api/coding/paas/v4`.
2. tiny `glm-5.1` chat completion.
3. `thinking: {"type":"disabled"}` vs default.
4. a moderate prompt with tool schemas.
5. optional streaming.

Do not print API keys or raw secret-bearing environment values.
