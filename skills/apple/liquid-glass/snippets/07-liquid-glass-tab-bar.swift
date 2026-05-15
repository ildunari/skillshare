import SwiftUI

@available(iOS 26.0, *)
struct LiquidGlassTabBarSnippet: View {
    enum Tab: String, CaseIterable, Identifiable {
        case threads, canvas, tools, settings
        var id: String { rawValue }
        var symbol: String {
            switch self { case .threads: "bubble.left.and.bubble.right"; case .canvas: "rectangle.on.rectangle"; case .tools: "wrench.and.screwdriver"; case .settings: "gearshape" }
        }
        var title: String { rawValue.capitalized }
    }

    @State private var selection: Tab = .threads

    var body: some View {
        ZStack(alignment: .bottom) {
            Text(selection.title).font(.largeTitle.bold())
                .frame(maxWidth: .infinity, maxHeight: .infinity)

            GlassEffectContainer(spacing: 10) {
                HStack(spacing: 8) {
                    ForEach(Tab.allCases) { tab in
                        Button {
                            withAnimation(.spring(response: 0.32, dampingFraction: 0.82)) { selection = tab }
                        } label: {
                            Label(tab.title, systemImage: tab.symbol)
                                .labelStyle(.iconOnly)
                                .frame(width: 48, height: 44)
                        }
                        .tabBarGlassStyle(selection == tab)
                        .accessibilityLabel(tab.title)
                        .tabBarSelectedTrait(selection == tab)
                    }

                    Button("Compose", systemImage: "plus") {}
                        .buttonStyle(.glassProminent)
                        .tint(.accentColor)
                        .frame(width: 54, height: 54)
                }
            }
            .padding(.horizontal, 14)
            .padding(.vertical, 10)
        }
    }
}

@available(iOS 26.0, *)
private extension View {
    @ViewBuilder
    func tabBarGlassStyle(_ isSelected: Bool) -> some View {
        if isSelected {
            self.buttonStyle(.glassProminent)
        } else {
            self.buttonStyle(.glass)
        }
    }

    @ViewBuilder
    func tabBarSelectedTrait(_ isSelected: Bool) -> some View {
        if isSelected {
            self.accessibilityAddTraits(.isSelected)
        } else {
            self
        }
    }
}
