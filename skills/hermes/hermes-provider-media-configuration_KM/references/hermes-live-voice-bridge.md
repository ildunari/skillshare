# Archived skill: hermes-live-voice-bridge

Original path: `/Users/Kosta/.hermes/profiles/gpt/skills/hermes/hermes-live-voice-bridge`
Absorbed into umbrella: `hermes-provider-media-configuration` on 2026-04-29.

---

---
name: hermes-live-voice-bridge
description: Use when designing, implementing, or debugging a Hermes live voice chat path, especially a Telegram Mini App Live Voice tab backed by Gemini 3.1 Flash Live, Grok Voice, OpenAI Realtime, Retell, LiveKit, or Pipecat while keeping Hermes/GPT-5.5 as the brain. Trigger on requests for Hermes live voice, realtime audio, voice calls, Mini App voice tab, Gemini Live API costs/credits, Google AI Pro API credit activation, or voice-provider architecture/spec work.
---

# Hermes Live Voice Bridge

Use this when Kosta wants live voice chat for Hermes without building a full native app or replacing Hermes with the realtime voice provider.

## Core decision

Structure voice as a **transport bridge into Hermes**, not as a replacement agent.

The realtime provider handles audio transport, VAD/turn-taking, transcript events, and spoken output. Hermes/GPT-5.5 remains the brain and keeps access to the normal session, tools, browser automation, MCP, subagents, memory, and Telegram context.

Recommended first target: **Gemini 3.1 Flash Live Preview**.

Why:
- It is the current Google realtime audio-to-audio target, not Gemini 2.5.
- It is cheap enough to test seriously.
- Kosta's Google AI Pro / Developer Program benefit can provide monthly cloud credits that may offset Gemini API usage.
- A provider adapter can keep Grok Voice and OpenAI Realtime swappable later.

## Current verified Google credit state on Mac Studio

During the April 26, 2026 session, a browser subagent activated Kosta's Google AI Pro / Google Developer Program benefit for `kosta963@gmail.com`.

Verified state:
- Benefit: `$10 monthly Gen AI & Cloud credits`
- Billing account: `My Billing Account`
- Remaining balance at activation: `$10`
- Cloud credit label: `Google Developer Program premium benefit - CREDIT_TYPE_MONTHLY`
- Start: Apr 26, 2026
- End: Apr 26, 2027
- Verified in both Google Developer Program Benefits and Google Cloud Billing Credits

Useful check URLs:
- https://developers.google.com/program/my-benefits
- https://console.cloud.google.com/billing/credits
- https://aistudio.google.com/app/billing

Important nuance:
- This is not the old Google Cloud `$300` free trial credit; Google docs say that free-trial credit does not apply to Gemini API / AI Studio usage.
- The AI Pro / Developer Program credit is different and was described by Google as usable for AI Studio, Vertex AI, and Google Cloud products.
- Before sustained tests, verify the Gemini API project/API key is tied to the billing account that has this credit.

## Cost estimates to reuse

Worst-case continuous audio estimates. Real use should be lower with VAD, push-to-talk, shorter replies, and idle timeouts.

```text
Provider/model                         Estimated live audio cost
Gemini 3.1 Flash Live Preview           ~$1.38/hr continuous in + out
Grok Voice Agent                        ~$3.00/hr
OpenAI gpt-4o-mini realtime preview     ~$1.80/hr continuous in + out
OpenAI gpt-realtime                     ~$5.76/hr continuous in + out
```

Gemini 3.1 Flash Live pricing used:
- audio input: `$0.005/min`
- audio output: `$0.018/min`
- combined: `$0.023/min = $1.38/hr`

With `$10/month` credits, Gemini covers roughly **7.2 hours/month** at worst-case continuous audio. Real interactive usage can stretch further.

## Recommended architecture

Add a `Live Voice` tab to the existing Telegram Mini App.

