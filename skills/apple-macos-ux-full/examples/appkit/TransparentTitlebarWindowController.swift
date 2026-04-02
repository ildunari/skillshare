import Cocoa
import SwiftUI

final class TransparentTitlebarWindowController: NSWindowController, NSWindowDelegate {
    convenience init() {
        let content = NSHostingView(rootView: Text("Hello macOS").padding())
        let window = NSWindow(contentRect: NSRect(x: 0, y: 0, width: 880, height: 560),
                              styleMask: [.titled, .closable, .resizable, .miniaturizable],
                              backing: .buffered,
                              defer: false)
        window.titleVisibility = .hidden
        window.titlebarAppearsTransparent = true
        window.isOpaque = false
        window.center()
        window.toolbarStyle = .unified
        window.title = "Transparent Titlebar"
        window.contentView = content
        self.init(window: window)
        window.delegate = self
        window.setFrameAutosaveName("TransparentTitlebar")
    }

    func windowWillClose(_ notification: Notification) {
        // persist any custom state if needed
    }
}
