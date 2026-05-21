import SwiftUI
import UIKit

// Example custom UIKit control
final class CounterControl: UIControl {
    private(set) var value: Int = 0 {
        didSet { sendActions(for: .valueChanged) }
    }
    func increment() { value += 1 }
}

struct CounterBridge: UIViewRepresentable {
    typealias UIViewType = CounterControl
    @Binding var value: Int

    func makeCoordinator() -> Coordinator { Coordinator(self) }

    func makeUIView(context: Context) -> CounterControl {
        let c = CounterControl()
        context.coordinator.control = c
        c.addTarget(context.coordinator, action: #selector(Coordinator.valueChanged), for: .valueChanged)
        return c
    }

    func updateUIView(_ uiView: CounterControl, context: Context) {
        if uiView.value != value { // avoid recursion
            // drive UIKit control from SwiftUI state if needed
        }
    }

    static func dismantleUIView(_ uiView: CounterControl, coordinator: Coordinator) {
        uiView.removeTarget(nil, action: nil, for: .allEvents)
    }

    final class Coordinator: NSObject {
        weak var control: CounterControl?
        var parent: CounterBridge

        init(_ parent: CounterBridge) { self.parent = parent }

        @objc func valueChanged() {
            // pull value from control to SwiftUI
            guard let control = control else { return }
            parent.value = control.value
        }
    }
}
