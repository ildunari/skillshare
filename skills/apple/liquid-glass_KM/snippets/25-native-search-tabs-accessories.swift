import SwiftUI

@available(iOS 26.0, *)
struct NativeSearchTabsAccessorySnippet: View {
    enum Root: Hashable { case threads, canvas, agents }

    @State private var selection: Root = .threads
    @State private var searchText = ""

    var body: some View {
        TabView(selection: $selection) {
            NavigationStack {
                ThreadSearchSurface(searchText: $searchText)
                    .navigationTitle("Threads")
                    .searchable(text: $searchText, prompt: "Search threads")
            }
            .tabItem { Label("Threads", systemImage: "bubble.left.and.bubble.right") }
            .tag(Root.threads)

            NavigationStack {
                CanvasSurface()
                    .navigationTitle("Canvas")
            }
            .tabItem { Label("Canvas", systemImage: "rectangle.on.rectangle") }
            .tag(Root.canvas)

            NavigationStack {
                AgentSurface()
                    .navigationTitle("Agents")
            }
            .tabItem { Label("Agents", systemImage: "brain") }
            .tag(Root.agents)
        }
        .tabBarMinimizeBehavior(.onScrollDown)
        .tabViewBottomAccessory {
            HStack(spacing: 8) {
                Image(systemName: "bolt.fill")
                Text("1 active agent")
                    .font(.footnote.weight(.semibold))
                Spacer(minLength: 12)
                Button("Stop", systemImage: "stop.fill") {}
                    .buttonStyle(.glass)
                    .tint(.red)
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 8)
        }
    }

    // If the active SDK exposes SwiftUI's typed Tab initializer with a search role,
    // use a real search tab for first-class search instead of faking search as an action.
    // Example shape to adapt locally:
    // Tab("Search", systemImage: "magnifyingglass", value: Root.search, role: .search) { SearchSurface() }
}

@available(iOS 26.0, *)
private struct ThreadSearchSurface: View {
    @Binding var searchText: String
    private let threads = ["Research plan", "SwiftUI glass audit", "Canvas preview", "Tool retry notes"]

    var body: some View {
        List(filtered, id: \.self) { thread in
            VStack(alignment: .leading, spacing: 4) {
                Text(thread).font(.headline)
                Text("Updated recently")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
            .padding(.vertical, 6)
        }
        .overlay(alignment: .bottom) {
            GlassEffectContainer(spacing: 8) {
                HStack(spacing: 8) {
                    Button("Unread", systemImage: "tray") {}
                        .buttonStyle(.glass)
                    Button("Pinned", systemImage: "pin") {}
                        .buttonStyle(.glass)
                    Button("New", systemImage: "plus") {}
                        .buttonStyle(.glassProminent)
                }
            }
            .padding(.bottom, 12)
        }
    }

    private var filtered: [String] {
        searchText.isEmpty ? threads : threads.filter { $0.localizedCaseInsensitiveContains(searchText) }
    }
}

@available(iOS 26.0, *)
private struct CanvasSurface: View {
    var body: some View {
        ZStack {
            LinearGradient(colors: [.indigo, .blue], startPoint: .topLeading, endPoint: .bottomTrailing)
                .ignoresSafeArea()
            Text("Canvas")
                .font(.largeTitle.bold())
                .foregroundStyle(.white)
        }
    }
}

@available(iOS 26.0, *)
private struct AgentSurface: View {
    var body: some View {
        List(["Planner", "Coder", "Researcher"], id: \.self) { agent in
            Label(agent, systemImage: "brain")
        }
    }
}

@available(iOS 26.0, *)
#Preview("Native search, tabs, accessory") {
    NativeSearchTabsAccessorySnippet()
}
