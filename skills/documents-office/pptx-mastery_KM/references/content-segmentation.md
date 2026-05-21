# Content segmentation

## Core mental model

A presentation deck is a **constraint system**, not a sequence of improvised slides. Every deck is defined by five interlocking subsystems that lock in quality before any content is placed:

- **Grid.** Margins, columns, gutters, baseline rhythm. For 16:9 (13.333 in x 7.5 in): 0.7 in margins, 12 columns, 0.25 in gutters.
- **Type scale.** Fixed roles with fixed size ranges. Never invent sizes per slide.
- **Color tokens.** Role-based tokens (bg, surface, text, primary, accent, chart series) enforcing palette discipline across every slide.
- **Component library.** Reusable elements (callout boxes, stat tiles, icon+label pairs, quote blocks, chart panels) built from grid and tokens.
- **Deck rhythm.** Planned sequence of archetype variety and density alternation across the full deck.

## The rule of one

Each slide communicates **one idea**. If a slide needs two takeaways, it becomes two slides. This is the single highest-leverage rule for slide quality.

## Segmentation heuristics

When breaking raw content into slides, score each candidate break point. Split when cumulative score >= 3.

| Signal | Code | Weight |
|---|---|---|
| Explicit heading or section marker | H1 | 2 |
| Topic shift (new subject, entity, or argument) | H2 | 2 |
| Rhetorical function change (problem→solution, claim→evidence) | H3 | 2 |
| Data block (table, chart, metric) that deserves its own visual | H4 | 2 |
| Bullet list with 4+ siblings (convert to grid/cards) | H5 | 1 |
| Word count exceeds 60 for current chunk | H6 | 1 |
| Temporal or sequential marker ("then", "next", "phase 2") | H7 | 1 |
| Contrast or comparison language ("however", "vs", "alternative") | H8 | 1 |

## Hierarchical segmentation (macro -> section -> slide)

Segment in three passes so deck structure stays coherent:

1. **Macro pass (deck sections).** Group source material into 3-6 major sections: opener, problem, evidence, plan, proof, close.
2. **Section pass (beats).** Inside each section, define 2-4 beats with clear rhetorical intent.
3. **Slide pass (single-idea cards).** Convert each beat into one or more slides using the rule of one and density thresholds.

Use this section-level planning frame:

| Level | Unit | Typical count | Validation check |
|---|---|---|---|
| L1 | Deck sections | 3-6 | Each section has one sentence objective |
| L2 | Section beats | 2-4 per section | Beat transition is explicit (cause, contrast, next step) |
| L3 | Slides | 1-3 per beat | Each slide has one assertion headline |

Escalation rule: if any L2 beat needs >3 slides, split that beat into two beats before assigning archetypes.

## Section-break guidance

Section breaks are intentional pacing devices, not filler slides.

Add a section break when one of these conditions is true:

- Shift from context to argument (problem -> solution, diagnosis -> plan)
- Audience mental reset is needed after 4-6 dense slides
- Narrative voice changes (analysis -> decision, technical -> executive summary)
- Visual mode changes (text-heavy block -> evidence/chart block)

Preferred section-break archetypes:

- `A2_section_divider` for hard transitions
- `A22_quote` for reflective pause
- `A4_assertion_hero_visual` for emotional or strategic reset

Section-break quality checks:

- Headline is <= 8 words and signals direction ("What must change next")
- Whitespace ratio >= 0.45
- No body bullet list on section-break slides
- Adjacent slides must not repeat the same archetype on both sides of the break

## Density thresholds

| Metric | Target | Hard limit |
|---|---|---|
| Words per slide body | 25-60 | 90 max |
| Bullets per slide | 3-5 | 7 max |
| Body text lines | 6-9 | 10 max |
| Whitespace ratio | 0.30-0.45 | 0.22 min |
| Reading time | 3-7 sec scan, 15 sec read | — |
| Headline length | 5-12 words | 12 max |
| Nesting depth (bullets) | 1 | 2 max |

## Rhetorical roles

Segment by function, not just topic. Common slide rhetorical roles: hook, problem statement, insight/claim, evidence/data, mechanism/how-it-works, plan/roadmap, comparison/tradeoff, decision/recommendation, recap/CTA, breather/transition.

## Before/after transformation patterns

Apply these as reusable transformations when raw content doesn't fit a single slide.

Canonical machine-readable pattern definitions live in `references/transformation-patterns.md`.

**Paragraph → claim + plan + timeline:** A paragraph with a key metric, a list of actions, and a timeframe becomes: Slide 1 (A7) hero number + assertion headline → Slide 2 (A14) process flow → Slide 3 (A12) timeline with milestones.

**Feature list → icon grid:** 4-6 features as bullets become a single slide (A8) 2x3 icon grid with icon + 2-word label + 1-line benefit per cell.

**Risk list → matrix + mitigation cards:** Slide 1 (A11) impact x likelihood matrix → Slide 2 (A9) card grid with one mitigation + owner per risk.

**Big table → chart + small table:** Slide 1 (A17) trend chart with annotated before/after → Slide 2 (A19) only the 4-6 rows executives actually need.

**Strategy memo → hero + comparison + case study:** Slide 1 (A4) hero visual with bold claim → Slide 2 (A10) old vs new comparison → Slide 3 (A21) case study.

**Architecture explanation → diagram + cards + QA:** Slide 1 (A16) architecture diagram → Slide 2 (A9) card grid with one responsibility per component → Slide 3 gate criteria.

**Executive summary → callout + matrix + timeline:** Slide 1 (A7) lead metric → Slide 2 (A11) impact vs effort matrix → Slide 3 (A12) 90-day execution timeline.
---

## Speaker notes (Phase 2)

The IR supports slide speaker notes:

- `slide.speaker_notes` (string | array of strings | object)
- `deck.speaker_notes_defaults` for deck-wide templates

### Why include notes?

- Keeps the spoken narrative consistent with the slide
- Helps reviewers understand intent without guessing
- Allows an LLM to generate tighter slide copy (the slide can be concise; detail goes in notes)

### Suggested note structure

For most business slides:

1. **1 sentence context**
2. **1 sentence “so what”**
3. **Walkthrough bullets** (in build order if animated)

Example:

```json
{
  "speaker_notes": [
    "Context: We’re optimizing onboarding to reduce time-to-value.",
    "So what: Two changes drive most of the improvement.",
    "Walkthrough: Left card = new self-serve flow. Right card = proactive support trigger."
  ]
}
```

---

## Density profiles

`deck.density_profile` and `slide.density_profile` control how aggressively the generator should pack information.

- `sparse` — fewer elements, larger text, more whitespace
- `comfortable` — default
- `dense` — tighter spacing, smaller text, but still within readability limits

Practical guidance:

- Use `sparse` for keynote / demo decks.
- Use `comfortable` for typical exec updates.
- Use `dense` only for appendix-style slides (tables, detailed comparisons).

Preflight enforces density thresholds (see `references/constraints-qa.md`).
