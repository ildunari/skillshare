#!/usr/bin/env python3
"""Static sanity checks for the GPT Image Craft skill."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

required = [
    "SKILL.md",
    "references/model-and-workflow.md",
    "references/prompt-framework.md",
    "references/prompt-recipes.md",
    "references/troubleshooting.md",
    "references/styles/science-education-figures.md",
    "references/styles/data-graphs-infographics.md",
    "references/styles/realism-photography-cinematic.md",
    "references/styles/design-marketing-ui.md",
    "references/styles/game-assets-icons-sprites.md",
    "references/styles/illustration-comics-character.md",
    "references/styles/print-editorial-typography.md",
    "references/styles/product-ecommerce-editing.md",
    "references/styles/niche-style-atlas.md",
    "scripts/image_prompt_audit.py",
    "evals/evals.json",
    "evals/trigger-eval.json",
]

missing = [p for p in required if not (ROOT / p).exists()]
if missing:
    raise SystemExit(f"Missing required files: {missing}")

skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
for phrase in ["gpt-image-2", "transparent", "exact numeric charts", "references/prompt-recipes.md"]:
    if phrase not in skill:
        raise SystemExit(f"SKILL.md missing expected phrase: {phrase}")

recipes = (ROOT / "references/prompt-recipes.md").read_text(encoding="utf-8")
recipe_count = recipes.count("### ")
if recipe_count < 25:
    raise SystemExit(f"Expected at least 25 recipes, found {recipe_count}")

atlas = (ROOT / "references/styles/niche-style-atlas.md").read_text(encoding="utf-8")
style_count = sum(1 for line in atlas.splitlines() if line.strip().startswith(tuple(f"{i}." for i in range(1, 61))))
if style_count < 50:
    raise SystemExit(f"Expected at least 50 style capsules, found {style_count}")

with (ROOT / "evals/evals.json").open(encoding="utf-8") as f:
    evals = json.load(f)
if evals.get("skill_name") != "gpt-image-craft" or len(evals.get("evals", [])) < 4:
    raise SystemExit("evals.json has wrong skill_name or too few evals")

with (ROOT / "evals/trigger-eval.json").open(encoding="utf-8") as f:
    triggers = json.load(f)
if len(triggers) != 20 or sum(1 for q in triggers if q["should_trigger"]) != 10:
    raise SystemExit("trigger-eval.json should contain 20 cases with 10 should-trigger queries")

print("Static checks passed")
