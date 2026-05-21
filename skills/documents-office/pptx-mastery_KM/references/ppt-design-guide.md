# AI presentation design reference

A single authoritative reference for AI agents that generate, critique, and repair slide decks. Synthesized from three research reports covering agentic architecture, layout intelligence, typography, color theming, data visualization, toolchain best practices, and quality assurance.

---

## 1. Core mental model

A presentation deck is a **constraint system**, not a sequence of improvised slides. Every deck should be defined by five interlocking subsystems that lock in quality before any content is placed.

**Grid.** Margins, columns, gutters, and a baseline rhythm that every element snaps to. For 16:9 slides (13.333 in x 7.5 in): 0.7 in margins, 12 columns, 0.25 in gutters.

**Type scale.** Fixed roles with fixed size ranges. Never invent sizes per slide.

**Color tokens.** Role-based tokens (bg, surface, text, primary, accent, chart series) that enforce palette discipline across every slide.

**Component library.** Reusable elements (callout boxes, stat tiles, icon+label pairs, quote blocks, chart panels) built from grid and tokens.

**Deck rhythm.** The planned sequence of archetype variety and density alternation across the full deck, preventing monotonous middle slides.

---

## 2. Content segmentation

### 2.1 The rule of one

Each slide communicates one idea. If a slide needs two takeaways, it becomes two slides. This is the single highest-leverage rule for slide quality.

### 2.2 Segmentation heuristics

When breaking raw content into slides, score each candidate break point against these signals (assign 1-2 points each, split at cumulative score >= 3):

| Signal | Code | Weight |
|---|---|---|
| Explicit heading or section marker | H1 | 2 |
| Topic shift (new subject, entity, or argument) | H2 | 2 |
| Rhetorical function change (problem -> solution, claim -> evidence) | H3 | 2 |
| Data block (table, chart, metric) that deserves its own visual | H4 | 2 |
| Bullet list with 4+ siblings (convert to grid/cards) | H5 | 1 |
| Word count exceeds 60 for current chunk | H6 | 1 |
| Temporal or sequential marker ("then", "next", "phase 2") | H7 | 1 |
| Contrast or comparison language ("however", "vs", "alternative") | H8 | 1 |

Table: Segmentation heuristic signals. Each signal contributes weight points; split the content into a new slide when cumulative score reaches 3 or higher.

### 2.3 Density thresholds

| Metric | Target | Hard limit |
|---|---|---|
| Words per slide body | 25-60 | 90 max |
| Bullets per slide | 3-5 | 7 max |
| Body text lines | 6-9 | 10 max |
| Whitespace ratio | 0.30-0.45 | 0.22 min |
| Reading time | 3-7 sec scan, 15 sec read | -- |
| Headline length | 5-12 words | 12 max |
| Nesting depth (bullets) | 1 | 2 max |

Table: Slide density thresholds. "Target" is the ideal range; "Hard limit" triggers a split or archetype change.

### 2.4 Rhetorical roles

Segment by function, not just topic. Common slide rhetorical roles: hook, problem statement, insight/claim, evidence/data, mechanism/how-it-works, plan/roadmap, comparison/tradeoff, decision/recommendation, recap/CTA, breather/transition.

---

## 3. Layout archetype taxonomy

**Source of truth for geometry:** use `references/renderer-archetypes.md` for human-readable slot contracts and `scripts/archetype-geometries.json` for machine-readable slot geometry.  
This design guide focuses on *when* to use each archetype and the qualitative design rules.



24 named archetypes. Every slide maps to exactly one. The archetype determines element placement, constraints, and visual grammar.

### 3.1 Full catalog

| ID | Name | When to use | Key geometry |
|---|---|---|---|
| A1 | Hero cover | Deck opening; full-bleed image + title overlay | Image 100% area; title in safe zone |
| A2 | Section divider | Section transitions; minimal text, strong whitespace | Primary bg fill; headline 64pt; min whitespace 55% |
| A3 | Agenda / TOC | Deck navigation; 3-7 items | Numbered list or icon+label rows |
| A4 | Assertion + hero visual | Emotional emphasis; big claim + supporting image | Image >= 50% area; headline + subtext overlay |
| A5 | Split 50/50 | Text + image side by side | Left text 50%, right image 50%; mirror variant available |
| A6 | Split 30/70 | Sidebar context + main content panel | Narrow sidebar 30%, main panel 70% |
| A7 | Big number callout | Single KPI moment; one metric dominates | Hero number 72-140pt; supporting text sidebar |
| A8 | Icon grid | 3-6 parallel features/capabilities | 2x3 or 3x2 cell grid; icon + label + 1-line benefit per cell |
| A9 | Card grid | 2-4 drivers/pillars/categories | 2x2 cards with title + body per card |
| A10 | Comparison | A vs B; two options/paths/states | Two mirrored columns with parallel structure |
| A11 | Matrix / quadrant | 2x2 positioning; impact x effort, etc. | Quadrant axes with positioned points |
| A12 | Timeline horizontal | Roadmap; 3-6 milestones | Horizontal rail with evenly spaced nodes |
| A13 | Timeline vertical | History; chronological sequence | Vertical rail with date markers |
| A14 | Process flow | Sequential steps; 3-5 stages with arrows | Horizontal step cards with connectors |
| A15 | Cycle / loop | Recurring process; feedback loops | Circular or oval arrangement with directional arrows |
| A16 | Architecture diagram | System components + data flow | Boxes + labeled arrows; max 8 components |
| A17 | Chart-first insight | Data trend/comparison is the main point | Chart >= 45% area; headline states the insight |
| A18 | Annotated chart | Chart + interpretation callout | Chart + sidebar callout box with takeaway |
| A19 | Table (light) | Exact values needed; small data | Max 6 rows x 6 columns; min font 18pt |
| A20 | Before / after | Transformation; state change | Side-by-side or stacked with clear before/after labels |
| A21 | Case study | Concrete example; problem -> intervention -> result | 3-block horizontal: Problem, Intervention, Result |
| A22 | Quote | Credibility; emotional resonance | Large quote text; attribution below; high whitespace |
| A23 | Team / profiles | People; org structure | Photo + name + role grid |
| A24 | Q&A / closing | Deck ending | Minimal text; contact info or CTA |

