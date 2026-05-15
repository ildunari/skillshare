import SwiftUI

@available(iOS 26.0, *)
struct AgentThinkingPill: View {
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var phase = 0

    var body: some View {
        HStack(spacing: 8) {
            Image(systemName: "sparkles")
                .symbolEffect(.pulse, options: reduceMotion ? .nonRepeating : .repeating, value: phase)
            Text("Agent is thinking")
            HStack(spacing: 3) {
                ForEach(0..<3) { index in
                    Circle()
                        .frame(width: 4, height: 4)
                        .opacity(reduceMotion ? 0.55 : (phase + index) % 3 == 0 ? 1 : 0.35)
                }
            }
        }
        .font(.caption.weight(.semibold))
        .padding(.horizontal, 12)
        .padding(.vertical, 8)
        .glassEffect(.regular.tint(.orange.opacity(0.16)), in: Capsule())
        .onAppear {
            guard !reduceMotion else { return }
            withAnimation(.easeInOut(duration: 0.8).repeatForever()) { phase = 1 }
        }
    }
}
