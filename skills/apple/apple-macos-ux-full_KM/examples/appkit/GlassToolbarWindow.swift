import AppKit

/// GlassToolbarWindow demonstrates a unified toolbar with Liquid Glass on macOS 26.
/// The toolbar uses a prominent style for its primary action, and the content
/// area is wrapped in an NSGlassEffectView with a rounded corner.  This
/// example shows how to adopt macOS 26 materials without losing AppKit
/// configurability.
@available(macOS 26.0, *)
final class GlassToolbarWindowController: NSWindowController, NSToolbarDelegate {
    override init(window: NSWindow?) {
        let wnd = NSWindow(contentRect: NSRect(x: 0, y: 0, width: 600, height: 400),
                           styleMask: [.titled, .resizable, .closable],
                           backing: .buffered,
                           defer: false)
        wnd.title = "Glass Toolbar"
        super.init(window: wnd)
        setupWindow()
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    private func setupWindow() {
        guard let window = self.window else { return }
        // Configure unified toolbar
        let toolbar = NSToolbar(identifier: NSToolbar.Identifier("GlassToolbar"))
        toolbar.delegate = self
        toolbar.displayMode = .iconOnly
        window.toolbar = toolbar
        window.toolbarStyle = .unified

        // Create a root view that hosts a glass container
        let root = NSView(frame: .zero)
        window.contentView = root
        root.translatesAutoresizingMaskIntoConstraints = false
        NSLayoutConstraint.activate([
            root.leadingAnchor.constraint(equalTo: window.contentView!.leadingAnchor),
            root.trailingAnchor.constraint(equalTo: window.contentView!.trailingAnchor),
            root.topAnchor.constraint(equalTo: window.contentView!.topAnchor),
            root.bottomAnchor.constraint(equalTo: window.contentView!.bottomAnchor)
        ])

        // Create a glass effect view
        let glass = NSGlassEffectView()
        glass.cornerRadius = 12
        glass.tintColor = .controlAccentColor

        // Example content inside the glass
        let stack = NSStackView()
        stack.orientation = .vertical
        stack.spacing = 12
        let label = NSTextField(labelWithString: "Welcome to Liquid Glass")
        label.font = .systemFont(ofSize: 16, weight: .medium)
        let button = NSButton(title: "Primary Action", target: nil, action: nil)
        stack.addArrangedSubview(label)
        stack.addArrangedSubview(button)
        glass.contentView = stack

        root.addSubview(glass)
        glass.translatesAutoresizingMaskIntoConstraints = false
        NSLayoutConstraint.activate([
            glass.leadingAnchor.constraint(equalTo: root.leadingAnchor, constant: 20),
            glass.trailingAnchor.constraint(equalTo: root.trailingAnchor, constant: -20),
            glass.topAnchor.constraint(equalTo: root.topAnchor, constant: 20),
            glass.bottomAnchor.constraint(equalTo: root.bottomAnchor, constant: -20)
        ])
    }

    // MARK: - NSToolbarDelegate
    func toolbarAllowedItemIdentifiers(_ toolbar: NSToolbar) -> [NSToolbarItem.Identifier] {
        return [NSToolbarItem.Identifier("compose"), .flexibleSpace]
    }

    func toolbarDefaultItemIdentifiers(_ toolbar: NSToolbar) -> [NSToolbarItem.Identifier] {
        return [NSToolbarItem.Identifier("compose"), .flexibleSpace]
    }

    func toolbar(_ toolbar: NSToolbar, itemForItemIdentifier itemIdentifier: NSToolbarItem.Identifier, willBeInsertedIntoToolbar flag: Bool) -> NSToolbarItem? {
        let item = NSToolbarItem(itemIdentifier: itemIdentifier)
        if itemIdentifier.rawValue == "compose" {
            item.image = NSImage(systemSymbolName: "square.and.pencil", accessibilityDescription: "Compose")
            item.label = "Compose"
            item.toolTip = "Compose"
            item.target = nil
            item.action = nil
            // Use prominent style with a custom tint to demonstrate glass
            item.style = .prominent
            item.backgroundTintColor = .systemBlue
        }
        return item
    }
}