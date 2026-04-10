# Agent Presets (Renderer Pipeline)

Use `scripts/pipeline.js` with a preset for predictable behavior in autonomous agent runs.

## Recommended default

```bash
node scripts/pipeline.js deck.snapped.ir.json deck.pptx --preset agent_polished
```

`agent_polished` keeps both preflight checks enabled, runs animation injection, and avoids auto-build animation heuristics by default.

## Preset table

| Preset | Intended use | Behavior |
|---|---|---|
| `agent_polished` | Default for Claude/ChatGPT agent runs | Preflight on, animation pass on, auto-build off, soft-fail preflight |
| `agent_polished_animated` | Curated animation polish pass | Same as polished with animation pass emphasized, auto-build still off by default |
| `agent_strict` | CI/quality gate | Same as polished, but preflight failures terminate run |
| `agent_fast` | Quick iteration | Skip preflight + animation pass for speed |

## CLI flags and env override

- `--preset <name>`: select preset from `assets/agent-presets.json`
- `--skip-preflight`: skip `preflight_ir.py` and `preflight_pptx.py`
- `--skip-animations`: skip `inject_animations.py`
- `--auto-animations`: pass `--auto` to animation injection
- `--strict-preflight`: turn preflight failures into non-zero exit
- `--vision-qa`: run thumbnail generation + optional vision QA hook before PPTX preflight
- `PPTX_AGENT_PRESET=<name>`: set default preset without changing command text

## What `--auto-animations` means

The animation injector supports an optional auto-build sequence (`--auto`) that can add staged element reveals inferred from object names and geometry. This can improve visual pacing, but may fail on some decks if bbox matching is ambiguous.

Default recommendation:
- Keep auto animations **off** for reliability.
- Enable only when you need staged reveals and can afford one extra QA pass:

```bash
node scripts/pipeline.js deck.snapped.ir.json deck.pptx --preset agent_polished --auto-animations
```

## Installed artifact smoke check

After installing the skill package, run:

```bash
node scripts/pipeline.js evals/files/sample.deck.ir.json out.pptx --preset agent_polished --skip-animations
```

Legacy convenience path (same file copied at repo root):

```bash
node scripts/pipeline.js sample.deck.ir.json out.pptx --preset agent_polished --skip-animations
```
