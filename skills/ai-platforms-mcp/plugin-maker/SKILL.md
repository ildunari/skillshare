---
name: plugin-maker
description: >
  Create, customize, debug, and manage Cowork and Claude Code plugins. Use when
  the user wants to create, build, scaffold, design, customize, configure,
  tailor, modify, or set up a plugin; add skills, MCP servers, agents, or hooks
  to a plugin; package a .plugin file; debug a plugin that isn't working; fix
  skill triggering; troubleshoot MCP connections; or test a plugin after building
  it. Also use for plugin architecture questions, component types, plugin.json
  manifests, or skill writing best practices. Covers the full lifecycle:
  discovery, planning, architecture, implementation, testing, debugging,
  customization, and packaging. Trigger even for partial requests like "add a
  skill to my plugin" or "why isn't my skill triggering." Do not use for general
  prompt writing unrelated to plugins or application code that merely mentions
  Claude.
---

# Plugin Maker

Build new Cowork plugins from scratch or customize existing ones. A plugin is a
self-contained directory that extends Claude's capabilities with skills, agents,
hooks, and MCP server integrations.

## Feedback Loop

Read `FEEDBACK.md` before every use.

1. **Detect** — After completing a build or customization, note anything that
   didn't land: a phase missed something, output quality was off, packaging
   failed, or a pattern emerged that the workflow doesn't handle.
2. **Search** — Check `FEEDBACK.md` for existing entries on the same issue.
3. **Scope** — One actionable observation per entry.
4. **Draft-and-ask** — Propose the entry: "I noticed [issue]. Want me to log this?"
5. **Write-on-approval** — Append with date and category tag.
6. **Compact-at-75** — Merge duplicates, promote patterns to reference files,
   archive resolved. Reset to ~30 entries.

## Routing

Determine which workflow to follow based on user intent:

| Signal | Workflow |
|--------|----------|
| "create a plugin", "build a plugin", "new plugin", "scaffold", no existing plugin referenced | **Create** (Phase 1–5) |
| "customize", "configure", "set up", "tailor", "modify", "adjust" + references an existing plugin | **Customize** (Phase C1–C4) |
| "add a skill/hook/agent/MCP to [existing plugin]" | **Customize** — scoped to that component |
| "not working", "doesn't trigger", "debug", "test", "troubleshoot", "MCP not connecting" | **Debug** — read `references/debugging-guide.md` |
| "how should I structure this plugin", "one skill or many", architecture questions | Read `references/plugin-architecture.md` for decision frameworks |
| "create a marketplace", "distribute plugins", "host plugins", marketplace.json, multi-plugin repo | **Marketplace** — read `references/marketplace-guide.md` |
| Ambiguous | Ask which workflow they need |

---

## Create Workflow

Walk the user through discovery, planning, design, implementation, and
packaging — delivering a ready-to-install `.plugin` file.

### Plugin Architecture

