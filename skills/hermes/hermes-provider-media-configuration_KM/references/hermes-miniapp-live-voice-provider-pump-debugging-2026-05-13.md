# Hermes Mini App live voice provider-pump debugging — 2026-05-13

Use this when Mini App voice connects to Gemini Live, hears/responds to an early prompt, then dies with a frontend/server message such as `provider event pump failed: ...`, especially after a `hermes_turn` tool call.

## Observed failure shape

Live service: `/Users/Kosta/LocalDev/hermes-voice-bridge`, local port `127.0.0.1:8765`, Mini App route `/voice`.

Key log sequence from `/Users/Kosta/.hermes/voice-bridge/system-launchd.err.log`:

```text
voice.session_created ... model='gemini-3.1-flash-live-preview'
voice.ws_open ...
voice.provider_connected ... provider='gemini-live'
voice.client.server_status ... state='ready'
voice.client.server_error ... message="provider event pump failed: No module named 'importlib.resources'"
voice.session_ended ... input_seconds=12.797 output_seconds=2.28
voice.client.ws_close ... code=1006
```

An earlier separate session completed two `voice.hermes_turn_completed` events, then hit SQLite accounting failures:

```text
voice.store_save_failed ... error='unable to open database file'
voice.store_end_failed ... error='unable to open database file'
```

Treat these as two adjacent failure classes: provider event-pump/tool-turn failure vs session-store persistence failure.

## Triage ladder

1. Check live service and logs without restarting the Telegram gateway:

```bash
curl -sS --max-time 5 http://127.0.0.1:8765/health
/usr/sbin/lsof -nP -iTCP:8765 -sTCP:LISTEN
tail -n 300 /Users/Kosta/.hermes/voice-bridge/system-launchd.err.log | egrep -i 'voice\.|provider event pump|importlib\.resources|sqlite|Traceback|Exception|error'
```

2. Verify the Hermes control path separately through the bridge settings, not with a bare curl that omits the API key:

```bash
cd /Users/Kosta/LocalDev/hermes-voice-bridge
source .venv/bin/activate
python - <<'PY'
import asyncio
from hermes_voice_bridge.config import get_settings
from hermes_voice_bridge.hermes_client import HermesClient
async def main():
    s = get_settings()
    print('has_key', bool(s.hermes_api_key), 'base', s.hermes_api_base)
    res = await HermesClient(s).ask('Can you hear me? Answer in one short sentence.', 'voice-debug')
    print(res.display_text[:500])
asyncio.run(main())
PY
```

3. Probe Gemini Live separately. A no-tool text prompt should connect and produce audio; a forced `hermes_turn` tool prompt should emit `tool.call`, accept `toolResponse.functionResponses[]`, and then produce audio/turn completion. If no-tool works but tool-turn stalls or throws, the fault is Live tool handling / provider normalization, not Hermes GPT.

4. Run the project verification before claiming a code change is safe:

```bash
cd /Users/Kosta/LocalDev/hermes-voice-bridge
source .venv/bin/activate
python -m pytest -q
python -m py_compile $(find src -name '*.py')
```

## Current-doc anchors

Google Live API docs checked 2026-05-13:

- Gemini 3.1 Flash Live Preview supports function calling, but synchronous only.
- Client messages over the WebSocket must contain exactly one of `setup`, `clientContent`, `realtimeInput`, or `toolResponse`.
- Tool responses are `toolResponse.functionResponses[]`, matched by function-call `id`.
- Live audio spec: input raw 16-bit PCM at 16 kHz; output raw 16-bit PCM at 24 kHz.

## Pitfalls

- Do not call this a token/context/time limit without logs. The reproduced crash happened after Gemini was ready and around provider event-pump handling.
- Do not diagnose Hermes GPT from a bare `curl` to `:8643` that lacks the bridge's configured API key; use `HermesClient(get_settings())` for the faithful path.
- Provider-pump errors need full server-side traceback logging; the UI string alone is not enough. Future fixes should preserve `voice.provider_event_pump_failed`-style traceback logging before chasing frontend causes.
- Claude Code review can be useful, but bound it tightly. Large repo-context Claude runs may time out or burn budget before returning findings; for this class, prefer a no-edit, file-scoped prompt with only `app.py`, `providers/gemini_live.py`, `sessions.py`, `hermes_client.py`, and tests in scope.
- If Gemini emits `tool.call` but stalls after the tool response, inspect the `FunctionResponse.response` shape. For Hermes voice bridge, wrap the Hermes turn payload under `response.result`; flat `spoken_text`/`display_text` at the response root can hang Gemini Live 3.1 synchronous tool turns.
