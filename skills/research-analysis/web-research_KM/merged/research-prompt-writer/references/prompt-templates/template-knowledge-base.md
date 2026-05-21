# Example Template: Knowledge Base / Domain Survey Prompt

> Use this template when the research goal is to build a comprehensive reference on a broad domain — not deep expertise in one tool, but a survey of the landscape with enough depth to make informed decisions. Common use cases: entering a new field, building a skill/reference document, competitive analysis, literature review, technology evaluation. This template encourages broader coverage with more focus areas and a more aggressive "invite surprise" posture.

---

# PROMPT: [Domain] — Comprehensive Landscape Survey and Reference Guide

## Context

I'm building a [reference document / knowledge base / decision framework / skill] for [domain/purpose]. This will serve as [how it will be used — e.g., "a reference I consult when making technology choices," "the foundation for an AI agent skill," "a team onboarding document," "a literature review for a grant proposal"].

My current knowledge: [1-3 sentences on what you already know, establishing the floor]. I need this research to go beyond what I could find by reading the obvious top-3 Google results and instead surface the landscape of approaches, the tradeoffs practitioners actually face, and the current state of the art as of [date].

[If for an AI agent/skill: The output will be consumed by an AI agent that needs to understand [domain] well enough to [specific capability]. The research should emphasize actionable patterns and concrete examples over theory.]

## Knowledge Gap

I need a comprehensive understanding of the [domain] landscape, including:
- What approaches/tools/methods exist and how they compare
- Which are currently dominant and why (and which are declining)
- What the key decision points are when choosing between approaches
- What practitioners actually do in production vs what documentation recommends
- What the frontier looks like — emerging techniques, recent breakthroughs, open problems

I don't need exhaustive depth in any single area — I need enough depth across the landscape to make informed decisions and know where to go deeper when I need to.

## Focus Areas

- **[Landscape area 1 — e.g., "Current state of the art"]:** What are the dominant approaches to [domain] as of [date]? How has the landscape changed in the past [1-2 years]? What's gained traction, what's lost relevance, and what's emerging? What would a well-informed practitioner consider the "default" approach today, and what are the leading alternatives?

- **[Landscape area 2 — e.g., "Key decision framework"]:** What are the major decision points a practitioner faces in [domain]? For each decision, what are the options and their tradeoffs? Provide a decision framework or flowchart that maps common scenarios to recommended approaches. What factors should drive each decision?

- **[Landscape area 3 — e.g., "Tools and implementations"]:** What tools, libraries, platforms, or frameworks do practitioners actually use? How do they compare on [relevant dimensions: ease of use, performance, cost, community support, maturity]? Which are production-grade and which are experimental? Provide a comparison table.

- **[Landscape area 4 — e.g., "Common pitfalls and failure modes"]:** What mistakes do newcomers commonly make in [domain]? What are the known failure modes that experienced practitioners watch for? What does "doing it wrong" look like, and what are the consequences?

- **[Landscape area 5 — e.g., "Best practices and patterns"]:** What patterns and practices do experienced practitioners follow? What does a well-executed [domain] workflow look like end-to-end? Provide concrete examples of good practice — not just principles, but what they look like in action.

- **[Landscape areas 6-8 as needed for coverage]:** [Continue with additional areas specific to the domain — e.g., "scaling considerations," "security implications," "regulatory landscape," "community and ecosystem," "emerging trends and open problems"]

Surface approaches, tools, techniques, or community practices I might not be aware of. Follow interesting threads even if they don't fit the focus areas above. This is a landscape survey — unexpected discoveries are especially valuable.

## Reporting Requirements

Target **8,000-15,000 words** organized into clearly delineated sections.

**Structure each major section with:**
- Overview of the area (what exists, what's important)
- Key decisions and their tradeoffs
- Concrete examples or case studies where available
- Recommendations or "default path" guidance for someone entering this area
- Source citations for claims and recommendations

**Include at minimum:**
- A landscape overview map or taxonomy (what categories of approaches exist)
- A comparison table of major [tools/approaches/methods] on key dimensions
- A decision framework or flowchart for the most common decisions
- 3+ concrete examples of [good practice / real implementations / case studies]
- A "getting started" recommendation: "If you're starting from scratch, here's the default path and why"
- A "further reading" section pointing to the best deep-dive resources for each sub-area
- An "emerging/watch" section on what's new and might change the landscape

**Do not:**
- Produce a Wikipedia-style neutral overview with no recommendations
- Pad with historical context beyond what's needed to understand current state
- Cover [out-of-scope adjacent domains]
- List every tool/approach without distinguishing which actually matter

**Balance breadth and depth.** This is a landscape survey, so coverage matters more than in a single-tool deep dive. But each section should still have concrete examples and actionable guidance, not just descriptions.

## Prioritized Sources

**Tier 1 — Landscape overviews and authoritative references:**
- **[Canonical reference/survey]** ([URL]): [Why it's the best starting point for landscape understanding]
- **[Official documentation hub]** ([URL]): [Description]

**Tier 2 — Practitioner experience and comparison:**
- **[Community platforms]** ([specific locations]): [What to look for — comparison threads, "what do you use" surveys, experience reports]
- **[Blogs/newsletters]** ([specific ones]): [Practitioners who cover the full landscape, not just one tool]

**Tier 3 — Deep-dive resources (for "further reading" section):**
- **[Domain-specific resources]**: [The best places to go deeper on specific sub-areas]

---

## Usage Notes

- **Single prompt** — even though the domain is broad, a landscape survey is a single coherent research task.
- **This prompt optimizes for breadth with sufficient depth.** Unlike a single-model prompt (which optimizes for maximum depth), this prompt should cover the full landscape at a level where the reader can make informed decisions and know where to go deeper.
- **If the research tool hits limits:** Prioritize (1) the comparison table and decision framework, (2) the landscape taxonomy, (3) concrete examples, (4) the "getting started" recommendation.
- **The most actionable output is the decision framework.** Everything else supports the reader's ability to make good decisions about which approaches to use when.
