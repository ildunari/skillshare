# Plugin Architecture Guide

Plugins are **packaging**, not behavior. The behavior lives in four mechanisms
with different strengths: skills carry reusable knowledge and workflows, agents
isolate work in separate context, hooks run deterministic automation on events,
and MCP gives Claude external tools and data. These layer rather than replace
one another.

Most bad plugin architecture comes from collapsing those roles. The structural
goal: **high trigger accuracy, low context waste, and a user-visible surface
that matches how humans think about the job**.

## Five Durable Heuristics

1. **Split by invocation semantics, not by step count.** A five-step workflow
   is usually one skill if the user thinks of it as one job.
2. **Keep knowledge in skills, noisy investigation in agents, deterministic
   automation in hooks, and external actions in MCP.**
3. **Make SKILL.md a router plus invariants; make references/ the deep corpus.**
4. **Default to abstract tool language; only name exact MCP tools where
   ambiguity is costly.**
5. **Warn against plugin sprawl, broad hooks, brittle MCP auth, and recursive
   command/skill indirection.**

---

## Decision Framework 1: One Skill or Many?

| Question | If yes | If no |
|---|---|---|
| Would a user ask for this subtask on its own? | Separate skill | Keep inside parent workflow |
| Do phases share the same working set of files/context? | Keep as one skill | Consider splitting |
| Does one phase have side effects while another is read-only? | Split the side-effectful phase | Keep together |
| Do phases need mostly different reference docs? | Split by reference boundary | Keep together |
| Do phases happen at different times (session start, audit, handoff)? | Split by cadence/lifecycle | Keep together |
| Is the only reason to split "there are five steps"? | Don't split | N/A |

**Bias toward fewer, sharper skills.** Large skill sets add repeated
description tokens every turn. Repeated skill loading can exhaust context
in long sessions. More skills means more chances for routing overlap.

### Real-world examples

**CLAUDE.md Management** — one maintenance skill with phased workflow, plus
one separate end-of-session command. Split by cadence and side effects, not
by internal steps.

**Memex** — eight skills (`init`, `session-start`, `session-end`, `idea`,
`update`, `archive`, `wikilinks`, `add-domain`). Split by lifecycle verbs,
not by implementation phase. Hooks wired only to session boundaries.

**Code Review** — one user-facing job, one entry point, multi-agent internals.
Internal complexity hidden behind one clear user intent.

---

## Decision Framework 2: Which Component Owns This Step?

| Step characteristic | Skill | Agent | Hook | MCP |
|---|---|---|---|---|
| Needs reusable domain knowledge | Best fit | Preload into agent | No | No |
| Needs iterative back-and-forth | Best fit | Poor fit | No | No |
| Produces lots of logs/search output | Sometimes | Best fit | No | No |
| Needs strict tool restrictions/isolation | Sometimes | Best fit | No | No |
| Must happen automatically on lifecycle event | No | No | Best fit | No |
| Requires external data/action | Guidance only | Guidance only | Maybe trigger | Best fit |
| Needs deterministic no-LLM automation | No | No | Best fit | Sometimes |

**Rule of thumb:**
- Skills encode **judgment** — how to think about the task.
- Agents consume judgment in **isolation** — noisy, parallelizable, or
  safety-isolated work.
- Hooks enforce **determinism** — things that should happen even if the
  model has no judgment call to make.
- MCP provides **capabilities** — external systems and data.

Don't use agents as a replacement for skills. If the knowledge should be
reusable across contexts, it belongs in a skill. If one phase just needs an
isolated worker, use an agent. Agents cannot spawn other agents, so avoid
deep delegation trees.

---

## Decision Framework 3: What Goes Where?

| Location | What belongs there | What does NOT belong there |
|---|---|---|
| Description / metadata | Trigger boundary, when to use, when not to use | Detailed workflow, examples |
| SKILL.md body | Core workflow, selection logic, reference index, escalation rules | Long API docs, giant examples, vendor catalogs |
| `references/` | Deep domain material, schemas, variant-specific guidance | Routing logic Claude needs every invocation |
| `scripts/` | Deterministic repeatable work | Human judgment or decision heuristics |
| MCP config | External capabilities and auth wiring | Workflow explanation |
| Hooks | Deterministic event automation | Things that need Claude's judgment |

When SKILL.md has 5+ reference file pointers, add a routing table:

