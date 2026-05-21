---
name: research-prompt-writer
description: >
  Write effective deep research prompts that produce comprehensive, source-backed results.
  Use when the user wants to research a topic in depth, build a knowledge base, write
  research prompts, create a reference document, prepare a literature review, do competitive
  analysis, or gather information across a broad domain. Triggers on "research X", "write
  research prompts for", "I need to learn about", "build a knowledge base on", "deep dive
  into", "help me research", "/learn", or any task requiring structured multi-query research.
  Also triggers when preparing prompts for Deep Research tools, AI research agents, or
  multi-step research workflows. Works for any domain — technical, business, scientific,
  creative, or otherwise.
---

# Research Prompt Writer

Write research prompts that produce deep, current, surprising results — for any purpose.

## Core Principle

**Describe the territory, not the map.** Define what you need to UNDERSTAND, not what you already KNOW. Let the researcher decide which specific techniques, details, and paths deserve depth.

## Feedback Loop

This skill improves over time. **MUST read `FEEDBACK.md` before every use** to apply lessons from prior runs.

**Cycle:**
1. **Detect** — After generating research prompts, note anything that felt off: prompts too leading, too broad, too narrow, user pushed back, user had to heavily edit, sources were wrong domain, topic split missed something obvious, output from a research run was thin.
2. **Search** — Check `FEEDBACK.md` for prior entries on the same issue.
3. **Scope** — Decide if this is a new entry or an update to an existing one.
4. **Draft-and-ask** — Draft a short feedback entry and present it to the user: *"I noticed [issue]. Want me to log this for future improvement?"*
5. **Write-on-approval** — If the user approves, append to `FEEDBACK.md` with category tag and date.
6. **Compact-at-75** — When `FEEDBACK.md` reaches 75 entries, consolidate: merge duplicates, promote recurring patterns into `SKILL.md` or reference files as permanent rules, archive resolved items. Reset to ~30 entries.

## Progressive Disclosure: What to Load (and When)

Load only what you need. Use this as a routing map.

| Resource | Load when... |
|---|---|
| `FEEDBACK.md` | **Always** — before every use |
| `references/prompt-quality-guide.md` | **Always** — before writing any prompt |
| `references/sizing-decision-framework.md` | Step 2: deciding prompt count and word targets |
| `references/focus-area-writing-guide.md` | Step 3: writing focus areas |
| `references/reporting-requirements.md` | Step 3: writing reporting requirements section |
| `references/source-tiering-guide.md` | Step 3: writing source sections |
| `references/prompt-templates/` | Calibration: when unsure what "good" looks like |
| `scripts/prompt-validator.py` | Step 4: validating completed prompts before delivery |

## Workflow

### Step 1: Gather Context Through Dialogue

**Use the `ask_user_input` tool** to clarify scope before writing anything. Don't guess — ask.

Gather iteratively. Start with the most important questions, then follow up based on answers. Keep going until you have enough context OR the user says they've given enough.

**First round — establish the basics:**
- What domain/subject to research?
- What's the purpose? (building a skill for an AI agent, writing a reference doc, making a decision, creating a knowledge base, literature review, competitive analysis, etc.)
- Who consumes the output? (AI agent, human expert, beginner, mixed audience)
- What's the current level of knowledge? (starting from zero, or updating existing expertise?)

**Follow-up rounds — based on answers, dig deeper:**
- Are there specific areas of emphasis or known gaps?
- Are there areas to explicitly EXCLUDE or deprioritize?
- What does "good" look like? (working code examples, conceptual understanding, comparison of options, decision framework, complete templates?)
- Any known authoritative sources, communities, or practitioners to prioritize?
- Any time-sensitivity? (need latest state of the art, or is foundational fine?)
- How will the research be run? (Claude Deep Research, ChatGPT Deep Research, Perplexity, AI agent, manual search?)
- Is this a follow-up to a previous research run that was thin? If so, what was missing?

**Stop gathering when:**
- You have enough to identify coherent topic areas
- The user says "that's enough" or "just go with what you have"
- Further questions would be nitpicking rather than shaping the research

Don't over-interrogate. 2-3 rounds of questions is typical. If the user gives a detailed initial description, you may only need 1 clarifying round.

### Step 2: Decide Prompt Count and Propose Topic Breakdown

**Load `references/sizing-decision-framework.md`** before this step.

Before writing full prompts, make two decisions:

**Decision 1: How many prompts?**