Every plugin follows this layout:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json           # Plugin manifest (recommended but optional)
├── skills/                   # Skills (subdirectories with SKILL.md)
│   └── skill-name/
│       ├── SKILL.md
│       └── references/
├── agents/                   # Subagent definitions (.md files)
├── hooks/                    # Event-driven automation
│   └── hooks.json
├── output-styles/            # Output style definitions (.md files)
├── .mcp.json                 # MCP server definitions
├── .lsp.json                 # LSP server definitions (code intelligence)
├── settings.json             # Default settings applied when plugin is enabled
└── README.md                 # Plugin documentation
```

**Rules:**
- `.claude-plugin/plugin.json` is recommended but optional — if omitted, Claude
  Code auto-discovers components in default locations and derives the name from
  the directory name. Include it when you need metadata or custom component paths.
- Component directories go at the plugin root, not inside `.claude-plugin/`
- Only create directories for components the plugin actually uses
- kebab-case for all directory and file names
- Use `${CLAUDE_PLUGIN_ROOT}` for all intra-plugin path references — never
  hardcode absolute paths
- Use `${CLAUDE_PLUGIN_DATA}` for persistent state that survives plugin updates
  (installed dependencies, caches, generated files). Located at
  `~/.claude/plugins/data/{id}/`.

### plugin.json Manifest

Located at `.claude-plugin/plugin.json`. Minimal required field is `name`.

```json
{
  "name": "plugin-name",
  "version": "0.1.0",
  "description": "Brief explanation of plugin purpose",
  "author": {
    "name": "Author Name"
  }
}
```

Name rules: kebab-case, lowercase with hyphens, no spaces or special characters.
Version: semver (MAJOR.MINOR.PATCH), start at `0.1.0`.

Custom component paths can be specified in plugin.json. Custom paths **replace**
the default directory — to keep the default and add more, include both in an
array:

```json
{
  "commands": "./custom-commands",
  "agents": ["./agents", "./specialized-agents"],
  "hooks": "./config/hooks.json",
  "mcpServers": "./.mcp.json",
  "lspServers": "./.lsp.json",
  "outputStyles": "./styles/"
}
```

User-configurable values (prompted at enable time) can be declared in
`userConfig`. Values are available as `${user_config.KEY}` in MCP/LSP configs
and hook commands, and as `CLAUDE_PLUGIN_OPTION_<KEY>` env vars:

```json
{
  "userConfig": {
    "api_endpoint": { "description": "Your API endpoint", "sensitive": false },
    "api_token": { "description": "API auth token", "sensitive": true }
  }
}
```

### Component Types

| Component | Location | Format | When to use |
|-----------|----------|--------|-------------|
| Skills | `skills/*/SKILL.md` | Markdown + YAML frontmatter | Domain knowledge, user-initiated actions, workflow guides |
| MCP Servers | `.mcp.json` | JSON | External service integration (APIs, SaaS tools) |
| Agents | `agents/*.md` | Markdown + YAML frontmatter | Autonomous multi-step tasks (uncommon in Cowork) |
| Hooks | `hooks/hooks.json` | JSON | Event-driven automation (rare in Cowork) |
| LSP Servers | `.lsp.json` | JSON | Code intelligence (go-to-definition, diagnostics, hover) |
| Output Styles | `output-styles/*.md` | Markdown | Custom output formatting modes |

Detailed schemas for each component type are in `references/component-schemas.md`.
Read it during implementation (Phase 4), not before.

> **Legacy `commands/` format**: Older plugins may have `commands/*.md` slash
> commands. Still works, but new plugins should use `skills/*/SKILL.md` instead.
> Cowork UI presents both as "Skills."

### Phase 1: Discovery

Understand what the user wants to build and why. Ask only what's unclear — skip
questions the user already answered.

- What should this plugin do? What problem does it solve?
- Who will use it and in what context?
- Does it integrate with any external tools or services?
- Is there a similar plugin or workflow to reference?

Summarize understanding and confirm before proceeding.

### Phase 2: Component Planning

Based on discovery, determine which component types are needed. Read
`references/plugin-architecture.md` if the user's needs are ambiguous or
the plugin scope is large enough to warrant structural decisions.

**Component selection:**

- **Skills** — On-demand knowledge or user-initiated actions. Most plugins
  need at least one. Skills encode *judgment* — how to think about the task.
- **MCP Servers** — External service integration. MCP provides *capabilities*.
- **Agents** (uncommon) — Noisy, parallelizable, or safety-isolated subtasks.
  Agents consume judgment in *isolation*. Cannot spawn other agents.
- **Hooks** (rare) — Deterministic event automation. Hooks enforce behavior
  even if the model has no judgment call to make. Use only at meaningful
  lifecycle boundaries (session start/end, pre-commit), not per-edit.

**Key architecture heuristics:**

1. Split by **invocation semantics**, not step count. A five-step workflow is
   one skill if the user thinks of it as one job.
2. Keep it as one skill when phases share context, artifacts, and permissions.
3. Split into multiple skills when subtasks are independently meaningful,
   happen at different lifecycle points, or have different side-effect profiles.
4. Bias toward **fewer, sharper skills** — large skill sets add repeated
   description tokens every turn and can exhaust context in long sessions.

Present a component plan table including types decided against:

```
| Component | Count | Purpose |
|-----------|-------|---------|
| Skills    | 2     | Domain knowledge for X, action for Y |
| MCP       | 1     | Connect to service Z |
| Agents    | 0     | Not needed |
| Hooks     | 0     | Not needed |
```

Get confirmation before proceeding.

### Phase 3: Design & Clarifying Questions

Specify each component in detail. Resolve all ambiguities before implementation.

**Skills:** What triggers it? What knowledge domains? Reference files needed?
If action-oriented: what arguments, what tools?

**Agents:** Proactive or on-request? Tools needed? Output format?

**Hooks:** Which events? Validate/block/modify/add context? Prompt-based or
command-based?

**MCP Servers:** Server type (stdio/SSE/HTTP)? Authentication? Tools exposed?

If user says "whatever you think is best," provide specific recommendations and
get explicit confirmation.

### Phase 4: Implementation

Read these reference files now — only the ones relevant to the components
being created:

- `references/component-schemas.md` — format specs for skills, agents, hooks,
  MCP servers
- `references/example-plugins.md` — complete example structures at three
  complexity levels
- `references/skill-writing-guide.md` — how to write skill bodies that Claude
  reliably follows (read this when creating any skill)
- `references/plugin-architecture.md` — decision frameworks and annotated
  real-world patterns (read if architecture questions arise during implementation)

**Order of operations:**

1. Create the plugin directory structure
2. Create `plugin.json` manifest
3. Create each component following schema specs
4. Create `README.md` documenting the plugin

**Skill implementation principles:**

SKILL.md is a **router plus invariants**, not documentation. It should tell
Claude how to choose the right branch and what to output. References should
tell Claude the detailed rules for that branch.

- Write operational instructions, not explanatory documentation. Reserve the
  body for actions, branches, defaults, and output contracts.
- Keep body lean: 60–120 lines for simple workflows, 100–200 for complex ones
  with 2–4 branches. Under 3,000 words max.
- Use progressive disclosure aggressively: lean SKILL.md body, detailed content
  in `references/`. Each reference file pointer must include **which** file,
  **when** to read it, and a stopping rule.
- Frontmatter description must be third-person with specific trigger phrases
  and explicit "do not use when" boundaries.
- Prefer explicit defaults over menus of equal options.
- For anything catastrophic if skipped (publish, delete, send), use hooks or
  manual invocation gates — not prose alone.

**Other component guidelines:**

- **Agents**: Description needs `<example>` blocks showing triggering conditions.
  System prompt in the markdown body.
- **Hooks**: Config in `hooks/hooks.json`. Use `${CLAUDE_PLUGIN_ROOT}` for
  script paths. Prefer prompt-based hooks for complex logic. Automate only at
  meaningful lifecycle boundaries — avoid broad PostToolUse matchers.
- **MCP configs**: `.mcp.json` at plugin root. Use `${CLAUDE_PLUGIN_ROOT}` for
  local server paths. Document required env vars in README. Default to abstract
  tool language in skill prose; only name exact MCP tools when ambiguity is costly.

### Phase 5: Review & Package

1. Summarize what was created — list each component and its purpose
2. Ask if the user wants adjustments
3. Validate: `claude plugin validate <path-to-plugin-json>` (fix errors/warnings)
4. Package — see **Packaging** section below
5. Offer to walk through the smoke test (Phase 6)

### Phase 6: Test & Debug

After packaging, walk the user through verifying the plugin works. Read
`references/debugging-guide.md` for the full debugging toolkit, diagnostic
decision tree, and non-obvious failure modes.

**Quick smoke test sequence:**

1. `claude plugin validate .` — structural validation
2. `claude --plugin-dir ./my-plugin --debug` — load locally without installing
3. `/help`, `/plugin`, `/mcp` — verify visibility
4. `/plugin-name:skill-name` — direct invocation (isolates load vs. routing)
5. Natural-language prompt that should auto-trigger → then "What skills are
   available?" to check routing
6. If hooks: trigger the relevant event, watch debug output
7. If MCP: `claude mcp list` / `claude mcp get <n>` / `/mcp`

**If something fails, classify before fixing:**
- Load failure → fix manifest, frontmatter, hooks.json, directory structure
- Routing failure → fix description wording, check disable-model-invocation,
  check `/context` for budget exclusion
- Execution failure → fix skill body, reference file handoffs
- Connectivity failure → fix MCP config, auth, env vars

**Cowork testing:** Debug in Claude Code CLI first (it has the best
observability). Validate distribution in Cowork second via direct ZIP upload.
If ZIP upload works but marketplace install doesn't, that's a delivery-pipeline
bug, not a plugin bug.

---

## Customize Workflow

Modify an existing plugin for specific needs — either scoped changes to one
component or broader reconfiguration.

### Locating the Plugin

For Cowork: `find mnt/.local-plugins mnt/.plugins -type d -name "*<plugin-name>*"`

For Claude.ai: Check `/mnt/user-data/uploads/` for uploaded plugin files, or ask
the user where the plugin lives.

If the plugin directory can't be found, tell the user: "I can't locate that
plugin. Can you upload it or point me to where it lives?"

### Determining Scope

After locating the plugin, read its files to understand the current structure.

**Scoped customization** — User asked to modify a specific part ("update the
standup skill", "change the ticket tool", "add an MCP server"). Focus only on
the relevant section.

**General customization** — User wants broad modifications. Read plugin files,
understand current config, ask what they want to change.

### Phase C1: Gather Context

If the user provided context alongside their request, record it and use it to
pre-fill answers later.

If not, ask a single focused question about what they want to change.

If knowledge MCPs are available (Slack, Google Drive, email), search them for
organizational context relevant to the customization. See
`references/search-strategies.md` for query patterns.

### Phase C2: Plan Changes

Build a list of changes to make, scoped appropriately:

- For scoped work: only items related to the specific section requested
- For general customization: identify all areas that need modification based on
  the user's stated goals

Use plain-language descriptions focused on the plugin's purpose, not file paths.

### Phase C3: Apply Changes

Work through each change using gathered context.

If context from C1 provides a clear answer: apply directly.
Otherwise: ask the user.

Types of changes: content updates, configuration values, URL patterns, MCP
server additions/removals, skill modifications.

> **Never rename** the plugin, its directories, or the name fields in manifests
> during customization.

### Phase C4: MCP Connection

After customization, check if any new tools were referenced that need MCP
servers. See `references/mcp-servers.md` for discovery and connection workflow.

For each tool identified:
1. Search the registry: `search_mcp_registry(keywords=[...])`
2. If unconnected: `suggest_connectors(directoryUuids=[...])`
3. Update the plugin's MCP config

Then package — see below.

---

## Packaging

Package the finished plugin as a `.plugin` file:

```bash
cd /path/to/plugin-dir && \
  zip -r /tmp/plugin-name.plugin . -x "*.DS_Store" -x "setup/*" && \
  cp /tmp/plugin-name.plugin /path/to/outputs/plugin-name.plugin
