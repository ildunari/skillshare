# Fal Seedance video generation and Hermes tool/plugin notes — 2026-05-06

## Current local setup

Hermes image generation should stay on Codex/OpenAI GPT Image:

```yaml
image_gen:
  provider: openai-codex
  model: gpt-image-2-medium
```

Fal is reserved for video generation:

```yaml
video_gen:
  provider: fal
  model: bytedance/seedance-2.0/text-to-video
  fal:
    text_to_video_model: bytedance/seedance-2.0/text-to-video
    image_to_video_model: bytedance/seedance-2.0/image-to-video
    resolution: 720p
    duration: auto
    generate_audio: true
```

The local built-in tool is `video_generate` in `tools/video_generation_tool.py`. It routes:

- text-only prompts to `bytedance/seedance-2.0/text-to-video`
- calls with `image_url` to `bytedance/seedance-2.0/image-to-video`

It returns JSON with `success`, `video`, `model`, `seed`, and raw `result`. Deliver returned video URLs or downloaded `.mp4` paths with normal Hermes media delivery (`MEDIA:/abs/path` for local files, or a video URL when the platform supports it).

## Fal API details checked

Current fal docs list:

- Text-to-video endpoint: `POST https://fal.run/bytedance/seedance-2.0/text-to-video`
- Endpoint ID: `bytedance/seedance-2.0/text-to-video`
- Image-to-video endpoint ID: `bytedance/seedance-2.0/image-to-video`
- Python pattern: `fal_client.subscribe(model_id, arguments={...}, with_logs=True)`
- Image-to-video input accepts `prompt`, `image_url`, optional `end_image_url`, `resolution`, `duration`, `aspect_ratio`, `generate_audio`, `seed`.
- Output includes `video.url` and `seed`.

Do not run live video smoke tests casually; Seedance calls spend fal credits.

Docs checked:

- https://fal.ai/docs/model-api-reference/video-generation-api/bytedance-seedance-2.0-text-to-video
- https://fal.ai/models/bytedance/seedance-2.0/image-to-video/api

## Hermes plugin and tool architecture notes

Hermes has two relevant paths for custom capability:

1. **Plugin path — preferred for personal/project-local custom tools.** Drop a directory under `~/.hermes/plugins/<name>/` with `plugin.yaml` and `__init__.py`. In `register(ctx)`, call `ctx.register_tool(name=..., toolset=..., schema=..., handler=...)`. Plugins can also register hooks, slash commands, CLI commands, bundled skills, gateway platforms, and backend providers.
2. **Built-in tool path — use for local branch/core behavior.** Add `tools/<tool>_tool.py` with a top-level `registry.register(...)`; Hermes auto-discovers built-in tool modules containing that registration. Add the tool to `toolsets.py` so normal platform toolset resolution exposes it, and update `hermes_cli/tools_config.py` if users should toggle it in `hermes tools`.

Built-in handlers receive `(args: dict, **kwargs)` and should return a JSON string, not a raw dict. Errors should be structured JSON instead of uncaught exceptions. `check_fn` controls whether a tool appears in the model schema; if it returns false, the model will not see the tool.

### Built-in tool exposure checklist

When adding a built-in media tool, do all of these before calling it complete:

1. Add `tools/<name>_tool.py` with a top-level `registry.register(...)`; auto-discovery only sees modules with that top-level call.
2. Put the tool in the right entry in `toolsets.py`. If it should be available to the API server or a platform composite, update those composite toolsets too, not just the small category toolset.
3. Update `hermes_cli/tools_config.py` if `hermes tools` should show a toggle/label for the toolset.
4. Add tests for the handler contract and toolset exposure. For media tools, include no-credit/no-quota checks that prove schema visibility without calling the paid provider.
5. Verify both registration and model-schema visibility: `registry.get_entry('<tool>')` can be true while `registry.get_definitions({'<tool>'})` is false if `check_fn` cannot see env/deps.

This session hit exactly that pitfall: `video_generate` existed, but the `video` toolset and API-server composite needed explicit updates before agents could reliably see it.

Project-local plugins under `./.hermes/plugins/` are disabled by default; only enable them for trusted repos with `HERMES_ENABLE_PROJECT_PLUGINS=true`.

Docs checked:

- https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins
- https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin
- https://hermes-agent.nousresearch.com/docs/developer-guide/adding-tools
- https://hermes-agent.nousresearch.com/docs/user-guide/features/tools

## Verification commands

From `~/.hermes/hermes-agent`:

```bash
source .venv/bin/activate
python -m py_compile tools/video_generation_tool.py toolsets.py hermes_cli/tools_config.py
pytest -q tests/tools/test_video_generation_tool.py tests/test_video_toolset.py tests/gateway/test_api_server_toolset.py
```

No-credit availability check:

```bash
python - <<'PY'
from hermes_cli.config import load_config
from tools.registry import registry, discover_builtin_tools
cfg = load_config()
print('image provider:', cfg.get('image_gen', {}).get('provider'))
print('video provider:', cfg.get('video_gen', {}).get('provider'))
print('video model:', cfg.get('video_gen', {}).get('model'))
discover_builtin_tools()
print('video_generate registered:', bool(registry.get_entry('video_generate')))
print('video_generate schema visible:', bool(registry.get_definitions({'video_generate'})))
PY
```
