# Qwopus custom provider live-gateway verification — 2026-05-10

Use this when wiring local OpenAI-compatible inference providers such as GamingPC RTX `qwopus-gpu` or Mac Studio `qwopus` into Hermes.

## Lesson

Endpoint health and fresh CLI one-shots are not enough. In this session, both Qwopus endpoints passed `/health`, `/v1/models`, direct non-stream/stream chat, forced tool schema, long-ish prompt, and fresh `hermes -z` one-shots. A live default Telegram gateway thread still got stuck after a `session_search` tool result while using `custom:RTX`, because the already-running gateway had not been restarted/reloaded after the custom-provider timeout fix and the exact live gateway tool-loop path had not been tested.

The missed test class was: **existing gateway process + selected custom provider + gateway session history + real tool call + second model turn after tool result**.

## Required verification ladder for Hermes custom providers

When changing or claiming support for a Hermes local/custom provider, verify in this order:

1. Endpoint basics from the Mac Studio:
   - `GET <base without /v1>/health`
   - `GET <base>/models`
2. Direct OpenAI-wire requests:
   - non-stream chat with common junk/provider fields present
   - streaming SSE
   - forced tool-call schema (`tools` + `tool_choice`)
   - a long-ish prompt that exercises prefill, not just `OK`
3. Fresh Hermes process:
   - `hermes --profile gpt -z ... --provider custom:<Name> -m <model>`
   - at least one real tool-use one-shot with `-t terminal` or another small deterministic tool
4. **Live gateway path before declaring Telegram/Discord done:**
   - restart or otherwise confirm the target gateway process has loaded the new code/config
   - select the provider in the same gateway surface the user will use
   - run a real tool-loop task that requires a tool result followed by another model turn
   - inspect the session transcript/logs to confirm the assistant continued after the tool result and a final response was delivered

## Timeout/config pitfall

Hermes timeout helpers historically looked only under `providers:`. Custom providers live under `custom_providers:` for routing/model picker purposes, so timeout/stale-timeout changes may be ignored by existing code paths unless the helper supports custom providers or mirrored entries exist under `providers:`. For long-context Qwopus, keep these values on the provider/model:

```yaml
request_timeout_seconds: 3600
stale_timeout_seconds: 1800
models:
  <model>:
    timeout_seconds: 3600
    stale_timeout_seconds: 1800
```

For already-running gateways, remember that config/code edits do not necessarily affect in-memory agents. Fresh `hermes -z` passing proves the new process path, not the old live gateway process.

## Stuck-session signal

If the Telegram UI shows a stale “thinking/typing” state but the session file stops immediately after a tool result and gateway logs have no `response ready`, treat it as a live gateway/tool-loop failure, not proof the inference endpoint is unhealthy. Check the model server logs for the expected POSTs, then reload/restart the affected gateway process with user approval and rerun the live-gateway tool-loop smoke.

## Structured tool-call mismatch signal

If an RTX Qwopus Hermes thread visibly prints pseudo-tool syntax such as `<memory-search>...</memory-search>`, `<tool_call>`, `<tool_code>`, or JSON-looking `{"name":"terminal","arguments":...}` instead of executing a tool, check the OpenAI tool contract directly before blaming general model instability.

A healthy `/health` and `/v1/models` response is not enough. In the 2026-05-12 check, the endpoint advertised `chat`, `streaming`, and `reasoning_content`, but not `tools`; direct OpenAI `tools`/`tool_choice` probes returned literal pseudo-tool text with `tool_calls=None`, and a Hermes `custom:RTX` terminal-tool one-shot returned raw JSON text instead of executing `terminal`.

Operational stance: RTX Qwopus is usable for model-only chat, no-thinking short calls, and memory microtasks. Tool-heavy Telegram/Discord sessions require an explicit compatibility layer: either the proxy must return structured OpenAI `tool_calls`, or Hermes must translate pure/single Qwopus pseudo-tool text into validated tool calls before normal execution.

## Hermes-side textual tool-call compatibility — 2026-05-12

Hermes now has a narrow Qwopus/RTX compatibility shim in `run_agent.py` for common textual tool-call outputs. It is scoped to Qwopus/RTX signals only (`qwopus` model, `custom:RTX`/`rtx` provider, or the RTX base URL) so normal providers are not affected.

The shim promotes only pure/single textual calls after response normalization and before normal Hermes tool validation/execution. Supported shapes observed in live testing:

- Bare JSON: `{"name":"terminal","arguments":{"command":"echo QWOPUS_TOOL_OK"}}`
- Short preface plus a single JSON suffix, such as `I'll load the skill.\n{"name":"skill_view","arguments":{"name":"bird"}}`, but only when the JSON object/array consumes the rest of the message and the preface does not contain earlier code fences.
- Short preface plus one final fenced JSON block, under the same “no earlier code fences” rule.
- Alias JSON: `{"tool":"terminal","args":{...}}`
- XML-ish single tool tags when the tool name is valid
- Pure terminal shell fences such as ````bash\necho QWOPUS_TOOL_OK\n```` mapped to `terminal` with `{"command": ...}`; prefaced shell fences are intentionally not promoted because they are too often documentation/examples.
- Qwopus/Codex-style JSON with `"name":"bash"`, `"name":"shell"`, `"name":"sh"`, `"name":"terminal_run"`, `"name":"run_terminal"`, or `"name":"print"` aliases mapped to Hermes' real `terminal` tool when `terminal` is loaded.
- Single-item JSON arrays/fenced JSON such as `[{"name":"bash","arguments":{"command":"printf DIRECT_TOOL_OK"}}]`, matching the RTX endpoint's forced-tool response shape.
- Terminal pseudo-tool args normalize `cmd` → `command` and `timeout_seconds` → `timeout` before dispatch.

Safety boundaries that should remain in future edits:

- Validate the parsed tool name against `self.valid_tool_names`; never execute unknown/hallucinated names.
- Do not parse arbitrary prose that merely contains tool-looking text; require a pure/single tool-call output.
- Keep the feature scoped to Qwopus/RTX until another provider is explicitly proven to need the same compatibility.
- Preserve targeted tests for JSON promotion, shell-fence promotion, and non-Qwopus non-promotion.

Verification recipe after changing this path:

```bash
pytest -q \
  tests/run_agent/test_run_agent.py::TestBuildAssistantMessage::test_qwopus_promotes_bare_json_tool_call \
  tests/run_agent/test_run_agent.py::TestBuildAssistantMessage::test_textual_tool_compat_is_scoped_to_qwopus \
  tests/run_agent/test_run_agent.py::TestBuildAssistantMessage::test_qwopus_promotes_terminal_shell_fence

HERMES_HOME=/Users/Kosta/.hermes hermes -z \
  'Use the terminal tool to print QWOPUS_TOOL_OK, then reply with the exact printed text.' \
  --provider custom:RTX -m qwopus-gpu -t terminal
```

Expected live smoke result: final answer contains exactly `QWOPUS_TOOL_OK`. This proves the Hermes compatibility path executed a real tool, but it is still a shim; it does not mean the Qwopus proxy itself provides native OpenAI tool calls.
