# Hermes Mini App live voice diagnostics — 2026-05-06

## Where it runs

- Bridge repo: `/Users/Kosta/LocalDev/hermes-voice-bridge`
- Live service: LaunchDaemon `system/com.kosta.hermes-voice-bridge-system`
- Local port: `127.0.0.1:8765`
- Public route used by Mini App: `https://macstudio.tailf7342a.ts.net/voice`
- Logs:
  - `/Users/Kosta/.hermes/voice-bridge/system-launchd.log`
  - `/Users/Kosta/.hermes/voice-bridge/system-launchd.err.log`
- Session DB: `/Users/Kosta/.hermes/voice-bridge/voice_sessions.sqlite3`
- Mini App source: `/Users/Kosta/.config/hermes-state/miniapp/index.html`

## Current architecture

The Mini App captures mic audio in the Telegram WebView, creates a bridge session with `POST /voice/session`, then opens `WebSocket /voice/ws/{session_id}?token=...`.

The bridge connects to Gemini Live using `gemini-3.1-flash-live-preview`. Gemini Live is instructed to stay as the low-latency voice front-end and call the single tool `hermes_turn` for substantive requests. `hermes_turn` forwards the transcript to Hermes GPT via `http://127.0.0.1:8643/v1/chat/completions`, so tool use, memory, web/files, and better text-model reasoning happen in Hermes rather than inside the small live voice model.

## Crash fixed / diagnostics added

A crash after a few seconds showed up as:

```text
sqlite3.OperationalError: unable to open database file
```

It happened while the WebSocket loop was saving session audio accounting. The fix in `VoiceSessionStore` reasserts the DB parent directory and schema on every connection so transient directory loss does not tear down an active voice call.

Diagnostics now log lifecycle events with `voice.*` lines through `uvicorn.error`, including:

- `voice.session_created`
- `voice.ws_open`
- `voice.provider_connected`
- `voice.client.ws_open`, `voice.client.ws_close`, `voice.client.ws_error`, `voice.client.server_error`
- `voice.hermes_turn_completed`
- `voice.store_save_failed` / `voice.store_end_failed` with DB path
- `voice.session_ended` with input/output seconds and estimated cost

The Mini App also reports frontend WebSocket close/error/message-parse/window-error events to `POST /voice/client-log`.

## Verification commands

From `/Users/Kosta/LocalDev/hermes-voice-bridge`:

```bash
source .venv/bin/activate
python -m pytest
python -m py_compile $(python - <<'PY'
from pathlib import Path
print(' '.join(str(p) for p in Path('src').rglob('*.py')))
PY
)
```

Check live bridge health:

```bash
curl -sS --max-time 8 http://127.0.0.1:8765/health
```

Restart without sudo when `launchctl kickstart system/...` is not permitted:

```bash
pid=$(/usr/sbin/lsof -tiTCP:8765 -sTCP:LISTEN -nP 2>/dev/null | head -1)
[ -n "$pid" ] && kill "$pid"
# launchd KeepAlive restarts it
curl -sS --max-time 8 http://127.0.0.1:8765/health
```

Client-log smoke without printing secrets:

```bash
python - <<'PY'
from pathlib import Path
from urllib import request
secret = None
for line in Path('.env').read_text().splitlines():
    if line.startswith('VOICE_BRIDGE_SECRET='):
        secret = line.split('=', 1)[1]
body = b'{"event":"local_smoke","session_id":"voice_smoke","message":"client log smoke"}'
req = request.Request('http://127.0.0.1:8765/voice/client-log', data=body, method='POST', headers={'Authorization': f'Bearer {secret}', 'Content-Type': 'application/json'})
with request.urlopen(req, timeout=5) as r:
    print(r.status, r.read().decode())
PY

tail -n 80 /Users/Kosta/.hermes/voice-bridge/system-launchd.err.log | grep 'voice.client.local_smoke'
```
