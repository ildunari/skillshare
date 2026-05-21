import SwiftUI

@available(iOS 26.0, *)
struct GlassBasicsSnippet: View {
    @Environment(\.accessibilityReduceTransparency) private var reduceTransparency

    var body: some View {
        VStack(spacing: 20) {
            Text("Native Liquid Glass")
                .font(.headline)
                .padding(.horizontal, 18)
                .padding(.vertical, 12)
                .background(glassBackground(shape: Capsule()))

            HStack(spacing: 12) {
                Label("Tools", systemImage: "slider.horizontal.3")
                Spacer()
                Image(systemName: "chevron.up")
            }
            .padding(16)
            .background(glassBackground(shape: RoundedRectangle(cornerRadius: 24, style: .continuous)))
        }
        .padding()
    }

    @ViewBuilder
    private func glassBackground<S: Shape>(shape: S) -> some View {
        if reduceTransparency {
            shape.fill(.background)
                .overlay(shape.stroke(.separator.opacity(0.7), lineWidth: 1))
        } else {
            shape.glassEffect(.regular, in: shape)
        }
    }
}

#Preview {
    if #available(iOS 26.0, *) {
        GlassBasicsSnippet()
            .background(LinearGradient(colors: [.blue, .purple], startPoint: .topLeading, endPoint: .bottomTrailing))
    }
}
