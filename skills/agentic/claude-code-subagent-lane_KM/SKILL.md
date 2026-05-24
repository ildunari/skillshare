---
description: Use when an agent should launch Claude Code as a planning, review, UI/UX, architecture, implementation, or specialized Claude Code lane. Covers one-shot `claude -p`, long-running/background jobs, interactive back-and-forth Claude Code sessions, `--agent`, `--worktree --tmux`, and ACP adapter choices.
metadata:
    targets:
        - antigravity
name: claude-code
---

# Claude Code Subagent Lane

Use this when the current agent wants Claude Code to act as a separate worker/lane.

## Position

For subscription-quota conservation after the June 15, 2026 Agent SDK credit split, prefer interactive Claude Code with `--prefill` when a human or PTY controller can submit the prefilled prompt. `claude -p` / `--print` is Agent SDK/headless mode and should be reserved for truly unattended scripts, CI, structured JSON capture, or cases where no interactive lane is possible.

Canonical prefilled launch:

```bash
cat > /tmp/claude-task.md <<'PROMPT'
<task prompt>
PROMPT

claude --permission-mode auto --prefill "$(cat /tmp/claude-task.md)"
```

Current observed state on Kosta's Macs: Claude Code 2.1.140+ accepts hidden `--prefill` even though it is not listed in `claude --help`; official docs warn that starting June 15, 2026 Agent SDK and `claude -p` usage on subscription plans draws from a separate monthly Agent SDK credit. Claude Code docs also state that `claude --help` does not list every flag. Do not copy older or guessed ACP examples that treat the raw `claude` binary as an ACP server.

## Permission mode default

Prefer Claude Code's `auto` permission mode for delegated Claude Code lanes:

```bash
claude --permission-mode auto --prefill "$(cat /tmp/claude-task.md)"
```

Use `auto` because it lets Claude Code run without repeated permission prompts while still routing risky actions through Claude Code's classifier. It is less disruptive than `plan`/`default` and safer than `bypassPermissions`.

Important caveats:

- `auto` requires Claude Code v2.1.83+, an eligible plan/account, a supported Claude model, and Anthropic API routing. If Claude reports that auto mode is unavailable, relaunch with `--permission-mode acceptEdits` for implementation work or `--permission-mode plan` for read-only planning/review.
- For non-interactive `claude --print` runs, repeated auto-mode blocks can abort the run because there is no user prompt to fall back to. If that happens, rerun with narrower context, clearer trusted-boundary instructions, or `acceptEdits`.
- Do not use `bypassPermissions` / `--dangerously-skip-permissions` unless Kosta explicitly asks for a YOLO lane in an isolated environment.
- To make auto persistent for normal Claude Code launches, set `permissions.defaultMode = "auto"` in Claude Code settings. Do not use VS Code's `claudeCode.initialPermissionMode` for this; it does not accept `auto`.

## Choose the right lane

Use these defaults:

- **Human/PTY-steered plan, review, or implementation**: foreground `claude --permission-mode auto --prefill "$(cat /tmp/claude-task.md)"` so the task opens in interactive Claude Code instead of spending Agent SDK / `-p` credits.
- **Truly unattended one-shot read-only plan/review**: `claude -p --permission-mode auto --output-format json` only when you need machine-readable output and no human/PTY submit path exists.
- **Truly unattended one-shot implementation with bounded scope**: `claude -p --permission-mode auto`; fall back to `acceptEdits` if auto is unavailable. Independently verify diffs/tests.
- **Long-running implementation or test loop**: prefer an interactive PTY/tmux Claude Code lane with `--prefill`; use managed background `claude -p` only when the parent system must consume structured JSON without user interaction.
- **Interactive back-and-forth**: run Claude Code in PTY mode or use Claude Code's native `--worktree --tmux` when the user wants to steer it manually across multiple turns.
- **Configured specialist**: add `--agent <name>`.
- **ACP subagent lane**: use the host's native delegation tool for isolated workers, not raw Claude Code ACP unless using a real ACP adapter.

## Default review budget and stall checks

For Claude Code review lanes, use a 15 minute cap by default unless Kosta gives a different limit. Check progress every 5 minutes while the lane is running so failures, blocked prompts, or silent stalls are caught during the run instead of after the timeout.

