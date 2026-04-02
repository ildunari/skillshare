---
name: swift-agentation
description: Set up the Swift Agentation visual annotation toolbar in an iOS/SwiftUI/UIKit project. Agentation lets users tap UI elements in a running app, annotate them with notes, and copy structured output (Markdown or JSON) describing the exact view hierarchy, frames, and labels — which they then paste into an AI coding session for precise element identification. Use this skill whenever the user mentions agentation in an iOS context, wants to add element annotation to a Swift app, asks about pointing at UI elements for AI coding, or needs to set up swift-agentation. Also trigger when adding the swift-agentation SPM dependency or configuring Agentation.shared.install().
---

# Swift Agentation Setup

Set up the [swift-agentation](https://github.com/ertembiyik/swift-agentation) visual annotation toolbar in an iOS project. This is the Swift/iOS port of the web-based agentation tool — it lets users tap elements in their running app, annotate them with notes, and copy structured output that an AI coding agent can consume to understand exactly which view they're referring to.

## What It Does

A floating toolbar overlay appears in the app during development. Users start a capture session, tap elements to annotate them, and copy the structured output (Markdown or JSON) to their clipboard. The output includes viewport size, element type, location path in the view hierarchy, frame coordinates, and the user's feedback notes.

## Installation Steps

### 1. Add the SPM dependency

Add to the project's `Package.swift` or via Xcode's File > Add Package Dependencies:

```
https://github.com/ertembiyik/swift-agentation.git
```

Requires iOS 17.0+ and Swift 5.9+. Has one transitive dependency: `UniversalGlass` (glassmorphism UI for the toolbar).

If the project uses a `.xcodeproj` without a `Package.swift`, instruct the user to add it through Xcode's package manager UI.

### 2. Add the install call

In the app's entry point, wrap the install in `#if DEBUG` so it never ships in release builds:

**SwiftUI App:**
```swift
#if DEBUG
import Agentation
#endif

@main
struct MyApp: App {
    init() {
        #if DEBUG
        Agentation.shared.install()
        #endif
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

**UIKit AppDelegate:**
```swift
#if DEBUG
import Agentation
#endif

class AppDelegate: UIResponder, UIApplicationDelegate {
    func application(_ application: UIApplication,
                     didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        #if DEBUG
        Agentation.shared.install()
        #endif
        return true
    }
}
```

### 3. (Optional) Tag SwiftUI views for View Hierarchy mode

The default data source is `.accessibility`, which works with both SwiftUI and UIKit out of the box using standard accessibility modifiers. If the user prefers the `.viewHierarchy` data source (better for UIKit-heavy apps), SwiftUI views need explicit tagging since they don't expose backing UIViews:

```swift
Text("Hello")
    .agentationTag("GreetingLabel")
```

For UIKit views, no tagging is needed — the view hierarchy data source traverses the UIView tree directly. Setting `accessibilityIdentifier` or `accessibilityLabel` improves naming in the output.

### 4. (Optional) Configure preferences

```swift
#if DEBUG
Agentation.shared.selectedDataSourceType = .accessibility  // default
Agentation.shared.outputFormat = .markdown                 // or .json
Agentation.shared.includeHiddenElements = false            // default
Agentation.shared.includeSystemViews = false               // default
#endif
```

## Data Sources

| Data Source | Best For | SwiftUI Support | UIKit Support |
|------------|---------|----------------|---------------|
| `.accessibility` (default) | Most projects | Works via accessibility modifiers | Works natively |
| `.viewHierarchy` | UIKit-heavy apps | Requires `.agentationTag()` | Works natively |

Recommend `.accessibility` for most projects — it requires zero extra setup if the app already has accessibility labels, and it works with both SwiftUI and UIKit.

## Confirming Setup

After adding the dependency and install call, tell the user:

1. Build and run the app in the simulator or on device
2. A floating sparkles button appears — tap it to expand the toolbar
3. Tap "Start" to begin a capture session
4. Tap any UI element to select it, add a note describing what you want changed
5. Tap "Copy" to get the structured output on your clipboard
6. Paste that output into your Claude Code / Codex / AI coding session

The output gives the AI agent precise coordinates, hierarchy paths, and element metadata — so it knows exactly which view you're referring to without ambiguity.
