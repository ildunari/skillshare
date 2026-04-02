#!/usr/bin/env python3
"""
navigation_scaffolder.py

Scaffold a basic navigation architecture using NavigationStack and NavigationDestination.

Given a list of screen names, this script creates a Swift file defining an enum
representing each screen, a root NavigationStack with a path binding, and stub
destination views.  Use this to bootstrap navigation in new SwiftUI projects.

Usage:
    python navigation_scaffolder.py --screens Home Settings Detail

This will generate a file called `Navigation.swift` containing an enum `Screen` with
cases `.home`, `.settings`, `.detail`, plus a root `NavigationStack` and placeholder
views `HomeView`, `SettingsView`, `DetailView`.
"""
import argparse
import os


def generate_navigation(screens: list[str]) -> str:
    enum_cases = [s[0].lower() + s[1:] for s in screens]
    lines = []
    lines.append("import SwiftUI\n")
    # Screen enum
    lines.append("enum Screen: Hashable {")
    for case_name in enum_cases:
        lines.append(f"    case {case_name}")
    lines.append("}\n")
    # Root view
    lines.append("struct RootNavigationView: View {")
    lines.append("    @State private var path: [Screen] = []")
    lines.append("    var body: some View {")
    lines.append("        NavigationStack(path: $path) {")
    lines.append("            List {")
    for case_name, screen_name in zip(enum_cases, screens):
        lines.append(f"                NavigationLink(value: Screen.{case_name}) {{ Text(\"{screen_name}\") }}")
    lines.append("            }")
    lines.append("            .navigationDestination(for: Screen.self) { screen in")
    lines.append("                switch screen {")
    for case_name, screen_name in zip(enum_cases, screens):
        lines.append(f"                case .{case_name}: {screen_name}View()")
    lines.append("                }")
    lines.append("            }")
    lines.append("        }")
    lines.append("    }\n}")
    # Destination stubs
    for screen_name in screens:
        lines.append("\nstruct {}View: View {{".format(screen_name))
        lines.append("    var body: some View {")
        lines.append(f"        Text(\"{screen_name} View\")")
        lines.append("    }\n}")
    # Preview
    lines.append("\n#if DEBUG\nstruct RootNavigationView_Previews: PreviewProvider {")
    lines.append("    static var previews: some View {")
    lines.append("        RootNavigationView()")
    lines.append("    }\n}\n#endif")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Scaffold a SwiftUI navigation architecture.")
    parser.add_argument("--screens", nargs='+', help="Names of screens to generate", required=True)
    parser.add_argument("--output", default=".", help="Output directory")
    args = parser.parse_args()
    content = generate_navigation(args.screens)
    filename = os.path.join(args.output, "Navigation.swift")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated {filename}")


if __name__ == '__main__':
    main()