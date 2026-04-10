---
name: "Vault Sorter"
description: "Automation skill for processing Kosta's Obsidian Brain vault inbox captures into enriched, properly filed vault notes. Read this skill before every vault processing run. Also use when the user asks to process inbox items, sort captures, enrich notes, triage the vault inbox, or file something into the Brain vault — even if they don't say 'vault sorter' explicitly."
---

# Vault Sorter

> Automation skill for processing Obsidian Brain inbox captures into enriched, properly filed vault notes.

This skill is the source of truth for the Vault Sorter automation. It's read before every scheduled run and can also be invoked manually. The skill is self-improving — the automation updates the editable sections (Preferences, Feedback, Learned Patterns) and reference files after each run.

## Step 0 — Pre-flight Inbox Check

**Before loading any reference files**, do a quick scan to see if there's actually work to do:

1. Glob for `.md` files in: `inbox/quick/`, `inbox/agent/`, `inbox/literature/`, `inbox/` root
2. Check vault root for stray `.md` captures (files not in any subfolder)
3. Exclude: `.gitkeep`, `Stik/settings.json`, `nsfw/` contents, daily notes, templates

**If total items == 0:** Log a single line to `daily/YYYY-MM-DD.md` (append if exists, create if not):
```
## Inbox Processing Report
**Run:** YYYY-MM-DD HH:MM EDT — No items found. Skipped.
```
Then stop. Do not load references, do not spawn sub-agents, do not commit.

**If total items > 0:** Proceed to Step 0.5.

## Step 0.5 — Load Context

Before processing items:

