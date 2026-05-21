---
name: NotebookLM
description: >
  Automate Google NotebookLM — create notebooks, add sources (URLs, PDFs, YouTube),
  generate podcasts, videos, quizzes, flashcards, slide decks, reports, infographics,
  mind maps, and data tables. Chat with documents and download artifacts. Use whenever
  the user mentions NotebookLM, wants to create a podcast from content, generate study
  materials, turn documents into audio/video, or asks about research-to-podcast workflows.
  Also triggers on: "create a podcast about", "summarize these URLs", "generate a quiz",
  "turn this into audio", "make flashcards", "create a video explainer", "make an
  infographic", "create a mind map". Supersedes manual web UI workflows for NotebookLM tasks.
requiredSources:
  - notebooklm
alwaysAllow:
  - Bash
---

# NotebookLM Automation

Complete programmatic access to Google NotebookLM via the `notebooklm` CLI — including
capabilities not exposed in the web UI. Create notebooks, add sources, generate all
artifact types, chat with documents, and download results in multiple formats.

## Prerequisites

The `notebooklm` CLI must be installed and authenticated. Verify before proceeding:

```bash
notebooklm --version    # Verify installation
notebooklm auth check   # Check auth status
```

If `notebooklm` is not found, install it with `pip install notebooklm-py` (or `uv tool install notebooklm-py`), then run `notebooklm login` to authenticate (opens browser for Google OAuth). If auth check fails, run `notebooklm login` to refresh the session.

This skill requires the `notebooklm` source to be configured in Craft Agents.

## When This Skill Activates

**Explicit:** User says "/notebooklm", "use notebooklm", or mentions the tool by name.

**Intent detection — recognize requests like:**
- "Create a podcast about [topic]"
- "Summarize these URLs/documents"
- "Generate a quiz from my research"
- "Turn this into an audio overview"
- "Create flashcards for studying"
- "Generate a video explainer"
- "Make an infographic"
- "Create a mind map of the concepts"
- "Download the quiz as markdown"

## Autonomy Rules

**Run automatically (no confirmation needed):**
- All read/list/status commands (`list`, `status`, `auth check`, `source list`, `artifact list`)
- `create` — creating notebooks
- `use <id>` — setting notebook context
- `ask "..."` — chat queries
- `source add` — adding sources
- `history` — viewing conversation history
- `language list/get/set` — language configuration

**Pause and ask before running these commands** (even though Bash is auto-approved, these warrant explicit user confirmation because they are destructive, long-running, or write to disk):
- `delete` — permanently removes notebooks or sources
- `generate *` — takes 5-45 minutes and consumes Google quota
- `download *` — writes files to the local filesystem
- `ask "..." --save-as-note` — modifies notebook content

## Quick Reference

| Task | Command |
|------|---------|
| List notebooks | `notebooklm list --json` |
| Create notebook | `notebooklm create "Title" --json` |
| Set context | `notebooklm use <notebook_id>` |
| Add URL | `notebooklm source add "https://..." --json` |
| Add file | `notebooklm source add ./file.pdf --json` |
| Add YouTube | `notebooklm source add "https://youtube.com/..." --json` |
| List sources | `notebooklm source list --json` |
| Wait for source | `notebooklm source wait <source_id>` |
| Chat | `notebooklm ask "question"` |
| Chat with refs | `notebooklm ask "question" --json` |
| Save answer as note | `notebooklm ask "question" --save-as-note` |
| Generate podcast | `notebooklm generate audio "instructions" --json` |
| Generate video | `notebooklm generate video --json` |
| Generate quiz | `notebooklm generate quiz --json` |
| Generate flashcards | `notebooklm generate flashcards --json` |
| Generate report | `notebooklm generate report --format study-guide` |
| Generate slide deck | `notebooklm generate slide-deck --json` |
| Generate infographic | `notebooklm generate infographic --json` |
| Generate mind map | `notebooklm generate mind-map` |
| Generate data table | `notebooklm generate data-table "description"` |
| Check artifacts | `notebooklm artifact list --json` |
| Wait for artifact | `notebooklm artifact wait <id>` |
| Download audio | `notebooklm download audio ./out.mp3` |
| Download video | `notebooklm download video ./out.mp4` |
| Download slides | `notebooklm download slide-deck ./out.pptx --format pptx` |
| Download quiz | `notebooklm download quiz ./out.json` |
| Download flashcards | `notebooklm download flashcards ./cards.json` |
| Download report | `notebooklm download report ./report.md` |
| Download mind map | `notebooklm download mind-map ./map.json` |
| Download data table | `notebooklm download data-table ./data.csv` |
| Web research | `notebooklm source add-research "query" --mode deep` |
| Delete notebook | `notebooklm notebook delete <id>` |

