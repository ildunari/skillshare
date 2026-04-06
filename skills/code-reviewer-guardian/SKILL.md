---
name: code-reviewer-guardian
user-invocable: false
description: >
  World-class Swift/iOS/macOS code review and quality guardianship Skill.
  Use this when the user asks to review Swift code, pull requests, or whole projects;
  enforce style, safety, security, performance, architecture and documentation standards,
  and propose concrete fixes with before/after patches.
version: 1.0.0
tags: [swift, ios, macos, code-review, quality, security, performance, accessibility]
# 'allowed-tools' is honored in Claude Code; SDKs control allowed tools via options.
allowed-tools: Read, Grep, Glob, Write, Bash
---

# Code Reviewer Guardian (Swift / iOS / macOS)

<!-- Merged from: receiving-code-review, requesting-code-review (2026-04-05). Legacy material preserved under merged/. -->

> **Purpose**: Provide rigorous, actionable reviews for Swift codebases. Detect problems early,
> propose safe refactors, and elevate overall engineering quality with repeatable checklists,
> analyzers, and configuration templates.

---

## Overview

This Skill equips Claude to perform **production-grade Swift code reviews** and **PR quality gates**.
It combines philosophy, checklists, and runnable analyzers that augment SwiftLint/SwiftFormat.
It also ships with **configuration templates** for CI, **security** and **accessibility** guidance,
**architectural** guardrails, and **examples** (good vs. bad) for fast learning-by-contrast.

**Inputs**: Source tree, diffs/PRs, coverage results, SwiftLint/SwiftFormat output.  
**Outputs**: Structured findings with **severity (P0–P3)**, rationale, and **fix strategies**,
plus suggested diffs, test additions, and follow-up tasks.

---

## When to Use

- Reviewing a **PR** or **merge request** for Swift code.
- Running a **pre-commit** or CI quality gate.
- Planning a **refactor** or **architecture modernization**.
- Auditing **security** (ATS, Keychain, CryptoKit), **performance**, **threading**, and **accessibility**.
- Building team standards for **naming**, **APIs**, **DocC** docs, and **test coverage**.

---

## Code Review Philosophy

**Goals**: Safety → Correctness → Clarity → Maintainability → Performance → UX Accessibility.

Principles:
1. **Prefer clarity over cleverness**. Optimize for future readers.
2. **Local reasoning**. Shrink scope of mutable state and effects.
3. **Small, behavior‑preserving steps**. Use refactorings with tests.
4. **Automate the obvious** (linters/formatters) so humans review design.
5. **Document intent** where code alone isn’t self-evident.
6. **Security by default**: HTTPS via ATS, least privilege, secure storage.
7. **Evidence matters**: Use measurements (coverage, complexity, Instruments).

Severity:
- **P0 (Critical)**: Crashers, data loss, security/privacy violations.
- **P1 (High)**: Concurrency bugs, retain cycles, architectural boundary breaks.
- **P2 (Medium)**: Maintainability issues, test gaps, style deviations that impede readability.
- **P3 (Low)**: Nits, minor idiomatic concerns, optional improvements.

---

## SwiftLint Rules (built-in + custom)

**Built-in/opt-in highlights**: `force_unwrapping`, `force_try`, `todo`, `type_body_length`,
`file_length`, `function_body_length`, `cyclomatic_complexity`, `identifier_name`,
`explicit_self`, `trailing_whitespace`, `vertical_parameter_alignment`.

**Custom rules provided** (see `configs/custom-rules.yml`):
- **no_dispatch_main_sync**: Forbids `DispatchQueue.main.sync` (deadlock risk).
- **no_print_in_prod**: Forbids `print()` in non-test code.
- **no_ats_disable**: Flags NSAppTransportSecurity exceptions that allow arbitrary loads.
- **weak_self_in_escaping**: Warn when escaping closures reference `self` without `[weak self]`.
- **no_hardcoded_secrets**: Flags likely keys/secrets (naive heuristics).
- **no_md5_or_sha1**: Insecure hashing in security-sensitive contexts.
- **no_force_cast**: Forbids `as!` in production code.

Why it matters: Linters catch **mechanical** issues quickly. Humans focus on **design & risk**.

How to fix: Adopt `.swiftlint.yml` provided, run in CI, and remediate findings with documented patterns.

---

## SwiftFormat Guidelines

- Enforce consistent whitespace, brace style, and argument wrapping.
- Prefer trailing comma for multiline collections (diff-friendly).
- Group imports; remove duplicates.
- Normalize `self` usage and `closure` style.
- Keep max line length reasonable (e.g., 120).

Why: Consistent formatting reduces diff noise and cognitive load.  
How: Use the included `.swiftformat` with `--lint` in CI and `swiftformat` locally for autofix.

---

## Code Smell Detection

We target smells per Fowler: **Long Method, God Object, Feature Envy, Data Clumps, Duplicate Code**.

