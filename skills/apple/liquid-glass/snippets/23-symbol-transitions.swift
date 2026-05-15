import SwiftUI

@available(iOS 26.0, *)
struct SymbolTransitionStateButton: View {
    enum StateKind { case idle, streaming, recording }
    @State private var state: StateKind = .idle

    var body: some View {
        GlassEffectContainer(spacing: 10) {
            HStack(spacing: 10) {
                Button(title, systemImage: symbol) { advance() }
                    .symbolTransitionGlassStyle(state == .idle)
                    .tint(tint)
                    .contentTransition(.symbolEffect(.replace))
                    .accessibilityLabel(accessibilityLabel)

                Button("Reset", systemImage: "arrow.counterclockwise") { state = .idle }
                    .buttonStyle(.glass)
            }
        }
    }

    private var title: String {
        switch state { case .idle: "Send"; case .streaming: "Stop"; case .recording: "Recording" }
    }

    private var symbol: String {
        switch state { case .idle: "arrow.up"; case .streaming: "stop.fill"; case .recording: "waveform.circle.fill" }
    }

    private var tint: Color {
        switch state { case .idle: .accentColor; case .streaming: .red; case .recording: .red }
    }

    private var accessibilityLabel: String {
        switch state { case .idle: "Send prompt"; case .streaming: "Stop streaming"; case .recording: "Stop voice recording" }
    }

    private func advance() {
        withAnimation(.spring(response: 0.28, dampingFraction: 0.82)) {
            switch state { case .idle: state = .streaming; case .streaming: state = .recording; case .recording: state = .idle }
        }
    }
}

@available(iOS 26.0, *)
private extension View {
    @ViewBuilder
    func symbolTransitionGlassStyle(_ isProminent: Bool) -> some View {
        if isProminent { self.buttonStyle(.glassProminent) }
        else { self.buttonStyle(.glass) }
    }
}

#Preview {
    if #available(iOS 26.0, *) { SymbolTransitionStateButton().padding() }
}
