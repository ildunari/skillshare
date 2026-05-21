# Filing Rules

> Decision tree for where to file each note type. The automation uses this to determine the destination folder for each processed inbox item.

## Quick Decision Flow

```
Is it NSFW? → SKIP (separate automation)
Is it academic/research/lab? → brown/
Is it an AI agent, MCP, or agent tool? → ai-agents/
Is it a coding project, language, or framework? → coding/
Is it a tool, app, or tech resource? → tech/
Doesn't fit? → See Ambiguous Items below
```

## Section 1: AI Agents Filing (`ai-agents/`)

| Pattern | Destination |
|---------|-------------|
| MCP server (name contains "mcp", "server", or is an MCP integration) | `ai-agents/agent-tools/mcp-servers/` |
| Agent orchestration tool (multi-agent, workflow, pipeline) | `ai-agents/agent-tools/orchestration-tools/` |
| Agent skill or skill framework | `ai-agents/agent-tools/skills/` |
| Agent profile or persona definition | `ai-agents/agent-tools/agent-profiles/` |
| Agent plugin, hook, or extension | `ai-agents/agent-tools/plugins-hooks/` |
| Prompt library, template collection | `ai-agents/agent-tools/prompts-templates/` |
| Agent monitoring, logging, observability | `ai-agents/agent-tools/monitoring-tools/` |
| Agent infrastructure (hosting, deployment, runtime) | `ai-agents/agent-tools/infrastructure/` |
| Session management tool | `ai-agents/agent-tools/session-managers/` |
| AI tool or service (Claude, ChatGPT, Elicit, etc.) | `ai-agents/tools/` |
| AI model comparison, benchmark, or analysis | `ai-agents/models/` |
| AI research paper or analysis | `ai-agents/research/` |
| AI/agent documentation, prompting guide, API docs | `ai-agents/docs/` |
| Guide page update: agent tool added | Update `ai-agents/guides/agent-tools.md` |
| Guide page update: AI tool/service added | Update `ai-agents/guides/ai-tools.md` |

## Section 2: Brown / Academic Filing (`brown/`)

| Pattern | Destination |
|---------|-------------|
| Matches existing PhD project (fibrosis, GLP-1, nanoparticle) | `brown/projects/{project}/` |
| Academic paper, journal article, preprint | `brown/literature/` |
| Web clip of academic content | `brown/literature/clips/` |
| Scientific concept or theory | `brown/concepts/` |
| Lab method or technique | `brown/methods/` |
| Academic person (professor, collaborator) | `brown/people/` |
| Grant proposal or funding | `brown/outputs/grants/` |
| Manuscript or paper draft | `brown/outputs/manuscripts/` |
| Presentation or slides | `brown/outputs/presentations/` |
| Meeting notes | `brown/meetings/` |
| Guide page update: computational tool | Update `brown/guides/computational-methods.md` |
| Guide page update: drug delivery topic | Update `brown/guides/drug-delivery.md` |
| Guide page update: paper to read | Update `brown/guides/reading-queue.md` |

## Section 3: Coding Filing (`coding/`)

| Pattern | Destination |
|---------|-------------|
| Matches existing software project (openclaw, paperbanana, vibenotes) | `coding/projects/{project}/` |
| Project idea or concept | `coding/ideas/` |
| Programming language notes or reference | `coding/languages/` |
| Framework comparison or notes | `coding/frameworks/` |
| Code snippet or recipe | `coding/snippets/` |
| Experimental code or prototype | `coding/lab/` |

## Section 4: Tech Filing (`tech/`)

| Pattern | Destination |
|---------|-------------|
| macOS app or CLI tool | `tech/mac-tools/` |
| iOS app or mobile tool | `tech/phone-tools/` |
| UI/UX design resource, component library, icon set | `tech/ui-design/` |
| General-purpose tool or utility | `tech/tools/` |
| Miscellaneous tool that doesn't fit elsewhere | `tech/extra-tools/` |
| Guide page update: macOS tool | Update `tech/guides/mac-tools.md` |
| Guide page update: iOS tool | Update `tech/guides/phone-tools.md` |
| Guide page update: design resource | Update `tech/guides/design-resources.md` |

## Section 5: NSFW Filing

**Do NOT process.** All NSFW content (`nsfw/` and `inbox/nsfw/`) is handled by a separate automation. Skip entirely.

## Section 6: Ambiguous Items

When an item doesn't clearly fit one section:

1. **Tool that uses AI but isn't an agent tool** — If it's primarily an AI-powered tool for end users (like an AI writing app), file in `ai-agents/tools/`. If it's a general tool that happens to use AI internally, file in `tech/tools/`.

2. **Academic tool** — If it's a research tool used specifically for lab work, file in `brown/methods/` or `brown/concepts/`. If it's a general tool that academics also use, file in `tech/tools/`.

3. **Multi-purpose item** — File based on the primary use case. If it's 50/50, prefer `tech/` for tools and `ai-agents/` for anything agent-related.

4. **New category needed** — If an item clearly doesn't fit any existing subfolder, create a new one under the most relevant top-level section. Document the new folder in the daily report and update `references/vault-structure.md`.

5. **Personal/life item** — File in `areas/personal/` or `areas/fitness/` as appropriate. If it's a personal tool, `tech/tools/` is fine.

6. **Default fallback** — `tech/tools/` for tools, `ai-agents/docs/` for documentation, `brown/literature/` for papers.
