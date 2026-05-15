import SwiftUI

@available(iOS 26.0, *)
public struct NativeSearchAccessoryRecipe: View {
    enum SectionTab: Hashable { case threads, canvas, agents }

    @State private var selected: SectionTab = .threads
    @State private var query = ""
    @State private var activeAgent = true

    public init() {}

    public var body: some View {
        TabView(selection: $selected) {
            NavigationStack {
                List(filteredThreads, id: \.self) { thread in
                    HStack(spacing: 12) {
                        Image(systemName: "bubble.left.and.bubble.right")
                            .foregroundStyle(.secondary)
                        VStack(alignment: .leading, spacing: 4) {
                            Text(thread).font(.headline)
                            Text("Searchable native thread row, not a glass card")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                    }
                    .padding(.vertical, 6)
                }
                .navigationTitle("Threads")
                .searchable(text: $query, prompt: "Search threads")
            }
            .tabItem { Label("Threads", systemImage: "bubble.left.and.bubble.right") }
            .tag(SectionTab.threads)

            NavigationStack {
                MediaCanvasControlsRecipe()
                    .navigationTitle("Canvas")
            }
            .tabItem { Label("Canvas", systemImage: "rectangle.on.rectangle") }
            .tag(SectionTab.canvas)

            NavigationStack {
                List(["Planner", "Coder", "Researcher"], id: \.self) { name in
                    Label(name, systemImage: "brain")
                }
                .navigationTitle("Agents")
            }
            .tabItem { Label("Agents", systemImage: "brain") }
            .tag(SectionTab.agents)
        }
        .tabBarMinimizeBehavior(.onScrollDown)
        .tabViewBottomAccessory {
            HStack(spacing: 8) {
                Image(systemName: activeAgent ? "bolt.fill" : "pause.circle")
                Text(activeAgent ? "Agent running" : "Agent idle")
                    .font(.footnote.weight(.semibold))
                Spacer(minLength: 12)
                Button(activeAgent ? "Stop" : "Resume", systemImage: activeAgent ? "stop.fill" : "play.fill") {
                    activeAgent.toggle()
                }
                .activeAgentButtonStyle(activeAgent)
                .tint(activeAgent ? .red : .blue)
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 8)
        }
    }

    private var filteredThreads: [String] {
        let all = ["Liquid Glass audit", "Chat composer polish", "Canvas overlay notes", "Agent tool retries"]
        return query.isEmpty ? all : all.filter { $0.localizedCaseInsensitiveContains(query) }
    }
}

@available(iOS 26.0, *)
private extension View {
    @ViewBuilder
    func activeAgentButtonStyle(_ isActive: Bool) -> some View {
        if isActive {
            self.buttonStyle(.glassProminent)
        } else {
            self.buttonStyle(.glass)
        }
    }
}

@available(iOS 26.0, *)
#Preview("Native Search + Accessory") {
    NativeSearchAccessoryRecipe()
}
