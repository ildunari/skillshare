import SwiftUI

@available(iOS 26.0, *)
struct GlassSegmentedControl<Value: Hashable & Identifiable>: View where Value.ID == String {
    let values: [Value]
    let title: (Value) -> String
    let symbol: (Value) -> String
    @Binding var selection: Value
    @Namespace private var namespace

    var body: some View {
        GlassEffectContainer(spacing: 6) {
            HStack(spacing: 6) {
                ForEach(values) { value in
                    Button {
                        withAnimation(.spring(response: 0.3, dampingFraction: 0.8)) { selection = value }
                    } label: {
                        Label(title(value), systemImage: symbol(value))
                            .font(.callout.weight(.semibold))
                            .padding(.horizontal, 12)
                            .padding(.vertical, 9)
                    }
                    .segmentGlassStyle(selection == value)
                    .glassEffectID(value.id, in: namespace)
                }
            }
        }
    }
}

@available(iOS 26.0, *)
private extension View {
    @ViewBuilder
    func segmentGlassStyle(_ isSelected: Bool) -> some View {
        if isSelected {
            self.buttonStyle(.glassProminent)
        } else {
            self.buttonStyle(.glass)
        }
    }
}
