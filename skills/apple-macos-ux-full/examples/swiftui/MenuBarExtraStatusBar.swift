import SwiftUI

@available(macOS 13.0, *)
struct UtilityMenuBar: Scene {
    var body: some Scene {
        MenuBarExtra("Utility") {
            VStack(alignment: .leading) {
                Text("MenuBar Utility")
                Divider()
                Button("Quit") { NSApp.terminate(nil) }
            }
            .padding(8)
            .frame(width: 200)
        }
    }
}
