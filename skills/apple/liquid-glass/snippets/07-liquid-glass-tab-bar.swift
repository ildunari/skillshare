import SwiftUI

// Canonical morphing custom tab bar (Apple Music–style selection morph).
// SDK-verified against iOS 26.4 simulator. See SKILL.md "Verified gotchas".
//
// GOTCHAS:
//   1. Selection glass renders for EVERY tab — Glass.identity for inactive,
//      .regular.tint(...) for active. Conditional `if isSelected { Glass() }` breaks morph.
//   2. Outer rail = .ultraThinMaterial, NOT another .glassEffect — avoids glass-on-glass
//      muting and invisible foreground text.
//   3. .animation(_:value:) on the container, NOT withAnimation in tap handler.
//
// Prefer the native iOS 26 TabView for primary navigation. Use this pattern only for
// bespoke bars (e.g. floating bottom bars in a canvas/agent surface) where a system
// TabView doesn't fit.

@available(iOS 26.0, *)
struct LiquidGlassTabBarSnippet: View {
    enum Tab: String, CaseIterable, Identifiable {
        case threads, canvas, tools, settings
        var id: String { rawValue }
        var symbol: String {
            switch self {
            case .threads: "bubble.left.and.bubble.right"
            case .canvas: "rectangle.on.rectangle"
            case .tools: "wrench.and.screwdriver"
            case .settings: "gearshape"
            }
        }
        var title: String { rawValue.capitalized }
    }

    @State private var selection: Tab = .threads
    @Namespace private var ns

    var body: some View {
        ZStack(alignment: .bottom) {
            Text(selection.title).font(.largeTitle.bold())
                .frame(maxWidth: .infinity, maxHeight: .infinity)

            HStack(spacing: 12) {
                // Morphing tab rail.
                GlassEffectContainer(spacing: 24) {
                    HStack(spacing: 4) {
                        ForEach(Tab.allCases) { tab in
                            Button { selection = tab } label: {
                                Label(tab.title, systemImage: tab.symbol)
                                    .labelStyle(.iconOnly)
                                    .font(.title3.weight(.semibold))
                                    .frame(width: 48, height: 44)
                            }
                            .buttonStyle(.plain)
                            .accessibilityLabel(tab.title)
                            .accessibilityAddTraits(selection == tab ? .isSelected : [])
                            .background {
                                Capsule()
                                    .fill(.clear)
                                    .glassEffect(
                                        selection == tab
                                            ? .regular.tint(.accentColor).interactive()
                                            : .identity,
                                        in: Capsule()
                                    )
                                    .glassEffectID("tab-selection", in: ns)
                            }
                        }
                    }
                    .padding(.horizontal, 6)
                    .padding(.vertical, 5)
                }
                // Material rail — NOT glassEffect — so the inner tab pill stays crisp.
                .background(.ultraThinMaterial, in: Capsule())
                .animation(.spring(response: 0.32, dampingFraction: 0.82), value: selection)

                // Compose FAB — its OWN glass surface, outside the rail container.
                Button("Compose", systemImage: "plus") {}
                    .labelStyle(.iconOnly)
                    .buttonStyle(.glassProminent)
                    .tint(.accentColor)
                    .frame(width: 54, height: 54)
            }
            .padding(.horizontal, 14)
            .padding(.vertical, 10)
        }
    }
}
