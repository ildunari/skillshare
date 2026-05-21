import SwiftUI
import Combine

/// Keyboard height publisher example bridged into SwiftUI
final class KeyboardObserver: ObservableObject {
    @Published var height: CGFloat = 0
    private var cancellables = Set<AnyCancellable>()

    init(center: NotificationCenter = .default) {
        center.publisher(for: UIResponder.keyboardWillChangeFrameNotification)
            .compactMap { $0.userInfo?[UIResponder.keyboardFrameEndUserInfoKey] as? CGRect }
            .map { $0.height }
            .receive(on: RunLoop.main)
            .sink { [weak self] h in self?.height = h }
            .store(in: &cancellables)
    }
}

struct KeyboardAvoidingScroll: View {
    @StateObject private var kb = KeyboardObserver()
    var body: some View {
        ScrollView {
            VStack(spacing: 16) {
                ForEach(0..<40) { i in
                    Text("Row \(i)").frame(maxWidth: .infinity).padding().background(Color.gray.opacity(0.1)).cornerRadius(8)
                }
            }.padding()
        }
        .padding(.bottom, kb.height)
        .animation(.default, value: kb.height)
    }
}
