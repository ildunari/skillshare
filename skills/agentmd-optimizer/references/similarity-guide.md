# Similarity Guide

Use this reference when clustering instruction files.

## Three similarity tiers

### Tier 1 — Exact duplicates
Definition: byte-identical files or identical content hashes.

Use when:
- proving that many files are literally the same payload
- estimating obvious duplicate token waste
- scoring canonical source vs copy locations

### Tier 2 — Near duplicates
Definition: files with mostly the same content, but small wrappers, intros, runtime headers, or a few changed sections.

Use heuristics such as:
- normalized sequence similarity
- heading overlap
- line-level Jaccard similarity
- frontmatter-only divergence

Typical interpretation:
- **0.90+**: likely mergeable with thin wrappers
- **0.78–0.89**: manual review; probably derived from one source
- **<0.78**: do not claim near-duplicate status

### Tier 3 — Semantic overlap
Definition: same directives or same meaning with different wording.

This is the least deterministic tier. Use it carefully.

Look for:
- repeated policy themes across files
- same tool preference stated in different words
- same response-style preference restated across runtimes
- copied rules rewritten to sound platform-specific

## Reporting rules

- Never present semantic overlap as if it were exact duplication.
- Report confidence separately for each tier.
- For destructive recommendations, exact or very high near-duplicate evidence should carry the weight — not semantic overlap alone.
- When in doubt, downgrade to “manual review” rather than overclaim similarity.
