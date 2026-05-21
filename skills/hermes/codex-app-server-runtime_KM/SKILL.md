---
name: codex-app-server-runtime_KM
description: >-
  Use when configuring or choosing how Hermes should run OpenAI/Codex models, when
  Kosta says to use Codex, when changing `model.openai_runtime`, or when deciding
  between Codex app-server and the default Hermes runtime.
metadata:
  targets:
    - hermes-default
    - hermes-gpt
    - claude-hermes
  hermes:
    command_priority: 430
---
# Codex App-Server Runtime

Default stance for Kosta's Hermes setup: **use Codex app-server for OpenAI/Codex turns**. It is better than treating Codex as just another Responses/chat backend because the model gets Codex CLI's native runtime: sandboxed shell, `apply_patch`, `update_plan`, `view_image`, and installed Codex plugins, while Hermes exposes its richer tools back to Codex through the `hermes-tools` MCP callback.

## When to use it

Use `model.openai_runtime: codex_app_server` for normal OpenAI-Codex coding/tool-heavy work, including implementation, refactors, tests, file edits, repo inspection, plugin-enabled work, and tasks that benefit from Codex's sandbox and native plugins.

Use the default Hermes runtime (`model.openai_runtime: auto`) only when the task specifically needs Hermes agent-loop state that Codex app-server cannot access through a stateless MCP callback:

- `delegate_task`
- `memory`
- `session_search`
- Hermes `todo`

Codex has its own `update_plan`, so lack of Hermes `todo` is usually fine inside a Codex coding turn.

## What app-server provides

- ChatGPT/Codex subscription auth via the Codex CLI session.
- Codex built-ins: sandboxed `shell`, `apply_patch`, `update_plan`, `view_image`, and Codex web search where configured.
- Native Codex plugins installed in Codex, such as GitHub, Linear, Gmail, Calendar, Google Drive, Figma, Canva-like/design plugins, and Kosta's local Codex plugin set.
- Hermes MCP callback tools: `web_search`, `web_extract`, browser tools, `vision_analyze`, `image_generate`, `skill_view`, `skills_list`, `text_to_speech`, and `kanban_*`.

## Configure

Preferred toggle in an active Hermes session:

```text
/codex-runtime codex_app_server
```

Equivalent config:

```yaml
model:
  openai_runtime: codex_app_server
```

Switch back when needed:

```text
/codex-runtime auto
```

The change takes effect on the next session because the current agent keeps its cached runtime.

## Verification

After enabling, verify:

```bash
codex --version
python - <<'PY'
import yaml, pathlib
for path in ['~/.hermes/config.yaml', '~/.hermes/profiles/gpt/config.yaml']:
    cfg = yaml.safe_load(pathlib.Path(path).expanduser().read_text()) or {}
    print(path, cfg.get('model', {}).get('openai_runtime'))
PY
python -m tomllib ~/.codex/config.toml 2>/dev/null || python - <<'PY'
import tomllib, pathlib
with pathlib.Path('~/.codex/config.toml').expanduser().open('rb') as f:
    tomllib.load(f)
print('codex config ok')
PY
```

Also check that `~/.codex/config.toml` has the Hermes-managed MCP block with `mcp_servers.hermes-tools`; this is what lets Codex call back into Hermes tools.

## Caveats

Do not enable this blindly for profiles/jobs whose core behavior depends on `delegate_task`, `memory`, `session_search`, or Hermes `todo`. For those, keep `openai_runtime: auto` or use a dedicated default-runtime profile.

Cron jobs using OpenAI-Codex inherit the runtime from their profile. If a cron job needs Hermes agent-loop tools, keep it on a profile with `openai_runtime: auto`.
