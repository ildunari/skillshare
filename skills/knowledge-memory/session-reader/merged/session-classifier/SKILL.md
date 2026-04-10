---
name: "Session Classifier"
description: "Use when classifying or labeling Craft Agent sessions, especially for requests like 'classify sessions', 'label sessions', 'tidy workspace', or 'session classifier'. Also use when running a daily or manual cleanup pass to organize previously unclassified sessions with consistent labels and statuses."
alwaysAllow: ["Bash", "Read", "Glob", "Grep", "Agent"]
---

# Session Classifier

> Review all sessions in the workspace, classify unorganized ones with appropriate labels and statuses, and keep the workspace tidy.

## Step 0 — Pre-flight Check

Before doing a full scan, count unclassified sessions with a single command:

```bash
python3 -c "
import json, os, glob
sessions_dir = os.path.expanduser('~/.craft-agent/workspaces/my-workspace/sessions')
count = 0
for d in glob.glob(os.path.join(sessions_dir, '*/session.jsonl')):
    try:
        with open(d) as f:
            meta = json.loads(f.readline())
        labels = meta.get('labels', [])
        status = meta.get('sessionStatus', '')
        real_labels = [l for l in labels if l not in ('Scheduled',)]
        if not real_labels or not status:
            count += 1
    except: pass
print(count)
"
```

**If count == 0:** Output "No unclassified sessions found. Skipping." and stop immediately.

**If count > 0:** Proceed to Step 1.

## Environment

- **Sessions directory:** `~/.craft-agent/workspaces/my-workspace/sessions/`
- **Session format:** Each session has a `session.jsonl` file. The first line is JSON metadata with fields: `name`, `sessionStatus`, `labels`, `preview`, `messageCount`, `model`, `lastMessageAt`.
- **Messages:** Subsequent lines have `type`: `user`, `assistant`, or `tool`. Only read `user` and `assistant` messages for classification.
- **Timezone:** America/New_York

## Available Statuses

| ID | Label | When to use |
|----|-------|-------------|
| `backlog` | Backlog | Ideas or plans discussed but not started |
| `todo` | Todo | Active work items that need completion |
| `needs-review` | Needs Review | Incomplete work or pending a decision |
| `done` | Done | Task completed successfully |
| `cancelled` | Cancelled | Abandoned, failed, or empty sessions |

## Available Labels

Use label **IDs** (not display names) when writing to session metadata.

### Development
- `code` — Code writing, refactoring, debugging
- `bug` — Bug investigation or fix
- `automation` — Automation scripts, pipelines, scheduled tasks
- `tools-other` — Tool configuration, setup, system admin

### Content
- `writing` — Document creation, editing, copywriting
- `research` — General research and exploration
- `design` — UI/UX design, visual work
- `planning` — Planning, architecture, strategy

### Craft Agents
- `agent-feedback` — Feedback about Craft Agent behavior
- `agent-research` — Researching AI agent capabilities, tools, frameworks
- `ideas` — Ideas for projects, features, or experiments
- `use-cases` — Exploring use cases for tools/features
- `tasks` — Task execution, chores, maintenance
- `dev-tools` — Developer tooling work

### Knowledge
- `docs` — Documentation reading/writing
- `how-to` — How-to guides, tutorials
- `openai` — OpenAI-related work
- `claude` — Claude/Anthropic-related work
- `gemini` — Google/Gemini-related work
- `craft-agents` — Craft Agent platform-specific work

### Other
- `reference` — Reference material, lookup
- `quick-chat` — Brief conversational exchanges
- `priority` — Priority flag (number value)
- `project` — Project tag (string value)

## Step 1 — Inventory

List all session directories. For each, read the first line of `session.jsonl` to get metadata. Build a list of sessions needing classification:

- Sessions with NO labels (empty `labels` array)
- Sessions with NO status (empty `sessionStatus`)
- Sessions with only the `Scheduled` label (auto-applied by automations, needs real labels)
- **Skip** this current session (it will have labels `automations` and `auto-labeler`)

Sessions that already have both a meaningful status AND at least one real label can be skipped.

## Step 2 — Classify (Sub-agents)

Dispatch sub-agents (model: **haiku**) in parallel batches of 3-4. Each sub-agent should:

1. Read the session metadata (first line of session.jsonl)
2. Read the last 10 user/assistant messages (skip `tool` type messages)
3. Return a JSON recommendation:
   ```json
   {"status": "done", "labels": ["code", "automation"], "reason": "One sentence."}
   ```

### Classification Heuristics

| Pattern | Status | Labels |
|---------|--------|--------|
| Quick config changes (permissions, labels, sources) | `done` | `craft-agents` or `tools-other` |
| Research/exploration sessions | `done` | `research` or `agent-research` |
| Ongoing development work | `todo` | `code` + relevant label |
| Automated runs (Obsidian, tool updater, etc.) | `done` | `automation` + `tasks` |
| Empty or 0-message sessions | `cancelled` | (none needed) |
| Question asked, no resolution | `needs-review` | topic label |
| Big ideas discussed, not implemented | `backlog` | `ideas` or `planning` |
| Bug fixes | `done` or `todo` | `bug` |
| Writing/documents | `done` or `todo` | `writing` |
| Brief Q&A or chat | `done` | `quick-chat` |

## Step 3 — Apply

For each classified session, update the first line of its `session.jsonl`:

```python
import json
path = '/path/to/session.jsonl'
with open(path) as f:
    lines = f.readlines()
meta = json.loads(lines[0])
meta['sessionStatus'] = 'done'
meta['labels'] = ['code', 'automation']
lines[0] = json.dumps(meta) + '\n'
with open(path, 'w') as f:
    f.writelines(lines)
```

**Batch this** — write a single Python script that applies all classifications in one pass, not one Bash call per session.

## Step 4 — Report

Output a summary:
- Total sessions scanned
- Sessions already classified (skipped)
- Sessions newly classified (with before/after labels and status)
- Any errors or sessions that couldn't be read

## Rules

1. **1-3 labels per session.** Only 4+ if genuinely multi-topic.
2. **Preserve existing good labels.** If a session already has meaningful labels, keep them — only add missing ones.
3. **Be conservative with status.** If unsure, use `needs-review` rather than guessing `done`.
4. **Skip your own session.** Don't classify the automation session you're running in.
5. **Don't modify message content.** Only update the metadata (first line) of session.jsonl files.
6. **Handle errors gracefully.** If a session.jsonl is corrupted or unreadable, skip it and note it in the report.
