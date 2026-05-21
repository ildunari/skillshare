# Sizing Decision Framework

How to decide whether to write 1 comprehensive prompt, 2-4 medium prompts, or 5+ prompts — and how to calibrate word targets for each.

## The core heuristic

**Ask: "Would the same researcher, reading the same sources, naturally cover all of this?"**

- If yes (source pools overlap >60%) → single comprehensive prompt
- If partially (source pools diverge for distinct sub-domains) → 2-4 medium prompts
- If no (genuinely different areas with separate source ecosystems) → 5+ prompts

Source pool overlap is the decision driver, not topic complexity. A complex topic with overlapping sources is better as one deep prompt than four thin ones.

## Decision matrix

### Single prompt (1 comprehensive run)

**Use when:**
- The topic is a coherent domain (one tool, one model, one methodology)
- A researcher would naturally read the same sources for all facets
- The focus areas are different angles on the same thing, not different things
- You want a single reference document, not a scattered collection

**Examples:**
- "Prompt engineering for GPT-5.x" — all focus areas (tool calling, instruction following, templates) share the same source pool (OpenAI docs, Cookbook, community forums)
- "Drug release kinetics from PLGA nanoparticles" — all aspects (synthesis, characterization, modeling) share the same journal/textbook sources
- "React performance optimization" — all techniques share the same documentation and community resources

**Word target:** 8,000-15,000 words
**Focus areas:** 6-10 interrogation-style paragraphs

### Medium prompts (2-4 separate runs)

**Use when:**
- The topic has genuinely distinct sub-domains with different source pools
- A single prompt would force the researcher to context-switch between unrelated source ecosystems
- Each sub-domain has enough depth for 5-8k words on its own
- The sub-domains benefit from separate deep dives that can be combined later

**Examples:**
- "AI image generation" split into: (1) text rendering and prompt engineering (community experiments, Reddit, comparison posts) vs (2) API integration and production pipelines (official docs, GitHub, cost data)
- "Startup fundraising" split into: (1) pitch deck and narrative (practitioner blogs, VC perspectives) vs (2) legal and financial structure (SEC filings, law firm guides, term sheet databases)

**Word target per prompt:** 5,000-10,000 words
**Focus areas per prompt:** 4-8 interrogation-style paragraphs

### Many prompts (5+ separate runs)

**Use when:**
- You're building a knowledge base across genuinely different areas
- Each area has its own documentation ecosystem, community, and terminology
- The areas share <40% of their source material
- You're covering multiple tools, models, or domains that happen to serve one larger goal

**Examples:**
- "Prompt engineering across 5 AI model families" — each model has its own docs, community, behavioral quirks, and source ecosystem
- "Full-stack web development reference" — frontend frameworks, backend architecture, database optimization, DevOps, and security each have distinct source pools

**Word target per prompt:** 5,000-12,000 words (varies by sub-topic depth)
**Focus areas per prompt:** 4-10 interrogation-style paragraphs

## When to merge proposed topics

Merge when:
- Two proposed topics would cite the same top 5 sources
- One topic is a subtopic of another (e.g., "tool calling" is a subtopic of "prompt engineering for GPT-5.x")
- The combined topic still fits within a single coherent research session
- Splitting would produce two thin reports instead of one deep one

## When to split proposed topics

Split when:
- You notice the source suggestions diverging significantly between sections
- One section requires community/practitioner sources while another requires academic/official sources
- The combined prompt would exceed ~15 focus areas (too many for one research run to handle well)
- Two focus areas are so unrelated that depth in one would come at the expense of the other

## The follow-up prompt pattern

When a v1 research output is thin (the research tool produced an overview instead of a deep dive), write a targeted follow-up prompt that:

1. **Explicitly says "this is a follow-up"** — "I already received a shorter overview report on this topic. This research should go significantly deeper."
2. **Names what was already covered** — "The previous report covered [X, Y, Z] at overview level."
3. **Attacks the specific gaps** — "This prompt specifically targets: [gap 1], [gap 2], [gap 3] which were missing or shallow in the previous output."
4. **Escalates the reporting requirements** — Higher word target, more specific minimum deliverables, tighter anti-padding rules.
5. **Keeps the same source pool** — The sources don't change; the depth of extraction does.

This is more effective than re-running the same prompt with minor edits, because it tells the research tool exactly where to invest additional effort.

## Quick reference

| Signal | → Decision |
|---|---|
| All focus areas share the same top sources | Single prompt |
| User wants one reference document | Single prompt |
| Sources diverge into 2-3 distinct pools | 2-4 medium prompts |
| Each sub-domain has 5k+ words of depth available | Medium prompts viable |
| Covering 4+ genuinely different tools/models/domains | 5+ prompts |
| v1 output was thin, need to go deeper | Follow-up prompt (not re-run) |
| User says "just one prompt for this" | Single prompt (respect the request) |
| Proposed breakdown exceeds 15 focus areas total | Split into multiple prompts |
