import AppKit

final class DragAndDropView: NSView, NSDraggingDestination {
    private let supportedTypes = [NSPasteboard.PasteboardType.fileURL]

    override init(frame frameRect: NSRect) {
        super.init(frame: frameRect)
        registerForDraggedTypes(supportedTypes)
        wantsLayer = true
        layer?.backgroundColor = NSColor.windowBackgroundColor.cgColor
    }

    required init?(coder: NSCoder) { super.init(coder: coder) }

    func draggingEntered(_ sender: NSDraggingInfo) -> NSDragOperation {
        return .copy
    }

    func performDragOperation(_ sender: NSDraggingInfo) -> Bool {
        let pasteboard = sender.draggingPasteboard
        if let items = pasteboard.pasteboardItems {
            for item in items {
                if let file = item.string(forType: .fileURL), let url = URL(string: file) {
                    Swift.print("Dropped file:", url.path)
                }
            }
        }
        return true
    }

    override func draw(_ dirtyRect: NSRect) {
        NSColor.quaternaryLabelColor.setStroke()
        NSBezierPath(roundedRect: bounds.insetBy(dx: 8, dy: 8), xRadius: 8, yRadius: 8).stroke()
        let attrs: [NSAttributedString.Key: Any] = [
            .font: NSFont.systemFont(ofSize: 14, weight: .semibold),
            .foregroundColor: NSColor.secondaryLabelColor
        ]
        let s = NSString(string: "Drop files here")
        let size = s.size(withAttributes: attrs)
        s.draw(at: NSPoint(x: bounds.midX - size.width/2, y: bounds.midY - size.height/2), withAttributes: attrs)
    }
}
