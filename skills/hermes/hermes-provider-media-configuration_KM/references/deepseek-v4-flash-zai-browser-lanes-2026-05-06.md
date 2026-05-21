# DeepSeek V4 Flash and Z.ai GLM lanes for browser/profile work — 2026-05-06

Condensed provider/model findings from BrowserAgent planning.

## Z.ai

- `glm-5.1`: text-only, 200K context, 128K max output, function calling/MCP/structured output/context caching. Good candidate for long-horizon text/tool planning, not visual browser work.
- `glm-5-turbo`: text-only, 200K context, 128K max output. Marketed for faster/stabler long-chain agent execution; benchmark before trusting as main operator.
- `glm-5v-turbo`: image/video/text/file input, 200K context, 128K max output, function calling. Best Z.ai lane for screenshot-heavy browser/GUI work.

Known-good Hermes-style vision auxiliary block:

```yaml
auxiliary:
  vision:
    provider: zai
    model: glm-5v-turbo
    base_url: https://api.z.ai/api/coding/paas/v4
    api_key: ''
    timeout: 30
    extra_body: {}
    download_timeout: 30
```

## DeepSeek V4 Flash

Useful as a fast text/tool browser-loop candidate, not as the sole high-stakes brain.

Official/provider facts found:

- Model ID: `deepseek-v4-flash` for new configs; avoid compatibility names `deepseek-chat` / `deepseek-reasoner` for new work because official docs scheduled them for deprecation.
- Context: 1M.
- Max output: 384K.
- Supports tool calls, JSON output, thinking/non-thinking modes.
- No official vision support found; treat as text-only.

Benchmark/reputation snapshots from the research pass:

- Artificial Analysis Intelligence Index around 47; speed around 77 output tok/s in its page at time of research; high hallucination tendency flagged.
- LiveBench snapshot: roughly 67.25 global, 69.23 coding, 50 agentic coding.
- OpenRouter provider tool-call error examples around 2–3%; provider speed varied around ~60–70 tok/s.

Recommendation for browser harness:

- Use DeepSeek V4 Flash for structured DOM/CDP/form/extraction loops when the harness makes the task explicit and verification-gated.
- Use `glm-5v-turbo` for visual ambiguity/screenshots.
- Escalate to `glm-5.1`, `deepseek-v4-pro`, or GPT when stuck twice, task is high-risk, or strategy/planning becomes the main problem.

Do not build a constant smart-orchestrator + fast-worker stack as the default. Browser state should usually live with the acting model; orchestration belongs at escalation boundaries.
