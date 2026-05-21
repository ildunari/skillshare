// swift/swift5_9/generics_existentials.swift
protocol Serializer {
    associatedtype Output
    func serialize() -> Output
}

struct AnySerializer<Output>: Serializer {
    private let _serialize: () -> Output
    init<S: Serializer>(_ s: S) where S.Output == Output { _serialize = s.serialize }
    func serialize() -> Output { _serialize() }
}

func write<S: Serializer>(item: S) where S.Output == Data { _ = item.serialize() }

func makeDataSerializer() -> some Serializer<Output == Data> {
    struct User: Serializer { func serialize() -> Data { Data() } }
    return User()
}

let serializers: [AnySerializer<Data>] = []
