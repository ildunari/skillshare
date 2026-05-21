# Token Budget Management

Strategies for handling research input that exceeds comfortable context limits. Load this when total input exceeds ~60k tokens.

## The Problem

Large input sets create two failure modes:
1. **Context overflow:** Can't load all reports simultaneously. Items extracted early may be forgotten by the time later reports are processed.
2. **Quality degradation:** Even within context limits, attention degrades as context grows. Items extracted from report 7 tend to be less carefully evaluated than items from report 1.

The working document solves both problems — it's the persistent state that survives across processing sessions.

## Estimation

Before starting, estimate the total token budget:

| Report size | Typical tokens |
|---|---|
| Short report (2-3 pages, ~1.5k words) | ~2k tokens |
| Medium report (5-10 pages, ~4k words) | ~5.5k tokens |
| Long report (15-25 pages, ~10k words) | ~14k tokens |
| Very long report (30+ pages, ~20k words) | ~27k tokens |

Multiply by number of reports. Add ~20% for the working document's own size as it grows.

## Processing Strategies

### Strategy 1: Sequential Processing (60k-120k tokens)

Process reports one at a time, building the working document incrementally.

**Procedure:**
1. Load the working document (initially empty)
2. Load one report (highest quality first)
3. Run Pass 1 extraction on that report. Write items to working document.
4. Unload the report from active context
5. Load the next report
6. Run Pass 1 extraction. During extraction, check new items against existing working document items for obvious duplicates — don't full-dedup yet, but note likely matches.
7. Repeat for all reports
8. When all reports are processed: the working document contains all extracted items with cross-references noted. Proceed to Pass 2 (dedup) working from the document alone.

**Key rule:** The working document must be loadable at all times. If it grows past ~8k tokens, compress it per the Size Management section of `references/working-document-protocol.md`.

**Context budget per report (approximate):**

| Allocation | Budget | Purpose |
|---|---|---|
| Working document | ~15-20k tokens | Running extraction state — grows with each report |
| Current report | ~30-40k tokens | The report being processed |
| Skill instructions | ~5-8k tokens | SKILL.md + relevant reference files |
| Thinking/generation | ~10-15k tokens | Reasoning and output |

If a single report exceeds 40k tokens, use Strategy 3 (Chunked Processing).

### Strategy 2: Batched Processing (120k-200k tokens)

Group reports into batches of 2-3 that fit comfortably in context alongside the working document.

**Procedure:**
1. Group reports by topic similarity (reports on related topics should be in the same batch — this makes cross-referencing easier)
2. Process each batch as a mini-distillation: load 2-3 reports + working document, extract items, note cross-references within the batch
3. After each batch, compress the working document if needed
4. After all batches: run Pass 2 on the full working document

### Strategy 3: Chunked Reading (single report >40k tokens)

For individual reports that are too large to load at once.

**Procedure:**
1. Load the report's table of contents, introduction, and conclusion first. These give you the report's structure and key claims.
2. Score the report based on the introduction/conclusion pass (this is a provisional score — may be adjusted)
3. Process the report section by section:
   - Load one section at a time
   - Extract items from that section
   - Write to working document
   - Move to next section
4. After processing all sections: review extracted items for coherence (did the section-by-section approach miss cross-section connections?)

## Working Document Size Management

The working document grows with each report. Keep it under ~8k tokens for comfortable loading alongside reports.

### Compression triggers

| Working document size | Action |
|---|---|
| <4k tokens | No compression needed |
| 4-8k tokens | Monitor. Compress if the next report is large. |
| 8-12k tokens | Compress Active Items to summary form |
| >12k tokens | Split into index file + detail files |

### Compression techniques

**Level 1: Summarize items.** Keep title, type, confidence, source, and a 1-line summary. Drop the full content. The full content can be reconstructed during Pass 3 (architecture) from the original report.

```markdown
### ITEM-042 — Inter font stack for UI text
- **Type:** specification | **Confidence:** high | **Source:** R2 § Typography
- **Summary:** Complete font stack with weights, sizes, line-heights for UI text
```

**Level 2: Collapse Cut Items.** Replace the full Cut Items section with a count and reason breakdown. Individual cut items don't need to be preserved if the loss auditor has already been run.

**Level 3: Index + detail split.** Create a companion file (`distill-detail.md`) containing full item content. The working document becomes an index with item IDs pointing to the detail file. During Pass 2-4, load the detail file only for the items you're actively working with.

## Bail-Out Protocol

If total input exceeds ~200k tokens (roughly 15+ substantial reports), distillation quality will suffer even with sequential processing. The working document becomes unwieldy, cross-referencing becomes unreliable, and the LLM's attention is spread too thin.

**Recommendation:** Split into multiple distillation runs by topic. Each run handles 3-5 reports on a coherent sub-topic. Then do a final "meta-distillation" that synthesizes the distillation outputs into a unified document.

Present this recommendation to the user:

```
This input set is very large ([n] reports, ~[tokens]k tokens). Processing it as
a single distillation run would compromise quality — cross-referencing and dedup
become unreliable past ~15 reports.

Recommendation: Split into [n] topic-based batches:
1. [Topic A]: Reports R1, R3, R7 ([tokens]k tokens)
2. [Topic B]: Reports R2, R4, R5 ([tokens]k tokens)
3. [Topic C]: Reports R6, R8, R9 ([tokens]k tokens)

I'll distill each batch separately, then synthesize the results into a unified output.
This produces better results than trying to process everything at once.

Want to proceed with this split, or would you prefer a different grouping?
```

## Recency and Context Decay

Even within token limits, extraction quality degrades as the session grows. Mitigate this:

1. **Process highest-quality reports first.** Best material gets best attention.
2. **Re-read the slop filter between reports.** Refreshes the patterns.
3. **Periodically re-read the working document's Active Items.** Prevents extracting duplicates of items already captured.
4. **After every 3 reports, do a mini-audit:** Are the last 3 reports' extraction quality on par with the first 3? If not, take a more careful pass on the most recent reports.
