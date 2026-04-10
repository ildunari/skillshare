# Skill Topology

This reference is for the skill-management side of the optimizer.

## Distinguish these roles

### Source skill
The authoring location where the skill should be maintained.

### Runtime install
A copy placed where a runtime expects to find the skill.

### Mirror / synced copy
A duplicate created by a sync workflow or filesystem mirroring.

### Packaged artifact
A built/exported skill package rather than the editable source.

## What to detect

For each skill slug:
- how many copies exist
- where they live
- whether they are exact duplicates or diverged
- which copy looks like the source of truth
- whether any runtime has a stale copy
- whether some copies look generated and should be regenerated rather than edited

## Reporting goals

The topology view should help answer:
- Where should I edit this skill?
- Which installs are stale?
- Which copies are safe to remove?
- Do multiple runtimes share one exact payload or have they drifted?