Table: Complete archetype catalog. ID is the canonical reference code used in slide IR and template specs. "When to use" describes the content signal that triggers selection. "Key geometry" summarizes the dominant layout constraint.

### 3.2 Layout selection decision tree

Given a content chunk, select an archetype by matching content signals:

```text
START
  |
  v
Has a single dominant metric/KPI? --> YES --> A7 Big number
  |
  NO
  v
Has a data table or dataset? --> YES --> Is one number the story? --> YES --> A7
  |                                       |
  |                                       NO --> Trend/comparison? --> YES --> A17/A18
  |                                                |
  |                                                NO --> Exact values needed? --> YES --> A19
  |
  NO
  v
Has comparison/contrast language? --> YES --> Two options? --> YES --> A10
  |                                           |
  |                                           NO --> Positioning/priority? --> YES --> A11
  |
  NO
  v
Has sequence/steps/phases? --> YES --> Linear? --> YES --> A14 Process flow
  |                                    |
  |                                    NO --> Recurring? --> YES --> A15 Cycle
  |                                           |
  |                                           NO --> Time-based? --> YES --> A12/A13 Timeline
  |
  NO
  v
Has 3-6 sibling items? --> YES --> Each needs icon? --> YES --> A8 Icon grid
  |                                 |
  |                                 NO --> Each needs detail? --> YES --> A9 Card grid
  |
  NO
  v
Has system/architecture? --> YES --> A16 Architecture diagram
  |
  NO
  v
Is a quote or testimonial? --> YES --> A22 Quote
  |
  NO
  v
Is a case study / example? --> YES --> A21 Case study
  |
  NO
  v
Needs emotional emphasis + image? --> YES --> A4 Hero visual
  |
  NO
  v
DEFAULT --> A5 Split (text + image) or A6 Split (sidebar + main)
```

### 3.3 Candidate ranking

For ambiguous content, generate 2-4 candidate layouts and score each:

| Factor | Weight | How to compute |
|---|---|---|
| Readability | 0.25 | Minimum font size achieved; total word count within target |
| Density | 0.20 | Element area / slide area; penalize < 0.22 or > 0.70 whitespace ratio |
| Hierarchy | 0.20 | Headline font / body font ratio (target >= 1.6); one focal region |
| Alignment | 0.15 | Number of aligned edges; snap to grid score |
| Consistency | 0.20 | Token usage; no off-palette colors; no new font families |

Table: Layout candidate scoring factors. Apply weights, pick highest score that passes all hard constraints.

---

## 4. Typography system

### 4.1 Type scale (16:9 slides)

| Role | Size range | Usage |
|---|---|---|
| H1 (headline) | 36-44 pt | Slide assertion headline; one per slide |
| H2 (subhead) | 28-34 pt | Card titles, section labels within a slide |
| Body | 18-24 pt | Paragraphs, bullet content |
| Caption | 14-16 pt | Source lines, footnotes, axis labels |
| Label | 12-14 pt | Data labels, tags (never for readable body text) |
| Big number | 72-140 pt | Hero metrics on A7 slides |

Table: Type scale roles and size ranges. Sizes are for 16:9 (13.333 x 7.5 in) slides. The "minimum readable body" is 18pt; accessibility-oriented decks should use 24pt.

### 4.2 Headline rules

Write **assertion headlines**, not topic labels. A headline should state a claim or takeaway, not a category.

Bad: "Market trends"
Good: "Demand is shifting from features to time-to-value."

Assertion headlines force message clarity and reduce bullet dumping. Cap at 12 words. Allow 2 lines maximum.

### 4.3 Font selection

One font family for most decks (clean sans-serif). Optionally a secondary serif for headlines if brand requires. Use weights 400/500/700 only; avoid ultra-thin weights that collapse at distance or on projectors. Prefer fonts that exist on target machines or embed via template. If a font isn't available on the viewing machine, PowerPoint falls back to its default, which can break layouts.

### 4.4 Typography anti-patterns

These are the tells of auto-generated slides:

- Auto-shrunk text to fit a box (instead of splitting content or changing archetype)
- Multiple font families without a system
- Center-aligned body paragraphs (center only for short titles, quotes, hero text)
- Low line spacing / cramped blocks
- Title Case on everything (use sentence case unless brand dictates otherwise)
- More than 3 font sizes on a single slide
- Line length exceeding 70 characters

---

## 5. Color theming

### 5.1 Token system

Define colors by role, not by hex value. Every color in the deck maps to a token.

