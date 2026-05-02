---
name: moss-multilingual-voice-cloning
description: Use when generating or debugging multilingual MOSS-TTS voice cloning, especially Hebrew or cross-language Samantha-style speech. Covers language codes, natural script prep, reference transcript pitfalls, continuation-mode caveats, speed/duration budgeting, and local verification on the Mac Studio MOSS setup.
targets:
  - hermes-default
  - hermes-gpt
  - claude-hermes
---

# MOSS Multilingual Voice Cloning

Use this when the user asks for MOSS TTS in Hebrew or another non-English language, complains that multilingual output sounds wrong, asks how to use MOSS languages properly, or wants to improve MOSS speed/quality.

## Local setup

Main wrapper:

```bash
~/LocalDev/voice/moss/bin/moss
```

Samantha profile:

```text
~/LocalDev/voice/moss/voices/samantha-her-a/reference.wav
~/LocalDev/voice/moss/voices/samantha-her-a/reference.txt
```

Canonical reference library copy:

```text
~/LocalDev/voice/reference-library/samantha-her-a/
```

## Language handling

Always pass a language code explicitly. Do not let the wrapper default to English for non-English text.

Examples:

```bash
--lang he   # Hebrew
--lang ar   # Arabic
--lang fa   # Persian/Farsi
--lang fr   # French
--lang es   # Spanish
--lang de   # German
--lang ja   # Japanese
--lang ko   # Korean
```

MOSS docs list broad multilingual support, but quality varies by language and by reference voice. An English reference voice can carry accent artifacts into Hebrew even when the text is good.

## Best default for short multilingual memos

For a user-facing short memo, use clone mode with explicit language and duration budget:

```bash
~/LocalDev/voice/moss/bin/moss say "$TEXT" \
  --lang he \
  --voice samantha-her-a \
  --fast \
  --seconds 45 \
  --out /tmp/moss_hebrew.wav
```

Convert for Telegram:

```bash
ffmpeg -y -i /tmp/moss_hebrew.wav -c:a libopus -b:a 48k /tmp/moss_hebrew.ogg
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 /tmp/moss_hebrew.ogg
```

Then send:

```text
MEDIA:/tmp/moss_hebrew.ogg
```

## Hebrew writing rules

The written Hebrew matters. MOSS will not fix translationese.

- Write natural Hebrew, not English sentence structure with Hebrew words.
- Prefer short, ordinary spoken sentences.
- Use simple punctuation.
- Write numbers as words if the exact numeric form sounds awkward.
- Use known Hebrew forms for names and places when common.
- For transliterated names, use straight apostrophes: `צ'ארלס`, not curly quote variants.
- Avoid dense foreign brand lists in Hebrew unless necessary; they often hurt pronunciation.

## Reference text and continuation pitfalls

The official MOSS docs describe `ref_text` and continuation-based cloning, but the local MLX path can include the reference transcript/prefix in the generated output. In local testing:

- plain clone with `--voice samantha-her-a` produced the intended short target audio
- using the saved Samantha transcript as `ref_text` caused the output to run to a long token budget
- continuation mode produced long audio including prefix-like material rather than a clean short memo

So for normal user-facing multilingual memos:

```text
Use:    --voice samantha-her-a --lang he --fast --seconds <target>
Avoid:  --use-ref-text, --ref-text, --mode continuation, --mode continuation-clone
```

Use reference-text or continuation modes only as diagnostic experiments, and verify the audio duration before sending anything.

## Speed controls

MOSS often runs until the token budget on short non-English clips. Use these controls:

- `--fast`: stable sampler defaults and text-based token budgeting
- `--seconds N`: explicit duration budget, mapped at about 12.5 audio tokens per second
- `--max-tokens N`: manual hard cap if you are doing controlled experiments

Good default for a one-minute-ish memo:

```bash
--fast --seconds 55
```

Good default for a concise 30-45 second Telegram memo:

```bash
--fast --seconds 35
```

Cold startup dominates very short clips. Do not expect a 3-second test sentence to be fast wall-clock; use a realistic 30-60 second sample when judging RTF.

## Verification checklist

Before saying a multilingual MOSS render is good or sending it:

1. Confirm the command used `--lang <code>`.
2. Confirm it did not accidentally use `--use-ref-text` or continuation mode for a normal memo.
3. Run `ffprobe` and check duration is in the requested range.
4. If the user complained about language quality, inspect/rewrite the source text first; then regenerate.
5. If pronunciation still sounds off after good text, label it as model/reference-voice limitation, not a script issue.

## Known local behavior

- `moss say` may print `Voice: None` even when Samantha is active, because the wrapper passes the resolved voice as `--ref_audio`.
- `~/LocalDev/voice/moss` is not necessarily a git repo. Back up or patch carefully; do not promise a worktree unless `git rev-parse --show-toplevel` succeeds.
- Current verified Hebrew Samantha run: `--fast --seconds 45` produced 42.4 seconds of audio in 27.8 seconds, about RTF 0.65.
