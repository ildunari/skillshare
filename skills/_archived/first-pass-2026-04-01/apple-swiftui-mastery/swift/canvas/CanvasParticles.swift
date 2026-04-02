import SwiftUI

/// A particle system using TimelineView and Canvas. Particles move upwards and fade.
struct Particle: Identifiable {
    let id = UUID()
    var x: CGFloat
    var y: CGFloat
    var velocity: CGFloat
    var life: Double
}

struct CanvasParticles: View {
    @State private var particles: [Particle] = []
    let timer = Timer.publish(every: 0.02, on: .main, in: .common).autoconnect()
    var body: some View {
        TimelineView(.animation) { context in
            Canvas { ctx, size in
                // update particles
                let now = context.date.timeIntervalSinceReferenceDate
                particles = particles.filter { now - $0.life < 1 }
                // draw particles
                for particle in particles {
                    let age = now - particle.life
                    let opacity = 1 - age
                    let point = CGPoint(x: particle.x, y: particle.y - CGFloat(age) * particle.velocity)
                    var circle = Path(ellipseIn: CGRect(x: point.x, y: point.y, width: 6, height: 6))
                    ctx.opacity = opacity
                    ctx.fill(circle, with: .color(.orange))
                }
            }
            .onReceive(timer) { _ in
                // Add new particle
                let x = CGFloat.random(in: 0...100)
                let velocity = CGFloat.random(in: 40...80)
                let newParticle = Particle(x: x, y: 200, velocity: velocity, life: context.date.timeIntervalSinceReferenceDate)
                particles.append(newParticle)
            }
            .frame(height: 200)
        }
    }
}

struct CanvasParticles_Previews: PreviewProvider {
    static var previews: some View {
        CanvasParticles()
    }
}