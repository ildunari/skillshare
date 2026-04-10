# Hermes targets workflow

This repo tracks the canonical Hermes allowlist in `hermes-allowlist.yaml`.
The local `config.yaml` file stays machine-specific and is intentionally not committed.

Rules:
- Studio is the only machine that manages Hermes Skillshare targets.
- MacBook stays isolated from Hermes Skillshare targets unless explicitly re-enabled.
- Hermes default and Hermes GPT must share the same allowlist.
- Do not bulk-copy all Skillshare skills into Hermes.
- Do not add `_archived/*` skills to Hermes.

Canonical files:
- `hermes-allowlist.yaml` — tracked source of truth for Hermes skills
- `scripts/sync_hermes_targets.py` — applies the tracked allowlist into local `config.yaml`

Common commands:

Studio:
```bash
cd ~/.config/skillshare
python3 scripts/sync_hermes_targets.py --mode studio
skillshare sync
git status
git add hermes-allowlist.yaml scripts/sync_hermes_targets.py hermes-targets.md .gitignore
git commit -m "Update Hermes allowlist"
git push
```

MacBook isolation:
```bash
cd ~/.config/skillshare
python3 scripts/sync_hermes_targets.py --mode isolate
```

When adding a skill to Hermes:
1. Edit `hermes-allowlist.yaml`
2. Run the Studio sync script
3. Run `skillshare sync`
4. Verify Hermes target counts look right
5. Commit and push the tracked change

Do not edit the Hermes allowlist directly inside `config.yaml` by hand unless you are recovering from a broken script.
