import SwiftUI

/// Demonstrates using PreferenceKey to propagate a child size up to a parent.
struct HeightKey: PreferenceKey {
    static var defaultValue: CGFloat = 0
    static func reduce(value: inout CGFloat, nextValue: () -> CGFloat) {
        value = max(value, nextValue())
    }
}

struct MeasuredChild: View {
    var body: some View {
        Text("Measure me!")
            .padding(8)
            .background(GeometryReader { proxy in
                Color.clear
                    .preference(key: HeightKey.self, value: proxy.size.height)
            })
    }
}

struct PreferenceKeyDemo: View {
    @State private var childHeight: CGFloat = 0
    var body: some View {
        VStack {
            MeasuredChild()
            Rectangle()
                .fill(Color.red.opacity(0.3))
                .frame(height: childHeight)
                .overlay(Text("Height: \(Int(childHeight))"))
        }
        .onPreferenceChange(HeightKey.self) { value in
            childHeight = value
        }
        .padding()
    }
}

struct PreferenceKeyDemo_Previews: PreviewProvider {
    static var previews: some View {
        PreferenceKeyDemo()
    }
}