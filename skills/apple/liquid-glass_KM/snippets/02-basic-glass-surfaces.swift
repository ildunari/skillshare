import SwiftUI

@available(iOS 26.0, *)
struct BasicGlassSurfaces: View {
    var body: some View {
        VStack(spacing: 16) {
            Label("Regular glass for controls", systemImage: "wand.and.sparkles")
                .padding(.horizontal, 18)
                .padding(.vertical, 12)
                .glassEffect(.regular, in: Capsule())

            Label("Interactive glass for pressable UI", systemImage: "hand.tap")
                .padding(.horizontal, 18)
                .padding(.vertical, 12)
                .glassEffect(.regular.interactive(), in: Capsule())

            Label("Tinted glass for semantic state", systemImage: "bolt.fill")
                .padding(.horizontal, 18)
                .padding(.vertical, 12)
                .glassEffect(.regular.tint(.orange.opacity(0.22)).interactive(), in: Capsule())
        }
        .padding()
    }
}
