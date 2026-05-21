import SwiftUI

@available(iOS 26.0, *)
struct AdaptiveGlassShell<Content: View>: View {
    @Environment(\.accessibilityReduceTransparency) private var reduceTransparency
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @Environment(\.accessibilityContrast) private var contrast
    @Environment(\.accessibilityDifferentiateWithoutColor) private var differentiateWithoutColor

    var cornerRadius: CGFloat = 26
    var tint: Color? = nil
    @ViewBuilder var content: Content

    var body: some View {
        content
            .padding(12)
            .background {
                RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                    .fill(reduceTransparency ? Color(.secondarySystemBackground) : .clear)
                    .overlay {
                        RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                            .stroke(borderStyle, lineWidth: contrast == .increased ? 1.2 : 0.7)
                    }
                    .modifier(ConditionalGlassModifier(enabled: !reduceTransparency, tint: tint))
            }
            .animation(reduceMotion ? .easeOut(duration: 0.12) : .spring(response: 0.32, dampingFraction: 0.82), value: reduceTransparency)
            .accessibilityElement(children: .contain)
    }

    private var borderStyle: some ShapeStyle {
        if differentiateWithoutColor || contrast == .increased {
            return AnyShapeStyle(.primary.opacity(0.28))
        } else {
            return AnyShapeStyle(.white.opacity(0.18))
        }
    }
}

@available(iOS 26.0, *)
private struct ConditionalGlassModifier: ViewModifier {
    let enabled: Bool
    let tint: Color?

    func body(content: Content) -> some View {
        if enabled, let tint {
            content.glassEffect(.regular.tint(tint.opacity(0.22)).interactive())
        } else if enabled {
            content.glassEffect(.regular.interactive())
        } else {
            content
        }
    }
}

@available(iOS 26.0, *)
struct AdaptiveGlassComposerAccessorySnippet: View {
    @State private var running = true

    var body: some View {
        AdaptiveGlassShell(tint: running ? .blue : nil) {
            HStack(spacing: 10) {
                Label(running ? "Agent running" : "Agent idle", systemImage: running ? "bolt.fill" : "pause.circle")
                    .font(.footnote.weight(.semibold))
                Spacer()
                Button(running ? "Stop" : "Start", systemImage: running ? "stop.fill" : "play.fill") {
                    running.toggle()
                }
                .adaptiveProminentStyle(running)
                .tint(running ? .red : .blue)
                .accessibilityLabel(running ? "Stop active agent" : "Start agent")
            }
        }
        .padding()
    }
}

@available(iOS 26.0, *)
#Preview("Adaptive glass shell") {
    AdaptiveGlassComposerAccessorySnippet()
}


@available(iOS 26.0, *)
private extension View {
    @ViewBuilder
    func adaptiveProminentStyle(_ isProminent: Bool) -> some View {
        if isProminent {
            self.buttonStyle(.glassProminent)
        } else {
            self.buttonStyle(.glass)
        }
    }
}