**Core tokens:**

| Token | Purpose |
|---|---|
| `bg` | Slide background |
| `surface` | Card/panel fill (slightly offset from bg) |
| `text` / `fg` | Primary text |
| `muted_text` | Secondary text, captions |
| `border` | Card/panel borders |

Table: Core color tokens. These define the neutral scaffold of every slide.

**Brand tokens:**

| Token | Purpose |
|---|---|
| `primary` | Main brand color; emphasis, key numbers, highlighted series |
| `primary_dark` | Darker variant for text-on-light or hover states |
| `primary_light` | Lighter variant for tinted backgrounds |
| `accent_1` | Secondary highlight; use sparingly |
| `accent_2` | Tertiary; rarely used |

Table: Brand color tokens. Primary is the workhorse; accents are used only when semantic distinction requires it.

**Chart tokens:**

| Token | Purpose |
|---|---|
| `series_1` through `series_6` | Chart data series colors (muted by default) |
| `good` / `warn` / `bad` | Semantic status colors |
| `gridline` | Chart gridlines (very low contrast) |
| `axis` | Axis lines and labels |
| `annotation` | Callout boxes on charts |

Table: Chart-specific color tokens. The "story series" gets `primary`; all others stay muted.

### 5.2 Color rules

**R1. One dominant accent per slide.** Use `primary` to highlight one element (headline emphasis, hero number, key chart series). Never compete with a second saturated color.

**R2. Neutral scaffolding.** Gridlines, axes, secondary labels should be low-contrast neutral. Scaffolding recedes; data speaks.

**R3. Dark backgrounds for moments only.** Section dividers, quote slides, hero moments. Random dark slides feel like template roulette.

**R4. Maximum 3 attention colors per slide.** Count distinct non-neutral colors. If more than 3, map extras to tokens or neutrals.

**R5. Contrast compliance.** Normal text: >= 4.5:1 contrast ratio (WCAG AA). Large-scale text (>= 18pt bold or >= 24pt): >= 3:1.

### 5.3 Chart palette rules

The chart palette is not the UI palette. Default series colors should be muted and distinct. Only the "story series" gets `primary`. Avoid rainbow palettes unless categorical data truly requires many classes. For accessibility, generate a colorblind-safe palette (Okabe-Ito is the standard) and map into brand hues where possible.

---

## 6. Imagery and iconography

### 6.1 When to add images

Add an image only if it provides context (product, environment), carries emotion (customer story, vision), provides structure (diagram, metaphor), or creates breathing room (hero/breather slide). Never add decorative stock next to bullet lists.

### 6.2 Placement rules

- If included, make the image dominant: >= 35% of slide area.
- Full-bleed images require a defined overlay text zone + contrast overlay (dark at 35-50% opacity).
- Face-safe crops: eyes in top third.
- Crop to stable aspect ratios that match the layout box.
- One image style per section (photo vs illustration vs icon; never mix).
- One icon library per deck; one photo treatment (color vs duotone) per deck.

### 6.3 Icon coherence

Use either outline or filled icons throughout the deck, never mixed. Match stroke weight to theme personality: 1.5px for editorial/minimal, 2px for bold/industrial. Color with the theme's primary or muted text token.

### 6.4 Asset sourcing strategies

**Stock APIs:** Prefer a single source per deck/section for style consistency.
**AI-generated images:** Use one style string per deck for coherence.
**Icons as vectors:** Prefer SVG, but convert to EMF/WMF or high-res PNG for PowerPoint compatibility (python-pptx cannot insert SVG into picture placeholders).

---

## 7. Data visualization on slides

Slide charts are not dashboard charts. They exist to make one point, not to provide interactive exploration.

### 7.1 Chart decision ladder

Given data, choose the simplest representation that communicates the insight:

1. **Single stat callout (A7)** if one number is the story.
2. **Simple chart (A17)** if a trend or comparison matters.
3. **Annotated chart (A18)** if the interpretation is non-obvious.
4. **Table (A19)** only if exact values are needed and the table is small (<= 6x6).
5. **Diagram/infographic** if the relationship is structural, not numerical.

### 7.2 Chart design rules

- Cap categories to 5-7 for live presentation slides.
- Cap series to 1-2 (3 maximum).
- Remove unnecessary gridlines; make remaining ones very low contrast.
- Axis labels >= caption size (14pt minimum).
- Always include a one-sentence takeaway, either as the headline or as an annotation callout.
- Highlight the key series with `primary` color; mute everything else.
- Never paste a screenshot of a table; redraw it.

---

## 8. Deck-level rhythm and variety

Most decks fail visually not because any single slide is bad, but because 15 slides in a row use the same structure.

### 8.1 Target distribution (12-20 slide deck)

| Category | % of slides | Examples |
|---|---|---|
| Hero / section / quote breathers | 10-20% | A1, A2, A4, A22 |
| Structured explanation | 30-45% | A5, A6, A8, A9, A14 |
| Evidence / data | 20-35% | A7, A17, A18, A19 |
| Decision / recap / CTA | 10-20% | A10, A11, A24 |

Table: Target archetype distribution for a typical 12-20 slide deck. Exact percentages flex with content, but the goal is visual variety.

### 8.2 Rhythm rules

