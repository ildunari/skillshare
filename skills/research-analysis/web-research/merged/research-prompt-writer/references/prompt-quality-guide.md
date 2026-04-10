# Prompt Quality Guide

Detailed examples, anti-patterns, positive patterns, and sizing guidance. Read this before writing any research prompts.

## Open Questions vs Leading Questions

Leading questions get back confirmation of what you already know. Open questions surface what you didn't expect.

**Bad — leading, prescriptive, answers baked in:**
> Research Perlin noise (2D, 3D), simplex noise, Worley noise, curl noise, and domain warping. For Perlin, implement using gradient vectors with a fade curve of 6t⁵-15t⁴+10t³.

**Good — open, exploratory:**
> What noise functions and procedural generation techniques are used in generative art today? What exists beyond the basics? What produces the most visually interesting results? What are the current best implementations?

**Bad — implementation spec disguised as research:**
> Implement A* pathfinding with Manhattan heuristic on a grid with diagonal movement costing 1.414. Also implement Jump Point Search, Dijkstra, flow fields, and NavMesh with funnel algorithm.

**Good — understanding-oriented:**
> What pathfinding approaches do real games use, and what are the tradeoffs at different scales? When does each approach become necessary vs overkill?

**Bad — exhaustive enumeration:**
> Cover these effects: fire, smoke, explosions, rain, snow, lightning, magic, water splash, confetti, fireflies, sparks, dust, trails, embers, blood splatter, shockwaves.

**Good — let researcher curate:**
> What particle effects do polished games commonly need, and what makes them look convincing rather than cheap?

## Prompt Sizing

See `references/sizing-decision-framework.md` for the full decision framework on 1 vs N prompts.

**Too narrow** (not enough to fill a research run):
- "How does screen shake work in browser games?"
- "What's the best A* implementation in JavaScript?"

**Too broad** (produces shallow everything):
- "Research everything about making browser games"
- "Tell me about all web development techniques"

**Right-sized** (coherent area with room to explore):
- "What makes browser games feel polished — the craft of game feel, visual feedback, and player psychology"
- "Real-time physics simulation in the browser — what's achievable at interactive frame rates, from rigid bodies to fluids"
- "Modern approaches to building accessible, performant data dashboards"

A right-sized prompt for a single comprehensive research run targets 8,000-15,000 words of output. For medium prompts in a multi-prompt set, target 5,000-10,000 words each.

## Helpful Context vs Constraining Context

**Include (helps the researcher be useful):**
- Purpose: what the research will be used for
- Constraints: technical limitations that affect relevance
- Quality bar: what "good output" means for this topic
- Sources: which communities and practitioners to trust (tiered — see `references/source-tiering-guide.md`)
- Currency: "past 3 months" or "2024-2025 state of the art" where it matters
- Expertise level: "I'm an experienced [X] — skip beginner content" or "I'm new to [X]"

**Avoid (constrains the researcher's exploration):**
- Specific algorithms or techniques to cover
- Exact code structures or function signatures
- Fixed numbers ("give me exactly 8 items")
- Pre-decided conclusions ("X is better than Y, confirm this")

## Inviting Surprise

Include at least one per prompt, typically as the final paragraph after all focus areas:

- "Surface approaches or techniques I might not know about"
- "Follow interesting threads you discover during research, even if they don't fit neatly into the focus areas above"
- "If the field has evolved past what's described here, prioritize what's current"
- "Decide which sub-topics deserve depth vs a brief mention based on your findings"

This gives the researcher permission to deviate from your assumptions.

## Source Suggestions

Tailor per prompt using the 4-tier model. See `references/source-tiering-guide.md` for the full guide.

**Good — tiered and specific:**
> **Tier 1 — Search first:**
> - **OpenAI Cookbook** (cookbook.openai.com): The GPT-5.2 prompting guide is the single most detailed resource
>
> **Tier 2 — Community intelligence:**
> - **Reddit** (r/OpenAI, r/ChatGPTCoding): Production experience reports, prompt sharing threads

**Bad — generic dump on every prompt:**
> Sources: Google, Stack Overflow, Wikipedia, YouTube, GitHub.

## Techniques That Improve Output Quality

These positive patterns consistently produce deeper, more useful research output. Apply them when writing prompts.

### Set minimum deliverables as countable items

The research tool can verify countable requirements. It can't verify "be thorough."

> Include at minimum: 2-3 complete templates, 5+ concrete examples, 3+ failure case studies

See `references/reporting-requirements.md` for the full guide with templates at three complexity levels.

### Use the before/after framing aggressively

Asking for "before/after comparisons" in both focus areas and reporting requirements forces the research tool to find concrete improvements rather than stating principles abstractly. This is the single highest-impact technique for output quality.

> Show concrete before/after examples of [X] that were rewritten for better performance.

### Include a "do not" anti-padding section

Without explicit exclusions, research tools pad with beginner advice, marketing summaries, and generic content.

> Do not provide advice that applies equally to any [tool/model] without [domain]-specific evidence.

This single line forces domain-specific depth across the entire report.

### Set word targets 2-3x higher than expected

Research tools treat word targets as ceilings. Target 10-15k when you want 6-10k. Target 8k when you want 5k. Never target the minimum acceptable output length.

### Write focus areas as interrogations, not headers

See `references/focus-area-writing-guide.md` for the full guide. Each focus area should be a paragraph with 3-6 aggressive sub-questions, not a single-line topic label.

### Include fallback priority ordering

> If the research tool hits limits, prioritize in this order: (1) [highest value], (2) [next], (3) [next]. These are the highest-impact areas for my use cases.

This ensures the most valuable content gets written even if the tool runs out of budget.

### Add time-sensitivity signals with specific dates

> [Model] launched [specific date]. Prioritize the most current sources. Patterns from [old version] may be counterproductive.

Specific dates are more effective than "prioritize recent content" because they give the tool a concrete freshness threshold.

### Name the gold mine source explicitly

> The OpenAI Cookbook is the gold mine — its prompting guides contain the most detailed, specific advice available.

Don't just list sources. Tell the tool which one deserves 3x the attention.

### Signal "this is a follow-up" when iterating

When a v1 output was thin and you're writing a follow-up prompt:

> I already received a shorter overview report on this topic; this research should go significantly deeper, with more concrete examples, complete templates, and detailed failure case studies.

This prevents the tool from producing another overview.

## Pre-Submission Checklist

Before finalizing:
- [ ] Each prompt asks questions, not specifications
- [ ] No prompt has more than 10 focus areas
- [ ] Each focus area is an interrogation paragraph (3-6 sub-questions), not a single-line header
- [ ] **Reporting requirements section included** with word target and minimum deliverables
- [ ] **Anti-padding "do not" section included** in reporting requirements
- [ ] **Sources are tiered** (Tier 1/2/3/4), not flat-listed
- [ ] **Gold mine source explicitly named** in Tier 1 or usage notes
- [ ] At least one "invite surprise" signal per prompt
- [ ] At least one "before/after" demand across the focus areas
- [ ] At least one "what breaks / failure modes" question across the focus areas
- [ ] Technical context and expertise level stated in each prompt (they're standalone documents)
- [ ] **Fallback priority ordering** in usage notes
- [ ] Topic breakdown was proposed to the user before writing full prompts
- [ ] Usage notes include batch order and dependencies (for multi-prompt sets)
- [ ] No prompt reads like it's writing its own answer
- [ ] Prompts work for any deep research tool, not just one product
- [ ] Word target is 2-3x higher than the minimum acceptable output length
