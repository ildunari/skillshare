# Feedback Log — subagent-orchestrator

Read this file before every skill use.

## Entries

- [2026-03-06] [craft-agent] In Craft Agent, do not assume a generic Task/subagent tool is exposed. Map subagent patterns to actual available tools: `spawn_session` for true independent workers, `call_llm` for isolated model-only analysis, or inline execution for simple work.
- [2026-03-06] [craft-agent] Never claim a model performed subagent work unless the actual tool result explicitly confirms the connection/model used.
