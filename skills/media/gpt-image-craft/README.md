# GPT Image Craft skill

A cross-platform open-format skill for creating, editing, debugging, and productionizing image-generation prompts with ChatGPT Images 2.0 / GPT Image 2.

## Contents

- `SKILL.md` — routing, core workflow, defaults, safety boundaries, and examples.
- `references/` — deeper model guidance, prompt frameworks, style libraries, recipes, troubleshooting, and source notes.
- `scripts/image_prompt_audit.py` — local prompt/parameter checker for GPT Image 2 risks.
- `evals/evals.json` — realistic test prompts and expectations.
- `evals/trigger-eval.json` — description routing tests.

## Quick audit example

```bash
python scripts/image_prompt_audit.py --prompt "make a transparent exact chart png" --model gpt-image-2 --size 1536x1024 --quality high
```

The script only audits prompt shape and parameters; it does not call the OpenAI API.
