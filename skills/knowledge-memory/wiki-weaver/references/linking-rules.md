# Linking Rules

> When to link, what counts as a connection, and confidence thresholds.

## Entity Types to Extract

| Entity Type | Examples | Where to search |
|-------------|----------|-----------------|
| Tool/product name | Cursor, Claude, Obsidian | Note titles in wiki/index.md |
| Person/author | Karpathy, @steipete | brown/people/, note body mentions |
| Technology/framework | Swift, React, MCP protocol | Note titles, tags |
| Concept/technique | RAG, fine-tuning, nanoparticle formulation | brown/concepts/, ai-agents/research/ |
| Project name | OpenClaw, PaperBanana | coding/projects/ |
| Platform | macOS, iOS, Linux, Web | tech/*-tools/, tags |

## Connection Strength Scoring

### Strong — always link
- Note A mentions entity X by name, and note X exists in vault
- Both notes are about the same specific tool/product
- One note is a sub-component of another (MCP server used by an agent framework)
- Author relationship (tool by same person/org)

### Medium — link if ≥2 signals
- Same tool category + same technology stack
- Same domain tag + overlapping key features
- One references a concept the other explains
- Both mentioned in the same guide page

### Weak — do NOT link
- Only shares a broad tag (#domain/agents is too broad alone)
- Only in the same folder
- Only added on the same day
- Superficial keyword overlap ("AI" appears in both)

## Inline Linking Rules

1. Only link first mention of each entity per note
2. Use aliased links: `[[full/path/to/note|Display Name]]`
3. Never link inside:
   - Code blocks (``` or indented)
   - YAML frontmatter (between ---)
   - URLs or markdown link text
   - The ## Related Notes section (use bare wikilinks there)
4. Never link to self
5. Never remove existing links
6. Case-insensitive matching, preserve original casing in alias
7. Skip common/ambiguous terms even if notes exist: "Python", "API", "tool", "agent" (unless context makes it specific)
8. When multiple notes could match (e.g., "Claude" → claude model note vs claude-code tool note), prefer the more specific match based on context

## Related Notes Categories

Use these categories in the ## Related Notes section:

| Category | When to use |
|----------|-------------|
| Similar tools | Same category, competing products, alternatives |
| Used with | Tools commonly used together, integrations |
| Part of | Sub-component or belongs to a project |
| See also | General topical connection, related concept |
| By same author | Same creator/organization |
| Competes with | Direct competitors |
| Related research | Academic papers on same topic |
| Built on | Underlying technology or dependency |
| Mentioned in | Guide pages or overview notes that reference this |

## Backlink Protocol

When adding A → B link:
1. Open note B
2. Check if B already has ## Related Notes section
3. If yes: add A under "See also" (or more specific category if obvious)
4. If no: create the section with A as first entry
5. Add A's path to B's `related_notes` frontmatter
6. Do NOT add inline wikilinks to B's body text — only the target note gets inline treatment