1. Read this entire SKILL.md (you're already reading it)
2. Read every file in `references/` — they contain filing rules, format specs, templates, and learned patterns
3. These files are your operating manual. They override any conflicting instructions elsewhere.

## Environment

- **Vault root:** `/Users/kosta/Library/Mobile Documents/iCloud~md~obsidian/Documents/Brain/`
- **All operations are LOCAL** — read/write files directly, no SSH needed
- **Timezone:** America/New_York
- **Daily notes:** `daily/`

The vault path contains spaces and a tilde character (`iCloud~md~obsidian`). Always quote paths in shell commands. Use absolute paths.

## Step 1 — Scan for Inbox Items

Scan these locations for unprocessed `.md` files:

1. `inbox/quick/` — iPhone/shortcut captures (primary source)
2. `inbox/agent/` — agent-deposited items
3. `inbox/literature/` — papers to process
4. `inbox/` root — stray captures
5. Vault root (`.`) — files that landed outside inbox by mistake

**Skip:** `inbox/Stik/settings.json`, any `.gitkeep` files, any file with `status: processed` in frontmatter, any file that is clearly a daily note or template. **Never touch `inbox/nsfw/`** — a separate automation handles all NSFW content.

**Filename sanitization:** If any filename contains newline characters, special characters (`|`, `·`), or exceeds 100 characters, rename it to kebab-case before processing. Twitter/X captures often have literal newlines in filenames — fix these first.

**Dedup check:** Before processing each item, search the vault for existing notes with the same URL or title. If a match exists, skip the item and log it as a duplicate.

## Step 2 — Classify Each Item

Read the file contents and determine what it is. See `references/capture-formats.md` for detection rules and parsing guidance for each format (bare links, link + comment, raw URL lists, web clips, Twitter shares, multi-link batches).

**User comments are critical.** When text exists below a link, it tells you what Kosta wants done with the capture. See `references/comment-patterns.md` for how to interpret enthusiasm signals, research requests, questions, batch instructions, and more.

## Step 3 — Research & Enrich

For each item, gather information to write a proper vault note. See `references/enrichment-guide.md` for what to extract from each source type and when to use sub-agents vs direct research.

**Simple items** (bare GitHub link, product page): Research the URL yourself. Gather description, key features, install method, stars/popularity, tech stack, URL.

**Complex items** (user says "research more", multi-link captures, comparison requests, academic papers): Spawn a sub-agent using the template below.

### Sub-Agent Prompt Template

When spawning a research sub-agent, use this prompt:

```
Research the following URL(s) and return a SINGLE markdown report. Do not create multiple files.

URL(s): {urls}
User context: {user_comment_if_any}

Research and return:
1. **Title** — clear, descriptive name
2. **One-line summary** — what it is and why it matters
3. **Overview** — 2-3 paragraph description
4. **Key points** — bullet list of important takeaways
5. **Technical details** — tech stack, install method, API, usage (if applicable)
6. **Category recommendation** — where in the vault this should be filed and why
7. **Related vault notes** — any existing notes this connects to (search for related terms)

If the user asked a question, RESEARCH THE ANSWER and include it in the overview.
If the user asked for a comparison, include a comparison section.
If multiple URLs, process each separately but return one consolidated report.

Use WebFetch or browser tools to read the URL content. For GitHub repos, read the README.
```

## Step 4 — Write Notes

Take each item's research and write a clean vault note. See `references/note-templates.md` for frontmatter templates and content structure for each note type.

**Filing:** Use the decision tree in `references/filing-rules.md` to determine the correct destination folder. When in doubt, the filing rules have a fallback for ambiguous items.

**Writing quality matters.** Every note should be something Kosta can scroll through and immediately understand. Don't just move files — produce real, useful notes. If the user had a question, the answer should be woven naturally into the overview.

## Step 5 — File & Link

1. Write the note to its destination using the Write tool with quoted absolute paths
2. Delete or archive the original inbox file — move to `archive/inbox-processed/` to keep a paper trail
3. If the new note belongs in an existing guide page, append a `[[wikilink]]` + description to the relevant guide. See `references/vault-structure.md` for guide page locations.

Don't restructure existing guide pages — just add the new entry in the appropriate section.

## Step 6 — Daily Report

Write a `## Inbox Processing Report` section to `daily/YYYY-MM-DD.md` (create if it doesn't exist). Include:

- Run timestamp
- Total entries found vs processed
- For each processed entry: original filename, destination path, type, brief description
- Any new categories/subcategories created
- Entries skipped (with reason — duplicate, already processed, etc.)
- Questions that were researched and answered

## Step 7 — Git Commit & Push

```bash
cd "/Users/kosta/Library/Mobile Documents/iCloud~md~obsidian/Documents/Brain"
git add -A
# only if there are staged changes:
git commit -m "daily: process inbox (YYYY-MM-DD)"
git push origin main
```

If no changes, skip gracefully.

## Step 8 — Self-Improve

After every run, check if you encountered anything new:
- New capture format? Add it to `references/capture-formats.md`
- New filing pattern? Add it to `references/filing-rules.md`
- New comment interpretation? Add it to `references/comment-patterns.md`
- Something went wrong? Add it to the Feedback section below
- Noticed a recurring pattern? Add it to Learned Patterns below

Timestamp every new entry with `<!-- Added YYYY-MM-DD -->`.

## Preferences

<!-- This section is auto-updated by the automation. Manual edits welcome. -->
<!-- Min entries: 10 | Max entries: 100 -->

- Default note status for new tools: `evaluating` <!-- Added 2026-03-25 -->
- Default note status for AI services: `evaluating` <!-- Added 2026-03-25 -->
- Skip empty NSFW inbox reports (single-line log only) <!-- Added 2026-03-25 -->
- Preserve user comments in a ## Kosta's Notes section <!-- Added 2026-03-25 -->
- GitHub repos: always include stars count, language, license <!-- Added 2026-03-25 -->
- Twitter captures: extract tweet content, don't just link <!-- Added 2026-03-25 -->
- Priority signal words: "important", "def wanna", "super cool", "must have" <!-- Added 2026-03-25 -->
- When user asks a question in comment, research and answer it in the note <!-- Added 2026-03-25 -->
- Prefer spawning sub-agents for URL research (orchestrator focuses on filing decisions) <!-- Added 2026-03-25 -->
- Create new subcategories freely when items don't fit — document in daily report <!-- Added 2026-03-25 -->

## Feedback

<!-- This section is auto-updated after each run. The automation logs what went wrong or what it learned. -->
<!-- Min entries: 10 | Max entries: 100 -->

- Sub-agent parallelization works well — 4 write-batches of 7-9 notes ran concurrently with no conflicts <!-- Added 2026-03-25 -->
- fxtwitter API is effective for extracting tweet content when x.com direct fetch fails <!-- Added 2026-03-25 -->
- Haiku model is sufficient for simple GitHub repo research; Sonnet needed for complex tweet article extraction <!-- Added 2026-03-25 -->
- Small batches (≤4 items) process cleanly in one pass without needing write-batch parallelization <!-- Added 2026-03-27 -->
- Product page research (e.g. Cline docs) works well with Haiku — sub-agents extract pricing, features, and comparisons efficiently <!-- Added 2026-03-27 -->
- Large web clips (>10K) often contain full README content — skip sub-agent research and extract directly from clip body <!-- Added 2026-03-28 -->
- Guide pages use hybrid Dataview + manual "Recent Additions (YYYY-MM-DD)" sections — append wikilinks to Recent Additions, don't modify Dataview blocks <!-- Added 2026-03-28 -->
- Sonnet sub-agent is best for viral tweet research — successfully extracted repo URL, technical details, and API docs from a 13K-like tweet announcement <!-- Added 2026-03-28 -->
- Multiple runs per day: append with "## Inbox Processing Report (Evening)" header and separate "---" divider to distinguish from morning run <!-- Added 2026-03-28 -->

## Learned Patterns

<!-- This section is auto-updated when the automation encounters new patterns. -->
<!-- Min entries: 10 | Max entries: 100 -->

- ~60% of captures are bare GitHub links — optimize for this format <!-- Added 2026-03-25 -->
- ~25% have user comments — always check for text below the link <!-- Added 2026-03-25 -->
- Twitter/X shares have newlines in filenames — sanitize first <!-- Added 2026-03-25 -->
- Stik app creates UUID-named files and settings.json — skip non-md files <!-- Added 2026-03-25 -->
- Web Clipper captures have `description: "web-clip"` frontmatter — strip HTML noise <!-- Added 2026-03-25 -->
- Most captures are AI/agent tools (~70%) — filing defaults to ai-agents/ or tech/ <!-- Added 2026-03-25 -->
- Vault root sometimes has stray captures — always scan root too <!-- Added 2026-03-25 -->
- Twitter/X articles (x.com/i/article/) can contain 30+ links — treat as multi-link batch, use sub-agent with fxtwitter API fallback <!-- Added 2026-03-25 -->
- Design resource listicles produce high note counts — consolidate same-site links (e.g., onepagelove.com main + /portfolio → one note) <!-- Added 2026-03-25 -->
- Vault may have pending uncommitted restructuring — git add -A will capture both new notes and prior moves <!-- Added 2026-03-25 -->
- Some runs find items ONLY in vault root with all inbox/ subdirs empty — root scan is critical, not just a fallback <!-- Added 2026-03-27 -->
- Enthusiasm phrases like "very cool", "very good product" should trigger `status: evaluating` + `priority` tag even without explicit "important" keyword <!-- Added 2026-03-27 -->
- Shortcut captures can re-capture URLs already processed — dedup check against vault AND archive is essential (notebooklm-py re-captured 24 days after initial processing) <!-- Added 2026-03-28 -->
- Multi-link captures without markdown formatting (bullet list with plain URLs) are a distinct format from Format 6 — parse by extracting URLs from plain text lines <!-- Added 2026-03-28 -->
- Twitter research requests ("get the full info and repo") need Sonnet-tier sub-agents — Haiku may miss linked repos or technical details from viral announcements <!-- Added 2026-03-28 -->
- "Agentic IDE" is an emerging category — tools like JetBrains Air file under ai-agents/tools/ (not tech/) since their primary value is agent orchestration <!-- Added 2026-03-28 -->

## Entry Limits

All editable sections (Preferences, Feedback, Learned Patterns) and all reference files follow these rules:
- **Minimum entries:** 10 (never delete below this threshold)
- **Maximum entries:** 100 (consolidate similar entries before adding when approaching limit)
- **Consolidation:** When at 90+ entries, merge related entries into grouped items before adding new ones
- **Timestamps:** Every entry gets `<!-- Added YYYY-MM-DD -->` suffix
- **Dedup:** Before adding, check if an equivalent entry already exists
- **Pruning:** Entries older than 90 days with no reinforcement can be consolidated during cleanup

## Related Skills

The automation may also use these skills for enhanced capabilities:
- `obsidian-markdown` — Obsidian-flavored markdown syntax (if available)
- `obsidian-second-brain` — Vault operations and Obsidian workflow guidance
