# Slop Filter

Machine-readable pattern lists for identifying filler, noise, and non-actionable content in research reports. Applied during Pass 1 (extraction) and again during Pass 2 (dedup comparison).

This filter is tuned for **research distillation**, not conversational rewriting. Some formal connectives that would be flagged in humanize-ai-content are acceptable here (e.g., "however" in a technical comparison is fine). The focus is on empty calories — content that takes up space without adding actionable information.

## How to Apply

**During Pass 1 (extraction):**
For each candidate item, check against HARD_REJECT first. If it matches, skip extraction entirely. Then check SOFT_FLAGS — if 2+ soft flags appear in a single item, treat it as a hard reject unless you can clearly rescue a specific, concrete gem. STRUCTURAL_FLAGS apply to groups of items, not individuals.

**During Pass 2 (dedup):**
Re-check all surviving items. Items that looked acceptable in isolation often reveal themselves as generic when you can see a better version of the same claim from another report. An item that's a SOFT_FLAG in isolation becomes a HARD_REJECT if a more specific version exists.

**Override rule:** If the user explicitly reinstates a filtered item, respect that. Log the pattern to FEEDBACK.md — the filter may be miscalibrated for this domain.

**The three-second test:** Read any extracted item and ask: "Could someone implement this right now with no additional research?" Yes → keep. Partially → flag as medium confidence. No → cut.

---

## HARD_REJECT

Content that never survives extraction. No exceptions unless the user overrides.

### Empty framing
- Introductions that restate the research question without answering it
- "In conclusion" / "To summarize" / "In summary" paragraphs that repeat prior content
- "As we explore..." / "Let's dive into..." / "In this section we will..." throat-clearing
- "It's important to note that..." / "It's worth mentioning..." wrapper sentences (delete the wrapper, keep the content if the content is actionable)
- Transition paragraphs between sections that contain zero new information
- "This area deserves further investigation" without specifying what or why
- Meta-commentary about the research process itself ("After extensive research...")
- "Moving on to another important aspect..." / "Furthermore, it should be noted..."
- Table of contents entries and section headers without content beneath them

### Definitional padding
- Definitions of basic terms the reader already knows (unless the distillation is for beginners and the user said so)
- "X is defined as..." / "Typography refers to the art of arranging type..."
- Wikipedia-style background paragraphs that any practitioner would skip
- Scope padding — three paragraphs explaining why the topic matters before any actual content

### Circular content

- Items that restate another item in different words without adding information
- "As mentioned above..." / "As noted earlier..." references that add nothing
- Executive summary content that duplicates the body (keep the body version)

Common circular patterns (hard reject):

| Pattern | Example | Why it's a hard reject |
|---|---|---|
| Tautology dressed as advice | "Choose the right tool for the job" | Says nothing. What tool? What job? What criteria? |
| Hedge stack | "It might be worth considering whether it could potentially be beneficial to..." | Four layers of uncertainty = zero information |
| Importance declaration | "It's important to note that accessibility matters" | Declaring importance ≠ providing guidance |
| Restated prompt | "When building dashboards, it's crucial to think about the user" | Yes, that's why we're here. What specifically? |
| Obvious implication | "Using red for errors helps users identify problems" | Explains the definition of the thing, not how to apply it |

### AI-generated filler
- "Comprehensive overview" / "holistic approach" / "robust framework" without specifics
- "This powerful approach enables remarkable flexibility" — adjective-stuffed nothing-sentence
- Claims followed by no evidence, no source, no concrete detail
- Paragraphs that could apply to any topic by swapping one noun ("This technology continues to evolve rapidly and presents both opportunities and challenges")
- Lists where every item is at the same level of abstraction with no concrete values or examples
- "Best practices include: [list of generic advice that could come from any domain]"

## /HARD_REJECT

---

## SOFT_FLAGS

Not always wrong, but frequently a sign of shallow content. Apply judgment. Extract the gem, discard the wrapper.

### Vague recommendations

