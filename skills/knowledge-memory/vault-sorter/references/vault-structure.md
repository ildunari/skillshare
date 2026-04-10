# Vault Structure

> Current folder map for the Obsidian Brain vault. Updated by the automation when new folders are created.

**Vault root:** `/Users/kosta/Library/Mobile Documents/iCloud~md~obsidian/Documents/Brain/`

## Top-Level Folders

| Folder | Purpose |
|--------|---------|
| `ai-agents/` | AI agents, agent tools, models, research, docs |
| `brown/` | PhD & academic (Brown University) |
| `coding/` | Programming projects, languages, frameworks, snippets |
| `tech/` | Technology tools, macOS/iOS apps, UI design |
| `nsfw/` | NSFW content (**never touch — separate automation**) |
| `inbox/` | Capture system (what we process) |
| `daily/` | Daily notes |
| `areas/` | Personal areas (fitness, personal) |
| `guides/` | Personal guides (weekly-dashboard) |
| `templates/` | Note templates |
| `assets/` | Images and PDFs |
| `archive/` | Retired items, processed inbox |
| `sidekick/` | Sidekick-related content |

## AI Agents Section (`ai-agents/`)

```
ai-agents/
├── agent-tools/          # Tools for AI agents
│   ├── agent-profiles/   # Agent configuration profiles
│   ├── infrastructure/   # Agent infrastructure tools
│   ├── mcp-servers/      # MCP server integrations
│   ├── monitoring-tools/ # Agent monitoring & observability
│   ├── orchestration-tools/ # Multi-agent orchestration
│   ├── plugins-hooks/    # Agent plugins and hooks
│   ├── prompts-templates/ # Prompt libraries and templates
│   ├── session-managers/ # Session management tools
│   └── skills/           # Agent skill definitions
├── docs/                 # AI/agent documentation and guides
├── guides/               # MOC pages (see Guide Pages below)
├── models/               # AI model notes and comparisons
├── research/             # AI research papers and analysis
└── tools/                # Standalone AI tools and services
```

## Brown Section (`brown/`)

```
brown/
├── areas/
│   ├── phd/              # PhD program notes
│   └── teaching/         # Teaching-related
├── concepts/             # Scientific/technical concepts
├── guides/               # MOC pages (see Guide Pages below)
├── literature/           # Processed literature notes
│   └── clips/            # Web clips of academic content
├── meetings/             # Meeting notes
├── methods/              # Research methods and techniques
├── outputs/
│   ├── grants/           # Grant proposals
│   ├── manuscripts/      # Paper drafts
│   └── presentations/    # Slide decks
├── people/               # Academic contacts
└── projects/
    ├── fibrosis-delivery/  # PhD project
    ├── glp1-agonists/      # PhD project
    └── nanoparticle-formulation/ # PhD project
```

## Coding Section (`coding/`)

```
coding/
├── frameworks/           # Framework notes and comparisons
├── guides/               # Coding MOC pages
├── ideas/                # Project ideas and concepts
├── lab/                  # Experimental code and prototypes
├── languages/            # Language-specific notes
├── projects/
│   ├── openclaw/         # OpenClaw project
│   ├── paperbanana/      # PaperBanana project
│   └── vibenotes/        # VibeNotes project
└── snippets/             # Code snippets and recipes
```

## Tech Section (`tech/`)

```
tech/
├── extra-tools/          # Miscellaneous tools
├── guides/               # MOC pages (see Guide Pages below)
├── mac-tools/            # macOS apps and CLI tools
├── phone-tools/          # iOS/mobile tools
├── tools/                # General-purpose tools
└── ui-design/            # UI/UX design resources
```

## Inbox Structure (what we scan)

```
inbox/
├── quick/                # iPhone/shortcut captures (primary)
├── agent/                # Agent-deposited items
├── literature/           # Papers to process
├── nsfw/                 # NSFW captures (SKIP — separate automation)
└── Stik/                 # Stik app data (skip settings.json)
```

## Guide Pages (MOC / Index Pages)

Guide pages are index notes that collect related content with wikilinks.

### AI Agents Guides (`ai-agents/guides/`)
- `agent-tools.md` — AI agent configuration, skills, MCP servers, plugins
- `ai-tools.md` — AI platforms, libraries, APIs, frameworks
- `agentic-tools-visual-landscape.md` — Visual landscape of agentic tools
- `agentic-workspace-tools-comparison.md` — Workspace tool comparisons

### Tech Guides (`tech/guides/`)
- `design-resources.md` — Component libraries, design tools, icons, UI references
- `mac-tools.md` — CLI tools, GUI apps, system extensions for macOS
- `phone-tools.md` — iOS apps, Shortcuts, widgets, automations
- `obsidian-visual-polish-guide.md` — Obsidian styling and visual polish

### Brown Guides (`brown/guides/`)
- `computational-methods.md` — Computational chemistry, molecular docking, ADMET
- `drug-delivery.md` — Fibrosis-targeted delivery, nanoparticles, hydrogels
- `reading-queue.md` — Academic reading pipeline tracker

### Personal Guides (`guides/`)
- `weekly-dashboard.md` — Weekly snapshot of active work and deadlines

### Guide Update Format

When adding a new note to a guide page, append to the appropriate section:
```markdown
- [[note-title]] — Brief one-line description of what it is
```
