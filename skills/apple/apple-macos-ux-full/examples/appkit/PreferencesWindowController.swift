import AppKit

final class PreferencesWindowController: NSWindowController, NSToolbarDelegate {
    enum PaneID: String { case general, advanced, updates }

    private let toolbar = NSToolbar(identifier: "PreferencesToolbar")
    private var views: [PaneID: NSView] = [:]

    convenience init() {
        let window = NSWindow(contentRect: NSRect(x: 0, y: 0, width: 640, height: 420),
                              styleMask: [.titled, .closable],
                              backing: .buffered, defer: false)
        window.center()
        window.title = "Settings"
        self.init(window: window)
        toolbar.delegate = self
        toolbar.allowsUserCustomization = false
        window.toolbar = toolbar
        buildPanes()
        showPane(.general)
    }

    private func buildPanes() {
        let general = NSStackView(views: [NSTextField(labelWithString: "General Settings")])
        general.edgeInsets = NSEdgeInsets(top: 20, left: 20, bottom: 20, right: 20)
        let advanced = NSStackView(views: [NSTextField(labelWithString: "Advanced Settings")])
        advanced.edgeInsets = NSEdgeInsets(top: 20, left: 20, bottom: 20, right: 20)
        let updates = NSStackView(views: [NSTextField(labelWithString: "Updates Settings")])
        updates.edgeInsets = NSEdgeInsets(top: 20, left: 20, bottom: 20, right: 20)
        views = [.general: general, .advanced: advanced, .updates: updates]
    }

    func toolbarAllowedItemIdentifiers(_ toolbar: NSToolbar) -> [NSToolbarItem.Identifier] {
        [NSToolbarItem.Identifier(PaneID.general.rawValue),
         NSToolbarItem.Identifier(PaneID.advanced.rawValue),
         NSToolbarItem.Identifier(PaneID.updates.rawValue)]
    }

    func toolbarDefaultItemIdentifiers(_ toolbar: NSToolbar) -> [NSToolbarItem.Identifier] {
        toolbarAllowedItemIdentifiers(toolbar)
    }

    func toolbar(_ toolbar: NSToolbar, itemForItemIdentifier itemIdentifier: NSToolbarItem.Identifier,
                 willBeInsertedIntoToolbar flag: Bool) -> NSToolbarItem? {
        let item = NSToolbarItem(itemIdentifier: itemIdentifier)
        item.label = itemIdentifier.rawValue.capitalized
        item.image = NSImage(systemSymbolName: "gearshape", accessibilityDescription: item.label)
        item.target = self
        item.action = #selector(selectPane(_:))
        return item
    }

    @objc private func selectPane(_ sender: NSToolbarItem) {
        if let id = PaneID(rawValue: sender.itemIdentifier.rawValue) {
            showPane(id)
        }
    }

    private func showPane(_ id: PaneID) {
        window?.contentView = views[id]
        window?.title = id.rawValue.capitalized
    }
}
