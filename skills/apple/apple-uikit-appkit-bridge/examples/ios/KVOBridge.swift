import SwiftUI
import WebKit
import Combine

final class ProgressModel: ObservableObject {
    @Published var progress: Double = 0
}

struct WebKVOExample: View {
    @State private var isLoading = false
    @StateObject private var model = ProgressModel()

    var body: some View {
        VStack {
            ProgressView(value: model.progress)
            WebViewBridge(url: URL(string: "https://apple.com")!,
                          isLoading: $isLoading,
                          progress: $model.progress)
        }
    }
}
