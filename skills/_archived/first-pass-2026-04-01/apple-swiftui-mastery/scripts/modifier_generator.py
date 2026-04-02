#!/usr/bin/env python3
"""
modifier_generator.py

Generate a SwiftUI ViewModifier template.

Usage:
    python modifier_generator.py MyModifier --param color:Color opacity:Double

This creates `MyModifier.swift` in the current directory with a struct conforming to
`ViewModifier` that applies parameters to the content.  It also generates an extension
to `View` for easy usage.
"""
import argparse
import os


def parse_params(params: list[str]):
    result = []
    for p in params:
        if ':' not in p:
            raise ValueError(f"Parameter '{p}' must be in name:Type format")
        name, typ = p.split(':', 1)
        result.append((name.strip(), typ.strip()))
    return result


def generate_modifier(name: str, params: list[tuple[str, str]]) -> str:
    lines = []
    lines.append("import SwiftUI\n")
    lines.append(f"public struct {name}: ViewModifier {{")
    # Parameter properties
    for param_name, param_type in params:
        lines.append(f"    let {param_name}: {param_type}")
    lines.append("\n    public func body(content: Content) -> some View {")
    lines.append("        content")
    # Apply sample modifications based on types
    for param_name, param_type in params:
        if param_type.endswith("Color"):
            lines.append(f"            .foregroundColor({param_name})")
        elif param_type.lower() in {"double", "float", "cgfloat"}:
            lines.append(f"            .opacity({param_name})")
    lines.append("    }\n}")
    # Extension for convenience
    lines.append("\nextension View {")
    # parameter list string
    param_list = ", ".join([f"{n}: {t}" for n, t in params])
    call_params = ", ".join([f"{n}: {n}" for n, _ in params])
    lines.append(f"    public func {name[0].lower() + name[1:]}({param_list}) -> some View {{")
    lines.append(f"        modifier({name}({call_params}))")
    lines.append("    }\n}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate a SwiftUI ViewModifier template.")
    parser.add_argument("name", help="Name of the modifier struct")
    parser.add_argument("--param", nargs="*", default=[], help="Parameters in name:Type format")
    parser.add_argument("--output", default=".", help="Output directory")
    args = parser.parse_args()

    try:
        params = parse_params(args.param)
    except ValueError as e:
        parser.error(str(e))

    content = generate_modifier(args.name, params)
    filename = os.path.join(args.output, f"{args.name}.swift")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated {filename}")


if __name__ == '__main__':
    main()