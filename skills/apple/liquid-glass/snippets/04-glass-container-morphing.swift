import SwiftUI

@available(iOS 26.0, *)
struct MorphingGlassCluster: View {
    @Namespace private var glassNamespace
    @State private var expanded = false

    var body: some View {
        GlassEffectContainer(spacing: 12) {
            HStack(spacing: 12) {
                Button {
                    withAnimation(.spring(response: 0.36, dampingFraction: 0.78)) {
                        expanded.toggle()
                    }
                } label: {
                    Label(expanded ? "Close" : "Tools", systemImage: expanded ? "xmark" : "slider.horizontal.3")
                        .contentTransition(.symbolEffect(.replace))
                }
                .buttonStyle(.glassProminent)
                .glassEffectID("cluster-primary", in: glassNamespace)

                if expanded {
                    Button("Files", systemImage: "paperclip") {}
                        .buttonStyle(.glass)
                        .glassEffectID("files", in: glassNamespace)
                    Button("Web", systemImage: "network") {}
                        .buttonStyle(.glass)
                        .glassEffectID("web", in: glassNamespace)
                    Button("Canvas", systemImage: "rectangle.on.rectangle") {}
                        .buttonStyle(.glass)
                        .glassEffectID("canvas", in: glassNamespace)
                }
            }
        }
    }
}

@available(iOS 26.0, *)
struct UnionGlassButtons: View {
    @Namespace private var unionNamespace

    var body: some View {
        GlassEffectContainer(spacing: 6) {
            HStack(spacing: 24) {
                Button("Back", systemImage: "chevron.left") {}
                    .buttonStyle(.glass)
                    .glassEffectUnion(id: "media-controls", namespace: unionNamespace)

                Button("Share", systemImage: "square.and.arrow.up") {}
                    .buttonStyle(.glass)
                    .glassEffectUnion(id: "media-controls", namespace: unionNamespace)
            }
        }
    }
}
