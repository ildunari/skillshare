import SwiftUI
import WebKit
import Combine

struct WebViewBridge: UIViewRepresentable {
    typealias UIViewType = WKWebView

    let url: URL
    @Binding var isLoading: Bool
    @Binding var progress: Double

    func makeCoordinator() -> Coordinator { Coordinator(self) }

    func makeUIView(context: Context) -> WKWebView {
        let web = WKWebView(frame: .zero)
        web.navigationDelegate = context.coordinator
        context.coordinator.progressCancellable = web.publisher(for: \.estimatedProgress)
            .receive(on: RunLoop.main)
            .sink { [weak coordinator = context.coordinator] value in
                coordinator?.parent.progress = value
            }
        web.load(URLRequest(url: url))
        return web
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {
        context.coordinator.parent = self
    }

    static func dismantleUIView(_ uiView: WKWebView, coordinator: Coordinator) {
        uiView.navigationDelegate = nil
        coordinator.progressCancellable?.cancel()
        coordinator.progressCancellable = nil
    }

    final class Coordinator: NSObject, WKNavigationDelegate {
        var parent: WebViewBridge
        var progressCancellable: AnyCancellable?

        init(_ parent: WebViewBridge) { self.parent = parent }

        func webView(_ webView: WKWebView, didStartProvisionalNavigation navigation: WKNavigation!) {
            parent.isLoading = true
        }
        func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
            parent.isLoading = false
        }
        func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
            parent.isLoading = false
        }
    }
}
