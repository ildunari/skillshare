import SwiftUI

@available(iOS 26.0, *)
struct GlassShaderInspiredDemo: View {
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var sweep = false

    var body: some View {
        ZStack {
            GlassShowcaseBackground()
            VStack(spacing: 24) {
                Text("Shader-inspired, public-API-safe")
                    .font(.title2.bold())
                    .multilineTextAlignment(.center)
                Button("Generate", systemImage: "sparkles") {}
                    .buttonStyle(.glassProminent)
                    .tint(.purple)
                    .overlay { highlight.mask(Capsule()).allowsHitTesting(false) }
                Text("Use overlays like this for subtle accents. Real Metal shaders belong in isolated hero effects, not ordinary controls.")
                    .font(.callout)
                    .multilineTextAlignment(.center)
                    .padding()
                    .background(.background.opacity(0.85), in: RoundedRectangle(cornerRadius: 18))
            }.padding()
        }
        .onAppear {
            guard !reduceMotion else { return }
            withAnimation(.easeInOut(duration: 1.8).repeatForever(autoreverses: false)) { sweep = true }
        }
        .navigationTitle("Highlights")
    }

    private var highlight: some View {
        Capsule()
            .strokeBorder(LinearGradient(colors: [.clear, .white.opacity(0.65), .clear], startPoint: .leading, endPoint: .trailing), lineWidth: 1.3)
            .offset(x: sweep ? 120 : -120)
            .opacity(reduceMotion ? 0 : 0.65)
    }
}

#Preview { if #available(iOS 26.0, *) { NavigationStack { GlassShaderInspiredDemo() } } }
