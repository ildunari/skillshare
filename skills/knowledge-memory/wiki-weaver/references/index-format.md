# Index Format

> How to build and maintain wiki/index.md and nsfwiki/index.md.

## wiki/index.md Structure

```yaml
---
type: wiki-index
auto_generated: true
last_built: 2026-04-06T21:30:00-04:00
note_count: 284
link_count: 1450
orphan_count: 12
---
```

## Sections

Organize by top-level vault folder, then by subfolder. Each entry on one line:

```markdown
# Brain Wiki Index

> Auto-generated catalog. External agents: read this + [[wiki/schema]] to understand the vault.

## ai-agents (134 notes)

### agent-tools/mcp-servers (20)
- [[ai-agents/agent-tools/mcp-servers/note-name]] — One-line description (type, status)

### agent-tools/orchestration-tools (12)
- [[ai-agents/agent-tools/orchestration-tools/note-name]] — Description (type, status)

### tools (38)
- [[ai-agents/tools/note-name]] — Description (type, status)

## brown (10 notes)
...

## coding (5 notes)
...

## tech (66 notes)
...

## Stats
- **Total notes:** N (excludes nsfw, daily, templates, archive, claudian)
- **Linked notes:** N (%)
- **Orphaned notes:** N (0 inbound links)
- **Total wikilinks:** N
- **Last vault sort:** timestamp
- **Last wiki weave:** timestamp
```

## Entry Format

Each entry follows: `- [[full/path/to/note]] — One-line summary (type, status)`

Extract the one-line summary from:
1. The `> One-line summary` blockquote if present
2. The `title` frontmatter field
3. First non-heading, non-frontmatter line of the note

## Daily Append vs Weekly Rebuild

**Daily:** Read current index.md. Find the correct section. Append new entries. Update the Stats section counts.

**Weekly:** Rebuild entirely. Scan all .md files in ai-agents/, brown/, coding/, tech/, areas/, guides/. Skip: daily/, templates/, archive/, claudian/, wiki/, nsfwiki/, .obsidian/, inbox/.

## nsfwiki/index.md

Same format but only includes nsfw/ notes. Completely separate from wiki/index.md. No cross-references.
