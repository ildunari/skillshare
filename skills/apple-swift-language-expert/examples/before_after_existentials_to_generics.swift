// examples/before_after_existentials_to_generics.swift
protocol Drawable { func draw() }
// BEFORE
func render(_ items: [any Drawable]) { items.forEach { $0.draw() } }
// AFTER
func render<T: Drawable>(_ items: [T]) { items.forEach { $0.draw() } }