**Note:** `source add --json` returns a JSON object containing `source_id`. Capture this value to use with `source wait` and source-specific generation (`-s <source_id>`).

## Generation Options

| Type | Key Options |
|------|-------------|
| Audio | `--format [deep-dive\|brief\|critique\|debate]`, `--length [short\|default\|long]` |
| Video | `--format [explainer\|brief]`, `--style [classic\|whiteboard\|kawaii\|anime\|watercolor\|retro-print]` |
| Slide Deck | `--format [detailed\|presenter]`, `--length [default\|short]` |
| Infographic | `--orientation [landscape\|portrait\|square]`, `--style [sketch-note\|professional\|bento-grid\|editorial]` |
| Report | `--format [briefing-doc\|study-guide\|blog-post\|custom]`, `--append "extra instructions"` |
| Quiz | `--difficulty [easy\|medium\|hard]`, `--quantity [fewer\|standard\|more]` |
| Flashcards | `--difficulty [easy\|medium\|hard]`, `--quantity [fewer\|standard\|more]` |

All generate commands also support: `-s/--source` for specific sources, `--language` for output language, `--retry N` for auto-retry on rate limits.

## Common Workflows

### Research to Podcast

```bash
notebooklm create "Research: [topic]" --json
notebooklm source add "https://url1.com" --json   # Returns {"source_id": "abc..."}
notebooklm source add "https://url2.com" --json   # Returns {"source_id": "def..."}
# Wait for each source to finish processing before generating
notebooklm source wait <source_id_1>
notebooklm source wait <source_id_2>
notebooklm generate audio "Focus on key insights, make it engaging" --json
# Note the artifact_id, then wait or check later
notebooklm artifact wait <artifact_id>
notebooklm download audio ./podcast.mp3
```

For automated wait+download, spawn a background subagent:
```
Task: "Wait for artifact {id} in notebook {nb_id}, then download.
       notebooklm artifact wait {id} -n {nb_id} --timeout 1200
       notebooklm download audio ./podcast.mp3 -a {id} -n {nb_id}"
```

### Document Analysis

```bash
notebooklm create "Analysis" --json
notebooklm source add ./document.pdf --json
notebooklm ask "What are the key themes?" --json
notebooklm ask "What are the main arguments?"
```

### Study Materials Generation

```bash
notebooklm create "Study: [subject]" --json
notebooklm source add "https://textbook-url.com" --json
notebooklm generate quiz --difficulty medium --json
notebooklm generate flashcards --quantity more --json
notebooklm generate report --format study-guide
# Download all
notebooklm download quiz ./quiz.json
notebooklm download flashcards ./cards.json
notebooklm download report ./study-guide.md
```

### Deep Web Research

```bash
notebooklm create "Research: [topic]" --json
notebooklm source add-research "query" --mode deep --no-wait
# Check status periodically or spawn subagent
notebooklm research wait --import-all --timeout 1800
notebooklm ask "Synthesize the key findings"
```

## Parallel Agent Safety

When running multiple agents concurrently, avoid `notebooklm use` (shared context file). Instead, always pass explicit notebook IDs:
- `-n <notebook_id>` for wait/download commands
- `--notebook <notebook_id>` for other commands
- `-c <conversation_id>` for chat continuations
- Set `NOTEBOOKLM_HOME=/tmp/agent-$ID` for full per-agent isolation

## Timing & Rate Limits

| Operation | Typical Time | Timeout |
|-----------|-------------|---------|
| Source processing | 30s - 10 min | 600s |
| Audio generation | 10 - 20 min | 1200s |
| Video generation | 15 - 45 min | 2700s |
| Quiz/flashcards | 5 - 15 min | 900s |
| Report/data table | 5 - 15 min | 900s |
| Mind map | Instant | n/a |
| Research (fast) | 30s - 2 min | 180s |
| Research (deep) | 15 - 30+ min | 1800s |

Rate limiting is common for audio/video/quiz/infographic generation. If generation fails, wait 5-10 minutes and retry. Notebooks, sources, chat, mind maps, and reports are always reliable.

## Error Handling

| Error | Fix |
|-------|-----|
| Auth/cookie error | `notebooklm login` |
| "No notebook context" | Use `-n <id>` or `notebooklm use <id>` |
| Rate limiting | Wait 5-10 min, retry |
| Download fails | Check `artifact list` — generation may not be complete |
| RPC protocol error | May need `pip install --upgrade notebooklm-py` |

## Features Beyond Web UI

These work via CLI but not in NotebookLM's web interface:
- Batch artifact downloads
- Quiz/flashcard export as JSON/Markdown/HTML
- Mind map JSON extraction
- Data table CSV export
- Slide deck as editable PPTX
- Individual slide revision
- Source fulltext access
- Programmatic sharing management
- Save chat answers as notes
