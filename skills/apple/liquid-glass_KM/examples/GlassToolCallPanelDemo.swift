import SwiftUI

@available(iOS 26.0, *)
struct GlassToolCallPanelDemo: View {
    @State private var expanded = true

    var body: some View {
        ZStack { GlassShowcaseBackground(); panel.padding() }
            .navigationTitle("Tool Panel")
    }

    private var panel: some View {
        VStack(alignment: .leading, spacing: 14) {
            HStack {
                Label("Tool calls", systemImage: "wrench.and.screwdriver").font(.headline)
                Spacer()
                Button(expanded ? "Collapse" : "Expand", systemImage: expanded ? "chevron.down" : "chevron.right") { withAnimation(.spring(response: 0.32, dampingFraction: 0.82)) { expanded.toggle() } }
                    .buttonStyle(.glass)
                    .contentTransition(.symbolEffect(.replace))
            }
            HStack(spacing: 8) {
                chip("Web search", "network", .orange)
                chip("Files", "paperclip", .green)
                chip("Canvas", "rectangle.on.rectangle", .blue)
            }
            if expanded {
                Text("Readable reasoning text stays on a plain background. The glass edge and chips show status without reducing legibility.")
                    .foregroundStyle(.secondary)
                    .transition(.opacity)
            }
        }
        .padding(16)
        .background(.background.opacity(0.92), in: RoundedRectangle(cornerRadius: 24, style: .continuous))
        .overlay(alignment: .leading) { Capsule().frame(width: 4).padding(.vertical, 18).glassEffect(.regular, in: Capsule()) }
    }

    private func chip(_ title: String, _ symbol: String, _ color: Color) -> some View {
        Label(title, systemImage: symbol).font(.caption.weight(.semibold)).padding(.horizontal, 10).padding(.vertical, 7).glassEffect(.regular.tint(color.opacity(0.22)), in: Capsule())
    }
}

#Preview { if #available(iOS 26.0, *) { NavigationStack { GlassToolCallPanelDemo() } } }
