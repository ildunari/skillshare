---
name: hermes-mem0-presence-check
description: Diagnose where mem0 is actually wired in on this machine when it seems to be missing from tool listings. Use when Hermes or Claude appears to have "lost" mem0, when `hermes tools` does not show mem0, or when there is confusion between Hermes memory-provider plugins and standalone MCP servers.
alwaysAllow:
  - Bash
targets: [hermes-default, hermes-gpt]
---

# Hermes mem0 presence check

Use this when the user says mem0 used to work, but it is not being listed now.

## What this usually means

There are often two separate things named "mem0":

1. A Hermes memory-provider plugin, commonly `mem0_oss`
2. A standalone MCP server repo, such as `mem0-custom-mcp`, used by Claude or other MCP clients

These are not the same integration path.

## Fast checklist

Start with the direct explanation before going deep: if the user's main question is "why isn't mem0 listed in tools?", the most likely answer is that mem0 is configured as a memory-provider plugin, not a normal toolset entry. Verify that first before detouring into cron or MCP troubleshooting.

1. Check Hermes memory config:
   ```bash
   rtk python3 - <<'PY'
   import yaml, pathlib
   p = pathlib.Path.home()/'.hermes'/'config.yaml'
   cfg = yaml.safe_load(p.read_text())
   print(cfg.get('memory', {}))
   PY
   ```
   Key field: `memory.provider`

2. Confirm the Hermes plugin exists:
   - Look under `~/.hermes/plugins/memory/`
   - Typical path for this machine: `~/.hermes/plugins/memory/mem0_oss/`
   - Config usually lives at `~/.hermes/mem0-oss.json`

3. Check whether `hermes tools` shows it:
   ```bash
   rtk hermes tools list --platform cli
   ```
   Important: `hermes tools` lists normal toolsets, not memory-provider plugins. So mem0 may be active even if it is absent from this list.

4. Check whether the old `mem0` skill is actually present in the live skill registry.
   - Run `skills_list` or inspect active skill dirs if needed.
   - Do **not** assume the historical `mem0` skill still exists just because older sessions or memories mention it.
   - A common failure mode now is:
     - Hermes memory provider `mem0_oss` still exists and loads
     - but `skill_view(name="mem0")` fails because the skill is no longer installed / exposed
   - That breaks prompts or cron jobs that still instruct the agent to load the `mem0` skill first.

5. Explain the distinction clearly:
   - Built-in/toolset tools show in `hermes tools`
   - Memory providers are injected separately by runtime startup
   - So a configured memory provider can expose tools during a live session without appearing as a configurable toolset row

5. Verify prior live sessions if needed:
   - Search `~/.hermes/sessions/*.json` for `mem0_profile`, `mem0_search`, `mem0_conclude`, `mem0_add_document`, `mem0_recall_recent`
   - If found, that proves Hermes previously injected mem0 tools into the live tool surface

6. If the user mentions a separate repo like `mem0-custom-mcp`, inspect it independently:
   - Check repo path
   - Read `README.md`, `package.json`, and entrypoint (`src/index.ts` or `dist/index.js`)
   - Determine whether it is a standalone MCP server for Claude-style clients rather than Hermes runtime memory

