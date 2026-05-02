---
name: hermes-subagent-prompt-designer
description: Spawn a prompt/instruction design delegate for system prompts, skills,
  agent briefs, and output contracts.
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
- claude-hermes
---

# hermes-subagent-prompt-designer

## Trigger description
Load this skill when the parent Hermes agent should spawn a focused `prompt_designer` delegate instead of doing all prompt/agent instruction design work in the main context.

## When to use
Use for Hermes skills, delegate prompts, agent/task briefs, gateway response style, evaluation rubrics, or prompt cleanup.

## Recommended delegate_task toolsets
- Primary: `['file', 'web']`
- Optional: add `skills` when inspecting skill conventions.
- Add `file` only when the delegate must inspect or write local files.
- Add `terminal` only when shell commands materially improve verification.
- Avoid giving broad `hermes-cli` access unless the task truly needs it.

## Copyable delegate_task prompt template
```python
delegate_task(
    goal="Design or revise the requested prompt/instructions. Make it concise, operational, tool-aware, and testable. Preserve Kosta’s style: direct, technical, low-ceremony, no robotic audit voice.",
    context="""
User/request: <paste the exact user ask>
Kosta-specific constraints: concise, technical, Telegram-friendly; avoid noisy tables unless fenced.
Known context: <paths, URLs, screenshots, constraints, prior findings, deadlines>
Definition of done: <what the parent needs back>
Do not assume parent conversation history; everything needed is in this context.

Return using the Output Contract below.
""",
    toolsets=['file', 'web']
)
```

## Output contract
Return a compact report with:
1. **Answer/result** — the direct conclusion or completed action.
2. **Evidence/actions** — links, commands, files inspected/changed, or UI steps.
3. **Recommendations/next steps** — only what matters.
4. **Issues/blockers** — uncertainty, missing access, or confirmation needed.

## Safety/confirmation rules
Do not add hidden policy claims or fake capabilities. Confirm before overwriting durable instruction files.

## Pitfalls
Verbose prompt bloat; vague personas; missing output contract; optimizing for benchmark style instead of Kosta’s workflows.
