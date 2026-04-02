import SwiftUI
import AppKit

/// AppKitGlassInSwiftUI embeds an NSGlassEffectView inside SwiftUI using
/// NSViewRepresentable.  The hosted glass view sets its own corner radius
/// and tint and exposes a label.  This pattern is useful when you need
/// AppKit‑level control (e.g. grouping or custom tints) inside a SwiftUI
/// hierarchy.
@available(macOS 26.0, *)
struct AppKitGlassInSwiftUI: View {
    var body: some View {
        VStack(spacing: 20) {
            Text("AppKit glass below")
            GlassHost()
                .frame(width: 220, height: 60)
        }
        .padding(20)
    }

    private struct GlassHost: NSViewRepresentable {
        func makeNSView(context: Context) -> NSGlassEffectView {
            let glass = NSGlassEffectView()
            glass.cornerRadius = 16
            glass.tintColor = .systemPink
            let label = NSTextField(labelWithString: "AppKit Glass")
            label.alignment = .center
            glass.contentView = label
            return glass
        }
        func updateNSView(_ nsView: NSGlassEffectView, context: Context) {}
    }
}

#if DEBUG
@available(macOS 26.0, *)
struct AppKitGlassInSwiftUI_Previews: PreviewProvider {
    static var previews: some View {
        AppKitGlassInSwiftUI()
    }
}
#endif