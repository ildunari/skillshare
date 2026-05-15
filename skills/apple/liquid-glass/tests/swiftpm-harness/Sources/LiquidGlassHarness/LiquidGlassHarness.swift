import SwiftUI
import UIKit

@available(iOS 26.0, *)
public struct LiquidGlassHarnessRoot: View {
    @State private var searchText = ""
    @State private var message = ""
    @State private var isExpanded = false
    @Namespace private var glassNamespace

    public init() {}

    public var body: some View {
        TabView {
            Tab("Threads", systemImage: "bubble.left.and.bubble.right") {
                NavigationStack {
                    List(["Glass composer", "Canvas controls", "Tool calls"], id: \.self) { item in
                        Text(item)
                    }
                    .navigationTitle("Threads")
                    .searchable(text: $searchText, prompt: "Search threads")
                }
            }

            Tab("Canvas", systemImage: "rectangle.on.rectangle") {
                CanvasHarnessView(message: $message, isExpanded: $isExpanded, namespace: glassNamespace)
            }
        }
        .tabBarMinimizeBehavior(.onScrollDown)
        .tabViewBottomAccessory {
            HStack(spacing: 8) {
                Image(systemName: "bolt.fill")
                Text("1 active agent")
                    .font(.footnote.weight(.semibold))
                Spacer()
                Button("Stop", systemImage: "stop.fill") {}
                    .buttonStyle(.glass)
                    .tint(.red)
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 8)
        }
    }
}

@available(iOS 26.0, *)
private struct CanvasHarnessView: View {
    @Binding var message: String
    @Binding var isExpanded: Bool
    let namespace: Namespace.ID

    var body: some View {
        ZStack {
            LinearGradient(colors: [.indigo, .blue, .purple], startPoint: .topLeading, endPoint: .bottomTrailing)
                .backgroundExtensionEffect()
                .ignoresSafeArea()

            GlassEffectContainer(spacing: 8) {
                Group {
                    if isExpanded {
                        VStack(alignment: .leading, spacing: 12) {
                            Text("Canvas tools")
                                .font(.headline)
                            HStack {
                                Button("Annotate", systemImage: "pencil.tip") {}
                                    .buttonStyle(.glass)
                                Button("Share", systemImage: "square.and.arrow.up") {}
                                    .buttonStyle(.glass)
                                Button("Collapse", systemImage: "chevron.down") {
                                    withAnimation(.spring(response: 0.32, dampingFraction: 0.82)) {
                                        isExpanded = false
                                    }
                                }
                                .buttonStyle(.glassProminent)
                            }
                        }
                        .padding()
                        .glassEffect(.regular, in: .rect(cornerRadius: 24))
                        .glassEffectID("canvas-tools", in: namespace)
                    } else {
                        Button("Tools", systemImage: "slider.horizontal.3") {
                            withAnimation(.spring(response: 0.32, dampingFraction: 0.82)) {
                                isExpanded = true
                            }
                        }
                        .buttonStyle(.glass)
                        .glassEffectID("canvas-tools", in: namespace)
                    }
                }
            }
        }
        .safeAreaBar(edge: .bottom, spacing: 0) {
            GlassEffectContainer(spacing: 8) {
                HStack(spacing: 8) {
                    Button("Attach", systemImage: "paperclip") {}
                        .buttonStyle(.glass)

                    TextField("Ask about this canvas", text: $message)
                        .textFieldStyle(.plain)
                        .padding(.horizontal, 12)
                        .padding(.vertical, 10)
                        .glassEffect(.regular.interactive(), in: Capsule())

                    Button("Send", systemImage: "arrow.up") {}
                        .buttonStyle(.glassProminent)
                        .contentTransition(.symbolEffect(.replace))
                }
                .padding(.horizontal, 12)
                .padding(.vertical, 10)
            }
        }
    }
}

@available(iOS 26.0, *)
public final class UIKitGlassHarnessView: UIView {
    private let effectView = UIVisualEffectView(effect: UIGlassEffect())

    public override init(frame: CGRect) {
        super.init(frame: frame)
        effectView.translatesAutoresizingMaskIntoConstraints = false
        addSubview(effectView)
        NSLayoutConstraint.activate([
            effectView.leadingAnchor.constraint(equalTo: leadingAnchor),
            effectView.trailingAnchor.constraint(equalTo: trailingAnchor),
            effectView.topAnchor.constraint(equalTo: topAnchor),
            effectView.bottomAnchor.constraint(equalTo: bottomAnchor)
        ])
    }

    @available(*, unavailable)
    public required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
}
