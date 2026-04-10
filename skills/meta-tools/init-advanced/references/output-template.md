# Output Template

Use this structure when delivering results.

## 1. Brief repo summary

State in a few bullets:
- what the project appears to be,
- important stack signals,
- important package or directory boundaries,
- any unresolved uncertainty.

## 2. File strategy

State whether you chose:
- fresh create,
- rewrite,
- layered update,
- audit + patch.

## 3. `AGENTS.md`

If writing the file, provide the full content or write it directly.
If auditing, summarize the key changes you would make.
Default behavior: present the draft first when user review is helpful; write directly when the user clearly asked for file creation/update and the environment permits it.

## 4. `CLAUDE.md`

If writing the file, provide the full content or write it directly.
If auditing, summarize the key changes you would make.

When a claim materially affects workflow, safety, or correctness, label it as `[verified]`, `[inferred]`, or `[assumed]` where useful.

## 5. Assumptions and follow-ups

List:
- anything the repo did not prove,
- anything the user should confirm,
- optional next improvements, such as package-level files or supporting docs.

## Quality bar

Before finishing, verify:
- both files use the same repo facts,
- both files use different model-appropriate wording,
- commands and paths are real,
- assumptions are clearly labeled,
- nothing important was invented.

When writing files directly, include a lightweight generated-date marker near the top, for example:
`<!-- Generated: YYYY-MM-DD by project-context-seeder -->`
