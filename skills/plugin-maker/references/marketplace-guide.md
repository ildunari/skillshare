# Plugin Marketplace Guide

A marketplace is a Git repository that catalogs multiple plugins for
discovery and distribution. Users add the marketplace once and can install
any plugin from it.

## Marketplace vs Plugin

A **plugin** is a self-contained directory with components (skills, agents,
hooks, MCP servers). A **marketplace** is a catalog that lists plugins and
tells Claude Code where to fetch each one. A single repo can be both — if it
has `.claude-plugin/marketplace.json` AND `.claude-plugin/plugin.json`, it
functions as a marketplace when added via `marketplace add` and as a plugin
when installed directly.

## Directory Structure

```
my-marketplace/
├── .claude-plugin/
│   └── marketplace.json       # Required: marketplace catalog
├── plugins/                   # Optional: bundled plugins
│   ├── plugin-a/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   └── skills/
│   └── plugin-b/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── skills/
└── README.md
```

## marketplace.json Schema

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Marketplace identifier (kebab-case). Users see this when installing: `plugin install my-tool@marketplace-name` |
| `owner` | object | Maintainer info: `name` (required), `email` (optional) |
| `plugins` | array | List of available plugins |

### Optional Metadata

| Field | Type | Description |
|-------|------|-------------|
| `metadata.description` | string | Brief marketplace description |
| `metadata.version` | string | Marketplace version |
| `metadata.pluginRoot` | string | Base directory prepended to relative plugin source paths |

### Example

```json
{
  "name": "team-tools",
  "owner": {
    "name": "DevTools Team",
    "email": "devtools@example.com"
  },
  "metadata": {
    "description": "Internal development tools",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "code-formatter",
      "source": "./plugins/formatter",
      "description": "Automatic code formatting",
      "version": "2.1.0"
    },
    {
      "name": "deploy-tools",
      "source": {
        "source": "github",
        "repo": "company/deploy-plugin"
      },
      "description": "Deployment automation"
    }
  ]
}
```

## Plugin Entry Fields

Each entry in the `plugins` array requires `name` and `source`. All other
fields from the plugin.json schema are also valid here (description, version,
author, homepage, repository, license, keywords, commands, agents, hooks,
mcpServers, lspServers).

Additional marketplace-specific fields:

| Field | Type | Description |
|-------|------|-------------|
| `category` | string | Plugin category for organization |
| `tags` | array | Tags for searchability |
| `strict` | boolean | Controls authority for component definitions (default: true) |

### Strict Mode

- **`true`** (default): plugin.json is authority. Marketplace entry supplements.
- **`false`**: Marketplace entry is entire definition. If plugin also has a
  plugin.json with components, that's a conflict and the plugin fails to load.

## Plugin Source Types

### Relative Path (bundled in marketplace repo)

```json
{ "source": "./plugins/my-plugin" }
```

Paths resolve relative to marketplace root (the directory containing
`.claude-plugin/`). Must start with `./`. Only works when the marketplace
is added via Git (not URL).

### GitHub Repository

```json
{
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4e5f6..."
  }
}
```

`ref` and `sha` are optional. Pin to a tag or commit for reproducibility.

### Git URL

```json
{
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git",
    "ref": "main"
  }
}
```

### Git Subdirectory (for monorepos)

```json
{
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/company/monorepo.git",
    "path": "tools/claude-plugin"
  }
}
```

Uses sparse clone to fetch only the subdirectory.

### npm Package

```json
{
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin",
    "version": "^2.0.0",
    "registry": "https://npm.example.com"
  }
}
```

## Common Mistakes

### 1. Top-level `version` / `description` / `$schema` instead of `metadata.*`

**The most dangerous mistake — seen in the wild in 2026-04, it partially
breaks plugin discovery.** The official schema puts `description`, `version`,
and `pluginRoot` under a `metadata` object. Do **not** hoist them to the top
level, and do **not** add a `$schema` field — it is not part of the spec.

```json
// ❌ WRONG — Claude Code won't load the marketplace cleanly
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "my-plugins",
  "version": "1.0.3",
  "description": "My plugins",
  "owner": { "name": "me" },
  "plugins": [ ... ]
}

// ✅ RIGHT
{
  "name": "my-plugins",
  "owner": { "name": "me" },
  "metadata": {
    "description": "My plugins",
    "version": "1.0.3"
  },
  "plugins": [ ... ]
}
```

