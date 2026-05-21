# Canonical Library Mode

Use this mode when the user wants analysis of the source-of-truth skill library rather than a generic runtime inventory.

## Canonical source
Treat:
- `/Users/kosta/.config/skillshare/skills`

as the editable source of truth.

Treat:
- `/Users/kosta/.config/skillshare/config.yaml`

as the authoritative distribution map.

## Key distinctions
Separate these roles:
1. canonical source
2. runtime install
3. mirror or synced copy
4. backup or archive
5. project-local exception

## Reporting rules
- Do not recommend merging canonical source with downstream install copies.
- Prefer sync/regenerate actions over merge/delete when source and target should match.
- If a runtime copy is newer than source, flag divergence rather than deleting it.
- Report source-only and install-only skills explicitly.
