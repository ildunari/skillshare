import AppKit

/// GlassContainerExample showcases how NSGlassEffectContainerView groups
/// multiple glass surfaces so they share sampling and morph together.  Two
/// buttons are wrapped in individual NSGlassEffectViews and placed inside
/// an NSStackView, which is then assigned as the contentView of the
/// container.  The container itself is centered in its parent.
@available(macOS 26.0, *)
final class GlassContainerExample: NSViewController {
    override func loadView() {
        self.view = NSView()
        buildUI()
    }

    private func buildUI() {
        // Create two glass buttons
        let glass1 = NSGlassEffectView()
        glass1.cornerRadius = 12
        let button1 = NSButton(title: "One", target: nil, action: nil)
        glass1.contentView = button1

        let glass2 = NSGlassEffectView()
        glass2.cornerRadius = 12
        let button2 = NSButton(title: "Two", target: nil, action: nil)
        glass2.contentView = button2

        // Arrange them in a horizontal stack
        let hstack = NSStackView(views: [glass1, glass2])
        hstack.orientation = .horizontal
        hstack.alignment = .centerY
        hstack.spacing = 8

        // Group into a glass container
        let container = NSGlassEffectContainerView()
        container.contentView = hstack

        self.view.addSubview(container)
        container.translatesAutoresizingMaskIntoConstraints = false
        NSLayoutConstraint.activate([
            container.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            container.centerYAnchor.constraint(equalTo: view.centerYAnchor),
            glass1.widthAnchor.constraint(equalToConstant: 80),
            glass2.widthAnchor.constraint(equalToConstant: 80),
            glass1.heightAnchor.constraint(equalToConstant: 32),
            glass2.heightAnchor.constraint(equalToConstant: 32)
        ])
    }
}