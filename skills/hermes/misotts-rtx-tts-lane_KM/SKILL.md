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
- Default TTS provider remains `kokoro` in both global and GPT profile config.
- Mac wrapper: `~/.hermes/bin/hermes-misotts-rtx.sh`.
- GamingPC helper: `gamingpc misotts start|status|test|stop`.
- GamingPC service path: `C:\Users\kosta\LocalAI\MisoTTS\serve_misotts_hermes.py`.
- Known-good GamingPC access: `ssh-gamingpc` using the 1Password “Mac mini SSH Key” temp key with `IdentityAgent=none IdentitiesOnly=yes`.
- Cold startup observed locally: about 90–100s to ready; latest measured `load_seconds` around 98s.
- Warm generation observed locally: roughly 4.5x realtime on a normal 8s answer; quality is better than Kokoro, but latency and VRAM cost are high.
- VRAM use after load can sit around 22–24 GB, so never leave it resident indefinitely by accident.

## Voice-note prewarm behavior

Hermes repo now has a voice-message prewarm hook in `gateway/platforms/base.py`:

- Trigger: incoming `MessageType.VOICE` where auto-TTS is enabled for that chat.
- Action: runs `~/.hermes/bin/hermes-misotts-rtx-start.sh` in the background immediately, overlapping Miso cold-load with STT, reasoning, and tool work.
- It never blocks message processing, never changes the selected TTS provider, and keeps Kokoro fallback intact.
- Default idle TTL: `HERMES_MISOTTS_PREWARM_TTL_SECONDS=1800` (30 minutes), after which it runs `~/.hermes/bin/hermes-misotts-rtx-stop.sh`.
- Disable with `HERMES_MISOTTS_PREWARM_ON_VOICE=0`.

Do not restart Telegram/Discord gateway from a Telegram-controlled session. If the hook was just changed, report that a safe gateway reload is needed before live messages use it.

## Voices and expressiveness

Official Miso docs do not expose a named voice catalog in the local open-source repo. The current local API supports:

- `speaker`: integer 0–9. These are speaker tokens, not documented named voices.
- `temperature`: default 0.9, clamped 0.2–1.5.
- `topk`: default 50, clamped 1–100.
- `profile`: optional prompt-audio context profile backed by `voice_profiles/<id>/reference.wav` + `transcript.txt` on GamingPC. This is how Miso gets actually different voices; `speaker 0–9` alone is not a voice catalog.
- `context`: upstream supports prompt-audio continuation/voice cloning through `Segment`; Kosta's service now exposes it through the safe profile allowlist, not arbitrary paths.

The official website preview exposes three UX presets: `friend`, `teacher`, and `voiceover`, but the GitHub/Python API currently documents only `speaker`, optional audio context, `temperature`, and `topk`. Treat the website preset names as style directions, not local API voice IDs.

Current profile status: three Moss/reference profiles are enabled: `samantha-her-a`, `hernandez-stroud-rikers-ny1`, and `emily-blunt-narrative`. `hermes_narrator` was removed from the Miso lane because the reference was not useful. Miso needs both `reference.wav` and transcript text for each prompt-audio context profile.

Recommended style directions for Hermes replies:

- Default Kosta assistant: friendly conversational / `friend` style. Short, warm, lightly expressive, not theatrical.
- Explainers: `teacher` style. Clear, paced, a little slower, with commas and sentence breaks.
- Announcements or longer summaries: `voiceover` style. More polished, but avoid hype.

## Prompting / text shaping

Miso responds best to natural spoken prose, not markdown dumps.

Before TTS:

- Keep the text short: ideally 1–4 spoken sentences.
- Use punctuation to control rhythm: commas for small pauses, periods for clean stops, line breaks only when intentional.
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

- `speaker=0`: current safest default for the base Miso voice; unknown named identity.
- `profile=samantha-her-a`: enabled voice-clone profile for a warmer assistant-style voice.
- `profile=emily-blunt-narrative`: enabled narrative voice profile.
- `profile=hernandez-stroud-rikers-ny1`: enabled authorized profile for Hernandez Stroud PowerPoint voice-over help; do not use for deceptive impersonation.
- `temperature=0.8–0.9`: stable natural speech.
- `temperature=1.0–1.1`: more expressive, may get less predictable.
- `topk=40–60`: default range; lower is steadier, higher is more varied.
- `max_audio_length_ms=10000–12000`: enough for a short answer without hard clipping.

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
