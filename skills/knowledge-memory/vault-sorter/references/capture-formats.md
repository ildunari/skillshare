# Capture Formats

> Documents each capture format the automation encounters. Describes how to detect, parse, and extract information from each type.

## Format 1: Bare Markdown Link (~60% of captures)

**Detection:** Single line, starts with `[`, contains `](http`
**Example:**
```markdown
[some-cool-tool](https://github.com/user/some-cool-tool)
```

**Parsing:**
- Extract title from `[Title]`
- Extract URL from `(URL)`
- Title is often the repo/page name, may need enrichment

**What to extract:** URL and title. Research the URL for full details.

## Format 2: Link + User Comment (~25% of captures)

**Detection:** Link on line 1, then blank line or text below
**Example:**
```markdown
[MCP Gateway](https://github.com/user/mcp-gateway)

No idea why this is better than openclaw, research it
```

**Parsing:**
- Line 1: extract link (same as bare link)
- Lines 2+: user comment — this is critical context
- The comment tells you what Kosta wants done with the capture

**What to extract:** URL, title, AND the user comment. See `comment-patterns.md` for how to interpret the comment.

## Format 3: Raw URL List

**Detection:** Multiple lines starting with `http` or `https`
**Example:**
```
https://github.com/user/tool-a
https://github.com/user/tool-b
https://example.com/some-article
```

**Parsing:**
- Each line is a separate URL
- Process each URL as an independent item (separate notes)
- If a user comment appears at the top or bottom, it applies to all URLs

**What to extract:** Each URL individually. Each becomes its own note.

## Format 4: Web Clip

**Detection:** YAML frontmatter with `description: "web-clip"` or extensive HTML-like content
**Example:**
```markdown
---
title: "Some Article Title"
source: "https://example.com/article"
description: "web-clip"
created: 2026-03-20
tags:
  - clippings
---

# Article Title

Full page content with lots of HTML noise, navigation elements, ads, etc.
```

**Parsing:**
- Extract URL from `source` frontmatter field
- Extract title from `title` frontmatter field
- The body contains the full page content — extract key info, discard HTML noise
- Don't re-fetch the URL unless the clip is truncated or unclear

**What to extract:** Title, URL, and the meaningful content from the body. Strip navigation, ads, boilerplate.

## Format 5: Twitter/X Share

**Detection:** URL contains `twitter.com` or `x.com`, filename often contains `@` and engagement stats (`likes`, `replies`, `retweets`)
**Example filename:** `@someuser · 42 likes · 5 replies.md`
**Example content:**
```markdown
[Tweet by @someuser](https://x.com/someuser/status/123456789)

This looks super cool for voice chat
```

**Parsing:**
- URL points to a specific tweet
- Filename may have newlines or special characters — sanitize first
- Extract the tweet author from the URL or filename
- Check for user comment below the link

**What to extract:** Tweet URL, author, tweet content (fetch via WebFetch or browser), and any user comment. Don't just link to the tweet — extract the actual tweet text and any media/links it references.

## Format 6: Multi-Link Batch

**Detection:** Multiple `[Title](URL)` lines in one file
**Example:**
```markdown
[Tool A](https://github.com/user/tool-a)
[Tool B](https://github.com/user/tool-b)
[Tool C](https://example.com/tool-c)

Add individually, each one separately
```

**Parsing:**
- Each `[Title](URL)` line is a separate item
- Process each as its own note (separate files)
- If a user comment says "add individually" or "each one separately", confirm split behavior
- If no split instruction, still default to separate notes per URL

**What to extract:** Each link individually. Each becomes its own note unless context suggests they should be a single grouped note.

## Format 7: Twitter/X Article Link <!-- Added 2026-03-25 -->

**Detection:** URL contains `x.com/i/article/` or tweet links to an X Article; filename often contains author name and engagement stats
**Example content:**
```markdown
[Leon Lin (@LexnLin)
71 likes · 4 replies](https://x.com/lexnlin/status/2036549813337031133)

Make sure to extract each one of the individual links as a an entry.
```

**Parsing:**
- Tweet URL may link to an X Article containing a curated list of 10-30+ URLs
- Fetch tweet content, then follow the article link to extract all embedded URLs
- Use fxtwitter API (`https://api.fxtwitter.com/{user}/status/{id}`) as fallback if x.com direct fetch fails
- Each extracted URL becomes a separate note (same as multi-link batch behavior)

**What to extract:** All URLs from the article, each processed individually. Treat the user comment as applying to all extracted items.

## Edge Cases

- **Empty file** — Skip, log as "empty capture"
- **File with only frontmatter** — Skip if no meaningful content
- **PDF or non-markdown** — Skip for now, log for manual review
- **Duplicate URL in multiple inbox files** — Process the first, skip the rest as duplicates
- **Broken URL** — Still file the note with whatever info is available from title and comments. Note the broken URL in the note.
- **GitHub release page link** — URL contains `/releases/tag/`. Research the repo root for overview AND the release page for changelog. Include a version-specific section in the note. <!-- Added 2026-03-29 -->
