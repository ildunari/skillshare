# Slide Deck Designer — quick cheatsheet

This file is a short, high-signal subset of `ppt-design-guide.md` for fast decisions.

## Non-negotiables (ship-ready)
- **One idea per slide.** Split early.
- **No text overflow.** Prefer split-slide over shrinking fonts.
- **Body font ≥ 18pt** (≥ 24pt for accessibility).
- **Whitespace ratio ≥ 0.22** on every slide.
- **Assertion headlines** (≤ 12 words; includes a verb).
- **No off-palette colors** (use tokens only).
- **Contrast**: normal text ≥ 4.5:1; large text ≥ 3:1.

## Default grid (16:9)
- Canvas: **13.333" × 7.5"**
- Margins: **0.7"** (absolute minimum safe zone: 0.5")
- Columns: **12**
- Gutter: **0.25"**

## Type scale (roles)
- H1: 36–44
- H2: 28–34
- Body: 18–24
- Caption: 14–16
- Big number: 72–140

## Archetype picker (fast)
- Single KPI → **A7 Big number**
- 3–6 siblings → **A8 Icon grid** (light) or **A9 Card grid** (detailed)
- Comparison / tradeoff → **A10 Comparison**
- Roadmap / milestones → **A12 Timeline**
- Process / steps → **A14 Process flow**
- Data trend/comparison → **A17 Chart-first** (or A18 Annotated chart)
- Quote/testimonial → **A22 Quote**
- System diagram → **A16 Architecture**

## Overflow ladder (in order)
1) Micro-edit (tighten wording)
2) Upgrade layout (grid/cards)
3) Split slide (claim → detail)
4) Expand box (if whitespace allows)
5) Reduce font (down to min)
6) Switch archetype

## Anti-patterns
- Topic-label headlines ("Market trends")
- Bullet walls (>90 words, >7 bullets)
- Mixed alignments (centered paragraphs + left body)
- Rainbow accents (>3 non-neutral colors)
- Tiny decorative images (<15% area)
