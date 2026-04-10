---
name: "Firecrawl"
description: >
  Web scraping, site crawling, web search, and AI-powered data extraction via
  the firecrawl CLI. Use this skill whenever the user asks to scrape a URL,
  fetch web page content, search the web, download a website, crawl docs,
  extract structured data from pages, or interact with a live web page. Also
  use when you need web content for research, comparison, or data gathering
  tasks — even if the user doesn't say "scrape" explicitly. Triggers on:
  "scrape this", "get the content from", "what does this page say",
  "download this site", "search the web for", "extract data from",
  "crawl the docs", "fetch this URL". Prefer this over curl/WebFetch when
  you need clean markdown, JavaScript-rendered content, multi-page crawling,
  or structured extraction.
alwaysAllow: ["Bash"]
---

# Firecrawl CLI

Web scraping, crawling, search, and AI extraction. Pre-authenticated via stored API key.

## Command Selection

Pick the right command for the job — this saves credits and tokens.

| Need | Command | Credits | Output |
|---|---|---|---|
| Content from a single URL | `scrape <url>` | 1 | stdout (markdown) |
| Content from 2+ known URLs | `scrape url1 url2 ...` | 1/page | saved to `.firecrawl/` dir |
| Ask a question about a page | `scrape <url> -Q "question"` | 1 | stdout (answer only) |
| Quick summary of a page | `scrape <url> -S` | 1 | stdout (summary) |
| Download entire site to local files | `download <url>` | 1/page | `.firecrawl/<domain>/` |
| Find URLs for a topic | `search "query"` | 1 | stdout (results) |
| Discover all URLs on a site | `map <url>` | 1 | stdout (URL list) |
| Crawl a site following links | `crawl <url>` | 1/page | async job (or `--wait`) |
| Complex multi-page AI extraction | `agent "prompt"` | 5-50+ | async job (or `--wait`) |
| Click/interact with a scraped page | `interact "prompt"` | 2/session | stdout |

**Key behavior:** Single-URL scrape outputs to stdout. Multi-URL scrape saves each page to `.firecrawl/<domain>.md` files and prints a summary. Use single-URL when you need the content inline; multi-URL when gathering a batch.

## Token-Efficient Defaults

Use these patterns by default — they minimize context window usage.

```bash
# Single page, clean content (the go-to command)
rtk firecrawl scrape <url> --only-main-content

# Ask a specific question — returns just the answer, not the full page
rtk firecrawl scrape <url> -Q "What is the pricing for the Pro plan?"

# Quick summary without full content
rtk firecrawl scrape <url> -S

# Web search — compact text output by default
rtk firecrawl search "query" --limit 5
```

Always prefix with `rtk` for output compression. Use `--only-main-content` by default — it strips nav, footer, and ads. Use `-Q` when you only need a specific fact from a page — this returns just the answer instead of dumping the entire page into context.

## Commands

### scrape

```bash
firecrawl scrape <url>                           # Single URL → stdout
firecrawl scrape url1 url2 url3                  # Multiple URLs → .firecrawl/ files
firecrawl <url>                                  # Shorthand for scrape
```

Every scrape prints a `Scrape ID:` line — save this if you plan to use `interact` afterward.

**Most useful flags:**
- `--only-main-content` — strip nav/footer/ads (recommended default)
- `-Q, --query "question"` — ask a question about the page content
- `-S, --summary` — summarize instead of returning full content
- `-f, --format <fmts>` — comma-separated: markdown, html, rawHtml, links, images, summary, json, attributes, branding. Single format = raw content; multiple formats = JSON
- `-H, --html` — shortcut for `--format html`
- `--wait-for <ms>` — wait for JavaScript rendering (use for SPAs, React/Vue/Angular sites)
- `--screenshot` / `--full-page-screenshot` — capture page image
- `--include-tags <tags>` / `--exclude-tags <tags>` — filter HTML elements
- `--country <code>` / `--languages <codes>` — geo-targeted scraping
- `--profile <name>` — persist browser state across scrapes (logged-in sessions)
- `-o <path>` — save to file
- `--json` / `--pretty` — structured JSON output
- `--timing` — show request timing

### search

```bash
firecrawl search "query"                                    # Basic search, 5 results
firecrawl search "query" --limit 10                         # More results (max 100)
firecrawl search "query" --scrape --scrape-formats markdown  # Search + scrape each result
firecrawl search "query" --tbs qdr:d                        # Last day (h/d/w/m/y)
firecrawl search "query" --sources web,news,images
firecrawl search "query" --categories github,research,pdf
firecrawl search "query" --json                             # Structured JSON output
```

