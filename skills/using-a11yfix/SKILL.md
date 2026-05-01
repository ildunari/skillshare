---
name: using-a11yfix
description: >
  Run the a11yfix CLI on a single Office file or a folder of Office files. Use when the user asks to scan, audit, fix, remediate, or check accessibility on .docx / .pptx files, or points at a folder containing them. Delegates the deterministic detection step to a Sonnet subagent (`a11y-detector`) so the main session preserves Opus context for judgment-call work.
metadata:
  when-to-use: >
    Trigger phrases: "run a11yfix", "scan this folder for accessibility", "fix accessibility on these files", "ADA check this deck", "make this compliant". Also when the user gives a folder path containing .docx/.pptx files and asks for accessibility work.
compatibility: Claude Code with `a11yfix` CLI installed (pipx or local venv) and the `a11y-detector` subagent available.
---

# using-a11yfix

This skill is the orchestrator for running the `a11yfix` CLI from a Claude Code session. It picks the right mode, delegates detection to the Sonnet subagent, and decides when to launch the stage-4 interactive remediation.

## When to use which mode

The CLI exposes three modes via `--mode`:

| Mode | What happens | When to pick |
|---|---|---|
| `scan` | Detect only, no writes. Produces a manifest JSON. | Audit, CI gate, "what's broken?" |
| `auto` | Stages 1+2: detect + deterministic fixes (header flags, document title from filename if `--default-lang` given for language). No AI, no network. | Bulk processing, "fix what you can without judgment" |
| `full` | Adds stage 3 (AI-generated alt text / link text / slide titles) and launches Claude Code on the residual findings via the `fixing-office-accessibility` skill. | Interactive remediation; user wants the works |

**Default policy in this skill:** if the user says "scan", "check", or "audit", use `scan`. If they say "fix" or "make compliant", use `auto` first, show them the residual count, then ask whether they want `full` for the rest. Never jump straight to `full` without confirmation — it spawns a separate interactive session.

## Single file

```bash
a11yfix /path/to/deck.pptx --mode scan
a11yfix /path/to/deck.pptx --mode auto --output /tmp/deck.manifest.json
```

## Folder (the common ask)

When the user points at a folder, walk it and dispatch the **`a11y-detector` Sonnet subagent** for the detection-heavy work. This is critical: detection on a folder of 50 documents would burn Opus tokens for nothing. The subagent does the deterministic work and returns a structured summary.

```bash
# In the main session, dispatch the subagent:
# (Use Claude Code's Task tool with subagent_type="a11y-detector")
```

The subagent's contract:
- **Input**: a folder path and a mode (`scan` or `auto`)
- **Output**: a JSON summary `{ files: [{ path, manifest_path, findings_total, residual_total, severity_counts }], total_findings, total_residual }`
- **It runs `a11yfix --mode {mode} --output ...` on every .docx/.pptx file in the folder (recursive by default)**
- **It does NOT load the `fixing-office-accessibility` skill** — that's stage 4, handled by the main session if asked

After the subagent returns, the main session presents the summary in a table, identifies any high-severity outliers, and asks the user whether to run `full` mode on individual files that need judgment.

## Interaction rules

- **Always confirm scope before running on a folder** — count the files first, show the count, then ask. "I see 47 .docx and 12 .pptx files in `~/Downloads/decks`. Run `auto` on all? (~2 min)"
- **Never run `full` mode in a batch** — it spawns interactive sessions; do them one file at a time after the user picks which.
- **Show the manifest path for each file** — the user may want to inspect them or hand them off to colleagues.
- **Per-file errors must not block the batch** — if one file fails, log it and continue.
- **When the run is done, summarize** — total files, total findings, total fixed, total residual; flag the worst offenders by error count.

## Example session flows

### "Run a11yfix on my Downloads folder"

1. List candidates: `find ~/Downloads -maxdepth 2 -type f \( -iname "*.docx" -o -iname "*.pptx" \)` — show the count.
2. Confirm with the user: mode? scan or auto?
3. Dispatch `a11y-detector` subagent with `{folder, mode}`.
4. Present the returned summary as a table sorted by error count.
5. Offer: "Want me to run `full` mode on the top 3 worst files?" — then handle one at a time.

### "Fix accessibility on this deck"

1. Single file → run directly with `auto` mode.
2. Show the residual count + top issues.
3. If residual > 0, ask: "There are N residual findings that need judgment. Run `full` mode? It launches an interactive Claude session."

### "Just scan, don't write anything"

1. Run with `scan` mode.
2. Present findings; do nothing else.

## CLI flags worth knowing

```bash
--mode scan|auto|full          # the user-facing knob
--dry-run                      # with --mode full: show the launch plan, don't execute
--output PATH                  # explicit manifest output path
--strict                       # non-zero exit on any Error severity (CI use)
--rules RULE,RULE              # allowlist subset of rules
--skip-rules RULE,RULE         # subset to skip
--default-lang en-US           # opt in to deterministic language tag
```

## Installation check

If `a11yfix` is not on PATH, suggest:

```bash
pipx install git+https://github.com/ildunari/a11yfix.git
officecli skills install pptx word
```

Don't install silently — confirm first.

## What this skill does NOT do

- It does not detect or fix issues itself; it always shells out to `a11yfix`.
- It does not load the `fixing-office-accessibility` skill — that's loaded only by the stage-4 launch from `--mode full`.
- It does not parse OOXML directly — that's `a11yfix`'s job.
