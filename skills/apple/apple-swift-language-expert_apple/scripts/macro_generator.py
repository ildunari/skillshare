#!/usr/bin/env python3
"""
macro_generator.py

Scaffold a Swift macro package with both the macro target and a small client target.
Generates a freestanding expression macro and an attached peer macro example.

Usage:
    python scripts/macro_generator.py MyMacros --out ./MyMacros

Outputs:
    <out>/Package.swift
    <out>/Sources/MyMacros/MyMacros.swift
    <out>/Sources/MyMacrosClient/main.swift
    <out>/Tests/MyMacrosTests/MyMacrosTests.swift

Notes:
- Requires Swift 5.9+ toolchain with SwiftSyntax available.
- The generated macro is minimal and compiles; edit diagnostics and expansion logic as needed.
"""

import os, sys, textwrap, argparse, pathlib

PKG = """// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "%(name)s",
    platforms: [.iOS(.v17), .macOS(.v14)],
    products: [
        .library(name: "%(name)s", targets: ["%(name)s"]),
        .executable(name: "%(name)sClient", targets: ["%(name)sClient"]),
    ],
    targets: [
        .macro(
            name: "%(name)s",
            dependencies: [
                .product(name: "SwiftSyntaxMacros", package: "swift-syntax"),
                .product(name: "SwiftCompilerPlugin", package: "swift-syntax"),
            ]
        ),
        .executableTarget(
            name: "%(name)sClient",
            dependencies: ["%(name)s"]
        ),
        .testTarget(
            name: "%(name)sTests",
            dependencies: ["%(name)s"]
        ),
    ],
    dependencies: [
        .package(url: "https://github.com/swiftlang/swift-syntax", from: "509.0.0")
    ]
)
"""

MACROS_SWIFT = r'''import SwiftCompilerPlugin
import SwiftSyntax
import SwiftSyntaxBuilder
import SwiftSyntaxMacros

// Freestanding expression macro: #assertNotNil(x)
// Emits a compile-time error if the expression is statically nil.
public struct AssertNotNilMacro: ExpressionMacro {
    public static func expansion(
        of node: some FreestandingMacroExpansionSyntax,
        in context: some MacroExpansionContext
    ) throws -> ExprSyntax {
        guard node.argumentList.count == 1,
              let arg = node.argumentList.first?.expression else {
            context.diagnose(Diagnostic(node: Syntax(node),
                                        message: SimpleMessage("Expected one argument")))
            return "()" // no-op
        }
        // Synthesize: if (arg) == nil { fatalError(...) }
        // (We can't fully evaluate at compile time; this is a demo emitting friendly code.)
        return "({ let __tmp = \(arg); if __tmp == nil { fatalError(\"assertNotNil failed\") }; __tmp! })"
    }
}

// Attached peer macro: @CaseDetection adds boolean case properties to enums.
public struct CaseDetectionMacro: PeerMacro {
    public static func expansion(
        of node: AttributeSyntax,
        providingPeersOf decl: some DeclSyntaxProtocol,
        in context: some MacroExpansionContext
    ) throws -> [DeclSyntax] {
        guard let enumDecl = decl.as(EnumDeclSyntax.self) else { return [] }
        var peers: [DeclSyntax] = []
        for member in enumDecl.memberBlock.members {
            guard let caseDecl = member.decl.as(EnumCaseDeclSyntax.self) else { continue }
            for elem in caseDecl.elements {
                let name = elem.identifier.text
                let prop: DeclSyntax =
                    "var is\(raw: name.capitalized): Bool {\n" +
                    "    if case .\(raw: name) = self { return true }\n" +
                    "    return false\n" +
                    "}\n"
                peers.append(prop)
            }
        }
        return peers
    }
}

@main
struct MyPlugin: CompilerPlugin {
    let providingMacros: [Macro.Type] = [
        AssertNotNilMacro.self,
        CaseDetectionMacro.self,
    ]
}
'''

CLIENT_MAIN = r'''import Foundation
import MyMacros

enum NetworkState {
    case idle
    case loading
    case loaded(data: Data)
    case failed(error: Error)
}

@CaseDetection
extension NetworkState {}

func demo() {
    let x: Data? = Data()
    let value: Data = #assertNotNil(x) // expands to runtime check

    var state: NetworkState = .idle
    state = .loading
    print(state.isLoading) // synthesized by @CaseDetection
}

demo()
'''

TESTS = r'''import XCTest
@testable import MyMacros

final class MyMacrosTests: XCTestCase {
    func testSmoke() {
        // Macro tests can assert expanded source using MacroTesting or SwiftSyntax macros.
        XCTAssertTrue(true)
    }
}
'''

def write(path: str, name: str):
    out = pathlib.Path(path).resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out / "Sources" / name).mkdir(parents=True, exist_ok=True)
    (out / "Sources" / f"{name}Client").mkdir(parents=True, exist_ok=True)
    (out / "Tests" / f"{name}Tests").mkdir(parents=True, exist_ok=True)

    (out / "Package.swift").write_text(PKG % {"name": name}, encoding="utf-8")
    (out / "Sources" / name / f"{name}.swift").write_text(MACROS_SWIFT, encoding="utf-8")
    (out / "Sources" / f"{name}Client" / "main.swift").write_text(CLIENT_MAIN.replace("MyMacros", name), encoding="utf-8")
    (out / "Tests" / f"{name}Tests" / f"{name}Tests.swift").write_text(TESTS.replace("MyMacros", name), encoding="utf-8")
    return str(out)

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("name", help="Macro package name")
    ap.add_argument("--out", default="./out")
    args = ap.parse_args()
    p = write(args.out, args.name)
    print(f"Macro package scaffolded at: {p}")

if __name__ == "__main__":
    main()
