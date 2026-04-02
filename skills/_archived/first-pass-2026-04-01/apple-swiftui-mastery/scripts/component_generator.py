#!/usr/bin/env python3
"""
component_generator.py

A CLI tool to scaffold SwiftUI component boilerplate with state management.  It generates
Swift files containing a view struct, optional state variables, a placeholder body and preview.

Usage:
    python component_generator.py ComponentName --state count:Int title:String

This creates a file named `ComponentName.swift` in the current working directory.  It
declares `@State` properties for each supplied variable and uses them in the body.
"""
import argparse
import os
from textwrap import indent


def parse_state_args(state_args):
    """Parse state arguments like ['count:Int', 'title:String'] into a list of (name, type)."""
    result = []
    for arg in state_args:
        if ':' not in arg:
            raise ValueError(f"State argument '{arg}' must be in the format name:Type")
        name, typ = arg.split(':', 1)
        name = name.strip()
        typ = typ.strip()
        result.append((name, typ))
    return result


def generate_component(name: str, states: list[tuple[str, str]]) -> str:
    """Return the contents of a SwiftUI component file."""
    lines = []
    lines.append("import SwiftUI\n")
    # Define the view struct
    lines.append(f"struct {name}: View {{")
    # Add state variables
    for state_name, state_type in states:
        default_value = ""  # choose a sensible default
        if state_type.lower() in {"int", "double", "float"}:
            default_value = " = 0"
        elif state_type.lower() == "string":
            default_value = " = \"\""
        elif state_type.lower() == "bool" or state_type.lower() == "boolean":
            default_value = " = false"
        lines.append(f"    @State private var {state_name}: {state_type}{default_value}")
    # Body
    lines.append("\n    var body: some View {")
    lines.append("        VStack {")
    lines.append(f"            Text(\"{name}\")")
    for state_name, _ in states:
        lines.append(f"            Text(\"{state_name}: \\({state_name}\)\")")
    lines.append("        }\n    }")
    lines.append("}\n")
    # Preview
    lines.append(f"#if DEBUG\nstruct {name}_Previews: PreviewProvider {{")
    lines.append("    static var previews: some View {")
    lines.append(f"        {name}()")
    lines.append("    }\n}\n#endif")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate a SwiftUI component boilerplate.")
    parser.add_argument("name", help="Name of the SwiftUI component (struct name)")
    parser.add_argument("--state", nargs="*", default=[], help="State variables in the format name:Type")
    parser.add_argument("--output", default=".", help="Directory to place the generated Swift file")
    args = parser.parse_args()

    try:
        states = parse_state_args(args.state)
    except ValueError as e:
        parser.error(str(e))

    content = generate_component(args.name, states)
    filename = os.path.join(args.output, f"{args.name}.swift")
    # Write file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {filename}")


if __name__ == "__main__":
    main()