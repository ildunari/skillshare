import AppKit
import SwiftUI

/// HybridGlassWindow demonstrates how to build an AppKit window whose
/// content is entirely SwiftUI but leverages Liquid Glass.  The window
/// adopts a unified toolbar style and hosts a SwiftUI view that uses
/// glassEffect and glass button styles.  This example illustrates
/// hybrid composition with modern materials.
@available(macOS 26.0, *)
final class HybridGlassWindow: NSWindowController {
    override init(window: NSWindow?) {
        let hostingView = NSHostingView(rootView: HybridContent())
        let wnd = NSWindow(contentRect: NSRect(x: 0, y: 0, width: 400, height: 250),
                           styleMask: [.titled, .closable, .resizable],
                           backing: .buffered,
                           defer: false)
        wnd.toolbarStyle = .unified
        wnd.title = "Hybrid Glass Window"
        wnd.contentView = hostingView
        super.init(window: wnd)
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    private struct HybridContent: View {
        var body: some View {
            VStack(spacing: 20) {
                Text("Hybrid window with SwiftUI glass")
                    .font(.headline)
                HStack(spacing: 12) {
                    Button("One") {}
                        .buttonStyle(.glass)
                    Button("Two") {}
                        .buttonStyle(.glass)
                }
                .padding(.horizontal, 16)
                .padding(.vertical, 10)
                .glassEffect(.regular, in: RoundedRectangle(cornerRadius: 16))
            }
            .padding(20)
        }
    }
}