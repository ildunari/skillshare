import AppKit
import SwiftUI

/// SwiftUIGlassInAppKit embeds a SwiftUI view that uses the glassEffect
/// modifier into an AppKit view controller.  This demonstrates how
/// SwiftUI glass surfaces can be integrated into legacy AppKit windows.
@available(macOS 26.0, *)
final class SwiftUIGlassInAppKit: NSViewController {
    override func loadView() {
        let swiftUIView = AnyView(
            HStack(spacing: 12) {
                Image(systemName: "heart.fill")
                    .padding(8)
                    .glassEffect(.regular, in: .circle)
                Text("SwiftUI Glass")
                    .padding(8)
                    .glassEffect(.regular, in: .capsule)
            }
            .padding(16)
        )
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