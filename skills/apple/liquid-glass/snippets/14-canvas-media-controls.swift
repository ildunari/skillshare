import SwiftUI

@available(iOS 26.0, *)
struct CanvasMediaOverlayControls: View {
    @State private var zoomed = false

    var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 28, style: .continuous)
                .fill(LinearGradient(colors: [.indigo, .cyan], startPoint: .topLeading, endPoint: .bottomTrailing))
                .overlay(alignment: .bottom) {
                    LinearGradient(colors: [.clear, .black.opacity(0.38)], startPoint: .top, endPoint: .bottom)
                }

            VStack {
                HStack {
                    GlassEffectContainer(spacing: 8) {
                        HStack(spacing: 8) {
                            Button("Back", systemImage: "chevron.left") {}.buttonStyle(.glass)
                            Button("Annotate", systemImage: "pencil.tip") {}.buttonStyle(.glass)
                        }
                    }
                    Spacer()
                    Button("Share", systemImage: "square.and.arrow.up") {}.buttonStyle(.glassProminent)
                }
                Spacer()
                HStack {
                    Text("Preview.pdf")
                        .font(.callout.weight(.semibold))
                        .padding(.horizontal, 12)
                        .padding(.vertical, 8)
                        .glassEffect(.regular, in: Capsule())
                    Spacer()
                    Button(zoomed ? "Fit" : "Zoom", systemImage: zoomed ? "arrow.down.right.and.arrow.up.left" : "arrow.up.left.and.arrow.down.right") {
                        zoomed.toggle()
                    }
                    .buttonStyle(.glass)
                    .contentTransition(.symbolEffect(.replace))
                }
            }
            .padding(16)
        }
        .frame(height: 420)
        .clipShape(RoundedRectangle(cornerRadius: 28, style: .continuous))
        .padding()
    }
}
