import SwiftUI

/// A reusable custom view modifier that adds rounded corners and a shadow.
struct RoundedShadowModifier: ViewModifier {
    var radius: CGFloat = 8
    var shadowColor: Color = .black.opacity(0.2)
    var shadowRadius: CGFloat = 4
    func body(content: Content) -> some View {
        content
            .clipShape(RoundedRectangle(cornerRadius: radius, style: .continuous))
            .shadow(color: shadowColor, radius: shadowRadius, x: 0, y: 2)
    }
}

extension View {
    func roundedShadow(radius: CGFloat = 8, shadowColor: Color = .black.opacity(0.2), shadowRadius: CGFloat = 4) -> some View {
        modifier(RoundedShadowModifier(radius: radius, shadowColor: shadowColor, shadowRadius: shadowRadius))
    }
}

struct RoundedShadowModifier_Demo: View {
    var body: some View {
        VStack(spacing: 20) {
            Text("Hello, world!")
                .padding()
                .background(Color.blue)
                .foregroundColor(.white)
                .roundedShadow()
            Image(systemName: "star.fill")
                .resizable()
                .frame(width: 50, height: 50)
                .foregroundColor(.yellow)
                .roundedShadow(radius: 12, shadowColor: .orange, shadowRadius: 6)
        }
        .padding()
    }
}

struct RoundedShadowModifier_Previews: PreviewProvider {
    static var previews: some View {
        RoundedShadowModifier_Demo()
    }
}