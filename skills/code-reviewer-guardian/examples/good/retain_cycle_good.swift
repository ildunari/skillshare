
import Foundation
class Downloader {
    var onComplete: ((Data) -> Void)?
    func start() {
        URLSession.shared.dataTask(with: URL(string: "https://example.com")!) { [weak self] data, _, _ in
            guard let self = self, let data = data else { return }
            self.onComplete?(data)
        }.resume()
    }
}
class Controller {
    let downloader = Downloader()
    func load() {
        downloader.onComplete = { [weak self] data in
            self?.handle(data)
        }
        downloader.start()
    }
    func handle(_ data: Data) { print(data.count) }
}
