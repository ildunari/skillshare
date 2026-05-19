import SwiftUI

// Canonical morphing-selection filter rail (SDK-verified against iOS 26.4 simulator).
//
// GOTCHAS this snippet exists to demonstrate the fix for:
//   1. Render the inner glass for EVERY cell, all the time — Glass.identity for inactive,
//      .regular.tint(...) for active. Conditional `if isSelected { Glass() }` breaks the morph.
//   2. The outer rail uses .ultraThinMaterial, NOT another .glassEffect — two glass surfaces
//      in one container mute each other and can make foreground text invisible.
//   3. Animation is state-bound .animation(_:value:) on the container, NOT withAnimation in
//      the tap handler (which captures stale state on rapid taps).

@available(iOS 26.0, *)
struct SearchFilterPillControls: View {
    @State private var query = ""
    @State private var selected: String = "All"
    @Namespace private var ns

    private let filters = ["All", "Pinned", "Running"]

    var body: some View {
        VStack(spacing: 12) {
            // Search field (own glass surface, separate visual group from the rail).
            HStack(spacing: 8) {
                Label("Search", systemImage: "magnifyingglass")
                    .labelStyle(.iconOnly)
                    .padding(.leading, 12)
                TextField("Search threads", text: $query)
                    .textFieldStyle(.plain)
            }
            .padding(.vertical, 8)
            .glassEffect(.regular.interactive(), in: Capsule())

            // Morphing filter rail.
            GlassEffectContainer(spacing: 24) {
                HStack(spacing: 6) {
                    ForEach(filters, id: \.self) { filter in
                        Button { selected = filter } label: {
                            Text(filter)
                                .font(.callout.weight(.semibold))
                                .padding(.horizontal, 14)
                                .padding(.vertical, 8)
                                .frame(maxWidth: .infinity)
                        }
                        .buttonStyle(.plain)
                        .background {
                            Capsule()
                                .fill(.clear)
                                .glassEffect(
                                    selected == filter
                                        ? .regular.tint(.accentColor).interactive()
                                        : .identity,
                                    in: Capsule()
                                )
                                .glassEffectID("selection", in: ns)
                        }
                    }
                }
                .padding(4)
            }
            // Outer rail is Material, NOT glassEffect — avoids glass-on-glass muting.
            .background(.ultraThinMaterial, in: Capsule())
            .animation(.spring(response: 0.34, dampingFraction: 0.82), value: selected)
        }
        .padding()
    }
}