**What to look for**
- Long **functions** (> 50 lines) or **types** with too many responsibilities.
- Methods that **poke** more at foreign types than their own (Feature Envy).
- Repeated **parameter groups** (Data Clumps).
- Copy‑pasted logic across files (naive duplicate detection by hashes).
- **Massive View Controllers** should trigger suspicion by default.

**Why it matters**
- Smells correlate with **bug density**, slow velocity, and costly onboarding.

**How to fix**
- Break down via **Extract Method**, **Extract Type**, **Introduce Parameter Object**.
- Apply **Replace Conditional with Polymorphism**; push behavior to data.
- Use **composition** over inheritance for variability.

Tools: `scripts/code_smell_detector.py` + `scripts/complexity_analyzer.py`.

---

## Architectural Violations

**What to look for**
- UI layers (UIKit/SwiftUI) performing **networking** or **persistence** directly.
- Cross‑module imports that **bypass domain boundaries**.
- Tight coupling to external SDKs deep in domain entities.

**Why it matters**
- Breaks testability; increases ripple effect of change; security concerns.

**How to fix**
- Enforce layers: **Presentation → Application → Domain → Infrastructure**.
- Use protocols for **inversion of control**; inject dependencies.
- Validate with `scripts/architecture_validator.py` based on imports and file paths.

---

## SOLID Principles in Swift

- **S**ingle Responsibility: Each type has **one reason to change**.
- **O**pen/Closed: Add via new types, avoid modifying stable code.
- **L**iskov Substitution: Respect substitutability contracts.
- **I**nterface Segregation: Prefer **small protocols**.
- **D**ependency Inversion: Rely on **abstractions**, inject concretions.

Why: Improves modularity and testing; prevents Massive View Controllers.

How: Extract protocols, introduce factories/builders, isolate side effects.

---

## Performance Anti‑Patterns

**What to look for**
- **N+1** queries / excessive iteration over large arrays.
- **Excessive copying** (e.g., value types copied in hot paths).
- **Retain cycles** causing leaks and memory growth.
- **Unnecessary allocations** in tight loops; avoid `DateFormatter` re-creation.

**Why it matters**
- UX, battery life, and stability depend on efficient code.

**How to fix**
- Batch operations, prefetch data, cache pure formatters.
- Use `lazy`, `inout`, and avoid intermediate arrays where possible.
- Profile with Instruments; confirm improvements.

---

## Threading Issues

**What to look for**
- Data races on shared mutable state.
- **Deadlocks** (`DispatchQueue.main.sync` or sync on same serial queue).
- **Priority inversion** due to mismatched QoS or blocking low‑priority work.

**Why it matters**
- Leads to random crashes, hangs, or jank.

**How to fix**
- Prefer **Swift Concurrency** (structured tasks, actors, `Sendable`).
- Keep UI work on main actor; offload heavy compute.
- Avoid sync APIs across queues; eliminate locks where actors suffice.

Tools: `scripts/retain_cycle_detector.py` & `scripts/code_analyzer.py` flags threading hazards.

---

## Force‑Unwrapping Dangers & Optional Handling

**What to look for**
- `!` in production code without airtight invariants.
- `try!` and `as!` that can crash under edge conditions.

**Why it matters**
- Crashes and undefined behavior in rare but real scenarios.

**How to fix**
- Use `guard let`, `if let`, failable initializers, and typed errors.
- Prefer `Result` or throwing APIs and **propagate** errors responsibly.

---

## Error Handling Patterns

- Use `throws` for recoverable errors; map to **user‑visible** states where needed.
- Centralize error mapping and logging; avoid swallowing errors.
- Prefer **typed** error enums at boundaries; log context for diagnostics.

---

## Retain Cycle Detection

**What to look for**
- Escaping closures capturing `self` without `[weak self]` when appropriate.
- Delegates that are `strong` instead of `weak`.
- NotificationCenter/Combine subscriptions not properly cancelled.

**Why it matters**
- Memory growth, leaks, degraded performance.

**How to fix**
- Add capture lists; mark delegates `weak`; cancel in `deinit` / lifecycle.
- Use `scripts/retain_cycle_detector.py` to scan for patterns.

---

## Massive View Controllers

**What to look for**
- View controllers that fetch, parse, validate, layout, and route all at once.

**Why it matters**
- Hinders reuse, testing, and onboarding; slows feature velocity.

**How to fix**
- Extract **ViewModels/Presenters**, **Coordinators/Routers**, and **Workers**.
- Keep VC focused on **binding & interaction**.

---

## Naming Conventions

- Types: **UpperCamelCase**; acronyms like URL/ID stay uppercase as suffixes.
- Methods & vars: **lowerCamelCase**; Boolean predicates start with `is/has/should`.
- Avoid abbreviations unless standardized; be specific and intention‑revealing.

Tools: `scripts/naming_validator.py` validates common patterns.

---

## Documentation Standards (Swift DocC)

- Public APIs must have **DocC** or `///` comments with summary + parameters/returns.
- Modules/features include **tutorials** and **articles** where appropriate.
- Keep **examples** current; docs are reviewed like code.

Tools: `scripts/documentation_checker.py` computes coverage.

