import SwiftUI

/// GlassToolbarIntegration shows how to embed glass buttons inside a
/// SwiftUI toolbar.  The toolbar item hosts a horizontal stack of buttons
/// that themselves adopt the `.glass` button style and are wrapped in a
/// glassEffect modifier.  This pattern can be extended to search fields
/// and segmented controls.
@available(macOS 26.0, *)
struct GlassToolbarIntegration: View {
    var body: some View {
        NavigationView {
            Text("Content goes here")
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .toolbar {
                    ToolbarItem(placement: .navigation) {
                        HStack(spacing: 12) {
                            Button(action: {}) {
                                Image(systemName: "plus")
                            }
                            .buttonStyle(.glass)

                            Button(action: {}) {
                                Image(systemName: "trash")
                            }
                            .buttonStyle(.glass)
                        }
                        .padding(.horizontal, 12)
                        .padding(.vertical, 8)
                        .glassEffect(.regular, in: RoundedRectangle(cornerRadius: 14))
                    }
                }
        }
    }
}

#if DEBUG
@available(macOS 26.0, *)
struct GlassToolbarIntegration_Previews: PreviewProvider {
    static var previews: some View {
        GlassToolbarIntegration()
    }
}
#endif