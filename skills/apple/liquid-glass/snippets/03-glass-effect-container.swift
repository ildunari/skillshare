import SwiftUI

@available(iOS 26.0, *)
struct GlassContainerToolbar: View {
    var body: some View {
        GlassEffectContainer(spacing: 10) {
            HStack(spacing: 10) {
                Button("Search", systemImage: "magnifyingglass") {}
                    .buttonStyle(.glass)
                Button("Filter", systemImage: "line.3.horizontal.decrease") {}
                    .buttonStyle(.glass)
                Button("New", systemImage: "plus") {}
                    .buttonStyle(.glassProminent)
            }
        }
        .padding()
    }
}
