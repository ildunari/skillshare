# Obsidian Second Brain Operator Playbook

This reference is the hard-mode operating procedure for finding, storing, modifying, and benchmarking work in Kosta's Brain vault. Use it when the task is more complex than a simple note create/read.

## Search ladder for hard-to-track data
Use a layered search ladder, stopping as soon as the evidence is strong enough:

1. **Path/name pass**: search filenames and folders first (`fd`, `find`, or `obsidian search`) because Kosta's vault has strong path semantics.
2. **Property pass**: inspect frontmatter keys (`type`, `status`, `project`, `tags`, `aliases`, `citekey`, `url`, `source_url`) before full-text guessing.
3. **Full-text pass**: use `rg -i` across Markdown, then narrow by section and modified time.
4. **Link graph pass**: inspect `[[wikilinks]]`, backlinks, embeds, guide pages, and Dataview queries around the hit.
5. **Alias/synonym pass**: try project aliases, old folder names, acronyms, paper citekeys, handles, product names, and spelling variants.
6. **Recent-capture pass**: check `inbox/`, `daily/`, and recent modified files when the thing may have been captured but not filed.

Prefer returning exact paths plus the breadcrumb trail that led there, not just a single matching line.

## Breadcrumb and wiki-walk procedure
For wiki-like navigation, walk from broad MOCs to specific notes and back:

- Start with top-level guides such as `ai-agents/guides/agent-tools.md`, `tech/guides/*.md`, `brown/guides/*.md`, or `guides/weekly-dashboard.md`.
- Follow explicit `[[wikilinks]]`, embedded notes, and Dataview/list sections.
- Inspect backlinks to understand why a note matters and where it belongs.
- Preserve breadcrumbs in the answer or note body: `[[agent-tools]] → [[skills-sh]] → [[serve-sim]]`.
- If a guide is stale, append a short `## Recent Additions` entry rather than rewriting the whole page.

When adding a new note, include a `## Related` section with 2-6 high-value internal links and update at least one relevant guide when the destination is clear.

## Storage and routing decision tree
Route new knowledge by primary use, not by source format:

- Brown/research/lab/papers/methods/people/outputs → `brown/`.
- Agent tools, MCPs, prompts, models, automation infrastructure → prefer live `ai-agents/` unless an existing `tech/agent-tools/` page is clearly the active home.
- Software project docs → `coding/projects/<project>/` or `tech/projects/<project>/` depending on existing neighborhood.
- General Mac/iOS/tools/design resources → `tech/` subfolders.
- Unsorted clips → `inbox/quick/` or `inbox/literature/`.
- Existing topic with nearby notes → stay in that neighborhood and link outward instead of inventing a new top-level folder.

Before creating, check for an existing note by slug, title, URL, aliases, and likely guide backlinks. New notes are safe; overwrites/moves/deletes require confirmation.

## Spec sheets and frontmatter discipline
Use the matching spec sheet in `references/vault-templates.md` before writing. Required baseline:

```yaml
---
type: <note-type>
status: <valid-status-if-the-type-uses-status>
tags:
  - type/<type-or-catalog-tag>
  - domain/<domain>
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Do not invent status values if the template defines valid ones. Preserve existing frontmatter key style in nearby notes. Use quoted strings for URLs, titles with colons, commands, and values that YAML may misread.

## Pretty Obsidian formatting patterns
Make notes readable in Obsidian, not just valid Markdown:

- Use a concise H1 matching the note title.
- Add a `> [!summary]` or `> [!abstract]` callout for the top-level takeaway when the note is more than a quick capture.
- Use `## Breadcrumbs`, `## Why it matters`, `## Usage`, `## Related`, and `## Sources` where relevant.
- Use internal `[[wikilinks]]` for vault notes and Markdown links only for external URLs.
- Use callouts sparingly: `tip` for workflow hints, `warning` for pitfalls, `example` for concrete commands, `todo` for follow-ups.
- Prefer compact tables only inside Obsidian notes when they improve scanning; otherwise use bullets and sections.

## Safe modification and idempotent updates
For existing notes and guides:

- Read the target before editing.
- Append under `## Recent Additions`, `## Log`, or a clearly matching section when possible.
- Make guide updates idempotent: search for the exact `[[Note]]` link first and do not duplicate it.
- Preserve hand-written Dataview blocks, embeds, comments, and custom CSS classes.
- Never rewrite a guide or template wholesale unless explicitly asked.
- If the edit touches many notes, stage it in a temporary plan first and report the intended paths.

## Verification gates
Verify after every operation:

- File exists at the intended path.
- Frontmatter starts and ends with `---`, parses as YAML, and includes required keys for the note type.
- Internal notes are linked with `[[wikilinks]]`; external URLs use Markdown links.
- The new note has at least one inbound or outbound navigation path unless it is an inbox capture.
- Guide append is present exactly once.
- If Obsidian is running, use `obsidian vault="Brain" open/read/search`; if not, verify by filesystem and note that CLI attach was unavailable.

## Benchmark metrics to track
For skill-evolution runs and hard vault tasks, track:

- wall-clock duration per search/write/verify step
- number of files scanned and files opened
- number of candidate hits and final evidence paths
- estimated context characters/tokens loaded from vault notes
- tool/API calls used
- success/failure per benchmark case
- formatting validity: YAML/frontmatter, wikilink use, duplicate guide entries, orphan risk
- created/modified paths and whether the operation touched live vault vs sandbox
- plateau signal: score improvement over the last four loops

Use `scripts/bench_obsidian_second_brain.py --json` for the baseline deterministic suite.

## Edge cases and fallbacks
Common edge cases:

- Obsidian CLI installed but Obsidian app not running: use filesystem reads/writes or MCP fallback, then verify paths directly.
- iCloud duplicate or stale paths: prefer the live `Brain` vault under `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Brain`; report suspicious duplicate vaults.
- Existing note conflict: read and summarize the existing note, then ask before overwrite.
- Ambiguous destination: create in `inbox/quick/` with good frontmatter and breadcrumbs for later filing.
- Broken links after renames: avoid manual moves without confirmation; Obsidian tracks renames better than raw filesystem moves.
- Sensitive/NSFW notes: preserve privacy, avoid unnecessary excerpts, and use paths/metadata when enough.

## Complex eval prompts
Use these eval prompts when checking future improvements:

1. Find a concept from a vague query, show the breadcrumb trail through guides/backlinks, and identify the most authoritative note.
2. File a new MCP server from a URL into the correct neighborhood, create a pretty note with frontmatter/callouts/sources, and update the relevant guide idempotently.
3. Convert a rough paper citation into a literature note with citekey, Brown project links, questions, and reading-queue entry.
4. Update an existing tool note without clobbering custom sections or duplicating guide links.
5. Handle Obsidian CLI unavailable by falling back to filesystem verification while still producing a valid note.
6. Search for hard-to-track data that may live under `ai-agents/`, `tech/`, `coding/`, `daily/`, or `inbox/` using path, property, full-text, and graph passes.
