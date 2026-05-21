import SwiftUI

@available(iOS 26.0, *)
public struct ThreadListRecipe: View {
    @State private var query = ""
    @State private var filter: ThreadFilter = .all
    @Namespace private var transitionNamespace

    private let threads = ThreadItem.sample

    public init() {}

    public var body: some View {
        NavigationStack {
            List(filteredThreads) { thread in
                NavigationLink(value: thread) {
                    ThreadRow(thread: thread)
                        .matchedTransitionSource(id: thread.id, in: transitionNamespace)
                }
            }
            .listStyle(.plain)
            .navigationTitle("Threads")
            .safeAreaInset(edge: .top) { filterBar.padding(.horizontal).padding(.vertical, 8) }
            .navigationDestination(for: ThreadItem.self) { thread in
                ThreadDetail(thread: thread)
                    .navigationTransition(.zoom(sourceID: thread.id, in: transitionNamespace))
            }
        }
    }

    private var filteredThreads: [ThreadItem] {
        threads.filter { thread in
            (query.isEmpty || thread.title.localizedCaseInsensitiveContains(query)) &&
            (filter == .all || (filter == .running && thread.status == .running) || (filter == .pinned && thread.isPinned))
        }
    }

    private var filterBar: some View {
        GlassEffectContainer(spacing: 8) {
            HStack(spacing: 8) {
                Label("Search", systemImage: "magnifyingglass").labelStyle(.iconOnly)
                TextField("Search threads", text: $query).textFieldStyle(.plain)
                Divider().frame(height: 22)
                ForEach(ThreadFilter.allCases) { item in
                    Button(item.title) { filter = item }
                        .threadRecipeGlassStyle(filter == item)
                }
            }
            .padding(8)
            .glassEffect(.regular.interactive(), in: Capsule())
        }
    }
}

private enum ThreadFilter: String, CaseIterable, Identifiable {
    case all, running, pinned
    var id: String { rawValue }
    var title: String { rawValue.capitalized }
}

private struct ThreadItem: Identifiable, Hashable {
    enum Status: String { case idle, running, failed }
    let id = UUID()
    let title: String
    let subtitle: String
    let status: Status
    let isPinned: Bool

    static let sample = [
        ThreadItem(title: "Launch plan", subtitle: "Agent drafted milestones", status: .idle, isPinned: true),
        ThreadItem(title: "Research synthesis", subtitle: "Web tool is running", status: .running, isPinned: false),
        ThreadItem(title: "Design critique", subtitle: "Needs review", status: .failed, isPinned: false)
    ]
}

@available(iOS 26.0, *)
private struct ThreadRow: View {
    let thread: ThreadItem
    var body: some View {
        HStack(spacing: 12) {
            VStack(alignment: .leading, spacing: 4) {
                Text(thread.title).font(.headline)
                Text(thread.subtitle).font(.subheadline).foregroundStyle(.secondary)
            }
            Spacer()
            if thread.status == .running {
                Label("Running", systemImage: "arrow.triangle.2.circlepath")
                    .font(.caption.weight(.semibold))
                    .padding(.horizontal, 9)
                    .padding(.vertical, 6)
                    .glassEffect(.regular.tint(.orange.opacity(0.2)), in: Capsule())
            }
            Button(thread.isPinned ? "Pinned" : "Pin", systemImage: thread.isPinned ? "pin.fill" : "pin") {}
                .threadRecipeGlassStyle(thread.isPinned)
                .labelStyle(.iconOnly)
        }
        .padding(.vertical, 8)
    }
}

@available(iOS 26.0, *)
private struct ThreadDetail: View {
    let thread: ThreadItem
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text(thread.title).font(.largeTitle.bold())
            Text(thread.subtitle).foregroundStyle(.secondary)
            Spacer()
        }.padding()
    }
}



@available(iOS 26.0, *)
private extension View {
    @ViewBuilder
    func threadRecipeGlassStyle(_ isSelected: Bool) -> some View {
        if isSelected {
            self.buttonStyle(.glassProminent)
        } else {
            self.buttonStyle(.glass)
        }
    }
}

#Preview {
    if #available(iOS 26.0, *) { ThreadListRecipe() }
}
