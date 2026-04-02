import SwiftUI

/// Demonstrates view composition by building a card from smaller components.
struct Avatar: View {
    let imageName: String
    var body: some View {
        Image(systemName: imageName)
            .resizable()
            .scaledToFit()
            .frame(width: 40, height: 40)
            .padding(4)
            .background(Color.gray.opacity(0.2))
            .clipShape(Circle())
    }
}

struct NameBadge: View {
    let name: String
    var body: some View {
        Text(name)
            .font(.headline)
    }
}

struct CardView: View {
    let image: String
    let name: String
    let detail: String
    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Avatar(imageName: image)
            VStack(alignment: .leading, spacing: 4) {
                NameBadge(name: name)
                Text(detail)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }
            Spacer()
        }
        .padding()
        .background(RoundedRectangle(cornerRadius: 12).fill(Color.white))
        .shadow(color: .black.opacity(0.1), radius: 4, x: 0, y: 2)
    }
}

struct ViewCompositionDemo: View {
    var body: some View {
        VStack(spacing: 20) {
            CardView(image: "person.circle", name: "Alice", detail: "Senior iOS Engineer")
            CardView(image: "person.circle.fill", name: "Bob", detail: "Designer")
        }
        .padding()
        .background(Color(.systemGroupedBackground))
    }
}

struct ViewCompositionDemo_Previews: PreviewProvider {
    static var previews: some View {
        ViewCompositionDemo()
    }
}