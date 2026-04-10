# Feedback Log — plugin-maker

Read this file before every use. Entries are ordered newest-first.
Each entry has a date, category tag, and one actionable observation.

**Categories:** `[workflow]` `[schema]` `[packaging]` `[customization]` `[edge-case]`

**Compaction rule:** At 75 entries, merge duplicates, promote recurring patterns
to reference files, archive resolved items. Reset to ~30 entries.

---

`[schema]` 2026-03-29 — plugin.json was documented as "always required" but
official docs confirm it's optional (auto-discovery works). Fixed. Also added
missing component types (LSP servers, output-styles), new hook events (25
total, was 9), new hook types (http, agent), new agent frontmatter fields
(effort, maxTurns, disallowedTools, isolation, etc.), ${CLAUDE_PLUGIN_DATA}
persistent directory, and userConfig support. (plugin-maker, established)

`[workflow]` 2026-03-29 — No marketplace documentation existed at all.
Created `references/marketplace-guide.md` covering marketplace.json schema,
all five source types (relative, github, url, git-subdir, npm), strict mode,
common mistakes (marketplace-as-plugin-source, version caching, relative
paths in URL marketplaces), team distribution via project settings. Added
marketplace routing entry to SKILL.md. (plugin-maker, established)
