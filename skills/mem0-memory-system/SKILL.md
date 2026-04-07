---
name: mem0-memory-system
description: Self-hosted Mem0 memory system shared across all of Kosta's machines and AI agents. Use to read/write durable facts about the user, code, environment, and workflows. Supports semantic search, metadata filtering, graph entity relationships, and a strict 5-field schema. Loaded by Hermes, Claude Code, Codex, Factory, Forge, and Craft Agent.
version: 1.0.0
author: Kosta
license: MIT
metadata:
  tags: [memory, mem0, persistence, multi-agent, knowledge-base]
  related_skills: []
---

# Mem0 Memory System

A shared, self-hosted memory layer for all of Kosta's AI agents.

## What it is

A central long-term memory store that any AI tool can read from and write to. Self-hosted on the Mac Studio, accessible from any machine over Tailscale. Backed by:

- **pgvector** for semantic search (768-dim Gemini embeddings)
- **Neo4j** for entity relationship graph
- **Claude Haiku** (via VibeProxy) for fact extraction and deduplication
- **REST API** at `http://100.69.228.58:8888` (Tailscale) or `http://localhost:8888` (Studio)
- **OpenAPI docs** at `/docs`

Every memory is automatically deduplicated, semantically indexed, and tagged with structured metadata so different agents can query relevant subsets.

## When to use it

Use the memory system when you need to:

- Recall facts about Kosta's preferences, machines, projects, or workflows from previous sessions
- Store new durable facts learned during the current session
- Look up environment details (paths, ports, machine roles, services)
- Find context about a project or codebase across sessions
- Avoid asking Kosta the same question twice

Do NOT use it for:

- Transient session state (pass via prompt or scratchpad instead)
- Per-session task progress (use TODO lists)
- Temporary debugging values
- Anything sensitive that should not survive the session unless explicitly marked sensitive

## The 5-field metadata schema

Every memory write should include structured metadata. The schema is intentionally minimal — five fields, strict enums where possible, optional except where noted.

REQUIRED on every write:
- `user_id` — always `kosta`

STRONGLY RECOMMENDED:
- `category` — one of: `coding`, `environment`, `preferences`, `personal`, `workflow`
- `source` — which agent stored it: `hermes`, `claude-code`, `craft-agent`, `codex`, `factory`, `forge`, `manual`, `document`, `builtin_memory`

OPTIONAL — only when relevant:
- `machine` — `mac-studio`, `macbook-pro`, or `mac-mini`. Set ONLY when the fact is host-specific (not for universal facts).
- `expires_at` — ISO 8601 date string. Set ONLY for temporary facts that should auto-expire (e.g., "currently debugging issue X").
- `sensitive` — boolean `true`. Set ONLY for private info (health, credentials, personal relationships). Sensitive memories are excluded from default searches.

### Category guide — when to use which

`coding` — programming languages, frameworks, code patterns, libraries, build tools, dev workflow, project-specific code conventions
- "Prefers TypeScript over JavaScript"
- "Project Foo uses Next.js 15 with App Router"
- "Uses pnpm not npm"

`environment` — machines, infrastructure, services, ports, databases, deployment, OS/system config
- "Mac Studio runs Docker via Colima with 4GB RAM"
- "Mem0 API at port 8888 on 100.69.228.58"
- "Neo4j auth password stored in ~/.hermes/mem0/.neo4j_pass"

`preferences` — communication style, formatting choices, response style, UI/UX preferences
- "Dislikes emoji in outputs"
- "Prefers shorter responses to make scrolling easier"
- "Uses macOS-native terminology — Return not Enter"

`personal` — identity, life facts, health, relationships, location, schedule
- "Lives in Providence RI weekdays, Westford MA weekends"
- "Allergic to peanuts" (set `sensitive: true`)
- "Timezone is America/New_York"

`workflow` — task processes, methodologies, agent behavior rules, multi-step procedures
- "Always plan before non-trivial coding work"
- "Spawn review subagent after major implementations"
- "Verify end-to-end through user-facing path, not just logs"

When unsure, default to `workflow`.

## How to write memories

### Via Hermes (mem0_conclude tool)

