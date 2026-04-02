import AppKit
import SwiftUI

struct InspectorPane: View {
    var title: String
    var body: some View {
        VStack(alignment: .leading) {
            Text(title).font(.headline)
            Toggle("Show Guides", isOn: .constant(true))
            Toggle("Snap to Grid", isOn: .constant(false))
        }
        .padding(16)
        .frame(width: 260)
    }
}

final class InspectorWindowController: NSWindowController {
    convenience init() {
        let root = InspectorPane(title: "Inspector")
        let hosting = NSHostingController(rootView: root)
        let window = NSWindow(contentViewController: hosting)
        window.styleMask = [.titled, .resizable, .closable]
        window.setFrameAutosaveName("InspectorWindow")
        self.init(window: window)
    }
}