Note: search supports `--json` but NOT `--pretty`. For structured output use `--json` only.

Other flags: `--location`, `--country`, `--timeout`, `--ignore-invalid-urls`, `-o <path>`

### download

Maps a site to discover pages, then scrapes them into `.firecrawl/<domain>/` as nested directories.

```bash
firecrawl download <url>                                           # Full site
firecrawl download <url> --limit 50 --only-main-content            # Cap pages
firecrawl download <url> --include-paths /docs,/blog -y            # Filter + skip prompt
firecrawl download <url> --exclude-paths /zh,/ja,/fr --only-main-content -y
```

Flags: `--limit`, `--include-paths`, `--exclude-paths`, `--allow-subdomains`, `--only-main-content`, `--wait-for`, `-f/--format`, `-H/--html`, `-S/--summary`, `--country`, `--languages`, `-y` (skip confirmation)

### map

```bash
firecrawl map <url>                                    # List all discovered URLs
firecrawl map <url> --search "api" --limit 50          # Filter by keyword
firecrawl map <url> --include-subdomains --json --pretty
```

Flags: `--limit`, `--search <query>`, `--include-subdomains`, `--sitemap only|include|skip`, `--ignore-query-parameters`, `--wait`, `--json`, `--pretty`

### crawl

```bash
firecrawl crawl <url> --wait --progress --limit 50     # Wait for completion
firecrawl crawl <url> --limit 100                      # Async — returns job ID
firecrawl crawl <job-id>                               # Check job status/results
```

Without `--wait`, crawl returns a job ID immediately. Check status by passing the job ID back: `firecrawl crawl <job-id>`.

Flags: `--limit`, `--max-depth`, `--include-paths`, `--exclude-paths`, `--allow-subdomains`, `--crawl-entire-domain`, `--delay <ms>`, `--max-concurrency`, `--timeout`, `--wait`, `--progress`, `--poll-interval`, `--pretty`

### agent

AI-powered multi-page extraction. Use sparingly — costs 5-50+ credits per job.

```bash
firecrawl agent "Find top 5 AI startups and their funding" --wait
firecrawl agent "Compare pricing" --urls https://a.com,https://b.com --wait
firecrawl agent "Extract products" --schema '{"name":"string","price":"number"}' --wait --json --pretty
firecrawl agent <job-id>                               # Check job status
```

For simple single-page extraction, prefer `scrape -Q` instead — it's 1 credit vs 5-50+.

Flags: `--urls`, `--model spark-1-mini|spark-1-pro`, `--schema`, `--schema-file`, `--max-credits`, `--wait`, `--json`, `--pretty`

### interact

Live browser interaction with a previously scraped page. Costs 2 credits per session.

```bash
# Step 1: Scrape a page (note the Scrape ID in output)
firecrawl scrape https://example.com

# Step 2: Interact with it (uses last scrape automatically)
firecrawl interact "Click the pricing tab"
firecrawl interact "What is the Pro plan price?"

# Step 3: End session
firecrawl interact stop
```

If the last scrape was multi-URL, pass the scrape ID explicitly:
```bash
firecrawl interact <scrape-id> "Click the signup button"
firecrawl interact -s <scrape-id> "What does this page show?"
```

Code execution in the browser:
```bash
firecrawl interact -c "await page.title()" --node
firecrawl interact -c "print(await page.title())" --python
```

### Utility

```bash
firecrawl --status                    # Auth, credits, version
firecrawl credit-usage --json --pretty
firecrawl view-config
```

## Agentic Workflow Patterns

### Research: find URLs then scrape the best ones
```bash
rtk firecrawl search "topic" --limit 5
# Review results, then scrape the relevant URLs:
rtk firecrawl scrape <url1> --only-main-content -Q "What does this say about X?"
```

### Documentation mirror
```bash
rtk firecrawl download https://docs.example.com --include-paths /api --only-main-content -y
# Results in .firecrawl/docs.example.com/ with nested .md files
```

### Targeted Q&A (cheapest and most token-efficient)
```bash
rtk firecrawl scrape https://example.com/pricing -Q "What are the plan prices and limits?"
```

### Interactive exploration (when you need to click through a site)
```bash
rtk firecrawl scrape https://example.com
rtk firecrawl interact "Navigate to the pricing page"
rtk firecrawl interact "What are the enterprise features?"
rtk firecrawl interact stop
```
