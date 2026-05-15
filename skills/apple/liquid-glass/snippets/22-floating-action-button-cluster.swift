import SwiftUI

@available(iOS 26.0, *)
struct FloatingActionButtonClusterSnippet: View {
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @Namespace private var namespace
    @State private var expanded = false

    private let actions = [
        ("New chat", "plus.bubble"),
        ("Upload", "paperclip"),
        ("Canvas", "rectangle.on.rectangle"),
        ("Image", "photo")
    ]

    var body: some View {
        GlassEffectContainer(spacing: 10) {
            VStack(alignment: .trailing, spacing: 10) {
                if expanded {
                    ForEach(actions, id: \.0) { action in
                        Button(action.0, systemImage: action.1) {}
                            .buttonStyle(.glass)
                            .glassEffectID(action.0, in: namespace)
                            .transition(.move(edge: .bottom).combined(with: .opacity).combined(with: .scale))
                    }
                }

                Button(expanded ? "Close" : "Create", systemImage: expanded ? "xmark" : "plus") {
                    withAnimation(reduceMotion ? .easeOut(duration: 0.12) : .spring(response: 0.34, dampingFraction: 0.74)) {
                        expanded.toggle()
                    }
                }
                .buttonStyle(.glassProminent)
                .glassEffectID("fab-primary", in: namespace)
                .contentTransition(.symbolEffect(.replace))
                .accessibilityLabel(expanded ? "Close create menu" : "Open create menu")
            }
        }
        .padding()
    }
}

#Preview {
    if #available(iOS 26.0, *) {
        FloatingActionButtonClusterSnippet()
            .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .bottomTrailing)
            .background(LinearGradient(colors: [.blue, .purple], startPoint: .topLeading, endPoint: .bottomTrailing))
    }
}
