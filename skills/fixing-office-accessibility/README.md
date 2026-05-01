# fixing-office-accessibility

Stage 4 Claude Code skill for residual Office accessibility remediation. It assumes an upstream Python CLI already handled deterministic detection, deterministic auto-fix, and single-shot AI fixes for obvious alt text, link text, and slide titles. This skill guides Claude through the remaining judgment-call fixes in `.docx` and `.pptx` files using OfficeCLI.

## Install

1. Install OfficeCLI and confirm it is on `PATH`:

```bash
officecli --help
```

2. Install the prerequisite OfficeCLI base skills for Claude Code. OfficeCLI documents these as single-skill installs; run both commands. Some newer versions may also accept the combined form `officecli skills install pptx word`.

```bash
officecli skills install pptx
officecli skills install word
```

3. Copy or unzip this directory into Claude Code's skill directory:

```bash
mkdir -p ~/.claude/skills
unzip fixing-office-accessibility.zip -d ~/.claude/skills/
ls ~/.claude/skills/fixing-office-accessibility/SKILL.md
```

No extra Python packages are required. Scripts target Python 3.11+ and use only the standard library plus the external `officecli` command when applying changes.

## Quickstart

Prompt Claude Code with a document path and the upstream residual manifest:

```text
Use the fixing-office-accessibility skill on ./benefits-guide.docx with ./benefits-guide.stage4-manifest.json. Ask me about ambiguous items, but fix high-confidence low-impact items and produce the JSON report.
```

The input manifest must follow `schemas/input-manifest.schema.json`. Each finding includes `rule_id`, `severity`, `location`, `current_value`, `why_human_needed`, and `related_findings_ids`.

## Smoke test

Run these from the skill directory:

```bash
python scripts/triage.py examples/sample-manifest.docx.json --json
python scripts/contrast.py --fg "#000000" --bg "#FFFFFF"
python scripts/report.py --manifest examples/sample-manifest.docx.json --out-json /tmp/a11y-report.json --out-md /tmp/a11y-report.md
```

A real document smoke test, when OfficeCLI and sample files are available, is:

```bash
officecli validate path/to/document.docx --json
```

## What this skill does not do

It does not run detection, re-run upstream auto-fixes, rewrite prose for clarity, repair unrelated formatting, or edit files directly with `python-docx` or `python-pptx`. OfficeCLI is the source of truth for reads, writes, validation, and raw XML fallback.

## Included helpers

- `scripts/triage.py` groups and orders manifest findings into a work plan.
- `scripts/contrast.py` calculates WCAG contrast ratios and can resolve Office theme colors from a theme XML file.
- `scripts/apply_batch.py` wraps `officecli batch` plus `officecli validate`, with backup and auto-restore on failure.
- `scripts/report.py` emits a terminal-friendly markdown report and a JSON report matching `schemas/output-report.schema.json`.
