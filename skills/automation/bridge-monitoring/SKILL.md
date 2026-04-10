---
name: bridge-monitoring
description: Test, debug, and monitor a running Office add-in via the local bridge server. Use this skill whenever you need to interact with a live Word, Excel, or PowerPoint add-in session — whether that's running a tool, taking a screenshot, checking runtime state, monitoring events, debugging a stuck plan, asserting state for CI gates, benchmarking tool latency, inspecting the DOM, focusing or clicking the Word side panel, or running regression tests. Also use it when the user mentions "bridge", "office-bridge", side panel state, add-in debugging, Hybrid Word, localhost:4017, localhost:4018, corpus-backed live testing, or tool execution against a live document. Even simple tasks like "check if Word is connected", "focus the add-in", or "what mode is the agent in" should trigger this skill because it knows the exact CLI and taskpane-focus workflow.
---

## When to Use This

The Office Bridge is a local HTTPS/WebSocket server (port 4017 by default, 4018 for the Hybrid Word setup in this repo) that connects to running Office add-in taskpanes during development. It lets you inspect state, execute tools, take screenshots, monitor events, and now focus/click the Word taskpane from the terminal.

Important: the pane-focus helper is not the main testing method. It only helps
surface or focus the Word side panel so the real bridge-based testing workflow
can proceed. The main method remains: confirm the live session, inspect
`summary` / `state` / `diag`, run tools, monitor `events` / `poll`, and capture
screenshots and artifacts.

Use this skill whenever you need to:
- **Verify** a tool works after a code change
- **Debug** why the agent is stuck, erroring, or behaving unexpectedly
- **Monitor** events in real-time during a test session
- **Assert** runtime state for automated checks
- **Compare** visual state before and after changes

The bridge must be running (`pnpm bridge:serve`) and an add-in must be open in an Office app for commands to work.

## Quick Start

```bash
pnpm bridge:serve                    # Start bridge (reuses if already running)
pnpm exec office-bridge list         # See connected sessions
pnpm exec office-bridge summary word # One-line status
```

For the Hybrid Word add-in in this repo, prefer:

```bash
pnpm bridge:serve:hybrid
pnpm exec office-bridge --url https://localhost:4018 list
scripts/bridge/focus-word-pane.sh --target body
```

If the pane is open but not focused, use:

```bash
scripts/bridge/focus-word-pane.sh --target header
scripts/bridge/focus-word-pane.sh --target body
scripts/bridge/focus-word-pane.sh --target input
```

## Choosing the Right Command

Pick your command based on what you're trying to accomplish. All commands accept a session identifier — usually the app name (`word`, `excel`, `powerpoint`).

**"What's happening right now?"** — Start with `summary` for a one-liner, then `state` for full runtime state JSON, or `diag` for a combined dump of state + events + session info.

**"Did my change work?"** — Use `tool` to execute a specific tool against the live document and inspect the result. Follow up with `assert` to programmatically verify the runtime is in the expected state.

**"Something is wrong"** — Use `state` to check mode/phase/errors, `events --limit 50` to see recent lifecycle events, and `diag` for the full picture. For UI issues, `dom visible-panels` shows what's visible and `screenshot` captures the current view.

**"I want to watch what happens"** — Use `poll` to stream events as NDJSON in real-time, filtered by type. For longer monitoring, use `scripts/bridge/event-monitor.sh` which logs to a JSONL file.

**"I need to benchmark or regression test"** — Use `bench` for tool latency, `screenshot-diff` for visual comparison, and the shell scripts in `scripts/bridge/` for automated test sequences.

**"The Word pane is open but I need to click or focus it"** — Use `scripts/bridge/focus-word-pane.sh` before trying manual or scripted side-panel interaction. Start with `--target body`, then `--target input` if you need the composer. After focusing the pane, continue with the normal bridge checks; do not treat the AppleScript helper as the test itself.

**"I need a live corpus-backed run, not a blank-doc smoke test"** — Use the Hybrid bridge URL (`4018`), run `wait-and-check.sh --hybrid-word`, focus the pane if needed, and then run `smoke-test.sh` with `--scenario` and `--fixture` so the artifacts are labeled by corpus case.

## Command Reference

Commands are invoked as `pnpm exec office-bridge <command> [session] [flags]`.

| Command | What it does |
|---------|-------------|
| `list` | Show all connected sessions |
| `inspect` | Full session snapshot as JSON |
| `metadata` | Document metadata only |
| `state` | Runtime state (mode, phase, streaming, plan, tokens, cost) |
| `summary` | One-line status string |
| `diag` | Combined diagnostics dump |
| `tool <name>` | Execute a named tool |
| `exec --code "..."` | Run JS in the taskpane (add `--sandbox` for Office.js context) |
| `dom <query>` | Run a pre-built DOM inspection query |
| `screenshot --out file.png` | Capture document screenshot |
| `events [--limit N]` | Recent events from ring buffer |
| `poll [--events TYPE1,TYPE2]` | Stream events as NDJSON via SSE |
| `assert --mode X --phase Y` | Exit 0 if state matches, 1 otherwise |
| `bench <tool> --runs N` | Tool latency benchmark (min/avg/max) |
| `reset [--keep-config]` | Clear IndexedDB + localStorage |
| `screenshot-diff <img1> <img2>` | Byte-level image comparison |
| `scripts/bridge/focus-word-pane.sh` | Click/focus the OpenWord Hybrid pane via macOS accessibility |

Output flags: `--json`, `--compact`, `--fields key1,key2`, `--max-tokens N`.