- Never repeat the same archetype more than 2 slides in a row.
- Alternate between heavy (text-dense) and light (image/whitespace-dominant) slides.
- Every 4-6 content slides, insert a breather (A2 section divider, A22 quote, A4 hero visual).
- Alternate split direction (text-left/image-right vs mirrored) to avoid monotony.
- Maintain 1-2 recurring design motifs (a consistent accent bar, card style, or number treatment) for cohesion.

### 8.3 Example rhythm schedule (14-slide deck)

```text
S1:  A1  Cover
S2:  A3  Agenda
S3:  A7  Big number (hook KPI)
S4:  A5  Split (problem context)
S5:  A17 Chart-first (evidence)
S6:  A2  Section divider
S7:  A9  Card grid (solution pillars)
S8:  A14 Process flow (how it works)
S9:  A10 Comparison (option A vs B)
S10: A22 Quote (stakeholder voice)
S11: A12 Timeline (roadmap)
S12: A7  Big number (target outcome)
S13: A21 Case study (proof point)
S14: A24 Q&A / closing
```

---

## 9. Intermediate representation (IR)

The IR is the contract between content planning and visual rendering. It must be renderer-agnostic.

### 9.1 Structure

```json
{
  "deck": {
    "tokens": {
      "fonts": {
        "headline": {"family": "Arial", "weight": 700},
        "body": {"family": "Arial", "weight": 400}
      },
      "sizes": {"h1": 40, "h2": 30, "body": 20, "caption": 14},
      "colors": {
        "bg": "#FFFFFF",
        "fg": "#111111",
        "muted": "#6B7280",
        "primary": "#2563EB",
        "accent": "#F59E0B"
      },
      "grid": {
        "canvas": {"w_in": 13.333, "h_in": 7.5},
        "margins_in": {"t": 0.7, "r": 0.7, "b": 0.7, "l": 0.7},
        "columns": 12,
        "gutter_in": 0.25
      }
    },
    "slides": [
      {
        "id": "S01",
        "archetype": "A7_big_number_callout",
        "headline": "Support cost is up 38% YoY",
        "elements": [
          {
            "semantic_type": "number",
            "role": "hero_metric",
            "content": "38%",
            "bbox": {"x": 0.7, "y": 1.9, "w": 6.2, "h": 2.4},
            "style_tokens": {"font": "headline", "size": 140, "color": "primary"}
          }
        ],
        "constraints": {
          "max_lines_supporting": 6,
          "min_whitespace_ratio": 0.35
        }
      }
    ]
  }
}
```

### 9.2 Element types

Each element in a slide has a `semantic_type` and a `role`:

| semantic_type | Roles | Notes |
|---|---|---|
| `headline` | h1, h2 | One h1 per slide; h2 for card titles |
| `text` | body, supporting, takeaway, caption | Body text blocks |
| `number` | hero_metric, stat | Large numbers; A7 slides |
| `chart` | main | Chart specification with kind, series, axes, style |
| `table` | data | Columns, rows, emphasis rules |
| `image` | hero, supporting, icon | Placement, overlay, crop settings |
| `card` | left, right, grid_item | Container with children elements |
| `step` | process_step | Used in A14 process flow |
| `node` | timeline_node | Used in A12/A13 timelines |
| `box` | component, label | Architecture diagram components |
| `arrow` | connector | Directional flow between boxes |
| `callout` | annotation | Highlighted insight boxes |
| `footer` | caption, source | Source lines, page numbers |
| `bg` | background | Solid fill or image background |

Table: IR element types and their roles. The semantic_type determines rendering behavior; the role determines styling and constraint rules.

---

## 10. Hard constraints (fail-fast checks)

These are non-negotiable. If any fails, the slide must be fixed before rendering.

### 10.1 Geometry constraints

| Code | Rule | Threshold |
|---|---|---|
| G1 | No text overflow / clipping | 0 violations |
| G2 | Minimum margins | Content never within 0.5-0.7 in of edges |
| G3 | Element overlap | No unintentional overlap between elements |
| G4 | Grid alignment | All major elements snap to column grid |
| G5 | Consistent gutters | Multi-column layouts share gutter width |

Table: Geometry constraints. All are hard-fail; any violation blocks rendering.

### 10.2 Text constraints

| Code | Rule | Threshold |
|---|---|---|
| T1 | Minimum font size | >= 18pt body (>= 24pt for accessibility decks) |
| T2 | Headline length | <= 12 words |
| T3 | Max bullets per slide | <= 7 (prefer <= 5) |
| T4 | Max nesting depth | <= 2 levels |
| T5 | Max body lines | <= 9 (split if exceeded) |
| T6 | Line length | <= 70 characters |
| T7 | No widows/orphans | Last line of a block >= 2 words |
| T8 | Single alignment system | Don't mix centered paragraphs with left-aligned body |

Table: Text constraints. T1 and T5 are hard-fail; others are strong warnings.

### 10.3 Color constraints

| Code | Rule | Threshold |
|---|---|---|
| C1 | Text contrast ratio (WCAG) | Normal text >= 4.5:1; large text >= 3:1 |
| C2 | Off-palette colors | 0 colors outside token set |
| C3 | Max attention colors per slide | <= 3 distinct non-neutral colors |
| C4 | One dominant accent per slide | Only 1 saturated region competes for attention |

Table: Color constraints. C1 is hard-fail; C2-C4 are strong warnings that trigger auto-fix.

### 10.4 Image constraints

