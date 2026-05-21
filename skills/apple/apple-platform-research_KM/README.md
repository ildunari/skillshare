# apple-platform-research

A complete, opinionated research Skill for Apple/iOS/macOS topics.

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r tools/requirements.txt
export GITHUB_TOKEN=ghp_xxx   # optional but recommended
export TWITTER_BEARER_TOKEN=xxxxx  # optional for twitter_monitor.py
export REDDIT_CLIENT_ID=xxxxx
export REDDIT_CLIENT_SECRET=xxxxx
export REDDIT_USER_AGENT="apple-platform-research"
export STACKEXCHANGE_KEY=xxxxx
```

Then run scripts in `scripts/` as needed. Use `tools/report_generator.py` to assemble a report.

## Layout

- `SKILL.md` — the meta-skill for Claude
- `scripts/` — data collection & analysis tools
- `tools/` — shared utilities & report builder
- `docs/` — methodology and playbooks
- `templates/` — checklists and write-up scaffolds
- `resources/` — curated directories and bookmarks

## Notes

- Most scripts work without API keys but may be rate-limited. Keys improve reliability.
- Use responsibly. Respect robots.txt and site terms. Set polite delays (already built-in).
- Charts use matplotlib; CSV/JSON artifacts are stored in `./out/` unless overridden.