## DOM Queries

Pre-built queries for `dom <session> <query>`. These run JavaScript in the actual taskpane DOM context, so they reflect the real UI state.

- `visible-panels` — which tabs and panels are currently visible
- `scroll-positions` — scroll state of key scrollable containers
- `computed-theme` — current CSS variable values (`--chat-*`)
- `layout-metrics` — bounding rects of major UI sections
- `message-count` — count of visible messages by type

## Event System

The bridge emits typed events at runtime lifecycle points. Use `poll --events` to filter:

| Category | Events | When they fire |
|----------|--------|---------------|
| Message | `message:created`, `message:completed` | User/assistant message lifecycle |
| Tool | `tool:started`, `tool:completed`, `tool:failed` | Tool execution lifecycle |
| Plan | `plan:created`, `plan:step_started`, `plan:completed` | Plan execution steps |
| State | `state:mode_changed`, `state:phase_changed` | Runtime mode/phase transitions |
| Error | `error:tool`, `error:runtime`, `error:office_js` | Errors by source |
| UI | `ui:tab_changed`, `ui:panel_toggled`, `ui:scroll_position` | Frontend state changes |
| Session | `session:hmr_reload` | Hot-reload detected (not a crash) |

## Shell Scripts

Automation scripts in `scripts/bridge/` for common workflows:

| Script | Purpose |
|--------|---------|
| `wait-and-check.sh` | Wait for a session, verify tools loaded — good as a CI gate |
| `smoke-test.sh` | Full integration smoke test (5 checks: session, screenshot, metadata, inspect, events) |
| `regression-loop.sh` | Run a tool sequence from a JSON file, compare results to baselines |
| `event-monitor.sh` | Long-running event poller with type filtering and JSONL output |
| `focus-word-pane.sh` | Focus/click the `OpenWord Hybrid` taskpane at `body`, `header`, or `input` offsets |

## Hybrid Word Workflow

Use this exact order when working against the Hybrid Word add-in:

1. Start or confirm the Hybrid bridge:
   - `pnpm bridge:serve:hybrid`
2. Verify the live session:
   - `BRIDGE_URL=https://localhost:4018 scripts/bridge/wait-and-check.sh --hybrid-word`
3. Focus the pane if needed:
   - `scripts/bridge/focus-word-pane.sh --target body`
   - `scripts/bridge/focus-word-pane.sh --target input`
4. Capture baseline state:
   - `pnpm exec office-bridge --url https://localhost:4018 summary word`
   - `pnpm exec office-bridge --url https://localhost:4018 state word`
   - `pnpm exec office-bridge --url https://localhost:4018 diag word`
5. Run the tool or smoke scenario.

The AppleScript/accessibility helper only exists to make step 3 reliable. The
actual test evidence comes from steps 2, 4, and 5.

## Window Discipline

Default to **one Word document window at a time** for live testing.

- Do not keep multiple corpus documents open unless you are explicitly testing
  concurrency or session-routing behavior.
- Before opening the next test document, close the previous one and confirm the
  bridge session count matches your expectation.
- Re-run `wait-and-check.sh --hybrid-word` after switching documents so you do
  not accidentally trust a stale session attached to the wrong window.
- If you intentionally test concurrency, say so explicitly in your notes and
  capture which session/document pairing belongs to each window.

## Corpus-Backed Live Validation

For realistic document testing, label runs by scenario and fixture so the
artifacts stay attributable:

```bash
BRIDGE_URL=https://localhost:4018 scripts/bridge/smoke-test.sh \
  --hybrid-word \
  --scenario review-heavy \
  --fixture comments.docx \
  --out-dir /tmp/office-agents-live-results
```

Recommended curated live subset:
- `comments.docx` — review-heavy
- `strict-format.docx` — formatting-heavy
- `having-images.docx` — media-heavy
- `Headers.docx` — structure-heavy

## Artifact Discipline

When running smoke or probe commands, always preserve:
- bridge URL
- session/document identity
- scenario label
- fixture name
- summary/state/diag outputs
- events and screenshots

This matters because Hybrid Word failures are often document-specific, not just
“bridge is broken.”

## Cleanup Discipline

Clean up continuously during live testing instead of waiting until the end.

- Close test documents you are no longer using.
- Prefer temporary copies of corpus files for live mutation experiments.
- Remove temporary output folders that were created only for failed dry runs or
  abandoned scenarios.
- Keep only the final evidence bundles you actually plan to reference in the
  report.
- If a scenario dirties the document or leaves the pane in a confusing state,
  reset by closing the window, reopening the target document, and re-running the
  Hybrid preflight before continuing.

## Hybrid Word Notes

- The Hybrid Word add-in in this repo uses the alternate bridge on `https://localhost:4018`.
- Use `--url https://localhost:4018` or `BRIDGE_URL=https://localhost:4018` for bridge commands.
- `focus-word-pane.sh` depends on macOS Accessibility access for `System Events`.
- It targets the pane by the accessibility group named `OpenWord Hybrid` and clicks by relative offsets inside that pane.
- It is reliable for focusing the pane and the lower input region, but deep web control names inside the pane are still sparse from Word’s accessibility tree.
- A live bridge session may stay attached to the currently open document window. If you switch documents, confirm metadata/session identity again before trusting results.
- Use it to help launch or focus the side panel, then immediately return to the
  normal bridge-driven testing method.

## Deeper Reference

For full HTTP endpoint documentation (curl examples, response shapes), the complete event payload type reference, and SSE streaming details, read `packages/bridge/AGENT-API.md`.
