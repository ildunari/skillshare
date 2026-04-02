import AppKit

/// GlassHUDWindow demonstrates a HUD‑style panel with a tinted glass
/// background.  HUD windows are typically used for transient feedback or
/// overlays that should not steal focus.  The glass tint increases
/// opacity to improve legibility over busy backgrounds.
@available(macOS 26.0, *)
final class GlassHUDWindow: NSWindow {
    init() {
        super.init(contentRect: NSRect(x: 0, y: 0, width: 220, height: 120),
                   styleMask: [.hudWindow],
                   backing: .buffered,
                   defer: false)
        self.titleVisibility = .hidden
        self.isOpaque = false
        self.backgroundColor = .clear

        // Set up glass content
        let glass = NSGlassEffectView()
        glass.cornerRadius = 16
        glass.tintColor = NSColor.controlBackgroundColor.withAlphaComponent(0.6)
        let label = NSTextField(labelWithString: "HUD Information")
        label.alignment = .center
        label.font = .systemFont(ofSize: 14, weight: .semibold)
        glass.contentView = label

        self.contentView = glass
    }
}