Flow:
1. User opens Telegram Mini App.
2. User taps `Live Voice`.
3. Mini App calls Hermes: `POST /api/voice/session`.
4. Hermes authenticates Telegram initData / bearer token.
5. Hermes creates a short-lived voice session and maps it to the active Telegram/Hermes session key.
6. Hermes returns provider config and only ephemeral credentials/tokens.
7. Mini App starts mic capture and connects to provider realtime endpoint or Hermes relay.
8. Provider produces transcript/turn events.
9. Provider calls `hermes_turn(transcript)` or Hermes relay receives the finalized transcript.
10. Hermes runs the normal full agent loop.
11. Hermes returns `spoken_text` plus optional richer `display_text`.
12. Provider speaks the response; Mini App shows transcript, status, and cost.

Do not try to make a native Telegram call clone first. Telegram bots cannot join normal Telegram calls as a human, and Telegram Mini App microphone/WebRTC behavior is inconsistent across clients.

## Suggested API surface

Add the voice routes near the API server / mini app backend, not inside the Telegram adapter first.

Likely endpoints:

- `POST /api/voice/session`
  - Authenticates Telegram initData / bearer token.
  - Creates voice session record.
  - Maps Telegram chat/thread/user to Hermes session key.
  - Returns provider config and ephemeral token.

- `POST /api/voice/end`
  - Ends session, revokes or marks token inactive, flushes metrics.

- `GET /api/voice/status/:id`
  - Optional status for UI/debug.

- `WS /api/voice/events/:id`
  - Optional Hermes-owned event stream to the mini app: transcripts, tool progress, cost, state.

- `POST /api/voice/hermes-turn`
  - Provider tool callback or internal relay endpoint.
  - Receives transcript/final user turn.
  - Calls the normal Hermes agent loop with platform/session metadata.
  - Returns concise spoken response plus optional display text.

## Provider adapter interface

Use an adapter boundary so Gemini can be replaced later.

```python
class VoiceProviderAdapter:
    async def create_session(self, voice_session: VoiceSession) -> ProviderSession: ...
    async def close_session(self, provider_session_id: str) -> None: ...
    async def handle_event(self, event: dict) -> None: ...
```

Initial adapter:
- `GeminiLiveAdapter`

Future adapters:
- `GrokVoiceAdapter`
- `OpenAIRealtimeAdapter`
- optionally Retell/LiveKit/Pipecat if the stack shifts toward hosted or self-hosted media infrastructure.

## Gemini 3.1 implementation notes

Verify current docs before coding, but the April 2026 findings were:
- Model: `gemini-3.1-flash-live-preview`
- Use Gemini Live API / realtime input path.
- Use `thinkingLevel`, not 2.5's `thinkingBudget`.
- Default `thinkingLevel` should probably be `minimal` for latency.
- Use `send_realtime_input` for live updates.
- Function calling is synchronous; do not assume async function calling.
- Server events can contain multiple content parts; process all parts in each event.
- Proactive audio and affective dialogue were not supported in 3.1 at the time of research.

## Hermes turn bridge contract

Input:
- `voice_session_id`
- transcript
- partial/final flag
- user identity
- platform/chat/thread metadata
- provider timing/cost metadata

Processing:
- Ignore partial transcripts for agent turns unless needed for interruption UX.
- For final turns, call the existing session-bound Hermes runner.
- Inject only a short context note if needed: user is speaking via Live Voice; answer concisely for speech unless tools are needed.
- Preserve normal tool use and session history.
- Stream tool progress back to the mini app if available.

Output shape:

```json
{
  "spoken_text": "Short natural answer for TTS.",
  "display_text": "Optional richer text for transcript/UI.",
  "should_speak": true,
  "interruptible": true,
  "metadata": {
    "session_id": "...",
    "provider": "gemini-live",
    "latency_ms": 1234
  }
}
```

## Security and product constraints

- Never expose long-lived provider API keys to the Mini App.
- Prefer ephemeral provider tokens/session secrets.
- Bind sessions to Telegram initData / user id / chat id.
- Expire idle sessions quickly.
- Rate-limit session creation.
- Start with a 10–15 minute hard max duration.
- Add a per-session cost meter and a hard cap.
- Sanitize spoken text so secrets, stack traces, huge tool dumps, and raw URLs are not spoken accidentally.

