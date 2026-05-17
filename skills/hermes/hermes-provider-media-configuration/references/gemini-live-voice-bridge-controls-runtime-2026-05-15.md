# Gemini Live Voice Bridge controls + runtime hardening (2026-05-15)

Use this when editing `~/LocalDev/hermes-voice-bridge`, the Telegram Mini App live voice UI, or Gemini Live tool/cancel behavior.

## Current Gemini Live behavior to preserve

- Voice selection is supported through `generationConfig.speechConfig.voiceConfig.prebuiltVoiceConfig.voiceName`.
- Gemini 3.1 Flash Live thinking uses `thinkingConfig.thinkingLevel` (`minimal`, `low`, `medium`, `high`).
- Server VAD config lives under `realtimeInputConfig.automaticActivityDetection`: `startOfSpeechSensitivity`, `endOfSpeechSensitivity`, `prefixPaddingMs`, `silenceDurationMs`.
- Barge-in is `realtimeInputConfig.activityHandling`: `START_OF_ACTIVITY_INTERRUPTS` or `NO_INTERRUPTION`.
- Manual/push-to-talk VAD requires automatic VAD disabled and `activityStart` / `activityEnd`; do not send those events in normal open-mic mode.
- Gemini 3.1 Flash Live tool calls are sequential; do not rely on `NON_BLOCKING` async function behavior for background jobs.
- Hermes tool responses must remain wrapped as `response: { result: <VoiceTurnResponse> }`; flat `response` payloads can hang Live tool turns.

## Runtime pitfalls found and fixed

- Do not process provider events serially through a blocking `await hermes.ask(...)`; otherwise `toolCallCancellation` cannot win while Hermes is in flight. Spawn tracked tool tasks and let cancellation/interruption mutate the gate immediately.
- Track Hermes tool tasks by Gemini `functionCall.id`, not just a bare task set. On explicit `toolCallCancellation`, cancel only matching call IDs and do **not** send a function response for the canceled call; reserve safe `should_speak: false` tool responses for stale generations where Gemini is still waiting.
- On `control.interrupt`, suppress provider output immediately and send `audio.clear`. Do not clear suppression just because user mic/audio/transcript keeps arriving after barge-in; Gemini Live transcriptions have no guaranteed ordering and late input transcripts can belong to the interrupted turn.
- If one Gemini `serverContent` frame contains `interrupted: true` plus `modelTurn` audio/text or input/output transcriptions, process `interrupted` first and drop same-frame audio/text/transcripts. The Live API docs say `interrupted` means clients should stop and empty playback; same-frame content is unsafe to play.
- On provider `interrupted` or `tool.cancel`, cancel/await tracked Hermes tool tasks before bumping the generation and sending `audio.clear`.
- On WebSocket/session shutdown, cancel/await tracked tool tasks before closing the provider so no orphan task later writes to a closed WebSocket/provider.
- Stamp client-visible events with generation IDs and have the Mini App ignore older generations. This protects stale audio/transcripts/status after barge-in.

## UI/session behavior to preserve

- WebSocket session tokens stay in `Sec-WebSocket-Protocol`, never `?token=` URLs.
- Voice controls are captured at session creation because Live setup config cannot be changed mid-connection. If the UI lets controls change while connected, make the change visibly apply only to the next session or lock/revert the control.
- Separate mic mute from speaker mute. Speaker mute clears queued playback; mic mute sends audio end/halts outgoing mic chunks.
- Implement sustained barge-in as duration-over-threshold plus cooldown, and reset the sustained timer whenever state leaves `speaking`, mic mute turns on, barge-in is disabled, or RMS drops below threshold. Otherwise a prior loud frame can cause an immediate false interrupt in a later speaking turn.
- Avoid duplicate transcript finals with a role/generation/text key.
- Show safe status/timeline summaries only; never expose raw chain-of-thought.
- For browser Mini App background progress, prefer authenticated fetch streaming of SSE-formatted events over polling. EventSource cannot send headers, so authenticated fetch-stream is the safer default here.
- For local browser smoke tests, if a dev auth shim is needed, pass the secret via localhost-only URL fragment and immediately move it to `sessionStorage` with `history.replaceState`; never use query-string bearer secrets, and never weaken production fail-closed auth.
- Bound background-job memory and stop/abort active client-side streams during cleanup. If the background job path is still bridge-side scaffolding, document it as stream/start/stop plumbing rather than a production Hermes async run manager.

## Verification pattern

From repo root:

```bash
python -m pytest
python -m py_compile $(find src -name '*.py')
node --check src/hermes_voice_bridge/static/app.js
```

If a browser smoke exists, run it too:

```bash
node --check scripts/smoke_voice_ui.mjs
node scripts/smoke_voice_ui.mjs
```

Useful smoke checks:

- `/health` returns ok.
- Authenticated `/voice/session` returns a WS URL with no `token=` and a separate `ws_token`.
- Mock Gemini `tool.call` -> Hermes `VoiceTurnResponse` -> wrapped Gemini tool response.
- Interruption sends `audio.clear`, suppresses stale provider audio/text, and cancels tracked tool tasks.
- A Gemini `serverContent` frame containing both `interrupted: true` and audio/text/transcriptions produces only interruption/turn-complete handling; same-frame stale content must not reach UI/audio.
- Late `inputTranscription` after interruption does not reopen provider-output suppression by itself.
- Background job starts, streams SSE-formatted progress via authenticated fetch, and can be stopped.
- Mini App static/browser checks cover controls, unsupported speed labeling, compact SVG/Lucide-style timeline, no emoji, no chain-of-thought labels, duplicate final suppression, and localhost-only dev auth.

Run Codex adversarial review after major checkpoints, but verify findings in source/tests before accepting them. High-value review prompts: stale-event speech, cancellation races while `hermes.ask()` is in flight, tool-response shape, auth regressions, manual VAD misuse, UI dead states, and orphaned jobs/tasks.