**Symptom:** the marketplace refuses to add, or adds but only a partial set
of plugins resolves and users see whatever was last successfully cached.
This exact bug was introduced into `ildunari/kosta-plugins` by an automated
Copilot PR that "fixed" the manifest by flattening `metadata`. Always diff
Copilot-authored marketplace PRs against the schema, and run
`claude plugin validate .` before merging.

### 2. Stray `marketplace.json` inside a plugin folder

A plugin directory (`plugins/<name>/.claude-plugin/`) must contain
`plugin.json`, never `marketplace.json`. If you inline a plugin that used to
be its own marketplace, delete the old `marketplace.json` from inside the
plugin folder as part of the inlining. Leaving both files produces a
malformed plugin that some loaders will reject.

### 3. Referencing a marketplace as a plugin source

If a plugin entry's `source` points to a repo that only has a
`marketplace.json` (no `plugin.json` and no auto-discoverable components at
root), Claude Code will clone it and fail to find a plugin. Fix: either add a
root `plugin.json` to the target repo, or use `git-subdir` to point at the
specific plugin directory inside it.

### 4. Version not bumped after changes

Claude Code uses the version to decide whether to update cached plugins. If
you change code but don't bump the version, existing users won't see changes.
Set version in either plugin.json or the marketplace entry — avoid setting it
in both (plugin.json wins silently). For cache-invalidation purposes, bumping
`metadata.version` in `marketplace.json` is the cleanest lever.

### 5. Relative paths in URL-based marketplaces

URL-based marketplaces (`marketplace add https://...`) only download the JSON
file, not the repo. Relative paths won't resolve. Use GitHub, npm, or git URL
sources instead, or add the marketplace via Git.

### 6. Broken YAML frontmatter in any skill / agent / command

A single malformed frontmatter block in any skill, agent, or command file
prevents the **entire plugin** from loading — not just that file. Same goes
for a malformed `hooks/hooks.json`. Always run `claude plugin validate .`
before committing, and prefer a CI job that fails the build on validation
errors.

### 7. `${CLAUDE_PLUGIN_ROOT}` mistakes

Plugins are copied to `~/.claude/plugins/cache/...` on install, so any
reference outside the plugin directory (via `..`) breaks. Use
`${CLAUDE_PLUGIN_ROOT}` inside hooks and MCP server configs to point at
plugin-local files. Use `${CLAUDE_PLUGIN_DATA}` (not `${CLAUDE_PLUGIN_ROOT}`)
for persistent state that should survive plugin upgrades.

### 8. Reserved marketplace names

These names cannot be used and attempting to register them will fail:
`claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`,
`anthropic-marketplace`, `anthropic-plugins`, `agent-skills`,
`knowledge-work-plugins`, `life-sciences`. Names that *impersonate* official
marketplaces (like `official-claude-plugins`) are also blocked.

## Pre-Distribution Checklist

Before pushing a marketplace update:

- [ ] `claude plugin validate .` returns clean
- [ ] `marketplace.json` has `name`, `owner`, `plugins` at top level —
      nothing else at top level except `metadata`
- [ ] `metadata.version` bumped since last release
- [ ] Every plugin in `plugins/` has a `.claude-plugin/plugin.json` with a
      `name` field and no stray `marketplace.json` alongside it
- [ ] No `$schema`, no top-level `version`, no top-level `description`
- [ ] CI runs `claude plugin validate .` or an equivalent schema check on
      every PR — this catches automated "fix" PRs that flatten `metadata`

## Distribution

### Host on GitHub (recommended)

```bash
claude plugin marketplace add owner/repo
```

### Host on other Git services

```bash
claude plugin marketplace add https://gitlab.com/company/plugins.git
```

### Private repositories

Works if `git clone` works in your terminal. For background auto-updates, set
the appropriate token: `GITHUB_TOKEN`, `GITLAB_TOKEN`, or `BITBUCKET_TOKEN`.

### Team distribution via project settings

Add to `.claude/settings.json` in your repo:

```json
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  },
  "enabledPlugins": {
    "formatter@team-tools": true
  }
}
```

Team members are prompted to install when they trust the project folder.

## Validation

```bash
claude plugin validate .
```

Checks marketplace.json syntax, plugin.json schemas, frontmatter, and
hooks.json. Fix all errors before distributing.
