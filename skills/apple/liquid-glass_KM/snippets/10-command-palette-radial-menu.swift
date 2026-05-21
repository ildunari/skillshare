import SwiftUI

@available(iOS 26.0, *)
struct RadialGlassMenu: View {
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var expanded = false
    private let actions: [(String, String)] = [
        ("web", "network"), ("files", "paperclip"), ("image", "photo"), ("code", "curlybraces")
    ]

    var body: some View {
        ZStack {
            ForEach(Array(actions.enumerated()), id: \.offset) { index, action in
                Button(action.0.capitalized, systemImage: action.1) {}
                    .buttonStyle(.glass)
                    .offset(expanded ? offset(for: index) : .zero)
                    .opacity(expanded ? 1 : 0)
                    .scaleEffect(expanded ? 1 : 0.6)
            }

            Button(expanded ? "Close" : "Actions", systemImage: expanded ? "xmark" : "sparkles") {
                withAnimation(reduceMotion ? .easeOut(duration: 0.12) : .spring(response: 0.36, dampingFraction: 0.72)) {
                    expanded.toggle()
                }
            }
            .buttonStyle(.glassProminent)
            .contentTransition(.symbolEffect(.replace))
        }
        .frame(width: 190, height: 190)
    }

    private func offset(for index: Int) -> CGSize {
        let angle = Double(index) / Double(max(actions.count, 1)) * .pi * 2 - .pi / 2
        return CGSize(width: cos(angle) * 78, height: sin(angle) * 78)
    }
}

@available(iOS 26.0, *)
struct GlassCommandPalette: View {
    @State private var query = ""
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            TextField("Command or prompt…", text: $query)
                .textFieldStyle(.plain)
                .padding(14)
                .glassEffect(.regular.interactive(), in: RoundedRectangle(cornerRadius: 20, style: .continuous))

            ForEach(["Summarize thread", "Create image", "Search files", "Run tool"], id: \.self) { command in
                Button(command, systemImage: "command") {}
                    .buttonStyle(.glass)
            }
        }
        .padding(16)
    }
}
