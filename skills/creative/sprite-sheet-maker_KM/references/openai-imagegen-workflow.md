# OpenAI And Imagegen Workflow

Use this for model/path decisions.

## Current Official Guidance

OpenAI docs checked on 2026-05-03:

- The Image API is suited to one-off image generation or edits from a prompt.
- The Responses API image generation tool is suited to conversational/editable image experiences.
- GPT Image output options include size, quality, format, compression, and background controls, depending on model support.
- `gpt-image-2` supports flexible size values but does not currently support transparent backgrounds; `background: "transparent"` fails for that model.
- Prompting guidance recommends structured prompts, intended use, concrete subject/style details, explicit preserve/avoid constraints, labeled multi-image inputs, and small iterative changes.

Sources:

- https://developers.openai.com/api/docs/guides/image-generation
- https://developers.openai.com/api/docs/guides/tools-image-generation
- https://developers.openai.com/cookbook/examples/multimodal/image-gen-1.5-prompting_guide

## Skill Routing

Use the installed `$imagegen` skill for normal visual generation:

```text
${CODEX_HOME:-$HOME/.codex}/skills/.system/imagegen/SKILL.md
```

Do not call the API directly unless the user explicitly asks for API/CLI mode or `$imagegen` directs a confirmed fallback.

## Transparency

Default path:

1. Generate on a flat chroma-key background with `$imagegen`.
2. Use `$imagegen`'s local chroma-key removal helper.
3. Validate transparent corners, subject coverage, and no key fringe.

Ask before CLI/native transparency when:

- The user asks for true/native transparent background.
- Chroma-key cleanup fails.
- The asset has hair, fur, glass, smoke, translucent fire, reflective surfaces, or colors that conflict with practical key colors.

## Multi-Row Sprite Runs

For row strips, attach:

- The canonical base as identity reference.
- User references with clear roles.
- Style/layout guides only if they will not appear in output.

In each prompt, explain that input images are references and must not be copied as scenery or labels.

