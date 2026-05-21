# Provenance

## Origin

- Upstream repository: https://github.com/leonardsellem/codex-specialized-subagents
- Upstream file: `.codex/skills/delegation-autopilot/SKILL.md`
- Upstream commit: `b8073ebbdda350d61ab0ac07ec083920005e912d`
- Initial import date: `2026-02-13`

## Local evolution

This skill was migrated from MCP delegation semantics to native subagent orchestration semantics.

- Migration date: `2026-02-16`
- Migration scope:
  - replaced MCP `delegate_*` execution guidance with native `spawn_agent`/`send_input`/`wait`/`resume_agent`/`close_agent` orchestration
  - removed MCP server prerequisite/timeouts as required setup for this skill
  - replaced `run_dir`-centric reporting with `agent_id`-centric persistence and track ledger guidance
  - added explicit exception for sequential `subagent-driven-development` workflow
  - preserved `delegate_*` mentions only in migration mapping context

## Current intent

Use this skill as parent-agent orchestration guidance for native parallel subagent workflows in Codex interactive mode.
