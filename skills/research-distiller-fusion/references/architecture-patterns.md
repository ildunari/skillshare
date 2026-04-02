# Architecture Patterns

Structural templates for organizing extracted items into a coherent output. Load this during Pass 3 to choose and apply the right architecture.

## Architecture Selection

Don't guess. Match the architecture to how the content will be consumed.

### Selection Heuristic

| Content profile | Best architecture | Why |
|---|---|---|
| "How do I do X?" content — procedures, workflows, setup guides | **Workflow** | Reader follows steps in order |
| "When should I use X vs Y?" content — tool selection, approach comparison | **Decision-oriented** | Reader needs to make a choice |
| "What are the rules for X?" content — style guides, standards, conventions | **Layered** | Reader needs principles first, then specifics on demand |
| "How do I do different tasks in domain X?" content — comprehensive reference | **Task-organized** | Reader drops in at the task they're doing right now |
| "Everything about domain X" content — knowledge base, complete coverage | **Domain-mapped** | Reader explores by topic area |

If the content spans multiple profiles (common for large distillations), use a **hybrid**: one primary architecture with embedded sections using a secondary pattern. Example: task-organized primary with decision trees embedded at choice points.

## Template 1: Task-Organized

Best for: skill reference files, cookbook-style guides, "how to do X" content.

Organized around what the reader needs to DO, not what the source reports talked about.

```
# [Title]

## How to use this [document/skill]
[1-2 paragraphs: who this is for, how to find things, what's NOT covered]

## Core principles
[5-10 top-level rules that apply across all tasks. Tightly written imperatives.
Each principle should have 1-2 sentences of rationale plus concrete implementation guidance.]

## Task: [First common task]
### Context
[When you'd do this. 2-3 sentences.]
### Rules
[Specific rules for this task — values, conditions, examples]
### Pitfalls
[What goes wrong and how to avoid it]

## Task: [Second common task]
...

## Quick reference tables
[Lookup tables, comparison matrices, format code references]
```

**Classification guidance:** Items become top-level principles if they apply across 3+ tasks. Otherwise they go in the specific task section they apply to. If an item applies to exactly 2 tasks, put it in the first and cross-reference from the second.

**Sizing:** 5-10 principles, 3-8 tasks. If you have >8 tasks, group them into 2-3 task categories. If you have <3 tasks, this architecture may be wrong — consider Layered instead.

## Template 2: Decision-Oriented

Best for: tool comparisons, technology selection guides, "which approach" content.

Organized around decision points the reader faces.

```
# [Title]

## How to use this guide
[The decisions this covers. What's out of scope.]

## Decision: [First choice point]
### Context
[When you face this decision. What matters.]
### Options
#### [Option A]
- **Best for:** [specific scenarios]
- **Tradeoffs:** [what you gain, what you lose]
- **Key specs:** [concrete values — performance, cost, limitations]

#### [Option B]
...

### Decision matrix
| Criteria | Option A | Option B | Option C |
|---|---|---|---|
| [criterion] | [rating + detail] | ... | ... |

### Recommendation
[Default choice for common case. Conditions that change the answer.]

## Decision: [Second choice point]
...

## Interaction effects
[How decisions affect each other. "If you chose X in Decision 1, that constrains Decision 3 to..."]
```

**Classification guidance:** Each comparison item becomes a cell in a decision matrix. Each rule becomes a recommendation or constraint. Each failure-mode becomes a "watch out" note under the relevant option.

**Sizing:** 3-7 decision points. If you have >7, the scope may be too broad — consider splitting into separate distillations.

## Template 3: Layered

Best for: style guides, design systems, standards documents, convention references.

Organized from general principles down to specific specifications.

```
# [Title]

## How to use this document
[Principles for the "why." Specifications for the "what." Examples for the "how."
Reference tables for quick lookup.]

## Principles
[5-10 high-level rules with rationale. Each is 2-4 sentences:
the rule, why it matters, and how it shapes downstream specs.]

## Specifications
### [Domain area 1]
[Concrete values, formats, configurations organized by topic.
Each spec references which principle(s) it implements.]

### [Domain area 2]
...

## Examples
### [Example type 1: before/after]
[Show the principle being violated, then applied correctly.]

### [Example type 2: complete case study]
...

## Reference tables
[Consolidated lookup tables. Color codes, format strings, size scales, etc.]

## Confidence notes
[Items with thin sourcing, unresolved conflicts, areas needing follow-up research.]
```

**Classification guidance:** Principles have no specific values — they're the "why." Specifications have concrete values — they're the "what." Examples show the principles and specs in action. Items that are principles-with-values go in Specifications with a cross-reference to the principle they implement.

## Template 4: Workflow

Best for: process documentation, setup guides, multi-step procedures.

Organized as a sequence with branching.

```
# [Title]

## Overview
[What this workflow produces. Prerequisites. Estimated time/effort.]

## Step 1: [Action verb + object]
### What
[What to do. Concrete instructions.]
### Why
[Why this step matters. What goes wrong if skipped.]
### Decision point (if applicable)
[If the step has a branch: conditions for each path.]
### Verification
[How to confirm this step succeeded before moving on.]

## Step 2: [Action verb + object]
...

## Troubleshooting
### [Common failure 1]
**Symptom:** [what you see]
**Cause:** [what went wrong]
**Fix:** [specific steps]

## Quick checklist
[Compressed version: step names only, for experienced users who've done this before]
```

## Template 5: Domain-Mapped

Best for: comprehensive knowledge bases, field overviews, "everything about X" references.

Organized to mirror the domain's natural structure.

```
# [Title]

## How to use this document
[Map of the domain. Where to start depending on what you need.]

## [Domain area 1]
### Overview
[What this area covers. Key concepts.]
### [Sub-area]
[Detailed content organized by whatever sub-structure is natural]

## [Domain area 2]
...

## Cross-cutting concerns
[Topics that span multiple domain areas — performance, accessibility,
security, testing, etc.]

## Glossary
[Domain-specific terms, if the audience might not know them all]
```

**When to use:** Only when the content genuinely spans a broad domain and the reader may enter from any direction. If there's a natural "first do this, then this" flow, use Workflow instead.

## Building the Skeleton

After choosing the architecture:

1. **Write section headers** with brief descriptions (1-2 sentences) of what goes in each section
2. **Assign items** to sections by scanning their Type and content. Keep a tally.
3. **Check balance:**
   - Any section with <3 items? Consider merging with an adjacent section.
   - Any section with >20 items? Split into sub-sections or move detail to a reference file.
   - Any items that don't fit anywhere? Either the architecture is wrong (adjust it) or the item is less valuable than you thought (consider cutting it).
4. **Present the skeleton to the user** with item counts per section. Get approval before filling in content.

## Hybrid Architectures

Large distillations often need a primary architecture with embedded secondary patterns:

- **Task-organized + Decision trees:** Each task section includes a decision tree for the choices within that task
- **Layered + Workflow:** Principles layer at the top, with a workflow section showing how to apply them in sequence
- **Domain-mapped + Layered:** Each domain area has its own principles → specs → examples progression

The primary architecture defines the top-level sections. The secondary architecture defines the internal structure of sections that need it.