| Pattern | What to look for | Action |
|---|---|---|
| "Consider using..." | Either recommend it or don't | Keep ONLY if followed by specific criteria for when to use it |
| "Use appropriate X" / "Ensure adequate Y" | Appropriate according to what? | Keep ONLY if specific values follow |
| "Follow best practices for X" | Which practices? What X? | Keep ONLY if the practices are enumerated |
| Conditional without specificity | "For complex dashboards, consider a grid system" | Rescue if you can extract the threshold and specific recommendation |

### Principles without implementation
- "Maintain visual hierarchy" → keep ONLY if followed by specific techniques (font sizes, weight ratios, spacing values). Cut the principle statement, keep the techniques
- "Use a consistent color palette" → keep ONLY if the palette is specified or criteria for choosing one are given
- Recommendation without rationale (e.g., "Use 16px as minimum body font size") → borderline. Keep the spec, flag as needing rationale if none is provided elsewhere

### Unsourced assertions
- "Studies show..." / "Research indicates..." / "Experts recommend..." without naming the studies, research, or experts
- "It is widely accepted that..." / "The consensus is..." without evidence of that consensus
- Comparative claims without criteria ("X is better than Y" — better how? measured by what?)

### Sourced generalities
- Famous findings broadly known (e.g., "According to Nielsen Norman Group, users scan in an F-pattern"). Keep only if the report adds specific application guidance beyond the citation

### Surface-level comparisons
- Feature checklists without tradeoff analysis (X has feature A, Y has feature B — so what?)
- "Pros and cons" lists where every item is one vague sentence
- Tool comparisons that read like marketing copy for all tools simultaneously

### Dated or unverifiable claims
- Recommendations citing specific tool versions without noting the version (may be outdated)
- "Currently, the best approach is..." without a date anchor
- Performance claims without benchmark methodology

### Examples without generalization
- A detailed case study with no extractable principle. Keep if concrete enough to serve as a template. Cut if it's just a story

**The 2+ rule:** If a single item triggers 2 or more soft flags, treat it as a hard reject unless you can identify a specific concrete gem buried inside it.

## /SOFT_FLAGS

---

## STRUCTURAL_FLAGS

These apply to groups of extracted items, not individuals. They indicate systematic extraction problems.

### Uniform abstraction level
All extracted items from a report are at the same granularity — either all principles with no specs, or all specs with no context. Sign of surface-level extraction. Go back and extract at multiple levels.

### Mirror structure
Extracted items follow the source report's section structure exactly. Sign of copying the outline instead of extracting the gems. Reorganize around what the reader needs to DO, not how the source was organized.

### One-source dominance
80%+ of extracted items come from a single report despite multiple reports being processed. Either the other reports are genuinely low quality (check quality scores) or extraction was too shallow on them.

### Confidence clustering
All items tagged the same confidence level. Real extraction produces a distribution. If everything is "medium," the tagger is being lazy — force differentiation.

### Template generation
Multiple items use identical phrasing patterns with only one noun swapped. Sign of LLM generating items instead of extracting them from the source. Every item should trace to a specific passage in a specific report.

## /STRUCTURAL_FLAGS

---

## Domain-Specific Calibration

| Domain | More permissive on | More aggressive on |
|---|---|---|
| **Technical/engineering** | Formal connectives connecting genuinely different points | Vague performance claims without benchmarks |
| **Scientific/academic** | Hedging ("may," "suggests," "is associated with") — appropriate caution | Claims without citations |
| **Business/strategy** | Qualitative assessments when quantitative data doesn't exist | Buzzwords and marketing language |
| **Creative/design** | Subjective judgments ("this feels more polished") | Generic aesthetic advice without concrete specifications |

If a domain calibration repeatedly comes up, log to FEEDBACK.md for potential promotion to a permanent preset.

## Anti-Slop Litmus Test

Before including ANY item in the final output, it must pass ALL of these:

- [ ] **Specific** — Contains concrete values, names, tools, thresholds, or steps
- [ ] **Novel** — Tells the reader something they wouldn't know from the section header alone
- [ ] **Actionable** — Reader can implement immediately without additional research
- [ ] **Earned** — Not padding the section to look more comprehensive
- [ ] **Irreducible** — Can't be shortened without losing information

If it fails any one, it's out.
