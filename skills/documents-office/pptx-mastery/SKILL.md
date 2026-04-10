---
name: "PowerPoint Mastery"
description: >
  Create, edit, critique, repair, and analyze slide decks and presentations.
  Use this skill whenever the user mentions PowerPoint, presentations, slides, PPTX,
  slide decks, pitch decks, talk decks, or any task involving creating or improving
  presentation content. Triggers on: "make a presentation", "build a deck", "create slides",
  "edit this PPTX", "fix my presentation", "make these slides look better",
  "create a pitch deck", "convert this to slides", "critique my deck",
  "redesign this presentation", or any request to produce or polish a .pptx file.
  Handles creation from scratch, editing existing files, template-based workflows,
  visual QA, critique scoring, and repair of overflow or design violations.
compatibility: >
  Mode A (IR pipeline) requires Node + PptxGenJS. Mode B (editing) requires Python 3 +
  markitdown. OOXML editing requires LibreOffice + Poppler for visual QA.
  html2pptx path requires Node + PptxGenJS + Playwright.
---

<!-- Merged from pptx-master and pptx-enhanced. Both source directories archived. -->

# PowerPoint Mastery

Turn raw content into ship-ready slide decks by enforcing a **constraint system** — grid, type scale, color tokens, component library, deck rhythm — rather than improvising slide-by-slide. Also handles full visual critique, repair, and editing of existing decks.

Four jobs:
1. **Mode A — Create** a new deck from notes, docs, or a topic (IR-first pipeline).
2. **Mode B1 — Template-based edit**: rearrange template slides, replace content.
3. **Mode B2 — OOXML direct edit**: XML-level changes (comments, notes, animations, layout).
4. **Mode C — Review + repair**: critique, score, fix, and iterate.

The authoritative design reference is `references/ppt-design-guide.md`. All thresholds, archetype specs, IR format, QA checks, and repair ladders live there.

---

## What to read when (routing table)

Read reference files based on what you're doing. Multiple files apply for full deck creation. Read them before writing any code or content.

| Task | Load these references |
|---|---|
| Content planning, slide count, segmenting raw text | `references/content-segmentation.md` |
| Narrative flow and section sequencing | `references/narrative-arcs.md` |
| Choosing a layout archetype for any slide | `references/ppt-design-guide.md` §3, `references/renderer-archetypes.md`, `scripts/archetype-geometries.json` |
| Assertion headline writing and audit | `references/headline-audit.md` |
| Spatial composition and spacing systems | `references/composition-principles.md` |
| Asset/image planning and style coherence | `references/asset-planning.md` |
| Transforming dense text into structured slides | `references/transformation-patterns.md` |
| Full design guide (thresholds, QA ladders, IR, acceptance criteria) | `references/ppt-design-guide.md` |
| Quick decisions without reading the full guide | `references/quick-cheatsheet.md` |
| Colors, themes, dark-mode rules | `references/visual-themes.md` |
| Typography, hierarchy, and archetype spacing cues | `references/typography-color.md` |
| Adding charts or data visualizations | `references/data-viz.md` |
| IR format and element schema | `references/ir-schema.md`, `references/ir.schema.json` |
| Agent runtime defaults/preset behavior | `references/agent-presets.md` |
| Hard constraint tables, overflow strategy, auto-fix ladder, QA rubric | `references/constraints-qa.md` |
| Renderer archetype coverage + canonical archetype ID strings | `references/renderer-archetypes.md`, `scripts/archetype-geometries.json` |
| Vision critique scoring prompt and output schema | `references/vision_critique_prompt.md` |
| Toolchain comparison, python-pptx best practices | `references/ppt-design-guide.md` Appendix A–B |
| Full new deck creation (Mode A, end-to-end) | All of the above, in routing order |
| html2pptx fallback path | `html2pptx.md` |
| OOXML direct editing | `ooxml.md` |

---

## Feedback Loop

