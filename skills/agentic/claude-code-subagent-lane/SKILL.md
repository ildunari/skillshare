---
name: claude-code
description: Use when an agent should launch Claude Code as a planning, review, UI/UX, architecture, implementation, or specialized Claude Code lane. Covers one-shot `claude -p`, long-running/background jobs, interactive back-and-forth Claude Code sessions, `--agent`, `--worktree --tmux`, and ACP adapter choices.
targets: [codex, droid, gemini, cursor, antigravity, copilot, kiro, "Forge Agent", "Craft-MyWorkspace", "Craft-Brown", hermes-default, hermes-gpt, xcode-codex]
---

# Claude Code Subagent Lane

Use this when the current agent wants Claude Code to act as a separate worker/lane.

## Position

Claude Code should usually be launched as a normal CLI subprocess with `claude -p`, not through Hermes `delegate_task(acp_command="claude")`.

Current observed state on this machine: Claude Code 2.1.123 does **not** document raw `claude --acp --stdio` in `claude --help`. Do not copy older or guessed ACP examples that treat the raw `claude` binary as an ACP server.

## Permission mode default

Prefer Claude Code's `auto` permission mode for delegated Claude Code lanes:

```bash
claude --print --input-format text --output-format json \
  --permission-mode auto \
  < /tmp/claude-task.md
```

Use `auto` because it lets Claude Code run without repeated permission prompts while still routing risky actions through Claude Code's classifier. It is less disruptive than `plan`/`default` and safer than `bypassPermissions`.

Important caveats:

- `auto` requires Claude Code v2.1.83+, an eligible plan/account, a supported Claude model, and Anthropic API routing. If Claude reports that auto mode is unavailable, relaunch with `--permission-mode acceptEdits` for implementation work or `--permission-mode plan` for read-only planning/review.
- For non-interactive `claude --print` runs, repeated auto-mode blocks can abort the run because there is no user prompt to fall back to. If that happens, rerun with narrower context, clearer trusted-boundary instructions, or `acceptEdits`.
- Do not use `bypassPermissions` / `--dangerously-skip-permissions` unless Kosta explicitly asks for a YOLO lane in an isolated environment.
- To make auto persistent for normal Claude Code launches, set `permissions.defaultMode = "auto"` in Claude Code settings. Do not use VS Code's `claudeCode.initialPermissionMode` for this; it does not accept `auto`.

## Choose the right lane

Use these defaults:

- **One-shot read-only plan/review**: foreground `claude -p --permission-mode auto --output-format json` by default so inspection commands are not denied; use `plan` only when edits must be impossible.
- **One-shot implementation with bounded scope**: foreground `claude -p --permission-mode auto`; fall back to `acceptEdits` if auto is unavailable. Independently verify diffs/tests.
- **Long-running implementation or test loop**: run Claude Code through the host's background process mechanism when available, then poll logs and verify output yourself before reporting success.
- **Interactive back-and-forth**: run Claude Code in PTY mode or use Claude Code's native `--worktree --tmux` when the user wants to steer it manually across multiple turns.
- **Configured specialist**: add `--agent <name>`.
- **ACP subagent lane**: use the host's native delegation tool for isolated workers, not raw Claude Code ACP unless using a real ACP adapter.

## Preferred one-shot pattern

Run from the repo/workdir that should provide project context. For anything longer than a sentence or two, write the prompt to a file and redirect stdin. This avoids shell quoting/argument parsing mistakes where Claude sees only `json` or receives no prompt.

```bash
cat > /tmp/claude-task.md <<'PROMPT'
<task prompt>
PROMPT

claude --print --input-format text --output-format json \
  --permission-mode auto \
  --append-system-prompt-file .hermes/prompts/claude-planning.md \
  < /tmp/claude-task.md
```

Use `--agent <name>` for a configured Claude Code agent:

```bash
cat > /tmp/claude-task.md <<'PROMPT'
<task prompt>
PROMPT

claude --print --input-format text --output-format json \
  --agent design-agent-claude \
  < /tmp/claude-task.md
```

Short one-liners can still use a positional prompt, but avoid `"$(cat prompt.md)"` for real tasks.

Use `--agents '<json>'` for ephemeral session-local agents when a file-backed agent is overkill.

## Background pattern

Use the host's background process tracking when Claude Code may take minutes, run tests, or iterate on a non-trivial repo change:

```bash
cat > /tmp/claude-task.md <<'PROMPT'
<implementation task>
PROMPT

claude --print --input-format text --output-format json \
  --permission-mode auto \
  --append-system-prompt "Return files changed, checks run, blockers, and exact verification commands." \
  < /tmp/claude-task.md
```

Start it with the host's managed background task API when one exists, not shell `&`, `nohup`, or `disown`. Use the host's polling/log APIs to inspect progress. If an early background notification says `no stdin data received` or asks what to do with `JSON`, that run did not receive the intended prompt; ignore that failed run, relaunch with the stdin pattern above, and verify the successful run's output separately. When it finishes, verify diffs and tests independently before telling Kosta it succeeded.

## Interactive / back-and-forth pattern

Use interactive Claude Code only when Kosta wants to steer the lane live or when the task benefits from a persistent Claude Code session:

```bash
claude --permission-mode auto
```

Run it with a PTY when launching from terminal tooling. For isolated repo work where Claude Code should create/manage its own branch workspace, prefer Claude Code's native support:

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

- Default to `--permission-mode auto` for Claude Code lanes so read/explore commands, edits, and tests can proceed without repeated permission prompts.
- Use `--permission-mode plan` only when the lane must be unable to edit.
- Use `--permission-mode acceptEdits` when auto is unavailable but edits should still be allowed.
- Use `--tools` to restrict what Claude can use.
- Use `--allowedTools` to auto-approve specific tools; it is not the same as restricting available tools.
- Avoid broad `--dangerously-skip-permissions` / bypass mode unless Kosta explicitly wants a YOLO implementation lane.

## ACP bridge, only when needed

If the host truly needs ACP transport, use an actual ACP adapter, not raw Claude Code. The current package is:

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

Test the adapter in the current environment before relying on it for real work. For most orchestration, direct `claude -p` is simpler, more debuggable, and closer to Claude Code's documented headless/programmatic mode.

## Freshness check

Before changing scripts or instructions around Claude Code flags, run:

```bash
claude --version
claude --help | grep -E -- '--agent|--agents|--print|--permission-mode|--tools|--allowedTools|--append-system-prompt|--add-dir|--bare|--worktree|--tmux'
claude --print --permission-mode auto --input-format text --output-format json <<< 'Say ok'
claude --acp --stdio
```

The last command should be treated as a negative check: if it still says `unknown option '--acp'`, do not use raw-Claude ACP examples.

## After updating Hermes instructions or tool schemas

If you correct a Hermes skill, prompt file, or `delegate_task` schema, remember that the current Telegram/gateway session may still show the old tool description until the gateway or session reloads. Verify the files and synced skills on disk, then restart/reload the relevant gateway/session before treating the new guidance as active in live tool schemas.
