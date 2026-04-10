import SwiftUI

/// GlassSidebarNavigation demonstrates a `NavigationSplitView` where the
/// sidebar adopts Liquid Glass via the `glassEffect` modifier.  The
/// example stores a selection state and shows the selected item in the
/// detail panel.  On macOS 26 the sidebar will appear airy and
/// translucent; on earlier systems it falls back to a solid list.
@available(macOS 26.0, *)
struct GlassSidebarNavigation: View {
    @State private var selection: String? = "Home"
    var body: some View {
        NavigationSplitView {
            List(selection: $selection) {
                Text("Home").tag("Home")
                Text("Settings").tag("Settings")
                Text("Profile").tag("Profile")
            }
            .frame(minWidth: 200)
            .glassEffect(.regular, in: RoundedRectangle(cornerRadius: 0))
        } detail: {
            Text(selection ?? "Home")
                .frame(maxWidth: .infinity, maxHeight: .infinity)
        }
    }
}

#if DEBUG
@available(macOS 26.0, *)
struct GlassSidebarNavigation_Previews: PreviewProvider {
    static var previews: some View {
        GlassSidebarNavigation()
            .frame(width: 500, height: 300)
    }
}
#endif