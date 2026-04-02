# Mode B eval: template-based deck creation

## Scenario
User provides a branded 40-slide PowerPoint template and asks for a 10-slide product launch deck.

## Input
- `template.pptx`: branded template with consistent colors, logo placement, and slide masters
- Topic: "Launching our ML-powered fraud detection product to enterprise financial services buyers"
- Audience: enterprise security and risk officers
- Target length: 10 slides

## Expected behavior

1. Extract template text and create thumbnail grid:
   ```
   python -m markitdown template.pptx > template-content.md
   python scripts/thumbnail.py template.pptx workspace/thumbnails
   ```
2. Analyze thumbnails; map each template slide to its archetype (A1–A24). Save `template-inventory.md`.
3. Apply segmentation heuristics (`references/content-segmentation.md`) to topic brief to determine 10 slide boundaries. Map each to a target archetype.
4. Select template slides matching each target archetype. Build `outline.md` with `template_mapping = [...]`.
5. Run `rearrange.py` to create `working.pptx` with only the 10 needed slides.
6. Run `inventory.py` to extract all shape positions and text into `text-inventory.json`.
7. Generate `replacement-text.json` with assertion headlines (≤12 words, verb present), bullets ≤7 per slide, body ≥18pt preserved.
8. Apply with `replace.py`. Verify no overflow errors.
9. Create thumbnail grid of `output.pptx` and inspect visually.

## Assertions
- Produces `template-inventory.md` with every slide catalogued by archetype
- Applies segmentation heuristics before selecting slide count
- All 10 slides have assertion headlines (not topic labels)
- `replacement-text.json` references only shapes that exist in the inventory
- `replace.py` reports 0 overflow violations
- No consecutive archetype repeats > 2
- Thumbnail grid is generated for final visual QA

## What would fail this eval
- Skipping template analysis and improvising layouts
- Using topic-label headlines ("Product Overview")
- Referencing shape IDs not in inventory → replace.py validation error
- Allowing font shrinkage below 18pt to handle overflow instead of splitting
