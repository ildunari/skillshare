import SwiftUI

@available(iOS 26.0, *)
struct GlassCanvasControlsDemo: View {
    @State private var selected = "pencil.tip"
    private let tools = ["hand.draw", "pencil.tip", "lasso", "textformat", "sparkles"]

    var body: some View {
        ZStack {
            GlassShowcaseBackground()
            RoundedRectangle(cornerRadius: 28, style: .continuous)
                .fill(.background.opacity(0.92))
                .padding(28)
                .overlay(Text("Media / PDF / Canvas").font(.title.bold()))
            VStack {
                HStack { Button("Back", systemImage: "chevron.left") {}.buttonStyle(.glass); Spacer(); Button("Share", systemImage: "square.and.arrow.up") {}.buttonStyle(.glassProminent) }
                Spacer()
                GlassEffectContainer(spacing: 8) {
                    HStack(spacing: 8) {
                        ForEach(tools, id: \.self) { tool in
                            Button(tool, systemImage: tool) { selected = tool }
                                .showcaseGlassStyle(selected == tool)
                                .labelStyle(.iconOnly)
                        }
                    }
                }
            }.padding()
        }.navigationTitle("Canvas")
    }
}

#Preview { if #available(iOS 26.0, *) { NavigationStack { GlassCanvasControlsDemo() } } }
