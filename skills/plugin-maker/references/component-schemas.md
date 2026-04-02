# Component Schemas

Detailed format specifications for every plugin component type. Reference this
during implementation.

## Skills

**Location**: `skills/skill-name/SKILL.md`
**Format**: Markdown with YAML frontmatter

### Frontmatter Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | String | Skill identifier (lowercase, hyphens; matches dir name) |
| `description` | Yes | String | Third-person description with trigger phrases |
| `metadata` | No | Map | Arbitrary key-value pairs (e.g., `version`, `author`) |

### Example Skill

```yaml
---
name: api-design
description: >
  This skill should be used when the user asks to "design an API",
  "create API endpoints", "review API structure", or needs guidance
  on REST API best practices, endpoint naming, or request/response design.
metadata:
  version: "0.1.0"
---
```

### Writing Style Rules

- **Frontmatter description**: Third-person ("This skill should be used
  when..."), with specific trigger phrases in quotes.
- **Body**: Imperative/infinitive form ("Parse the config file," not "You should
  parse the config file").
- **Length**: Keep SKILL.md body under 3,000 words (ideally 1,500–2,000). Move
  detailed content to `references/`.

### Skill Directory Structure

```
skill-name/
├── SKILL.md              # Core knowledge (required)
├── references/           # Detailed docs loaded on demand
│   ├── patterns.md
│   └── advanced.md
├── examples/             # Working code examples
│   └── sample-config.json
└── scripts/              # Utility scripts
    └── validate.sh
```

### Progressive Disclosure Levels

1. **Metadata** (always in context): name + description (~100 words)
2. **SKILL.md body** (when skill triggers): core knowledge (<5k words)
3. **Bundled resources** (as needed): references, examples, scripts (unlimited)

## Agents

**Location**: `agents/agent-name.md`
**Format**: Markdown with YAML frontmatter

### Frontmatter Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | String | Lowercase, hyphens, 3–50 chars |
| `description` | Yes | String | Triggering conditions with `<example>` blocks |
| `model` | Yes | String | `inherit`, `sonnet`, `opus`, or `haiku` |
| `color` | Yes | String | `blue`, `cyan`, `green`, `yellow`, `magenta`, `red` |
| `tools` | No | Array | Restrict to specific tools |
| `disallowedTools` | No | Array | Tools the agent cannot use |
| `effort` | No | String | `low`, `medium`, `high` — controls reasoning depth |
| `maxTurns` | No | Number | Max conversation turns before agent stops |
| `skills` | No | Array | Skills available to this agent |
| `memory` | No | Boolean | Whether the agent retains memory |
| `background` | No | Boolean | Run in background |
| `isolation` | No | String | Only valid value: `"worktree"` |

### Example Agent

```markdown
---
name: code-reviewer
description: Use this agent when the user asks for a thorough code review or
  wants detailed analysis of code quality, security, and best practices.

<example>
Context: User has just written a new module
user: "Can you do a deep review of this code?"
assistant: "I'll use the code-reviewer agent to provide a thorough analysis."
<commentary>
User explicitly requested a detailed review, which matches this agent's specialty.
</commentary>
</example>

model: inherit
color: blue
tools: ["Read", "Grep", "Glob"]
---

You are a code review specialist focused on identifying issues across security,
performance, maintainability, and correctness.

**Analysis Process:**

1. Read all files in scope
2. Identify patterns and anti-patterns
3. Categorize findings by severity
4. Provide specific remediation suggestions

**Output Format:**
Present findings grouped by severity (Critical, Warning, Info) with:
- File path and line number
- Description of the issue
- Suggested fix
```

### Agent Naming Rules

- 3–50 characters
- Lowercase letters, numbers, hyphens only
- Must start and end with alphanumeric
- No underscores, spaces, or special characters

### Color Guidelines

- Blue/Cyan: Analysis, review
- Green: Success-oriented tasks
- Yellow: Caution, validation
- Red: Critical, security
- Magenta: Creative, generation

## Hooks

**Location**: `hooks/hooks.json`
**Format**: JSON

### Available Events

| Event | When it fires |
|-------|--------------|
| `SessionStart` | When a session begins or resumes |
| `SessionEnd` | When a session terminates |
| `UserPromptSubmit` | When the user sends a message, before Claude processes it |
| `PreToolUse` | Before a tool call executes (can block it) |
| `PostToolUse` | After a tool call succeeds |
| `PostToolUseFailure` | After a tool call fails |
| `PermissionRequest` | When a permission dialog appears |
| `Stop` | When Claude finishes a response |
| `StopFailure` | When the turn ends due to an API error |
| `SubagentStart` | When a subagent is spawned |
| `SubagentStop` | When a subagent finishes |
| `TaskCreated` | When a task is created via TaskCreate |
| `TaskCompleted` | When a task is marked completed |
| `TeammateIdle` | When an agent team teammate is about to go idle |
| `InstructionsLoaded` | When a CLAUDE.md or rules file is loaded into context |
| `ConfigChange` | When a config file changes during a session |
| `CwdChanged` | When the working directory changes |
| `FileChanged` | When a watched file changes on disk (matcher = filename) |
| `WorktreeCreate` | When a worktree is created |
| `WorktreeRemove` | When a worktree is removed |
| `PreCompact` | Before context compaction |
| `PostCompact` | After context compaction completes |
| `Notification` | When a notification fires |
| `Elicitation` | When an MCP server requests user input |
| `ElicitationResult` | After a user responds to an MCP elicitation |

### Hook Types

**Prompt-based** (recommended for complex logic):

```json
{
  "type": "prompt",
  "prompt": "Evaluate whether this file write follows project conventions: $TOOL_INPUT",
  "timeout": 30
}
```

Supported events: Stop, SubagentStop, UserPromptSubmit, PreToolUse.

**Command-based** (deterministic checks):

```json
{
  "type": "command",
  "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/validate.sh",
  "timeout": 60
}
```

**HTTP-based** (webhook POST):

```json
{
  "type": "http",
  "url": "https://api.example.com/hooks/validate",
  "timeout": 30
}
```

Sends the event JSON as a POST request to the URL.

**Agent-based** (agentic verifier with tools):

```json
{
  "type": "agent",
  "prompt": "Verify that the code changes follow the project architecture guidelines.",
  "timeout": 120
}
```

Runs an agentic verifier with tool access for complex verification tasks.

### Hook Output Format (Command Hooks)

```json
{
  "decision": "block",
  "reason": "File write violates naming convention"
}
```

Decisions: `approve`, `block`, `ask_user` (ask for confirmation).

### Example hooks.json

```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Check that this file write follows project coding standards. If it violates standards, explain why and block.",
          "timeout": 30
        }
      ]
    }
  ],
  "SessionStart": [
    {
      "matcher": "",
      "hooks": [
        {
          "type": "command",
          "command": "cat ${CLAUDE_PLUGIN_ROOT}/context/project-context.md",
          "timeout": 10
        }
      ]
    }
  ]
}
```

## MCP Servers

**Location**: `.mcp.json` at plugin root
**Format**: JSON

### Server Types

**stdio** (local process):

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/server.js"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

**SSE** (remote server, server-sent events):

```json
{
  "mcpServers": {
    "asana": {
      "type": "sse",
      "url": "https://mcp.asana.com/sse"
    }
  }
}
```

**HTTP** (remote server, streamable HTTP):

```json
{
  "mcpServers": {
    "api-service": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${API_TOKEN}"
      }
    }
  }
}
```

### Environment Variable Expansion

All MCP configs support `${VAR_NAME}` substitution:

- `${CLAUDE_PLUGIN_ROOT}` — plugin directory (always use for portability)
- `${ANY_ENV_VAR}` — user environment variables

Document all required environment variables in the plugin README.

### Directory Servers Without a URL

Some MCP directory entries have no `url` because the endpoint is dynamic.
Plugins can reference these by **name** — if the server name in the config
matches the directory entry name, it's treated the same as a URL match.

## LSP Servers

**Location**: `.lsp.json` at plugin root (or inline in plugin.json as `lspServers`)
**Format**: JSON mapping language server names to configs

LSP servers give Claude real-time code intelligence: instant diagnostics,
go-to-definition, find references, and hover information.

### Required Fields

| Field | Description |
|-------|-------------|
| `command` | The LSP binary to execute (must be in PATH) |
| `extensionToLanguage` | Maps file extensions to language identifiers |

### Optional Fields

| Field | Description |
|-------|-------------|
| `args` | Command-line arguments for the server |
| `transport` | `stdio` (default) or `socket` |
| `env` | Environment variables |
| `initializationOptions` | Options passed during initialization |
| `settings` | Settings via `workspace/didChangeConfiguration` |
| `restartOnCrash` | Auto-restart on crash |
| `maxRestarts` | Max restart attempts |

### Example .lsp.json

```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

> The plugin configures how Claude connects to a language server but does not
> bundle the server binary. Users must install the binary separately (e.g.,
> `pip install pyright`, `npm install -g typescript-language-server`).

## Output Styles

**Location**: `output-styles/style-name.md`
**Format**: Markdown defining output formatting modes

Output styles let users switch Claude's response format. Example: a `terse`
style that produces minimal output, or a `detailed` style for verbose
explanations.

## Commands (Legacy)

> Prefer `skills/*/SKILL.md` for new plugins. The `commands/` format still
> works but only use it if you specifically need single-file format with
> `$ARGUMENTS`/`$1` substitution and inline bash execution.

**Location**: `commands/command-name.md`
**Format**: Markdown with optional YAML frontmatter

### Frontmatter Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `description` | No | String | Brief description (<60 chars) |
| `allowed-tools` | No | String or Array | Tools the command can use |
| `model` | No | String | Model override: `sonnet`, `opus`, `haiku` |
| `argument-hint` | No | String | Documents expected arguments |

### Key Rules

- Commands are instructions FOR Claude, not messages for the user.
- `$ARGUMENTS` captures all arguments; `$1`, `$2`, `$3` capture positional.
- `@path` syntax includes file contents in the command context.
- `` !`command` `` executes bash inline for dynamic context.
- Use `${CLAUDE_PLUGIN_ROOT}` for plugin file references.

### allowed-tools Patterns

```yaml
# Specific tools
allowed-tools: Read, Write, Edit, Bash(git:*)

# Bash with specific commands only
allowed-tools: Bash(npm:*), Read

# MCP tools (specific)
allowed-tools: ["mcp__plugin_name_server__tool_name"]
```

## README.md

Every plugin should include a README with:

1. **Overview** — what the plugin does
2. **Components** — list of skills, agents, hooks, MCP servers
3. **Setup** — required environment variables or configuration
4. **Usage** — how to trigger each skill/command
