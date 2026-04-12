# Placement taxonomy

## Use memory when
- the information is a durable user preference, correction, or stable environment fact

## Use skills when
- the information is a reusable procedure, workflow, or decision tree

## Use shared durable-state when
- the artifact is durable operational state that should survive repo updates and be inspectable outside the repo checkout

## Use profile/config/plugin/script locations when
- the artifact is runtime wiring, profile behavior, machine-local helper code, cron state, env/config, or plugin data

## Use the repo when
- the change is real Hermes source code, tests, repo docs, or repo instruction-layer logic

## Use patches when
- you need a preservation/replay layer for outside-repo files or selected local customizations
- but do not treat patches as the canonical home for the state itself
