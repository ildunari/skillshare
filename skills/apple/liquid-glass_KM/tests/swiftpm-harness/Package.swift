// swift-tools-version: 6.2
import PackageDescription

let package = Package(
    name: "LiquidGlassHarness",
    platforms: [
        .iOS(.v26)
    ],
    products: [
        .library(name: "LiquidGlassHarness", targets: ["LiquidGlassHarness"])
    ],
    targets: [
        .target(name: "LiquidGlassHarness")
    ]
)
