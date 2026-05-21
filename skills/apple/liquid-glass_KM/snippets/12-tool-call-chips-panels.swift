import SwiftUI

@available(iOS 26.0, *)
struct ToolCallStatusChip: View {
    enum Status { case running, success, failed }
    let title: String
    let status: Status

    var body: some View {
        Label(title, systemImage: symbol)
            .font(.caption.weight(.semibold))
            .padding(.horizontal, 10)
            .padding(.vertical, 7)
            .glassEffect(.regular.tint(tint.opacity(0.22)).interactive(), in: Capsule())
            .accessibilityLabel("\(title), \(accessibilityStatus)")
    }

    private var symbol: String { status == .running ? "arrow.triangle.2.circlepath" : status == .success ? "checkmark" : "exclamationmark.triangle" }
    private var tint: Color { status == .running ? .orange : status == .success ? .green : .red }
    private var accessibilityStatus: String { status == .running ? "running" : status == .success ? "complete" : "failed" }
}

@available(iOS 26.0, *)
struct CollapsibleToolPanel: View {
    @State private var expanded = false

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            Button {
                withAnimation(.spring(response: 0.32, dampingFraction: 0.82)) { expanded.toggle() }
            } label: {
                HStack {
                    ToolCallStatusChip(title: "Web search", status: .running)
                    Spacer()
                    Image(systemName: expanded ? "chevron.down" : "chevron.right")
                        .contentTransition(.symbolEffect(.replace))
                }
            }
            .buttonStyle(.plain)

            if expanded {
                Text("Searching trusted sources and extracting citations…")
                    .font(.callout)
                    .foregroundStyle(.secondary)
                    .transition(.opacity.combined(with: .move(edge: .top)))
            }
        }
        .padding(14)
        .background(.background, in: RoundedRectangle(cornerRadius: 18, style: .continuous))
        .overlay(alignment: .trailing) {
            Capsule()
                .frame(width: 4)
                .glassEffect(.regular, in: Capsule())
                .padding(.vertical, 12)
        }
    }
}
