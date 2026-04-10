# Transformation patterns

Canonical transformation library for converting dense source content into slide-friendly structures.

Use these patterns as deterministic inputs to planning and repair loops.

## Pattern schema

```json
{
  "pattern_id": "P001",
  "name": "paragraph_to_claim_plan_timeline",
  "input_signals": ["long_paragraph", "time_markers", "action_list"],
  "output_sequence": [
    {"archetype": "A7_big_number_callout", "intent": "claim"},
    {"archetype": "A14_process_flow", "intent": "mechanism"},
    {"archetype": "A12_timeline_horizontal", "intent": "plan"}
  ],
  "constraints": {
    "max_words_per_slide": 60,
    "headline_words_max": 12
  }
}
```

## Core pattern set

### P001 Paragraph -> claim + plan + timeline

- Input signals: long narrative paragraph, milestone dates, action verbs
- Output: `A7 -> A14 -> A12`
- Best for: strategy and execution updates

### P002 Feature list -> icon grid

- Input signals: 4-6 sibling bullets with repeated structure
- Output: `A8`
- Best for: capability summaries

### P003 Risk list -> matrix + mitigation cards

- Input signals: risks with impact/likelihood language
- Output: `A11 -> A9`
- Best for: operations and governance decks

### P004 Large table -> chart + short table

- Input signals: >6 rows, trend/comparison story
- Output: `A17 or A18 -> A19`
- Best for: executive reporting

### P005 Memo block -> hero + comparison + case study

- Input signals: argument text plus before/after claims
- Output: `A4 -> A10 -> A21`
- Best for: change-management narratives

### P006 Architecture text -> diagram + ownership cards

- Input signals: components, flows, responsibilities
- Output: `A16 -> A9`
- Best for: technical architecture communication

### P007 Executive summary -> metric + decision matrix + roadmap

- Input signals: recommendation plus options and timing
- Output: `A7 -> A11 -> A12`
- Best for: decision meetings

## Machine-readable batch config

Use this list as a compact selector map for automation:

```json
[
  {"pattern_id":"P001","trigger":"long_paragraph+timeline"},
  {"pattern_id":"P002","trigger":"sibling_bullets_4_to_6"},
  {"pattern_id":"P003","trigger":"risk_language_with_severity"},
  {"pattern_id":"P004","trigger":"table_over_6_rows"},
  {"pattern_id":"P005","trigger":"before_after_argument"},
  {"pattern_id":"P006","trigger":"system_components_and_flows"},
  {"pattern_id":"P007","trigger":"recommendation_with_options_and_plan"}
]
```

## Selection rules

1. Match content signals first, not favorite archetypes.
2. If two patterns match, pick the one with fewer slides unless clarity suffers.
3. If output violates density constraints, split pattern output into an extra support slide.