Apply the source-pool-overlap heuristic:
- **Single prompt** if source pools overlap >60% (most common for single-tool/model/domain research)
- **2-4 medium prompts** if source pools diverge for distinct sub-domains
- **5+ prompts** if covering genuinely different areas with separate source ecosystems

Present your recommendation with reasoning: *"I recommend a single comprehensive prompt because all the focus areas share the same source pool (official docs, community forums, practitioner blogs). Splitting into multiple prompts would produce overlapping thin reports instead of one deep one."*

**Decision 2: Topic breakdown**

Present the proposed focus areas to the user. For each, give a 1-sentence description of what the prompt would cover.

Let the user:
- Approve the breakdown
- Merge topics they think are too granular
- Split topics they think are too broad
- Add areas you missed
- Reprioritize what matters most
- Override the prompt count recommendation

### Step 3: Write Prompts

**Load these references before writing:**
- `references/focus-area-writing-guide.md` — for interrogation-style focus areas
- `references/reporting-requirements.md` — for the output enforcement section
- `references/source-tiering-guide.md` — for tiered source structure
- `references/prompt-templates/` — for calibration if unsure what "good" looks like

Each prompt follows this structure:

```
# PROMPT [N]: [Descriptive Title — include the domain and scope]

## Context
[Who you are. What you're building. 3-4 use cases in priority order.
Expertise level and cross-domain context. Follow-up signal if applicable.
2-3 paragraphs.]

## Knowledge Gap
[1-2 paragraphs: What you don't know. Why this specific topic requires
different treatment than what you already know. What architecturally or
behaviorally is different. Specific gaps to target.]

## Focus Areas
[6-10 areas for comprehensive prompts, 4-8 for medium prompts.
Each is a bold-labeled paragraph with 3-6 aggressive sub-questions
using the interrogation pattern. Mix the five question types:
beyond basics, show me, what breaks, compare, how should practitioners.

End with surprise invitation paragraph.]

## Reporting Requirements
[Word target (2-3x expected output). "Structure each section with"
framework. Minimum deliverables as countable items. "Do not" anti-padding
rules. "Prioritize depth over breadth" instruction.
Use the appropriate complexity level from reporting-requirements.md.]

## Prioritized Sources
[4 tiers: Gold mine (search first) → Community intelligence →
Practitioner synthesis → Comparative context (use sparingly).
Name the gold mine source explicitly. Include freshness guidance.]

---

## Usage Notes
[Single vs multi-prompt. Time-sensitivity with specific dates.
Fallback priority ordering. Follow-up signal if applicable.
Gold mine source callout.]
```

**Mandatory rules (see quality guide for examples):**
- Focus areas use interrogation style with 3-6 sub-questions each — never single-line headers
- Reporting requirements section included with word target, minimum deliverables, and anti-padding rules
- Sources are tiered (Tier 1/2/3/4), not flat-listed
- At least one "invite surprise" signal per prompt
- At least one "before/after" demand across the focus areas
- At least one "what breaks / failure modes" question across the focus areas
- Technical context, expertise level, and use case priority stated in each prompt (they're standalone documents)
- Fallback priority ordering in usage notes
- No exhaustive checklists or enumerations — describe the space, don't list every item in it
- Don't pre-decide algorithms, techniques, or structures — let the researcher choose what deserves depth

### Step 4: Validate and Deliver

**If tools are available**, run the validator:

```bash
python scripts/prompt-validator.py <output_file.md>
```

Fix any FAIL results. Address WARN results where practical.

**If tools aren't available**, manually check against the pre-submission checklist in `references/prompt-quality-guide.md`.

**Add usage notes** at the bottom of the output file:
- Suggested batch order (which prompts to run first, which can run in parallel)
- Dependencies (does prompt 3 benefit from prompt 1's results being available?)
- Practical notes (estimated research time, how to combine results, any known gaps)
- A reminder that each prompt is self-contained and can run independently

**Output:** Produce one markdown file per prompt (or a single file with clear `# PROMPT N: Title` separators for multi-prompt sets). Save to `/mnt/user-data/outputs/` and present to user.

### Step 5: Handle Thin Output (Follow-Up Prompts)

If the user reports that a research run produced thin output:

1. **Diagnose** — Ask what was missing: depth, examples, templates, failure cases, specific areas?
2. **Apply the follow-up pattern** (see `references/sizing-decision-framework.md`):
   - Explicitly say "this is a follow-up"
   - Name what was already covered
   - Attack the specific gaps
   - Escalate reporting requirements (higher word target, more specific deliverables, tighter anti-padding)
3. **Write the follow-up prompt** using the same structure but with the knowledge gap focused entirely on the gaps
