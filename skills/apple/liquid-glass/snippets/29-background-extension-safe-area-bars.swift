import SwiftUI

@available(iOS 26.0, *)
struct BackgroundExtensionSafeAreaBarsSnippet: View {
    @State private var message = ""

    var body: some View {
        NavigationSplitView {
            List(["Canvas", "PDF", "Image"], id: \.self) { item in
                Label(item, systemImage: "rectangle.on.rectangle")
            }
            .navigationTitle("Library")
        } detail: {
            MediaDetailWithExtendedBackground(message: $message)
        }
    }
}

@available(iOS 26.0, *)
private struct MediaDetailWithExtendedBackground: View {
    @Binding var message: String

    var body: some View {
        ZStack {
            LinearGradient(colors: [.indigo, .blue, .purple], startPoint: .topLeading, endPoint: .bottomTrailing)
                .backgroundExtensionEffect()
                .ignoresSafeArea()

            VStack(spacing: 16) {
                Image(systemName: "photo.on.rectangle.angled")
                    .font(.system(size: 72, weight: .semibold))
                    .foregroundStyle(.white.opacity(0.82))

                Text("Media canvas")
                    .font(.largeTitle.bold())
                    .foregroundStyle(.white)

                Text("The background extension effect helps this media surface continue under sidebars or inspectors; the controls remain the glass layer.")
                    .font(.callout)
                    .multilineTextAlignment(.center)
                    .foregroundStyle(.white.opacity(0.8))
                    .padding(.horizontal)
            }
        }
        .safeAreaBar(edge: .bottom, spacing: 0) {
            GlassEffectContainer(spacing: 8) {
                HStack(spacing: 8) {
                    Button("Attach", systemImage: "paperclip") {}
                        .buttonStyle(.glass)

                    TextField("Ask about this canvas", text: $message)
                        .textFieldStyle(.plain)
                        .padding(.horizontal, 12)
                        .padding(.vertical, 10)
                        .glassEffect(.regular, in: Capsule())

                    Button("Send", systemImage: "arrow.up") {}
                        .buttonStyle(.glassProminent)
                }
                .padding(.horizontal, 12)
                .padding(.vertical, 10)
            }
            .padding(.horizontal, 12)
            .padding(.bottom, 8)
        }
    }
}

@available(iOS 26.0, *)
#Preview("Background extension + safe-area bar") {
    BackgroundExtensionSafeAreaBarsSnippet()
}