| Code | Rule | Threshold |
|---|---|---|
| I1 | Resolution | Minimum effective DPI for print/projection |
| I2 | Aspect ratio distortion | No stretch/squash |
| I3 | Tiny decorative images | Image < 15% slide area -> remove or promote to dominant |
| I4 | Style coherence | One style per section (photo/illustration/icon) |

Table: Image constraints. I2 is hard-fail; others are warnings.

### 10.5 Data viz constraints

| Code | Rule | Threshold |
|---|---|---|
| D1 | Category count | <= 7 for live slides |
| D2 | Label size | >= caption size (14pt) |
| D3 | Missing takeaway | Every chart needs a one-sentence insight |
| D4 | Series count | <= 3 |

Table: Data visualization constraints. D3 is hard-fail for annotated charts.

---

## 11. Overflow strategy

When a text block overflows its bounding box, apply fixes in this order. **Never shrink fonts as the first response.**

1. **Micro-edits.** Tighten wording, remove redundancy. If the text is LLM-generated, regenerate more concisely.
2. **Layout upgrade.** Convert bullets to card grid (A9) or icon grid (A8). This often resolves the density issue entirely.
3. **Split slide.** Break into claim slide + detail slide. Use assertion headline on slide 1, supporting structure on slide 2.
4. **Box expansion.** If whitespace allows, expand the text box within margin constraints.
5. **Font reduction (last resort).** Reduce font size, but enforce a hard floor: body >= 18pt (or >= 24pt for accessibility decks). Never shrink headline below H2 range.
6. **Archetype switch.** If nothing works, select a different archetype that naturally accommodates more content (e.g., A6 sidebar+main instead of A5 50/50).

---

## 12. Auto-fix rules

Each common violation maps to a deterministic fix ladder.

