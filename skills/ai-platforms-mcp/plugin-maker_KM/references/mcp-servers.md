# MCP Discovery and Connection

How to find and connect MCP servers during plugin creation or customization.

## Available Tools

### `search_mcp_registry`

Search the MCP directory for available connectors.

**Input:** `{ "keywords": ["array", "of", "search", "terms"] }`

**Output:** Up to 10 results, each with:
- `name`: MCP display name
- `description`: One-liner description
- `tools`: List of tool names the MCP provides
- `url`: MCP endpoint URL (use this in `.mcp.json`)
- `directoryUuid`: UUID for use with suggest_connectors
- `connected`: Boolean — whether user has this MCP connected

### `suggest_connectors`

Display Connect buttons to let users install/connect MCPs.

**Input:** `{ "directoryUuids": ["uuid1", "uuid2"] }`

**Output:** Renders UI with Connect buttons for each MCP.

## Category-to-Keywords Mapping

| Category | Search Keywords |
|----------|----------------|
| `project-management` | `["asana", "jira", "linear", "monday", "tasks"]` |
| `software-coding` | `["github", "gitlab", "bitbucket", "code"]` |
| `chat` | `["slack", "teams", "discord"]` |
| `documents` | `["google docs", "notion", "confluence"]` |
| `calendar` | `["google calendar", "calendar"]` |
| `email` | `["gmail", "outlook", "email"]` |
| `design-graphics` | `["figma", "sketch", "design"]` |
| `analytics-bi` | `["datadog", "grafana", "analytics"]` |
| `crm` | `["salesforce", "hubspot", "crm"]` |
| `wiki-knowledge-base` | `["notion", "confluence", "outline", "wiki"]` |
| `data-warehouse` | `["bigquery", "snowflake", "redshift"]` |
| `conversation-intelligence` | `["gong", "chorus", "call recording"]` |

## Workflow

1. **Identify the tool** — From user input or knowledge MCP search results
2. **Search the registry** — `search_mcp_registry` with mapped keywords, or
   search for the specific tool name if already known
3. **Check connection status** — If `connected: true`, skip to step 5
4. **Connect** — `suggest_connectors(directoryUuids=[...])`, user completes auth
5. **Update plugin config** — Add the server entry to `.mcp.json`

## Updating Plugin MCP Configuration

### Finding the Config File

1. Check `plugin.json` for an `mcpServers` field pointing to a custom location
2. If no custom path, use `.mcp.json` at the plugin root (default)
3. If `mcpServers` only points to `.mcpb` files (bundled servers), create a new
   `.mcp.json` at the plugin root

### Config File Format

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```

Use the `url` field from `search_mcp_registry` results.

### Directory Entries Without a URL

Some entries have no `url` because the endpoint is dynamic. Reference these by
**name** in the plugin config — if the name matches the directory entry name,
it's treated the same as a URL match.
