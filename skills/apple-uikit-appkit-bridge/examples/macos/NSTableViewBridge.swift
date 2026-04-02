import SwiftUI
import AppKit

struct TableViewMacBridge: NSViewRepresentable {
    typealias NSViewType = NSScrollView

    @Binding var items: [String]
    var onSelect: ((Int) -> Void)?

    func makeCoordinator() -> Coordinator { Coordinator(self) }

    func makeNSView(context: Context) -> NSScrollView {
        let scroll = NSScrollView()
        let table = NSTableView()
        let column = NSTableColumn(identifier: .init("col"))
        column.title = "Items"
        table.addTableColumn(column)
        table.headerView = nil
        table.delegate = context.coordinator
        table.dataSource = context.coordinator
        scroll.documentView = table
        return scroll
    }

    func updateNSView(_ nsView: NSScrollView, context: Context) {
        context.coordinator.parent = self
        (nsView.documentView as? NSTableView)?.reloadData()
    }

    static func dismantleNSView(_ nsView: NSScrollView, coordinator: Coordinator) {
        if let t = nsView.documentView as? NSTableView {
            t.delegate = nil; t.dataSource = nil
        }
    }

    final class Coordinator: NSObject, NSTableViewDelegate, NSTableViewDataSource {
        var parent: TableViewMacBridge
        init(_ parent: TableViewMacBridge) { self.parent = parent }
        func numberOfRows(in tableView: NSTableView) -> Int { parent.items.count }
        func tableView(_ tableView: NSTableView, viewFor tableColumn: NSTableColumn?, row: Int) -> NSView? {
            let id = NSUserInterfaceItemIdentifier("cell")
            let v = tableView.makeView(withIdentifier: id, owner: nil) as? NSTableCellView ?? {
                let c = NSTableCellView()
                c.identifier = id
                c.textField = NSTextField(labelWithString: "")
                c.addSubview(c.textField!)
                c.textField!.translatesAutoresizingMaskIntoConstraints = false
                NSLayoutConstraint.activate([
                    c.textField!.leadingAnchor.constraint(equalTo: c.leadingAnchor, constant: 8),
                    c.textField!.centerYAnchor.constraint(equalTo: c.centerYAnchor)
                ])
                return c
            }()
            v.textField?.stringValue = parent.items[row]
            return v
        }
        func tableViewSelectionDidChange(_ notification: Notification) {
            guard let t = notification.object as? NSTableView else { return }
            parent.onSelect?(t.selectedRow)
        }
    }
}
