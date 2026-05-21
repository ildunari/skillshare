---
name: "Update Global Tools"
description: "Use when the user asks to scan globally installed developer tools on the machine, update them across Homebrew, npm, and standalone binaries, and report the important version changes. Trigger on requests like 'update my global tools', 'check brew and npm globals for updates', or 'run the daily tool update workflow'; do not use for project-local dependency upgrades."
alwaysAllow: ["Bash", "Read", "Write", "Edit", "Glob", "Grep", "Agent", "WebSearch", "mcp__session__mermaid_validate", "mcp__session__transform_data"]
targets: ["Craft-MyWorkspace"]
---

# Update Global Tools Skill

You are running the daily tool update workflow. Your job is to scan the system for all installed tools, check for updates, apply them, and produce a structured visual report.

## Inventory File

The tool inventory lives at:
`/Users/kosta/.craft-agent/workspaces/my-workspace/skills/meta-tools__update-global-tools/tool-inventory.md`

Read it at the start of every run. It contains every tracked tool, its current version, update command, and last changelog notes.

## Workflow

### Phase 0: Pre-flight Check

Before spawning any sub-agents, run a quick check:

```bash
brew outdated 2>/dev/null
npm outdated -g --json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d),'outdated')" 2>/dev/null || echo "0 outdated"
```

If both show zero outdated packages, do a quick binary version check (claude, droid) against the inventory file's recorded versions. If everything matches, output "All tools up to date. Skipping." and stop — do not launch discovery sub-agents or continue to Phase 2+.

If anything is outdated, proceed to Phase 1.

### Phase 1: Discovery (Sub-agents — use haiku for speed)

Launch **parallel sub-agents** (model: haiku) to quickly scan each category. Each sub-agent should return a simple list of `tool: version` pairs.

**Sub-agent 1 — Brew scan:**
```
Run: brew outdated 2>/dev/null
Run: brew outdated --cask 2>/dev/null
Return the list of outdated packages with current -> latest versions.
```

**Sub-agent 2 — npm global scan:**
```
Run: npm outdated -g 2>/dev/null
Return the list of outdated packages with current -> latest versions.
```

**Sub-agent 3 — Standalone binaries scan:**
```
Check these binaries and compare to latest GitHub releases:
- claude (claude --version) — repo: anthropics/claude-code
- droid (~/.local/bin/droid) — check against latest
- factoryd (~/.local/bin/factoryd) — self-updating, just check version

For each, run `<tool> --version` and then check the latest release:
  gh api repos/<owner>/<repo>/releases/latest --jq '.tag_name'

Note: RTK is managed by Homebrew now, no need to check separately.
```

**Sub-agent 4 — New tool discovery + missing-tool detection (sonnet 4.6):**
```
First, read the inventory file at:
/Users/kosta/.craft-agent/workspaces/my-workspace/skills/meta-tools__update-global-tools/tool-inventory.md

Extract all tracked tool names. Note the Blocklist section AND the "Removed Tools" section — never report tools listed there.

Then scan the system:
  ls /opt/homebrew/bin/ 2>/dev/null
  ls ~/.local/bin/ 2>/dev/null
  npm ls -g --depth=0 2>/dev/null
  brew list --cask 2>/dev/null
  ls ~/.local/share/uv/tools/ 2>/dev/null

Build the canonical list of installed .app bundles (RECURSIVELY — the user organizes apps into subfolders like /Applications/AI, /Applications/Coding, /Applications/Setapp, /Applications/Utilities; an app is NOT missing just because it isn't at the top level):
  find /Applications -maxdepth 4 -name "*.app" -type d 2>/dev/null
  find ~/Applications -maxdepth 4 -name "*.app" -type d 2>/dev/null

Return THREE lists:

1. **NEW tools** — installed but not in inventory and not blocklisted/removed. For each: name, version (run `<tool> --version` if possible), location (brew / npm / ~/.local/bin / uv / cask), one-line description.

2. **MISSING tools** — tracked in inventory but binary/package/app cannot be found anywhere on the system after the recursive scans. DO NOT propose reinstalling these — assume the user removed them intentionally. Just list: name, where the inventory expected it, last recorded version. The main agent will move these to the inventory's "Removed Tools" section in Phase 4 (NOT reinstall them).

3. **LOCATION CONFLICTS** — cask apps that brew thinks are missing from `/Applications` but were found in a subfolder. List: cask name, found path, brew-recorded version.

If nothing new and nothing missing: say "No discovery changes."
```

### Phase 2: Update (Main agent)

After sub-agents return, apply updates:

1. **Brew**: `brew update && brew upgrade && brew upgrade --cask --greedy 2>&1` (covers RTK, ollama, gog, asc, node, etc.)
2. **npm**: `npm update -g 2>&1`
3. **Claude Code**: `claude update 2>&1` (if outdated)
4. **Ollama**: If brew upgraded ollama, run `brew services restart ollama`
5. **Cask app-not-found errors** — when `brew upgrade --cask` fails with "App source not there":
   - **DO NOT** auto-reinstall. The user may have intentionally moved the app to a subfolder (e.g. `/Applications/AI/`).
   - First, search for the app in `/Applications/` subfolders:
     ```bash
     find /Applications -maxdepth 4 -name "<AppName>.app" -type d 2>/dev/null
     ```
   - If found in a subfolder: **skip the reinstall**. Log it as a "Cask Location Conflict" in the report (see Phase 5). The user organized it there intentionally.
   - If NOT found anywhere: flag it in the report as "Missing Cask App" and ask the user whether to reinstall or remove from tracking. **Default: leave uninstalled** (do not reinstall without explicit user confirmation).

### Phase 3: Alerts + Changelog Research

**Run two things simultaneously:**

**A. Deprecation/warning scan (main agent)** — scan the npm update output from Phase 2 for any `warn deprecated` lines. Each one becomes a ⚠️ alert in the report. For each deprecated package note: which package, the warning message, and any replacement mentioned in the warning.

Also compare inventory-recorded versions against installed versions for all tracked tools (use `brew list --versions` and `npm ls -g --depth=0` for a quick snapshot). If any tool's installed version is newer than what the inventory records, flag it as an **Inventory Correction** — a stale record, not an update done this run.

**B. Major changelog research (sub-agent — sonnet 4.6)** — only if there were major version bumps:

- Use WebSearch to find release notes for the specific version jump
- Check GitHub releases pages
- Summarize in 3–5 bullet points per tool; call out any breaking changes explicitly

**Do NOT research minor/patch bumps** — just note the version change in the table.

Major = first number changed (1.x → 2.x) **or** a large pre-1.0 jump spanning many minors (e.g. 0.89 → 0.115).

### Phase 4: Update Inventory File