| Violation | Fix sequence |
|---|---|
| `OVERFLOW` | copy_trim -> box_expand -> font_down_to_min -> split_slide -> switch_archetype |
| `LOW_CONTRAST` | swap_text_color -> add_overlay_panel -> swap_bg |
| `TOO_MANY_BULLETS` | convert_to_tiles (A8/A9) -> split_slide |
| `REPEATED_ARCHETYPE` | switch_to_alternate_for_role -> insert_breather |
| `OFF_PALETTE_COLOR` | map_to_nearest_token -> reject |
| `TINY_IMAGE` | remove_image -> promote_to_dominant -> replace_with_icon |
| `TEXT_WALL` (>90 words or <0.22 whitespace) | convert_to_grid -> split_into_claim+support |
| `LABEL_HEADLINE` (<3 words, no verb) | rewrite_as_assertion |
| `MISALIGNED_EDGES` (>6 unique left-edge clusters) | snap_to_grid -> switch_to_template_archetype |
| `RAINBOW_SLIDE` (>3 non-neutral colors) | lock_to_tokens (primary + neutrals) |
| `IMAGE_FILLER` (semantically unrelated) | remove_image -> replace_with_icon -> use_full_bleed_hero |
| `CHART_CLUTTER` | simplify_ticks -> enlarge_labels -> mute_scaffolding -> convert_to_A7 |
| `DECK_MONOTONY` (>3 same archetype in row) | inject_breather -> swap_archetype |
| `TEMPLATE_MISMATCH` (content doesn't fit) | rerun_layout_selection -> split_or_merge_content |
| `EXPORT_MISMATCH` | check_fonts -> remove_gradients -> compress_images -> apply_pptx_compliance_mode |

Table: Auto-fix rule ladder. Apply fixes in sequence from left to right; stop at the first fix that resolves the violation.

---

## 13. Vision-model critique rubric

Canonical implementation prompt: `references/vision_critique_prompt.md`.

Use this rubric to score rendered slide images. Run programmatic pre-checks first (overflow, font size, font family count, accent color count); only invoke vision scoring after computed checks pass.

### 13.1 Scoring categories (1-5 each)

| Category | What to evaluate |
|---|---|
| Takeaway clarity | Can you identify the main point in 3 seconds? |
| Visual hierarchy | Is there one dominant anchor (headline, number, image)? |
| Layout and alignment | Grid-aligned? Consistent margins and gutters? |
| Density and whitespace | Breathing room present? Not crowded, not barren? |
| Typography | Min sizes respected? Consistent capitalization? No mixed alignment? |
| Color and contrast | WCAG compliant? Accents used sparingly? No rainbow? |
| Imagery relevance | Does the image support the claim, or is it decorative filler? |
| Data viz clarity | Scaffolding recedes? Takeaway highlighted? Labels readable? |
| Deck consistency | Same type scale, color tokens, icon style across all slides? |

Table: Vision-model scoring categories. Each scored 1-5. Overall pass requires mean >= 3.5 and no category below 2.

### 13.2 Output schema

```json
{
  "slide_id": "S12",
  "scores": {
    "takeaway_clarity": 4,
    "visual_hierarchy": 3,
    "layout_alignment": 3,
    "density_whitespace": 2,
    "typography": 4,
    "color_contrast": 4,
    "imagery_relevance": 3,
    "data_clarity": 5,
    "deck_consistency": 4
  },
  "overall_score": 3.6,
  "verdict": "pass_with_warnings",
  "top_issues": [
    {
      "code": "DENSITY_HIGH",
      "severity": "high",
      "evidence": "Body text fills 78% of content area",
      "fix": "Split into two slides: drivers (A9) then plan (A12)"
    },
    {
      "code": "MISALIGNED_EDGES",
      "severity": "medium",
      "evidence": "Left edges of cards differ by 0.15 in",
      "fix": "Snap card x positions to grid columns 1 and 7"
    }
  ],
  "recommended_fixes": [
    {"type": "split_slide", "target": "S12", "instruction": "Break into claim + evidence pair"},
    {"type": "snap_to_grid", "target": "card1,card2", "instruction": "Align left edges to col 1"}
  ],
  "suggested_archetype_change": {"from": "A5_split", "to": "A9_card_grid"}
}
```

### 13.3 Programmatic pre-checks (before vision critique)

Fail fast on these computed checks:

- Any text overflow -> fail
- Any font < 14pt (except citations/footnotes) -> fail
- More than 2 font families -> fail
- More than 1 dominant accent color -> warn/fix
- Whitespace ratio < 0.22 -> fail
- Headline word count > 12 -> warn

---

## 14. Agentic pipeline architecture

### 14.1 Multi-stage pipeline

```text
1. INPUT DIGESTION
   Extract: outline, facts, data tables, assets, audience, purpose

2. STORYBOARD
   Plan: deck sections, slide count per section, rhetorical roles, archetype candidates

3. LAYOUT PLANNING
   Select: archetype per slide via decision tree; generate slide IR with elements and constraints

4. ASSET PLANNING
   Decide: image vs icon vs diagram vs chart per slide; source assets; enforce style coherence

5. RENDERING
   Build: PPTX using base template + IR; populate placeholders; add shapes for dynamic content

6. QA (COMPUTED)
   Check: all hard constraints (overflow, font sizes, contrast, alignment, density)

7. QA (VISION)
   Score: rendered slide images against critique rubric (only after computed QA passes)

8. REPAIR LOOP
   Fix: apply auto-fix rules to IR; re-render; re-check; iterate 1-3 times max
```

### 14.2 Key principle: separate content from layout from rendering

- **LLM** produces slide IR and concise text.
- **Layout engine** enforces geometry, constraints, and archetype rules.
- **Renderer** draws shapes into PPTX (or other format).

This separation is what makes Beautiful.ai's Smart Slides work: design rules are enforced by the engine, not improvised by the AI.

### 14.3 Text measurement

The layout engine must estimate text height for a given font size and box width. Three tiers of accuracy:

**Tier A: Heuristic estimate (fast, imperfect).** Assume average character width ~= 0.5 x font size in points. Compute line count as `ceil(text_width / box_width)`. Multiply by line height. Works for early planning; fails on edge cases.

**Tier B: Font metric measurement (recommended).** Use a real font file to measure text (Pango/HarfBuzz/FreeType). Compute exact line breaks and height. Required for "never overflows" guarantee.

**Tier C: Render-and-measure (most accurate).** Render the text box off-screen and measure bounding boxes from the render. Slowest but provides ground truth for the QA loop.

---

## 15. Template specifications

This section provides reference examples only. Canonical renderer geometry remains in `references/renderer-archetypes.md` + `scripts/archetype-geometries.json`.

### 15.1 Shared coordinate system

All templates assume: 16:9 canvas (13.333 in x 7.5 in), 0.7 in margins, 12-column grid, 0.25 in gutters. Positions are in inches. Convert to EMUs at render time only.

### 15.2 Archetype intent guidance (non-geometric)

- **A7 Big number callout:** prioritize one metric with one short proof block; keep the metric visually dominant and supporting text concise.
- **A10 Comparison:** preserve mirrored visual weight across columns; force one-paragraph parity to avoid asymmetric scan paths.
- **A17 Chart-first insight:** chart must occupy primary visual area, with one explicit takeaway callout and one quantified implication.
- **A2 Section divider:** use as a pacing reset; one assertion headline and optional short context line.
- **A12 Timeline:** encode stage progression left-to-right with consistent node spacing and explicit stage verbs.
- **A8 Icon grid:** use for parallel benefits/capabilities; enforce label brevity and icon family consistency.

### 15.3 Constraint representation

Use IR-level constraints for testability and deterministic auto-fix, but keep coordinate truth in:

- `references/renderer-archetypes.md`
- `scripts/archetype-geometries.json`

Recommended constraint families:
- alignment (`align_left`, `align_center`, column consistency)
- scale (`min_font_size`, `max_lines`)
- density (`min_whitespace_ratio`, element count limits)
- rhythm (archetype repetition and section pacing)

---

## 16. Before/after transformation patterns

Canonical machine-readable patterns live in `references/transformation-patterns.md`. This section is a quick narrative summary.

### 16.1 Paragraph -> claim + plan + timeline

**Input:** A paragraph with a key metric, a list of actions, and a timeframe.
**Transform:** Slide 1 (A7): hero number + assertion headline. Slide 2 (A14): process flow with steps. Slide 3 (A12): timeline with milestones.

### 16.2 Feature list -> icon grid

**Input:** 4-6 features as bullets.
**Transform:** Single slide (A8): 2x3 icon grid with icon + 2-word label + 1-line benefit per cell.

### 16.3 Risk list -> matrix + mitigation cards

**Input:** A list of risks.
**Transform:** Slide 1 (A11): impact x likelihood matrix with positioned risk points. Slide 2 (A9): card grid with one mitigation per risk + owner metric.

### 16.4 Big table -> chart + small table

**Input:** A data table with many rows.
**Transform:** Slide 1 (A17): trend chart with annotated before/after. Slide 2 (A19): only the 4-6 rows executives actually need.

### 16.5 Strategy memo -> hero + comparison + case study

**Input:** A strategic argument with a claim and supporting evidence.
**Transform:** Slide 1 (A4): hero visual with bold claim. Slide 2 (A10): comparison of old vs new approach. Slide 3 (A21): case study with problem, intervention, result.

### 16.6 Architecture explanation -> diagram + cards + QA

**Input:** A description of system components and data flow.
**Transform:** Slide 1 (A16): architecture diagram with boxes and arrows. Slide 2 (A9): card grid with one responsibility per component. Slide 3 (A17 or custom): QA rubric or gate criteria.

### 16.7 Executive summary -> callout + matrix + timeline

**Input:** A paragraph arguing for a priority shift with causes and a plan.
**Transform:** Slide 1 (A7): lead metric. Slide 2 (A11): impact vs effort matrix for initiatives. Slide 3 (A12): 90-day execution timeline.

---

## 17. Computable quality metrics

These metrics can be computed from the IR or from rendered slide images without a vision model.

### 17.1 Alignment score

Extract left/right/top/bottom edges of all major elements. Cluster edges within a tolerance (e.g., 0.05 in). Score = sum(cluster_size^2) / total_edges. Higher = more aligned.

### 17.2 Density / whitespace ratio

`occupied_area = union_area(element_boxes)`
`whitespace_ratio = 1 - occupied_area / slide_area`

Flags: < 0.22 = cramped; 0.30-0.45 = healthy; > 0.60 = possibly too empty (unless hero slide).

### 17.3 Hierarchy score

`headline_font_size / body_font_size` (target >= 1.6). If body area dominates total text area, the slide reads like a document.

### 17.4 Color discipline score

Count distinct non-neutral colors on the slide (using LAB space tolerance). Penalize > 1 accent color competing for attention and low fg/bg contrast.

### 17.5 Visual balance (center of mass)

```text
cx = sum(area(e) * centerX(e)) / sum(area(e))
cy = sum(area(e) * centerY(e)) / sum(area(e))
balance_penalty = distance((cx, cy), slide_center)
```

Surprisingly strong detector of "random placements."

### 17.6 Repetition detector (deck-level)

Penalize runs of identical archetypes longer than 2. Penalize identical text density class runs (e.g., 8 text-heavy slides in a row). Encourage alternation between structure/data/breather.

---

## 18. Toolchain comparison

| Tool | Language | Control level | Template support | Agentic loop fit | Key limitation |
|---|---|---|---|---|---|
| python-pptx | Python | High | Slide layouts + masters | Strong (IR -> render -> QA) | No SVG; text fit is manual |
| PptxGenJS | JS/TS | High | Code-defined templates | Strong | Must implement style system yourself |
| Google Slides API | REST | Medium | Copy template + batchUpdate | Good for branded decks | Painful for custom layouts from scratch |
| Gamma API | REST | Medium-high | Themes + Smart Layouts | Good for drafts; no edit loop | Cannot edit existing gammas via API |
| Beautiful.ai | SaaS | Medium | 300+ Smart Slides | N/A (closed system) | Not programmable for custom pipelines |
| Canva | SaaS | Low-medium | Huge template library + brand kit | N/A (closed system) | Limited programmatic control |
| Figma Slides | Design tool | High (design) | Design-first | Export to PPTX as reference template | Gradients/fonts may not export cleanly |
| Quarto/Pandoc | Markdown | Low-medium | reference-doc PPTX | Good for data/metrics decks | Limited layout variety |
| Slidev/Reveal.js | HTML/CSS | High (web) | Code-defined | Web-native; PDF/PPTX via capture | PPTX export is screenshot-based |
| Office.js | JS | High (edit) | Works inside PowerPoint | Best for "edit existing deck" agents | Requires Office host |

Table: Toolchain comparison for AI-driven presentation generation. "Agentic loop fit" rates how well the tool integrates into a plan-render-QA-repair pipeline. python-pptx and PptxGenJS offer the most control for custom agentic systems.

### 18.1 python-pptx best practices

- Always start from a "golden template" PPTX with slide masters, fonts, and placeholder layouts for each archetype.
- Think in inches, convert to EMUs at render time only.
- Snap x positions to grid columns and y positions to a spacing scale.
- The biggest visual quality jump comes from **consistent left edges** and **consistent gutters**.
- For text fit: prefer split-slide over auto-shrink. python-pptx text autofit has known pain points; handle overflow in the layout engine before rendering.
- For icons: pre-convert SVG to EMF/WMF or high-res PNG.
- Implement template renderers per archetype: `render_A7(slide, data)`, not generic "add shapes."

### 18.2 Gamma API best practices

- Use `cardSplit: "inputTextBreaks"` with `\n---\n` markers for explicit segmentation control.
- Use `numCards` as a design budget (e.g., 12 for a pitch, 20+ for a lecture).
- Use `textOptions.amount` as a density guardrail.
- Use `imageOptions.source: "placeholders"` for decks that need post-editing.
- Apply `themeId` for brand consistency; import themes from existing PPTX.
- Treat Gamma as a strong draft generator, not an edit-loop engine.

---

## 19. Acceptance criteria

For a deck to be "ship-ready":

- 0 text overflows.
- Body font never below minimum (18pt general; 24pt accessibility).
- At least 25% of slides use non-bullet archetypes (A7, A8, A9, A10, A11, A12, A17, etc.).
- No more than 2 consecutive slides share the same archetype.
- Contrast checks pass for all text elements.
- Whitespace ratio >= 0.22 on every slide.
- Headline on every content slide is an assertion (has a verb), not a label.
- Render-QA diffs below threshold after a full export-to-PNG loop.
- No off-palette colors.
- Icon/image style is consistent within each section.

---

## 20. Industry lessons

### 20.1 Gamma

Cards as responsive building blocks. Smart Layouts as constraint templates with auto-alignment. Theme system as tokenization (colors, fonts, logos, design features, image style). Segmentation as a first-class API parameter. Key takeaway: make segmentation, density, imagery, and theme controls explicit and parameterized in your own IR.

### 20.2 Beautiful.ai

Smart Slides = templates + responsive rules + constraint enforcement. 300+ layouts mean you can almost always match content semantics to a template. The "Design AI" framing is an expert system (knowledge base + inference engine), not a generative model. Key takeaway: 30 excellent templates with a deterministic selector gets you 80% of the quality lift.

### 20.3 Canva

Breadth of templates + brand kit as tokenization + integrated chart tooling. Magic Design generates drafts from prompts with formatting handled. Magic Charts choose chart type algorithmically from data shape. Key takeaway: treat data visualization as its own module with a chart decision ladder, not a generic "insert chart" step.

### 20.4 Tome (cautionary)

Narrative scaffolding (story-first, pages-before-slides) is necessary but not sufficient. Without a template + layout intelligence layer, output won't consistently reach designer quality at scale. Tome pivoted away from presentations. Key takeaway: the designer engine (templates + layout logic + tokenization) is the durable value.

---

## 21. North star principles

1. **Never overflow text; never shrink below minimum; always split or change archetype.**
2. A deck is a constraint system, not a sequence of improvised slides.
3. Assertion headlines, not topic labels.
4. One idea per slide. One dominant accent per slide. One focal point per slide.
5. Templates first, AI-generated content second.
6. Separate content generation from layout enforcement from visual rendering.
7. Design variety comes from archetype alternation, not from ad-hoc creativity.
8. Every chart needs a takeaway. Every image needs a purpose.
9. Enforce quality with computable checks before invoking vision models.
10. Treat "export to PPTX" as a fallible step with preflight checks.

---

## Appendix A. Toolchain comparison

| Tool | Language | Control | Agentic loop fit | Key limitation |
|---|---|---|---|---|
| python-pptx | Python | High | Strong (IR → render → QA) | No SVG; text fit is manual |
| PptxGenJS | JS/TS | High | Strong — used by this skill's renderer | Must implement style system yourself |
| Google Slides API | REST | Medium | Good for branded decks | Painful for custom layouts from scratch |
| Gamma API | REST | Medium-high | Good for drafts; no edit loop | Cannot edit existing gammas via API |
| Beautiful.ai | SaaS | Medium | N/A (closed system) | Not programmable for custom pipelines |
| Quarto/Pandoc | Markdown | Low-medium | Good for data/metrics decks | Limited layout variety |
| Slidev/Reveal.js | HTML/CSS | High (web) | Web-native; PDF/PPTX via capture | PPTX export is screenshot-based |
| Office.js | JS | High (edit) | Best for "edit existing deck" agents | Requires Office host |
| html2pptx (PPX fallback) | JS/Node | Medium | Fallback when PptxGenJS unavailable | HTML-first breaks IR separation |

Table: Toolchain comparison. PptxGenJS via `scripts/render_pptx.js` is the primary renderer. python-pptx is the best alternative for Python-only environments. html2pptx is a fallback, not the primary path.

## Appendix B. python-pptx best practices

When implementing a custom renderer in python-pptx instead of PptxGenJS:

- Always start from a "golden template" PPTX with slide masters, fonts, and placeholder layouts for each archetype.
- Think in inches; convert to EMUs at render time only (`1 inch = 914400 EMU`).
- Snap x positions to grid columns and y positions to a spacing scale.
- The biggest visual quality jump comes from consistent left edges and consistent gutters.
- For text fit: prefer split-slide over auto-shrink. python-pptx text autofit has known pain points; handle overflow in the layout engine before rendering.
- For icons: pre-convert SVG to EMF/WMF or high-res PNG (python-pptx cannot insert SVG into picture placeholders).
- Implement template renderers per archetype: `render_A7(slide, data)`, not generic "add shapes."
---
## Appendix C. Canonical reference map

To avoid duplicated guidance, use these files as the source of truth:

- Theme selection + dark mode: `references/visual-themes.md`
- Typography system + archetype spacing cues: `references/typography-color.md`
- Hierarchical segmentation + section-break rules: `references/content-segmentation.md`
- Narrative arc planning: `references/narrative-arcs.md`
- Composition and spacing systems: `references/composition-principles.md`
- Asset planning and image workflow: `references/asset-planning.md`
- Transformation pattern library (machine-readable): `references/transformation-patterns.md`
- Vision critique prompt contract: `references/vision_critique_prompt.md`
- Motion animation spec: `references/animations.md`
- Icon standards: `references/icon-library.md`
