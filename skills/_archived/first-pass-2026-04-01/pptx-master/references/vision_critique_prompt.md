# Vision critique prompt

Use this prompt contract after computed preflight checks pass.

## Preconditions

Run these before vision critique:

1. `python scripts/preflight_ir.py ...`
2. `python scripts/preflight_pptx.py ...` (if a PPTX exists)
3. Render slide images via thumbnail workflow for visual review

If hard-fail count is non-zero, fix those first.

## Prompt template

```text
You are a slide design critic. Score the slide(s) using the provided rubric.

Rubric categories (1-5):
- takeaway_clarity
- visual_hierarchy
- layout_alignment
- density_whitespace
- typography
- color_contrast
- imagery_relevance
- data_clarity
- deck_consistency

Rules:
- Ground every finding in visible evidence.
- Return at most 5 top issues per slide.
- Map each issue to a fix code from:
  OVERFLOW, LOW_CONTRAST, TOO_MANY_BULLETS, REPEATED_ARCHETYPE, OFF_PALETTE_COLOR,
  TEXT_WALL, MISALIGNED_EDGES, RAINBOW_SLIDE, CHART_CLUTTER, DECK_MONOTONY.
- Include concrete fix actions with target archetype/element where possible.
```

## Expected output schema

```json
{
  "slide_id": "S08",
  "scores": {
    "takeaway_clarity": 4,
    "visual_hierarchy": 3,
    "layout_alignment": 3,
    "density_whitespace": 2,
    "typography": 4,
    "color_contrast": 4,
    "imagery_relevance": 3,
    "data_clarity": 4,
    "deck_consistency": 4
  },
  "overall_score": 3.4,
  "verdict": "pass_with_warnings",
  "top_issues": [
    {
      "code": "DENSITY_HIGH",
      "severity": "high",
      "evidence": "Body text occupies most of the content area",
      "fix": "Split into claim slide and support slide"
    }
  ],
  "recommended_fixes": [
    {
      "type": "split_slide",
      "target": "S08",
      "instruction": "Convert to A7 + A9 pair"
    }
  ],
  "suggested_archetype_change": {
    "from": "A5_split_50_50",
    "to": "A9_card_grid"
  }
}
```

## Integration path

1. Attach slide thumbnails in sequence.
2. Ask for per-slide JSON with strict schema compliance.
3. Convert returned fixes into IR edits.
4. Re-run preflight and iterate up to 3 times.

## Failure handling

- If the model returns vague feedback, re-run with explicit evidence requirement.
- If outputs are not schema-valid JSON, request regeneration with "JSON only" instruction.
- If visual critique conflicts with computed checks, computed checks win unless a clear false-positive is proven.
