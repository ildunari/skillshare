# Enrichment Guide

> How to research and enrich different source types. Covers what to extract, when to use sub-agents vs direct research, and quality standards.

## When to Spawn a Sub-Agent vs Research Directly

### Direct research (orchestrator handles it)
- Bare GitHub link with no user comment — just read the README
- Simple product page — extract features and pricing
- Items where the title + URL give you enough context to classify and file
- Estimated research time: < 2 minutes

### Spawn a sub-agent
- User says "research this", "look into this", "dig deeper"
- Multiple URLs in one capture (sub-agent handles the batch)
- Comparison request ("compare to X", "vs Y")
- Academic paper (need to extract structured data)
- Complex product requiring pricing, alternatives, or technical deep-dive
- Tweet thread that links to multiple resources
- Estimated research time: > 2 minutes

### Parallelization
- Spawn up to 3-4 sub-agents simultaneously for speed
- Each sub-agent should return a SINGLE markdown report (not multiple files)
- The orchestrator (you) makes all filing decisions — sub-agents only research

## Source Type: GitHub Repository

**What to extract:**
- **Name and description** — from the repo page or README header
- **Stars count** — popularity indicator
- **Primary language** — from GitHub's language detection
- **License** — MIT, Apache 2.0, GPL, etc.
- **Last commit date** — is it actively maintained?
- **Key features** — from README, usually in a features section or bullet list
- **Installation** — how to install (npm, pip, brew, cargo, etc.)
- **Tech stack** — what it's built with, what it depends on
- **README quality** — if the README is sparse, note it

**How to fetch:**
```
Use WebFetch on the GitHub URL to get the README content.
For stars/language/license, parse the GitHub page or use the API.
```

**Common patterns:**
- GitHub repos with "mcp" in name → likely an MCP server → `ai-agents/agent-tools/mcp-servers/`
- GitHub repos with "agent" or "llm" in name → likely AI-related → `ai-agents/`
- GitHub repos with "cli" in name → likely a tool → `tech/tools/` or `tech/mac-tools/`

## Source Type: Product Website

**What to extract:**
- **Name and tagline**
- **What it does** — in plain terms
- **Key features** — usually from a features page or homepage
- **Pricing** — free, freemium, paid (note tiers if relevant)
- **Platform** — web, macOS, iOS, Linux, cross-platform
- **Alternatives** — if the user asked or if they're well-known

**How to fetch:**
```
Use WebFetch on the homepage URL. If the page is JS-heavy and WebFetch
returns minimal content, use browser tools to render it.
```

## Source Type: Twitter/X Post

**What to extract:**
- **Tweet author** — username and display name
- **Tweet content** — the actual text of the tweet
- **Embedded links** — any URLs shared in the tweet (these are often the real content)
- **Media** — note if images/video are attached (describe if relevant)
- **Thread** — if it's part of a thread, get the full thread context
- **Engagement** — note if highly viral (useful context but don't over-index)

**How to fetch:**
```
Use WebFetch on the tweet URL. If that fails (common with X),
use the bird CLI: bird tweet get <tweet_id> --json
Extract the tweet text and any embedded URLs, then research those URLs separately.
```

**Important:** Don't just link to the tweet. Extract the content and research any URLs it links to. The value is in what the tweet points to, not the tweet itself.

## Source Type: Academic Paper

**What to extract:**
- **Title** — exact paper title
- **Authors** — first author + "et al." for long author lists
- **Journal/venue** — where it was published
- **Year** — publication year
- **DOI** — for permanent linking
- **Abstract** — the paper's summary
- **Key findings** — 3-5 main results
- **Methods** — brief description of approach
- **Relevance** — how it connects to Kosta's work (fibrosis delivery, GLP-1 agonists, nanoparticle formulation)

**How to fetch:**
```
Use WebFetch on the paper URL (DOI, PubMed, arXiv, etc.)
For paywalled papers, extract what's available from the abstract page.
```

## Source Type: Blog Post / Article

**What to extract:**
- **Title and author**
- **Publication date**
- **Key points** — summarize the article, don't just copy it
- **Code snippets** — if it's a technical tutorial, extract the important code
- **Links** — any tools, repos, or resources mentioned

**How to fetch:**
```
Use WebFetch on the article URL. For Medium articles behind paywalls,
note that it's paywalled and extract what's available.
```

## Source Type: Multi-URL Capture

**What to extract:**
- Process each URL independently
- Return a consolidated report with a section per URL
- Note any relationships between the URLs (same author, competing tools, etc.)

**How to handle:**
```
Spawn a sub-agent with all URLs. The sub-agent researches each one
and returns a single report. The orchestrator then splits the report
into individual notes, one per URL.
```

## Quality Standards

1. **Every note should be self-contained** — someone reading it should understand what it is without clicking the source link
2. **Summaries should be in your own words** — don't copy-paste descriptions verbatim from READMEs
3. **Technical details should be practical** — include install commands, config snippets, API examples where relevant
4. **If a URL is dead**, still file the note with whatever info is available from the filename, title, and user comments. Note that the URL was unreachable.
5. **If research turns up very little**, it's OK to write a shorter note. Don't pad with filler. A 5-line note that accurately describes an obscure tool is better than 20 lines of fluff.
