# Fact Preservation Rules

**Non-negotiable:** preserve meaning and every factual element the user didn’t explicitly authorize you to change.

This skill treats “facts” as *verbatim tokens* in many cases because accidental drift is common during rewrites.

---

## What must not change (default)

### Always preserve verbatim

- **Numbers**: counts, prices, percentages, measurements, ranges, versions (e.g., `3.5`, `v2`, `40%`, `1–2 weeks`)
- **Dates and times**: `2026-01-12`, `Jan 12, 2026`, `Q4 2025`, `9:30am`
- **Proper nouns**: people, companies, product names, project names, org names
- **Identifiers**: emails, phone numbers, ticket IDs, invoice numbers, addresses
- **URLs**
- **Quotes**: anything inside quotation marks the user provided
- **Code / commands**: fenced code blocks and inline code
- **Legal/compliance language**: disclaimers, policy text, contract clauses
- **Citations**: bracketed refs, DOIs, footnotes, URLs

### Usually preserve (unless user asks to change)

- **Units** (don’t convert kg→lb, USD→EUR, etc.)
- **Named claims** (e.g., “we shipped X”, “we tested Y”)
- **Attribution** (who said/did what)

---

## What you *can* change safely

- Word order around facts
- Punctuation and paragraphing
- Verb tense (if it doesn’t change meaning)
- Active vs passive voice (if actor stays the same)
- Replacing vague words with clearer ones **without adding new facts**

---

## Workflow for preserving facts

1. **Extract constraints**
   - Use `scripts/extract_constraints.py` when possible to capture obvious hard facts (numbers, dates, URLs, quotes, code).
2. **Manually add missing facts**
   - The extractor can’t reliably identify every proper noun.
   - In Diagnosis, add must-keep items like company names, product names, and titles.
3. **Rewrite around the facts**
   - Treat must-keep items like “islands” you build sentences around.
4. **Validate**
   - Run `scripts/validate_preservation.py` and fix any missing items.

---

## If the input fact looks wrong

Do **not** correct it unless the user explicitly asked for fact-checking. You may *flag it* as a potential issue in diagnostics:

- “You wrote X. If that number/date is a typo, tell me and I’ll update it.”

---

## Edge cases

- **Reformatting** (e.g., `1,000` → `1000`) counts as a change. Don’t do it unless requested.
- **Smart quotes** vs straight quotes: keep the user’s original quote characters when possible.
- **Headers/bullets**: you may restructure, but preserve factual tokens.