## Telegram Mini App risks

Known issues from research:
- Telegram Mini Apps are WebViews/iframes, not a guaranteed native mic/call surface.
- iOS Telegram WebView media capture may differ from Safari.
- Android may repeatedly prompt for microphone permission.
- MediaRecorder can produce zero-byte chunks in some Telegram WebViews unless codec/path is chosen carefully.
- Background capture is not safe to promise.

Mitigation:
- Make `Open in browser` a first-class fallback.
- Feature-detect mic/realtime support.
- Keep session starts user-gesture-driven.
- Test on actual iPhone, Android, Telegram Desktop, and normal browser before calling it shipped.

## Preferred MVP architecture after code/doc research

Start with a **server-side Gemini Live relay**, not browser-direct ephemeral tokens.

Flow:

```text
Mini App → Hermes API/WebSocket → Gemini Live WebSocket → Gemini toolCall hermes_turn → Hermes runner bridge → Gemini toolResponse/audio → Mini App
```

Why server-side first:
- No long-lived Google key in the browser.
- Simpler `hermes_turn` bridge and logging.
- Avoids early dependence on Gemini ephemeral-token/session-resumption quirks.
- Keeps Hermes session and voice state in one place.

Move to browser-direct constrained ephemeral tokens only if the relay latency is unacceptable.

## External-first implementation path validated on Mac Studio

For the first serious build, prefer a standalone companion repo over Hermes core edits:

```text
/Users/Kosta/LocalDev/hermes-voice-bridge
```

This proved update-proof and fast to validate. The bridge can run as an external FastAPI service and call Hermes through existing API surfaces while keeping all realtime audio/provider churn outside `~/.hermes/hermes-agent`.

Validated scaffold shape:

```text
src/hermes_voice_bridge/app.py                  FastAPI app, health/session/status/end/ws routes
src/hermes_voice_bridge/config.py               env/settings
src/hermes_voice_bridge/models.py               pydantic session/response models
src/hermes_voice_bridge/sessions.py             SQLite-backed session store
src/hermes_voice_bridge/auth.py                 bearer/session auth helpers
src/hermes_voice_bridge/hermes_client.py        Hermes /v1/chat/completions client + spoken-text cleanup
src/hermes_voice_bridge/cost.py                 Gemini Live cost estimator
src/hermes_voice_bridge/audio.py                PCM helpers
src/hermes_voice_bridge/providers/base.py       provider protocol
src/hermes_voice_bridge/providers/gemini_live.py Gemini Live WebSocket adapter
src/hermes_voice_bridge/static/index.html       browser voice UI
src/hermes_voice_bridge/static/style.css        UI styles
src/hermes_voice_bridge/static/app.js           mic capture, resampling, playback, WS client
```

Security/robustness findings from the implementation pass:
- Create a per-session `client_secret` and include it only in the returned `ws_url` as `?token=...`.
- Validate that token before accepting `WS /voice/ws/{session_id}`.
- Keep `GEMINI_API_KEY` and `HERMES_API_KEY` server-side only; never leak long-lived provider keys to the browser/Mini App.
- Add idle timeout handling and explicit session end/status routes.
- Send cost/session updates back over the WebSocket so the UI can show spend while connected.
- Treat browser/WebView mic QA as a separate gate; passing desktop browser smoke tests is not enough to call Telegram/iPhone/Android shipped.
- Guard `navigator.mediaDevices.getUserMedia()` with a user-visible timeout. Local Chrome/browser automation can leave the page stuck forever at `requesting mic` when the permission prompt is blocked or hidden; the bridge UI should fail after about 15 seconds with a clear “open in Chrome/Safari / allow mic access” message and re-enable Start.
- When exposing the external bridge through the same stable Tailscale Funnel host as the GPT miniapp, add a path route instead of replacing the miniapp root:
  ```bash
  tailscale serve --bg --set-path /voice 8765
  tailscale funnel --bg --set-path /voice 8765
  ```
  This preserves `/ -> 8643` for the miniapp/API server while making `https://macstudio.tailf7342a.ts.net/voice/` proxy to the bridge.
