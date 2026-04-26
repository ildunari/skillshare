---
name: hermes-subagent-voice-audio
description: Spawn an audio/voice delegate for TTS, transcripts, voice-note prep,
  audio files, and speech workflow debugging.
version: 0.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags:
    - hermes
    - subagent
    - delegation
    - template
targets:
- hermes-default
- hermes-gpt
---

# hermes-subagent-voice-audio

## Trigger description
Load this skill when the parent Hermes agent should spawn a focused `voice_audio` delegate instead of doing all voice/audio workflow work in the main context.

## When to use
Use for voice notes, TTS copy, audio conversion, transcript cleanup, ElevenLabs/OpenAI/Edge TTS checks, or podcast/meeting snippets.

## Recommended delegate_task toolsets
- Primary: `['terminal', 'file', 'tts']`
- Optional: add `web` for provider docs.
- Add `file` only when the delegate must inspect or write local files.
- Add `terminal` only when shell commands materially improve verification.
- Avoid giving broad `hermes-cli` access unless the task truly needs it.

## Copyable delegate_task prompt template
```python
delegate_task(
    goal="Handle voice/audio work: inspect files, generate or prepare speech, debug TTS/transcription pipelines, and return playable artifact paths when created. Optimize for Telegram-friendly outputs.",
    context="""
User/request: <paste the exact user ask>
Kosta-specific constraints: concise, technical, Telegram-friendly; avoid noisy tables unless fenced.
Known context: <paths, URLs, screenshots, constraints, prior findings, deadlines>
Definition of done: <what the parent needs back>
Do not assume parent conversation history; everything needed is in this context.

Return using the Output Contract below.
""",
    toolsets=['terminal', 'file', 'tts']
)
```

## Output contract
Return a compact report with:
1. **Answer/result** — the direct conclusion or completed action.
2. **Evidence/actions** — links, commands, files inspected/changed, or UI steps.
3. **Recommendations/next steps** — only what matters.
4. **Issues/blockers** — uncertainty, missing access, or confirmation needed.

## Safety/confirmation rules
Confirm before sending generated audio externally or overwriting originals. Do not expose API keys; avoid cloning voices without rights/consent.

## Pitfalls
Wrong codec for Telegram; overwriting source audio; overproducing long audio; not providing MEDIA path when useful.
