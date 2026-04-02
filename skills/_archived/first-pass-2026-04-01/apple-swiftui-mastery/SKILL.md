---
name: apple-swiftui-mastery
user-invocable: false
description: |-
  Use when the user needs help writing, understanding, debugging, or refactoring SwiftUI for iOS or macOS, especially around state management, layout systems, navigation, animations, accessibility, performance, or newer SwiftUI APIs. Also use for requests mentioning SwiftUI, the Layout protocol, view update behavior, navigation stacks, or related declarative UI concerns across iOS 17 through iOS 26.
version: 1.0.0
tags: [swiftui, ios, macos, ui, layout, state-management, navigation, animation, performance]
---

## Overview

SwiftUI is Apple’s modern declarative UI framework for building user interfaces across iOS, macOS, watchOS and tvOS.  Instead of imperative view controllers and manual layout code, developers describe their UI as a function of **state**, and SwiftUI figures out how to update the screen when that state changes.  This skill teaches Claude how to generate and critique SwiftUI code like a senior engineer, incorporate the latest platform features, and avoid common traps.  It emphasises the importance of naming conventions, progressive disclosure and clear descriptions when authoring skills—principles drawn from Anthropic’s own skill guidelines【664623278056752†L369-L399】【664623278056752†L404-L420】.

### Progressive Disclosure and Structure

This skill uses a progressive disclosure pattern to keep the `SKILL.md` file readable while still providing exhaustive details.  Each major topic links to a dedicated document under the `docs/` directory.  Scripts that generate or analyse code live in the `scripts/` directory, while real‑world examples sit in the `swift/` directory.  By splitting the content into separate files the skill remains under the recommended 500‑line limit【664623278056752†L464-L471】.  The YAML frontmatter above specifies the name, description, version and tags fields as required by Anthropic’s skill metadata guidelines【664623278056752†L1462-L1468】.

## When to Use This Skill

Invoke this skill whenever a user asks to:

* Understand or implement a SwiftUI view, component or layout.
* Compare property wrappers or state management strategies (`@State`, `@StateObject`, `@ObservedObject`, `@EnvironmentObject`, `@Binding`, or the new `@Observable` macro).
* Build navigation stacks, deep linking or complex navigation architectures.
* Create custom layouts, grids, shapes, animations, transitions or matched geometry effects.
* Optimise view performance, reduce unnecessary updates, or troubleshoot view update cycles.
* Integrate accessibility and dynamic type correctly.
* Explore new features introduced in iOS 17 through iOS 26, such as the Observation framework or advanced detents.

## SwiftUI Fundamentals

SwiftUI views are lightweight value types that conform to the `View` protocol.  Each view describes its body—another view—forming a tree.  Because views are simple structs, the system can recreate them cheaply whenever state changes.  SwiftUI computes a diff between the previous and new view tree and updates only what changed.  This structural identity is critical: two view instances of the same type in the same position represent the *same* identity, whereas different branches or conditionally created types produce distinct identities【152934397403680†L392-L406】.  For clarity on identity and how it affects transitions, see the View Identity & Stability section.

State drives the UI.  When you mutate a piece of state, SwiftUI re‑invokes the view’s `body`.  You shouldn’t directly compare or store views—treat them as transient descriptions.  Instead, rely on property wrappers (see below) and environment values to manage data flow.

## View Protocol & `body`

Every SwiftUI type that appears on screen conforms to the `View` protocol and implements a computed `var body: some View` property.  `some View` is an opaque return type indicating that the body returns a single view (possibly composed of many subviews).  The body must not perform expensive work; avoid network requests or heavy computations here.  Instead, use asynchronous tasks or separate model layers.

### ViewBuilder Deep Dive

The `@ViewBuilder` attribute powers the declarative syntax that allows multiple children in a `body` or closures like `NavigationStack { ... }`.  A `ViewBuilder` collects up to 10 child views and wraps them into a single `TupleView` or `AnyView`.  Use explicit `Group` or `AnyView` to exceed the 10‑view limit or when returning heterogeneous branches.  Remember that `if` and `switch` statements inside a `@ViewBuilder` can create distinct structural identities for each branch, which influences animations and transitions【152934397403680†L510-L567】.