- If the bridge lives under `/voice/`, its static HTML/JS must use relative paths (`static/app.js`, `voice/session`) and `VOICE_BRIDGE_PUBLIC_BASE_URL` must include the `/voice` prefix so returned websocket URLs look like `wss://.../voice/voice/ws/...`.
- Do not make the public bridge unauthenticated just so Telegram can start it. Load Telegram WebApp JS in the bridge UI, send `X-Telegram-Init-Data` to `voice/session`, and let the bridge validate that initData with `TELEGRAM_BOT_TOKEN`; keep the bearer secret fallback for browser/dev use.
- If `POST /voice/session` returns `{detail:"Missing bearer token"}` from inside the GPT Telegram Mini App, check for a bot-token mismatch before chasing frontend headers: the bridge may be validating initData with root `~/.hermes/.env` while the GPT Mini App is signed by `~/.hermes/profiles/gpt/.env`. A synthetic initData probe signed with each token should show GPT-signed data returning 200.

Useful validation commands from the scaffold:

```bash
cd /Users/Kosta/LocalDev/hermes-voice-bridge
python -m pytest
python -m py_compile $(find src -name '*.py')
uvicorn hermes_voice_bridge.app:create_app --factory --host 127.0.0.1 --port 8765
curl -s http://127.0.0.1:8765/health
```

Known good result from the April 2026 build:
- `python -m pytest` passed: 10 tests.
- `py_compile` passed.
- Gemini Live provider smoke connected and returned ready/setupComplete.
- Hermes API smoke returned the expected `voice bridge ok` response.
- Browser page loaded at `http://127.0.0.1:8765/`.
- Initial repo commit: `fa5842c Build external Hermes live voice bridge scaffold`.

Important: if you briefly edit the profile Mini App while exploring UI integration, avoid leaving unrelated profile-local edits behind. Revert those unless the user explicitly wants Mini App integration in that pass.

## Local Hermes implementation map

Use these integration points only if/when Kosta chooses deeper Hermes-native integration after the external bridge proves the device UX:

Use these integration points on Mac Studio:

- API server route glue: `/Users/Kosta/.hermes/hermes-agent/gateway/platforms/api_server.py`
  - Reuse `_validate_telegram_init_data()` and `_check_auth()`.
  - Add routes near existing `/api/...` registrations.
  - Keep provider logic out of this file; it is already large.

- Mini App UI: `/Users/Kosta/.hermes/profiles/gpt/miniapp/index.html`
  - The GPT profile serves this profile-local file, not necessarily shared `~/.hermes/miniapp/index.html`.
  - Existing `headers()` sends `X-Telegram-Init-Data`, `X-Hermes-Session-Id`, and Bearer token; reuse for voice routes.
  - Existing CSP may need `connect-src`/`media-src`/worker updates for voice transport and playback.

- Real Hermes session bridge: `/Users/Kosta/.hermes/hermes-agent/gateway/run.py`
  - Do **not** rely on `APIServerAdapter._create_agent()` for the final design; that creates an `api_server`-platform agent and risks losing Telegram/gateway semantics.
  - Add a runner-level external turn method that reuses `_run_agent()` / normal gateway session machinery.
  - If `APIServerAdapter` cannot access the runner cleanly, pass a runner/external-turn callback into the adapter during registration or create a shared voice bridge service.

Suggested runner method shape:

```python
async def run_external_turn(
    self,
    *,
    source: SessionSource,
    text: str,
    session_id: str | None = None,
    session_key: str | None = None,
    message_type: MessageType = MessageType.TEXT,
    ephemeral_note: str | None = None,
    event_sink: Callable[[dict], None] | None = None,
) -> dict:
    ...
```

- Session identity: `/Users/Kosta/.hermes/hermes-agent/gateway/session.py`
  - Use `SessionSource` as canonical platform/chat/thread/user identity.
  - Beware: Telegram Mini App initData identifies the user but may not include exact chat/topic context. For exact topic continuity, pass signed chat/thread context in the Mini App launch path or map user → active Telegram session.

