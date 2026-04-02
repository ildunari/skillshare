import AppKit

final class UnifiedToolbarWindow: NSWindowController, NSToolbarDelegate, NSToolbarItemValidation {
    private let toolbar = NSToolbar(identifier: "UnifiedToolbar")

    convenience init() {
        let window = NSWindow(contentRect: NSRect(x: 0, y: 0, width: 900, height: 600),
                              styleMask: [.titled, .resizable, .closable, .miniaturizable],
                              backing: .buffered, defer: false)
        window.titlebarAppearsTransparent = true
        window.titleVisibility = .hidden
        window.toolbarStyle = .unified
        self.init(window: window)
        toolbar.delegate = self
        toolbar.allowsUserCustomization = true
        window.toolbar = toolbar
        window.setFrameAutosaveName("UnifiedToolbarWindow")
    }

    func toolbarAllowedItemIdentifiers(_ toolbar: NSToolbar) -> [NSToolbarItem.Identifier] {
        [.flexibleSpace, .space,
         NSToolbarItem.Identifier("com.example.new"),
         NSToolbarItem.Identifier("com.example.refresh")]
    }

    func toolbarDefaultItemIdentifiers(_ toolbar: NSToolbar) -> [NSToolbarItem.Identifier] {
        [NSToolbarItem.Identifier("com.example.new"), .flexibleSpace, NSToolbarItem.Identifier("com.example.refresh")]
    }

    func toolbar(_ toolbar: NSToolbar, itemForItemIdentifier itemIdentifier: NSToolbarItem.Identifier,
                 willBeInsertedIntoToolbar flag: Bool) -> NSToolbarItem? {
        switch itemIdentifier.rawValue {
        case "com.example.new":
            let it = NSToolbarItem(itemIdentifier: itemIdentifier)
            it.label = "New"
            it.image = NSImage(systemSymbolName: "plus", accessibilityDescription: "New")
            it.target = nil
            it.action = #selector(newDocument(_:))
            return it
        case "com.example.refresh":
            let it = NSToolbarItem(itemIdentifier: itemIdentifier)
            it.label = "Refresh"
            it.image = NSImage(systemSymbolName: "arrow.clockwise", accessibilityDescription: "Refresh")
            it.target = nil
            it.action = #selector(refresh(_:))
            return it
        default: return nil
        }
    }

    func validateToolbarItem(_ item: NSToolbarItem) -> Bool {
        // Example: disable Refresh if nothing is selected
        if item.itemIdentifier.rawValue == "com.example.refresh" {
            return true
        }
        return true
    }

    @objc func newDocument(_ sender: Any?) {}
    @objc func refresh(_ sender: Any?) {}
}
