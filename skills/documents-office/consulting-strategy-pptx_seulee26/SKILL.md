---
name: consulting-strategy-pptx_seulee26
description: Use when the user asks for a McKinsey/consulting/strategy/business-review style native .pptx deck from a short brief: executive summary, KPI dashboard, market sizing, BCG matrix, roadmap, org chart, growth chart, strategic options, board update, QBR, or Korean/English consulting slides. Best for fast consulting-style deck generation using a bundled template catalog.
metadata:
  upstream: https://github.com/seulee26/mckinsey-pptx
  best_for: Consulting-style native PPTX decks from short business briefs using ~40 packaged slide templates.
---
# Consulting Strategy PPTX

Imported from https://github.com/seulee26/mckinsey-pptx and renamed for Skillshare routing. Upstream ships as a Claude Code plugin with a subagent; this local version wraps the same `mckinsey_pptx` Python package as a normal skill.

Use this when speed and consulting structure matter: QBRs, board decks, strategy reports, market scans, executive summaries, growth charts, KPI dashboards, roadmaps, org charts, matrices, and Korean/English McKinsey-style slides.

## Workflow

1. Understand the brief: audience, decision, known numbers, unknown placeholders, language, and desired slide count.
2. Read `mckinsey_pptx/agent/CATALOG.md` before choosing slide templates. Do not invent template names or payload shapes.
3. Generate a Python build script in the working directory, usually under `output/`, using the bundled package.
4. Make the package importable from this skill directory. Resolve the skill directory from this `SKILL.md`, then add it to `PYTHONPATH` / `sys.path` in the generated script:

```python
from pathlib import Path
import sys
SKILL_DIR = Path("/Users/Kosta/.config/skillshare/skills/documents-office/consulting-strategy-pptx")
sys.path.insert(0, str(SKILL_DIR))
from mckinsey_pptx import PresentationBuilder
```

If running from an installed target copy, locate this skill folder with `find ~/.hermes ~/.claude -path '*consulting-strategy-pptx/SKILL.md' -print -quit` and use that parent path instead of hard-coding the canonical path.

5. Build the `.pptx`. If preview tools exist (`soffice`, `pdftoppm`), render PNG previews; do not block delivery if preview tooling is missing.
6. Report the output path, the slide arc, the template choices, and caveats for invented/placeholder data.

## First-run setup

Check importability first:

```bash
python3 -c "import mckinsey_pptx"
```

If it fails, install upstream dependencies from this skill directory:

```bash
pip install -r requirements.txt
```

For previews on macOS, optional tools are LibreOffice and poppler:

```bash
brew install --cask libreoffice
brew install poppler
```

## Pairing

Pair with `documents-office__powerpoint` when the task needs general PPTX reading/editing, raw OOXML inspection, thumbnail QA, comments, notes, or post-generation fixes outside the consulting-template package.
