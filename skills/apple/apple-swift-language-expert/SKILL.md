---
name: apple-swift-language-expert
user-invocable: false
description: >
  Use when the task is about Swift language semantics or version-sensitive language features rather than app architecture, especially Swift 5.9 through Swift 6.x migrations, macros, ownership, generics, typed throws, Sendable, actors, or strict concurrency changes. Also use when the user asks what changed in a recent Swift release, whether a Swift Evolution proposal is implemented yet, or needs Swift guidance that must be checked against the current toolchain before answering.
version: 2.0.0
tags:
  - swift
  - concurrency
  - actors
  - sendable
  - macros
  - generics
  - typed-throws
  - ownership
  - performance
  - swift-6
---

# apple‑swift‑language‑expert

Swift moves faster than almost any other Apple technology.  
**Version numbers tick quarterly** and the language steering group regularly accepts new proposals.  
This skill equips Claude to act as a senior Swift engineer **only if it stays current**.  
Therefore, the number one rule is **never assume the language version**—**always check it**.

## ⚠️ CRITICAL: Swift Version Awareness

Swift’s concurrency model, macro system and type system have changed dramatically across 5.9→6.2.  
Giving advice based on stale assumptions can break a user’s project.  

### Mandatory: Verify the Current Swift Version **before suggesting anything**

1. **Discover the user’s toolchain:** run `swift --version` or use the `xcodebuild -version` command.  
   Alternatively, ask the user which Xcode version they’re using.  New Xcode releases often bump the Swift minor version.  
2. **Perform targeted searches** using this skill’s built‑in web search macro or manual research.  For example: 
   * `web_search("Swift current version 2025")`
   * `web_search("Xcode <version> Swift version")` (replace `<version>` with the user’s Xcode version)
   * `web_search("Swift Evolution proposals implemented <current year>")`
   * `web_search("Swift <version> release notes")`
3. **Check Swift Evolution:** list accepted and implemented proposals using the official dashboard or community summaries.  The README of `swift-evolution` explains that each release (6.0, 6.1, 6.2) has its own announcement and proposals【419488574665770†L14-L26】.  
4. **Update this skill’s feature matrix**—the matrix below marks unknown cells with `?`.  **If the user’s version is newer than this skill**, stop, search, and update the matrix before giving concrete advice.

> **Last verified:** 2025‑10‑28 using Swift 6.2 release notes and Swift Evolution summaries.  
> **Next mandatory update:** after Swift 7 announcement (likely WWDC 2025).

### When Users Ask…

– “What’s new in Swift 6.2?” → Search release notes and highlight new concurrency and performance features【117116631220052†L34-L85】【117116631220052†L87-L112】.  
– “How do I migrate to Swift 6?” → Follow the migration checklist in this skill and consult the official migration guide【552176114195062†L120-L162】.  
– “Does SE‑0436 work yet?” → Search `"Swift Evolution SE-0436 status"` to confirm the implementation status【710982694019516†L41-L103】.  
– “What is `@concurrent`?” → Look up Swift 6.2 approachable concurrency documentation and verify syntax【117116631220052†L34-L85】.

If the user’s Swift version is **newer** than anything documented here, **pause** and verify all APIs.  Do **not** rely on training data alone.

## Swift Evolution Tracking

Swift Evolution proposals define the language.  Always check the current state:

1. **Proposals page:** browse the [swift‑evolution dashboard](https://github.com/apple/swift-evolution) and filter by *Accepted* and *Implemented*.  The Swift 6 announcement notes that a complete list of implemented proposals can be found on the dashboard【370919858884139†L193-L205】.  
2. **Recent proposals:** search for proposals accepted in the current year, e.g., `web_search("Swift Evolution proposals accepted 2025")`.  Summaries on community sites like Fline Dev compile accepted proposals (e.g., SE‑0438 metatype keypaths, SE‑0439 trailing commas)【710982694019516†L41-L103】.  
3. **Breaking changes:** search `web_search("Swift <version> breaking changes")` before suggesting a migration.  Swift 6 introduced strict concurrency and typed throws【552176114195062†L120-L162】, while Swift 6.2 relaxed some isolation requirements【733986796193328†L42-L64】.
4. **Proposal status quick check:** statuses are typically *Implemented*, *Accepted* (coming soon), *Active Review*, or *Rejected*.  Only use *Implemented* features; treat *Accepted* features as unstable.

### Evolution Proposals to Watch (2024–2025)

Recent accepted and implemented proposals include:

| SE Number | Description | Notes |
|---------|-----------|------|
| **SE‑0436** | **Objective‑C implementations in Swift** — allows `@objc @implementation` extensions to implement Objective‑C class methods in Swift【710982694019516†L41-L103】 | Implemented in Swift 6.1. Useful for mixed Objective‑C projects. |
| **SE‑0438** | **Metatype key paths** — static property key paths like `\.type`【710982694019516†L41-L103】 | Implemented in Swift 6.1. |
| **SE‑0439** | **Extended trailing comma support** — allows trailing commas in more contexts【710982694019516†L41-L103】 | Implemented in Swift 6.1. |
| **SE‑0443** | **Warning control flags** — fine‑grained compiler warning controls【710982694019516†L41-L103】 | Implemented in Swift 6.1 and refined in Swift 6.2. |
| **SE‑0444** | **Member import visibility** — imports must explicitly opt into members【710982694019516†L169-L233】 | Implemented in Swift 6.1. |
| **SE‑0446** | **Nonescapable types** — introduces nonescapable (`~Copyable`) types for unique ownership【370919858884139†L110-L134】 | Implemented in Swift 6.0 with improvements in later releases. |
| **SE‑0447** | **`Span` safe contiguous storage** — provides `Span` and `InlineArray` types for low‑level programming【117116631220052†L87-L112】 | Implemented in Swift 6.2 for safe systems code. |
| **SE‑0448** | **Regex look‑behind assertions** — enhancements to the regex engine【710982694019516†L169-L233】 | Implemented in Swift 6.1. |
| **SE‑0449** | **Limit implicit global actor inference** — `nonisolated` prevents accidental inference【710982694019516†L169-L233】 | Implemented in Swift 6.1. |
| **SE‑0450** (hypothetical) | *Check current proposals.* | If the user asks about SE‑0450, search first. |

Keep this table updated as new proposals land.

## Swift Version Feature Matrix

This matrix summarises core features across Swift 5.9–6.2.  **Cells marked `?` require verification via search**.  Use this table to determine if a feature is available in the user’s toolchain.

| Feature / Topic | Swift 5.9 | Swift 6.0 | Swift 6.1 | Swift 6.2 | Verify |
|---|---|---|---|---|---|
| **Strict concurrency mode** | Available as warnings via `-strict-concurrency=complete`【552176114195062†L120-L162】 | Default for Swift 6 language mode; warnings become errors【552176114195062†L120-L162】 | Improved `nonisolated` inference and fewer false positives【12387186911315†L21-L62】 | Single‑threaded mode introduced; `async` functions run in caller context; `@concurrent` attribute available【117116631220052†L34-L85】 | Search for changes in future releases |
| **Typed throws** | No | Introduced in Swift 6; functions can specify the error type thrown【370919858884139†L64-L94】 | Same | Same | Ensure syntax hasn’t changed |
| **Noncopyable (`~Copyable`) types** | Preview (SE‑0429) in 5.9 | Supported generically; used by new Synchronization library【370919858884139†L110-L144】 | Same | Same | Confirm improvements |
| **Region‑based isolation** | Experimental (SE‑0414) with `sending` semantics | Part of Swift 6 strict concurrency; warnings | Improved diagnostics and `nonisolated` to types【12387186911315†L21-L62】 | Relaxed rules for common patterns; `nonisolated(nonsending)` reduces friction【733986796193328†L42-L64】 | Check new defaults |
| **Macro system** | Introduced (5.9) with freestanding and attached macros; @Observable and custom macros available【691042557916549†L36-L107】 | Enhanced with typed macro roles, `#assert` etc.; macros can be used as default arguments (SE‑0422)【900005069537335†L185-L205】 | Build‑time improvements via prebuilt swift‑syntax; new `@implementation` macro for Objective‑C bridging; `@DebugDescription` macro for LLDB【12387186911315†L61-L83】【370919858884139†L209-L233】 | Support for streaming observation via `Observations` AsyncSequence【850874383909912†L286-L310】 and macros in Swift Testing | Verify new macro roles, e.g., `@attached(body)` |
| **Synchronization library & `Atomic`** | Not available | Introduced: low‑level atomic operations and mutex API (SE‑04xx)【370919858884139†L61-L64】 | Same | Same | Check for API additions |
| **InlineArray & Span** | No | No | No | Added in 6.2; safe low‑level contiguous storage【117116631220052†L87-L112】 | Verify improvements |
| **Pack iteration & value parameter packs** | Preview (Swift 5.9) | Available; `for` loops over parameter packs【370919858884139†L193-L205】 | Same | Same | Confirm syntax |
| **Debugging macros & explicit modules** | Not available | `@DebugDescription` macro introduced in Swift 6【370919858884139†L209-L233】 | Same | Same; explicit modules improve LLDB startup【370919858884139†L254-L264】 | Check for enhancements |
| **Foundation unified implementation** | OS‑specific | Unified cross‑platform implementation introduced in Swift 6【370919858884139†L266-L284】 | Same | Same | Check for new APIs |

### How to Use This Matrix

1. Determine the user’s Swift version (major + minor).  
2. Consult the row for the relevant feature.  If the cell is marked with `?` or contains outdated information, perform a web search before making recommendations.  
3. Update the matrix as part of maintaining this skill.

## Overview

Modern Swift rests on three evolving pillars:

1. **Concurrency & Isolation** — tasks and actors provide structured concurrency, but the rules around isolation and sendability have tightened.  Swift 6 made strict concurrency the default, and Swift 6.2 introduces *approachable concurrency* where `async` functions run in the caller’s context by default【117116631220052†L34-L85】.  Migration requires careful auditing of `@Sendable` closures and the new `sending` ownership model.
2. **Ownership & Types** — the type system continues to expand with noncopyable (`~Copyable`) types, parameter packs, and typed throws.  These features enable performance‑conscious code and better error propagation【370919858884139†L110-L144】.  Swift 6 also unified Foundation across platforms【370919858884139†L266-L284】.
3. **Compile‑time Metaprogramming** — macros, result builders and property wrappers allow generation of boilerplate and compile‑time diagnostics.  Swift 6 adds new macro roles, including `@DebugDescription` and macros for testing, and pre‑built swift‑syntax reduces build times【850874383909912†L170-L188】.

This skill covers these pillars with an emphasis on their **current state**.  Older patterns (e.g., `DispatchQueue`, callback‑based APIs) are contrasted with modern idioms.  All examples include **version tags** so you can see which features require Swift 6 or 6.2.

## When to Use

– **Migrating to Swift 6 or 6.2** — Use this skill to plan and execute a migration from Swift 5.9, including enabling strict concurrency gradually and addressing new compiler errors【198246060894125†L17-L32】.  
– **Implementing concurrency** — Choose between `async let` and `TaskGroup` for parallelism, apply `nonisolated` judiciously, and design actors that tolerate reentrancy.  
– **Exploring macros** — Learn how to write and use macros, including `@Observable`, `@Test` and `@DebugDescription` macros, and verify which roles are available in your Swift version【691042557916549†L36-L107】.  
– **Designing generic APIs** — Decide between generics/`some` and `any` existentials based on performance and dynamic requirements.  
– **Tuning performance** — Use value types, `Span` and `InlineArray` for memory‑safe speed, and profile to eliminate unnecessary allocations and exclusivity checks【167601622601565†L92-L103】.

## Concurrency & Isolation (Updated for Swift 6.2)

### Mental Model

Swift’s concurrency model is task‑oriented. A *task* executes asynchronous work.  Tasks form a tree (structured concurrency); cancellation flows from parent to children.  Suspension points (`await`) allow other tasks to interleave.  Actors serialize access to their state, while executors schedule work.  Strict concurrency mode introduces `sending` semantics and region‑based isolation to prevent data races.

### Version‑Specific Notes

**Swift 5.9** — Introduced structured concurrency and actors with opt‑in strict concurrency warnings.  `@TaskLocal` carried task‑local values.  `nonisolated` could only apply to functions and properties.

**Swift 6.0** — Strict concurrency becomes the default language mode.  Typed throws, noncopyable types, and low‑level synchronization APIs are introduced.  Data‑race safety warnings become errors【552176114195062†L120-L162】.  Migration requires enabling the Swift 6 mode and resolving `Sendable` and isolation errors【552176114195062†L120-L162】.

**Swift 6.1** — Extends `nonisolated` to **types and extensions**, allowing you to mark an entire type as nonisolated【12387186911315†L21-L62】.  The compiler infers `withTaskGroup` result types, reducing the need to specify `of: Element.self`【12387186911315†L61-L83】.  Trailing comma support and better warning controls reduce friction.

**Swift 6.2** — Introduces **approachable concurrency**: `async` functions no longer hop to a global actor by default but run in the caller’s context.  A new `@concurrent` attribute expresses that an async function may execute concurrently with its caller【117116631220052†L34-L85】.  Swift 6.2 also relaxes region‑based isolation rules (e.g., `nonisolated(nonsending)`) to reduce unnecessary errors【733986796193328†L42-L64】.  Concurrency debugging improves via named tasks and better LLDB integration【850874383909912†L214-L225】.

### Patterns

* **`async let`** — Spawn a fixed number of child tasks.  Must be awaited before leaving the scope.  Suitable for simple parallelism.  Available since Swift 5.5.
* **`withTaskGroup` / `withThrowingTaskGroup`** — Spawn a dynamic number of tasks.  In Swift 6.1 the compiler infers the result type【12387186911315†L61-L83】.  Cancel child tasks promptly when the result is known.
* **Actors** — Use `actor` to protect mutable state.  Mark pure functions as `nonisolated` when they don’t access actor state.  In Swift 6.1 you can mark entire types or extensions as `nonisolated`【12387186911315†L21-L62】.  Use `MainActor` for UI‑bound types.
* **Region‑Based Isolation & `sending`** — Region‑based isolation (SE‑0414) models ownership transfer across concurrency boundaries.  When passing a value to a `@Sendable` closure, ensure it conforms to `Sendable` or mark the closure `@unchecked Sendable` with care.  Swift 6.2 introduces `nonisolated(nonsending)` to indicate that an async method neither hops actors nor transfers ownership【733986796193328†L42-L64】.
* **Task Locals** — Use `@TaskLocal` to store contextual values (trace IDs, locale) that propagate through child tasks.

### Concurrency Migration Checklist

1. **Inventory your codebase** — Identify concurrency hotspots.  Tools like the provided `concurrency_analyzer.py` (see `scripts/`) can scan Swift files for potential data races.
2. **Enable strict concurrency as warnings** — In Swift 5.x, set `SWIFT_STRICT_CONCURRENCY=complete` to see potential issues without breaking the build【552176114195062†L120-L162】.
3. **Resolve `Sendable` warnings** — Annotate types as `Sendable` where appropriate or redesign APIs to avoid capturing mutable state【101147520668621†L123-L140】.  Use actors to protect shared mutable state or adopt value semantics.
4. **Gradually switch to the Swift 6 language mode** — After addressing warnings, change the Swift language version in your project settings.  Expect errors for remaining issues; fix them iteratively【198246060894125†L17-L32】.
5. **Adopt approachable concurrency features** — If using Swift 6.2, determine where the new `defaultIsolation` semantics simplify your code.  Consider adding `@concurrent` or `@MainActor` annotations where explicit cross‑actor execution is required.

## Ownership, Generics & Existentials

Swift 6 expands the type system with **typed throws**, **noncopyable types**, and **parameter packs**.

### Typed throws

Functions can now specify the exact type of error they throw: `throws(ErrorType)`【370919858884139†L64-L94】.  This allows the compiler to infer error types in `do/catch` blocks and generic code.  Use typed throws to reduce boilerplate and make APIs more predictable.  A non‑throwing function is equivalent to `throws(Never)`, and an untyped `throws` is equivalent to `throws(any Error)`【370919858884139†L87-L93】.

### Noncopyable (`~Copyable`) types & Ownership

Swift 5.9 previewed noncopyable types; Swift 6 makes them fully generic【370919858884139†L110-L144】.  Types annotated with `~Copyable` cannot be implicitly copied, enabling efficient use of resources.  Use noncopyable types for unique resources (file handles, network streams) and consider the new `Atomic` type in the Synchronization library for low‑level concurrency.  Switch statements can now avoid copying when pattern‑matching enums containing noncopyable payloads【370919858884139†L138-L142】.

### Parameter packs & pack iteration

Parameter packs allow functions and types to accept an arbitrary number of generic parameters.  Swift 6 introduces `for` loops over parameter packs (pack iteration)【370919858884139†L193-L205】.  Use packs to build variadic generic APIs without resorting to tuples.

### Generics vs. Existentials

Use **generics** (`some P`) when you need call‑site specialization and zero‑cost abstractions.  Use **existentials** (`any P`) for true heterogeneity or when dynamic dispatch is acceptable.  Protocols with `associatedtype` or `Self` cannot be used as existentials—either use generics or provide type erasers.  Primary associated types improve expressiveness by allowing the compiler to infer associated types from context.

## Compile‑time Metaprogramming: Macros & Builders

Swift’s macro system allows code generation and compile‑time diagnostics.  Always verify the available macro roles and macro packages for the current Swift version.

### Macro Roles (Swift 6.2)

Macros come in two categories:

* **Freestanding macros** (e.g., `#URL`, `#assert`) generate code or diagnostics at the call site.  SE‑0422 introduced expression macros as caller‑side default arguments【900005069537335†L185-L205】.
* **Attached macros** (e.g., `@Observable`, `@Test`, `@DebugDescription`) attach to declarations and augment them.  Roles include `@attached(peer)`, `@attached(accessor)`, `@attached(memberAttribute)`, `@attached(member)`, `@attached(conformance)`, and new in Swift 6: `@attached(body)` for synthesizing function bodies【370919858884139†L193-L205】.  

### Built‑in Macros

* **`@Observable`** — opt a class into observation tracking.  Swift 6.2 introduces an `Observations` type that streams state changes via an `AsyncSequence`【850874383909912†L286-L310】.  Updates are transactional: synchronous changes to multiple properties are combined into a single value【850874383909912†L298-L303】.
* **`@Test` and Swift Testing** — Swift 6 includes the **Swift Testing** library, offering expressive macros like `@Test`, `#expect`, and exit tests.  Custom attachments allow recording data to diagnose failures【850874383909912†L313-L337】.
* **`@DebugDescription`** — new macro to provide LLDB summaries for your types【370919858884139†L209-L233】.

### Writing Custom Macros

To implement a macro, create a Swift package with an **exploration library**, a **compiler plugin**, and tests.  Macros use SwiftSyntax to transform the abstract syntax tree.  Roles such as `@freestanding(expression)` or `@attached(member)` determine how the macro interacts with user code【691042557916549†L86-L107】.  Testing macros is crucial—use packages like MacroTesting or the built‑in `#assert` to validate expansions.  Because macros rely on the SwiftSyntax package, performance can suffer; Swift 6.2 supports pre‑built swift‑syntax libraries to significantly reduce clean build times【850874383909912†L173-L185】.

### Macro Troubleshooting

* **Build fails with missing SwiftSyntax** — Ensure your macro package depends on a tagged swift‑syntax release, allowing Xcode and SwiftPM to download pre‑built binaries【850874383909912†L183-L189】.
* **Macro doesn’t expand** — Check that the correct role is declared and that your macro module is imported.  Use `swift‑build -Xfrontend -debug‑expand‑macro` to debug expansions.
* **LLDB doesn’t display custom descriptions** — Ensure the type conforms to `CustomDebugStringConvertible` and apply the `@DebugDescription` macro【370919858884139†L209-L233】.

## Memory Management & Performance (Swift 6.2)

Swift’s ARC remains the backbone of memory management, but new tools help you write high‑performance code:

* **InlineArray & Span** — Swift 6.2 adds `InlineArray` and `Span` types for safe contiguous storage【117116631220052†L87-L112】.  Use `InlineArray` for fixed‑size arrays stored inline without heap allocation; use `Span` to borrow slices of memory without copying.  These types are ideal for embedded systems and performance‑critical code.
* **Exclusivity & Eliminating Retains** — Performance sessions from WWDC25 recommend eliminating unnecessary exclusivity checks and reference counting operations.  Identify hot paths with Instruments and convert heap allocations to stack allocations where possible【167601622601565†L92-L103】.
* **Synchronization Library & `Atomic`** — For low‑level concurrency, the new Synchronization library provides atomic types and mutexes【370919858884139†L61-L64】.  Use them sparingly; prefer high‑level abstractions like actors where possible.
* **Typed throws & Noncopyable Types** — Reducing error overhead and avoiding unnecessary copies can improve performance.  For example, typed throws avoid dynamic casting of errors【370919858884139†L64-L94】.

## Best Practices (2025)

* **Version‑aware advice** — Always confirm the user’s Swift version and consult release notes before recommending a feature.
* **Structured concurrency first** — Prefer `async let` and `TaskGroup` over unstructured `Task {}`; coalesce actor calls to reduce cross‑actor hops.  Name your tasks and use Instruments to profile concurrency【850874383909912†L214-L225】.
* **Balance isolation and pragmatism** — Avoid blanket `nonisolated(unsafe)`; instead, refactor data ownership or use `nonisolated(nonsending)` where appropriate【733986796193328†L42-L64】.
* **Design macros with diagnostics** — Provide clear error messages and fix‑its when writing custom macros.  Test macro expansions thoroughly.
* **Value semantics & `Span`** — Choose structs and value types for thread‑safe sharing; use `Span` for borrowed memory regions【117116631220052†L87-L112】.
* **Use typed throws and primary associated types** to improve error handling and generic code readability【370919858884139†L64-L94】.

## Anti‑Patterns

* **Ignoring version differences** — Don’t assume Swift 6.0 code works the same in 6.2.  Changes in concurrency semantics can introduce subtle bugs.
* **Fire‑and‑forget `Task {}`** — Unstructured tasks complicate ownership and cancellation.  Use structured concurrency instead.
* **Using `any` by default** — Existentials introduce indirection; prefer generics and `some` for performance‑critical APIs.
* **Excessive `nonisolated(unsafe)`** — Overusing unsafe annotations defeats the purpose of strict concurrency.  Use actors or `nonisolated(nonsending)` properly【733986796193328†L42-L64】.
* **Heavy work in result builders or macros** — Result builder phases should be pure; macros should avoid expensive compile‑time work.  Precompute heavy data where possible.

## Troubleshooting & Common Diagnostics

* **“actor‑isolated property used from a non‑isolated context”** → Either mark the calling context `@MainActor`/`nonisolated`, or access the property via `await` when crossing actors.
* **“non‑Sendable type captured in `@Sendable` closure”** → Redesign the API to use value types or actors; consider marking the closure `@unchecked Sendable` only after careful analysis【101147520668621†L123-L140】.
* **“Passing closure as a ‘sending’ parameter risks data races”** → Audit region‑based isolation; perhaps adopt `nonisolated(nonsending)` or restructure the code to avoid transfers.
* **“Type ‘any P’ cannot conform to ‘P’”** → You used an existential where a protocol with `Self` or `associatedtype` is required.  Use generics or type erasure.
* **Macro build failures** → Ensure swift‑syntax is prebuilt and your macro’s dependencies are tagged【850874383909912†L173-L185】.

## Migration Guide (5.9 → 6.x → 6.2)

1. **Upgrade toolchains** — Install the latest Swift toolchain (Swift 6.2) using Xcode or `swiftly`.  Use `swiftly` to manage multiple toolchains【850874383909912†L117-L129】.
2. **Enable warnings** — In Swift 5.x projects, set `SWIFT_STRICT_CONCURRENCY=complete` to surface data‑race issues without breaking the build【552176114195062†L120-L162】.
3. **Refactor for Sendability** — Convert shared mutable state to value types or actors; annotate types with `Sendable`.  Use `@preconcurrency` to annotate legacy APIs that are not yet sendable.
4. **Adopt typed throws** — Update function signatures to specify error types when possible.  Propagate error types in generic code.
5. **Evaluate macros** — Replace boilerplate (e.g., observation, testing) with macros.  For example, convert `ObservableObject` classes to use `@Observable` and `Observations` streaming【850874383909912†L286-L310】.
6. **Explore `Span` and `InlineArray`** — For performance‑sensitive or embedded code, refactor arrays to use these new types【117116631220052†L87-L112】.
7. **Incrementally move to Swift 6 language mode** — After addressing warnings, set the Swift Language Version to “6.0”, then to “6.2” once your code compiles.  Test thoroughly and profile for performance regressions.
8. **Keep learning** — Monitor the Swift Evolution proposals page for new changes and update this skill accordingly.

## Helper Scripts (`scripts/`)

The `scripts/` directory contains tools to aid migration and verification.  Highlights include:

* `check_swift_version.py` — Runs `swift --version` and compares the installed version to this skill’s baseline.  It warns if the toolchain is older than documented and reminds you to consult the feature matrix.  Use it before asking this skill for advice.
* `evolution_tracker.py` — Fetches the latest Swift Evolution proposals from GitHub and summarises their statuses.  Use it to update the evolution table above.  If network access fails, the script prints instructions for manual verification.
* `concurrency_analyzer.py` — Scans Swift source files for potential data races and highlights non‑Sendable captures (unchanged from previous version).  Useful during migration.
* `modernization_suggester.py` — Suggests replacing callbacks and `DispatchQueue` calls with structured concurrency (unchanged from previous version).
* `generic_validator.py`, `memory_leak_detector.py`, `macro_generator.py` — Additional helpers from the prior version remain available.  Consider updating them to handle new macros and typed throws.

Refer to each script’s documentation comments for usage.

## License & Notes

The examples and scripts in this skill are provided under the MIT license.  This skill is structured like Anthropic Agent Skills with YAML frontmatter, comprehensive Markdown documentation, helper scripts, and runnable code samples.  **Because Swift evolves quickly, maintainers must update this skill quarterly**.

---

© 2025, updated for Swift 6.2.  See citations for sources and always verify before using.
