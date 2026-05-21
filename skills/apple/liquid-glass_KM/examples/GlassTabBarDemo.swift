import SwiftUI

@available(iOS 26.0, *)
struct GlassTabBarDemo: View {
    enum Tab: String, CaseIterable, Identifiable {
        case chats, canvas, agents, settings
        var id: String { rawValue }
        var symbol: String { switch self { case .chats: "bubble.left.and.bubble.right"; case .canvas: "rectangle.on.rectangle"; case .agents: "person.2.wave.2"; case .settings: "gearshape" } }
    }

    @State private var selected: Tab = .chats
    @State private var expanded = false

    var body: some View {
        ZStack(alignment: .bottom) {
            GlassShowcaseBackground()
            ScrollView { VStack(spacing: 16) { ForEach(0..<16) { Text("\(selected.rawValue.capitalized) row \($0 + 1)").frame(maxWidth: .infinity).padding().background(.background.opacity(0.35), in: RoundedRectangle(cornerRadius: 18)) } }.padding().padding(.bottom, 130) }
            VStack(spacing: 10) {
                if expanded {
                    HStack { Button("New chat", systemImage: "plus.bubble") {}.buttonStyle(.glass); Button("New image", systemImage: "photo") {}.buttonStyle(.glass) }
                        .transition(.scale.combined(with: .opacity))
                }
                GlassEffectContainer(spacing: 8) {
                    HStack(spacing: 8) {
                        ForEach(Tab.allCases) { tab in
                            Button(tab.rawValue, systemImage: tab.symbol) { withAnimation(.spring(response: 0.3, dampingFraction: 0.82)) { selected = tab } }
                                .showcaseGlassStyle(selected == tab)
                                .labelStyle(.iconOnly)
                                .accessibilityLabel(tab.rawValue.capitalized)
                        }
                        Button("Create", systemImage: expanded ? "xmark" : "plus") { withAnimation(.spring(response: 0.34, dampingFraction: 0.72)) { expanded.toggle() } }
                            .buttonStyle(.glassProminent)
                            .contentTransition(.symbolEffect(.replace))
                    }
                }
            }.padding()
        }
        .navigationTitle("Tab Bar")
    }
}

#Preview { if #available(iOS 26.0, *) { NavigationStack { GlassTabBarDemo() } } }
