import SwiftUI

/// Shows proper use of GeometryReader by constraining its size and using it for responsive layout.
struct GeometryReaderExample: View {
    var body: some View {
        VStack {
            Color.blue
                .frame(height: 100)
                .overlay(
                    GeometryReader { proxy in
                        let width = proxy.size.width
                        Text("Width: \(Int(width))")
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity, alignment: .center)
                    }
                )
            Spacer()
            ResponsiveGrid()
        }
        .padding()
    }
}

/// A responsive grid that adapts number of columns based on available width.
struct ResponsiveGrid: View {
    let items = Array(1...20)
    var body: some View {
        GeometryReader { proxy in
            let columns = Int(proxy.size.width / 80)
            LazyVGrid(columns: Array(repeating: GridItem(.flexible(), spacing: 8), count: max(columns, 1)), spacing: 8) {
                ForEach(items, id: \ .self) { item in
                    Text("\(item)")
                        .frame(height: 40)
                        .frame(maxWidth: .infinity)
                        .background(Color.blue.opacity(0.2))
                        .cornerRadius(8)
                }
            }
        }
        .frame(height: 200)
    }
}

struct GeometryReaderExample_Previews: PreviewProvider {
    static var previews: some View {
        GeometryReaderExample()
            .previewLayout(.sizeThatFits)
    }
}