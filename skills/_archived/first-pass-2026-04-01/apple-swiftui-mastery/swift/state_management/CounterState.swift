import SwiftUI

/// A simple counter using @State and @Binding.
/// The parent view owns the source of truth; the child modifies it via a binding.
struct CounterStateParent: View {
    @State private var count: Int = 0

    var body: some View {
        VStack {
            Text("Parent count: \(count)")
                .font(.headline)
            CounterStateChild(value: $count)
            Button("Reset") { count = 0 }
        }
        .padding()
    }
}

struct CounterStateChild: View {
    @Binding var value: Int
    var body: some View {
        VStack {
            Text("Child count: \(value)")
            HStack {
                Button("-1") { value -= 1 }
                Button("+1") { value += 1 }
            }
        }
    }
}

struct CounterStateParent_Previews: PreviewProvider {
    static var previews: some View {
        CounterStateParent()
    }
}