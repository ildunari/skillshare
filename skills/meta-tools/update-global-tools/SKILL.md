---
name: "Update Global Tools"
description: "Use when the user asks to scan globally installed developer tools on the machine, update them across Homebrew, npm, and standalone binaries, and report the important version changes. Trigger on requests like 'update my global tools', 'check brew and npm globals for updates', or 'run the daily tool update workflow'; do not use for project-local dependency upgrades."
alwaysAllow: ["Bash", "Read", "Write", "Edit", "Glob", "Grep", "Agent", "WebSearch"]
targets: ["Craft-MyWorkspace"]
---

# Update Global Tools Skill

You are running the daily tool update workflow. Your job is to scan the system for all installed tools, check for updates, apply them, and produce a report.

## Inventory File

The tool inventory lives at:
`/Users/kosta/.craft-agent/workspaces/my-workspace/skills/meta-tools__update-global-tools/tool-inventory.md`

Read it at the start of every run. It contains every tracked tool, its current version, update command, and last changelog notes.

## Workflow

### Phase 0: Pre-flight Check

Before spawning any sub-agents, run a quick check:

```bash
brew outdated 2>/dev/null | head -5
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

**Sub-agent 4 — New tool discovery (use sonnet 4.6):**
```
Scan the system for tools NOT in the inventory file:
- ls /opt/homebrew/bin/ and compare against known tools
- ls ~/.local/bin/ and compare
- npm ls -g --depth=0 and compare
- Check for any new brew casks: brew list --cask
- Check for pip/uv tools: ls ~/.local/share/uv/tools/ 2>/dev/null

Report any NEW tools found that aren't tracked in the inventory.
```

### Phase 2: Update (Main agent)

After sub-agents return, apply updates:

1. **Brew**: `brew update && brew upgrade && brew upgrade --cask --greedy 2>&1` (covers RTK, ollama, gog, asc, node, etc.)
2. **npm**: `npm update -g 2>&1`
3. **Claude Code**: `claude update 2>&1` (if outdated)
4. **Ollama**: If brew upgraded ollama, run `brew services restart ollama`
5. **Cask quirks**: codexbar and osaurus sometimes need `brew reinstall --cask <name>` if the app isn't in /Applications

### Phase 3: Changelog Research (Sub-agent — use sonnet 4.6)

For tools that had a **major version bump** (not just patch/minor), launch a sub-agent to research what changed:

- Use WebSearch to find release notes for the specific version jump
- Check GitHub releases pages
- Summarize in 2-5 bullet points per tool

**Do NOT research minor/patch bumps** — just note the version change.

Major = first number changed (1.x -> 2.x) OR significant feature release (0.23 -> 0.30 is major for pre-1.0 tools).

### Phase 4: Update Inventory File

Edit `tool-inventory.md`:
- Update version numbers for everything that changed
- Update "Last Update Notes" with shortened bullet-point changelogs (major changes only)
- Add any NEW tools discovered by sub-agent 4
- Keep the file lean — only the LAST update's changelog per tool, not historical

### Phase 5: Report

Output a report to the user. Format:

```
## Tool Update Report — {date}

### Updated ({count})
| Tool | From | To | Notes |
|------|------|----|-------|
...only list tools that actually changed...

### Major Changes
#### {tool name} {old} -> {new}
- bullet point 1
- bullet point 2

### New Tools Discovered
- {tool}: {version} — {what it is}

### Failed Updates
- {tool}: {error}

### No Updates Needed
{count} tools already up to date.
```

**Only include the "Major Changes" section if there ARE major changes. Skip minor/patch version bumps in the detailed notes.**

## Important Notes

- Always read the inventory file first
- **Check the Blocklist section** in the inventory before adding any tools. Never install, track, or re-add blocklisted tools. If a blocklisted tool appears in `brew outdated` or discovery scans, skip it silently.
- If a new tool discovery sub-agent finds a blocklisted tool, do NOT report it as new
- Use parallel sub-agents for scanning (haiku for speed, sonnet for research)
- Don't waste context on minor bumps — just update the version in the file
- If a brew upgrade fails for casks, try `brew reinstall --cask <name>`
- After updating ollama, restart the service
- RTK is managed by Homebrew (`brew upgrade rtk`)
- factoryd self-updates on launch, just verify the version
- The droid CLI binary may lag behind the cask version — note discrepancies
