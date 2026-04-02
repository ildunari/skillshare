
# Architecture Review Checklist

- [ ] Layering respected (UI ↔ ViewModel/Interactor ↔ Domain ↔ Data)
- [ ] Domain independent of UI frameworks
- [ ] Dependencies injected, not singletons (except carefully scoped)
- [ ] Cross-module APIs documented and stable
- [ ] Boundaries enforced in CI (architecture_validator)
