# Testing, Debugging, and Iterating on Plugins

## Debugging Toolkit

### CLI Tools

| Command | What it does |
|---|---|
| `claude plugin validate .` | Check plugin.json, frontmatter, hooks.json structure |
| `claude --plugin-dir ./my-plugin` | Load plugin locally without installing |
| `claude --plugin-dir ./my-plugin --debug` | Load with debug logging enabled |
| `claude --bare` | Skip all autodiscovery (hooks, skills, plugins, MCP, CLAUDE.md) |
| `claude --disable-slash-commands` | Isolate skill/command effects |
| `claude mcp list` | Show configured MCP servers |
| `claude mcp get <name>` | Inspect one MCP server, verify auth |

### In-Session Commands

| Command | What it does |
|---|---|
| `/help` | List available skills and commands |
| `/agents` | List available agents |
| `/plugin` | Plugin manager — check Errors tab for load failures |
| `/reload-plugins` | Hot-reload changes without restarting session |
| `/mcp` | Live MCP server status, including plugin-provided servers |
| `/context` | Check context budget — warns when skills are excluded |
| `/debug` | Enable debug logging mid-session |
| `/doctor` | Installation/configuration sanity check |
| `Ctrl+O` | Show hook progress in transcript |

## Standard Smoke Test Sequence

Run this on every new plugin before considering it done.

### 1. Validate from plugin root

```bash
claude plugin validate .
```

Expect clean output. Common failures: invalid manifest syntax, missing
required fields, malformed hooks.json, duplicate plugin names.

### 2. Load locally with debug

```bash
claude --plugin-dir ./my-plugin --debug
```

Local `--plugin-dir` takes precedence over installed marketplace copies
for that session. Test here first, install second.

### 3. Run visibility checks

```
/help
/agents
/plugin
/reload-plugins
/mcp
```

Healthy: skills appear in `/help`, agents in `/agents`, `/reload-plugins`
reports counts without errors, `/plugin` Errors tab is empty, `/mcp` shows
plugin-provided servers.

### 4. Invoke one skill directly

```
/my-plugin:my-skill
```

Direct invocation separates load problems from routing problems. If this
fails, the plugin is not loading correctly. If this works but natural
language does not, the plugin loads fine — you are debugging routing.

### 5. Test natural-language triggering

Run one prompt that should auto-trigger the skill. Then ask:

```
What skills are available?
```

If the skill does not appear, check the description wording, `/context`
for budget exclusion, and `disable-model-invocation` in frontmatter.

### 6. Trigger one hook event

Cause the event your hook listens for (write a file for `Write|Edit`,
run a bash command for `Bash`). Watch `claude --debug` output.
Use `Ctrl+O` for transcript-level hook detail.

### 7. Validate MCP separately from skills

```
claude mcp list
claude mcp get my-server
/mcp
```

If the skill works but `/mcp` is empty or unauthenticated, you have an
MCP problem, not a skill problem. Test MCP in isolation before blaming
the skill.

## Diagnostic Decision Tree

Use in order when something isn't working.

```
Start
│
├─ Does `claude plugin validate .` fail, or `/plugin` → Errors show issues?
│  └─ Yes → Fix manifest/frontmatter/hooks/structure first.
│
├─ Does direct invocation work? (`/plugin-name:skill-name`)
│  └─ No → Load/visibility/path/frontmatter problem, not a trigger problem.
│
├─ Direct invocation works, but natural language does not?
│  └─ Check:
│     • Description wording — does it contain words users actually say?
│     • `disable-model-invocation` — is it accidentally true?
│     • "What skills are available?" — does the skill appear?
│     • `/context` — is the skill excluded due to budget?
│     • Competition — are other skills with similar descriptions installed?
│
├─ Skill runs, but side effects are missing?
│  ├─ Hook missing → inspect `claude --debug`, use `Ctrl+O`, verify:
│  │  • chmod +x on hook scripts
│  │  • Valid shebang line
│  │  • ${CLAUDE_PLUGIN_ROOT} in command paths
│  │  • Case-sensitive event names
│  │  • Correct matcher pattern
│  │  • Whether `async: true` is delaying output to next turn
│  └─ MCP missing → check `/mcp`, `claude mcp list/get`, verify:
│     • Auth status
│     • Transport type (prefer HTTP over deprecated SSE)
│     • ${CLAUDE_PLUGIN_ROOT} and env var expansion
│
└─ Works locally with `--plugin-dir`, breaks after install or in Cowork?
   └─ Suspect caching, versioning, or delivery:
      • Bump version in plugin.json
      • /reload-plugins
      • Test via direct ZIP upload in Cowork
      • If ZIP works but marketplace doesn't, it's a delivery bug
```

## Non-Obvious Failure Modes

### 1. Plugin loads, but components are missing

Three common causes:

- **Wrong placement**: Only plugin.json belongs inside `.claude-plugin/`.
  Skills, agents, hooks, commands go at the plugin root.
