---
name: "Wiki Weaver"
description: "Automated knowledge graph builder for Kosta's Obsidian Brain vault. Reads existing notes, finds connections, adds wikilinks (inline + Related Notes section), maintains wiki/index.md and wiki/schema.md, and keeps guide pages current. Runs daily after Vault Sorter and weekly for fortification. Read this skill before every wiki weaving run."
targets: [Craft-MyWorkspace]
---

# Wiki Weaver

> Automated knowledge graph builder that stitches vault notes together with wikilinks, indexes, and cross-references.

This skill is the source of truth for the Wiki Weaver automation. It runs in two modes:
- **Daily (21:30)** — targets only that day's Vault Sorter additions
- **Weekly (Sunday 22:00)** — broader fortification pass across the week's additions

The skill is self-improving — the automation updates Feedback and Learned Patterns after each run.

## Environment

- **Vault root:** `/Users/kosta/Library/Mobile Documents/iCloud~md~obsidian/Documents/Brain/`
- **All operations are LOCAL** — read/write files directly, no SSH needed
- **Timezone:** America/New_York
- **Wiki folder:** `wiki/` at vault root
- **NSFW wiki:** `nsfwiki/` at vault root (completely isolated from wiki/)

The vault path contains spaces and a tilde character (`iCloud~md~obsidian`). Always quote paths in shell commands. Use absolute paths.

## Step 0 — Pre-flight Check

1. `git pull origin main` to get Vault Sorter's latest changes
2. Read `wiki/last-sort-manifest.json`
3. **If manifest doesn't exist or is empty:** Check `wiki/log.md` for last weave timestamp. If less than 2 hours ago, log "nothing to weave" to daily note and stop. Otherwise fall through to weekly-style full scan.
4. **If manifest has items:** Proceed to Step 1.

**For weekly runs:** Skip the manifest check entirely — go straight to Step 1 with mode=weekly.

## Step 1 — Load Context

1. Read this entire SKILL.md
2. Read `wiki/index.md` (the vault catalog — this is your search index)
3. Read `wiki/schema.md` (structure reference)
4. Read `wiki/log.md` (last 20 lines — for last run state)
5. Read all files in `references/`

## Step 2 — Identify Targets

### Daily mode
Read `wiki/last-sort-manifest.json`. Your targets are only the notes listed in `notes_created`. This is typically 2-8 notes.

### Weekly mode
Read all files in `wiki/manifests/` from the past 7 days. Collect every note path. Also scan for:
- Notes with fewer than 3 outbound wikilinks (under-linked)
- Notes with 0 inbound links (orphans — search wiki/index.md for notes that nobody links to)
- Guide pages that may be missing recent additions

## Step 3 — Extract Entities

For each target note:
1. Read the full note content
2. Extract key entities:
   - **Tool/product names** mentioned in the text
   - **People/authors** referenced
   - **Technologies/frameworks** (languages, libraries, protocols)
   - **Concepts/techniques** (patterns, methodologies)
   - **Project names** from the vault
3. Record entities as a working list for Step 4

## Step 4 — Find Connections

For each target note's entity list:
1. Search `wiki/index.md` for matching note titles and descriptions
2. For ambiguous matches, read the candidate note to verify relevance
3. Score each potential connection:
   - **Strong (auto-link):** Same entity name, direct tool relationship, explicit mention
   - **Medium (auto-link):** Same category + shared technology, same author
   - **Weak (skip):** Only shares a tag, only in same folder, temporal proximity only

**Read only the notes you need.** Don't scan the whole vault — use the index.

## Step 5 — Weave Links

For each target note, apply two types of linking:

### 5a. Inline wikilinks (aggressive)

Scan the note body for entity names that have their own vault note. Convert first mention to a wikilink:

**Before:**
```
Director uses Claude as its underlying model and competes with Cursor and Windsurf.
```

**After:**
```
Director uses [[ai-agents/models/claude|Claude]] as its underlying model and competes with [[ai-agents/tools/cursor|Cursor]] and [[ai-agents/tools/windsurf|Windsurf]].
```

**Rules:**
- Only link the **first mention** of each entity per note
- Use aliased links `[[path|Display Text]]` to keep text readable
- **Never** link inside: code blocks, frontmatter, URLs, headings, the Related Notes section itself
- **Never** link to self
- **Never** remove or modify existing wikilinks
- Preserve the original text casing in the alias

### 5b. Related Notes section

Append or update a `## Related Notes` section at the very bottom of the note:

```markdown
## Related Notes

- **Similar tools:** [[cursor]], [[windsurf]]
- **Used with:** [[claude-code-mcp]]
- **Part of:** [[coding/projects/openclaw/openclaw]]
- **See also:** [[ai-agents/docs/prompt-engineering]]
```

**Categories to use:** Similar tools, Used with, Part of, See also, By same author, Competes with, Related research, Built on, Mentioned in

If the section already exists, merge new links into existing categories. Never remove existing links.

### 5c. Frontmatter update

Add or update `related_notes` in frontmatter:

