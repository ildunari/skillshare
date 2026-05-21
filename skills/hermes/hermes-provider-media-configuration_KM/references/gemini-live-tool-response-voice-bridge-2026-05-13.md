# Gemini Live tool-response debugging for Hermes Voice Bridge — 2026-05-13

Use when the Telegram Mini App live voice bridge connects to Gemini Live but hangs/crashes around `hermes_turn`, especially after the first spoken prompt or with UI text like `provider event pump failed`.

## Durable lesson

For Gemini 3.1 Flash Live synchronous function calling, respond to `toolCall.functionCalls[]` with `toolResponse.functionResponses[]` where the `id` matches the call id. In the Hermes voice bridge, do **not** send the Hermes `VoiceTurnResponse` flat as the FunctionResponse `response`; wrap it under a normal result object:

```json
{
  "toolResponse": {
    "functionResponses": [
      {
        "id": "<call id>",
        "name": "hermes_turn",
        "response": {"result": {"spoken_text": "...", "display_text": "...", "metadata": {}}}
      }
    ]
  }
}
```

A flat payload such as `"response": {"spoken_text": ...}` can make Gemini Live 3.1 leave the synchronous tool turn hanging. The failure can look like a time/token issue because the first turn may work or partially speak, then the second turn never completes.

## Debugging ladder

1. Check voice bridge logs first: `~/.hermes/voice-bridge/system-launchd.err.log` and `.log`. Look for `voice.provider_connected`, `voice.hermes_turn_completed`, `voice.provider_event_pump_failed`, `voice.store_save_failed`, and client `server_error`/`ws_close` lines.
2. Verify Hermes-as-brain independently through `HermesClient.ask()` or the GPT profile API server. If direct `HermesClient.ask()` works for normal and tool-using prompts, the break is in the Gemini Live bridge/control path, not Hermes GPT.
3. Build a direct Gemini Live repro that sends two text turns, forces `hermes_turn`, sends the exact tool response shape, and waits for `response.done` on both turns. This isolates Live API protocol shape from iOS mic/WebView issues.
4. Treat SQLite/accounting writes as non-fatal. A DB save error should log and send a warning, but must not kill the active WebSocket or stop audio forwarding.
5. If the UI says only `provider event pump failed: ...`, make sure `_pump_provider_events()` logs the full exception traceback server-side before returning the user-facing error.

## Verification signals

- Unit tests should cover the tool response shape and provider-pump/accounting failure behavior.
- `python -m pytest` and `python -m py_compile $(find src -name '*.py')` pass in `~/LocalDev/hermes-voice-bridge`.
- Direct Gemini Live two-turn repro reaches `response.done` for both turns.
- After restart, `/health` on `127.0.0.1:8765` returns OK and the live logs show two `voice.hermes_turn_completed` lines for a two-prompt Mini App session.
