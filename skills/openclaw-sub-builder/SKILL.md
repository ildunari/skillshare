---
name: openclaw-sub-builder
description: Use when creating a new OpenClaw sub-agent profile, especially for requests like /sub, "make a new agent", "create a profile", "add a sub-agent", or "set up a new agent role". Also use when the task includes scaffolding the sub-agent directory, writing AGENTS.md or SOUL.md, registering it in openclaw.json, and verifying that the new agent works.
---

# OpenClaw Sub Builder

Build complete, ready-to-spawn OpenClaw sub-agent profiles. Handles the full lifecycle: requirements gathering, file scaffolding, config registration, git commit, and verification.

## `/sub` Command

When the user writes `/sub` followed by a description, or just `/sub` with context in the conversation:

1. **`/sub [text]`** — Use `[text]` as the agent spec. Extract role, ID, voice, and scope. If sparse, ask the minimum questions needed to fill gaps.
2. **`/sub`** (no arguments) — Pull context from the current conversation. Look for any agent descriptions, role definitions, or personality traits discussed. Synthesize into a spec and confirm before building.

In both cases, run the complete pipeline (Steps 1–7) and report the result.

## Feedback Loop

When reading this skill, also read `FEEDBACK.md` in this skill's directory (if it exists) for accumulated improvements.

Feedback protocol:
1. **Detect** — After each profile creation, note what worked and what didn't
2. **Search** — Check if similar feedback already exists
3. **Scope** — Keep feedback entries to 1-2 lines, category-tagged
4. **Draft and ask** — Propose the feedback entry to the user
5. **Write on approval** — Append to FEEDBACK.md
6. **Compact at 75** — When entries hit 75, consolidate patterns into rules

Categories: `[scaffold]` `[template]` `[config]` `[verify]` `[voice]` `[workflow]`

---

## Prerequisites

Before starting, verify these exist (create if missing):

| Path | Purpose |
|------|---------|
| `~/.openclaw/workspace-profiles/` | Profile root directory |
| `~/.openclaw/openclaw.json` | OpenClaw config with `agents.list` |

If the profiles directory doesn't exist, create it. If `openclaw.json` doesn't exist or lacks `agents.list`, alert the user — something's wrong with their OpenClaw install.

---

## Pipeline

### Step 1: Gather Requirements

Extract from the user's request or ask for what's missing.

**Required (must have before building):**

| Field | Description | Example |
|-------|-------------|---------|
| **Role** | What does this agent do? 1-2 sentences. | "Deep research and analysis, producing structured reports with citations." |
| **ID** | Short lowercase name, no spaces. | `researcher`, `writer`, `sysadmin` |

**Optional (use sensible defaults if not specified):**

| Field | Default | Description |
|-------|---------|-------------|
| Display name | Capitalized ID | Human-readable name for logs |
| Model | `agents.defaults.subagents.model` | Override default model |
| Voice/tone | Direct and professional | Communication style |
| Specific skills | None | Agent-specific skills beyond main workspace |
| Safety rules | None | Only if handling sensitive content |
| Shared files | USER.md symlink | Which files to share with main workspace |
| Identity/persona | None | Only if agent needs a distinct persona |

**If the user gives enough info upfront, don't ask — just build.**

### Step 2: Scaffold the Directory

```bash
mkdir -p ~/.openclaw/workspace-profiles/<id>
```

### Step 3: Write AGENTS.md

This is the runtime contract — the most important file. Follow this schema exactly:

