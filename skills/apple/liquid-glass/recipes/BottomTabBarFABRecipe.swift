import SwiftUI

@available(iOS 26.0, *)
public struct BottomTabBarFABRecipe: View {
    enum AppTab: String, CaseIterable, Identifiable {
        case chat, canvas, agents, settings
        var id: String { rawValue }
        var title: String { rawValue.capitalized }
        var symbol: String {
            switch self { case .chat: "bubble.left.and.bubble.right"; case .canvas: "rectangle.on.rectangle"; case .agents: "person.2.wave.2"; case .settings: "gearshape" }
        }
    }

    @State private var selected: AppTab = .chat
    @State private var fabExpanded = false

    public init() {}

    public var body: some View {
        ZStack(alignment: .bottom) {
            ScrollView {
                VStack(spacing: 16) {
                    Text(selected.title).font(.largeTitle.bold()).frame(maxWidth: .infinity, alignment: .leading)
                    ForEach(0..<20) { index in
                        RoundedRectangle(cornerRadius: 18).fill(.secondary.opacity(0.08)).frame(height: 70).overlay(Text("Content row \(index + 1)"))
                    }
                }.padding().padding(.bottom, 120)
            }

            VStack(spacing: 12) {
                if fabExpanded { fabActions.transition(.scale.combined(with: .opacity)) }
                tabBar
            }
            .padding(.horizontal, 16)
            .padding(.bottom, 10)
        }
    }

    private var tabBar: some View {
        GlassEffectContainer(spacing: 8) {
            HStack(spacing: 8) {
                ForEach(AppTab.allCases) { tab in
                    Button { withAnimation(.spring(response: 0.32, dampingFraction: 0.82)) { selected = tab } } label: {
                        Image(systemName: tab.symbol).frame(width: 42, height: 42)
                    }
                    .bottomTabRecipeGlassStyle(selected == tab)
                    .accessibilityLabel(tab.title)
                    .bottomTabRecipeSelectedTrait(selected == tab)
                }
                Button("New", systemImage: fabExpanded ? "xmark" : "plus") {
                    withAnimation(.spring(response: 0.34, dampingFraction: 0.72)) { fabExpanded.toggle() }
                }
                .buttonStyle(.glassProminent)
                .tint(.accentColor)
                .contentTransition(.symbolEffect(.replace))
                .frame(width: 56, height: 56)
            }
        }
    }

    private var fabActions: some View {
        GlassEffectContainer(spacing: 8) {
            HStack(spacing: 8) {
                Button("Chat", systemImage: "plus.bubble") {}.buttonStyle(.glass)
                Button("Image", systemImage: "photo") {}.buttonStyle(.glass)
                Button("Task", systemImage: "checklist") {}.buttonStyle(.glass)
            }
        }
    }
}



@available(iOS 26.0, *)
private extension View {
    @ViewBuilder
    func bottomTabRecipeGlassStyle(_ isSelected: Bool) -> some View {
        if isSelected {
            self.buttonStyle(.glassProminent)
        } else {
            self.buttonStyle(.glass)
        }
    }

    @ViewBuilder
    func bottomTabRecipeSelectedTrait(_ isSelected: Bool) -> some View {
        if isSelected {
            self.accessibilityAddTraits(.isSelected)
        } else {
            self
        }
    }
}

#Preview {
    if #available(iOS 26.0, *) { BottomTabBarFABRecipe() }
}
