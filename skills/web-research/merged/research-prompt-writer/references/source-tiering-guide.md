# Source Tiering Guide

How to organize and prioritize source suggestions so the research tool extracts deeply from the best material instead of skimming everything equally.

## Why tiering matters

A flat list of 10 sources gets roughly equal attention. The research tool doesn't know that Source #3 (an official cookbook with 50 pages of detailed examples) is 10x more valuable than Source #8 (a blog post summarizing the same cookbook). Tiering tells the research tool where to start and where to spend most of its time.

## The 4-tier model

### Tier 1 — Gold mine (search first)

1-3 sources that contain the most concentrated, authoritative, detailed information on the topic. These are the sources you'd read cover-to-cover if you were doing the research yourself.

Characteristics:
- Official documentation, cookbooks, or technical guides from the tool/platform creator
- Comprehensive community repos with battle-tested configurations
- Canonical textbooks or review papers in academic domains
- Primary sources (the people who built the thing writing about how to use it)

**Always name the single most valuable source explicitly.** Add a sentence like: "The OpenAI Cookbook is the gold mine — its GPT-5.2 prompting guide is the most detailed single resource available."

### Tier 2 — Community intelligence

5-8 sources where practitioners share real-world experience, gotchas, and patterns not found in official docs.

Characteristics:
- Reddit threads (specific subreddits for the domain)
- Twitter/X from practitioners and tool creators
- GitHub Issues and Discussions (reveal real behavior through bug reports)
- Community forums (OpenAI community, Anthropic Discord, specialized forums)
- Stack Overflow for established technologies

Tier 2 is especially valuable for:
- Fast-moving topics where official docs lag behind reality
- Known issues and workarounds that aren't documented officially
- Comparative assessments ("I tried both X and Y, here's what happened")
- Community-discovered techniques and optimizations

### Tier 3 — Practitioner synthesis

3-5 sources where experienced practitioners synthesize and analyze.

Characteristics:
- Technical blogs (Simon Willison, Zvi Mowshowitz, field-specific bloggers)
- Conference talks and presentations
- In-depth Medium/Dev.to posts from credible practitioners
- YouTube content with substantive technical depth (not hype)
- Agent framework documentation (reveals patterns through their implementations)

### Tier 4 — Comparative context (use sparingly)

1-3 sources from adjacent domains or competing tools, used only for comparison and calibration.

Characteristics:
- Documentation from competing tools (for cross-tool comparison)
- Adjacent field resources (for methodology transfer)
- Historical versions (for migration context)

Mark Tier 4 explicitly as "use sparingly" or "for comparative context only" to prevent the research tool from spending significant time here.

## How to identify gold mine sources by domain

| Domain | Typical gold mine sources |
|---|---|
| AI/ML tools and models | Official cookbooks, SDK repos, platform docs, model cards |
| Scientific research | Specific journals (name them), review papers, PubMed, key research groups |
| Software engineering | Official framework docs, RFC documents, architecture decision records |
| Business/market research | SEC filings, industry analyst reports, company 10-Ks, earnings transcripts |
| Medical/clinical | Clinical practice guidelines, Cochrane reviews, UpToDate, specific trial registries |
| Legal | Case law databases, statute texts, bar association practice guides |
| Open source projects | The repo itself (README, CONTRIBUTING, issues, discussions), maintainer blogs |

## Source freshness guidance

Include a time window when recency matters:

- **Fast-moving topics (AI tools, crypto, policy):** "Prioritize sources from the past 3 months ([Month Year] – [Month Year])"
- **Moderately changing topics (frameworks, best practices):** "Prioritize sources from the past year"
- **Stable topics (algorithms, established science):** "Foundational sources are fine; note any recent developments"
- **Specific version/release:** "Focus on content after [release date] — earlier patterns may be counterproductive"

Be specific about dates. "[Model] launched [date]" tells the research tool exactly how recent it needs to be.

## Template for writing the sources section

```
## Prioritized Sources

Search deeply and exhaustively across these, prioritizing recent content ([time range]):

**Tier 1 — Highest value, search first:**
- **[Source name]** ([URL/location]): [1-sentence description of what's there and why it's valuable]
- **[Source name]** ([URL/location]): [description]
[The [specific source] is the gold mine — [why].]

**Tier 2 — Community intelligence:**
- **[Platform]** ([specific communities]): [what type of content to look for]
- **[Platform]** ([specific accounts/communities]): [description]

**Tier 3 — Practitioner synthesis:**
- **[Blog/author]** ([URL]): [specific relevant content]
- **[Platform]** ([description]): [what to look for]

**Tier 4 — Comparative context (use sparingly):**
- **[Competing tool docs]**: For direct comparison of [specific aspect]
- **[Adjacent domain resources]**: For [specific comparative purpose]
```

## Common mistakes

- **Flat source lists** — "Sources: Google, Stack Overflow, Wikipedia, YouTube, GitHub" gives no priority signal
- **Same sources on every prompt** — different topics need different authorities, even within the same research project
- **Generic source categories** — "Look at blogs and forums" vs "Reddit r/ClaudeAI, r/ChatGPTCoding; Twitter accounts: [specific practitioners]"
- **No gold mine callout** — the research tool doesn't know which source deserves 3x the attention
- **Academic sources for practitioner research** — peer-reviewed papers are Tier 1 for scientific research but Tier 3-4 for "how do people actually use this tool"
- **No freshness guidance** — the tool doesn't know whether 2023 content is relevant or dangerously outdated
- **Too many Tier 1 sources** — if everything is Tier 1, nothing is. Keep Tier 1 to 1-3 sources.
