import SwiftUI

@available(iOS 26.0, *)
struct PublicAPIShaderInspiredHighlight: View {
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var sweep = false

    var body: some View {
        Label("Generate", systemImage: "sparkles")
            .font(.headline)
            .padding(.horizontal, 20)
            .padding(.vertical, 14)
            .glassEffect(.regular.tint(.purple.opacity(0.18)).interactive(), in: Capsule())
            .overlay {
                if !reduceMotion {
                    Capsule()
                        .strokeBorder(
                            LinearGradient(
                                colors: [.clear, .white.opacity(0.55), .clear],
                                startPoint: .leading,
                                endPoint: .trailing
                            ),
                            lineWidth: 1.2
                        )
                        .offset(x: sweep ? 90 : -90)
                        .opacity(0.55)
                        .mask(Capsule())
                }
            }
            .onAppear {
                guard !reduceMotion else { return }
                withAnimation(.easeInOut(duration: 1.8).repeatForever(autoreverses: false)) {
                    sweep = true
                }
            }
    }
}

@available(iOS 26.0, *)
struct ChromaticEdgeInspiredOverlay: View {
    var body: some View {
        RoundedRectangle(cornerRadius: 28, style: .continuous)
            .strokeBorder(
                AngularGradient(colors: [.red.opacity(0.18), .blue.opacity(0.18), .green.opacity(0.14), .red.opacity(0.18)], center: .center),
                lineWidth: 1
            )
            .blendMode(.plusLighter)
            .allowsHitTesting(false)
    }
}