```yaml
related_notes:
  - ai-agents/tools/cursor
  - ai-agents/tools/windsurf
  - ai-agents/agent-tools/mcp-servers/claude-code-mcp
```

### 5d. Backlinks (bidirectional)

For every link added A → B, check note B:
- If B doesn't link back to A, add A to B's `## Related Notes` section
- Add A to B's `related_notes` frontmatter
- **Do not** add inline links to B's body (only the target note gets inline treatment)

## Step 6 — Update Index

### Daily mode
Append new entries to `wiki/index.md` under the correct section. Don't rebuild the whole file.

### Weekly mode
Rebuild `wiki/index.md` completely. See `references/index-format.md` for the full format spec.

Also rebuild `nsfwiki/index.md` for NSFW notes (isolated, no cross-references to wiki/).

## Step 7 — Update Guide Pages

Check each guide page (see `references/guide-pages.md`) for notes that match its scope but aren't listed. Append missing entries in the standard format:

```markdown
- [[note-title]] — One-line description
```

Only append — never restructure or remove from guide pages.

## Step 8 — Log & Report

### wiki/log.md
Append a run entry:
```
## YYYY-MM-DD HH:MM EDT — [daily|weekly] weave
- Notes processed: N
- Inline links added: N
- Related Notes links added: N
- Backlinks added: N
- Orphans resolved: N
- Under-linked notes remaining: N
- Guide pages updated: [list]
```

### Daily note
Append to `daily/YYYY-MM-DD.md`:
```
## Wiki Weave Report
**Run:** YYYY-MM-DD HH:MM EDT — [daily|weekly]
- Processed N notes, added N links
- [Brief summary of what was connected]
```

## Step 9 — Git Commit & Push

```bash
cd "/Users/kosta/Library/Mobile Documents/iCloud~md~obsidian/Documents/Brain"
git add -A
git commit -m "wiki: [daily|weekly] weave (YYYY-MM-DD)"
git push origin main
```

## Step 10 — Self-Improve

After every run, check for:
- New entity types worth extracting? Add to Learned Patterns
- Connection patterns that were missed? Add to Feedback
- Linking rules that need refinement? Update references/linking-rules.md

## NSFW Isolation Rules

- `nsfwiki/` has its own `index.md` — built from nsfw/ notes only
- NSFW notes **never** link to non-NSFW notes and vice versa
- The weekly run builds nsfwiki/index.md separately
- NSFW notes can link to other NSFW notes within nsfwiki/

## Minimum Link Threshold

- Every content note should have **at least 3 outbound wikilinks**
- Notes below this threshold are flagged as "under-linked" in wiki/log.md
- The weekly pass targets under-linked notes specifically

## Preferences

<!-- Min entries: 10 | Max entries: 100 -->

- Use aliased wikilinks for readability: `[[path|Display Text]]` <!-- Added 2026-04-06 -->
- Prefer "See also" category when connection type is ambiguous <!-- Added 2026-04-06 -->
- Don't link common words even if a note exists (e.g., don't link "Python" in every note) <!-- Added 2026-04-06 -->
- Link threshold: 3 minimum outbound links per content note <!-- Added 2026-04-06 -->
- Skip linking for: daily notes, templates, archive, claudian workspace <!-- Added 2026-04-06 -->
- Weekly run should log orphan list to wiki/log.md for tracking <!-- Added 2026-04-06 -->
- When adding backlinks, use the "See also" category by default <!-- Added 2026-04-06 -->
- Index entries should include note type and status in parentheses <!-- Added 2026-04-06 -->
- Guide page updates: only append to "Recent Additions" sections, don't touch Dataview blocks <!-- Added 2026-04-06 -->
- Entity matching is case-insensitive but display should preserve original casing <!-- Added 2026-04-06 -->

## Feedback

<!-- Min entries: 10 | Max entries: 100 -->

- Initial setup: skill created 2026-04-06, no runs yet <!-- Added 2026-04-06 -->

## Learned Patterns

<!-- Min entries: 10 | Max entries: 100 -->

- ~70% of vault notes are AI/agent tools — most connections will be within ai-agents/ <!-- Added 2026-04-06 -->
- Vault Sorter already adds initial guide page links — weaver should not duplicate these <!-- Added 2026-04-06 -->
- NSFW section (174 notes) is the second largest — needs its own index pass <!-- Added 2026-04-06 -->

## Entry Limits

All editable sections follow these rules:
- **Minimum entries:** 10 (never delete below this threshold)
- **Maximum entries:** 100 (consolidate similar entries before adding when approaching limit)
- **Timestamps:** Every entry gets `<!-- Added YYYY-MM-DD -->` suffix
- **Dedup:** Before adding, check if an equivalent entry already exists
- **Pruning:** Entries older than 90 days with no reinforcement can be consolidated

## Related Skills

- `vault-sorter` — Runs before Wiki Weaver; outputs the manifest this skill consumes
- `obsidian-markdown` — Obsidian-flavored markdown syntax
- `obsidian-second-brain` — Vault operations and workflow guidance
