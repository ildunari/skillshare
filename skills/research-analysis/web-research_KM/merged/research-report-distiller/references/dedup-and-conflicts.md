# Dedup & Conflict Resolution

Detailed procedure for Pass 2: merging duplicates, resolving contradictions, and applying the second slop filter pass.

## Phase 1: Group Similar Items

Read through all Active Items in the working document. Cluster items that address the same topic or make the same recommendation.

### Similarity Levels

| Level | Definition | Action |
|---|---|---|
| **Exact duplicate** | Same claim, same level of specificity, possibly different wording | Merge. Keep the version with better sourcing or clearer language. |
| **Near-duplicate** | Same core recommendation, different level of detail or scope | Merge into enriched version. Use the more specific version as base, add unique details from the other. |
| **Related** | Same domain/topic, but making genuinely different claims or covering different aspects | Keep both. Add cross-reference notes between them. |
| **Superficially similar** | Same keywords but different actual meaning or context | Keep both. No action needed. |

### Grouping Procedure

1. Sort items by Type first (all rules together, all specifications together, etc.)
2. Within each type, look for topic clusters (items about the same subject)
3. Within each topic cluster, assess similarity level using the table above
4. Mark pairs/groups for merge, cross-reference, or no-action

Don't try to cluster everything perfectly on the first pass. Start with obvious pairs, then look for subtler connections.

## Phase 2: Merge Duplicates

For each merge candidate pair/group:

### Merge Protocol

1. **Pick the base version.** The item with the highest combination of:
   - Confidence level (high > medium > low)
   - Specificity (concrete values > general principles)
   - Source quality (sourced > unsourced; higher quality report > lower)

2. **Enrich from duplicates.** Scan each duplicate for unique details not in the base:
   - Additional conditions or edge cases
   - More specific values or configurations
   - Better examples
   - Additional sources
   - Failure modes or limitations

3. **Write the merged item.** Add the enriched content to the base item. Update its tags:
   - **Status:** `merged-from-[ITEM-nnn, ITEM-nnn]`
   - **Confidence:** Upgrade if multiple independent sources now support it. A medium-confidence item corroborated by a second independent source becomes high-confidence.
   - **Source:** List all contributing sources: `R1 § section, R3 § section`

**Example merge:**

```
Report A (score 4.2): "Body text line-height: 1.4-1.6 for readability"
Report B (score 3.1): "Use appropriate line spacing, generally around 1.5"
Report C (score 4.5): "Line-height: 1.4-1.6 for body (research: Dyson, 2004), 1.1-1.2 for headings"

→ Merged item (base: Report C, enriched from A):
  "Line-height: 1.4-1.6 for body text (Dyson, 2004), 1.1-1.2 for headings."
  Confidence: high (3 reports converge, 1 cites research)
  Sources: R1 § Typography, R2 § Spacing, R3 § Line Height
  Report B's version → CUT (duplicate-of-ITEM-nnn, fully subsumed)
```

4. **Move duplicates to Cut Items.** Reason: `duplicate-of-ITEM-[nnn]`

### Compression Tracking

Track items before dedup → items after. A healthy compression ratio is 20-40% for 3+ reports on the same topic. Below 10%: reports may not overlap much (fine) or grouping is too granular (review). Above 50%: reports were largely redundant.

### Confidence Adjustment Rules

| Scenario | Adjustment |
|---|---|
| Two independent reports make the same specific claim | Upgrade to high (if not already) |
| Three+ reports agree on the same recommendation | High confidence, note as "consensus" |
| One sourced claim matches one unsourced claim | Keep sourced version's confidence, note corroboration |
| Two unsourced claims agree | Upgrade to medium (not high — could be shared misconception) |
| One report's claim is more specific than another's | Adopt the more specific version; confidence follows the specific version's confidence |

## Phase 3: Resolve Conflicts

When two or more items contradict each other on the same topic.

### Conflict Resolution Decision Tree

