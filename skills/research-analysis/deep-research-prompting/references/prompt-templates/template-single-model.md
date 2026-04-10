# Example Template: Single Model/Tool Deep Research Prompt

> This is a complete example showing the structure, tone, and depth expected from a well-written single-model research prompt. Adapt the bracketed content to your specific topic. The structural patterns (section ordering, interrogation-style focus areas, tiered sources, reporting requirements) should be preserved.

---

# PROMPT: [Tool/Model Name] — [Primary Use Case] — Complete Practitioner's Guide

## Context

I'm building and refining [what you're building] for [tool/model/platform]. My use cases span:

1. **[Primary use case]** — [2-sentence description of what you're doing and why it matters]. This is my primary use case.
2. **[Secondary use case]** — [2-sentence description].
3. **[Tertiary use case]** — [2-sentence description].

The output will serve as both a comprehensive reference document I'll consult repeatedly and an immediately applicable guide for [specific application]. I'm an experienced [your background] who works across [relevant tools/domains] daily — skip beginner-level content entirely and focus on [tool/model]-specific behaviors, calibration, and patterns that actually change outcomes at the practitioner level. [If follow-up: I already received a shorter overview report on this topic; this research should go significantly deeper, with more concrete examples, complete templates, and detailed failure case studies.]

## Knowledge Gap

I need a thorough, practitioner-grade understanding of how to [core objective] for [tool/model], including the specific and substantial differences between [variant A], [variant B], and [variant C]. [1-2 sentences explaining why this tool/model requires different treatment than alternatives you already know — what's architecturally or behaviorally different.]

I specifically need depth on areas that surface-level guides skip: [list 4-6 specific gaps — complete templates, tool description copywriting, failure case studies, configuration patterns, calibration methodology, migration gotchas, etc.].

## Focus Areas

- **[Topic 1 — bold label]:** [Beyond basics opener]. [Sub-question about methodology/approach]. [Sub-question requesting concrete examples or before/after comparisons]. [Sub-question about failure modes or known gotchas]. [Sub-question about cross-variant differences]. [Sub-question about practitioner workflow].

- **[Topic 2 — bold label]:** [Beyond basics opener]. [Sub-question 1]. [Sub-question 2]. [Sub-question requesting "show me" concrete examples]. [Sub-question about what breaks]. [Sub-question about comparison with alternative approaches].

- **[Topic 3 — bold label]:** [Continue pattern — 3-6 sub-questions per area, mixing the five question types: beyond basics, show me, what breaks, compare, how should practitioners].

- **[Topic 4]:** [...]

- **[Topic 5]:** [...]

- **[Topic 6]:** [...]

- **[Topics 7-10 if needed for comprehensive single-prompt research]:** [...]

Surface approaches, patterns, or [domain-specific] behaviors I might not be aware of — especially findings from the past [time period] that reflect real production experience. Follow interesting threads you discover during research, even if they don't fit neatly into the focus areas above.

## Reporting Requirements

Target **[8,000-15,000]** words organized into clearly delineated sections.

**Structure each major section with:**
- The principle or pattern being described
- Why it matters (what fails without it)
- Concrete [code/prompt/configuration] examples — real copy-paste-ready content, not pseudocode
- Before/after comparisons where a pattern was improved
- [Variant]-specific callouts (flag anything that differs between [A], [B], and [C])
- Source citation for every non-obvious claim

**Include at minimum:**
- [N] complete end-to-end [templates/configurations] for different use cases
- [N]+ concrete [examples] showing [good vs bad / optimized vs unoptimized] patterns
- [N]+ detailed failure case studies with diagnosis and fix
- A [calibration table / decision matrix] mapping [task types] to recommended [settings]
- A [comparison table / migration checklist] for [relevant transition]
- [Any domain-specific deliverable]

**Do not:**
- Repeat beginner [domain] advice ([specific examples of what to skip])
- Pad with generic [safety/ethics/marketing] content
- Summarize [company]'s marketing materials or blog post announcements
- Cover [list irrelevant adjacent topics]
- Provide advice that applies equally to any [tool/model/method] without [domain]-specific evidence

**Prioritize depth over breadth.** If you find one area has exceptionally rich practitioner data, spend 3000 words there rather than giving 500 words to eight areas. Let the density of available information guide section length.

## Prioritized Sources

Search deeply and exhaustively across these, prioritizing recent content ([time range]):

**Tier 1 — Highest value, search first:**
- **[Primary official resource]** ([URL]): [Why it's valuable — specific guides, examples, or documentation to extract from]
- **[Secondary official resource]** ([URL]): [Description]
[The [specific source] is the gold mine — [1-sentence explanation of why].]

**Tier 2 — Community intelligence:**
- **[Platform]** ([specific communities/subreddits]): [What to look for — experience reports, prompt sharing, bug reports, comparisons]
- **[Platform]** ([specific accounts or communities]): [Description]
- **[Platform]** ([specific repos or issue trackers]): [Description — bug reports and workarounds that reveal real behavior]

**Tier 3 — Practitioner synthesis:**
- **[Blogger/author]** ([URL]): [Specific relevant content]
- **[Platform/publication]**: [What type of content to look for]

**Tier 4 — Comparative context (use sparingly):**
- **[Competing tool/model docs]**: For direct comparison of [specific aspect]

---

## Usage Notes

- **Single prompt** — run as one Deep Research session. The topic is coherent despite its breadth; the source pools overlap heavily.
- **Time-sensitivity is critical.** [Tool/model] [launched/updated] [specific date]. Prioritize the most current sources. Patterns from [old version] may be counterproductive on [new version].
- **If the research tool hits limits:** Prioritize in this order: (1) [Highest value area], (2) [Next], (3) [Next], (4) [Next]. These are the highest-impact areas for my use cases.
- **[Gold mine callout].** The [specific source] contains [specific type of content]. Prioritize extracting and synthesizing patterns from it.
