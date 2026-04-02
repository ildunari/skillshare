import SwiftUI
import Observation

/// Demonstrates the @Observable macro introduced in iOS 17.
@Observable
class CounterModel {
    var count: Int = 0
    func increment() { count += 1 }
}

struct ObservableMacroCounter: View {
    @State private var model = CounterModel()
    var body: some View {
        VStack {
            Text("Count: \(model.count)")
                .font(.largeTitle)
            Button("Add") { model.increment() }
        }
        .padding()
    }
}

struct ObservableMacroCounter_Previews: PreviewProvider {
    static var previews: some View {
        ObservableMacroCounter()
    }
}