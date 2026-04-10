// swift/swift5_9/property_wrapper_examples.swift
import Foundation

@propertyWrapper
struct Clamped<Value: Comparable> {
    private var value: Value
    let range: ClosedRange<Value>
    init(wrappedValue: Value, _ range: ClosedRange<Value>) {
        self.range = range
        self.value = min(max(wrappedValue, range.lowerBound), range.upperBound)
    }
    var wrappedValue: Value {
        get { value }
        set { value = min(max(newValue, range.lowerBound), range.upperBound) }
    }
    var projectedValue: Self { self }
}

@propertyWrapper
struct MainActorBox<T> {
    @MainActor private var value: T
    init(wrappedValue: @MainActor T) { self._value = MainActor.assumeIsolated(wrappedValue) }
    var wrappedValue: T {
        get { value }
        set { value = newValue }
    }
}

struct AudioSettings {
    @Clamped(0...1) var volume: Double = 0.5
}
