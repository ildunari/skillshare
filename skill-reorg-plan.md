# Skill reorganization plan

Status: planned, not yet executed.

Goal:
- Move active non-archived skills into 13 top-level buckets.
- Keep `_archived/` untouched.
- Preserve Skillshare behavior across all targets.
- Avoid breaking target include/exclude filters and sibling-relative references.

Hard rules
- Use global mode explicitly for all validation: `-g`.
- Treat the old -> new path map as canonical for the migration.
- Update config filters and move files in the same change set.
- Do not run a real `skillshare sync` until dry-run verification and downstream path diff pass.
- Keep merged helper skills with their parent family.

Known risks already confirmed
1. Config filters will break if left unchanged.
   Current live global config has target filters for:
   - `claude` excludes: `brainstorming`, `branch-finish-release`, `systematic-debugging`, `test-driven-development`, `using-superpowers`, `completion-verification-gate`
   - `hermes-default` includes: tracked small Hermes allowlist
   - `hermes-gpt` includes: tracked small Hermes allowlist

2. Relative sibling references exist and must be preserved or patched together.
   Confirmed examples include cross-links in:
   - `figma-generate-design/SKILL.md` -> `../figma-use/...`
   - `officecli-pitch-deck/creating.md` -> `../officecli-pptx/creating.md`
   - several Microsoft Foundry skill docs using `../../` and `../../../` links

3. Skillshare config is machine-local.
   - `config.yaml` remains gitignored.
   - Tracked migration assets must live outside `config.yaml`.

Migration buckets
- `agentic`
- `code-quality`
- `github-release`
- `apple`
- `ui-ux`
- `documents-office`
- `research-analysis`
- `knowledge-memory`
- `automation`
- `ai-platforms-mcp`
- `meta-tools`
- `media-creative`
- `personal-ops`

Execution plan
1. Generate canonical old -> new map for every active non-archived skill.
   Output a tracked mapping file, one line per skill.

2. Audit cross-skill references against the map.
   Scan for relative references like:
   - `../other-skill/...`
   - `../../family/...`
   Patch or co-locate related skills so references remain valid.

3. Audit all target filters against the map.
   Rewrite every include/exclude pattern in global `config.yaml` to the new paths.
   This is not Hermes-only.

4. Prepare downstream expectation snapshots before any move.
   Collect:
   - `skillshare list -g --json`
   - `skillshare status -g --json`
   - `skillshare sync -g --dry-run --json`
   - target directory manifests for affected targets

5. Apply the file moves in one reversible pass.
   Move only active non-archived skills.
   Leave `_archived/` untouched.

6. Patch docs and references immediately after moves.
   Fix any sibling-relative links revealed by the move.

7. Rewrite local global config filters.
   Update target include/exclude entries to the new bucketed paths.

8. Validate in global mode.
   Run:
   - `skillshare list -g --json`
   - `skillshare status -g --json`
   - `skillshare sync -g --dry-run --json`
   - downstream expected-vs-actual path diff for affected targets

9. Only after all checks pass, run real sync.

10. Commit and push the tracked migration assets and reference patches.

Suggested tracked artifacts
- `skill-reorg-map.yaml` — canonical old -> new path map
- `skill-reorg-plan.md` — this execution plan
- optional audit outputs under `migration-artifacts/`

Immediate next step
- Generate `skill-reorg-map.yaml` from the approved 13-bucket layout before moving any directories.
