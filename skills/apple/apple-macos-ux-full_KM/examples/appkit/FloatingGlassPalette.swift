import AppKit

/// FloatingGlassPalette shows how to build a floating panel (inspector)
/// that uses Liquid Glass for its background.  The panel is non‑activating
/// and floats above all other windows.  Each button is arranged in a
/// vertical stack within the glass surface.
@available(macOS 26.0, *)
final class FloatingGlassPalette: NSPanel {
    init() {
        super.init(contentRect: NSRect(x: 0, y: 0, width: 240, height: 180),
                   styleMask: [.titled, .nonactivatingPanel],
                   backing: .buffered,
                   defer: false)
        self.isFloatingPanel = true
        self.hidesOnDeactivate = false
        self.level = .floating
        self.title = "Floating Palette"
        self.collectionBehavior = [.moveToActiveSpace, .transient]

        // Create glass surface
        let glass = NSGlassEffectView()
        glass.cornerRadius = 12
        glass.tintColor = .tertiaryLabelColor

        // Add some controls inside the glass
        let stack = NSStackView()
        stack.orientation = .vertical
        stack.alignment = .leading
        stack.spacing = 8
        let button1 = NSButton(title: "Action One", target: nil, action: nil)
        let button2 = NSButton(title: "Action Two", target: nil, action: nil)
        stack.addArrangedSubview(button1)
        stack.addArrangedSubview(button2)
        glass.contentView = stack

        self.contentView = glass
    }
}