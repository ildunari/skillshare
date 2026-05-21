import SwiftUI

// Canonical morphing segmented control (SDK-verified against iOS 26.4 simulator).
//
// GOTCHAS this snippet exists to demonstrate the fix for:
//   1. The selection glass is rendered for EVERY segment, all the time —
//      Glass.identity for inactive, .regular.tint(...) for active. A previous draft used
//      conditional `if isSelected { .buttonStyle(.glassProminent) }`, which destroys and
//      re-creates the glass view and breaks the morph.
//   2. The outer rail uses .ultraThinMaterial, NOT another .glassEffect — glass-on-glass
//      inside one container mutes the inner pill and can hide foreground text.
//   3. State-bound .animation(_:value:) on the container drives the morph. DO NOT use
//      withAnimation in the tap handler — it captures stale state on rapid taps.

@available(iOS 26.0, *)
struct GlassSegmentedControl<Value: Hashable & Identifiable>: View where Value.ID == String {
    let values: [Value]
    let title: (Value) -> String
    let symbol: (Value) -> String
    @Binding var selection: Value
    @Namespace private var ns

    var body: some View {
        GlassEffectContainer(spacing: 24) {
            HStack(spacing: 6) {
                ForEach(values) { value in
                    Button { selection = value } label: {
                        Label(title(value), systemImage: symbol(value))
                            .font(.callout.weight(.semibold))
                            .padding(.horizontal, 12)
                            .padding(.vertical, 9)
                            .frame(maxWidth: .infinity)
                    }
                    .buttonStyle(.plain)
                    .background {
                        Capsule()
                            .fill(.clear)
                            .glassEffect(
                                selection.id == value.id
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
        // Material rail — NOT glassEffect — so the inner pill stays readable.
        .background(.ultraThinMaterial, in: Capsule())
        .animation(.spring(response: 0.30, dampingFraction: 0.80), value: selection.id)
    }
}