---

## API Design Guidelines

- Follow **Swift.org API Design Guidelines**.
- Prefer **clarity at call site**, **use parameter labels** wisely, avoid needless words.
- Mutating vs nonmutating naming; choose **nouns vs verbs** appropriately.

---

## Refactoring Strategies

- **Extract Method / Extract Type**: Reduce long methods and god objects.
- **Introduce Parameter Object**: Eliminate data clumps.
- **Replace Conditional with Polymorphism**: Open/Closed improvements.
- **Move Function / Move Field**: Address Feature Envy.
- **Inline / Decompose Conditional**: Clarify control flow.

Each refactor must be **covered by tests** and verified with Instruments when perf‑sensitive.

---

## Accessibility Violations

**What to look for**
- Missing labels/hints/traits; poor contrast; tiny hit targets.
- Dynamic type not respected; focus order wrong.

**Why it matters**
- Legal/compliance risk and **excludes users**.

**How to fix**
- Add `.accessibilityLabel`, `.accessibilityHint`, `.accessibilityAddTraits`.
- Test with **Accessibility Inspector** and automated audits where possible.

---

## Security Review Patterns

**What to look for**
- ATS disabled or broad exceptions.
- Insecure crypto (MD5/SHA1), custom crypto, hard‑coded secrets.
- Weak Keychain accessibility classes; sensitive data in logs.
- WebViews with arbitrary JS bridges without domain allowlists.

**How to fix**
- Enforce HTTPS via ATS; pin or validate certificates as needed.
- Use **CryptoKit**; store secrets in **Keychain** with restrictive accessibility.
- Remove secrets from code; use configuration and secure storage.
- Harden WebViews (contentMode, scheme allowlists).

Tools: `scripts/security_scanner.py` finds common issues.

---

## Test Coverage Analysis

- Enable Xcode coverage; export with `xccov` JSON for CI ingestion.
- Track **diff coverage** on PRs; focus on **behavior‑changing** code.
- Add **property‑based** tests for pure functions; UI tests cover flows.

Tools: `scripts/test_coverage_analyzer.py` suggests test gaps.

---

## PR Review Process

1. **Triage**: P0/P1 must block merge. P2 may block at reviewer’s discretion. P3 are suggestions.
2. **Scope**: Confirm PR right‑sizing; ask to split if noisy.
3. **Signals**: Linters clean, analyzers passing, tests green, coverage trend up or stable.
4. **Narrative**: Clear description, screenshots/videos for UI, test plan documented.
5. **Follow‑ups**: Track non‑blocking items in issues with owners/dates.

---

## Best Practices & Anti‑Patterns

- ✅ Small PRs; ✅ descriptive names; ✅ early returns; ✅ immutability.
- ❌ Force‑unwraps; ❌ business logic in views; ❌ debug prints; ❌ blocking main thread.

---

## Troubleshooting

- If analyzers produce noise, tune thresholds in `configs/*.yml`.
- If a rule conflicts with code generation, add path‑based ignores.
- Use **whitelisting** for known safe exceptions with justification.

---

## Review Checklists

See `checklists/` for: **general**, **SwiftUI**, **UIKit**, **performance**, **security**,
**accessibility**, **architecture**. Each is concise and copy‑paste ready for PRs.

---

## Graduated Review Levels

- **Junior**: Focus on crashes, force‑unwraps, formatting, obvious smells, test presence.
- **Mid‑level**: Architecture adherence, error handling rigor, concurrency safety.
- **Senior/Staff**: Cross‑cutting concerns (perf/security/accessibility), API design,
  long‑term maintainability, migration paths, and coaching.

---

## Running the Analyzers

```bash
# Run all analyzers on the repository
python3 scripts/code_analyzer.py --path . --out findings.json
python3 scripts/code_smell_detector.py --path . --out smells.json
python3 scripts/complexity_analyzer.py --path . --out complexity.json
python3 scripts/retain_cycle_detector.py --path . --out retains.json
python3 scripts/documentation_checker.py --path . --out docs.json
python3 scripts/naming_validator.py --path . --out names.json
python3 scripts/security_scanner.py --path . --out security.json
python3 scripts/test_coverage_analyzer.py --coverage coverage.json --out coverage_findings.json
python3 scripts/architecture_validator.py --path . --out arch.json
```

Aggregate results in CI, fail on **P0/P1**.

---

## Swift Analysis Examples

See `examples/good` and `examples/bad` for **before/after** refactors: retain cycles, naming,
security (ATS), performance (N+1), threading, documentation, and Massive View Controllers.

---

## Integration Notes

- Place this Skill under **`.claude/skills/code-reviewer-guardian/`** in your repo (project Skill),
  or in **`~/.claude/skills/`** (personal Skill).  
- In Claude Code, `allowed-tools` here limits tool use when this Skill is active.  
- In the **Agent SDK**, enable Skills via settings (`setting_sources`) and allow the `"Skill"` tool.

---

## License

MIT for the analyzers & templates. Adapt to your org’s policy as needed.
