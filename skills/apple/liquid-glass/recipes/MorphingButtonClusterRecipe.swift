import SwiftUI

@available(iOS 26.0, *)
public struct MorphingButtonClusterRecipe: View {
    @Namespace private var glassNamespace
    @State private var expanded = false
    private let actions = [
        ("Search", "magnifyingglass"),
        ("Attach", "paperclip"),
        ("Canvas", "rectangle.on.rectangle"),
        ("Agent", "person.2.wave.2")
    ]

    public init() {}

    public var body: some View {
        ZStack {
            Color.secondary.opacity(0.08).ignoresSafeArea()

            GlassEffectContainer(spacing: 12) {
                HStack(spacing: 12) {
                    Button(expanded ? "Close" : "Actions", systemImage: expanded ? "xmark" : "sparkles") {
                        withAnimation(.spring(response: 0.36, dampingFraction: 0.76)) { expanded.toggle() }
                    }
                    .buttonStyle(.glassProminent)
                    .contentTransition(.symbolEffect(.replace))
                    .glassEffectID("primary", in: glassNamespace)

                    if expanded {
                        ForEach(actions, id: \.0) { action in
                            Button(action.0, systemImage: action.1) {}
                                .buttonStyle(.glass)
                                .glassEffectID(action.0, in: glassNamespace)
                                .transition(.scale.combined(with: .opacity))
                        }
                    }
                }
            }
        }
    }
}

#Preview {
    if #available(iOS 26.0, *) { MorphingButtonClusterRecipe() }
}
