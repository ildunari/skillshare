import AppKit

final class WindowRestorationExample: NSWindowController, NSWindowDelegate, NSWindowRestoration {
    static func restoreWindow(withIdentifier identifier: NSUserInterfaceItemIdentifier, state: NSCoder, completionHandler: @escaping (NSWindow?, Error?) -> Void) {
        let wc = WindowRestorationExample()
        completionHandler(wc.window, nil)
    }

    convenience init() {
        let window = NSWindow(contentRect: NSRect(x: 0, y: 0, width: 640, height: 400),
                              styleMask: [.titled, .closable, .resizable, .miniaturizable],
                              backing: .buffered, defer: false)
        window.isRestorable = true
        window.identifier = NSUserInterfaceItemIdentifier("RestorableWindow")
        window.setFrameAutosaveName("RestorableWindow")
        self.init(window: window)
        window.delegate = self
        type(of: self).register(as: "RestorableWindow", restorationClass: type(of: self))
    }

    func window(_ window: NSWindow, willEncodeRestorableState state: NSCoder) {
        state.encode(1, forKey: "version")
    }

    func window(_ window: NSWindow, didDecodeRestorableState state: NSCoder) {
        let _ = state.decodeInteger(forKey: "version")
    }
}