7. Check whether Claude actually has the MCP server registered:
   - Inspect `~/.claude.json`
   - Inspect `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Search for the MCP server name, repo path, `MEM0_API_URL`, and `DEFAULT_USER_ID`

## What to tell the user

Lead with the answer:
- mem0 may still be present
- Hermes may be using it as a memory provider plugin, not as a normal toolset
- therefore `hermes tools` not listing it is expected
- a separate `mem0-custom-mcp` repo is a different path and may or may not be registered in Claude

## Extra checks when mem0 used to be primary but vanished from one surface

1. Compare root Hermes config with the active profile config.
   - Check both `~/.hermes/config.yaml` and `~/.hermes/profiles/<profile>/config.yaml`
   - If root has `memory.provider: mem0_oss` but the active profile does not, the profile will not load the mem0 provider even though Hermes overall still has mem0 configured
   - This is especially important after profile-isolation / profile-cutover changes

2. Check whether the active profile is running under its own `HERMES_HOME` and therefore cannot see the root mem0 assets.
   - A profile-scoped gateway / cron process may be using only `~/.hermes/profiles/<profile>` at runtime
   - In that case, root-level mem0 files can exist and still be invisible to that profile session
   - On this machine, the critical assets to compare are typically:
     - `~/.hermes/plugins/memory/mem0_oss/`
     - `~/.hermes/mem0-oss.json`
     - `~/.hermes/.env` vs `~/.hermes/profiles/<profile>/.env`
   - If the profile home lacks the plugin dir, config file, or required API keys, mem0 may silently disappear from that profile only

3. Confirm runtime prerequisites, not just config files.
   - Do not stop after finding `memory.provider: mem0_oss`
   - Check that the active runtime environment can actually import the mem0 stack and its embedding / DB dependencies
   - Typical failures include missing packages such as:
     - `mem0ai`
     - `google-genai`
     - `psycopg[binary]`
     - `psycopg[pool]`
     - `langchain-neo4j`
     - `rank-bm25`
     - `croniter` for cron-path execution if the failure only appears there
   - If config is present but imports fail, the tool surface may omit mem0 or cron may complete without actually writing memories

4. Confirm the runtime behavior in code when needed.
   - In `run_agent.py`, external memory providers are only activated when `memory.provider` is set in the active config
   - If that field is empty for the active profile, mem0 tools will not be injected into the live tool surface

5. Check cron separately if the user mentions nightly harvesting.
   - Inspect `~/.hermes/cron/jobs.json` and `~/.hermes/profiles/<profile>/cron/jobs.json` to see whether the mem0/nightly job is actually enabled and whether root/profile cron state has drifted.
   - Inspect `~/.hermes/hermes-agent/cron/scheduler.py` for `skip_memory=True`
   - `skip_memory=True` blocks both built-in memory and the mem0 provider loader, so a mem0-first cron prompt can still be non-functional at runtime
   - Do not trust cron `last_status: ok` by itself. Read the latest cron output markdown under `~/.hermes[/profiles/<profile>]/cron/output/<job_id>/...` and check whether the run explicitly says mem0 tools were unavailable or that 0 items were written.
   - Another common failure mode: the scheduler marks the job successful because the prompt completed, but the actual report admits `skill_view("mem0")` failed or `mem0_search` / `mem0_conclude` were not exposed, meaning the harvest was operationally a no-op.

## Repair moves when root Hermes has mem0 but a profile does not

If the diagnosis shows root Hermes is healthy but the active profile is isolated from mem0, the usual repair is to restore profile parity instead of changing the user-facing prompt.

1. Make the profile see the same mem0 plugin/config assets.
   - Ensure the profile home contains or points at:
     - `plugins/memory/mem0_oss`
     - `mem0-oss.json`
   - Symlinks are fine if the root assets are canonical on that machine

2. Mirror required secrets into the active profile runtime.
   - Compare root and profile `.env`
   - If embeddings / model keys such as `GOOGLE_API_KEY` exist only at root, the profile may load config but still fail at runtime

3. Re-run the failing surface itself.
   - Do not stop after making files line up
   - Re-run the profile-scoped gateway or cron path that was failing
   - A successful verification should show real mem0 activity, not just `last_status: ok`

4. If cron was the symptom, inspect the actual cron output report.
   - Confirm the run explicitly reports mem0 writes / recalls
   - Treat "prompt completed" without mem0 activity as a failed harvest, even if cron metadata says success

## Useful evidence to cite

- `~/.hermes/config.yaml` contains `memory.provider: mem0_oss`
- `~/.hermes/profiles/<profile>/config.yaml` may be missing `memory.provider`, which explains why that specific surface lost mem0
- `~/.hermes/plugins/memory/mem0_oss/` exists
- `~/.hermes/mem0-oss.json` exists and is populated
- prior Hermes session JSON files contain `mem0_*` tool schemas
- profile-specific session JSON files may lack `mem0_*` tools, confirming the active profile is not loading the provider
- `~/.hermes/cron/jobs.json` shows whether the nightly mem0 harvest job is enabled or disabled
- `cron/scheduler.py` may still contain `skip_memory=True`, which disables mem0 in cron runs
- Claude config files do or do not include the standalone MCP registration

## Backend/index location and shared-store checks

1. Make the storage location explicit.
   - The live Mem0 store/index is under `~/.hermes`, not `~/LocalDev`
   - Typical paths on this machine:
     - `~/.hermes/mem0/pgdata` — PostgreSQL / pgvector data
     - `~/.hermes/mem0/neo4j_data` — Neo4j graph data
     - `~/.hermes/mem0/history` — API-side history DB
     - `~/.hermes/mem0-oss.json` — Hermes plugin config
   - `~/LocalDev/mem0-custom-mcp` is just a repo / MCP wrapper, not the canonical vector index

2. Check whether another agent is sharing the same underlying Mem0 corpus.
   - For Hermes, inspect `~/.hermes/mem0-oss.json` for:
     - `user_id`
     - `agent_id`
     - `vector_store.collection_name`
     - host / port / dbname
   - For MCP wrappers, inspect their config or README for:
     - `MEM0_API_URL`
     - `DEFAULT_USER_ID`
   - Same backend requires the same Mem0 API / database
   - Same recalled memory corpus usually also requires the same `user_id`
   - Different `user_id` values can hit the same backend while still reading/writing different logical memory buckets

3. If the user asks whether LocalDev is involved, answer clearly.
   - LocalDev may contain code, wrappers, docs, and old synced profile layouts
   - The live Mem0 index/data is in local Hermes state under `~/.hermes`

## Pitfalls

- Do not assume `hermes tools` is the full truth for memory providers
- Do not assume root `~/.hermes/config.yaml` reflects what a profile-scoped surface is actually using
- Do not conflate Hermes memory plugins with MCP servers just because both expose mem0-like tools
- Do not claim the custom MCP server is active unless you actually found it in Claude config
- Session history proving old mem0 tools existed does not prove the active profile still loads mem0 today
- A mem0-first cron prompt does not prove cron can actually use mem0 if `skip_memory=True` is still set
