import SwiftUI

@available(iOS 26.0, *)
struct GlassButtonsAndTint: View {
    @State private var isStreaming = false
    @State private var isRecording = false

    var body: some View {
        GlassEffectContainer(spacing: 12) {
            HStack(spacing: 12) {
                Button("Attach", systemImage: "paperclip") {}
                    .buttonStyle(.glass)

                Button(isRecording ? "Stop recording" : "Voice", systemImage: isRecording ? "stop.fill" : "mic.fill") {
                    withAnimation(.spring(response: 0.3, dampingFraction: 0.75)) {
                        isRecording.toggle()
                    }
                }
                .buttonStyle(.glass)
                .tint(isRecording ? .red : .primary)
                .contentTransition(.symbolEffect(.replace))

                Button(isStreaming ? "Stop" : "Send", systemImage: isStreaming ? "stop.fill" : "arrow.up") {
                    withAnimation(.spring(response: 0.28, dampingFraction: 0.8)) {
                        isStreaming.toggle()
                    }
                }
                .buttonStyle(.glassProminent)
                .tint(isStreaming ? .red : .accentColor)
                .contentTransition(.symbolEffect(.replace))
            }
        }
    }
}
