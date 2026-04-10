---
name: humanize-ai-content
description: >
  Rewrite AI-sounding text into natural human prose without changing meaning or facts.
  Trigger when the user asks to "make this sound human," "make this less robotic,"
  "humanize this," "rewrite so it doesn't read like AI," "same message better flow,"
  "polish this but keep the facts," or any variant involving posts, emails, blogs,
  reports, LinkedIn content, sales copy, academic writing, or technical docs that
  sound AI-generated. Supports tone presets (crisp-human, warm-human, expert-human,
  story-lean) and includes automated validators for fact preservation, banned-phrase
  scanning, structural tell detection, readability metrics, and diff/length guardrails.
  Works with pasted text or file paths.
---

# Humanize AI Content

Turn stiff, AI-sounding writing into natural human prose **without changing meaning or facts**.

This skill uses two passes:

1. **Diagnosis**: find concrete AI tells (vocabulary, rhythm, structure) and extract non-negotiable constraints.
2. **Reconstruction**: rewrite with the diagnosis in mind, then validate that nothing important changed.

## Hard rules (never violate)

- Never add facts, stats, quotes, names, or claims not in the source.
- Never change numbers, dates, URLs, code, or quoted text unless the user asks.
- Never introduce new AI-isms while removing others (the rewrite must pass the same scan).
- Never output a rewrite longer than **130%** of the original without flagging it.
- If the user's text is intentionally informal (slang, fragments, profanity), match that register. Don't “correct” it into professional prose.

## Progressive disclosure: what to load (and when)

Load only what you need. Use this as a routing map.

| Resource | Load when... |
|---|---|
| `references/fact-preservation.md` | Diagnosis: constraint extraction |
| `references/taboo-phrases.md` | Diagnosis: AI-ism scan; Validation: phrase scan |
| `references/structural-tells.md` | Diagnosis: structure analysis |
| `references/presets/<name>.md` | After preset selection |
| `references/edit-library.md` | Reconstruction (rewrite moves) |
| `references/rubric.md` | Self-scoring / QA (final pass) |
| `assets/examples/` | Calibration only if unsure what “good” looks like |
| `assets/twitter-post.png` | Context for the system concept (not required for execution) |

## Workflow

### 0) Decide output mode

Default output is **just the rewritten text**.

Only include a diagnostics report if:
- the user asked for it, or
- validation fails and you need to explain what broke.

### 1) Pass 1 — Diagnosis (required)

**Goal:** produce a concrete, testable plan (not vibes).

1) **Identify audience + intent**
- Who is the reader?
- What’s the desired effect (inform, persuade, apologize, sell, teach)?
- What tone fits (formal, casual, confident, warm, blunt)?

2) **Pick a preset (routing)**
- `crisp-human`: terse, direct, minimal fluff.
- `warm-human`: friendly, empathetic, gentle rhythm.
- `expert-human`: confident, precise, not salesy.
- `story-lean`: narrative flow with one concrete example (no invented facts).

If the user doesn’t specify, infer from the text and context.

3) **Extract “must-keep” facts**
- Apply `references/fact-preservation.md`.
- If tools are available, run:
  - `python scripts/extract_constraints.py --stdin --out constraints.json`
- Then sanity-check the JSON and **manually add** any missing:
  - proper nouns, product names, titles, quoted strings, identifiers.

4) **Scan for banned phrases**
- If tools are available:
  - `python scripts/banned_phrase_scan.py --taboo references/taboo-phrases.md --stdin`
- Otherwise, use `references/taboo-phrases.md` as a checklist.

5) **Check rhythm + repetition**
- Flag:
  - repetitive sentence length,
  - repetitive sentence starters (“This… This… This…”),
  - listicle cadence (every paragraph the same shape).
- If tools are available:
  - `python scripts/readability_metrics.py --stdin`

6) **Scan for structural AI patterns**
Structural tells are often louder than vocabulary now.

- Check for:
  - participial phrase overuse (“X..., enabling/creating/revealing Y”),
  - em dash overuse (**>2 per 500 words** is suspicious),
  - tricolon / “rule of three” abuse (“X, Y, and Z” repeated),
  - hyper-symmetry (paragraphs of near-identical length),
  - five-paragraph essay template (intro + 3 body + conclusion),
  - “from X to Y” range constructions,
  - correlative conjunction stacking (“not only...but also”, “whether...or”).
- See `references/structural-tells.md`.

### 2) Pass 2 — Reconstruction (required)

**Goal:** rewrite using Diagnosis outputs.

Rules:

- **Preserve every must-keep fact** (exact text match for numbers/dates/URLs/quotes/code unless user requests otherwise).
- Use rewrite moves from `references/edit-library.md`.
- Follow the selected preset (`references/presets/<name>.md`).
- Vary rhythm naturally: mix short, medium, and occasional long sentences. Avoid “metronome” pacing.
- Replace abstract verbs with concrete ones. Prefer concrete nouns over abstractions.
- Cut template structures (throat-clearing intros, recap conclusions, forced transitions).
- **Length guardrail:** target output within **±15%** of the original word count. If you need to go over, say why (e.g., clarifying ambiguity the user asked you to clarify).

### 3) Validate (required)

If tools are available, validate the draft.

Recommended sequence:

1) **Fact preservation**
- `python scripts/validate_preservation.py --constraints constraints.json --stdin`

2) **Banned phrase + structural flag scan**
- `python scripts/banned_phrase_scan.py --taboo references/taboo-phrases.md --stdin`

3) **Readability + rhythm + structural metrics**
- `python scripts/readability_metrics.py --stdin`
- Target: most sentences ~8–25 words, but not rigid. Avoid low variance.
- Structural red flags should be reduced (not necessarily driven to zero).

4) **Diff + length guardrail**
- Default max change is **40%** (to prevent rewriting into a different message).
- `python scripts/diff_check.py --before before.txt --after after.txt --max-change 0.40`
- Flag if word-count ratio is > **1.3** (bloat) or < **0.6** (over-compression).

If any validator fails, revise and re-run until it passes (or explain why a constraint is impossible).

### 4) Self-score with the rubric (recommended)

Use `references/rubric.md` and aim for:

- average **>= 4.0**, and
- **no** individual trait below **4**.

If you score <4 anywhere, do another targeted edit pass focused on that trait.

## Example invocations

Conversational:
- “Make this sound human, but keep every number and name exactly the same: …”
- “Humanize this LinkedIn post. Keep it crisp.”
- “Rewrite this email so it doesn't read like ChatGPT wrote it.”

Claude Code:
- `humanize crisp-human path/to/draft.md`
