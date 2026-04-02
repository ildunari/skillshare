import SwiftUI

/// A five-pointed star shape.
struct StarShape: Shape {
    func path(in rect: CGRect) -> Path {
        let center = CGPoint(x: rect.midX, y: rect.midY)
        let points = stride(from: 0, to: 360, by: 72).map { angle -> CGPoint in
            let radians = CGFloat(angle) * .pi / 180
            let radius = min(rect.width, rect.height) / 2
            let x = center.x + radius * cos(radians)
            let y = center.y + radius * sin(radians)
            return CGPoint(x: x, y: y)
        }
        var path = Path()
        guard let first = points.first else { return path }
        path.move(to: first)
        for i in 1..<points.count {
            let idx = (i * 2) % points.count
            path.addLine(to: points[idx])
        }
        path.closeSubpath()
        return path
    }
}

struct StarShapeDemo: View {
    var body: some View {
        StarShape()
            .stroke(Color.purple, lineWidth: 4)
            .frame(width: 120, height: 120)
            .padding()
    }
}

struct StarShapeDemo_Previews: PreviewProvider {
    static var previews: some View {
        StarShapeDemo()
    }
}