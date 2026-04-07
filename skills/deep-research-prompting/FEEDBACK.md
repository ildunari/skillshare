# Deep Research Prompting — Skill Feedback Log

> **MUST-READ DIRECTIVE:** Read this file before every use of the skill. Apply all lessons below when generating research prompts. Entries are tagged by category and dated.

<!-- CATEGORIES: prompt-quality, topic-splitting, user-interaction, source-selection, bias-detection, scope-sizing, output-format, workflow -->

<!-- Max 75 entries. When this limit is reached, compact: merge duplicates, promote recurring patterns to SKILL.md or references/prompt-quality-guide.md, archive resolved items. Reset to ~30 entries. -->

---

### 2026-02-13 | scope-sizing | Prompt count decision framework was missing
The skill defaulted to proposing 8 separate prompts for 5 topics (AI model prompt engineering across 5 model families). No guidance existed for when 1 comprehensive prompt outperforms multiple thin ones. Key heuristic: if source pools overlap >60%, use a single prompt. For the 5 model families, each was a genuinely different source ecosystem, so 5 prompts was correct — but 8 was over-split. Addressed by adding `references/sizing-decision-framework.md`.

### 2026-02-13 | output-format | Research output was 4k tokens (thin) because prompt had no output enforcement
v1 prompts produced overview-quality output (~4k tokens, rated 7.5/10) because they lacked: explicit word targets, minimum deliverables, section structure requirements, anti-padding rules. The reporting requirements section is the single highest-leverage addition to any research prompt. Addressed by adding `references/reporting-requirements.md`.

### 2026-02-13 | prompt-quality | Focus areas written as headers produce summaries; interrogations produce depth
"Tool calling reliability" (header) → research tool produces a summary paragraph. "Beyond strict: true, how should descriptions be written for 95%+ accuracy? Show before/after examples" (interrogation) → produces a deep section with real examples. Each focus area should be a paragraph with 3-6 aggressive sub-questions. Addressed by adding `references/focus-area-writing-guide.md`.

### 2026-02-13 | source-selection | Flat source lists produce even coverage; tiered lists produce deep extraction
Listing 10 sources flat gives equal weight to all of them. 4-tier structure (gold mine → community → synthesis → comparative) with explicit "search first" instructions and a named gold mine source focuses research effort on the highest-value material. Addressed by adding `references/source-tiering-guide.md`.

### 2026-02-13 | output-format | Word targets are treated as ceilings, not floors
Setting a 3-6k word target produced 4k output. Setting an 8-15k target produced 6-10k output. Always set the target 2-3x higher than the minimum acceptable output. Documented in `references/reporting-requirements.md`.

### 2026-02-13 | prompt-quality | "Do not" anti-padding rules are essential
Without explicit exclusions, research tools pad with beginner advice, marketing summaries, generic safety content, and advice applicable to any tool/model. The most important single exclusion: "Do not provide advice that applies equally to any [tool/model] without [domain]-specific evidence." This forces domain-specific depth. Documented in `references/reporting-requirements.md`.

### 2026-02-13 | scope-sizing | Scope should match user's actual primary use case
v1 GPT-5.x prompt was too API-centric when the user's primary use case was Codex CLI and coding agents. The context section should list use cases in priority order, and the tool should be told to prioritize accordingly. The most important use case should be listed first and mentioned in the knowledge gap section.

### 2026-02-13 | workflow | Follow-up prompts beat re-runs for thin v1 output
When research output is thin, don't just re-run the same prompt with minor edits. Write a targeted follow-up that explicitly says "this is a follow-up," names what was already covered, and attacks the specific gaps. This is more effective because it tells the research tool exactly where to invest additional effort.
