#if canImport(UIKit)
import UIKit

@available(iOS 26.0, *)
final class UIKitLiquidGlassToolbar: UIView {
    private let glassView = UIVisualEffectView(effect: UIGlassContainerEffect())
    private let stack = UIStackView()
    private let sendButton = UIButton(type: .system)
    private var isStreaming = false

    override init(frame: CGRect) {
        super.init(frame: frame)
        setUpGlassContainer()
        setUpButtons()
    }

    required init?(coder: NSCoder) {
        super.init(coder: coder)
        setUpGlassContainer()
        setUpButtons()
    }

    private func setUpGlassContainer() {
        translatesAutoresizingMaskIntoConstraints = false
        glassView.translatesAutoresizingMaskIntoConstraints = false
        glassView.clipsToBounds = true
        glassView.layer.cornerCurve = .continuous
        glassView.layer.cornerRadius = 28

        addSubview(glassView)
        NSLayoutConstraint.activate([
            glassView.leadingAnchor.constraint(equalTo: leadingAnchor),
            glassView.trailingAnchor.constraint(equalTo: trailingAnchor),
            glassView.topAnchor.constraint(equalTo: topAnchor),
            glassView.bottomAnchor.constraint(equalTo: bottomAnchor)
        ])

        stack.axis = .horizontal
        stack.alignment = .center
        stack.spacing = 10
        stack.isLayoutMarginsRelativeArrangement = true
        stack.directionalLayoutMargins = NSDirectionalEdgeInsets(top: 10, leading: 12, bottom: 10, trailing: 12)
        stack.translatesAutoresizingMaskIntoConstraints = false
        glassView.contentView.addSubview(stack)
        NSLayoutConstraint.activate([
            stack.leadingAnchor.constraint(equalTo: glassView.contentView.leadingAnchor),
            stack.trailingAnchor.constraint(equalTo: glassView.contentView.trailingAnchor),
            stack.topAnchor.constraint(equalTo: glassView.contentView.topAnchor),
            stack.bottomAnchor.constraint(equalTo: glassView.contentView.bottomAnchor)
        ])
    }

    private func setUpButtons() {
        stack.addArrangedSubview(makeButton(title: "Tools", symbol: "slider.horizontal.3", action: #selector(showTools)))
        stack.addArrangedSubview(makeButton(title: "Voice", symbol: "mic.fill", action: #selector(startVoice)))
        stack.addArrangedSubview(sendButton)
        configureSendButton()
    }

    private func makeButton(title: String, symbol: String, action: Selector) -> UIButton {
        let button = UIButton(type: .system)
        var configuration = UIButton.Configuration.plain()
        configuration.title = title
        configuration.image = UIImage(systemName: symbol)
        configuration.imagePadding = 6
        configuration.cornerStyle = .capsule
        configuration.symbolContentTransition = UISymbolContentTransition(.replace)
        button.configuration = configuration
        button.addTarget(self, action: action, for: .touchUpInside)
        button.accessibilityLabel = title
        return button
    }

    private func configureSendButton() {
        var configuration = UIButton.Configuration.filled()
        configuration.title = isStreaming ? "Stop" : "Send"
        configuration.image = UIImage(systemName: isStreaming ? "stop.fill" : "arrow.up")
        configuration.imagePadding = 6
        configuration.cornerStyle = .capsule
        configuration.baseBackgroundColor = isStreaming ? .systemRed : .tintColor
        configuration.symbolContentTransition = UISymbolContentTransition(.replace)
        sendButton.configuration = configuration
        sendButton.accessibilityLabel = isStreaming ? "Stop streaming" : "Send prompt"
        sendButton.removeTarget(nil, action: nil, for: .touchUpInside)
        sendButton.addTarget(self, action: #selector(toggleStreaming), for: .touchUpInside)
    }

    @objc private func toggleStreaming() {
        isStreaming.toggle()
        UIView.animate(withDuration: 0.22, delay: 0, options: [.allowUserInteraction, .beginFromCurrentState]) {
            self.configureSendButton()
        }
    }

    @objc private func showTools() {}
    @objc private func startVoice() {}
}
#endif
