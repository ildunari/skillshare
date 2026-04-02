---
name: "Freshness Verifier"
description: >
  Verify that APIs, SDKs, libraries, CLI flags, and documentation are current before
  using them in code or plans. Use this skill whenever implementation depends on external
  APIs or SDKs and you need current, source-backed verification before coding.
  Triggers on: checking if an API/SDK is current, verifying that a CLI flag still exists,
  confirming a package version, detecting stale dependencies, checking for breaking changes,
  migrating to a new version, verifying documentation freshness, or any situation where
  you are about to write code calling an external API you haven't verified this session.
  Use proactively — invoke before using any unfamiliar or potentially-changed API/SDK,
  not just when the user explicitly asks.
---

<!-- Merged from docs-freshness-verifier and research-freshness. Both source directories archived. -->

# Freshness Verifier

Prevents stale implementation by forcing current-doc verification and source receipts before coding. Treat this as the "you don't get to guess" workflow.

## When to invoke

Invoke any time you are about to:
- Write code that calls an external API or SDK
- Change build tooling, CLIs, or deployment scripts
- Migrate versions
- Rely on a flag, config key, or command you are not 100% certain is current
- Use an API you haven't verified this session
- Integrate a new library or SDK
- Encounter unexpected API behavior

## Cost-benefit threshold

**Do verify when:**
- Unfamiliar API (haven't used in this session or 3+ months)
- User specifies a version number
- API is known to change frequently
- High-stakes code (production, security-sensitive)

**Skip when:**
- Just verified this session
- Very stable, unchanging API (e.g., basic standard library types)
- User explicitly says "use version X" with confidence
- Simple, well-known patterns

---

## Tool stack (in order)

Use tools in this priority order — escalate only when the previous step is insufficient:

1. **First-party web search** (`search_query` or `mcp__brave-search__brave_web_search`)
   — Use first for "what changed recently" and broad recall.

2. **Context7 / official docs MCP** (e.g., `openai-docs` for OpenAI questions)
   — Use for exact API signatures and versioned docs pages. Prefer official vendor docs and release notes.

3. **Exa** (`mcp__exa__web_search_exa`)
   — Quality override when first-party results are noisy or incomplete. Bias toward official docs, GitHub releases, and primary sources.

4. **Firecrawl** (`mcp__firecrawl__firecrawl_scrape`)
   — Use only when you must extract content from JS-heavy sites, long pages, or paywalls. Extract the smallest relevant section.

## Skill activation order

- Load `openai-docs` for OpenAI API/SDK questions before broad web search.
- Load `mcp-operations` if MCP docs/search tooling is misconfigured or failing.

---

## Anti-hallucination rules

- If you cannot verify a symbol/flag/endpoint from docs or real examples, do not use it.
- Refuse to invent unverified APIs or options.
- Prefer "show me the exact snippet / version line" over paraphrase.
- Confirm versions explicitly (package.json, lockfile, --version output, release note date).
- If evidence is weak, slow down and verify before concluding.

---

## Required research order

1. Native web search (`search_query`) for recency and broad signal.
2. Official docs/tools (Context7, vendor MCP tools).
3. Firecrawl only for extraction-heavy or JS-heavy pages.

---

## Output requirements ("freshness receipts")

At the end of the task report, include a short section (2–3 sources is enough):

```
Freshness receipts:
- Source: <doc URL or release note>  Version/date: <…>  Notes: <1 line>
- Source: <…>
```

Also confirm:
- Exact symbol/flag availability from current docs
- Versions/dates recorded from authoritative sources
- Any conflicts or uncertainty explicitly listed

Keep code comments minimal. Put the receipts in the report unless a call site is genuinely non-obvious.

---

## Sub-agent spawn template (for offloading to a research agent)

When the verification task is substantial enough to warrant offloading (to preserve main context), spawn a research sub-agent using this template:

```
## Task: Research [Library/API Name]

### Deliverables
1. Current stable version number
2. API signatures for: [specific functions/methods needed]
3. Any breaking changes from version [X] to current
4. Migration notes if applicable
5. Official documentation links

### Scope
- Primary source: Official documentation
- Secondary: Release notes, changelogs
- Tertiary: Official GitHub repo issues/discussions
- Out of scope: Blog posts, Stack Overflow, tutorials

### Context
I need to use [specific functionality] in a [project type] project.
Current assumption: [what you think the API looks like]
Need to verify: [specific concerns]

### Report Format
## Research Report: [Library/API]

### Version
Current stable: X.Y.Z
Verified from: [source link]

### API Signatures
[verified signatures for requested functions]

### Breaking Changes
- [List any relevant breaking changes]

### Sources
- [Link 1]: [what was found there]

### Confidence Level
[High/Medium/Low] — [reasoning]
```

Use `subagent_type: "search-specialist"` for web research, or `subagent_type: "Explore"` for codebase exploration.

### Handling research results

**If API is current:** Proceed with implementation. No note needed.

**If API has changed:**
1. Update your approach to use the current API
2. Note explicitly: "Updated to current API. Previous approach used [old method], now using [new method] per [source]."

**If research is inconclusive:**
1. Note the uncertainty
2. Use most recent reliable source
3. Flag in plan: "API info from [date], may need verification"
4. Consider asking user for clarification

---

## Integration with planning

Research should happen during the **planning phase**, before writing the detailed plan:

1. Identify APIs/libraries needed
2. Verify unfamiliar ones (inline or via sub-agent)
3. Incorporate findings into plan
4. Present plan to user
5. Implement with verified information

---

## Test cases

- Verify new SDK method exists before use
- Confirm CLI flag deprecation and replacement
- Confirm exact API signature for an endpoint you haven't used recently
- Verify package version compatibility before starting a migration
