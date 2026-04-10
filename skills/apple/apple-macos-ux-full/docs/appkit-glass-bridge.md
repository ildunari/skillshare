# Bridging AppKit and SwiftUI for Liquid Glass

Liquid Glass is available to both AppKit and SwiftUI in macOS 26.  When
building hybrid applications, you often need to embed glass surfaces across
framework boundaries.  This guide demonstrates how to bridge Liquid Glass
between AppKit and SwiftUI using the familiar representable/hosting
patterns.

## AppKit glass inside SwiftUI

You can host an `NSGlassEffectView` within a SwiftUI hierarchy by
conforming to `NSViewRepresentable`.  This allows you to use all the
capabilities of AppKit’s glass view — such as grouping, custom tinting
and exact control over corner radii — from a SwiftUI scene.

```swift
import SwiftUI
import AppKit

struct GlassHost: NSViewRepresentable {
    func makeNSView(context: Context) -> NSGlassEffectView {
        let glass = NSGlassEffectView()
        glass.cornerRadius = 18
        glass.tintColor = .controlAccentColor

        // Example content inside the glass
        let label = NSTextField(labelWithString: "AppKit in SwiftUI")
        label.font = .systemFont(ofSize: 14, weight: .medium)
        label.textColor = .secondaryLabelColor
        glass.contentView = label

        return glass
    }
    func updateNSView(_ nsView: NSGlassEffectView, context: Context) {
        // Update properties based on SwiftUI state if needed
    }
}

struct ExampleSwiftUIView: View {
    var body: some View {
        VStack(spacing: 24) {
            Text("Above the glass")
            GlassHost()
                .frame(width: 200, height: 60)
            Text("Below the glass")
        }
        .padding(20)
    }
}
```

**Notes**

* Use `NSViewRepresentable` when you need AppKit‑specific control such
  as grouping (`NSGlassEffectContainerView`) or custom tints not yet
  exposed in SwiftUI.
* The hosted AppKit view participates in the SwiftUI layout just like
  any other view.  Provide explicit frame constraints to avoid zero‑size
  results.

## SwiftUI glass inside AppKit

To use SwiftUI’s `glassEffect` inside an AppKit view hierarchy, embed a
SwiftUI view inside an `NSHostingView` or `NSHostingController`.  This
approach is ideal when your UI is primarily AppKit but you want to
sprinkle in SwiftUI glass patterns.

```swift
import AppKit
import SwiftUI

final class GlassHostingViewController: NSViewController {
    override func loadView() {
        // Create a SwiftUI view using glassEffect
        let swiftUIView = AnyView(
            HStack(spacing: 20) {
                Image(systemName: "star.fill")
                    .frame(width: 24, height: 24)
                    .padding(8)
                    .glassEffect(.regular, in: .circle)
                Text("SwiftUI in AppKit")
                    .padding(8)
                    .glassEffect(.regular, in: .capsule)
            }
            .padding(16)
        )
        // Host the SwiftUI view in AppKit
        let hosting = NSHostingView(rootView: swiftUIView)
        hosting.translatesAutoresizingMaskIntoConstraints = false
        self.view = NSView()
        self.view.addSubview(hosting)
        NSLayoutConstraint.activate([
            hosting.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            hosting.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            hosting.topAnchor.constraint(equalTo: view.topAnchor),
            hosting.bottomAnchor.constraint(equalTo: view.bottomAnchor)
        ])
    }
}
```

**Notes**

* SwiftUI’s `glassEffect` supports `.regular`, `.clear` and `.identity`
  styles and accepts any `InsettableShape` (e.g. `Capsule`, `RoundedRectangle`).
* When bridging into AppKit, the hosted SwiftUI view carries its own
  semantics and focus handling.  Use `NSHostingController` if you need a
  full controller with lifecycle methods.

## Data flow & state

When combining AppKit glass and SwiftUI glass, manage shared state via
observable objects or other binding mechanisms.  For example, you can
expose a `@State` property in SwiftUI that drives the tint color and
propagate changes back to AppKit via the `Coordinator` pattern if you
implement `NSViewRepresentable`.  Conversely, when embedding SwiftUI in
AppKit, you can set `HostingView.rootView` again to update the SwiftUI
state when an AppKit action occurs.

In hybrid architectures, it’s often simplest to treat glass surfaces as
presentation details while keeping core app state in models and view
controllers that are agnostic of the material system.