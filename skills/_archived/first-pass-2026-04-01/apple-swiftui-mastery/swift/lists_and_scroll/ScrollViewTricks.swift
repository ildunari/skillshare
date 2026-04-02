import SwiftUI

/// Demonstrates advanced ScrollView behaviours such as programmatic scrolling and scroll indicators.
struct ScrollViewTricks: View {
    let items = Array(1...50)
    @State private var scrollToIndex: Int? = nil
    var body: some View {
        VStack {
            Button("Scroll to 40") {
                scrollToIndex = 40
            }
            .padding()
            ScrollViewReader { proxy in
                ScrollView(.vertical) {
                    VStack(alignment: .leading, spacing: 8) {
                        ForEach(items, id: \ .self) { item in
                            Text("Row \(item)")
                                .id(item)
                                .padding()
                                .frame(maxWidth: .infinity, alignment: .leading)
                                .background(Color.gray.opacity(0.1))
                        }
                    }
                }
                .onChange(of: scrollToIndex) { value in
                    if let value = value {
                        withAnimation {
                            proxy.scrollTo(value, anchor: .top)
                        }
                    }
                }
                .scrollIndicators(.visible) // show scroll indicators on iOS 16+
            }
        }
    }
}

struct ScrollViewTricks_Previews: PreviewProvider {
    static var previews: some View {
        ScrollViewTricks()
    }
}