## New files/modules to create

Prefer a small voice package:

```text
gateway/voice/__init__.py
gateway/voice/models.py
gateway/voice/store.py
gateway/voice/bridge.py
gateway/voice/providers/base.py
gateway/voice/providers/gemini_live.py
```

Suggested responsibilities:
- `models.py`: `VoiceSession`, `ProviderSession`, `VoiceTurnRequest`, `VoiceTurnResponse`, `VoiceProviderCapabilities`, `VoiceEvent`.
- `store.py`: profile-local SQLite or JSONL voice session lifecycle/cost store; prefer SQLite if quick.
- `bridge.py`: spoken text cleanup, event fanout, Hermes turn bridge helpers.
- `providers/base.py`: provider-neutral interface.
- `providers/gemini_live.py`: Gemini setup, WebSocket handling, tool calls, `goAway`, resumption, and event normalization.

Normalize provider events to hide provider grammar:
- `audio.delta`
- `audio.done`
- `transcript.delta`
- `transcript.final`
- `tool.call`
- `tool.cancel`
- `response.done`
- `usage`
- `error`

## Gemini 3.1 docs-fresh implementation details

April 2026 doc checks found:
- Live API is stateful WebSocket. First message must be `setup`; wait for `setupComplete`.
- Server API-key endpoint: `wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1beta.GenerativeService.BidiGenerateContent?key=YOUR_API_KEY`.
- Browser ephemeral token endpoint requires `v1alpha` constrained path: `...BidiGenerateContentConstrained?access_token=...`.
- Client messages have exactly one top-level field: `setup`, `clientContent`, `realtimeInput`, or `toolResponse`.
- Server messages include `setupComplete`, `serverContent`, `toolCall`, `toolCallCancellation`, `goAway`, `sessionResumptionUpdate`, `inputTranscription`, `outputTranscription`, and `usageMetadata`.
- Function response IDs must match Gemini function call IDs.
- Process every `serverContent.modelTurn.parts[]` item; Gemini 3.1 can put multiple content parts in one event.
- If automatic VAD is enabled and mic/audio pauses for more than ~1s, send `audioStreamEnd`; if manual VAD is used, send `activityStart`/`activityEnd` and do not send `audioStreamEnd`.
- Audio-only sessions are about 15 minutes without compression; WebSocket lifetime is around 10 minutes; handle `goAway` and store latest `sessionResumptionUpdate.newHandle` where possible.

## Billing/API key gate

Before coding against Live API, verify the key routing:

```text
API key → Google Cloud project → linked Cloud Billing account → activated Google AI Pro / Developer Program credit
```

Checklist:
1. Open https://aistudio.google.com/app/apikey and identify the exact API key/project for Hermes.
2. Confirm that project is linked to the billing account where the `$10 monthly Gen AI & Cloud credits` were activated.
3. Open https://aistudio.google.com/app/billing and confirm active billing/prepay/postpay status.
4. Set a low project spend cap before testing.
5. Store the key safely and use a single canonical env var: `GEMINI_API_KEY`.
6. Avoid setting both `GEMINI_API_KEY` and `GOOGLE_API_KEY`; Google docs say `GOOGLE_API_KEY` can take precedence.
7. Run one tiny API/Live smoke test and confirm usage appears under the intended project.

## Tests to add

Recommended new tests:

```text
tests/gateway/test_api_server_voice.py
tests/gateway/test_live_voice_bridge.py
tests/gateway/test_voice_session_store.py
```

Cover:
- voice routes reject unauthenticated requests and accept Bearer/Telegram auth.
- session create/end/status lifecycle.
- no long-lived provider secret leaks to frontend.
- voice session binds to `X-Hermes-Session-Id` and user/chat identity.
- final transcript invokes Hermes bridge; partial transcript does not.
- spoken text is sanitized/truncated.
- concurrent turns for same session are queued/rejected/serialized according to chosen policy.
- cost/time accounting and idle expiry.

Relevant existing tests to run after changes:

