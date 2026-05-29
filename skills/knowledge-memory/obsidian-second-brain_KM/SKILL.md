---
name: obsidian-second-brain_KM
description: >-
  Use when the user asks to put something in the second brain, save a note to Obsidian,
  file research, capture a tool or reference, process inbox items, create a daily note,
  add a literature note, log a meeting, or interact with the Brain vault in any way.
  Also use when the user says "second brain", "Brain vault", "add to Obsidian", "save this",
  "file this", "capture this", or any variation of storing, retrieving, or organizing
  knowledge in their Obsidian vault. Also use for Obsidian Flavored Markdown questions:
  wikilinks, embeds, callouts, properties/frontmatter, tags, comments, highlights, math,
  Mermaid diagrams, block IDs, or any Obsidian-specific syntax when creating or editing notes.
  Supersedes obsidian-markdown for active Obsidian note and syntax work.
metadata:
  hermes:
    command_priority: 430
    command_aliases:
      - obsidian
      - second-brain
      - brain
---
<!-- Merged from: obsidian-markdown (2026-03-31). Source directory archived 2026-04-01. -->
<!-- Merged from: obsidian-bases, obsidian-cli (2026-04-05). Legacy material preserved under merged/. -->

# Obsidian Second Brain

Kosta's second brain is an Obsidian vault called **"Brain"** synced via iCloud. It follows a structured knowledge management system organized into three main sections — **Brown** (PhD/academic), **Tech** (tools & reference), and **NSFW** — plus shared infrastructure (inbox, daily notes, templates).

## Ask vs Act

**Act immediately** (no confirmation needed):
- Creating any new note (all sections)
- Appending to guide pages
- Creating/updating daily notes
- Quick-capturing to `inbox/`

**Pause and confirm** before:
- Overwriting an existing note (`--force` or equivalent)
- Deleting or archiving notes
- Moving notes between top-level sections
- Modifying template files under `templates/`

Rule: if the operation is reversible locally and the destination path is deterministic, do it.

## Access Methods

Two ways to interact with the vault:

1. **Obsidian CLI** — `obsidian vault="Brain" <command>` (requires Obsidian running)
2. **MCP proxy** — via ForgeMax `obsidian_brain` server (retrieve_tools, call_tool_read/write)

Prefer the CLI for direct operations. Use `vault="Brain"` on every command. If the CLI returns an error (Obsidian unavailable or not running), fall back to direct filesystem reads/writes against the vault path, note which method succeeded, and verify via `head` or `ls`.

## Vault Structure

Current observed vault root (Mac Studio, 2026-05-18): `Brain/` exists at `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Brain` with ~720 Markdown notes. Besides the historical `brown/`, `tech/`, and `nsfw/` sections, the live vault also has active top-level sections including `ai-agents/`, `apple/`, `coding/`, `claudian/`, `daily/`, `guides/`, `inbox/`, `sidekick/`, `wiki/`, and `templates/`. Prefer the live filesystem over this static tree if they differ.

