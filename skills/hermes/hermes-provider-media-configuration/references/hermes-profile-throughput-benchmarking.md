# Hermes profile throughput benchmarking

Session lesson: benchmarking visible final-output throughput across Hermes profiles is useful, but do not "fix" speed variance by changing the intended reasoning default without confirming policy. The default/general DeepSeek profile intentionally uses `agent.reasoning_effort: high`; GPT commonly uses `medium`. If asked to compare speed, report that reasoning setting as part of the test matrix instead of normalizing it away.

## Safe benchmark shape

Use one-shot final-output prompts so the measurement is mostly model/provider latency plus visible generation, not tools or profile prompt overhead:

```bash
HERMES_HOME=/Users/Kosta/.hermes \
  hermes --ignore-rules -z 'Return only the final answer. Do not explain, do not reason aloud, do not use tools. Write exactly 300 words of plain English about why benchmarking matters. No markdown.'

HERMES_HOME=/Users/Kosta/.hermes/profiles/gpt \
  hermes --ignore-rules -z 'Return only the final answer. Do not explain, do not reason aloud, do not use tools. Write exactly 300 words of plain English about why benchmarking matters. No markdown.'
```

For more rigorous runs, use Python with `time.perf_counter()` and `tiktoken` (`o200k_base`) to count final visible output tokens. Report wall-clock visible-output tokens/sec. Hidden reasoning tokens are not counted, but their latency is included in wall time.

## What to report

- Profile path, model, provider, and `agent.reasoning_effort` for each profile.
- Median tokens/sec over several runs, not just average; provider stalls create outliers.
- Whether `--ignore-rules` was used.
- Caveat that this is visible final-output throughput, not provider-side total token accounting.

## Pitfall

Do not silently change `agent.reasoning_effort` to improve benchmark numbers. For the default DeepSeek profile, `high` is the expected default. If Kosta asks to "fix it" after a benchmark, inspect likely causes and recommend options, but preserve intended profile semantics unless he explicitly approves changing them.