Write the updated `tool-inventory.md`:
- Update the "Last full scan" date at the top
- Update version numbers for everything that changed **and** for every inventory correction found in Phase 3A
- Update "Last Update Notes" — major changes only, 1–2 lines per tool
- Add ⚠️ deprecation note to the entry for any deprecated package
- Add any NEW tools discovered by sub-agent 4 in the appropriate section
- For each MISSING tool reported by sub-agent 4: **remove its entry from the active sections** and append a one-liner under a `## Removed Tools` section at the bottom (create the section if it doesn't exist). Format: `- **{tool}** — last seen v{version}, removed {YYYY-MM-DD}. Reason: not found on system.` Future runs read this section and never re-track or reinstall these.
- Keep the file lean — only the LAST update's notes per tool, no historical accumulation

**Never reinstall a missing tool unless the user explicitly asks.** Missing = removed by the user.

### Phase 5: Report

Use Craft Agent's native rendering tools to produce a rich, visual report — **not just markdown paragraphs and plain tables**. Structure the output in this order:

---

#### 5a. ⚠️ Alerts (only if there are deprecations, critical failures, or security notes)

Lead with this section when present — it's the most actionable content. One entry per alert:

```
### ⚠️ Alerts
- **package-name** — deprecation message. Replacement: X (if mentioned). Impact: which sources/workflows rely on this.
```

Do not bury alerts inside the update table. They get their own prominent section.

---

#### 5b. Opening summary (2–3 sentences)
Plain-English: how many tools updated, any major jumps, anything that failed. Written for someone who wants to know "what actually matters" at a glance.

---

#### 5c. Visual breakdown — Mermaid xychart

Render a horizontal bar chart showing how many tools updated per category. Only include categories with ≥1 update.

```mermaid
xychart-beta horizontal
  title "Updates by Category"
  x-axis ["Brew Formulae", "Brew Casks", "npm", "Standalone"]
  bar [N, N, N, N]
```

---

#### 5d. Updated tools — datatable

Render an **interactive datatable** with all tools that changed. Inline the rows (no `src` needed for typical runs with <20 rows).

```datatable
{
  "title": "Tool Updates — {date}",
  "columns": [
    { "key": "tool",     "label": "Tool",     "type": "text" },
    { "key": "category", "label": "Category", "type": "badge" },
    { "key": "from",     "label": "From",     "type": "text" },
    { "key": "to",       "label": "To",       "type": "text" },
    { "key": "type",     "label": "Type",     "type": "badge" },
    { "key": "notes",    "label": "Notes",    "type": "text" }
  ],
  "rows": [...]
}
```

Column values:
- `category`: `"Brew"`, `"Brew Cask"`, `"npm"`, `"Standalone"`, `"uv"`
- `type`: `"patch"`, `"minor"`, `"major"`, `"rebuild"` (formula-only rebuild, no real version change)
- `notes`: one-line summary of what changed, or empty for pure patch bumps
- Only list tools that **actually changed**. Include formula rebuilds as `"rebuild"` type.

---

#### 5e. Inventory Corrections (only if stale records were found)

A plain markdown table — small, no interactivity needed. These are tools whose inventory entry was behind what was actually installed. Nothing was installed this run; the record just needed catching up.

| Tool | Was Recorded | Actually At |
|------|-------------|-------------|

---

#### 5f. Major changes (only if there ARE major bumps)

For each tool with a major bump, a tight section:

```
#### tool-name vOLD → vNEW
- bullet 1
- bullet 2 (4–6 bullets max)
```

Major = first number changed (1.x → 2.x) **or** pre-1.0 minor jump ≥0.02 (e.g. 0.13 → 0.14, 0.37 → 0.38). Skip patch bumps entirely from this section.

---

#### 5g. New tools discovered (only if found)

A small datatable — skip standard system utilities (bat, jq, rg, tmux, tree, wget). Only surface active developer tools or AI agent integrations.

```datatable
{
  "title": "New Tools Discovered",
  "columns": [
    { "key": "tool",     "label": "Tool",       "type": "text" },
    { "key": "location", "label": "Location",   "type": "badge" },
    { "key": "version",  "label": "Version",    "type": "text" },
    { "key": "desc",     "label": "What it is", "type": "text" }
  ],
  "rows": [...]
}
```

---

#### 5h. Cask Location Conflicts (only if any)

Apps found in `/Applications` subfolders — brew can't upgrade them because it expects them at the root. These were **not reinstalled** to avoid duplicates.

```datatable
{
  "title": "Cask Location Conflicts — Action Needed",
  "columns": [
    { "key": "cask",     "label": "Cask",          "type": "text" },
    { "key": "found",    "label": "Found At",      "type": "text" },
    { "key": "version",  "label": "Brew Version",  "type": "text" },
    { "key": "action",   "label": "Action",        "type": "badge" }
  ],
  "rows": [
    { "cask": "...", "found": "/Applications/AI/Craft Agents.app", "version": "0.9.x", "action": "Move to /Applications or skip" }
  ]
}
```

---

#### 5i. Missing cask apps (only if any)

Plain list. Left uninstalled by default — ask user before taking action.

---

#### 5j. Removed tools — pruned from inventory (only if any)

Tools tracked previously but no longer found on the system. **Not reinstalled** — moved to the inventory's `## Removed Tools` list so they're never re-added on future runs. If the user wants any of them back, they can ask.

| Tool | Last Recorded Version | Where It Was |
|------|-----------------------|--------------|

---

#### 5k. Failed updates (only if any)

Plain list with the exact error and a suggested fix command if obvious.

---

#### 5l. No updates needed

Single line: `N tools already up to date.`

## Important Notes

- Always read the inventory file first
- **Check the Blocklist section** in the inventory before adding any tools. Never install, track, or re-add blocklisted tools. If a blocklisted tool appears in `brew outdated` or discovery scans, skip it silently.
- If a new tool discovery sub-agent finds a blocklisted tool, do NOT report it as new
- Use parallel sub-agents for scanning (haiku for speed, sonnet for research)
- Don't waste context on minor bumps — just update the version in the file
- **NEVER auto-reinstall cask apps.** If brew upgrade fails because the app isn't in `/Applications/` root, check subfolders first (`find /Applications -maxdepth 4 -name "*.app"`). The user organizes apps into subfolders like `/Applications/AI/`. Reinstalling creates duplicates. See Phase 2 step 5 for the full flow.
- **NEVER reinstall a tracked tool just because it's missing.** Missing = the user removed it intentionally. Move it to the inventory's "Removed Tools" section instead.
- After updating ollama, restart the service
- RTK is managed by Homebrew (`brew upgrade rtk`)
- factoryd self-updates on launch, just verify the version
- The droid CLI binary may lag behind the cask version — note discrepancies
- After the run, if any tool was deprecated or had a breaking change, store a note in mem0 (category: `environment`, source: `craft-agent`) so future sessions are aware without needing to re-discover it