1. **Detect:** Notice when a reference, constraint, or workflow step helped or failed.
2. **Search:** Check `FEEDBACK.md` for existing related entries before adding.
3. **Scope:** One actionable observation per entry.
4. **Draft and ask:** Propose the entry to the user before writing.
5. **Write on approval:** Append to `FEEDBACK.md` with date and category tag.
6. **Compact at 75:** When entries reach 75, merge duplicates, promote patterns to reference files, archive resolved items. Reset to ~30 entries.

---

## Minimal intake (don't over-interview)

Proceed with defaults; ask only if missing information blocks execution.

1. **Audience + purpose** (investors? internal? conference talk?)
2. **Target length** (default: 12–14 slides)
3. **Brand constraints** (logo/colors/fonts) if provided
4. **Output format** (PPTX via IR renderer vs outline/IR only)

**Reasonable defaults when unspecified:**
- 16:9 (13.333" × 7.5"), margins 0.7", 12-column grid, 0.25" gutters
- Fonts: Inter or closest available; H1 36–44pt, H2 28–34pt, Body 18–24pt, Caption 14–16pt
- Colors: neutral bg, dark fg, single primary + single accent (see palette gallery in `references/typography-color.md`)
- Runtime preset: `agent_polished` (preflight on, animation pass on, auto-build animations off)

---

## Default deliverables (always produce)

Deliver all of these unless the user explicitly opts out:

- **Slide plan** (`slide-plan.md`) — one line per slide: role → archetype → assertion headline
- **Deck IR** (`deck.ir.json`) — renderer-agnostic contract following the schema in `references/ir-schema.md`
- **QA report** (`qa.report.json` + `qa.report.md`) — pass/fail against hard constraints + prioritized fixes
- **`deck.pptx`** — if script execution is available (Mode A) or the user requests a file

If making changes to an existing deck: also produce **`diff.md`** listing what changed per slide.

---

## Mode A — Create a new deck (IR-first pipeline)

**This is the primary creation path.** The renderer takes `deck.ir.json` and outputs `deck.pptx` via PptxGenJS — keeping content, layout, and rendering strictly separated.

### Mandatory design step before any code

Read these before writing a single line:
1. `references/content-segmentation.md` — apply segmentation heuristics and density thresholds to the raw content
2. `references/narrative-arcs.md` — choose arc shape and section pacing before slide-level design
3. `references/ppt-design-guide.md` §3 + `references/renderer-archetypes.md` + `scripts/archetype-geometries.json` — map each content chunk to a named archetype (A1–A24) using the decision tree and canonical geometry contracts
4. `references/composition-principles.md` + `references/typography-color.md` — select spacing system, type scale, and hierarchy treatment
5. `references/visual-themes.md` + `references/asset-planning.md` — select theme/mode and planned asset strategy
6. State your design approach (arc, archetype-per-slide mapping, color palette, deck rhythm plan) before writing the IR

**State your design approach before generating IR.**

### Design approach: content-informed color selection

Before writing code, consider:
- **Subject matter**: What tone, industry, or mood does this content suggest?
- **Brand signals**: If the user mentions a company/organization, consider their identity
- **Palette matching**: Select colors that reflect the content, not just defaults

**Color palette examples** (use to spark choices — adapt or create your own):

Classic Blue / Teal & Coral / Bold Red / Warm Blush / Burgundy Luxury / Deep Purple & Emerald / Pink & Purple / Black & Gold / Sage & Terracotta / Forest Green / Vibrant Orange

See `references/visual-themes.md` for the full palette gallery with hex values.

### Pipeline

#### Step 1 — Input digestion
Extract: facts, claims, numbers, tables, required sections, any must-include visuals.

Output: `inputs.digest.md` (short summary) + structured list of candidate slide chunks.

#### Step 2 — Storyboard (rule of one)
Segment content using the heuristics in `references/content-segmentation.md`. One idea per slide. Assign each slide a rhetorical role (hook, problem, evidence, plan, etc.).