```markdown
# [Agent Name] — Runtime Contract

Last updated: YYYY-MM-DD

Purpose: [One sentence describing this agent's role and workspace.]

---

## Session Start (Required)

Before responding:
1. Read `SOUL.md`
2. Read `MEMORY.md` (if exists)
3. [Any other startup reads — daily memory, shared files, etc.]

---

## Core Role

[1-3 sentences defining what this agent does. Be specific.]

[Optional: list primary task loops or workflows]

---

## Execution Behavior

[How the agent should work:]
- [Communication style during work — status updates? silent until done?]
- [How to handle ambiguity — ask or make a call?]
- [How to handle errors — retry? escalate? report?]
- [Verification requirements — always test? spot-check? trust the output?]

---

## Scope & Safety

[What the agent is allowed to do and where:]
- [Write scope — which directories, repos, services]
- [Read scope — what can it access]
- [Forbidden actions — what it must never do]
- [Escalation rules — when to stop and ask the user]

---

## [Domain-Specific Sections]

[Add sections relevant to the agent's role. Examples:]
- "Research Methodology" for a researcher
- "Code Standards" for a coder
- "Output Format" for a report writer
- "Source Priorities" for a discovery agent

---

## Sub-Agent Discipline

### Checkpoint Protocol
Every 5-10 tool calls, write a brief text checkpoint, then continue working:
1. **Done so far:** 1-2 sentences on what you've completed
2. **Next:** what you plan to do next
3. **Issues:** if you've hit a blocker, list 3 possible solutions ranked by likelihood, then try them in order

After writing the checkpoint, resume your task immediately. This is a quick status update, not a pause point.

### Error Recovery
If something fails or produces unexpected results:
1. Assess what went wrong — don't retry blindly
2. List 3 possible causes, ranked by likelihood
3. Try the most likely fix first
4. If 2 fixes fail, note the issue for your final response and move on to the rest of your task

### Final Response Rule
**CRITICAL:** Your very last message MUST be a plain text response containing your findings/results. Never end on a tool call or thinking block. The announcement system can only read text blocks — if your last message is a tool call, your work will be lost and reported as "(no output)."

---

## Link-Outs

[References to external docs, runbooks, or shared resources the agent may need.]
```

**AGENTS.md rules:**
- Session Start must be the first section after the header
- Keep it under 200 lines — split domain content into linked docs if longer
- Don't duplicate SOUL.md content (voice/personality goes there, not here)
- Include the "Last updated" date for staleness tracking
- The Sub-Agent Discipline block is **mandatory** — it prevents runaway tool chains and lost output

### Step 4: Write SOUL.md

This is the personality file. Follow this schema:

```markdown
# SOUL.md — [Agent Name]

## Role
[1-2 sentences: what kind of entity is this? Senior engineer? Research analyst? Casual assistant?]

## Voice
- Tone: [e.g., direct, warm, technical, casual, formal]
- Length: [e.g., match complexity of ask, default concise, always thorough]
- Structure: [e.g., paragraphs over lists, tables when useful, headers for long responses]
- Humor: [e.g., dry one-liners, none, playful, situational]

## Signature Behaviors
[What makes this agent distinctive?]
- [e.g., "Always leads with substance — first sentence contains real information"]
- [e.g., "Shows reasoning, but doesn't overexplain"]
- [e.g., "Cites sources with dates"]

## Anti-Patterns
[Things this agent should never do]
- [e.g., "No canned AI phrasing: 'Great question', 'I'd be happy to help'"]
- [e.g., "Don't restate the user's question"]
- [e.g., "Don't hedge when the answer is clear"]

## Canonical Rules
- Operational behavior and safety live in `AGENTS.md`.
- If guidance conflicts, `AGENTS.md` wins.
```

**SOUL.md rules:**
- Keep it under 80 lines
- Be concrete — "direct and technical" beats "communicates effectively"
- Anti-patterns are often more useful than positive rules
- The Canonical Rules footer is mandatory — it establishes AGENTS.md > SOUL.md hierarchy
- "Helpful and professional" describes every agent — be specific about what makes this one *different*

### Step 5: Write Optional Files

Create these only when needed:

**USER.md** — Symlink to main workspace (default):

```bash
cd ~/.openclaw/workspace-profiles/<id> && ln -s ../../workspace/USER.md USER.md
```

Only create a custom USER.md if this agent needs a different/reduced view of the user (e.g., stripping PII for a less-trusted agent).

**MEMORY.md** — Start empty:

```markdown
# MEMORY.md — [Agent Name] Persistent Memory

*Empty — will be populated through use.*
```

**IDENTITY.md** — Only if the agent has a distinct persona (name, emoji, avatar):

```markdown
# IDENTITY.md — Who Am I?

- **Name:** [agent name]
- **Creature:** [what it is]
- **Vibe:** [personality keywords]
- **Emoji:** [representative emoji]
- **Avatar:** [path to avatar image, or "none"]
```

**SAFETY.md** — Only for agents handling sensitive content:

```markdown
# SAFETY — [Agent Name] Safety Rules

## Hard Refusals (non-negotiable)
- [refusal rule]

## Soft Boundaries (configurable)
- [boundary]

## Escalation
- [when to stop and ask the user]
```

**Directories** — Create only when needed:
- `skills/` — Agent-specific skills (symlink shared ones from main workspace)
- `scripts/` — Agent-specific utility scripts
- `docs/` — Reference material, runbooks

### Step 6: Validate

After creating all files, verify:

