# Layout and files

## Recommended first layout

```text
~/.hermes/shared/durable-state/
  README.md
  SPEC.md
  MAP.yaml
  REGISTRY.md
  change-log/
    README.md
    daily/
  specs/
    placement-rules.md
    change-log-spec.md
    map-spec.md
    maintenance-audit-spec.md
```

## File roles

- `README.md` — orientation
- `SPEC.md` — top-level contract
- `MAP.yaml` — machine-readable layout map
- `REGISTRY.md` — human-readable placement guide
- `change-log/` — canonical operational history
- `specs/` — normative sub-area specs

## Source-of-truth classes

- `change-log/` = canonical operational history
- `specs/` = normative docs for sub-areas
- `MAP.yaml` = machine-readable layout source of truth
- `REGISTRY.md` = human-readable placement registry