Output: slide plan draft.

#### Step 3 — Layout planning

Choose one archetype per slide using `references/ppt-design-guide.md` §3.2 decision tree + canonical IDs in `references/renderer-archetypes.md` (`scripts/archetype-geometries.json` for machine checks). Prefer transforming bullet dumps into structure:

- 3–6 siblings → A8 (icon grid) or A9 (card grid)
- Comparisons → A10
- Roadmap → A12/A13
- Process steps → A14
- Single KPI → A7
- Data insight → A17/A18

**This step requires a filled planning table as its output. You may not proceed to Step 4 until this table is complete and both rhythm checks pass.**

| Slide | Role | Archetype | Rationale (≤10 words) | Assertion headline | Verb? | Claim? |
|---|---|---|---|---|---|---|
| S01 | … | … | … | … | ✓/✗ | ✓/✗ |

Rules for the Verb? and Claim? columns — read `references/headline-audit.md`:
- **Verb?** ✓ = headline contains at least one conjugated verb (is, are, produces, forces, reduces, enables). Gerunds ("using," "leveraging") do not count.
- **Claim?** ✓ = headline makes a falsifiable or comparative statement, not a topic category.

If any row has ✗ in either column, fix that headline before continuing.

**Rhythm summary (required at bottom of table):**

```
Non-bullet archetypes: X / N  (need ≥ 25% = ≥ ceil(N * 0.25)) → PASS / FAIL
Longest consecutive same archetype run: N → PASS (≤ 2) / FAIL (> 2)
Breather slides present: Y/N (required every 4–6 content slides)
```

If either rhythm row shows FAIL, redesign the affected slides before writing any IR.

#### Step 4 — Produce IR
Create `deck.ir.json` following `references/ir-schema.md` and valid against `references/ir.schema.json`:
- `deck.tokens`: fonts, sizes, colors, grid
- `deck.slides[]`: `id`, `archetype` (canonical string from `renderer-archetypes.md`), assertion `headline`, `elements[]` with `bbox` in inches

Validate: `python scripts/validate_ir.py deck.ir.json`

#### Step 5 — Snap to grid
```bash
python scripts/snap_to_grid.py deck.ir.json --out deck.snapped.ir.json
```

#### Step 6 — Render (pipeline default)
```bash
node scripts/pipeline.js deck.snapped.ir.json deck.pptx --preset agent_polished
```

CLI options: `--preset <name>`, `--skip-preflight`, `--skip-animations`, `--auto-animations`, `--strict-preflight`, `--vision-qa`

For direct renderer-only runs:
```bash
node scripts/render_pptx.js deck.snapped.ir.json deck.pptx
```