```
Brain/
├── apple/              # Apple-platform work
│   ├── index.md
│   ├── swift-and-swiftui.md
│   ├── ios-simulator-and-xcode.md
│   ├── app-store-and-testflight.md
│   └── apple-ui-animation-and-motion.md
├── brown/              # PhD & Academic (Brown University)
│   ├── projects/       # PhD research projects
│   │   ├── fibrosis-delivery/
│   │   ├── glp1-agonists/
│   │   └── nanoparticle-formulation/
│   ├── literature/     # Processed literature notes (papers, articles)
│   │   └── clips/      # Web clips and excerpts
│   ├── outputs/        # Academic deliverables
│   │   ├── grants/
│   │   ├── manuscripts/
│   │   └── presentations/
│   ├── meetings/       # Meeting notes (lab, committee, etc.)
│   ├── people/         # Academic contacts (advisors, collaborators)
│   ├── concepts/       # Scientific/technical concepts
│   ├── methods/        # Research methods and techniques
│   ├── areas/          # Academic life areas
│   │   ├── phd/
│   │   └── teaching/
│   └── guides/         # Lab MOC pages
│       ├── computational-methods.md
│       ├── drug-delivery.md
│       └── reading-queue.md
├── tech/               # Technology & Tools
│   ├── projects/       # Software projects
│   │   ├── openclaw/
│   │   ├── paperbanana/
│   │   └── vibenotes/
│   ├── agent-tools/    # MCP servers, skills, agent profiles, hooks, prompts
│   │   ├── mcp-servers/
│   │   ├── agent-profiles/
│   │   ├── skills/
│   │   ├── plugins-hooks/
│   │   └── prompts-templates/
│   ├── ai-tools/       # AI-powered tools and services
│   ├── docs/           # Prompting guides, API docs, config guides
│   ├── mac-tools/      # macOS tools and apps
│   ├── phone-tools/    # iOS/mobile tools
│   ├── tools/          # General-purpose tools
│   ├── extra-tools/    # Misc tools
│   ├── ui-design/      # UI/UX design resources
│   └── guides/         # Tech MOC pages
│       ├── agent-tools.md
│       ├── ai-tools.md
│       ├── design-resources.md
│       ├── mac-tools.md
│       └── phone-tools.md
├── nsfw/               # NSFW content organization
│   ├── websites/       # Sites by category
│   │   ├── tubes/
│   │   ├── niche/
│   │   ├── premium/
│   │   ├── cams/
│   │   ├── aggregators/
│   │   ├── forums/
│   │   └── creator-platforms/
│   ├── twitter/        # Twitter/X accounts
│   │   ├── models/
│   │   ├── studios/
│   │   ├── curators/
│   │   └── fitness/
│   ├── reddit/         # Subreddits and users
│   │   ├── subs-general/
│   │   ├── subs-niche/
│   │   ├── subs-fitness/
│   │   ├── subs-celebrity/
│   │   └── users/
│   ├── instagram/      # Instagram accounts
│   │   ├── models/
│   │   ├── fitness/
│   │   └── photographers/
│   ├── lpsg/           # LPSG threads
│   │   ├── celebrity/
│   │   ├── verified/
│   │   ├── amateur/
│   │   └── discussion/
│   ├── bodybuilders/   # Bodybuilders & fitness
│   │   ├── pro/
│   │   ├── classic/
│   │   ├── physique/
│   │   ├── influencers/
│   │   └── powerlifting/
│   └── onlyfans/       # OnlyFans/Fansly creators
│       ├── of/
│       ├── fansly/
│       └── other/
├── inbox/              # Unsorted captures (shared across all sections)
│   ├── quick/          # Quick captures from Stik, shortcuts, or agent drops
│   ├── agent/          # Agent-deposited items (automated captures)
│   └── literature/     # Papers/articles to be processed into literature notes
├── daily/              # Daily notes (YYYY-MM-DD.md)
├── areas/              # Personal life areas (non-academic)
│   ├── fitness/
│   └── personal/
├── guides/             # Personal MOC pages
│   └── weekly-dashboard.md
├── templates/          # Note templates (used by Templater plugin)
├── assets/             # Binary assets
│   ├── images/
│   └── pdfs/
└── archive/            # Retired/processed items
    └── inbox-processed/
```

## Note Types and Templates

Every note has a `type` property in frontmatter. Use the matching template when creating notes.

| Type | Template | Where it goes | When to use |
|------|----------|---------------|-------------|
| `daily` | Daily note | `daily/` | Daily journal, tasks, captures |
| `tool` | Tool note | `tech/{subcategory}/` | New tool, app, CLI, service |
| `reference` | Reference note | `tech/{subcategory}/` or `brown/concepts/` | Concept, technique, general reference |
| `knowledge` | Knowledge doc | `tech/docs/` | Guides, prompt docs, API references |
| `literature` | Literature note | `brown/literature/` | Academic paper or article |
| `meeting` | Meeting note | `brown/meetings/` | Meeting minutes and action items |
| `project` | Project note | `brown/projects/{name}/` or `tech/projects/{name}/` | New project tracker |
| `person` | Person note | `brown/people/` | Contact, advisor, collaborator |
| `output` | Output note | `brown/outputs/{type}/` | Manuscript, grant, presentation |
| `mcp-server` | MCP server | `tech/agent-tools/mcp-servers/` | MCP server configuration |
| `skill-ref` | Skill reference | `tech/agent-tools/skills/` | Documenting an installed skill |
| `agent-profile` | Agent profile | `tech/agent-tools/agent-profiles/` | Specialized agent documentation |
| `nsfw-website` | NSFW website | `nsfw/websites/{category}/` | NSFW website |
| `nsfw-creator` | NSFW creator | `nsfw/{platform}/{category}/` | NSFW creator/account |
| `nsfw-subreddit` | NSFW subreddit | `nsfw/reddit/{category}/` | NSFW subreddit |
| `nsfw-bodybuilder` | NSFW bodybuilder | `nsfw/bodybuilders/{category}/` | Bodybuilder/fitness model |
| `nsfw-lpsg` | NSFW LPSG thread | `nsfw/lpsg/{category}/` | LPSG forum thread |

