import SwiftUI

@available(iOS 26.0, *)
struct AgentThreadRowControls: View {
    let title: String
    let subtitle: String
    let isPinned: Bool

    var body: some View {
        HStack(spacing: 12) {
            VStack(alignment: .leading, spacing: 4) {
                Text(title).font(.headline)
                Text(subtitle).font(.subheadline).foregroundStyle(.secondary)
            }
            Spacer()
            GlassEffectContainer(spacing: 8) {
                HStack(spacing: 8) {
                    Button(isPinned ? "Unpin" : "Pin", systemImage: isPinned ? "pin.fill" : "pin") {}
                        .threadControlsGlassStyle(isPinned)
                        .contentTransition(.symbolEffect(.replace))
                    Button("More", systemImage: "ellipsis") {}
                        .buttonStyle(.glass)
                }
            }
        }
        .padding(.vertical, 10)
    }
}

@available(iOS 26.0, *)
struct ThreadFilterPills: View {
    @State private var selected = "All"
    let filters = ["All", "Pinned", "Running", "Unread"]

    var body: some View {
        GlassEffectContainer(spacing: 8) {
            HStack(spacing: 8) {
                ForEach(filters, id: \.self) { filter in
                    Button(filter) { selected = filter }
                        .threadControlsGlassStyle(selected == filter)
                }
            }
        }
    }
}

@available(iOS 26.0, *)
private extension View {
    @ViewBuilder
    func threadControlsGlassStyle(_ isSelected: Bool) -> some View {
        if isSelected {
            self.buttonStyle(.glassProminent)
        } else {
            self.buttonStyle(.glass)
        }
    }
}
