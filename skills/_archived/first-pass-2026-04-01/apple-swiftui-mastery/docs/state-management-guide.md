# State Management Guide

SwiftUI’s declarative paradigm revolves around **state**.  Understanding the nuances of each property wrapper is essential for building robust, maintainable interfaces.  This guide expands upon the overview provided in `SKILL.md` and supplies examples and edge cases.

## Source of Truth

The **source of truth** is the single authoritative storage for a piece of data.  Views should not own data that belongs elsewhere.  If multiple views need read/write access, lift the state up or use an environment model.  Misplaced state leads to inconsistent UI and unpredictable behaviour.

## `@State`

Use `@State` for simple value types (booleans, strings, structs) that belong exclusively to a single view.  When the value changes, SwiftUI re‑renders the view.  The storage persists as long as the view is alive.  Because views are recreated frequently, avoid heavy objects in `@State`.

**Example:**

```swift
struct ToggleExample: View {
    @State private var isOn = false

    var body: some View {
        Toggle("Enable Feature", isOn: $isOn)
    }
}
```

### Computed State

Sometimes you want derived values from state.  Use computed properties instead of additional `@State` variables.  For example, compute a formatted string from a `Date` state rather than storing both date and string.

## `@Binding`

Bindings allow child views to mutate state owned by an ancestor.  You can pass a binding down using the `$` operator on a `@State` property.  SwiftUI automatically updates the UI when the binding changes.

**Example:**

```swift
struct SliderRow: View {
    @Binding var value: Double
    var label: String

    var body: some View {
        VStack(alignment: .leading) {
            Text("\(label): \(Int(value))")
            Slider(value: $value, in: 0...100)
        }
    }
}

struct Parent: View {
    @State private var brightness: Double = 50

    var body: some View {
        SliderRow(value: $brightness, label: "Brightness")
    }
}
```

Avoid creating bindings from mutable global variables or computed properties; only derive bindings from other bindings or state.

## `@StateObject` and `@ObservedObject`

As the overview notes, both wrappers subscribe to an `ObservableObject` and trigger view updates when published properties change.  Use `@StateObject` when the view creates the model itself.  Use `@ObservedObject` when the model comes from the outside.  Failing to use `@StateObject` can lead to repeated reinitialisations【185021888277737†L38-L65】.

**Pitfall:** Creating a view model inside `body` with `@ObservedObject` resets the model on every update.  Instead, instantiate it in the view’s initializer or use `@StateObject`.

## `@Environment` and `@EnvironmentObject`

Environment values are key–value pairs accessible throughout the view hierarchy.  Read system values like `colorScheme`, `dynamicTypeSize`, or custom keys.  Use `@EnvironmentObject` for shared data models; mark the model class with `ObservableObject` and inject it at the root via `.environmentObject()`.

**Example:**

```swift
final class Settings: ObservableObject {
    @Published var darkMode: Bool = false
}

struct ContentView: View {
    @EnvironmentObject var settings: Settings
    var body: some View {
        Toggle("Dark Mode", isOn: $settings.darkMode)
    }
}

@main
struct AppMain: App {
    @StateObject private var settings = Settings()
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(settings)
        }
    }
}
```

## The New `@Observable` Macro

iOS 17 introduced `@Observable` to reduce boilerplate.  Annotating a class with `@Observable` automatically synthesises observation.  You can then use `@State` to host the model and pass it down via initialisers.  According to Apple, this approach simplifies state and eliminates the need for `@Published` and `ObservableObject` conformance【228322540172834†L38-L83】.

**Example:**

```swift
import Observation

@Observable
class CounterModel {
    var count: Int = 0
    func increment() { count += 1 }
}

struct CounterView: View {
    @State private var model = CounterModel()
    var body: some View {
        VStack {
            Text("Count: \(model.count)")
            Button("Increment") { model.increment() }
        }
    }
}
```

This model automatically notifies SwiftUI when `count` changes.  The `CounterView` uses `@State` to own the model, preserving it across body recomputations.

## Combining Property Wrappers

You can mix wrappers.  For example, a view may own a model via `@StateObject` and also expose a binding to one of its properties.  Avoid circular dependencies—don’t bind a value back to itself.

## Passing State to Previews

In SwiftUI previews, provide sample data via `@State` or `@StateObject`.  Do not rely on global state or environment.  Previews should be deterministic and self‑contained.

## Debugging State Issues

If a view isn’t updating, verify that:

* The state is mutated on the main thread.
* The property is marked with the correct wrapper (`@State`, `@StateObject`, etc.).
* For `ObservableObject`, changes are marked `@Published` or the class uses `@Observable`.
* The view or its parent holds onto the model and isn’t re‑creating it every update.

Use SwiftUI’s `print()` within `body` or `onChange(of:)` to trace state changes.  Xcode’s “View Hierarchy” and “Memory Graph” tools can also help diagnose ownership and retention cycles.