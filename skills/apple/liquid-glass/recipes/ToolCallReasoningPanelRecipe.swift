import SwiftUI

@available(iOS 26.0, *)
public struct ToolCallReasoningPanelRecipe: View {
    @State private var expanded = true

    public init() {}

    public var body: some View {
        VStack(alignment: .leading, spacing: 14) {
            HStack {
                Label("Reasoning", systemImage: "brain.head.profile")
                    .font(.headline)
                Spacer()
                Button(expanded ? "Collapse" : "Expand", systemImage: expanded ? "chevron.down" : "chevron.right") {
                    withAnimation(.spring(response: 0.32, dampingFraction: 0.84)) { expanded.toggle() }
                }
                .buttonStyle(.glass)
                .contentTransition(.symbolEffect(.replace))
            }

            HStack(spacing: 8) {
                StatusChip(title: "Web", symbol: "network", tint: .orange)
                StatusChip(title: "Files", symbol: "paperclip", tint: .green)
                StatusChip(title: "Code", symbol: "curlybraces", tint: .blue)
            }

            if expanded {
                VStack(alignment: .leading, spacing: 8) {
                    Text("The panel body is intentionally plain and readable. Glass lives on the controls, status chips, and edge handle.")
                    Text("• Searching sources\n• Comparing snippets\n• Preparing implementation")
                        .foregroundStyle(.secondary)
                }
                .font(.callout)
                .transition(.opacity.combined(with: .move(edge: .top)))
            }
        }
        .padding(16)
        .background(.background, in: RoundedRectangle(cornerRadius: 22, style: .continuous))
        .overlay(alignment: .leading) {
            Capsule().frame(width: 4).padding(.vertical, 18).glassEffect(.regular, in: Capsule())
        }
        .padding()
    }
}

@available(iOS 26.0, *)
private struct StatusChip: View {
    let title: String
    let symbol: String
    let tint: Color
    var body: some View {
        Label(title, systemImage: symbol)
            .font(.caption.weight(.semibold))
            .padding(.horizontal, 10)
            .padding(.vertical, 7)
            .glassEffect(.regular.tint(tint.opacity(0.2)), in: Capsule())
    }
}

#Preview {
    if #available(iOS 26.0, *) { ToolCallReasoningPanelRecipe() }
}
