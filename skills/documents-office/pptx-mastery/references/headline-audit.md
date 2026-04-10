---
title: Assertion Headline Audit
scope: pptx-master
version: 1.0
---

# Assertion Headline Audit

Every content slide must have an assertion headline — a short claim that tells the audience
what to believe after reading the slide, not what topic the slide covers.

---

## The two-part test

A headline passes only if both conditions are true:

1. **Verb present** — contains at least one conjugated verb.
   - ✓ Passing verbs: is, are, was, were, produces, forces, reduces, enables, reveals,
     determines, outperforms, requires, shows, causes, prevents, drives
   - ✗ Failing patterns: gerunds ("using," "leveraging," "understanding"), infinitives as
     topic labels ("to improve clarity"), noun phrases alone ("Advanced Techniques")

2. **Claim present** — makes a falsifiable or comparative statement. A topic label restated
   as a sentence does not qualify.
   - ✓ Claim: "Vague prompts produce unpredictable outputs"
   - ✗ Not a claim: "Prompts can be vague or specific"

Both must be ✓. One ✗ = rewrite required.

---

## Bad → good examples

| Bad (topic label) | Good (assertion) |
|---|---|
| Context is Everything | Missing context forces Claude to guess wrong |
| Being Specific and Clear | Specificity narrows the output space |
| Advanced Techniques | Chain-of-thought prompts unlock multi-step reasoning |
| Core Principles | Four principles separate useful prompts from noise |
| Iterative Refinement | Second-draft prompts consistently outperform first drafts |
| Why Prompting Matters | Prompt quality determines output quality more than model choice |
| Providing Examples | One concrete example beats three sentences of instruction |
| Negative Prompting | Telling Claude what to avoid reduces format errors by half |

---

## Banned headline patterns

Reject any headline matching these patterns — rewrite before proceeding:

- "X is Important" / "X Matters"
- "Understanding X" / "The Role of X"
- "X Best Practices" / "X Tips and Tricks"
- "Advanced X" / "Introduction to X"
- Any headline that could serve as a textbook chapter title without sounding wrong

---

## Length and format rules

- ≤ 12 words
- Sentence case (capitalize first word and proper nouns only)
- No trailing period
- Questions allowed only on hook (S01) and closing slides
- No colons used as topic separators ("Prompting: Why It Matters" → rewrite as assertion)
