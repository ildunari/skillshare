
import Foundation

class Downloader {
    var onComplete: ((Data) -> Void)?

    func start() {
        URLSession.shared.dataTask(with: URL(string: "https://example.com")!) { data, _, _ in
            guard let data = data else { return }
            self.onComplete?(data) // retain cycle potential if self owns onComplete
        }.resume()
    }
}

class Controller {
    let downloader = Downloader()
    func load() {
        downloader.onComplete = { data in
            self.handle(data) // [weak self] missing
        }
        downloader.start()
    }
    func handle(_ data: Data) { print(data.count) }
}