- [ ] AGENTS.md exists and has: Session Start, Core Role, Execution Behavior, Scope & Safety, Sub-Agent Discipline
- [ ] SOUL.md exists and has: Role, Voice, Signature Behaviors, Anti-Patterns, Canonical Rules
- [ ] Sub-Agent Discipline block is present with all three subsections (Checkpoint, Error Recovery, Final Response Rule)
- [ ] No placeholder text left (`[fill in]`, `TODO`, `{{template}}`)
- [ ] Symlinks resolve correctly (if created)
- [ ] AGENTS.md is under 200 lines
- [ ] SOUL.md is under 80 lines

### Step 7: Register in Config

Add the agent to `openclaw.json` `agents.list`:

```json
{
  "id": "<id>",
  "name": "<Display Name>",
  "workspace": "/Users/kosta/.openclaw/workspace-profiles/<id>",
  "model": "<model or omit for default>"
}
```

**Config fields reference:**

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique identifier. Lowercase, no spaces. Used for spawning and bindings. |
| `workspace` | Yes | Absolute path to profile directory. |
| `name` | No | Display name for logs and status. |
| `model` | No | Override default model. Inherits from `agents.defaults.model` if omitted. |
| `agentDir` | No | Override session data location. Usually leave unset. |
| `heartbeat` | No | Heartbeat config. Omit if agent doesn't need heartbeats. |
| `sandbox` | No | Sandbox mode override. |

**Registration method:** Use `gateway config.patch` with the `agents.list` entry.

**Critical warning:** `config.patch` on `agents.list` is an array — it can **replace** instead of **append**. Always:
1. Use `config.get` first to read the current `agents.list`
2. Append the new entry to the existing array
3. Use `config.apply` with the full updated array

### Step 8: Commit

```bash
cd ~/.openclaw && git add workspace-profiles/<id>/ && git commit -m "feat: add <id> agent profile" && git push
```

### Step 9: Verify

Spawn a test sub-agent:

```
sessions_spawn(agentId="<id>", task="Introduce yourself. Describe your role, how you communicate, and what you're designed to do. Keep it to 3-5 sentences.")
```

Confirm:
- Sub-agent responds (no "(no output)")
- Response matches the intended personality and role
- No errors in spawn or execution

Report the result to the user.

---

## File Hierarchy & Conflict Resolution

When files exist in multiple places, precedence order:

1. **AGENTS.md** — highest authority for operational rules
2. **SAFETY.md** — highest authority for safety/refusal rules (if present)
3. **SOUL.md** — personality/voice (yields to AGENTS.md on operational conflicts)
4. **MEMORY.md** — learned knowledge (yields to all above)
5. **USER.md** — user context (informational, no authority)

---

## Symlink Rules

- **Symlink** files that should stay in sync with main workspace (USER.md, shared skills)
- **Copy** files that should diverge (AGENTS.md, SOUL.md, MEMORY.md)
- **Never symlink** AGENTS.md or SOUL.md — these define the agent's unique behavior

---

## Common Mistakes

| Mistake | Why it's bad | Fix |
|---------|-------------|-----|
| Forgetting Sub-Agent Discipline block | Agent runs away with tool calls or ends on a tool call and returns "(no output)" | Always include the block — it's mandatory |
| Symlinking AGENTS.md or SOUL.md | These define uniqueness — symlinked = identical to another agent | Always create unique copies |
| Generic SOUL.md ("helpful and professional") | Describes every agent — adds no value | Be specific about voice and behaviors |
| Not testing after registration | Config errors are silent until you try to use the agent | Always spawn a test |
| Array clobbering in config.patch | `agents.list` gets replaced instead of appended | Read existing list first, then apply full updated array |
| Creating profiles for one-off tasks | Overkill — just put instructions in the `task` prompt | Only create profiles for reusable roles |
| Scattering safety rules | Rules in AGENTS.md AND SOUL.md AND inline = confusion | Consolidate in SAFETY.md if needed, otherwise Scope & Safety in AGENTS.md |
| Overstuffing AGENTS.md | 300+ lines = agent ignores half of it | Keep under 200 lines, link out for domain docs |

---

## Quick Reference

| Action | Command/Path |
|--------|-------------|
| Profile directory | `~/.openclaw/workspace-profiles/<id>/` |
| Register agent | `gateway config.patch` → `agents.list` |
| Test agent | `sessions_spawn(agentId="<id>", task="Introduce yourself...")` |
| Remove agent | Remove from `agents.list`, restart gateway, delete directory |
| Commit | `cd ~/.openclaw && git add workspace-profiles/<id>/ && git commit -m "feat: add <id> agent profile" && git push` |
