import SwiftUI

/// Basic NavigationStack example using NavigationPath and navigationDestination.
enum AppScreen: Hashable {
    case home
    case detail(Int)
}

struct NavigationExample: View {
    @State private var path: [AppScreen] = []
    var body: some View {
        NavigationStack(path: $path) {
            List(0..<10) { index in
                NavigationLink(value: AppScreen.detail(index)) {
                    Text("Row \(index)")
                }
            }
            .navigationDestination(for: AppScreen.self) { screen in
                switch screen {
                case .home: Text("Home")
                case .detail(let i): Text("Detail for \(i)")
                }
            }
            .navigationTitle("Home")
        }
    }
}

struct NavigationExample_Previews: PreviewProvider {
    static var previews: some View {
        NavigationExample()
    }
}