```
mem0_conclude(
    conclusion="Mac Studio runs Docker via Colima for the Mem0 stack",
    category="environment",
    machine="mac-studio"
)
```

The `category` parameter is REQUIRED. The plugin auto-fills `source=hermes` and uses the local machine ID by default.

### Via REST API (any agent)

```
curl -X POST http://100.69.228.58:8888/memories \
  -H 'Content-Type: application/json' \
  -d '{
    "messages": [{"role": "user", "content": "User prefers vim over emacs"}],
    "user_id": "kosta",
    "agent_id": "claude-code",
    "metadata": {
      "category": "preferences",
      "source": "claude-code"
    }
  }'
```

The `messages` array goes through the extraction LLM (Claude Haiku) which dedupes against existing memories and stores only new facts. The REST API requires the `messages` field — posting raw text is not supported. If you want to store a single verbatim fact, phrase it as a single user message in the array.

### Updating metadata only (no re-embedding)

```
curl -X PATCH http://100.69.228.58:8888/memories/{memory_id}/metadata \
  -H 'Content-Type: application/json' \
  -d '{"category": "coding", "machine": "mac-studio"}'
```

This is faster than a full update because it skips re-embedding the text.

## How to search memories

### Basic semantic search

Via Hermes: `mem0_search(query="git workflow")`

Via REST:
```
curl -X POST http://100.69.228.58:8888/search \
  -H 'Content-Type: application/json' \
  -d '{"query": "git workflow", "user_id": "kosta"}'
```

### Filtered search by category

Via Hermes: `mem0_search(query="dependencies", category="coding")`

Via REST:
```
{
  "query": "dependencies",
  "user_id": "kosta",
  "filters": {"category": "coding"}
}
```

### Filtered by category AND machine

```
{
  "query": "Docker setup",
  "user_id": "kosta",
  "filters": {
    "AND": [
      {"category": "environment"},
      {"machine": "mac-studio"}
    ]
  }
}
```

### Filter operators (Mem0 OSS v1.0+)

- `eq`, `ne` — equals / not equals
- `gt`, `gte`, `lt`, `lte` — comparison
- `in`, `nin` — in list / not in list
- `contains`, `icontains` — substring match
- `AND`, `OR`, `NOT` — logical, can be nested

Example with logical ops:
```
{
  "filters": {
    "AND": [
      {"category": {"in": ["coding", "environment"]}},
      {"NOT": [{"sensitive": true}]}
    ]
  }
}
```

### Recall recent memories

Via Hermes: `mem0_recall_recent(hours_ago=24)` or `mem0_recall_recent(hours_ago=24, category="coding")`

Useful for "what did we work on yesterday" queries. Uses the auto-generated `created_at` timestamps.

## Connecting non-Hermes agents

The Mem0 REST API speaks standard HTTP — any agent or tool can integrate.

### Quick connection check

```
curl http://100.69.228.58:8888/docs
```

If reachable, the OpenAPI swagger UI loads.

### Per-agent setup

When this skill is loaded by Claude Code, Codex, Factory, Forge, or Craft Agent:

1. Set the appropriate `source` field on writes (`claude-code`, `codex`, `factory`, `forge`, `craft-agent`)
2. Use the same `user_id: "kosta"` across all agents
3. Optionally set `agent_id` to track which tool stored a memory (defaults to your source name)
4. Always provide a `category` on writes
5. Search broadly first, then filter by category if results are noisy

### MCP integration (optional)

For tools that prefer MCP, use one of:
- `mem0-custom-mcp` (TypeScript wrapper around the REST API) — set `MEM0_API_URL=http://100.69.228.58:8888`
- Write a thin MCP wrapper that translates tool calls into HTTP requests

## REST API endpoints reference

