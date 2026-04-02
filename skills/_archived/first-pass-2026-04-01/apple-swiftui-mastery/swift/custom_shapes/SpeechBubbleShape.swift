import SwiftUI

/// A speech bubble shape with a rounded rectangle and a tail.
struct SpeechBubbleShape: Shape {
    func path(in rect: CGRect) -> Path {
        var path = Path()
        let cornerRadius: CGFloat = 12
        let tailWidth: CGFloat = 20
        let tailHeight: CGFloat = 12
        let bubbleRect = CGRect(x: rect.minX, y: rect.minY, width: rect.width - tailWidth, height: rect.height)
        path.addRoundedRect(in: bubbleRect, cornerSize: CGSize(width: cornerRadius, height: cornerRadius))
        // Tail
        let tailTip = CGPoint(x: bubbleRect.maxX + tailWidth, y: bubbleRect.midY)
        let tailStart = CGPoint(x: bubbleRect.maxX, y: bubbleRect.midY - tailHeight/2)
        let tailEnd = CGPoint(x: bubbleRect.maxX, y: bubbleRect.midY + tailHeight/2)
        path.move(to: tailStart)
        path.addLine(to: tailTip)
        path.addLine(to: tailEnd)
        path.closeSubpath()
        return path
    }
}

struct SpeechBubbleShape_Demo: View {
    var body: some View {
        SpeechBubbleShape()
            .fill(Color.blue)
            .frame(width: 200, height: 80)
            .overlay(
                Text("Hello!")
                    .foregroundColor(.white)
                    .padding(.leading, 16), alignment: .leading
            )
            .padding()
    }
}

struct SpeechBubbleShape_Previews: PreviewProvider {
    static var previews: some View {
        SpeechBubbleShape_Demo()
    }
}