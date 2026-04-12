---
name: moss-samantha-voiceover
description: Generate a short spoken-style voiceover from a normal answer using the local MOSS CLI with Samantha as the default voice. Use when the user wants a reply turned into audio, a voice memo, a spoken summary, or asks for Samantha or MOSS specifically.
targets:
  - hermes-default
  - hermes-gpt
---

# MOSS Samantha Voiceover

Use this when the user wants a response converted into a spoken-style script and rendered as audio with the local MOSS pipeline.

## What this skill is for
This is an orchestrator-facing skill. Use it to:
- rewrite the answer into a listenable voiceover script
- keep the wording TTS-friendly
- generate audio with local `~/LocalDev/voice/moss/bin/moss`
- default to Samantha unless the user explicitly asks for another voice

## Default voice
Use `samantha-her-a` by default.

If the local MOSS wrapper already defaults to Samantha, you can omit `--voice`.
If you need to be explicit, pass:
- `--voice samantha-her-a`

## Spoken-style rewrite rules
Before rendering audio, rewrite the text for listening:
- use plain prose, not bullet lists unless the user truly wants list cadence
- remove markdown formatting
- avoid ellipses and odd Unicode punctuation
- keep sentences relatively short and natural to say aloud
- spell out or smooth awkward symbols, percentages, file paths, and code-ish fragments when needed
- prefer short transitions like "Here’s the short version" or "The main point is"
- do not add new facts

## Good output shape
Aim for:
1. quick framing sentence
2. core explanation in plain spoken language
3. brief closing sentence

## Rendering steps
1. Draft a clean spoken-style script in a temp text file.
2. Generate audio with MOSS.
3. Convert to `.ogg` for Telegram voice-message delivery when needed.
4. Return or send the final media path.

## Commands
Basic local render:
```bash
~/LocalDev/voice/moss/bin/moss say "<text>" --out /tmp/voiceover.wav
```

Explicit Samantha render:
```bash
~/LocalDev/voice/moss/bin/moss say "<text>" --voice samantha-her-a --out /tmp/voiceover.wav
```

Convert to Telegram-friendly voice note:
```bash
ffmpeg -y -i /tmp/voiceover.wav -c:a libopus -b:a 48k /tmp/voiceover.ogg
```

## Verification
After generation, verify:
- output file exists
- duration is non-zero
- if sending to Telegram, prefer `.ogg`

## Notes
- Treat MOSS and Samantha voice work as Studio-centric unless the user asks to replicate it elsewhere.
- If the user wants a longer document transformed for TTS, also read `document-to-tts-transcript` first.
