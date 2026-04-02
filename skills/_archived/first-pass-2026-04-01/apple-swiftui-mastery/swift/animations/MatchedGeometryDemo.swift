import SwiftUI

/// Demonstrates matchedGeometryEffect for smooth transitions.
struct MatchedGeometryDemo: View {
    @Namespace private var ns
    @State private var expanded = false
    var body: some View {
        VStack {
            if expanded {
                RoundedRectangle(cornerRadius: 20)
                    .fill(Color.pink)
                    .matchedGeometryEffect(id: "shape", in: ns)
                    .frame(width: 300, height: 200)
                    .onTapGesture { withAnimation { expanded.toggle() } }
            } else {
                Circle()
                    .fill(Color.pink)
                    .matchedGeometryEffect(id: "shape", in: ns)
                    .frame(width: 100, height: 100)
                    .onTapGesture { withAnimation { expanded.toggle() } }
            }
        }
    }
}

struct MatchedGeometryDemo_Previews: PreviewProvider {
    static var previews: some View {
        MatchedGeometryDemo()
    }
}