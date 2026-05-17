# Archived skill: hermes-voice-pipeline-audit

Original path: `/Users/Kosta/.hermes/profiles/gpt/skills/hermes/hermes-voice-pipeline-audit`
Absorbed into umbrella: `hermes-provider-media-configuration` on 2026-04-29.

---

---
name: hermes-voice-pipeline-audit
description: Audit Hermes voice-mode speech detection, STT provider resolution, and background-noise sensitivity on the local machine. Use when voice feels too sensitive, clicks/keyboard noise are being treated as speech, or there is confusion about whether Hermes is using Whisper, Parakeet MLX, or some smarter VAD/noise rejection layer.
---

# Hermes Voice Pipeline Audit

Use this when the user says Hermes is hearing too much background noise, stopping/starting badly, or seems to be using the wrong speech recognizer.

## What this audit is for

This workflow answers four separate questions that users often blur together:

1. What STT provider is actually live right now?
2. What gate decides whether audio counts as speech?
- Discord/Telegram voice notes using the same gate as CLI voice mode?
4. Does Hermes have true live voice-channel or phone-call style transport, versus only voice-note transcription?
5. Are config knobs present but not actually wired into live code?

## Steps

1. Read the live config first.
   - Check `~/.hermes/config.yaml`.
   - Pull these sections specifically:
     - `stt`
     - `voice`
   - Also inspect profile configs if the user may be running a named profile:
     - `~/.hermes/profiles/*/config.yaml`

2. Resolve the real STT path instead of trusting labels.
   - Inspect `~/.hermes/hermes-agent/tools/transcription_tools.py`.
   - Verify:
     - provider resolution in `_get_provider()`
     - local-command handling in `_transcribe_local_command()`
     - dispatch in `transcribe_audio()`
   - If `stt.provider: local_command`, also check `HERMES_LOCAL_STT_COMMAND` in the live environment.

3. If local_command is active, inspect the wrapper script.
   - Read the file referenced by `HERMES_LOCAL_STT_COMMAND`.
   - Confirm whether it is a real Parakeet/MLX path or just a Whisper CLI wrapper.
   - Check what arguments it actually forwards. In particular, look for whether it passes tuning controls like:
     - `--frame-threshold`
     - `--chunk-duration`
     - prompt/context parameters
   - Do not assume those controls are in effect just because the backend CLI supports them.

4. Inspect the speech detection layer for CLI voice mode.
   - Read `~/.hermes/hermes-agent/tools/voice_mode.py`.
   - Confirm whether the gate is:
     - fixed RMS threshold
     - silence timer
     - minimum speech duration
     - dip tolerance / hysteresis
   - Read `~/.hermes/hermes-agent/cli.py` to verify which config values are copied into the recorder at runtime.

5. Check docs and defaults, but treat code as source of truth.
   - Useful files:
     - `website/docs/guides/use-voice-mode-with-hermes.md`
     - `website/docs/user-guide/features/voice-mode.md`
     - `hermes_cli/config.py`
   - Use docs to explain behavior in plain English, not to prove the live path.

6. Distinguish CLI voice mode from gateway voice messages.
   - Inspect `gateway/run.py` and any relevant platform adapter.
   - Verify whether Telegram/Discord uploaded voice notes are pre-gated by the same silence detector or just downloaded and sent straight to STT.
   - This distinction matters: users often think one “voice system” exists when there are really multiple paths.

7. If the question is about OpenAI Realtime / phone-call-style voice, check for live voice transports separately.
   - Search for `voice channel`, `/voice channel`, `join_voice_channel`, `VoiceReceiver`, `Twilio`, `Realtime`, `WebRTC`, and `phone`.
   - In current Hermes, Discord live voice channel support may exist even if phone/Twilio/OpenAI-Realtime transport does not.
   - Confirm whether live voice input is routed back into the normal gateway message pipeline and full agent loop, not a limited assistant wrapper.