```bash
python -m py_compile gateway/platforms/api_server.py gateway/run.py
python -m pytest tests/gateway/test_api_server.py tests/gateway/test_api_server_multimodal.py tests/gateway/test_api_server_subscription_usage.py
```

## Native Mini App voice UI integration pattern

Use this when the user says the voice feature feels like an embedded box, iframe, demo app, isolated card, or not first-party inside the Telegram Mini App.

Design direction:
- Treat the external bridge as a service/API layer only; let the GPT Mini App own the UI.
- Remove iframe/container framing from the Mini App Voice tab when possible. The first-party panel should call `/voice/voice/session` directly, open the returned WebSocket, and render controls/transcript inside the existing Mini App shell.
- Reuse the Mini App vocabulary: `--tg-theme-*` variables, `--bg`, `--sec-bg`, `--section-bg`, `--text`, `--hint`, `--btn`, `--accent`, `--border`, Hermes monospace stack, `status-chip`, chat-bubble radii, tab/header layout, and safe-area behavior.
- Avoid separate-demo styling: no standalone hero, visible bridge URL row, cyan/slate palette, glowing static dot, radial page background, max-width centered shell, nested card/iframe, or implementation copy like “Gemini Live transport”.
- Preferred native layout: status/cost chips at top, a compact first-party waveform/voice card that reflects mic/output level, Start/Mute/Stop controls using existing button vocabulary, short Telegram/WebView mic fallback copy, and transcript rows styled like Hermes user/assistant bubbles.
- For waveform design, use product precedents rather than flashy visualizers: Telegram and WhatsApp voice-note bars, Apple Voice Memos' restrained centerline/playhead, and ChatGPT's voice-inside-chat approach. Avoid neon music visualizers, giant assistant orbs, fake equalizers, gradient text, and demo-app chrome.
- A good Hermes waveform pattern is 24–44px tall with ~32–40 rounded bars, a subtle centerline, idle bars using `var(--hint)`/border opacity, listening bars using muted success green, assistant-speaking bars using `var(--accent)`, and error bars using the destructive red. It should adapt through existing `--tg-theme-*` / Hermes CSS vars for light and dark mode.
- If Kosta asks for a more minimal ASCII/TUI direction, prefer a semantic braille signal trace over a generic equalizer. Treat braille density as amplitude, opacity as recency, and horizontal position as time: listening injects irregular user energy from the left into a short-lived memory trace; thinking scans or pulses across held trace memory; assistant speaking becomes smoother phase-aligned waves; interrupt/error briefly collapses into sparse broken glyphs before stabilizing. For front-end design exploration, use Claude Code with `claude-opus-4-7 --effort high` by default; Codex is fine for the implementation pass if Kosta explicitly asks for it. Review artifacts may show all states at once, but the product UI should show one live waveform that switches based on `voiceState`/RMS/model activity. Avoid a too-flat trace: use a multi-row braille rasterizer with real vertical gain, e.g. about 16 dot rows -> 4 braille text rows inside a compact ~72px component; active listening/speaking should visibly occupy the y-axis at mobile screenshot size, while idle stays visible but quieter. Implement with pre-created row elements and `requestAnimationFrame`, updating a handful of `<pre>` row `textContent` values per frame; respect `prefers-reduced-motion` by slowing/noise-gating rather than freezing status feedback. Validated artifacts from the April 2026 pass: `/Users/Kosta/LocalDev/hermes-artifacts/voice-braille-signal-lab-opus.html` and smoke screenshot `/Users/Kosta/LocalDev/hermes-artifacts/voice-miniapp-braille-implemented.png`. The production GPT Mini App implementation uses markers `VoiceSignalTrace`, `braille-trace`, `VOICE_TRACE_H = 16`, and no `.voice-wavebar` remnants.
- Drive the waveform with real mic/output RMS when available, but avoid two sources fighting: if assistant audio is speaking, let output level own the waveform and use mic RMS only for barge-in detection. Add a very low-amplitude idle breathing loop for `idle`, `requesting mic`, and `connecting` so the component does not look frozen before audio starts.
- Motion should convey state only: listening/speaking/muted/error waveform states, transcript streaming cursor, button press/haptic feedback, barge-in interrupt flash. Keep transitions around 150–250 ms and animate transforms/opacity, not layout.
- Add barge-in behavior if audio playback is buffered: measure mic RMS during assistant playback, stop active audio sources, reset playback queue, send `{type:'control.interrupt'}`, and show a brief interrupt state.
- Keep `/voice/` fallback page available for Safari/Chrome, but restyle it to inherit Telegram theme tokens and compact first-party layout so fallback does not look like a different app.

