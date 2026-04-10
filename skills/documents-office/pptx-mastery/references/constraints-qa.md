---
title: Constraints and QA
scope: pptx-master
version: 1.0
---

# Constraints and QA

pptx-master enforces quality via two layers:

1) **IR preflight** (`scripts/preflight_ir.py`) — catches layout/content problems before rendering  
2) **PPTX preflight** (`scripts/preflight_pptx.py`) — catches OOXML/rendering problems after rendering

The goal is to eliminate the common failure modes:

- text overflow / cramped layout
- misalignment / jitter across slides
- unreadable contrast (especially dark themes)
- blurry images / charts
- broken animations
- missing embedded fonts (causes reflow on other machines)

---

## Pre-IR rhythm gate (runs on planning table, before any IR is written)

These checks run on the Step 3 planning table output — before IR generation. A FAIL here blocks Step 4. Fix the slide plan, not the IR.

| Constraint | Threshold | How to check | Fail action |
|---|---|---|---|
| Bullet-only archetype ratio | < 75% of slides use A2/A3/A4/A5 variants | Count bullet archetypes in plan table | Convert 2+ bullet slides to grid, split, timeline, or card archetype before continuing |
| Consecutive same archetype | ≤ 2 slides in a row with identical archetype | Scan plan table order top to bottom | Insert breather (A6/A7) or swap archetype on the third slide |
| Breather slide frequency | At least 1 every 4–6 content slides | Count content slides between A6/A7 breathers | Add a single-stat or visual break slide after dense runs |
| Non-structural archetype ratio | ≥ 25% of slides use A7–A24 non-bullet archetypes | Count A7–A24 in plan | Redesign slides from bullet to structural before writing IR |

**Enforcement rule:** the rhythm summary rows in the Step 3 planning table must explicitly reference this gate and show PASS/FAIL counts. A table without rhythm summary rows is incomplete — do not proceed.

---

## IR preflight checks

### 1) Alignment

- Finds groups of elements that should align (left edges, centers, right edges)
- Flags near-misses (e.g., two cards are 0.08 in off)

### 2) Spacing / density

- Counts elements and total text to estimate “visual density”
- Flags slides that exceed density thresholds for the chosen `density_profile`

### 3) Overflow risk (heuristic)

- Uses a conservative text measurement heuristic to estimate whether text fits its bbox:
  - greedy word wrap using average character width
  - line height estimate by font size × theme line-height
- Marks:
  - **WARN** when estimate exceeds bbox height by > 5%
  - **FAIL** when exceeds by > 20%

> This is a heuristic; the PPTX pass is the source of truth for final layout.

### 4) Contrast (WCAG)

For each text element, preflight estimates background color by:

1. nearest enclosing container fill (card/panel), otherwise
2. slide background (`tokens.colors.bg` or theme `bg`)

Contrast ratio is computed with WCAG relative luminance.

Thresholds:

- normal text: ≥ 4.5:1
- large text (≥ 24 pt regular or ≥ 18 pt bold): ≥ 3.0:1

### 5) Deck-level consistency

Preflight checks for cross-slide consistency drift:

- headline x/y position variance (within tolerance)
- number of distinct font families used
- card radii / border styles inconsistencies
- palette token misuse (e.g., mixing multiple primaries)

---

## PPTX preflight checks

### 1) Safe zone / bounds

- Ensures shapes stay within margins (default 0.7 in) unless explicitly marked as full-bleed background.

### 2) Image resolution (effective DPI)

For each placed image:

- compute displayed inches from shape bbox
- read pixel dimensions from `ppt/media/*`
- compute effective DPI per axis

Thresholds (guideline):

- ≥ 150 DPI for large photos / charts
- ≥ 100 DPI for small icons / thumbnails

### 3) Font embedding

Collects the set of fonts used in the deck and checks:

- whether the PPTX includes embedded fonts (`ppt/fonts/*` and/or `p:embeddedFontLst`)
- warns when non-standard fonts are used without embedding

### 4) Animation validity

When `<p:timing>` is present:

- validates that all `p:spTgt/@spid` targets exist on the slide
- checks timing tree basic integrity (ids present, mainSeq exists)
- flags malformed filters (unknown wipe direction, etc.)

---

## Severity model

- **FAIL:** should block rendering/shipping
- **WARN:** allowed but must be reviewed
- **INFO:** advisory

---

## Practical workflow

1. Generate IR
2. Run `validate_ir.py` (schema)
3. Run `preflight_ir.py`
4. Render PPTX
5. Run `preflight_pptx.py`
6. Optionally inject animations (`inject_animations.py`) and re-run `preflight_pptx.py`