For unattended `claude --print` review lanes, prefer an outer `timeout 900 ...` and poll the captured process with `ps -p <pid> -o pid=,etime=,stat=,comm=` or the host's managed process/log API at roughly 300 second intervals. Avoid `pgrep -fl` patterns that can print the whole prompt unless no safer PID is available. If a lane reaches the cap without useful output, report it as inconclusive, not as a clean review.

## Preferred prefilled interactive pattern

Run from the repo/workdir that should provide project context. For anything longer than a sentence or two, write the prompt to a file first, then prefill the interactive prompt. This avoids `claude -p` / Agent SDK credits when a human or PTY controller can press Enter and steer the run:

```bash
cat > /tmp/claude-task.md <<'PROMPT'
<task prompt>
PROMPT

claude --permission-mode auto \
  --append-system-prompt "Return files read, commands run, findings, blockers, and exact verification steps." \
  --prefill "$(cat /tmp/claude-task.md)"
```

For a configured Claude Code agent:

```bash
cat > /tmp/claude-task.md <<'PROMPT'
<task prompt>
PROMPT

claude --agent design-agent-claude \
  --prefill "$(cat /tmp/claude-task.md)"
```

Only use the old `claude --print --input-format text --output-format json ... "$(cat /tmp/claude-task.md)"` pattern when the caller truly needs unattended machine-readable output. On Kosta's Mac Studio, do **not** use stdin redirection (`< /tmp/task.md`) with the native Claude Code binary from Hermes background processes — it has produced `stty: stdin isn't a terminal` and no useful result.

Use `--agents '<json>'` for ephemeral session-local agents when a file-backed agent is overkill.

## Background pattern

Use the host's PTY/tmux/background process tracking when Claude Code may take minutes, run tests, or iterate on a non-trivial repo change. Prefer an interactive prefilled lane so it stays on normal Claude Code subscription usage:

```bash
cat > /tmp/claude-task.md <<'PROMPT'
<implementation task>
PROMPT

claude --permission-mode auto \
  --append-system-prompt "Return files changed, checks run, blockers, and exact verification commands." \
  --prefill "$(cat /tmp/claude-task.md)"
```

Start it with the host's managed PTY/background task API when one exists, not shell `&`, `nohup`, or `disown`. Use the host's polling/log APIs to inspect progress. If no PTY/interactive submit path exists and machine-readable capture is required, fall back to `claude --print --input-format text --output-format json ...`; parse/capture the `session_id`, verify diffs and tests independently, and only then rely on the report.

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
- Prefer prompt files plus `--prefill "$(cat /tmp/claude-task.md)"` for human/PTY-steered Claude Code lanes; avoid `claude -p` unless the run must be unattended or produce structured JSON.
- Avoid stdin redirection from Hermes background processes because it can fail with `stty: stdin isn't a terminal`.
- Use `--append-system-prompt` or `--append-system-prompt-file` to preserve Claude Code's default behavior while adding lane-specific instructions.
- Use `--system-prompt` only when intentionally replacing Claude Code's default system prompt.
- For `--add-dir`, put the prompt before variadic flags or use the tested prompt-file positional pattern to avoid argument parsing mistakes.
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

Test the adapter in the current environment before relying on it for real work. For most human-steered orchestration, interactive `claude --prefill` is simpler and avoids Agent SDK credit burn; use `claude -p` only when the parent system truly needs unattended structured output.

## Freshness check

Before changing scripts or instructions around Claude Code flags, run:

```bash
claude --version
claude --help | grep -E -- '--agent|--agents|--print|--permission-mode|--tools|--allowedTools|--append-system-prompt|--add-dir|--bare|--worktree|--tmux' || true
python - <<'PY'
import subprocess, time
p = subprocess.Popen(['claude','--prefill','prefill smoke'], cwd='/tmp')
time.sleep(2)
print('prefill_accepted_started_interactive=', p.poll() is None)
p.terminate()
PY
claude --print --permission-mode auto --input-format text --output-format json <<< 'Say ok'
claude --acp --stdio
```

The last command should be treated as a negative check: if it still says `unknown option '--acp'`, do not use raw-Claude ACP examples.

## After updating Hermes instructions or tool schemas

If you correct a Hermes skill, prompt file, or `delegate_task` schema, remember that the current Telegram/gateway session may still show the old tool description until the gateway or session reloads. Verify the files and synced skills on disk, then restart/reload the relevant gateway/session before treating the new guidance as active in live tool schemas.