Implementation notes from the Mac Studio pass:
- GPT Mini App path: `/Users/Kosta/.hermes/profiles/gpt/miniapp/index.html`.
- External bridge fallback files: `/Users/Kosta/LocalDev/hermes-voice-bridge/src/hermes_voice_bridge/static/index.html`, `style.css`, `app.js`.
- If the native Mini App opens a `wss://macstudio.tailf7342a.ts.net/...` voice socket, update CSP `connect-src` for that host.
- Existing Mini App helpers `headers()` and `fetchWithTimeout()` can be reused so Telegram initData and `X-Hermes-Session-Id` stay consistent with the rest of the shell.
- After static Mini App changes, verify the served public file, not just disk, and bump the Telegram menu-button URL with `?v=$(date +%s)` to defeat Telegram WebView cache.

Verification for native voice UI changes:
```bash
# Extract and syntax-check the single-file Mini App script.
python3 - <<'PY'
from pathlib import Path
s=Path('/Users/Kosta/.hermes/profiles/gpt/miniapp/index.html').read_text()
start=s.index('<script>')+len('<script>')
end=s.index('</script>', start)
Path('/tmp/miniapp-inline.js').write_text(s[start:end])
PY
node --check /tmp/miniapp-inline.js

# Verify the phone-facing public route has native voice UI and no iframe shell.
curl -s 'https://macstudio.tailf7342a.ts.net/miniapp/index.html?v=test' -o /tmp/served-miniapp.html
python3 - <<'PY'
from pathlib import Path
s=Path('/tmp/served-miniapp.html').read_text()
print('native_voice=', all(x in s for x in ['voice-root','voiceStart()','/voice/voice/session']))
print('iframe_removed=', 'voice-frame' not in s)
print('voice_wss_csp=', 'wss://macstudio.tailf7342a.ts.net' in s)
PY

# Keep backend bridge verification too.
cd /Users/Kosta/LocalDev/hermes-voice-bridge
python -m pytest
python -m py_compile $(find src -name '*.py')
```

## MVP sequence

1. Verify AI Studio/Gemini API project and key use the activated credit-backed billing account.
2. Build a minimal Gemini Live smoke test outside Telegram.
3. Create `gateway/voice/*` models/store/provider skeleton.
4. Add authenticated `/api/voice/session`, `/api/voice/end`, and status route stubs with fake provider.
5. Add runner-level external Hermes turn bridge in `gateway/run.py`.
6. Wire `/api/voice/hermes-turn` to the real Hermes session path.
7. Implement `GeminiLiveAdapter` server-side relay and event normalization.
8. Add a native `Live Voice` tab to the GPT profile Mini App.
9. Wire one complete turn: mic → Hermes relay/Gemini → transcript/tool callback → Hermes → spoken response.
10. Add transcript/status/cost UI in the Mini App shell, not an iframe, unless explicitly doing a temporary fallback.
11. Test in normal browser first, then Telegram Desktop, then iPhone/Android.
12. Only after successful manual testing, polish barge-in/interruption and fallback behavior.

## Existing artifacts from planning passes

Planning artifacts were written here:
- `/Users/Kosta/LocalDev/hermes-live-voice-bridge-spec.md`
- `/Users/Kosta/LocalDev/hermes-live-voice-bridge-architecture.html`
- `/Users/Kosta/LocalDev/hermes-artifacts/hermes-live-voice-bridge-architecture.png`
- `/Users/Kosta/LocalDev/hermes-live-voice-implementation-plan.md`

Because `~/LocalDev` is Syncthing-synced on this machine, be careful with destructive changes to those files.
