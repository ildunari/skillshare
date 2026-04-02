import SwiftUI

/// Demonstrates the difference between @StateObject and @ObservedObject.
/// ViewModel persists when owned by @StateObject, but not when recreated.
final class CounterViewModel: ObservableObject {
    @Published var count: Int = 0
    init() {
        print("CounterViewModel init")
    }
}

struct StateObjectView: View {
    @StateObject private var viewModel = CounterViewModel()
    var body: some View {
        VStack {
            Text("StateObject count: \(viewModel.count)")
            Button("Increment") { viewModel.count += 1 }
        }
        .padding()
    }
}

struct ObservedObjectView: View {
    @ObservedObject var viewModel: CounterViewModel
    var body: some View {
        VStack {
            Text("ObservedObject count: \(viewModel.count)")
            Button("Increment") { viewModel.count += 1 }
        }
        .padding()
    }
}

struct ObjectStateDemo: View {
    @State private var toggle = false
    var body: some View {
        VStack {
            Button("Toggle View") { toggle.toggle() }
            if toggle {
                StateObjectView()
            } else {
                ObservedObjectView(viewModel: CounterViewModel())
            }
        }
    }
}

struct ObjectStateDemo_Previews: PreviewProvider {
    static var previews: some View {
        ObjectStateDemo()
    }
}