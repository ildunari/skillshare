import SwiftUI

@available(iOS 26.0, *)
struct FloatingGlassToolbar: View {
    @State private var selectedTool = "cursorarrow"
    private let tools = ["cursorarrow", "pencil.tip", "lasso", "textformat", "sparkles"]

    var body: some View {
        GlassEffectContainer(spacing: 8) {
            HStack(spacing: 8) {
                ForEach(tools, id: \.self) { tool in
                    Button {
                        withAnimation(.spring(response: 0.28, dampingFraction: 0.82)) { selectedTool = tool }
                    } label: {
                        Image(systemName: tool).frame(width: 42, height: 42)
                    }
                    .toolbarGlassStyle(selectedTool == tool)
                    .accessibilityLabel(tool)
                }
            }
        }
        .padding(10)
    }
}

@available(iOS 26.0, *)
private extension View {
    @ViewBuilder
    func toolbarGlassStyle(_ isSelected: Bool) -> some View {
        if isSelected {
            self.buttonStyle(.glassProminent)
        } else {
            self.buttonStyle(.glass)
        }
    }
}
