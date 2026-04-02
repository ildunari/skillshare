import AppKit

final class MenuBarResponderValidation: NSViewController, NSMenuItemValidation {
    override func loadView() { self.view = NSView() }

    @objc func copy(_ sender: Any?) { /* perform copy */ }
    @objc func paste(_ sender: Any?) { /* perform paste */ }
    @objc func toggleSidebar(_ sender: Any?) { /* toggle sidebar */ }

    func validateMenuItem(_ menuItem: NSMenuItem) -> Bool {
        switch menuItem.action {
        case #selector(copy(_:)):
            // Enable copy when there's a selection
            return true
        case #selector(paste(_:)):
            return NSPasteboard.general.canReadObject(forClasses: [NSString.self], options: [:])
        case #selector(toggleSidebar(_:)):
            menuItem.title = "Hide Sidebar" // or "Show Sidebar"
            return true
        default:
            return true
        }
    }
}
