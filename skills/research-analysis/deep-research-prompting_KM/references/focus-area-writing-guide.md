# Focus Area Writing Guide

How to write focus areas that produce deep, example-rich sections instead of summary paragraphs.

## The core problem

A focus area written as a header produces a summary:

> - Tool calling reliability and calibration

A focus area written as an interrogation produces depth:

> - **Tool calling reliability and tool description engineering:** Beyond `strict: true` and schema design basics, how should tool descriptions be *written* to maximize correct invocation? What's the difference between a tool description that gets 80% accuracy and one that gets 95%+? Show concrete before/after examples of tool descriptions that were rewritten for better performance. What patterns prevent the "fake tool call" problem (model printing JSON as text instead of emitting function_call)? How should large tool sets (15-30+ tools) be managed — description length, naming conventions, categorization? What are the specific differences in tool calling behavior between [variant A] and [variant B]?

The difference: the interrogation style has 6 sub-questions that each force a different type of depth. The header style lets the research tool decide what "tool calling reliability" means — and it will choose the shallowest interpretation.

## The interrogation pattern

Every focus area should be a paragraph containing 3-6 aggressive sub-questions. Structure:

1. **Bold label + colon** — the topic name, for scanability
2. **"Beyond basics" opener** — start with what you already know to push past surface-level
3. **3-6 sub-questions** — each targeting a different depth angle
4. **At least one "show me" demand** — requesting concrete examples, templates, or before/after comparisons

### The five types of sub-questions

Mix these across your focus areas. Not every focus area needs all five, but each prompt should use all five types across its focus areas.

**1. The "beyond basics" question**
Starts with what you already know, then asks what's past it.

> Beyond basic schema validation, how should [X] be configured for [specific quality goal]?

> Beyond the standard [technique], what approaches do practitioners actually use in production?

This tells the research tool your floor. Without it, it starts from zero.

**2. The "show me concrete examples" demand**
Explicitly asks for real examples, not descriptions of examples.

> Show concrete before/after examples of [X] that were rewritten for better performance.

> Provide at least [N] complete [templates/configurations] for different use cases.

> What does a production-grade [X] actually look like? Show the full thing, not a snippet.

**3. The "what breaks" question**
Asks about failure modes, anti-patterns, and known gotchas.

> What causes [specific failure mode] and how is it prevented?

> What are the known failure modes — [example 1], [example 2]? For each, what's the mitigation?

> What patterns that worked on [old version] are now actively harmful on [new version]?

**4. The "compare" question**
Asks for cross-tool, cross-version, or cross-approach comparison.

> How does [A]'s approach to [X] differ from [B]'s in concrete terms?

> What are the specific differences in [behavior] between [variant 1] and [variant 2]?

> Where does [approach A] win vs [approach B], and what tasks are a toss-up?

**5. The "how should practitioners" question**
Asks for actionable methodology, not theory.

> How should [tool descriptions / configurations / prompts] be structured for [specific goal]?

> What is the concrete methodology for [practice] beyond the buzzword?

> How should practitioners handle the tension between [tradeoff A] and [tradeoff B]?

## Before/after examples

### Example 1: AI model prompting

**Before (header style — produces summary):**
> - Instruction following and constraint enforcement

**After (interrogation style — produces depth):**
> - **Instruction following, constraint enforcement, and failure modes:** How should rules, constraints, and behavioral boundaries be written for [Model]'s literal-interpretation behavior? Provide concrete before/after examples of constraints that failed and how they were rewritten. What causes "hallucinated compliance" (model pretending to follow rules it's violating) and how is it prevented? How do positive framing ("always do X") vs negative framing ("never do Y") vs explained constraints ("never do Y because Z") compare in practice? What's the full picture on instruction drift over long conversations — how fast does it happen, what drifts first, and what are all the mitigation strategies?

### Example 2: Scientific research

**Before (header style):**
> - Drug release kinetics from polymer nanoparticles

**After (interrogation style):**
> - **Drug release kinetics and modeling:** Beyond basic Higuchi and Korsmeyer-Peppas fitting, what release models accurately capture biphasic release from PLGA nanoparticles? How should burst release be modeled separately from sustained release? What are the known failure modes of each model (e.g., Higuchi assumes infinite sink — when does this break)? Show concrete examples of release data that was poorly fit by one model and well fit by another, with the diagnostic criteria used to choose. What computational tools do practitioners actually use for release modeling, and how do they compare?

### Example 3: Software architecture

**Before (header style):**
> - Database optimization strategies

**After (interrogation style):**
> - **Query optimization and indexing strategy:** Beyond basic B-tree indexing and EXPLAIN ANALYZE, what indexing strategies do practitioners use for complex query patterns (partial indexes, expression indexes, covering indexes)? Show concrete before/after examples of queries that went from seconds to milliseconds with specific index changes. How should index maintenance be managed at scale — when does index bloat become a problem, and what are the monitoring/remediation patterns? What are the specific differences between PostgreSQL and MySQL indexing behavior that affect optimization decisions?

## Calibration by prompt size

| Prompt type | Focus areas | Sub-questions per area |
|---|---|---|
| Single focused prompt (8-15k target) | 6-10 | 4-6 each |
| Medium prompt in multi-prompt set (5-10k target) | 4-8 | 3-5 each |
| Narrow supplemental prompt (3-5k target) | 3-5 | 2-4 each |

## The surprise invitation

End the focus areas section (after the last focus area) with a surprise invitation. This gives the research tool permission to deviate from your assumptions and follow interesting threads:

> Surface approaches, patterns, or [domain-specific] behaviors I might not be aware of — especially findings from the past [time period]. Follow interesting threads you discover during research, even if they don't fit neatly into the focus areas above.

This is a single paragraph after all focus areas, not a separate focus area.

## Common mistakes

- **Writing focus areas as single-line headers** — produces summaries, not depth
- **Too many focus areas (>10)** — the research tool can't go deep on all of them; it spreads thin
- **No "beyond basics" opener** — the tool starts from beginner level
- **No "show me" demands** — the tool describes what examples would look like instead of providing them
- **No "what breaks" questions** — the output reads like marketing (all benefits, no failure modes)
- **All sub-questions are the same type** — e.g., all "how should" questions without any "what breaks" or "compare" questions
- **Focus area is actually a specification** — "Cover X, Y, and Z with examples of each" is a spec, not a research question. "What approaches to [domain] do practitioners use, and what are the tradeoffs?" is a research question.
