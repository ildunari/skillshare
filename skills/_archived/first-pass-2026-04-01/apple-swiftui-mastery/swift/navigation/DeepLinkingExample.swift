import SwiftUI

/// Demonstrates handling deep links by decoding URL components into navigation path.
enum DeepLinkScreen: Hashable, Codable {
    case item(id: Int)
    case settings
}

struct DeepLinkingExample: View {
    @State private var path = NavigationPath()
    var body: some View {
        NavigationStack(path: $path) {
            VStack(spacing: 20) {
                Button("Open Item 5") {
                    path.append(DeepLinkScreen.item(id: 5))
                }
                Button("Open Settings") {
                    path.append(DeepLinkScreen.settings)
                }
            }
            .navigationDestination(for: DeepLinkScreen.self) { screen in
                switch screen {
                case .item(let id): Text("Item detail for id \(id)")
                case .settings: Text("Settings screen")
                }
            }
            .navigationTitle("Deep Links")
        }
        // Example of handling a URL; in real app use .onOpenURL in App
        .onAppear {
            let exampleURL = URL(string: "myapp://item/3")!
            if let screen = parse(url: exampleURL) {
                path.append(screen)
            }
        }
    }
    func parse(url: URL) -> DeepLinkScreen? {
        let components = url.pathComponents.filter { $0 != "/" }
        guard let first = components.first else { return nil }
        if first == "item", let idString = components.dropFirst().first, let id = Int(idString) {
            return .item(id: id)
        } else if first == "settings" {
            return .settings
        }
        return nil
    }
}

struct DeepLinkingExample_Previews: PreviewProvider {
    static var previews: some View {
        DeepLinkingExample()
    }
}