---
name: misotts-rtx-tts-lane_KM
description: Operate and improve Kosta's GamingPC MisoTTS RTX 4090 lane for Hermes voice replies: voice-note prewarm, Kokoro fallback, startup/TTL, speed/quality benchmarks, speaker/temperature/topk knobs, prompting for expressive English speech, and safe GPU coexistence. Use when Kosta asks about MisoTTS, RTX TTS, GamingPC TTS, voice-note prewarm, expressive TTS prompting, Miso voices, or improving Hermes voice replies.
metadata:
  targets:
    - hermes-default
    - hermes-gpt
    - claude-hermes
  hermes:
    command_priority: 438
---
# MisoTTS RTX TTS Lane

Use this for Kosta's opt-in high-quality TTS lane on the GamingPC RTX 4090. Kokoro remains the safe default/fallback unless Kosta explicitly switches providers.

## Current local lane

- Hermes provider name: `misotts_rtx`.
- Provider output format is `ogg` in GPT and global config so Telegram voice notes use the wrapper’s own 64k Opus encode instead of a generic post-conversion path.
- Default TTS provider remains `kokoro` in both global and GPT profile config.
- Mac wrapper: `~/.hermes/bin/hermes-misotts-rtx.sh`.
- GamingPC helper: `gamingpc misotts start|status|test|stop`.
- GamingPC service path: `C:\Users\kosta\LocalAI\MisoTTS\serve_misotts_hermes.py`.
- Known-good GamingPC access: `ssh-gamingpc` using the 1Password “Mac mini SSH Key” temp key with `IdentityAgent=none IdentitiesOnly=yes`.
- Cold startup observed locally: about 90–100s to ready; latest measured `load_seconds` around 98s.
- Warm generation observed locally: roughly 4.5x realtime. Keep Miso requests short; the wrapper now follows upstream’s short single-pass pattern instead of stitching independent chunks.
- VRAM use after load can sit around 22–24 GB, so never leave it resident indefinitely by accident.
- Miso is not a drop-in long-form narrator. Official docs show short `generator.generate(..., max_audio_length_ms=10_000)` calls and expose a 2,048-token max sequence length; long replies should use Kokoro or another long-form lane unless explicitly testing chunking.

## Voice-note prewarm behavior

Hermes repo now has a voice-message prewarm hook in `gateway/platforms/base.py`:

- Trigger: incoming `MessageType.VOICE` where auto-TTS is enabled for that chat.
- Action: runs `~/.hermes/bin/hermes-misotts-rtx-start.sh` in the background immediately, overlapping Miso cold-load with STT, reasoning, and tool work.
- It never blocks message processing, never changes the selected TTS provider, and keeps Kokoro fallback intact.
- Default idle TTL: `HERMES_MISOTTS_PREWARM_TTL_SECONDS=1800` (30 minutes), after which it runs `~/.hermes/bin/hermes-misotts-rtx-stop.sh`.
- Disable with `HERMES_MISOTTS_PREWARM_ON_VOICE=0`.

## Wait-for-ready (no premature Kokoro fallback)

As of the wrapper rework, `hermes-misotts-rtx.sh` no longer falls back to Kokoro the instant `/health` reports not-ready. It polls and waits for the model to finish loading, so a cold/loading model produces a real Miso voice note instead of a Kokoro one (just later). Behavior:

- If `/health` is reachable but `ready:false` (mid-load), it keeps polling until ready, up to `HERMES_MISOTTS_READY_WAIT_SECONDS` (default 150).
- It also fires the loader itself once (idempotent `hermes-misotts-rtx-start.sh`) if the model isn't up — so it self-heals even outside the voice-note prewarm path. Disable with `HERMES_MISOTTS_AUTO_START=0`.
- If the endpoint is genuinely unreachable (box off / service never answers) for `HERMES_MISOTTS_UNREACHABLE_GRACE_SECONDS` (default 25), it gives up early and falls back to Kokoro rather than burning the full wait.
- Poll cadence: `HERMES_MISOTTS_READY_POLL_SECONDS` (default 3).
- Fallback still respects `HERMES_MISOTTS_DISABLE_FALLBACK` and the explicit-voice-profile no-fallback rule.

Net effect: loading is treated as "wait", off is treated as "fall back". The trade is latency — the first voice note after a cold start can take ~90-100s while Miso loads, instead of returning fast in Kokoro.

Do not restart Telegram/Discord gateway from a Telegram-controlled session. If the hook was just changed, report that a safe gateway reload is needed before live messages use it.

## Voices and expressiveness

Official Miso docs do not expose a named voice catalog in the local open-source repo. The current local API supports:

- `speaker`: integer 0–9. These are speaker tokens, not documented named voices.
- `temperature`: default 0.9, clamped 0.2–1.5.
- `topk`: default 50, clamped 1–100.
- `profile`: optional prompt-audio context profile backed by `voice_profiles/<id>/reference.wav` + `transcript.txt` on GamingPC. This is how Miso gets actually different voices; `speaker 0–9` alone is not a voice catalog.
- `context`: upstream supports prompt-audio continuation/voice cloning through `Segment`; Kosta's service now exposes it through the safe profile allowlist, not arbitrary paths.

The official website preview exposes three UX presets: `friend`, `teacher`, and `voiceover`, but the GitHub/Python API currently documents only `speaker`, optional audio context, `temperature`, and `topk`. Treat the website preset names as style directions, not local API voice IDs.

Default voice policy: use the base voice Miso ships with (`voice: default`, `speaker=0`, no `profile`) unless Kosta explicitly asks to test a prompt-audio profile. The enabled reference profiles are experimental only and should not be used for normal Hermes replies.

Recommended style direction for Hermes replies: plain conversational base voice. Short, clear, lightly warm, not theatrical. Do not use website preset names like `friend`, `teacher`, or `voiceover` as local voice IDs; the GitHub/Python API documents only `speaker`, optional audio context, `temperature`, and `topk`.

## Prompting / text shaping

Miso responds best to natural spoken prose, not markdown dumps.

Before TTS:

- Keep the text short: ideally 1–4 spoken sentences.
- Use punctuation to control rhythm: short periods are more reliable than commas for Miso. Avoid colon/list syntax like “keep this simple: warm the model, use the profile…” because Miso can read it as a run-on sentence.
- Keep generation short. The Mac wrapper defaults to one single-pass upstream-style call: about 180 characters max, `max_audio_length_ms=10000`, and 96k Opus output for Telegram voice notes. Chunking is opt-in with `HERMES_MISOTTS_ENABLE_CHUNKING=1` because stitched chunks sounded worse.
- Avoid tables, code blocks, raw paths, long command output, URLs, and bullet inventories in voice output.
- Spell acronyms or add spaces when pronunciation matters: `G P U`, `T T S`, `S S H`, `A P I`.
- Convert file paths into speakable phrasing when possible: say “the Hermes config file” instead of `/Users/Kosta/.hermes/config.yaml`.
- For emotion, write the emotion into the language itself rather than bracket tags: “Yeah, that’s annoying — the useful fix is…” works better than `[frustrated]`.
- For emphasis, use normal wording and punctuation, not markdown bold.

Good voice text example:

```text
Yeah, that idea is exactly right. I can start warming Miso as soon as your voice note lands, so by the time I finish the actual work, the voice model is probably already loaded.
```

Bad voice text example:

```text
## Status
- provider: misotts_rtx
- path: /Users/Kosta/.hermes/bin/hermes-misotts-rtx.sh
- command: gamingpc misotts start
```

## Current best knobs

Use these as starting points, then benchmark by ear:

- `speaker=0` / `voice=default`: use the base Miso voice that ships with the model. This is the normal lane.
- Prompt-audio profiles such as `samantha-her-a`, `emily-blunt-narrative`, and `hernandez-stroud-rikers-ny1` are experimental; only use them when Kosta explicitly asks to test that profile.
- `temperature=0.8–0.9`: stable natural speech.
- `temperature=1.0–1.1`: more expressive, may get less predictable.
- `topk=40–60`: default range; lower is steadier, higher is more varied.
- `max_audio_length_ms=10000`: upstream example default for short speech; pair with the 180-character cap so endings do not clip.
- `HERMES_MISOTTS_OPUS_BITRATE=96k`: current Telegram voice-note default. Lower bitrates made already-rough Miso samples sound worse.

Do not claim we have ten real “voices” just because `speaker` is clamped 0–9. Say we have ten speaker IDs available to test, but no official names.

## Verification checklist

For code/config changes:

```bash
bash -n ~/.hermes/bin/hermes-misotts-rtx*.sh ~/.local/bin/gamingpc ~/.local/bin/ssh-gamingpc
python -m pytest tests/gateway/test_voice_command.py tests/tools/test_tts_command_providers.py tests/tools/test_tts_opus_routing.py -q
```

For live lane checks:

```bash
gamingpc misotts status
gamingpc misotts start
gamingpc misotts test
```

For benchmarking, disable fallback so Kokoro cannot mask RTX failure:

```bash
HERMES_MISOTTS_DISABLE_FALLBACK=1 ~/.hermes/bin/hermes-misotts-rtx.sh input.txt output.ogg
```

If fallback is intentionally enabled, report whether the artifact came from RTX or Kokoro.
