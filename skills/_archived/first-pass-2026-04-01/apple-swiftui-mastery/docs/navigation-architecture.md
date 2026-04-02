# Navigation Architecture

Navigation in SwiftUI has evolved significantly with `NavigationStack` and `NavigationSplitView`.  This guide delves into declarative navigation, deep linking, programmatic path manipulation and best practices for large applications.

## NavigationStack

`NavigationStack` replaces `NavigationView` for hierarchical navigation.  It takes an optional `path` binding that represents the current navigation stack.  Each element in the path must conform to `Hashable` (or `Codable` for deep linking).  Use `.navigationDestination(for:destination:)` to define how to present each type of element.

```swift
@State private var path: [Screen] = []

var body: some View {
    NavigationStack(path: $path) {
        List(items) { item in
            NavigationLink(value: Screen.detail(item)) {
                Text(item.title)
            }
        }
        .navigationDestination(for: Screen.self) { screen in
            switch screen {
            case .detail(let item): DetailView(item: item)
            case .settings: SettingsView()
            }
        }
    }
}
```

Push a screen programmatically by appending to the path: `path.append(.settings)`.  Pop screens using `path.removeLast()` or clear the path to return to the root.

## NavigationSplitView

On iPad and macOS, `NavigationSplitView` provides a three‑column layout.  The first column is the sidebar, the second is the content list, and the third displays detail content.  Bindings to selection values maintain the current selection across the columns.

```swift
@State private var selection: Item?
var body: some View {
    NavigationSplitView {
        List(items, selection: $selection) { item in
            Text(item.title)
        }
    } content: {
        if let selected = selection {
            Text(selected.description)
        } else {
            Text("Select an item")
        }
    } detail: {
        Text("Detail view")
    }
}
```

Use `NavigationSplitView` when building universal apps that target iPad or macOS to take advantage of sidebars and three‑pane navigation.

## Deep Linking and URL Schemes

To support universal links or custom schemes, conform your path elements to `Codable`.  SwiftUI can then decode a URL into the appropriate path.  In `@main` App, use the `.onOpenURL` modifier to handle incoming URLs and update your navigation path accordingly.  Always validate untrusted URLs before using them.

## Programmatic Navigation

Avoid embedding business logic inside view bodies.  Instead, store navigation state in view models and update path bindings based on user actions.  This simplifies unit testing and decouples navigation from the view hierarchy.  Use `enum` or `struct` types to represent screens rather than raw strings.

## Modular Architecture

For large applications, break navigation into modules.  Each module exposes its own `NavigationStack` or `NavigationSplitView` with typed path elements.  Share global state via `@EnvironmentObject` or via dependency injection.  Avoid passing path bindings through many layers—use callbacks to bubble navigation events back up to the owning container.

## Tools and Scripts

The `scripts/navigation_scaffolder.py` script scaffolds a new navigation architecture.  Provide the names of your screens, and it generates Swift files defining the path enum, a root `NavigationStack`, and placeholder destination views.  Use this as a starting point for new projects.