All endpoints accept JSON over HTTP. Base URL: `http://100.69.228.58:8888`

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/memories` | Add memories (uses extraction LLM) |
| GET | `/memories?user_id=kosta` | List all memories for a user |
| GET | `/memories/{id}` | Get a single memory by ID |
| POST | `/search` | Semantic search with optional filters |
| PUT | `/memories/{id}` | Update memory text (re-embeds) |
| PATCH | `/memories/{id}/metadata` | Update metadata only (no re-embed) |
| GET | `/memories/{id}/history` | Audit log for a memory |
| DELETE | `/memories/{id}` | Delete a single memory |
| DELETE | `/memories?user_id=X` | Delete all memories for a user |
| POST | `/configure` | Replace runtime config |
| POST | `/reset` | Wipe everything (dangerous) |

OpenAPI spec at `/docs`.

## Anti-patterns

DO NOT:

- Skip the `category` field — it makes filtered search impossible
- Use free-text categories like `"programming"` or `"coding stuff"` — stick to the 5 enums (the Hermes plugin will coerce common variants but other agents won't)
- Store secrets, passwords, or credentials. If you must store something private, set `sensitive: true`
- Store transient session state ("currently looking at file X") — use TODO lists or scratch memory instead
- Re-add the same fact every session — Mem0's extraction LLM handles deduplication, but only when using POST `/memories` with the messages array
- Bypass the extraction LLM for organic facts (use `messages` array, not `text` string) — extraction handles dedup and entity linking
- Set `machine` for universal facts — only set it when the fact is genuinely host-specific
- Use `expires_at` as a substitute for proper memory hygiene — most facts should NOT expire

## Memory hygiene

- Mem0 auto-dedupes via the extraction LLM. Don't over-engineer.
- `expires_at` is enforced at read time — expired memories are filtered out of search, profile, and recall_recent. Use ISO 8601 format (e.g. `"2026-12-31T00:00:00Z"`). Invalid formats are dropped at write time with a warning.
- Use `sensitive: true` for health, credentials, personal relationships. Sensitive memories are excluded from default searches unless `include_sensitive: true` is passed.
- Mem0 auto-adds `created_at` and `updated_at` — don't add manual timestamps
- For event dates ("visited Japan in 2023"), bake the date into the fact text instead of using a separate field
- Periodically audit via `GET /memories?user_id=kosta` and review for staleness

## Troubleshooting

### "Connection refused" or "name not resolved"

The Studio may be offline or Tailscale isn't connected. Check:
```
ping 100.69.228.58
curl -I http://100.69.228.58:8888/docs
```

If unreachable from a remote machine, the issue is Tailscale or the Studio is asleep. From the Studio itself, try `localhost:8888`.

### "Filtered search returns 0 results"

The metadata filter syntax is strict. Common mistakes:
- Used `"category": "code"` instead of `"category": "coding"` (wrong enum value)
- Filter spelling typo
- The memory you expected genuinely doesn't have that category — check with unfiltered search first
- The `sensitive` filter excludes results by default; pass `include_sensitive: true` to override

### "Fact extraction returned 0 facts"

Mem0's extraction LLM determined the input had no novel facts. This is usually correct (deduplication working). If you need to force-store, use the `text` field instead of `messages`.

### "Got 500 Internal Server Error on PUT"

mem0 OSS has a known bug where `Memory.update()` re-embeds and chokes on dict input. Use `PATCH /memories/{id}/metadata` for metadata-only updates instead.

### Service status check

From the Mac Studio directly:
```
docker ps --format 'table {{.Names}}\t{{.Status}}' | grep mem0
```

Should show three healthy containers: `mem0-postgres`, `mem0-neo4j`, `mem0-api`.

From any other machine, hit the health endpoint over Tailscale:
```
curl -I http://100.69.228.58:8888/docs
```

A 200 or 307 response means the API is up. Anything else means Tailscale is down, the Studio is asleep, or the stack crashed.

## Architecture summary

```
[Any AI Agent] --HTTP--> http://100.69.228.58:8888 (Mem0 REST API)
                                |
                                +--> pgvector  (semantic search, 768-dim Gemini embeddings)
                                +--> Neo4j     (entity relationship graph)
                                +--> VibeProxy (LLM extraction via Claude Haiku)
```

All three backing services run as Docker containers on Mac Studio (Colima-managed). The Hermes plugin uses the same backing store directly via the mem0 Python library; other agents go through the REST API.

The system survives reboots (containers set to `restart: unless-stopped`) and Colima auto-starts via `brew services`.
