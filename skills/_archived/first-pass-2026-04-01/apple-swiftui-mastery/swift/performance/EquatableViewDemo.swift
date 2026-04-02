import SwiftUI

/// Demonstrates using Equatable to avoid unnecessary view updates.
struct ScoreView: View, Equatable {
    var score: Int
    static func == (lhs: ScoreView, rhs: ScoreView) -> Bool {
        lhs.score / 10 == rhs.score / 10
    }
    var body: some View {
        Text("Score: \(score)")
            .padding()
            .background(Color.green.opacity(0.2))
            .cornerRadius(8)
    }
}

struct EquatableViewDemo: View {
    @State private var score: Int = 0
    var body: some View {
        VStack(spacing: 20) {
            ScoreView(score: score)
            Button("Add 1") { score += 1 }
            Text("Tap the button; the view only updates when score crosses a multiple of 10.")
                .font(.footnote)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
        }
        .padding()
    }
}

struct EquatableViewDemo_Previews: PreviewProvider {
    static var previews: some View {
        EquatableViewDemo()
    }
}