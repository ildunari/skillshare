import SwiftUI

@available(iOS 26.0, *)
struct SearchFilterPillControls: View {
    @State private var query = ""
    @State private var selected = "All"

    var body: some View {
        GlassEffectContainer(spacing: 8) {
            HStack(spacing: 8) {
                Label("Search", systemImage: "magnifyingglass")
                    .labelStyle(.iconOnly)
                    .padding(.leading, 12)
                TextField("Search threads", text: $query)
                    .textFieldStyle(.plain)
                    .frame(minWidth: 120)

                Divider().frame(height: 24)

                ForEach(["All", "Pinned", "Running"], id: \.self) { filter in
                    Button(filter) { selected = filter }
                        .filterPillsGlassStyle(selected == filter)
                }
            }
            .padding(8)
            .glassEffect(.regular.interactive(), in: Capsule())
        }
    }
}

@available(iOS 26.0, *)
private extension View {
    @ViewBuilder
    func filterPillsGlassStyle(_ isSelected: Bool) -> some View {
        if isSelected {
            self.buttonStyle(.glassProminent)
        } else {
            self.buttonStyle(.glass)
        }
    }
}