- **Custom path replaces default**: Declaring a custom `skills` path in
  plugin.json stops Claude from scanning the default `skills/` folder
  unless you explicitly include both paths in the array.
- **Marketplace path errors**: These appear as "No commands found in
  plugin" or "Plugin directory not found at path."

### 2. Skill exists but doesn't auto-trigger

Beyond description wording:

- `disable-model-invocation: true` prevents auto-loading (skill only
  runs via slash command).
- `user-invocable: false` hides from slash menu but allows auto-invoke.
- Context budget exceeded: `/context` shows when skills are excluded.
- **Don't use `claude -p` for trigger testing** — there's an open bug
  (March 2026) where headless `-p` produces 0% recall on should-trigger
  cases even when the same skills fire correctly in interactive sessions.
  Use interactive sessions for routing accuracy testing.

### 3. Skill runs but ignores reference files after install

Suspect file resolution, not prompting. Installed plugins are copied to
`~/.claude/plugins/cache`. Paths that traverse outside the plugin root
(e.g., `../shared-utils`) break because external files are not copied.

Fix: keep all files inside the plugin root. Use `${CLAUDE_PLUGIN_ROOT}`
for bundled files and `${CLAUDE_PLUGIN_DATA}` for persistent state that
survives updates.

### 4. Hooks don't fire or fire at wrong time

Mechanical checks first:
- `chmod +x` on hook scripts
- Valid shebang line
- `${CLAUDE_PLUGIN_ROOT}` in command paths
- Case-sensitive event names (e.g., `PreToolUse` not `pretooluse`)
- Correct matcher regex

Timing issue: if `async: true`, the hook cannot block the action and its
output returns on the **next** turn, not immediately. If your hook feels
"late," check this before assuming lifecycle breakage.

Known bugs (as of March 2026):
- User-typed slash commands (`/my-skill`) don't trigger `PreToolUse` /
  `PostToolUse` hooks matched on `Skill`. Only `UserPromptSubmit` fires.
- Skill-scoped hooks in SKILL.md frontmatter may not fire when the skill
  lives inside a plugin. Put plugin hooks in `hooks/hooks.json` instead.

### 5. MCP is the part that's actually broken

Debugging path:
1. `/mcp` for live status
2. `claude mcp list` to see configured servers
3. `claude mcp get <name>` to inspect and verify auth
4. For standalone testing: `claude mcp add` before wiring into plugin

Non-obvious failures:
- Missing env vars in `.mcp.json` can prevent config parsing entirely.
- Local/project/user MCP scopes have precedence rules — a local config
  duplicating a claude.ai connector causes the connector to be skipped.
- Cosmetic "MCP server skipped — same command/URL" messages in `/plugin`
  Errors can be noise, not actual failures.
- On Windows, stdio servers via `npx` need `cmd /c` prefix.

**Known --plugin-dir MCP bug**: When loading via `--plugin-dir`, plugin
components load but MCP servers may not start. Workaround:

```bash
claude --plugin-dir ~/.claude/plugins/my-plugin \
       --mcp-config ~/.claude/plugins/my-plugin/.mcp.json
```

## Claude Code vs. Cowork: The Edit-Test Cycle

**Debug in Claude Code CLI first.** It has `--plugin-dir`, `/reload-plugins`,
`/plugin` Errors, `/mcp`, `/context`, `/debug`, and `/doctor`.

**Validate distribution in Cowork second.** Cowork supports installing from
the plugin browser or uploading a custom plugin ZIP directly. Admin-managed
plugins can be distributed via manual ZIP upload or GitHub sync.

If the same plugin works in Claude Code and in Cowork via direct ZIP upload,
but breaks from a Cowork marketplace install, that's strong evidence of a
delivery-pipeline bug rather than a plugin-authoring bug.

### Hot Reload vs. Version Bumps

- **Local development**: `/reload-plugins` applies changes without restart.
- **Distributed updates**: Bump the version in plugin.json. Claude Code
  uses the version to decide whether to update cached plugins.
- **Stale marketplace state**: May occasionally require full
  uninstall → remove-marketplace → add-marketplace → reinstall cycle.

## Practical Debugging Workflow

Experienced plugin authors consistently follow this pattern:

1. **Reduce surface area first.** Test one plugin at a time with
   `--plugin-dir`. Invoke one skill directly. Only then test
   natural-language routing.
2. **Use controls.** `claude --bare` removes the entire extension layer
   (hooks, skills, plugins, MCP, CLAUDE.md) — good baseline for "does
   this problem disappear without extensions?"
3. **Prefer interactive trigger testing** over headless `claude -p` due
   to the known skill-trigger recall bug.
4. **Treat Cowork ZIP upload as an isolation tool.** If direct upload
   works and marketplace install doesn't, stop editing the plugin and
   debug distribution instead.
5. **Classify before you fix.** Figure out whether the failure is in
   load, routing, execution, or connectivity before changing anything.