```

**Rules:**
- Always create the zip in `/tmp/` first, then copy to the outputs folder.
  Writing directly to outputs may fail due to permissions.
- Use the plugin name from `plugin.json` for the `.plugin` filename.
- The `.plugin` file appears in chat as a rich preview where the user can browse
  files and install by pressing a button.

If on Claude.ai with `present_files` available, copy to
`/mnt/user-data/outputs/` and present.

## Nontechnical Output

Keep all user-facing conversation in plain language. Do not expose file paths,
directory structures, schema fields, or implementation details unless the user
asks. Frame everything in terms of what the plugin will do.

## Additional Resources

Read only the files relevant to the current task.

| File | Read when… |
|------|-----------|
| `references/component-schemas.md` | Creating or editing component schemas (Phase 4) |
| `references/example-plugins.md` | Need reference structures during implementation (Phase 4) |
| `references/skill-writing-guide.md` | Writing or revising any skill body — instruction quality, progressive disclosure, description design, anti-patterns |
| `references/plugin-architecture.md` | Making structural decisions — one skill vs. many, component ownership, reference organization, MCP tool naming |
| `references/debugging-guide.md` | Testing, debugging, or troubleshooting a plugin (Phase 6 or standalone debug workflow) |
| `references/mcp-servers.md` | Discovering and connecting MCP servers (Phase C4 or MCP-scoped work) |
| `references/search-strategies.md` | Searching knowledge MCPs for organizational context (Phase C1) |
| `references/marketplace-guide.md` | Creating or managing plugin marketplaces — marketplace.json schema, source types, distribution, version management |

Do not read multiple reference files unless the task clearly spans them.