```markdown
| File | Read when… |
|------|-----------|
| `references/triage.md` | Classifying or prioritizing |
| `references/comms.md` | Drafting communications |
| `references/rollback.md` | Reverting or undoing changes |
```

Organize references by **decision boundary**, not file type.

---

## Decision Framework 4: How Skills Reference MCP Tools

Three levels, use the least specific one that works:

1. **Default — describe the action abstractly:**
   "Look up the contract in the connected cloud storage system."

2. **If vendors are swappable — refer to a capability category:**
   "Use the connected project tracker to create a ticket."

3. **Only when exactness matters — name the specific tool:**
   "Use `mcp__github__create_inline_comment` to post inline PR comments."

Use abstract language in skill prose when multiple tools can satisfy the
intent. Use exact tool names in constrained workflows, commands, or
safety-critical sections where ambiguity causes failure.

For side-effectful skills (deploy, commit, send-message), consider
`disable-model-invocation: true` so the skill only runs when explicitly
invoked.

---

## Ten Anti-Patterns

### 1. Plugin sprawl
Large installed skill sets consume repeated context from descriptions every
turn. A plugin with lots of overlapping skills is not "modular" — it's
expensive.

### 2. Splitting by implementation phase
A workflow having five steps is not a reason to create five skills. Split by
cadence, side effects, or user intent instead.

### 3. Command-wrapping-skill recursion
Wrapping a skill in a command can recurse. Disabling model invocation to
stop recursion can also block the command path. Avoid clever indirection.

### 4. Hooks that fire too often
Broad `PostToolUse` or always-on hooks become accidental tax. Automate only
at meaningful lifecycle boundaries (session start/end, pre-commit).

### 5. Shell commands when native tools exist
Replace `find` with `Glob`, shell `cat` with `Read`. Unnecessary shell
commands cause permission prompts and friction.

### 6. Hardcoded paths and environment assumptions
Use `${CLAUDE_PLUGIN_ROOT}` for plugin files, `${CLAUDE_PLUGIN_DATA}` for
persistent state. Never hardcode `~/.claude/` — honor `CLAUDE_CONFIG_DIR`.

### 7. Underexplained MCP auth
If a plugin depends on tokens or OAuth, setup is part of architecture, not
documentation garnish. Missing setup guidance produces "not authenticated"
dead ends.

### 8. MCP servers that block startup
Heavyweight or environment-sensitive MCP configs can hang Claude Code on
startup. Treat these as structural risk.

### 9. Overautonomous background agents
Orphaned agents can continue modifying files after the user denies approval.
Never use background agents for risky side effects without approval gates.

### 10. Executable examples in skill bodies
Inline `!` command syntax inside fenced documentation examples can execute
during skill loading. Escape examples carefully.

---

## Two Architectural Patterns

### Pattern A: One Visible Job, Agents Underneath

Use when the workflow is operationally complex but conceptually one job.

```
incident-commander/
├── .claude-plugin/
│   └── plugin.json
├── .mcp.json
├── commands/
│   └── incident-review.md
├── skills/
│   └── incident-playbook/
│       ├── SKILL.md
│       └── references/
│           ├── triage.md
│           ├── comms.md
│           ├── rollback.md
│           └── postmortem.md
├── agents/
│   ├── log-sweeper.md
│   ├── blast-radius.md
│   └── patch-reviewer.md
└── README.md
```

One user-facing entry point. One shared skill holds doctrine and routes to
references. Agents exist only for noisy parallel subtasks. No hooks —
incident response needs judgment and timing control.

### Pattern B: Role Plugin, Multiple Standalone Skills

Use when the plugin supports a role with independently-invocable verbs.

```
customer-success-ops/
├── .claude-plugin/
│   └── plugin.json
├── .mcp.json
├── hooks/
│   └── hooks.json
├── skills/
│   ├── account-brief/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── account-health.md
│   │       └── qbr-template.md
│   ├── renewal-risk/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── churn-signals.md
│   │       └── escalation-policy.md
│   ├── draft-reply/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── tone-guide.md
│   ├── meeting-brief/
│   │   └── SKILL.md
│   └── session-close/
│       └── SKILL.md
└── README.md
```

Skills are separate because a user may independently ask for an account
brief, a renewal-risk assessment, a customer reply, or a meeting brief.
Each skill has its own narrow reference set. A low-frequency `SessionEnd`
hook prompts `session-close` to capture follow-ups.
