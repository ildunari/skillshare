import SwiftUI

struct MailLikeSidebar: View {
    enum Box: Hashable { case inbox, drafts, sent, archive }
    @State private var selection: Box? = .inbox

    var body: some View {
        NavigationSplitView {
            List(selection: $selection) {
                Label("Inbox", systemImage: "tray").tag(Box.inbox)
                Label("Drafts", systemImage: "doc.text").tag(Box.drafts)
                Label("Sent", systemImage: "paperplane").tag(Box.sent)
                Label("Archive", systemImage: "archivebox").tag(Box.archive)
            }
            .listStyle(.sidebar)
        } detail: {
            switch selection {
            case .inbox: Text("Inbox")
            case .drafts: Text("Drafts")
            case .sent: Text("Sent")
            case .archive: Text("Archive")
            case .none: Text("Select a mailbox")
            }
        }
        .navigationSplitViewStyle(.balanced)
    }
}
