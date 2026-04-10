# Polish Checklist

Detailed procedure for Pass 4: transforming the structured draft into the final deliverable. This is where craft matters — the difference between a useful document and one people actually want to read.

## Stage 1: Spec Compliance

Borrowed from superpowers-methodology's two-stage self-review. First check: did you build what was asked?

### Checklist

- [ ] Every section in the approved skeleton has content (no empty sections)
- [ ] Output matches the agreed format (skill package or reference document)
- [ ] All user decisions from between-pass check-ins are honored (reinstated items included, excluded items absent, architecture approved)
- [ ] Compression ratio is reasonable: 40-60% reduction from total input is typical for multi-report distillation. <30% suggests under-filtering. >70% suggests over-filtering — audit for lost gems.
- [ ] All pending conflicts have been resolved (either by user decision or by your final assessment if user delegated)
- [ ] Working document metadata is current and accurate

## Stage 2: Language Tightening

Transform verbose explanations into concise imperatives.

### Rules

**For rules and specifications:** Use imperative voice. "It is recommended that developers should consider using" → "Use." Strip "should," "consider," "may want to," "it is important to" wrappers.

**For explanations and rationale:** Use declarative voice. "The reason why this approach is preferred by many practitioners is that it reduces" → "This reduces." One clause where possible.

**For comparisons:** Lead with the differentiator. "Both tools can do X, but Tool A is faster" → "Tool A is faster at X. Tool B matches on features but not speed."

**For examples:** Show, don't narrate. "The following example demonstrates how to properly configure X" → just show the configuration with a brief label.

### Common tightening patterns

| Verbose | Tight |
|---|---|
| "In order to achieve X, you should..." | "To achieve X:" |
| "It is worth noting that X can cause Y" | "X causes Y" |
| "One approach that has been found to be effective is" | "Effective approach:" |
| "There are several factors to consider, including" | "Key factors:" |
| "This is particularly important when" | "Especially when" or "Critical for" |
| "The following table provides an overview of" | [just show the table with a descriptive caption] |

### Kill list — words and phrases to eliminate on sight

| Eliminate | Replace with |
|---|---|
| "In order to" | "To" |
| "It should be noted that" | Delete — just state the thing |
| "As mentioned earlier/above" | Delete — good structure makes these unnecessary |
| "Basically" / "Essentially" / "Fundamentally" | Delete or replace with the actual clarification |
| "Leverage" | "Use" |
| "Utilize" | "Use" |
| "Facilitate" | "Enable" or "Allow" or describe what happens |
| "Robust" / "Comprehensive" / "Powerful" | Delete unless you can quantify the claim |
| "Ecosystem" (for tools) | "Tools" or "Stack" |
| "Seamless" / "Streamlined" | Delete |
| "Best-in-class" | Delete |
| "Key" / "Critical" / "Crucial" | Delete unless the item would genuinely fail without this |
| "It is important to" | Delete — start with the actual instruction |
| "There are several X, including" | "[List the X directly]" |
| "It's worth noting that" | Delete wrapper, keep content |

**Budget:** Final output should average 15-25 words per sentence for body text. Specification entries can be shorter. Explanatory paragraphs can be slightly longer. If your average exceeds 30 words/sentence, tighten.

## Stage 3: Consistency Pass

Enforce uniform conventions throughout the document.

### Terminology
Scan for the same concept being called different things. Common examples:
- "cell padding" vs "cell margin" vs "cell spacing"
- "typeface" vs "font" vs "font family"
- "endpoint" vs "route" vs "URL"
Pick one term and use it everywhere. Add a note at first use if the chosen term might surprise the reader.

