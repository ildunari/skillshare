import SwiftUI

/// Demonstrates implicit and explicit spring animations.
struct SpringAnimationDemo: View {
    @State private var offset: CGFloat = -200
    @State private var scale: CGFloat = 0.5

    var body: some View {
        VStack(spacing: 40) {
            // Implicit animation using .animation modifier
            Circle()
                .fill(Color.green)
                .frame(width: 100, height: 100)
                .offset(x: offset)
                .animation(.spring(response: 0.5, dampingFraction: 0.6), value: offset)

            // Explicit animation using withAnimation
            Rectangle()
                .fill(Color.orange)
                .frame(width: 100, height: 100)
                .scaleEffect(scale)
                .onTapGesture {
                    withAnimation(.interpolatingSpring(stiffness: 100, damping: 8)) {
                        scale = scale > 1 ? 0.5 : 1.5
                    }
                }
        }
        .padding()
        .onAppear {
            // Kick off implicit animation
            offset = 200
        }
    }
}

struct SpringAnimationDemo_Previews: PreviewProvider {
    static var previews: some View {
        SpringAnimationDemo()
    }
}