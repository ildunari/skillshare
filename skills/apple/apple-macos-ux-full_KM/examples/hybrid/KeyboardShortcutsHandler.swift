import AppKit

final class KeyboardShortcutsHandler: NSResponder {
    override func keyDown(with event: NSEvent) {
        if event.modifierFlags.contains(.command) && event.charactersIgnoringModifiers == "n" {
            NSApp.sendAction(#selector(newDocument(_:)), to: nil, from: self)
        } else {
            super.keyDown(with: event)
        }
    }

    @objc func newDocument(_ sender: Any?) {
        // create a new document or window
    }
}