8. Treat config-only knobs skeptically.
   - Search the repo for settings such as:
     - `barge_in_*`
     - `busy_ambient_*`
   - If they exist in config but not in the live source tree, say so plainly.
   - Also search archived patches/plans if needed to determine whether the feature was planned or partially landed before disappearing.

## What to report back

Lead with the actual behavior, not the file tour.

Good structure:
- actual STT backend in use
- actual speech/noise gate in use
- whether smart/adaptive noise rejection is really present
- whether messaging voice notes use the same path
- whether live voice-channel or phone-call-style voice exists, and which platforms support it
- likely cause of oversensitivity
- best next knob/code fix

## Known findings worth remembering

On this Mac Studio setup, a real audit found:
- Hermes was using `stt.provider: local_command`
- `HERMES_LOCAL_STT_COMMAND` pointed at `~/.hermes/scripts/parakeet_mlx_stt.py`
- that wrapper called `mlx_audio.stt.generate` with `mlx-community/parakeet-tdt-0.6b-v3`
- CLI voice-mode detection was originally basically a fixed RMS gate plus silence timer (`silence_threshold`, `silence_duration`) with minimum speech confirmation in `tools/voice_mode.py`
- that gate was later tightened to require speech to beat both the base threshold and an adaptive ambient-noise floor, with explicit knobs for `min_speech_duration`, `max_dip_tolerance`, `adaptive_threshold_margin`, `adaptive_threshold_multiplier`, and `noise_floor_smoothing`
- after changing live voice gating, preserve it in a top-level replay artifact under `~/.hermes/patches/` before considering the work durable across `hermes update`
- the Parakeet wrapper did not forward extra MLX tuning controls like `--frame-threshold`
- `barge_in_*` and `busy_ambient_*` existed in config but were not found wired into the current live source tree during that audit
- `voice.max_recording_seconds` was previously config-only, but is now enforced in CLI voice mode by a watchdog in `cli.py` that hard-stops overlong recordings even if ongoing speech/noise prevents silence auto-stop
- Local TTS assets may exist and `tts.provider` may be set to `kokoro`, but that does **not** prove Kokoro is live in Hermes. In one real audit, `tools/tts_tool.py` had no Kokoro branch, so unknown provider `kokoro` fell through to the default Edge TTS path while still returning JSON that claimed `provider: "kokoro"`.
- That Kokoro mismatch was later fixed in the live code, and the docs/config comments were refreshed so the visible TTS provider matrix again matches live support: Edge, ElevenLabs, OpenAI, MiniMax, Kokoro, and NeuTTS.
- Hermes has a Discord live voice channel path in `gateway/run.py` and `gateway/platforms/discord.py`: `/voice channel` joins the user's current Discord voice channel, `VoiceReceiver` captures/decodes audio, STT transcribes utterances, and `_handle_voice_channel_input()` creates a synthetic gateway `MessageEvent` that goes through the normal full agent pipeline with spoken replies. This is different from Telegram/Discord voice notes and different from a Twilio/OpenAI-Realtime phone-call transport.
- As of the observed Mac Studio checkout, Hermes did **not** show a true phone-call/OpenAI-Realtime/Twilio voice transport in the local repo search, even though the full-agent voice-channel plumbing exists for Discord.

## Pitfalls

- Do not claim “Whisper is active” just because `stt.openai.model: whisper-1` appears in config. Provider resolution may never use it.
- Do not confuse STT accuracy with voice-activity detection. They are separate stages.
- Do not assume Discord/Telegram voice notes benefit from the CLI recorder’s silence logic.
- Do not assume a setting is live just because it is present in `config.yaml`.
- If the user says “smart noise rejection,” verify in code. Memory of a prior setup is often partially right but attached to the wrong path.

## Verification checklist

Before finishing, verify all of these from live files or runtime:
- resolved provider
- live command/environment if using local_command
- actual recorder threshold/duration logic
- whether gateway voice notes bypass CLI silence detection
- whether suspected config knobs are actually referenced in live code
