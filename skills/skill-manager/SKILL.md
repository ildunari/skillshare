---
name: skill-manager
user-invocable: true
description: >
  Use when managing shared skills across coding agents through SkillSync Dash,
  especially for requests like "install this skill", "add skill", "update skills",
  "sync skills", "skill status", "what skills do I have", "edit skill", "remove skill",
  "change GitHub repo", "push skills", or "pull skills". Also use when the task is
  to propagate skill changes across multiple agents from one source of truth. Use this
  for the local SkillSync Dash workflow, not for skillshare CLI workflows under
  ~/.config/skillshare.
---

# Skill Manager

Manage skills across all coding agents through the SkillSync Dash server (port 3849).
All skill changes are committed and pushed to GitHub automatically so every machine stays in sync.

## Key Paths

- **Git repo (editable source):** `~/LocalDev/kosta-agent-skills/skills/`
- **Canonical dir (auto-synced from repo):** `~/.agents/skills/`
- **Agent skill dirs (symlinks):** `~/.claude/skills/`, `~/.codex/skills/`, etc.

**Always edit skills in the git repo directory** — agent dirs contain symlinks that are managed by SkillSync.

## Installing a Skill

### From a GitHub repository

```bash
# 1. Clone or download the skill into the repo
cd ~/LocalDev/kosta-agent-skills/skills/
git clone https://github.com/owner/repo.git skill-name
# Or just create the directory and SKILL.md manually

# 2. Commit and push — this syncs to all agents and all computers
curl -s -X POST http://localhost:3849/api/skills/commit-push \
  -H 'Content-Type: application/json' \
  -d '{"message":"install: skill-name from owner/repo"}'
```

### From scratch (creating a new skill)

```bash
# 1. Create the skill directory and SKILL.md in the repo
mkdir -p ~/LocalDev/kosta-agent-skills/skills/my-new-skill
cat > ~/LocalDev/kosta-agent-skills/skills/my-new-skill/SKILL.md << 'SKILL_EOF'
---
name: my-new-skill
description: What this skill does and when to use it
---

# My New Skill

Instructions for the coding agent...
SKILL_EOF

# 2. Commit and push
curl -s -X POST http://localhost:3849/api/skills/commit-push \
  -H 'Content-Type: application/json' \
  -d '{"message":"install: my-new-skill"}'
```

## Editing a Skill

```bash
# 1. Edit the SKILL.md directly in the repo
# (Use Read/Edit tools to modify ~/LocalDev/kosta-agent-skills/skills/<name>/SKILL.md)

# 2. Commit and push
curl -s -X POST http://localhost:3849/api/skills/commit-push \
  -H 'Content-Type: application/json' \
  -d '{"message":"edit: <name> — <what changed>"}'
```

## Removing a Skill

```bash
# 1. Delete from the repo
rm -rf ~/LocalDev/kosta-agent-skills/skills/<name>/

# 2. Commit and push
curl -s -X POST http://localhost:3849/api/skills/commit-push \
  -H 'Content-Type: application/json' \
  -d '{"message":"remove: <name>"}'
```

## Syncing (Pull Latest from GitHub)

```bash
curl -s -X POST http://localhost:3849/api/sync/pull
```

This pulls from GitHub, rsyncs to canonical dir, and re-applies active profiles.

## Checking Status

### Sync status vs GitHub
```bash
curl -s http://localhost:3849/api/sync/compare | jq '{status, aheadCount, behindCount, localChanges, remoteChanges}'
```

### Drift detection (what's out of sync on disk)
```bash
curl -s http://localhost:3849/api/drift | jq
```

### List all skills
```bash
ls ~/.agents/skills/ | head -20
curl -s http://localhost:3849/api/state | jq '.totalSkills'
```

### Recent activity
```bash
curl -s http://localhost:3849/api/journal | jq '.entries[:5]'
```

## Applying Profiles and Packs

### Apply a skill pack to an agent
```bash
curl -s -X POST http://localhost:3849/api/folders/apply \
  -H 'Content-Type: application/json' \
  -d '{"folderName":"<pack-name>","agentId":"claude-code"}'
```

### Apply a unified profile
```bash
curl -s -X POST http://localhost:3849/api/unified-profiles/apply \
  -H 'Content-Type: application/json' \
  -d '{"agentId":"claude-code","profile":"ios","force":true}'
```

## Changing the GitHub Repository

To use a different GitHub repo as the source of truth:

```bash
curl -s -X PUT http://localhost:3849/api/repo-info \
  -H 'Content-Type: application/json' \
  -d '{"remoteUrl":"https://github.com/<owner>/<repo>.git"}'
```

Check current repo:
```bash
curl -s http://localhost:3849/api/repo-info | jq
```

## Supported Agents

| Agent | Skill Directory | CLI |
|-------|----------------|-----|
| Claude Code | `~/.claude/skills` | `claude` |
| Codex | `~/.codex/skills` | `codex` |
| Cursor | `~/.cursor/rules` | — |
| Windsurf | `~/.windsurf/skills` | — |
| Cline | `~/.cline/skills` | — |
| Droid | `~/.factory/skills` | `droid` |
| Xcode | `~/Library/Developer/Xcode/.../skills` | — |
| Kiro | `~/.kiro/skills` | `kiro` |

## Important Rules

1. **Always edit in the git repo** (`~/LocalDev/kosta-agent-skills/skills/`), never in agent dirs (those are symlinks)
2. **Always commit+push after changes** so GitHub stays as the source of truth
3. **Use the `/api/skills/commit-push` endpoint** — it handles staging, committing, pushing, rsyncing, and re-applying profiles in one call
4. **Pull before making changes** if unsure whether GitHub has updates from another machine
5. **Profile auto-detection** is handled by SkillSync — when you open a project, the right profile is applied based on file patterns (Package.swift → ios, package.json → web, etc.)
