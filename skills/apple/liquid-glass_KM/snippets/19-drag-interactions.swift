import SwiftUI

@available(iOS 26.0, *)
struct SpringyGlassDrawerHandle: View {
    @GestureState private var dragY: CGFloat = 0
    @State private var expanded = false

    var body: some View {
        VStack(spacing: 10) {
            Capsule().frame(width: 42, height: 5).foregroundStyle(.secondary)
            Text(expanded ? "Tools expanded" : "Drag for tools")
                .font(.footnote.weight(.semibold))
        }
        .padding(.horizontal, 22)
        .padding(.vertical, 12)
        .glassEffect(.regular.interactive(), in: Capsule())
        .offset(y: dragY)
        .gesture(
            DragGesture(minimumDistance: 8)
                .updating($dragY) { value, state, _ in
                    state = max(-80, min(40, value.translation.height))
                }
                .onEnded { value in
                    let projected = value.translation.height + value.velocity.height * 0.12
                    withAnimation(.interpolatingSpring(stiffness: 260, damping: 28)) {
                        expanded = projected < -44
                    }
                }
        )
    }
}
