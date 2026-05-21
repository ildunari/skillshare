import SwiftUI

@available(iOS 26.0, *)
struct LiquidGlassComposerSnippet: View {
    @Environment(\.accessibilityReduceTransparency) private var reduceTransparency
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var text = ""
    @State private var toolsExpanded = false
    @State private var streaming = false

    var body: some View {
        VStack(spacing: 10) {
            if toolsExpanded {
                HStack(spacing: 8) {
                    ComposerChip(title: "Web", icon: "network")
                    ComposerChip(title: "Files", icon: "paperclip")
                    ComposerChip(title: "Canvas", icon: "rectangle.on.rectangle")
                    Spacer(minLength: 0)
                }
                .transition(.move(edge: .bottom).combined(with: .opacity))
            }

            GlassEffectContainer(spacing: 10) {
                HStack(alignment: .bottom, spacing: 10) {
                    Button("Tools", systemImage: toolsExpanded ? "xmark" : "plus") {
                        withAnimation(reduceMotion ? .easeOut(duration: 0.12) : .spring(response: 0.34, dampingFraction: 0.78)) {
                            toolsExpanded.toggle()
                        }
                    }
                    .buttonStyle(.glass)
                    .contentTransition(.symbolEffect(.replace))

                    TextField("Ask the agent…", text: $text, axis: .vertical)
                        .lineLimit(1...5)
                        .textFieldStyle(.plain)
                        .padding(.horizontal, 14)
                        .padding(.vertical, 12)
                        .background(composerFieldBackground)

                    Button(streaming ? "Stop" : "Send", systemImage: streaming ? "stop.fill" : "arrow.up") {
                        streaming.toggle()
                    }
                    .buttonStyle(.glassProminent)
                    .tint(streaming ? .red : .accentColor)
                    .contentTransition(.symbolEffect(.replace))
                    .disabled(text.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty && !streaming)
                }
            }
        }
        .padding(.horizontal)
        .padding(.vertical, 10)
    }

    @ViewBuilder private var composerFieldBackground: some View {
        let shape = RoundedRectangle(cornerRadius: 24, style: .continuous)
        if reduceTransparency {
            shape.fill(.background).overlay(shape.stroke(.separator.opacity(0.5)))
        } else {
            shape.glassEffect(.regular.interactive(), in: shape)
        }
    }
}

@available(iOS 26.0, *)
private struct ComposerChip: View {
    let title: String
    let icon: String
    var body: some View {
        Label(title, systemImage: icon)
            .font(.footnote.weight(.semibold))
            .padding(.horizontal, 12)
            .padding(.vertical, 8)
            .glassEffect(.regular, in: Capsule())
    }
}
