import SwiftUI

struct ThreadPreview: Identifiable, Hashable {
    let id = UUID()
    let title: String
    let excerpt: String
}

@available(iOS 26.0, *)
struct NavigationZoomThreads: View {
    @Namespace private var transitionNamespace
    private let threads = [
        ThreadPreview(title: "Research agent", excerpt: "Summarizing sources…"),
        ThreadPreview(title: "Canvas plan", excerpt: "Generating layout options…")
    ]

    var body: some View {
        NavigationStack {
            List(threads) { thread in
                NavigationLink(value: thread) {
                    VStack(alignment: .leading) {
                        Text(thread.title).font(.headline)
                        Text(thread.excerpt).foregroundStyle(.secondary)
                    }
                    .matchedTransitionSource(id: thread.id, in: transitionNamespace)
                }
            }
            .navigationDestination(for: ThreadPreview.self) { thread in
                ThreadDetail(thread: thread)
                    .navigationTransition(.zoom(sourceID: thread.id, in: transitionNamespace))
            }
        }
    }
}

@available(iOS 26.0, *)
private struct ThreadDetail: View {
    let thread: ThreadPreview
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text(thread.title).font(.largeTitle.bold())
            Text(thread.excerpt)
            Spacer()
        }
        .padding()
    }
}
