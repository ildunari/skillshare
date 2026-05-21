# Z.ai / GLM BrowserAgent diagnostics — 2026-05-06

Session lesson from diagnosing `browser-agent-ralph` and `browser-agent-glm51` failures on Mac Studio.

## What looked wrong

`browser-agent-ralph` repeatedly failed full Smoke-10 runs with `HTTP 429` from Z.ai/GLM and no result file. Tiny GLM prompts worked, which made the issue look like provider unreliability under load.

## What actually caused most of it

The browser backend was misconfigured through inherited environment variables:

```text
AGENT_BROWSER_AUTO_CONNECT=1
BROWSER_CDP_URL=http://localhost:9222
```

`agent-browser` treats auto-connect and explicit CDP as mutually exclusive. Browser tools failed with:

```text
Cannot use --auto-connect and --cdp together
```

Ralph then fell back to terminal/curl scraping, which dumped huge raw HTML into the conversation. A failed request dump showed a ~143k-char body, ~50k chars of terminal output, repeated browser failure messages, and then provider retry exhaustion. The 429 symptom was downstream of the bad browser path, not proof that Z.ai was globally broken.

## Direct Z.ai probes

Direct probes against `https://api.z.ai/api/coding/paas/v4` showed:

- `/models` worked.
- `glm-5.1` tiny calls worked.
- streaming worked.
- ~44k-token prompt + tools worked repeatedly.
- `glm-5-turbo` was much faster for tiny/direct calls.
- GLM-5.1 default thinking can burn output tokens as `reasoning_content`; `thinking: {"type":"disabled"}` made tiny calls use far fewer tokens and return faster.

## Fix/workaround

For BrowserAgent benchmark runs, unset both env vars in the runner:

```bash
env -u BROWSER_CDP_URL -u AGENT_BROWSER_AUTO_CONNECT hermes --profile <profile> ...
```

Also remove stale `BROWSER_CDP_URL`/`AGENT_BROWSER_AUTO_CONNECT` from profile `.env` files. If the current gateway inherited old env, do not restart it from Telegram; use explicit `env -u` in benchmark scripts until the gateway is restarted from a safe local shell.

## Model conclusion from this session

This note captures an earlier diagnostic phase, not the final promotion decision. At this point, the provisional recommendation was to keep DeepSeek Flash as the default operator and use GLM/Ralph for review/self-improvement lanes.

Superseded later the same day by the canonical promotion documented in `hermes-maintenance-and-distribution/references/browser-agent-canonical-profile-promotion-2026-05-06.md`: hardened one-task fresh-context Smoke-10 runs promoted canonical `browser-agent` to Z.ai `glm-5.1` with `glm-5v-turbo` as the explicit vision auxiliary. Do not treat this older diagnostic note as the current default-profile recommendation.
