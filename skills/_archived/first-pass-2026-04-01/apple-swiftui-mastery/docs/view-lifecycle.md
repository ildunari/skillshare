# View Lifecycle

SwiftUI views are value types that are recreated whenever state changes.  They don’t have the same lifecycle as UIKit view controllers, but there are still places to perform side effects and manage asynchronous work.  This guide explains the available hooks and best practices.

## Creation and Identity

Views conforming to `View` are structs; they are created whenever their parent recomputes its body.  Do not rely on `init()` being called only once—rely on property wrappers like `@State` and `@StateObject` to persist data across updates.  Identity comes from the view’s type and position in the hierarchy【152934397403680†L392-L406】.  Conditional branches or different types break identity and cause new views to be created【152934397403680†L510-L567】.

## `onAppear` and `onDisappear`

Use `.onAppear` to perform side effects when a view becomes visible.  This is similar to `viewDidAppear` in UIKit.  Conversely, `.onDisappear` runs when the view is removed or hidden.  These modifiers are attached to the view they apply to, not to the entire subtree.  Avoid heavy work in `onAppear` that may block the main thread.

```swift
struct DataLoadingView: View {
    @State private var items: [Item] = []

    var body: some View {
        List(items) { item in
            Text(item.name)
        }
        .onAppear {
            Task { await loadItems() }
        }
    }

    func loadItems() async {
        // fetch from network
    }
}
```

`onDisappear` is useful for cancelling tasks or resetting temporary state.

## `task` Modifier

Introduced in iOS 15, `.task` attaches an asynchronous task to a view.  The task runs when the view appears and cancels when the view disappears.  Use the `id` parameter to restart the task when dependencies change.

```swift
struct WeatherView: View {
    var location: String
    @State private var forecast: Forecast?

    var body: some View {
        VStack {
            if let forecast = forecast {
                Text(forecast.description)
            } else {
                ProgressView()
            }
        }
        .task(id: location) {
            forecast = await fetchForecast(for: location)
        }
    }
}
```

## `onChange` and Publishers

Use `.onChange(of:)` to run code when a value changes.  For multiple dependencies, chain `.onChange` calls or centralise logic in a model.  Combine publishers with `.onReceive` to react to asynchronous events.

## Avoiding Side Effects in `body`

Never perform side effects like API calls, database writes or heavy computations in `body`.  Because `body` can run many times, this leads to duplicated work.  Offload such tasks to `onAppear`, `task`, or view models.  Use `@StateObject` to manage asynchronous operations and store results.

## Destruction and Cleanup

Views are transient, but associated objects (view models, tasks, timers) persist.  Cancel timers and tasks in `onDisappear` or deinit of observable objects.  For example, use the `ObservableObject`’s `deinit` to stop network listeners.

## Relationship to UIKit/AppKit

In mixed projects, SwiftUI views embed inside `UIHostingController` or `NSHostingController`.  The hosting controller’s lifecycle (e.g., `viewDidLoad`, `viewWillAppear`) still applies.  Use these methods to manage bridging behaviours, but keep SwiftUI code pure where possible.

Understanding the lifecycle helps avoid memory leaks, race conditions and unresponsive interfaces.