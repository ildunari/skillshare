import UIKit
import SwiftUI

extension UIViewController {
    /// Adds a SwiftUI view as a child via UIHostingController and pins it to the given container.
    func embed<Content: View>(_ view: Content, in container: UIView) -> UIHostingController<Content> {
        let host = UIHostingController(rootView: view)
        addChild(host)
        host.view.translatesAutoresizingMaskIntoConstraints = false
        container.addSubview(host.view)
        NSLayoutConstraint.activate([
            host.view.topAnchor.constraint(equalTo: container.topAnchor),
            host.view.leadingAnchor.constraint(equalTo: container.leadingAnchor),
            host.view.trailingAnchor.constraint(equalTo: container.trailingAnchor),
            host.view.bottomAnchor.constraint(equalTo: container.bottomAnchor),
        ])
        host.didMove(toParent: self)
        return host
    }
}
