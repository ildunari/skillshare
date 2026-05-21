import SwiftUI

@available(iOS 26.0, *)
public struct FloatingToolbarRecipe: View {
    @State private var selected = "pencil.tip"
    @State private var hidden = false
    private let tools = ["cursorarrow", "pencil.tip", "highlighter", "textformat", "sparkles", "ellipsis"]

    public init() {}

    public var body: some View {
        ZStack(alignment: .topTrailing) {
            ScrollView {
                VStack(spacing: 16) {
                    ForEach(0..<18) { index in
                        RoundedRectangle(cornerRadius: 22, style: .continuous)
                            .fill(.secondary.opacity(0.08))
                            .frame(height: 120)
                            .overlay(Text("Scrollable canvas content \(index + 1)"))
                    }
                }
                .padding()
            }

            if !hidden { toolbar.padding(16).transition(.move(edge: .trailing).combined(with: .opacity)) }
        }
        .toolbar {
            ToolbarItem(placement: .topBarTrailing) {
                Button(hidden ? "Show toolbar" : "Hide toolbar", systemImage: hidden ? "eye" : "eye.slash") {
                    withAnimation(.spring(response: 0.3, dampingFraction: 0.82)) { hidden.toggle() }
                }
                .buttonStyle(.glass)
            }
        }
    }

    private var toolbar: some View {
        GlassEffectContainer(spacing: 8) {
            VStack(spacing: 8) {
                ForEach(tools, id: \.self) { tool in
                    Button(tool, systemImage: tool) { withAnimation(.spring(response: 0.25, dampingFraction: 0.82)) { selected = tool } }
                        .floatingToolbarRecipeGlassStyle(selected == tool)
                        .labelStyle(.iconOnly)
                        .frame(width: 46, height: 46)
                }
            }
        }
    }
}



@available(iOS 26.0, *)
private extension View {
    @ViewBuilder
    func floatingToolbarRecipeGlassStyle(_ isSelected: Bool) -> some View {
        if isSelected {
            self.buttonStyle(.glassProminent)
        } else {
            self.buttonStyle(.glass)
        }
    }
}

#Preview {
    NavigationStack { if #available(iOS 26.0, *) { FloatingToolbarRecipe() } }
}
