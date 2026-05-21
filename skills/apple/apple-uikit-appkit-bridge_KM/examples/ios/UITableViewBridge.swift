import SwiftUI
import UIKit

struct TableBridge: UIViewRepresentable {
    typealias UIViewType = UITableView

    @Binding var items: [String]
    var onSelect: ((Int) -> Void)?

    func makeCoordinator() -> Coordinator { Coordinator(self) }

    func makeUIView(context: Context) -> UITableView {
        let tableView = UITableView(frame: .zero, style: .plain)
        tableView.register(UITableViewCell.self, forCellReuseIdentifier: "Cell")
        tableView.dataSource = context.coordinator
        tableView.delegate = context.coordinator
        tableView.rowHeight = UITableView.automaticDimension
        tableView.estimatedRowHeight = 44
        return tableView
    }

    func updateUIView(_ uiView: UITableView, context: Context) {
        context.coordinator.parent = self // refresh closures/bindings
        uiView.reloadData()
    }

    static func dismantleUIView(_ uiView: UITableView, coordinator: Coordinator) {
        uiView.dataSource = nil
        uiView.delegate = nil
    }

    final class Coordinator: NSObject, UITableViewDataSource, UITableViewDelegate {
        weak var tableView: UITableView?
        var parent: TableBridge

        init(_ parent: TableBridge) {
            self.parent = parent
        }

        deinit { print("TableBridge.Coordinator deinit") }

        func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
            self.tableView = tableView
            return parent.items.count
        }

        func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
            let cell = tableView.dequeueReusableCell(withIdentifier: "Cell", for: indexPath)
            var config = UIListContentConfiguration.cell()
            config.text = parent.items[indexPath.row]
            cell.contentConfiguration = config
            return cell
        }

        func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
            parent.onSelect?(indexPath.row)
            tableView.deselectRow(at: indexPath, animated: true)
        }
    }
}

// Preview / usage
struct TableBridgeDemo: View {
    @State private var rows = ["One", "Two", "Three"]
    var body: some View {
        TableBridge(items: $rows) { index in
            print("Selected row \(index)")
        }
        .frame(maxHeight: 300)
    }
}
