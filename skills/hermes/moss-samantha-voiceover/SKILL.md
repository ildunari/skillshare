---
name: moss-samantha-voiceover
description: Generate a short spoken-style voiceover from a normal answer using the local MOSS CLI with Samantha as the default voice. Use whenever the user asks for Samantha, MOSS TTS, a voice memo, spoken summary, Telegram voice note, or non-English Samantha narration; includes current local flags for speed, duration budgeting, Hebrew/multilingual quality, and verification.
targets:
  - hermes-default
  - hermes-gpt
---

# MOSS Samantha Voiceover

Use this when the user wants a response converted into a spoken-style script and rendered as audio with the local MOSS pipeline.

## Default voice
Use `samantha-her-a` by default. The local wrapper already defaults to Samantha, but be explicit when quality matters:

```bash
~/LocalDev/voice/moss/bin/moss say "<text>" --voice samantha-her-a --out /tmp/voiceover.wav
```

## Spoken-style rewrite rules
Before rendering audio, rewrite the text for listening:
- use plain prose, not bullet lists unless the user truly wants list cadence
- remove markdown formatting
- avoid ellipses and unusual punctuation that TTS may read badly
- keep sentences relatively short and natural to say aloud
- spell out or smooth awkward symbols, percentages, file paths, and code-ish fragments
- do not add new facts

For Hebrew, write idiomatic Hebrew directly. Avoid English phrase order translated word-for-word. Prefer natural phrasing such as `הנה עדכון קצר מהיום` and `לפי רויטרס`. Use simple punctuation and straight apostrophes for transliterated names, e.g. `צ'ארלס`.

## Current best command for short Telegram memos

Use explicit language and the short-memo preset. Add `--seconds` when the user gave a target length.

```bash
~/LocalDev/voice/moss/bin/moss say "<text>" \
  --lang he \
  --voice samantha-her-a \
  --fast \
  --seconds 45 \
  --out /tmp/voiceover.wav
```

Then convert to Telegram-friendly Opus:

```bash
ffmpeg -y -i /tmp/voiceover.wav -c:a libopus -b:a 48k /tmp/voiceover.ogg
```

## Multilingual / Hebrew notes

- Always pass `--lang <code>` for non-English. Hebrew is `--lang he`.
- Samantha is an English reference voice. MOSS can apply the timbre to Hebrew, but accent/pronunciation may be weaker than the written Hebrew.
- The active Samantha profile has a saved transcript at `~/LocalDev/voice/moss/voices/samantha-her-a/reference.txt`, copied from the canonical reference library. Do not assume using it improves short memos.
- The local MLX MOSS path can emit the reference transcript/prefix as part of the output when `--ref-text`, `--use-ref-text`, or continuation mode is used. For normal short memos, prefer plain clone mode: `--voice samantha-her-a` without reference text.
- Treat `--mode continuation`, `--mode continuation-clone`, `--ref-text`, and `--use-ref-text` as experimental diagnostics, not the default user-facing path.

## Performance notes

- Local MOSS generation can look stuck in Telegram because the CLI does not stream progress.
- Cold process startup is a big part of short-clip latency. A 4-second Hebrew smoke clip can take ~24 seconds wall time even though longer clips run faster than live.
- Use `--fast` and `--seconds` for short memos. On the Mac Studio, a Hebrew Samantha memo budgeted at 45 seconds generated 42.4 seconds of audio in 27.8 seconds, RTF about 0.65.
- Avoid uncapped non-English short clips. They may run to the token budget and produce ~90 seconds of audio.
- The CLI may print `Voice: None` even when Samantha is used; the wrapper passes Samantha as `--ref_audio`, so verify via the wrapper command/output rather than that line.

## Rendering steps

1. Draft a clean spoken-style script in a temp text file if the text is more than one sentence.
2. Generate with `moss say`, passing `--lang` and usually `--fast --seconds <target>`.
3. Convert to `.ogg` for Telegram voice-message delivery.
4. Verify duration and file size before sending.

## Verification

After generation, verify:

```bash
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 /tmp/voiceover.ogg
```

Return the media path as `MEDIA:/tmp/voiceover.ogg`.

## Notes

- Treat MOSS and Samantha voice work as Mac Studio-centric unless the user asks to replicate it elsewhere.
- If the user wants a longer document transformed for TTS, also read `document-to-tts-transcript` first.
