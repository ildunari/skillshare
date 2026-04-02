import SwiftUI

/// Demonstrates list performance patterns using Identifiable data and row view models.
final class RowViewModel: ObservableObject, Identifiable {
    let id = UUID()
    @Published var value: Int
    init(value: Int) { self.value = value }
}

struct ListPerformance: View {
    @State private var items: [RowViewModel] = (0..<100).map { RowViewModel(value: $0) }
    var body: some View {
        List {
            ForEach(items) { item in
                ListRowView(viewModel: item)
            }
        }
        .refreshable {
            // Simulate refresh by shuffling values
            items.shuffle()
        }
    }
}

struct ListRowView: View {
    @ObservedObject var viewModel: RowViewModel
    var body: some View {
        HStack {
            Text("Value: \(viewModel.value)")
            Spacer()
            Button("+1") { viewModel.value += 1 }
        }
        .padding(.vertical, 4)
    }
}

struct ListPerformance_Previews: PreviewProvider {
    static var previews: some View {
        ListPerformance()
    }
}