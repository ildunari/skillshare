import AppKit

/// GlassSidebarWindow demonstrates how to implement a split view where the
/// sidebar sits on a Liquid Glass surface.  The sidebar uses an
/// NSGlassEffectView and is grouped with the content using an
/// NSSplitView.  The example applies concentric rounded corners on the
/// outer edges of the window.
@available(macOS 26.0, *)
final class GlassSidebarWindowController: NSWindowController, NSSplitViewDelegate {
    override init(window: NSWindow?) {
        let wnd = NSWindow(contentRect: NSRect(x: 0, y: 0, width: 800, height: 500),
                           styleMask: [.titled, .resizable, .closable],
                           backing: .buffered,
                           defer: false)
        wnd.title = "Glass Sidebar"
        super.init(window: wnd)
        setupWindow()
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    private func setupWindow() {
        guard let window = self.window else { return }
        // Create split view for sidebar and content
        let splitView = NSSplitView()
        splitView.isVertical = true
        splitView.dividerStyle = .thin
        splitView.delegate = self

        // Sidebar on glass
        let sidebarGlass = NSGlassEffectView()
        sidebarGlass.cornerRadius = 0 // inner corners will merge with content
        let list = NSScrollView()
        let document = NSView()
        document.wantsLayer = true
        document.layer?.backgroundColor = NSColor.clear.cgColor
        list.documentView = document
        sidebarGlass.contentView = list
        // You would populate 'document' with your sidebar items

        // Solid content area
        let content = NSView()
        content.wantsLayer = true
        content.layer?.backgroundColor = NSColor.windowBackgroundColor.cgColor

        splitView.addArrangedSubview(sidebarGlass)
        splitView.addArrangedSubview(content)
        splitView.setHoldingPriority(.defaultLow, forSubviewAt: 1)

        window.contentView = splitView

        // Constrain split view to window
        splitView.translatesAutoresizingMaskIntoConstraints = false
        NSLayoutConstraint.activate([
            splitView.leadingAnchor.constraint(equalTo: window.contentView!.leadingAnchor),
            splitView.trailingAnchor.constraint(equalTo: window.contentView!.trailingAnchor),
            splitView.topAnchor.constraint(equalTo: window.contentView!.topAnchor),
            splitView.bottomAnchor.constraint(equalTo: window.contentView!.bottomAnchor)
        ])

        // Fix initial sidebar width
        sidebarGlass.widthAnchor.constraint(equalToConstant: 240).isActive = true
    }
}