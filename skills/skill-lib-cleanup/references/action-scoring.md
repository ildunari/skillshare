# Action Scoring

Every skill should end with one primary recommendation.

## Actions
- KEEP
- KEEP + REWRITE
- MERGE INTO
- SPLIT
- ARCHIVE
- REMOVE
- SYNC FROM SOURCE
- PUSH TO TARGETS
- PROMOTE TO SOURCE
- REGENERATE INSTALLS
- FIX ROUTING
- MARK PROJECT-LOCAL EXCEPTION

## Principles
- Use sync/regenerate actions before delete actions when canonical source exists.
- Use promote-to-source when runtime copy is the only live version of a skill worth keeping.
- Use remove only with high confidence and when the item is not canonical source material.
