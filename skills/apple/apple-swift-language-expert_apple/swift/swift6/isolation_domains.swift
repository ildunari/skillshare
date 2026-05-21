// swift/swift6/isolation_domains.swift
struct ImageChunk { var bytes: [UInt8] }
struct Image { var chunks: [ImageChunk] }

func process(_ img: Image, transform: (Image) -> Image) -> Image {
    return transform(img)
}

func pipeline(incoming: [Image]) -> [Image] {
    incoming.map { img in
        process(img) { im in
            var out = im
            out.chunks.reverse()
            return out
        }
    }
}