```
1. CHECK SOURCING QUALITY
   Item A has citations/data AND Item B does not?
     → Favor A. Move B to Cut Items. Reason: "superseded by better-sourced ITEM-[A]"
   Both have citations?
     → Continue to step 2
   Neither has citations?
     → Continue to step 2

2. CHECK CONSENSUS
   Do 3+ reports agree with one position and only 1 disagrees?
     → Favor the majority position. Keep the dissent as a NOTE on the surviving item:
       "Note: R[n] disagrees, arguing [brief summary]. Included here for completeness."
   Split evenly (2 vs 2, or 1 vs 1)?
     → Continue to step 3

3. CHECK RECENCY
   Is this a fast-moving topic (tools, APIs, versions, market conditions)?
     → Favor the more recent source. Tag: "Preferred based on recency; older sources recommended [alternative]."
   Is this a stable topic (principles, algorithms, physics)?
     → Recency doesn't matter. Continue to step 4.

4. CHECK REPORT QUALITY SCORE
   Is one report significantly higher quality (>1.0 difference in composite)?
     → Favor the higher-quality report's position. The reasoning: higher-quality reports
       have demonstrated better judgment and specificity overall.
   Quality scores are similar?
     → Continue to step 5

5. FLAG FOR USER DECISION
   Create a CONFLICT entry in the working document. Present both positions with your assessment.
   Do NOT silently pick one.
```

### Presenting Conflicts to User

For each unresolvable conflict, present:

```
**Conflict: [topic]**

Position A (from R[n], quality [score]):
[Specific claim with context]

Position B (from R[n], quality [score]):
[Specific claim with context]

My assessment: [Which is likely correct and why, based on available evidence.
If genuinely uncertain, say so.]

Recommendation: [Keep A / Keep B / Keep both with scope notes / Need more info]
```

Use `ask_user_input` to collect the user's decision (A / B / keep both / need more info). If they don't want to decide ("just pick one"), apply your assessment and record it as a judgment call in the CONFLICT entry.

## Phase 4: Second Slop Filter Pass

After dedup and conflict resolution, re-read all surviving Active Items with fresh eyes.

### What the second pass catches

Items that looked acceptable during extraction often reveal themselves as generic when you can now see them in context:

1. **Outclassed items.** Item says "use appropriate spacing." Another item (from a better report) says "use 8px spacing scale: 8/16/24/32/48/64px." The vague version survived Pass 1 because it was the only spacing item at the time. Now it's clearly outclassed. Cut it. Reason: `superseded-by-ITEM-[nnn]`

2. **Orphaned enrichment flags.** Items tagged `[NEEDS-ENRICHMENT]` during extraction that never got enriched. If no other report provided the missing specificity, these are vague principles that didn't pan out. Cut them unless they're genuinely the only coverage of an important topic.

3. **Redundant low-confidence items.** Low-confidence items that now overlap with high-confidence items on the same topic. The high-confidence version should have absorbed anything useful during merge. If the low-confidence item still exists separately, it's probably noise.

4. **Topic drift.** Items that seemed relevant during extraction but, now that you can see the full item set, are actually tangential to the distillation's purpose. Example: extracting a CSS trick from a report about data visualization — useful in isolation, but if the distillation is about visualization best practices, not CSS techniques, it doesn't belong.

### Second pass procedure

1. Re-read the slop filter (`references/slop-filter.md`) — refresh the patterns
2. Walk through all Active Items sequentially
3. For each item, ask: "Is there a more specific version of this claim already in the working document?" If yes, and this item adds nothing unique, cut it.
4. Check STRUCTURAL_FLAGS: uniform abstraction, mirror structure, one-source dominance, confidence clustering, template generation
5. Update Pipeline Stats with the new counts

## Reporting to User After Pass 2

```
## Pass 2 Complete: Dedup & Resolve Summary

**Before dedup:** [count] items
**After dedup:** [count] items
**Compression ratio:** [percentage] reduction

**Merges:** [count] merge groups resolved
**Conflicts found:** [count]
  - Resolved by evidence: [count]
  - Resolved by consensus: [count]
  - Resolved by recency: [count]
  - Flagged for your decision: [count]

**Second slop pass:** [count] additional items cut
  - Outclassed by better version: [count]
  - Orphaned enrichment: [count]
  - Redundant low-confidence: [count]
  - Topic drift: [count]

**Current confidence distribution:** [high]H / [medium]M / [low]L

[Conflicts awaiting your decision, if any — present each one]

Ready for Pass 3 (Architecture)?
```
