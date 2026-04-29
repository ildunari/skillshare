---
name: claude-code-subagent-lane
description: Use when Hermes should launch Claude Code as a planning, review, UI/UX, architecture, implementation, or specialized Claude Code agent lane. Covers one-shot `claude -p`, long-running/background `terminal(background=true)` jobs, interactive back-and-forth Claude Code sessions, `--agent`, `--worktree --tmux`, Hermes `delegate_task`, and ACP adapter choices.
targets: [hermes-default, hermes-gpt]
---

# Claude Code Subagent Lane for Hermes

Use this when Hermes wants Claude Code to act as a separate worker/lane.

## Position

Claude Code should usually be launched as a normal CLI subprocess with `claude -p`, not through Hermes `delegate_task(acp_command="claude")`.

Current observed state on this machine: Claude Code 2.1.122 does **not** document raw `claude --acp --stdio` in `claude --help`. Do not copy older or guessed ACP examples that treat the raw `claude` binary as an ACP server.

## Choose the right lane

Use these defaults:

- **One-shot read-only plan/review**: foreground `claude -p --permission-mode plan --output-format json`.
- **One-shot implementation with bounded scope**: foreground `claude -p --permission-mode acceptEdits` or `dontAsk`, then independently verify diffs/tests.
- **Long-running implementation or test loop**: run Claude Code through `terminal(background=true, notify_on_complete=true)`, then poll logs and verify output yourself before reporting success.
- **Interactive back-and-forth**: run Claude Code in PTY mode or use Claude Code's native `--worktree --tmux` when the user wants to steer it manually across multiple turns.
- **Configured specialist**: add `--agent <name>`.
- **Hermes subagent**: use `delegate_task` for isolated Hermes workers, not for raw Claude Code unless using a real ACP adapter.

## Preferred one-shot pattern

Run from the repo/workdir that should provide project context:

```bash
claude -p --output-format json \
  --permission-mode plan \
  --append-system-prompt-file .hermes/prompts/claude-planning.md \
  "<task prompt>"
```

Use `--agent <name>` for a configured Claude Code agent:

```bash
claude -p --agent design-agent-claude --output-format json "<task prompt>"
```

Use `--agents '<json>'` for ephemeral session-local agents when a file-backed agent is overkill.

## Background pattern

Use Hermes' background process tracking when Claude Code may take minutes, run tests, or iterate on a non-trivial repo change:

```bash
claude -p --output-format json \
  --permission-mode acceptEdits \
  --append-system-prompt "Return files changed, checks run, blockers, and exact verification commands." \
  "<implementation task>"
```

Start it with `terminal(background=true, notify_on_complete=true)`, not shell `&`, `nohup`, or `disown`. Use `process.poll`, `process.log`, or `process.wait` to inspect progress. When it finishes, verify diffs and tests independently before telling Kosta it succeeded.

## Interactive / back-and-forth pattern

Use interactive Claude Code only when Kosta wants to steer the lane live or when the task benefits from a persistent Claude Code session:

```bash
claude --permission-mode default
```

Run it with a PTY when launching from Hermes terminal tooling. For isolated repo work where Claude Code should create/manage its own branch workspace, prefer Claude Code's native support:

```bash
claude --worktree <name> --tmux
```

Use this mode sparingly from Telegram because interactive sessions need active polling/stdin handling. If Kosta is not present to steer, use print/background mode instead.

## Prompting rules

- Pass all task context explicitly; Claude Code does not know the Hermes parent chat unless you include it.
- Prefer prompt text via stdin or a prompt file when it is long.
- Use `--append-system-prompt` or `--append-system-prompt-file` to preserve Claude Code's default behavior while adding lane-specific instructions.
- Use `--system-prompt` only when intentionally replacing Claude Code's default system prompt.
- For `--add-dir`, put the prompt before variadic flags or use stdin/prompt files to avoid argument parsing mistakes.
- Directories added with `--add-dir` grant file access but do not normally load their `.claude/` agents or memory as project config.

## Permissions and tools

- For read-only planning/review, default to `--permission-mode plan`.
- Use `--tools` to restrict what Claude can use.
- Use `--allowedTools` to auto-approve specific tools; it is not the same as restricting available tools.
- Avoid broad `--dangerously-skip-permissions` / bypass mode unless Kosta explicitly wants a YOLO implementation lane.

## ACP bridge, only when needed

If Hermes truly needs ACP transport, use an actual ACP adapter, not raw Claude Code. The current package is:

```bash
npx -y @agentclientprotocol/claude-agent-acp
```

Hermes ACP override shape:

```python
delegate_task(
    goal="...",
    context="...",
    acp_command="npx",
    acp_args=["-y", "@agentclientprotocol/claude-agent-acp"],
)
```

Test the adapter in the current environment before relying on it for real work. For most Hermes orchestration, direct `claude -p` is simpler, more debuggable, and closer to Claude Code's documented headless/programmatic mode.

## Freshness check

Before changing scripts or instructions around Claude Code flags, run:

```bash
claude --version
claude --help | grep -E -- '--agent|--agents|--print|--permission-mode|--tools|--allowedTools|--append-system-prompt|--add-dir|--bare|--worktree|--tmux'
claude --acp --stdio
```

The last command should be treated as a negative check: if it still says `unknown option '--acp'`, do not use raw-Claude ACP examples.

## After updating Hermes instructions or tool schemas

If you correct a Hermes skill, prompt file, or `delegate_task` schema, remember that the current Telegram/gateway session may still show the old tool description until the gateway or session reloads. Verify the files and synced skills on disk, then restart/reload the relevant gateway/session before treating the new guidance as active in live tool schemas.