If PptxGenJS is unavailable: output IR + human-editable outline. See [Fallback: html2pptx](#fallback-html2pptx) below.

#### Step 7 — QA (computed, fail-fast)
For explicit/manual QA runs:

```bash
python scripts/preflight_ir.py deck.snapped.ir.json --out qa.report.json --md qa.report.md
python scripts/preflight_pptx.py deck.pptx --out qa.pptx.json --md qa.pptx.md
```

**Visual thumbnail review is always required before delivery** — it catches geometry failures that preflight scripts cannot detect from XML alone.

```bash
python scripts/thumbnail.py deck.pptx thumbnails
# Or fallback:
soffice --headless --convert-to pdf deck.pptx
pdftoppm -jpeg -r 150 deck.pdf slide
```

Work through each thumbnail and check: column widths equal on card/grid slides? No text overflow? Meaningful whitespace? Visually distinct consecutive slides?

If scripts are unavailable, state this explicitly and mark the deck as **UNVERIFIED — visual QA not completed**.

#### Step 8 — Repair loop (1–3 iterations max)
Apply fixes in order (from `references/constraints-qa.md`):
1. Overflow strategy: micro-edit → layout upgrade → split slide → expand box → font floor → switch archetype
2. Apply auto-fix ladders for each violation code
3. Update IR, re-snap, re-render, re-run preflight

Stop when all hard constraints pass + acceptance criteria met, OR 3 iterations reached.

---

## Mode B1 — Template-based content replacement

Use when: user provides a branded template and wants a new deck built from it.

#### Step 1 — Extract template content and create thumbnail grid
```bash
python -m markitdown template.pptx > template-content.md
python scripts/thumbnail.py template.pptx workspace/thumbnails --cols 4
```
Read `template-content.md` completely. **Never set range limits when reading this file.**

#### Step 2 — Analyze and save template inventory
Review thumbnail grid(s) visually. Map each template slide to its closest archetype (A1–A24). Save `template-inventory.md`:

```markdown
# Template Inventory
**Total Slides: [count]**
**IMPORTANT: Slides are 0-indexed**

- Slide 0: [Archetype ID] — Description/purpose
[... EVERY slide listed with its index ...]
```

#### Step 3 — Build outline and template mapping
Match each content chunk to a target archetype, then to a template slide offering that archetype. **Match layout to actual content:** two-column layouts only when you have exactly 2 items; image layouts only when you have actual images.

Save `outline.md` with:
```
template_mapping = [0, 34, 34, 50]  # indices are 0-based; repeat to duplicate
```

#### Step 4 — Rearrange slides
```bash
python scripts/rearrange.py template.pptx working.pptx 0,34,34,50
```

#### Step 5 — Extract text inventory
```bash
python scripts/inventory.py working.pptx text-inventory.json
```
Read `text-inventory.json` completely. **Never set range limits.** Only reference shapes that exist in this inventory.

#### Step 6 — Generate replacement text
Create `replacement-text.json`. Rules:
- All content slide headlines must be assertions (verb + claim, ≤ 12 words)
- Bullets: `"bullet": true, "level": 0` (no manual bullet symbols)
- Titles/headers: `"bold": true`
- Preserve alignment properties from inventory
- Colors: `"color": "FF0000"` (RGB) or `"theme_color": "DARK_1"` (theme token)
- Shapes not listed in replacement JSON are automatically cleared

#### Step 7 — Apply replacements and QA
```bash
python scripts/replace.py working.pptx replacement-text.json output.pptx
python scripts/thumbnail.py output.pptx workspace/output-thumbnails --cols 4
python scripts/preflight_pptx.py output.pptx --out qa.pptx.json --md qa.pptx.md
```

Produce `diff.md` listing what changed per slide.

---

## Mode B2 — OOXML direct editing

Use when: editing comments, speaker notes, animations, slide layouts, or any structural change beyond content replacement.

**MANDATORY**: Read `ooxml.md` completely before touching any XML. **Never set range limits.**

```bash
python ooxml/scripts/unpack.py <office_file> <output_dir>
# Edit XML files
python ooxml/scripts/validate.py <output_dir> --original <original_file>  # after EVERY edit
python ooxml/scripts/pack.py <output_dir> <output_file>
python scripts/preflight_pptx.py output.pptx --out qa.pptx.json --md qa.pptx.md
```

Key paths: `ppt/slides/slide{N}.xml`, `ppt/notesSlides/notesSlide{N}.xml`, `ppt/comments/modernComment_*.xml`, `ppt/theme/theme1.xml`

Positions are in EMUs. Conversion: `1 inch = 914400 EMU`. Safe margin floor: `0.5 in = 457200 EMU`.

---

## Mode C — Review and repair

Use when: user provides a deck and wants critique, polish, or "make this look professional."

1. If a PPTX is provided: run `preflight_pptx.py` first for computed violations.
2. Apply `references/vision_critique_prompt.md` for the scoring prompt + JSON schema.
3. Produce a prioritized issue list with evidence, issue codes, and concrete fixes.
4. If able to render: apply top fixes, re-run QA, produce updated deck.

Map all issues to guide codes: `OVERFLOW`, `LOW_CONTRAST`, `RAINBOW_SLIDE`, `LABEL_HEADLINE`, `TEXT_WALL`, `MISALIGNED_EDGES`, `CHART_CLUTTER`, `DECK_MONOTONY`, etc.

---

## Fallback: html2pptx

**Use only when Node/PptxGenJS is unavailable and a rendered PPTX is required, OR for creating from scratch without the full IR pipeline.**

Read `html2pptx.md` fully before using this path. **Never set range limits when reading it.**

Key differences from Mode A:
- HTML is written per slide instead of IR; rasterize gradients and icons as PNG images first using Sharp
- Use `<p>`, `<h1>`-`<h6>`, `<ul>`, `<ol>` for all text content; `class="placeholder"` for chart/table areas
- For slides with charts/tables: use full-slide or two-column layout (NEVER vertically stack)
- Rendering goes through `scripts/html2pptx.js` → PptxGenJS
- QA still runs on the output PPTX via `preflight_pptx.py`
- Treat output as draft quality, not ship-ready

All design rules still apply: assertion headlines, density thresholds, archetype selection.

---

## Design rules (non-negotiable)

### Hard constraints (must pass before shipping)

- **No text overflow or clipping** — 0 violations
- **Body font ≥ 18pt** (≥ 24pt for accessibility decks)
- **Whitespace ratio ≥ 0.22** on every slide
- **Contrast:** normal text ≥ 4.5:1; large text ≥ 3:1 (WCAG AA)
- **No off-palette colors** — token set only
- **Assertion headlines** on all content slides (≤ 12 words, includes a verb)
- **No more than 2 consecutive slides** with the same archetype
- **≥ 25% of slides** use non-bullet structural archetypes

Consult `references/ppt-design-guide.md` §10–12 and `references/constraints-qa.md` for the full constraint table and auto-fix ladders.

### Overflow repair order

Never shrink fonts as the first response to overflow. Apply in this order:
1. Micro-edit (tighten wording)
2. Layout upgrade (convert bullets to grid/cards)
3. Split slide (claim → detail pair)
4. Expand box (if whitespace allows)
5. Reduce font (down to 18pt floor only)
6. Switch archetype

---

## Creating thumbnail grids

```bash
python scripts/thumbnail.py presentation.pptx [output_prefix] [--cols N]
```

Creates `thumbnails.jpg` (or numbered files for large decks). Default: 5 columns, max 30 slides per grid. Slides are 0-indexed.

---

## Converting slides to images (for visual inspection)

```bash
soffice --headless --convert-to pdf presentation.pptx
pdftoppm -jpeg -r 150 presentation.pdf slide
# Specific range: -f 2 -l 5 for pages 2–5 only
```

---

## Slide plan format

```
- S01 — [role] — [archetype] — Assertion headline here
- S02 — [role] — [archetype] — Another assertion headline
```

Save to `slide-plan.md`. Present in-chat summary before generating IR.

---

## QA report format

`qa.report.md` structure:
1. Summary (PASS/FAIL + hard fail count + warning count)
2. Hard-fail violations (slide ID, code, evidence, fix)
3. Warnings (prioritized)
4. Fixes applied this iteration
5. Remaining recommendations

---

## Code style guidelines

- Write concise code
- Avoid verbose variable names and redundant operations
- Avoid unnecessary print statements

---

## Dependencies

```bash
# Python
python3 -m pip install --user --break-system-packages "markitdown[pptx]" defusedxml lxml pillow jsonschema pyyaml

# Node (from skill root)
npm install pptxgenjs sharp adm-zip

# System
sudo apt-get install libreoffice poppler-utils
```

## Known limitations

- `render_pptx.js` has dedicated archetype handlers for A1–A24, but slide quality still depends on IR quality.
- `preflight_ir.py` uses grid sampling to approximate whitespace ratio — accurate to ~2% but not pixel-perfect.
- `preflight_pptx.py` cannot detect text overflow/clipping from XML alone; visual QA via thumbnail grid is always required after rendering.
