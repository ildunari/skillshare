import SwiftUI

@available(iOS 26.0, *)
public struct GalleryBrowserRecipe: View {
    @Namespace private var namespace
    private let items = Array(0..<12)

    public init() {}

    public var body: some View {
        NavigationStack {
            ScrollView {
                LazyVGrid(columns: [GridItem(.adaptive(minimum: 150), spacing: 14)], spacing: 14) {
                    ForEach(items, id: \.self) { item in
                        NavigationLink(value: item) {
                            RoundedRectangle(cornerRadius: 22, style: .continuous)
                                .fill(LinearGradient(colors: [.blue.opacity(0.8), .purple.opacity(0.8)], startPoint: .topLeading, endPoint: .bottomTrailing))
                                .frame(height: 150)
                                .overlay(alignment: .bottomLeading) {
                                    Text("Preview \(item + 1)")
                                        .font(.caption.weight(.bold))
                                        .padding(8)
                                        .glassEffect(.regular, in: Capsule())
                                        .padding(10)
                                }
                                .matchedTransitionSource(id: item, in: namespace)
                        }
                        .buttonStyle(.plain)
                    }
                }.padding()
            }
            .navigationTitle("Gallery")
            .toolbar { ToolbarItem(placement: .topBarTrailing) { Button("Filter", systemImage: "line.3.horizontal.decrease") {}.buttonStyle(.glass) } }
            .navigationDestination(for: Int.self) { item in
                GalleryDetail(item: item)
                    .navigationTransition(.zoom(sourceID: item, in: namespace))
            }
        }
    }
}

@available(iOS 26.0, *)
private struct GalleryDetail: View {
    let item: Int
    var body: some View {
        ZStack(alignment: .bottom) {
            LinearGradient(colors: [.blue, .purple, .pink], startPoint: .topLeading, endPoint: .bottomTrailing).ignoresSafeArea()
            GlassEffectContainer(spacing: 8) {
                HStack(spacing: 8) {
                    Button("Annotate", systemImage: "pencil.tip") {}.buttonStyle(.glass)
                    Button("Share", systemImage: "square.and.arrow.up") {}.buttonStyle(.glassProminent)
                }
            }.padding()
        }
        .navigationTitle("Preview \(item + 1)")
    }
}

#Preview {
    if #available(iOS 26.0, *) { GalleryBrowserRecipe() }
}
