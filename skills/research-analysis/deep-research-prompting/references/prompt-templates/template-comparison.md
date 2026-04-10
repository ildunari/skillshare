# Example Template: Cross-Tool/Cross-Model Comparison Prompt

> Use this template when the research goal is to compare 2-4 tools, models, approaches, or frameworks — producing a decision framework and routing guide rather than deep expertise in one tool. The key structural difference from the single-model template: focus areas emphasize head-to-head comparison, and the required deliverables include comparison tables and routing guides.

---

# PROMPT: [Tool A] vs [Tool B] [vs Tool C] — [Domain] Comparison and Routing Guide for Practitioners

## Context

I'm evaluating [tools/models/approaches] for [specific use case]. I have access to all of them and need a practical routing guide — not marketing comparison, but task-level guidance on which tool to use when based on concrete behavioral differences.

My background: [1-2 sentences establishing expertise level and cross-tool experience]. I already know [what you know about each tool at a high level]. I need the comparison to go beyond "Tool A is better at X" to "here's specifically how Tool A handles X differently from Tool B, with concrete examples showing the difference."

My primary use cases for this comparison:
1. **[Use case 1]** — [description, and why the tool choice matters here]
2. **[Use case 2]** — [description]
3. **[Use case 3]** — [description]

## Knowledge Gap

I need a detailed, task-level comparison of [tools] that goes beyond surface-level feature lists. Specifically, I need to understand: where each tool genuinely excels (not marketing claims, but practitioner experience), where each tool fails or has known limitations, and the "translation layer" — how to adapt a workflow optimized for one tool when switching to another.

The comparison should be grounded in [specific domain/task type], not generic "which is better" assessment. Different tasks route to different tools, and I need the routing rules with evidence.

## Focus Areas

- **[Core capability 1] — head-to-head comparison:** How does [Tool A]'s approach to [capability] differ from [Tool B]'s in concrete terms — not just "better/worse" but specific behavioral differences? Show side-by-side examples of the same task executed on each tool, highlighting where the outputs diverge. What does each tool get right that the other gets wrong? What tasks are genuinely a toss-up?

- **[Core capability 2] — behavioral differences:** Where does [Tool A] produce different results than [Tool B] for the same input? Provide concrete examples showing identical prompts/inputs producing different outputs on each tool. What are the specific failure modes unique to each — problems you'll hit on [Tool A] that don't exist on [Tool B], and vice versa?

- **[Workflow/methodology differences]:** How does the overall workflow differ between [Tool A] and [Tool B]? What's the "translation layer" — when I'm experienced with [Tool A]'s approach, what do I need to change when switching to [Tool B]? What [Tool A] patterns are counterproductive on [Tool B]? Provide a migration/adaptation checklist.

- **[Configuration/setup comparison]:** How do the configuration approaches differ? Show equivalent configurations side-by-side — "here's how you'd achieve [goal] on [Tool A], and here's the equivalent on [Tool B]." Where is one tool's configuration model more expressive or flexible than the other's?

- **[Performance, cost, or practical constraints]:** What are the concrete differences in [speed/cost/context limits/rate limits/availability]? How do these practical constraints affect tool routing decisions? What are the hidden costs or constraints that aren't obvious from documentation?

- **[Community and ecosystem]:** What's the state of each tool's community, plugin/extension ecosystem, and documentation quality? Where can you find help when things break? How responsive are the respective teams to bug reports and feature requests?

Surface differences or routing rules I might not be aware of, especially from practitioners who actively use both tools.

## Reporting Requirements

Target **8,000-12,000 words** organized into clearly delineated sections.

**Structure each major section with:**
- The specific behavioral difference being described
- Concrete side-by-side examples (same task, different tools)
- Which tool wins for which sub-tasks within this area
- Source citation for non-obvious claims

**Include at minimum:**
- A detailed task-routing comparison table: [Tool A] vs [Tool B] [vs Tool C] broken down by specific task type (not generic categories — specific tasks like "text rendering," "multi-turn editing," "structured output generation")
- 5+ side-by-side examples showing the same input on different tools
- 3+ "translation layer" patterns (how to adapt [Tool A] approach for [Tool B])
- A migration/adaptation checklist for practitioners switching between tools
- A decision tree or routing flowchart: "If your task is [X], use [Tool]. If [Y], use [Tool]."
- 2+ failure case studies unique to each tool (problems you'd hit on one but not the other)

**Do not:**
- Produce a generic "pros and cons" list without task-level specificity
- Rely on benchmark scores without practical context
- Pad with marketing claims from either tool's creator
- Cover features or capabilities irrelevant to [the domain/use cases listed above]
- Present one tool as universally better — the value is in the routing nuance

## Prioritized Sources

**Tier 1 — Head-to-head comparisons:**
- **Community comparison posts** ([specific subreddits, forums, or blogs where practitioners compare these tools]): Real-world head-to-head testing with concrete examples
- **Official documentation for both tools**: For verifying claimed capabilities and understanding intended usage patterns

**Tier 2 — Tool-specific practitioner experience:**
- **[Tool A community]** ([specific locations]): Power user reports, known issues, advanced patterns
- **[Tool B community]** ([specific locations]): Same as above

**Tier 3 — Analysis and synthesis:**
- **[Practitioner blogs/YouTube]** that cover both tools: Comparative analysis from people who use both

---

## Usage Notes

- **Single prompt** — the comparison is a single coherent research task despite covering multiple tools.
- **The most valuable output is the task-routing table and decision tree.** These are what I'll reference daily. Everything else supports these deliverables.
- **If the research tool hits limits:** Prioritize (1) task-routing comparison table, (2) side-by-side examples, (3) translation layer patterns.