## State Management

SwiftUI offers several property wrappers to manage state across the view hierarchy.  Choose the right wrapper depending on where the source of truth lives and how many views consume it.

### `@State`

Use `@State` to declare simple value types that belong to a single view.  When the state changes, the view redraws.  Because the storage lives in the view’s lifetime, the property persists across re‑evaluations of `body`.  Don’t pass `@State` values down directly; instead, expose a `Binding`.

### `@Binding`

A binding is a two‑way reference into a piece of state.  It allows child views to read and write state owned by an ancestor.  Use `$` prefix to derive a binding from `@State` or other bindings.  Avoid passing mutable bindings too deep; consider `@EnvironmentObject` for global state.

### `@StateObject` vs `@ObservedObject`

Both wrappers subscribe to an `ObservableObject` and refresh the view when the object’s `@Published` properties change.  The key difference is lifetime: `@StateObject` *creates* and owns the model, ensuring it persists across view re‑creations, while `@ObservedObject` expects the model to be supplied from the parent.  Recreating the model inside a view with `@ObservedObject` causes it to reset; using `@StateObject` ensures stable identity【185021888277737†L38-L65】【185021888277737†L154-L156】.

### `@Environment` & `@EnvironmentObject`

Environment values propagate contextual information down the hierarchy.  Use `@Environment` to read system values such as locale, color scheme, dynamic type sizes, or your own custom `EnvironmentKey`s.  `@EnvironmentObject` injects shared models into the environment.  When the object changes, all subscribed views update automatically.  This is ideal for global app state but be mindful of overusing it—it can obscure data flow.

### Observation Framework: `@Observable` (iOS 17+)

Apple introduced the `@Observable` macro in iOS 17 to simplify building observable models.  Mark a class with `@Observable` to automatically synthesise object willChange notifications.  Combine this with `@State` or `@Environment` to create a source of truth at the application or view level【228322540172834†L38-L83】【228322540172834†L90-L102】.  Observed fields update SwiftUI views without manual `@Published` annotations.

For more on state patterns and edge cases—including combining property wrappers, using computed bindings, and avoiding value type mutation—see `docs/state-management-guide.md`.

## Layout Systems

SwiftUI layouts are declarative.  Use built‑in stacks (`HStack`, `VStack`, `ZStack`) and grids (`LazyVGrid`, `LazyHGrid`, `Grid`) to arrange views.  Grids lazily create cells and are ideal for large data sets.  Use `LazyVStack` and `LazyHStack` when you want the benefits of a `List` but with custom styling.

The new `Layout` protocol allows you to define completely custom layouts by implementing two methods: `sizeThatFits(_ proposed: ProposedViewSize, subviews: ViewSubviews, cache: inout Cache?) -> CGSize` to compute the container size, and `placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: ViewSubviews, cache: inout Cache?)` to position each subview【540782554707304†L21-L43】.  This offers full control over how children are measured and placed.  See `docs/layout-deep-dive.md` for examples of flow layouts, tag clouds and flexible grids.

### GeometryReader

`GeometryReader` exposes the size and coordinate space of the containing view.  Use it when you need adaptive layouts or dynamic positioning.  Be cautious: a `GeometryReader` takes up the **entire available space** unless constrained.  Limit its footprint by wrapping it in a `frame` or using an overlay/background【45585243622685†L37-L46】.  If you just need to draw shapes based on size, prefer the `Shape` API rather than `GeometryReader`【45585243622685†L73-L86】.  More patterns and anti‑patterns are discussed in `docs/layout-deep-dive.md`.

### PreferenceKey and Anchors

Preferences allow child views to send information up the view hierarchy.  Apple explains: “Whereas you use the environment to configure the subviews of a view, you use preferences to send configuration information from subviews toward their container”【233209377127931†L30-L58】.  You define a `PreferenceKey` with a default value and a reduce function, then emit preferences in child views and read them using `.onPreferenceChange`.  This pattern is essential for measuring child sizes, aligning cross‑siblings, or implementing custom navigational titles.  Anchors complement this by letting you refer to specific coordinates within a view for alignment.

## View Identity & Stability