## Frontmatter Conventions

All notes use these common properties:

```yaml
type: <note-type>          # Required — determines template and behavior
status: <status>           # Varies by type (see below)
aliases:                   # Optional — alternate names for Obsidian search/link
  - alternate name
  - short acronym
tags:                      # Always include type tag + domain tag
  - type/<type-tag>
  - domain/<domain>
created: YYYY-MM-DD        # Creation date
updated: YYYY-MM-DD        # Last meaningful update
```

**YAML quoting rules**: Always quote `url:`, `install_command:`, and any value containing a colon (e.g., `title: "Fast: A CLI Tool"`). Array fields use the `  - item` list style.

### Status values by type

| Type | Statuses |
|------|----------|
| `tool` | `active`, `inactive`, `evaluating` |
| `reference` | `draft`, `stable`, `outdated` |
| `knowledge` | `current`, `outdated`, `archived` |
| `literature` | `to_read`, `reading`, `done` |
| `meeting` | `raw`, `processed` |
| `project` | `active`, `paused`, `completed`, `archived` |
| `output` | `draft`, `in_review`, `submitted`, `published` |

## Tag Taxonomy

Tags follow a hierarchical namespace pattern:

- **`#type/*`** — Note classification: `type/reference`, `type/catalog`, `type/config`, `type/daily`, `type/skill`, `type/agent-profile`
- **`#domain/*`** — Knowledge domain: `domain/research`, `domain/prompting`, `domain/academia`, `domain/mcp`, `domain/macos`, `domain/design`, `domain/infrastructure`, `domain/drug-delivery`
- **`#topic/*`** — Specific topics: `topic/tools`, `topic/ai-tools`, `topic/claude`, `topic/openai`, `topic/github`
- **`#tier/*`** — Quality/importance tier: `tier/s`, `tier/a`
- **`#project/*`** — Project association: `project/paperbanana`, `project/openclaw`

## Workflow: Adding Something to the Second Brain

**Determine section first:**
- Academic/research/lab-related → **`brown/`**
- Agent tools, MCP servers, skills, agent profiles, automation infra → **`ai-agents/`** (live section; fallback to `tech/agent-tools/` only if the active note is clearly there)
- Software dev notes, coding projects → **`coding/`** or `tech/projects/`
- General tool, app, service, or tech reference → **`tech/`**
- NSFW content → **`nsfw/`**
- Not sure → **`inbox/quick/`** (sort later)

Then create the note and verify. No confirmation needed for new notes.

### Images for curated entries

For curated second-brain entries about tools, references, design resources, projects, or guides, generate a relevant image at the end of the workflow unless Kosta explicitly says not to. Save the image inside the Brain vault, normally under `assets/beautify/<section>/<slug>/hero.png`, and embed it in the note with an Obsidian-relative image link like `![](assets/beautify/<section>/<slug>/hero.png)`. Do not leave the note pointing at a Hermes cache path or external generated-image URL.

### Quick capture (unsorted)
```bash
obsidian vault="Brain" create name="<descriptive-name>" path="inbox/quick/<name>.md" content="<content>" silent
```

**Verify:**
```bash
obsidian vault="Brain" open path="inbox/quick/<name>.md"
```
If the CLI returns a not-found error, retry with MCP proxy: `call_tool_write(obsidian_brain, create, {...})`.

### Example: Adding a new tool
```bash
obsidian vault="Brain" create name="my-tool" path="tech/mac-tools/my-tool.md" content="---
type: tool
status: active
tool_category: cli
install_method: homebrew
install_command: \"brew install my-tool\"
url: \"https://example.com\"
aliases:
  - my tool
  - mytool
tags:
  - type/catalog
  - domain/macos
created: 2026-03-08
updated: 2026-03-08
---

# My Tool

Description of what it does.

## Install

\`\`\`bash
brew install my-tool
\`\`\`

## Usage

## Links
- [GitHub](https://example.com)" silent
```

