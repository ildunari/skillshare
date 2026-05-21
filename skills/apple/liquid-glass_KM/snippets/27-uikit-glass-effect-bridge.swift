#if canImport(UIKit)
import SwiftUI
import UIKit

@available(iOS 26.0, *)
final class UIKitGlassAccessoryView: UIVisualEffectView {
    private let stack = UIStackView()
    private let stopButton = UIButton(type: .system)

    init() {
        let glass = UIGlassEffect()
        glass.isInteractive = true
        super.init(effect: glass)
        configureView()
        configureButtons()
    }

    required init?(coder: NSCoder) {
        let glass = UIGlassEffect()
        glass.isInteractive = true
        super.init(coder: coder)
        effect = glass
        configureView()
        configureButtons()
    }

    private func configureView() {
        clipsToBounds = true
        layer.cornerCurve = .continuous
        layer.cornerRadius = 24

        stack.axis = .horizontal
        stack.alignment = .center
        stack.spacing = 8
        stack.isLayoutMarginsRelativeArrangement = true
        stack.directionalLayoutMargins = NSDirectionalEdgeInsets(top: 8, leading: 10, bottom: 8, trailing: 10)
        stack.translatesAutoresizingMaskIntoConstraints = false
        contentView.addSubview(stack)

        NSLayoutConstraint.activate([
            stack.leadingAnchor.constraint(equalTo: contentView.leadingAnchor),
            stack.trailingAnchor.constraint(equalTo: contentView.trailingAnchor),
            stack.topAnchor.constraint(equalTo: contentView.topAnchor),
            stack.bottomAnchor.constraint(equalTo: contentView.bottomAnchor)
        ])
    }

    private func configureButtons() {
        let status = UILabel()
        status.text = "Agent running"
        status.font = .preferredFont(forTextStyle: .footnote)

        var secondary = UIButton.Configuration.glass()
        secondary.title = "Tools"
        secondary.image = UIImage(systemName: "slider.horizontal.3")
        secondary.imagePadding = 6

        let toolsButton = UIButton(configuration: secondary)
        toolsButton.accessibilityLabel = "Open agent tools"

        var prominent = UIButton.Configuration.prominentGlass()
        prominent.title = "Stop"
        prominent.image = UIImage(systemName: "stop.fill")
        prominent.imagePadding = 6
        prominent.baseForegroundColor = .systemRed

        stopButton.configuration = prominent
        stopButton.accessibilityLabel = "Stop active agent"

        stack.addArrangedSubview(status)
        stack.addArrangedSubview(toolsButton)
        stack.addArrangedSubview(stopButton)
    }
}

@available(iOS 26.0, *)
struct UIKitGlassAccessoryRepresentable: UIViewRepresentable {
    func makeUIView(context: Context) -> UIKitGlassAccessoryView {
        UIKitGlassAccessoryView()
    }

    func updateUIView(_ uiView: UIKitGlassAccessoryView, context: Context) {}
}

@available(iOS 26.0, *)
final class UIKitGlassBottomAccessoryTabController: UITabBarController {
    override func viewDidLoad() {
        super.viewDidLoad()

        let accessory = UIHostingController(rootView:
            HStack(spacing: 8) {
                Image(systemName: "bolt.fill")
                Text("Agent running")
                    .font(.footnote.weight(.semibold))
                Button("Stop", systemImage: "stop.fill") {}
                    .buttonStyle(.glass)
                    .tint(.red)
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 8)
        )

        setBottomAccessory(accessory, animated: false)
    }
}

@available(iOS 26.0, *)
#Preview("UIKit glass bridge") {
    UIKitGlassAccessoryRepresentable()
        .frame(height: 56)
        .padding()
}
#endif
