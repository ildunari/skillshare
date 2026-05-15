import SwiftUI

@available(iOS 26.0, *)
public struct MediaCanvasControlsRecipe: View {
    @State private var page = 3
    @State private var selectedTool = "hand.draw"

    public init() {}

    public var body: some View {
        ZStack {
            LinearGradient(colors: [.white, .blue.opacity(0.18)], startPoint: .top, endPoint: .bottom).ignoresSafeArea()
            RoundedRectangle(cornerRadius: 26, style: .continuous)
                .fill(.background)
                .shadow(radius: 18)
                .padding(30)
                .overlay(Text("PDF / image / video canvas").font(.title2.weight(.semibold)))

            VStack {
                topControls
                Spacer()
                bottomControls
            }
            .padding()
        }
    }

    private var topControls: some View {
        HStack {
            GlassEffectContainer(spacing: 8) {
                HStack(spacing: 8) {
                    Button("Back", systemImage: "chevron.left") {}.buttonStyle(.glass)
                    Button("Thumbnails", systemImage: "square.grid.2x2") {}.buttonStyle(.glass)
                    Text("Page \(page)").font(.caption.weight(.semibold)).padding(.horizontal, 10).padding(.vertical, 8).glassEffect(.regular, in: Capsule())
                }
            }
            Spacer()
            Button("Share", systemImage: "square.and.arrow.up") {}.buttonStyle(.glassProminent)
        }
    }

    private var bottomControls: some View {
        GlassEffectContainer(spacing: 8) {
            HStack(spacing: 8) {
                ForEach(["hand.draw", "pencil.tip", "textformat", "sparkles"], id: \.self) { tool in
                    Button(tool, systemImage: tool) { selectedTool = tool }
                        .mediaCanvasRecipeGlassStyle(selectedTool == tool)
                        .labelStyle(.iconOnly)
                }
            }
        }
    }
}



@available(iOS 26.0, *)
private extension View {
    @ViewBuilder
    func mediaCanvasRecipeGlassStyle(_ isSelected: Bool) -> some View {
        if isSelected {
            self.buttonStyle(.glassProminent)
        } else {
            self.buttonStyle(.glass)
        }
    }
}

#Preview {
    if #available(iOS 26.0, *) { MediaCanvasControlsRecipe() }
}
