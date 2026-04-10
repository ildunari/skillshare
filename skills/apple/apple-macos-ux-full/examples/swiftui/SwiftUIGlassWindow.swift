import SwiftUI

/// SwiftUIGlassWindow demonstrates how to apply the glassEffect modifier to
/// a SwiftUI view on macOS 26.  The buttons adopt the `.glass` button style
/// and the surrounding HStack is wrapped in a glass effect with a rounded
/// rectangle.  This pattern scales to navigation bars, toolbars and
/// panels in SwiftUI.
@available(macOS 26.0, *)
struct SwiftUIGlassWindow: View {
    var body: some View {
        VStack(spacing: 20) {
            Text("SwiftUI Liquid Glass")
                .font(.title2)
            HStack(spacing: 16) {
                Button(action: {}) {
                    Label("Like", systemImage: "hand.thumbsup.fill")
                }
                .buttonStyle(.glass)

                Button(action: {}) {
                    Label("Share", systemImage: "square.and.arrow.up")
                }
                .buttonStyle(.glass)
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 12)
            .glassEffect(.regular, in: RoundedRectangle(cornerRadius: 16))
        }
        .padding(32)
        .frame(width: 400, height: 220)
    }
}

#if DEBUG
@available(macOS 26.0, *)
struct SwiftUIGlassWindow_Previews: PreviewProvider {
    static var previews: some View {
        SwiftUIGlassWindow()
    }
}
#endif