### Formatting
- All specifications in the same format (if some use inline code and others use plain text, standardize)
- All examples in the same structure (if some have labels and others don't, add labels to all)
- All tables use the same column conventions
- All decision trees use the same visual format

### Tone
- Rules and specifications: imperative and neutral ("Use X." "Set Y to Z.")
- Explanations and rationale: declarative and concise ("This prevents X." "Y improves Z.")
- Comparisons: neutral — don't editorialize unless there's a clear winner with evidence
- Failure modes: direct but not alarming ("This breaks when..." not "WARNING: CRITICAL FAILURE")

### Style
- Capitalization: match the output format's conventions (sentence case for docs, title case for headings if the skill template uses it)
- Punctuation: consistent list item endings (all periods, or all no periods — don't mix)
- Code formatting: consistent use of inline code for values, parameters, filenames

## Stage 4: Actionability Audit

The core always-on rule operationalized. Read every rule, specification, and recommendation and ask:

**"Could someone implement this right now with no additional research?"**

If the answer is no:
1. **Can you fill the gap from items in the working document?** Check Cut Items — something useful might have been cut during dedup.
2. **Can you fill the gap from your own knowledge?** If you're confident about the missing detail, add it with a `[enriched during polish]` note.
3. **Is the gap small enough to ignore?** If implementation requires one quick google search, it's probably fine. Flag it with a parenthetical: "(see [tool name] docs for exact syntax)."
4. **Is the gap too large to patch?** Flag it in the Confidence Notes section: "This recommendation needs follow-up research on [specific gap] before implementation."

### Actionability red flags
- A rule that says "use X" without saying how to configure X
- A comparison that says "A is better for Y" without saying what "better" means specifically
- A decision tree that ends with "evaluate your needs" instead of concrete criteria
- An example that shows correct output but not the input or process that produced it

## Stage 5: Loss Check

Compare the working document's high-confidence Active Items against the final output.

### Procedure

1. List all items tagged `confidence: high` in the working document
2. For each: does the item's core claim appear in the final output? (Not necessarily verbatim — the claim may have been reorganized, combined, or reworded)
3. Any high-confidence item NOT present in the final output is a potential loss
4. For each potential loss:
   - Was it intentionally cut during architecture (no good section for it)? → Fix the architecture or add a section
   - Was it accidentally dropped? → Find it a home
   - Was it merged into another item and the merge lost specificity? → Restore the lost detail
5. Log losses found and resolved

### Acceptable loss
Some high-confidence items may legitimately not belong in the final output:
- Items that turned out to be tangential to the distillation's scope
- Items that are redundant with a better-expressed version already in the output
- Items that the user explicitly deprioritized

Log these as "intentional exclusion" in the working document, not as losses.

## Stage 6: Final Slop Check

One last pass with the slop filter active. This catches AI-isms that crept in during architecture and polish — it's common for connecting text, section introductions, and transition sentences to introduce generic language even when all the extracted items were clean.

### What to scan
- Section introductions (the text before the first rule/spec in each section)
- Transition sentences between items
- Table captions and list preambles
- The "How to use this document" section (often written from scratch during architecture — high slop risk)
- Any text you WROTE during polish that wasn't extracted from reports

### Quick check
Read the output as if you're a hostile reviewer looking for AI tells. Does any sentence sound like it could apply to any document by swapping one noun? Cut it or make it specific.

## Stage 7: Output-Format-Specific Finishing

### For Skill Packages
Load `references/skill-output-guide.md` and verify:
- [ ] SKILL.md is under 500 lines
- [ ] Routing table is complete (every reference file has an entry)
- [ ] Always-on rules are present (5-10 max)
- [ ] Frontmatter description is aggressive enough to trigger correctly
- [ ] Feedback loop section is included
- [ ] Reference files are properly named and linked
- [ ] Each reference file is under 300 lines
- [ ] FEEDBACK.md has the standard header

### For Reference Documents
Load `references/document-output-guide.md` and verify:
- [ ] "How to use this document" section is present and accurate
- [ ] Core principles are 5-10, each with rationale and implementation guidance
- [ ] All cross-references point to real sections
- [ ] Reference tables are present (if applicable)
- [ ] Confidence notes section covers items with thin sourcing
- [ ] Sources section lists contributing reports with quality scores

## Reporting to User

Present the final output with a brief summary:

```
## Distillation Complete

**Input:** [n] reports, [total tokens] tokens, quality range [low]-[high]
**Output:** [format] — [line count] lines across [file count] files

**Compression:** [items extracted] items extracted → [items in output] items in final output ([percentage]% reduction)
**Confidence:** [high]H / [medium]M / [low]L in final output
**Loss check:** [count] high-confidence items verified present; [count] intentional exclusions

[Any caveats: thin areas, unresolved soft conflicts, areas flagged for follow-up research]
```

Present the file(s) for the user to review.