Then update the relevant guide (append, not overwrite — safe):
```bash
obsidian vault="Brain" append file="mac-tools" content="- [[my-tool]] — Short description"
```

**Verify both steps succeeded:**
```bash
obsidian vault="Brain" read path="tech/mac-tools/my-tool.md" | head -5
obsidian vault="Brain" search query="[[my-tool]]" limit=1
```

If guide append fails (file not found), check the guide path matches `tech/guides/mac-tools.md` and retry with full path.

### Example: Adding a literature note
```bash
obsidian vault="Brain" create name="smith2025-hydrogel" path="brown/literature/smith2025-hydrogel.md" content="---
type: literature
status: to_read
citekey: smith2025-hydrogel
title: 'Hydrogel-Based Drug Delivery Systems'
authors:
  - 'Smith, J.'
year: 2025
venue: 'Nature Materials'
doi: '10.1038/...'
url: ''
projects:
  - fibrosis-delivery
tags:
  - type/reference
  - domain/research
created: 2026-03-08
updated: 2026-03-08
---

# Hydrogel-Based Drug Delivery Systems

## Key findings

## Methods

## Relevance to my work

## Questions / follow-ups

## Raw notes" silent
```

Then append to reading queue:
```bash
obsidian vault="Brain" append file="reading-queue" content="- [[smith2025-hydrogel]] — Hydrogel-Based Drug Delivery Systems (2025)"
```

**Verify:**
```bash
obsidian vault="Brain" read path="brown/literature/smith2025-hydrogel.md" | head -3
```

### Handling conflicts (existing note at target path)

Before overwriting, check:
```bash
obsidian vault="Brain" read path="<target-path>" 2>/dev/null | head -5
```

If the note exists and Kosta didn't explicitly say to overwrite it, stop and report what's there. Do not silently clobber.

## Guide Pages (MOCs)

Guide pages are curated index notes with Dataview queries. When adding a new note that fits a guide's scope, append a link to the guide's "Recent Additions" section. Append is always safe; never rewrite a guide page wholesale without being asked.

### Tech guides (in `tech/guides/`)
- `agent-tools.md` — MCP servers, skills, agent profiles
- `ai-tools.md` — AI-powered tools and services
- `mac-tools.md` — macOS tools and apps
- `phone-tools.md` — iOS/mobile tools
- `design-resources.md` — UI/UX design resources

### Brown guides (in `brown/guides/`)
- `computational-methods.md` — Lab computational methods
- `drug-delivery.md` — Drug delivery research
- `reading-queue.md` — Papers to read

### Personal guides (in `guides/`)
- `weekly-dashboard.md` — Weekly overview

## Enabled Plugins

- **Templater** — Template engine (use `template="Template Name"` when creating notes)
- **Dataview** — Query engine for dynamic lists and tables
- **Tasks** — Task management with due dates and recurrence
- **Omnisearch** — Full-text search
- **QuickAdd** — Quick capture macros
- **Metadata Menu** — Frontmatter management
- **Obsidian Linter** — Auto-formatting
- **BRAT** — Beta plugin manager


## Hard-mode operator workflow

For hard-to-track data, breadcrumb following, high-quality note creation, or skill-evaluation work, use `references/operator-playbook.md` before acting. It covers the search ladder, wiki-walk procedure, storage routing, spec sheets, pretty Obsidian formatting, safe modification, verification gates, edge cases, and benchmark metrics.

Run the deterministic benchmark when changing this skill or when behavior feels stale:

```bash
python ~/.config/skillshare/skills/knowledge-memory/obsidian-second-brain/scripts/bench_obsidian_second_brain.py --json
```

## Reference Files

For detailed information on specific topics, see:
- [vault-templates.md](references/vault-templates.md) — Complete template definitions with all frontmatter fields

**Obsidian Flavored Markdown syntax** (consult when creating or editing notes):
- [obsidian-syntax.md](references/obsidian-syntax.md) — Full OFM syntax: wikilinks, embeds, callouts, properties, tags, comments, math, Mermaid, footnotes
- [CALLOUTS.md](references/CALLOUTS.md) — Full callout type list with aliases, nesting, and custom CSS callouts
- [EMBEDS.md](references/EMBEDS.md) — All embed types: audio, video, search embeds, external images
- [PROPERTIES.md](references/PROPERTIES.md) — All property types, tag syntax rules, and advanced frontmatter usage
