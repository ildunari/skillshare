# Reporting Requirements Guide

How to write the section that turns a research prompt from "produce an overview" into "produce a practitioner-grade reference document." This is the single highest-leverage addition to any research prompt — without it, research tools optimize for breadth coverage and minimum viable output.

## Why this section exists

Research tools (Deep Research, Perplexity, AI agents) treat your prompt as a ceiling, not a floor. If you say "target 3-6k words," you'll get 3k. If you say nothing about output quality, you'll get a summary blog post. The reporting requirements section is your enforcer — it defines what "good output" looks like in concrete, countable terms that the research tool can't hand-wave past.

## The three components

Every reporting requirements section needs three things:

1. **Section structure template** — how each section should be organized
2. **Minimum deliverables** — countable items the output must contain
3. **Anti-padding rules** — what to explicitly exclude

### Component 1: Section structure template

Tell the research tool how to organize each major section. This framework produces depth:

```
Structure each major section with:
- The principle or pattern being described
- Why it matters (what fails without it)
- Concrete examples — real copy-paste-ready content, not pseudocode or descriptions
- Before/after comparisons where a pattern was improved
- [Domain]-specific callouts (flag anything that differs between [variants])
- Source citation for every non-obvious claim
```

Adapt the bracketed items per topic. For a coding tool, "[Domain]-specific" becomes "Model-specific" with the variants listed. For a scientific topic, it becomes "methodology-specific" or "field-specific."

The key elements are:
- **"Why it matters"** forces the tool to explain consequences, not just state facts
- **"Concrete examples"** with "not pseudocode" prevents abstract descriptions of what examples would look like
- **"Before/after comparisons"** is the single most effective depth driver — it forces the tool to find real improvements
- **"Source citation for every non-obvious claim"** prevents hallucinated assertions

### Component 2: Minimum deliverables

Write countable requirements. The research tool can verify whether it met these or not.

**Weak (unenforceable):**
> Be thorough and provide examples where relevant.

**Strong (countable):**
> Include at minimum:
> - 2-3 complete system prompt templates for different use cases
> - 5+ concrete tool description examples showing good vs bad patterns
> - 3+ detailed failure case studies with diagnosis and fix
> - A calibration table mapping task types to recommended settings
> - A migration checklist for moving from [old] to [new]

Rules for writing minimum deliverables:
- Every item should be countable (N templates, N examples, N case studies)
- Include at least one "complete template" requirement (forces end-to-end depth, not snippets)
- Include at least one "table or matrix" requirement (forces structured comparison)
- Include at least one "failure case study" requirement (forces practical depth over theory)
- Include at least one "before/after" requirement (forces concrete improvement examples)
- Calibrate the numbers to the topic complexity — don't ask for 10 templates on a narrow topic

### Component 3: Anti-padding rules ("Do not" section)

Without explicit exclusions, research tools pad with beginner advice, marketing summaries, generic safety content, and advice that applies to any tool/model/domain without specific evidence.

**Template:**
```
Do not:
- Repeat beginner [domain] advice ([specific examples of what to skip])
- Pad with generic [safety/ethics/marketing] content
- Summarize [company]'s marketing materials or announcement blog posts
- Cover [irrelevant adjacent topics] unless directly illuminating
- Provide advice that applies equally to any [tool/model/method] without [domain]-specific evidence
```

The last bullet is the most important. "Provide advice that applies equally to any LLM without GPT-5.x-specific evidence" forces model-specific depth across the entire report. Adapt this pattern to any domain:
- "...without Python-specific evidence" (for a Python research prompt)
- "...without clinical trial evidence" (for a medical research prompt)
- "...without production deployment data" (for an infrastructure research prompt)

## Word target calibration

Research tools treat word targets as ceilings. Set targets 2-3x higher than what you actually expect.

| Actual desired output | Set target to | Expected result |
|---|---|---|
| ~4k words (focused overview) | 6-8k words | 4-5k words |
| ~8k words (thorough reference) | 10-15k words | 6-10k words |
| ~12k+ words (comprehensive guide) | 15-20k words | 8-15k words |