SwiftUI relies on **structural identity** to determine whether a view is the same across updates.  If the type and position are unchanged, SwiftUI considers it the same view and can animate property changes.  When you conditionally switch between two different view types (e.g., `Image` vs `Text`), they have different structural identities; transitions may behave unexpectedly【152934397403680†L510-L567】.  To preserve identity, wrap branches in an `AnyView` or `Group`, or provide an explicit `.id()` value.  You can also use `id(_:)` on data in `ForEach` to disambiguate repeated elements.  For more examples of identity issues, refer to `swift/view_identity_examples.swift`.

## Animations and Transitions

SwiftUI animates changes automatically when you wrap state mutations in `withAnimation { ... }`.  Animations are values describing timing curves (e.g., `.easeInOut`, `.spring(response:dampingFraction:)`).  Use `.animation(_: value:)` on views to animate a specific value without wrapping logic.  Transitions define how views appear and disappear—`opacity`, `slide`, `scale`, `move`, etc.—and you can combine them with `.transition()`.  `matchedGeometryEffect(id:in:isSource:)` synchronises the geometry of multiple views for seamless animations【257252862286697†L30-L43】【257252862286697†L100-L124】.  See `docs/animation-patterns.md` for advanced spring curves, keyframe animations, and timeline‑based effects.

### TimelineView & Canvas

`TimelineView` lets you drive view updates based on a schedule rather than state changes.  Use built‑in schedules like `.everyMinute` or `.animation` for smooth, time‑based animations【871986411204682†L23-L49】.  Combine `TimelineView` with `Canvas` to perform immediate‑mode drawing using a `GraphicsContext`【429239476571212†L23-L50】.  `Canvas` can draw shapes, gradients, text, and images, and can be animated by `TimelineView`【429239476571212†L90-L110】.  Example code lives in `swift/canvas_examples.swift`.

## Custom View Modifiers

Create your own view modifiers to encapsulate styling or behaviours across many views.  A struct conforming to `ViewModifier` defines a `body(content:)` method that receives the current view and returns a modified view.  Parameterise your modifiers to allow configuration, and chain them via `.modifier(MyModifier(param: value))`.  When creating property wrappers or environment keys, pair them with modifiers for a consistent API.  The `scripts/modifier_generator.py` script can scaffold a new modifier file automatically.

## Custom Shapes & Paths

The `Shape` protocol is ideal for drawing vector graphics.  Implement the `path(in:) -> Path` method to draw lines, curves and arcs.  Use `inset(by:)` to adjust the drawing rect, and combine shapes via `.offset()`, `.rotation()`, `.trim()`, and `.strokeBorder()`.  For more complex scenes or pixel‑level control, use the `Canvas` API.  See `swift/custom_shapes.swift` and `swift/canvas_examples.swift`.

## SwiftUI Lifecycle and View Lifecycle Methods

Views are transient, but you can hook into their lifecycle using modifiers: `.onAppear` runs when a view becomes visible, `.onDisappear` when it leaves.  New in iOS 15+, `.task` attaches an async context to a view.  Use `.task(id:)` to cancel and restart tasks when dependencies change.  Avoid heavy side effects in `init()` or `body`; instead, schedule them in tasks or dedicated models.  See `docs/view-lifecycle.md` for more details.

## Navigation Patterns

`NavigationStack` and `NavigationSplitView` replace the older `NavigationView`.  Use a binding to a `NavigationPath` to programmatically push and pop destinations.  For hierarchical navigation, conform data types to `Hashable` and call `.navigationDestination(for:)`.  To support deep linking, decode URLs into path elements.  `NavigationSplitView` offers three columns for iPad and macOS.  The `scripts/navigation_scaffolder.py` can scaffold a navigation architecture with routes.  See `docs/navigation-architecture.md`.

Present secondary content with `.sheet` or `.fullScreenCover`.  On iOS 16+, support multiple sheet detents (`.medium`, `.large`, `.fraction`, custom heights), and use `.presentationDetents()` to specify them.  Provide `.presentationBackground()` to adjust backgrounds.

## Lists and Scroll Views

