# Note Templates

> YAML frontmatter templates and content structure for each note type. Use these when writing processed vault notes.

## Common Frontmatter Fields

All notes share these fields:

```yaml
---
title: "Clear, descriptive title"
source: "original URL"
created: YYYY-MM-DD
status: processed    # or 'evaluating' for priority items
tags:
  - relevant-tag-1
  - relevant-tag-2
type: tool | article | paper | snippet | reference | project | resource
---
```

## Template 1: Tool Note (for `tech/mac-tools/`, `tech/tools/`, `tech/phone-tools/`)

```markdown
---
title: "Tool Name"
source: "https://example.com/tool"
created: YYYY-MM-DD
status: processed
tags:
  - tool
  - platform-tag (macos, ios, cli, web, etc.)
type: tool
---

# Tool Name

> One-line summary: what it does and why it's useful.

## Overview

2-3 paragraphs describing the tool — what problem it solves, who it's for, how it works at a high level.

## Key Features

- Feature 1
- Feature 2
- Feature 3

## Installation

How to install (brew, npm, download, App Store, etc.)

## Kosta's Notes

(User's personal comments, opinions, or context — if they included any)

## Links

- [Source](url)
- [Documentation](url)
```

## Template 2: AI Tool Note (for `ai-agents/tools/`)

```markdown
---
title: "AI Tool Name"
source: "https://example.com/ai-tool"
created: YYYY-MM-DD
status: evaluating
tags:
  - ai-tool
  - category-tag (llm, image, audio, code, etc.)
type: tool
---

# AI Tool Name

> One-line summary: what AI capability it provides.

## Overview

2-3 paragraphs on the tool's AI capabilities, model/approach, and key differentiators.

## Key Features

- Feature 1
- Feature 2

## Pricing

Free tier / paid plans / open source.

## Technical Details

API availability, model details, integration options, tech stack.

## Kosta's Notes

(User comments if any)

## Links

- [Source](url)
- [Documentation](url)
- [API Reference](url)
```

## Template 3: MCP Server Note (for `ai-agents/agent-tools/mcp-servers/`)

```markdown
---
title: "MCP Server Name"
source: "https://github.com/user/mcp-server"
created: YYYY-MM-DD
status: evaluating
tags:
  - mcp-server
  - integration-type (database, api, filesystem, etc.)
type: tool
github_stars: N
language: TypeScript/Python/etc.
license: MIT/Apache-2.0/etc.
---

# MCP Server Name

> One-line summary: what data/service it connects to.

## Overview

What the MCP server does, what tools it exposes, what integrations it enables.

## Tools Provided

- `tool_name` — description
- `tool_name_2` — description

## Installation

```bash
npx @modelcontextprotocol/install <package>
```

Or manual installation steps.

## Configuration

Config snippet for Claude/Craft Agent integration.

## Kosta's Notes

(User comments if any)

## Links

- [GitHub](url)
- [npm](url)
```

## Template 4: Agent Orchestration Tool (for `ai-agents/agent-tools/orchestration-tools/`)

Same as MCP Server template but with sections for:
- **Architecture** — how agents communicate, what patterns it supports
- **Supported Models** — which LLMs/providers it works with
- **Comparison** — how it differs from similar tools (if user asked)

## Template 5: Knowledge Doc (for `ai-agents/docs/`)

```markdown
---
title: "Document Title"
source: "https://example.com/doc"
created: YYYY-MM-DD
status: processed
tags:
  - docs
  - topic-tag
type: reference
---

# Document Title

> One-line summary of what this document covers.

## Summary

Key takeaways in 3-5 bullet points.

## Details

Main content, organized by topic. Extract the most useful information — don't just copy the entire source.

## Links

- [Source](url)
```

## Template 6: Project Idea (for `coding/ideas/`)

```markdown
---
title: "Project Idea Name"
source: "URL if inspired by something"
created: YYYY-MM-DD
status: backlog
tags:
  - idea
  - tech-stack-tag
type: project
---

# Project Idea Name

> One-line pitch.

## Concept

What the project would do and why it matters.

## Technical Approach

How it could be built — stack, architecture, key challenges.

## Inspiration

What prompted the idea (link, conversation, existing tool).

## Kosta's Notes

(User comments if any)
```

## Template 7: Literature Note (for `brown/literature/`)

```markdown
---
title: "Paper Title"
source: "DOI or URL"
created: YYYY-MM-DD
status: processed
tags:
  - paper
  - field-tag (drug-delivery, computational, etc.)
type: paper
authors: "Author1, Author2, et al."
year: YYYY
journal: "Journal Name"
doi: "10.xxxx/xxxxx"
---

# Paper Title

> One-line summary of the paper's contribution.

## Abstract

Brief abstract or summary of the paper's goals and findings.

## Key Findings

- Finding 1
- Finding 2
- Finding 3

## Methods

Relevant methods used (brief, focus on what's applicable to Kosta's work).

## Relevance to Current Work

How this connects to Kosta's PhD projects (fibrosis delivery, GLP-1 agonists, nanoparticle formulation).

## Links

- [Paper](url)
- [DOI](doi-url)
```

## Template 8: Design Resource (for `tech/ui-design/`)

```markdown
---
title: "Resource Name"
source: "URL"
created: YYYY-MM-DD
status: processed
tags:
  - design
  - resource-type (components, icons, fonts, templates, etc.)
type: resource
---

# Resource Name

> One-line summary of the design resource.

## Overview

What it provides, what design system or framework it's for.

## Highlights

- Notable components or features
- Standout qualities

## Links

- [Source](url)
- [Preview/Demo](url)
```

## Writing Guidelines

1. **Titles should be clear and descriptive** — not just the repo name. "MCP Server for PostgreSQL" is better than "pg-mcp".
2. **One-line summaries should answer "what is this and why should I care?"**
3. **Don't pad notes** — if there's nothing useful for a section, skip it entirely
4. **Kosta's Notes only appears if the user actually wrote a comment** — don't fabricate opinions
5. **Tags should be lowercase, hyphenated** — `mcp-server`, `mac-tool`, `drug-delivery`
6. **Use wikilinks** for connections to existing vault notes: `[[existing-note-title]]`