Always pair the word target with: **"Prioritize depth over breadth. If you find one area has exceptionally rich practitioner data, spend 3000 words there rather than giving 500 words to eight areas. Let the density of available information guide section length."**

This instruction gives the tool permission to go deep on high-signal areas instead of spreading thin across everything.

## Complete examples at three complexity levels

### Light (simple topic, focused research)

```
## Reporting Requirements

Target 6,000-8,000 words. Structure each section with the principle, why it matters,
and at least one concrete example. Cite sources for non-obvious claims.

Include at minimum:
- 3+ concrete configuration examples
- 1 comparison table ([A] vs [B] for key behaviors)
- 2+ failure mode descriptions with mitigations

Do not repeat beginner setup instructions or summarize marketing announcements.
Prioritize depth over breadth.
```

### Standard (most research — the default)

```
## Reporting Requirements

Target 8,000-12,000 words organized into clearly delineated sections.

Structure each major section with:
- The principle or pattern being described
- Why it matters (what fails without it)
- Concrete examples — real copy-paste-ready content, not pseudocode
- Before/after comparisons where applicable
- [Domain]-specific callouts where behavior differs between [variants]
- Source citation for every non-obvious claim

Include at minimum:
- 2-3 complete [templates/configurations] for different use cases
- 5+ concrete [examples] showing [good vs bad / optimized vs unoptimized] patterns
- 3+ detailed failure case studies with diagnosis and fix
- A [comparison table / decision matrix / calibration guide] for [key decision]
- A [migration checklist / setup guide / workflow] for [common task]

Do not:
- Repeat beginner [domain] advice ([specific examples])
- Pad with generic [safety/ethics] content
- Summarize [company] marketing materials
- Cover [irrelevant adjacent topics]
- Provide advice that applies equally to any [tool/model] without [domain]-specific evidence

Prioritize depth over breadth. Let the density of available information guide section length.
```

### Heavy (practitioner-grade reference document)

```
## Reporting Requirements

This report needs to be substantially more detailed than a typical overview.
Target 10,000-15,000 words organized into clearly delineated sections.

Structure each major section with:
- The principle or pattern being described
- Why it matters (what fails without it)
- Concrete code/prompt/configuration examples — real copy-paste-ready content,
  not pseudocode or descriptions of what examples would look like
- Before/after comparisons where a pattern was improved
- [Domain]-specific callouts (flag anything that differs between [variant A],
  [variant B], and [variant C])
- Source citation for every non-obvious claim

Include at minimum:
- 2-3 complete end-to-end [templates] (not snippets — full documents that
  could be used as starting points)
- 5+ concrete [examples] showing [optimization pattern] with before/after
- 3+ detailed failure case studies with full diagnosis and fix
- A [calibration table] mapping [task types] to recommended [settings/approaches]
- A [comparison table] documenting [key behavioral differences]
- A [migration checklist] for moving from [old version] to [new version]
- [Any domain-specific deliverable: API code examples, workflow diagrams, etc.]

Do not:
- Repeat beginner [domain] advice ([list specific things to skip])
- Pad with generic [safety/ethics/marketing] content
- Summarize [company]'s marketing materials or blog post announcements
- Cover [list irrelevant adjacent topics]
- Provide advice that applies equally to any [tool/model/method] without
  [domain]-specific evidence
- Include content about [out-of-scope items] unless directly comparative

Prioritize depth over breadth. If you find one area has exceptionally rich
practitioner data (e.g., [example area]), spend 3000 words there rather than
giving 500 words to eight areas. Let the density of available information
guide section length.
```

## Common mistakes

- **No reporting requirements at all** — the research tool produces a summary blog post
- **Vague quality language** ("be thorough," "provide good examples") — unenforceable
- **Word target too low** — 3-6k for a complex topic guarantees shallow coverage
- **No anti-padding rules** — the tool pads with beginner advice and marketing
- **Minimum deliverables without "complete"** — asking for "templates" gets snippets; asking for "complete end-to-end templates" gets usable documents
- **No "prioritize depth over breadth"** — the tool spreads thin across all areas equally
