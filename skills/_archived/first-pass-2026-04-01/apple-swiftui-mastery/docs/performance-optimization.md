# Performance Optimization

SwiftUI is designed for efficiency, but careless code can still degrade performance.  This guide covers strategies for reducing view recomputation, managing memory, and ensuring smooth scrolling in lists and grids.  It also touches on accessibility considerations because accessible apps must perform well across assistive technologies.

## Understand the Update Cycle

When any observed state changes, SwiftUI reevaluates the `body` of the view that holds that state.  If the resulting view tree differs in structure or identity, SwiftUI computes a diff and updates the UI.  Frequent updates are not inherently bad—views are cheap to recreate—but heavy work inside `body` can slow things down.  Avoid performing calculations, formatting, or network requests in `body`.

## Equatable Views

If a view’s output depends solely on an equatable value, conform it to `Equatable`.  SwiftUI will compare the previous and current values; if they are equal, it skips updating the view.  Alternatively, wrap subviews in `EquatableView` and supply a value for comparison.

```swift
struct TemperatureView: View, Equatable {
    let temp: Double
    static func == (lhs: TemperatureView, rhs: TemperatureView) -> Bool {
        lhs.temp.rounded() == rhs.temp.rounded()
    }
    var body: some View {
        Text("\(Int(temp))°C")
    }
}
```

The view only re-renders when the rounded temperature changes.

## Memoization and Caching

Expensive operations like image decoding or text formatting should be cached outside of `body`.  Create helper objects or functions that memoize results.  For example, precompute `DateFormatter`s and reuse them rather than creating a new formatter each time.

## Use `@StateObject` and `@Observable` Correctly

Instantiating models in `body` resets them every update.  Use `@StateObject` or `@Observable` with `@State` to ensure models persist【185021888277737†L38-L65】【228322540172834†L38-L83】.  For lists, assign a dedicated view model per row to avoid recomputing heavy logic when other rows update.

## Efficient Lists and Grids

`List` and `LazyVGrid` lazily create rows and cells as they appear on screen.  To maintain performance:

1. **Use Identifiable Data:** Provide stable identifiers via `Identifiable` conformance or `id` parameter so SwiftUI can reuse cells.
2. **Minimise Overdraw:** Avoid heavy backgrounds or unnecessary overlays inside rows.  Keep row views simple.
3. **Avoid Complex Layout in Rows:** Move heavy computations into models or separate views.
4. **Use Lazy Stacks for Custom Scroll Views:** Combine `ScrollView` with `LazyVStack` for custom lists.  But don’t embed a `LazyVStack` inside another scroll view; nested scrolls are expensive.

## Throttling Updates

When responding to continuous inputs like sliders or text fields, you may want to throttle updates to avoid overwhelming the UI.  Use `onChange(of:)` with a debounce mechanism or rely on Combine’s `debounce` operator.

## Instrumentation and Diagnostics

Xcode offers tools to measure performance:

* **Instruments – SwiftUI View Body Counts:** Shows how often each view’s body recomputes.
* **Time Profiler:** Identifies slow functions or heavy operations.
* **Memory Graph:** Detects leaks and cycles.

Log state changes with `print()` or `os_log()` and use `#if DEBUG` to exclude logs from production builds.

## Accessibility and Performance

Accessibility features such as VoiceOver and Dynamic Type can impact layout and performance.  Always test with these features enabled.  Provide lazy loading and avoid infinite animations when `accessibilityReduceMotion` is true.  Use `.accessibilityHidden(_:)` judiciously—hiding large subtrees can reduce processing for VoiceOver.

## Common Pitfalls

* **Creating views inside loops without identifiers** leads to identity confusion and repeated row creation.
* **Using `GeometryReader` for simple size queries** can cause layout thrashing【45585243622685†L37-L46】.
* **Storing view state in models** can cause cross‑view contamination.  Keep view‑specific state in the view layer.
* **Updating global state too frequently** triggers widespread updates via `@EnvironmentObject`.

Follow the best practices and patterns across this skill to build fluid, responsive interfaces.