`List` is the easiest way to present a scrolling collection with automatic separators and row interactions.  Use `ForEach` inside `List` for dynamic data; supply an `id` to avoid identity issues.  For more custom layouts, use `ScrollView` with `LazyVStack`.  To improve performance, avoid heavy view modifiers inside list rows and favour `@StateObject` models to preserve row state.  Use `scrollIndicators`, `scrollPosition`, `refreshable` and `scrollDismissesKeyboard` for advanced behaviours.  Examples live in `swift/list_and_scroll.swift`.

## Accessibility Integration

Accessibility is not optional.  Always provide meaningful labels, hints and traits using `.accessibilityLabel()`, `.accessibilityHint()`, and `.accessibilityValue()`.  Use `.accessibilityAddTraits(.isButton)` to identify tappable items, and `.accessibilitySortedChildren()` to customise reading order.  Test with VoiceOver and dynamic type sizes.  The `scripts/accessibility_validator.py` tool scans SwiftUI files for missing labels and hints.  See `docs/performance-optimization.md` for tips on accessible performance.

## Dynamic Type & Adaptivity

SwiftUI automatically scales text and controls based on user’s dynamic type settings.  To support custom views, use `.dynamicTypeSize(...)` environment values and avoid hard‑coding pixel sizes.  Use `GeometryReader`, `Layout` protocol or `ViewThatFits` to adapt to available space.  Provide alternate layouts for accessibility sizes (e.g., `.accessibilitySizeCategory`).

## Performance Optimisation & View Update Cycles

SwiftUI’s diff engine is efficient, but misuse can cause unnecessary updates or memory leaks.  Understand the view update cycle: changing any state triggers a `body` recalculation; if the new view structure differs, SwiftUI updates the UI.  Use `Equatable` views to avoid recomputation when data hasn’t changed; conform your view to `Equatable` or wrap expensive subviews in `EquatableView`.  Avoid creating new objects in `body`, especially formatters, date formatters, or `ObservableObject`s.  Use `.onAppear` or `@StateObject` to manage lifetimes.  For lists, ensure row models are `Identifiable` and use `id` for stable identity.  More pitfalls and solutions are in `docs/performance-optimization.md`.

## Best Practices

* Keep views small and focused.  Break complex UIs into reusable components.
* Separate data models from views; use MVVM patterns with `@StateObject` or `@Observable` models.
* Use environment and preferences judiciously to avoid implicit dependencies.
* Test with accessibility tools and dynamic type to ensure inclusive design.
* Embrace value types and treat views as data.  Don’t store view instances.
* Use progressive disclosure: complex topics have dedicated docs (see `docs/`).

## Anti‑Patterns

* Performing network requests or long‑running work inside `body`.  Use `async` tasks instead.
* Overusing `GeometryReader` to calculate sizes; prefer `Layout` protocol or `LayoutPriority`.
* Creating new objects or closures every time `body` runs, leading to memory churn.
* Using `.onAppear` to schedule repeating timers; use `TimelineView` for scheduled updates【871986411204682†L94-L117】.
* Modifying state inside a view’s initializer, which can cause unpredictable behaviour.
* Excessive global state via `@EnvironmentObject` causing unclear dependencies.

## Common Pitfalls & Troubleshooting

If animations don’t run, ensure state changes happen inside `withAnimation {}` and that the view identity remains consistent.  When navigation links don’t update, check that your path’s element conforms to `Hashable` and that you mutate the path binding.  For layout glitches, verify that your `GeometryReader` is constrained and that your custom layout returns correct sizes.  Use Xcode’s `SwiftUI Preview` and inspect geometry in the inspector.  When something appears off, reduce the view to a minimal reproducible example.

## iOS 26+ Features

Stay current with new APIs.  iOS 26 introduces `Grid` for fully automatic grids, `FlowLayout` for wrapping content, improved detents for sheets, and new environment values like `{\.presentationCompactMode\}`.  Keep an eye on WWDC talks for details and update this skill accordingly.

## Further Reading

For deeper dives, open the markdown files in the `docs/` directory.  These guides expand on state management, layout systems, animation patterns, navigation architectures, performance optimisations and view lifecycle behaviours, each with full examples and citations.  Real‑world SwiftUI examples live in `swift/`, and Python scripts to generate components and analyse code reside in `scripts/`.  Use these resources to extend your understanding and generate high‑quality SwiftUI code.
