#!/usr/bin/env python3
"""
layout_generator.py

Generate a custom layout implementing the SwiftUI Layout protocol.

Usage:
    python layout_generator.py FlowLayout --orientation horizontal --spacing 8

It produces a Swift file `FlowLayout.swift` in the current directory.  The generated
layout arranges its subviews in either horizontal or vertical flow, wrapping
to new rows or columns when exceeding available space.
"""
import argparse
import os


def generate_layout(name: str, orientation: str, spacing: float) -> str:
    is_horizontal = orientation.lower() == 'horizontal'
    lines = []
    lines.append("import SwiftUI\n")
    lines.append(f"public struct {name}: Layout {{")
    lines.append(f"    public var spacing: CGFloat = {spacing}")
    lines.append("\n    public func sizeThatFits(_ proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) -> CGSize {")
    if is_horizontal:
        lines.append("        var totalWidth: CGFloat = 0")
        lines.append("        var maxHeight: CGFloat = 0")
        lines.append("        var rowWidth: CGFloat = 0")
        lines.append("        var rowHeight: CGFloat = 0")
        lines.append("        let maxWidth = proposal.width ?? .infinity")
        lines.append("        for subview in subviews {")
        lines.append("            let size = subview.sizeThatFits(proposal)")
        lines.append("            if rowWidth + size.width + spacing > maxWidth {")
        lines.append("                totalWidth = max(totalWidth, rowWidth)")
        lines.append("                maxHeight += rowHeight + spacing")
        lines.append("                rowWidth = size.width")
        lines.append("                rowHeight = size.height")
        lines.append("            } else {")
        lines.append("                rowWidth += size.width + spacing")
        lines.append("                rowHeight = max(rowHeight, size.height)")
        lines.append("            }")
        lines.append("        }")
        lines.append("        totalWidth = max(totalWidth, rowWidth)")
        lines.append("        maxHeight += rowHeight")
        lines.append("        return CGSize(width: totalWidth, height: maxHeight)")
    else:
        lines.append("        var totalHeight: CGFloat = 0")
        lines.append("        var maxWidth: CGFloat = 0")
        lines.append("        var columnHeight: CGFloat = 0")
        lines.append("        var columnWidth: CGFloat = 0")
        lines.append("        let maxHeight = proposal.height ?? .infinity")
        lines.append("        for subview in subviews {")
        lines.append("            let size = subview.sizeThatFits(proposal)")
        lines.append("            if columnHeight + size.height + spacing > maxHeight {")
        lines.append("                totalHeight = max(totalHeight, columnHeight)")
        lines.append("                maxWidth += columnWidth + spacing")
        lines.append("                columnHeight = size.height")
        lines.append("                columnWidth = size.width")
        lines.append("            } else {")
        lines.append("                columnHeight += size.height + spacing")
        lines.append("                columnWidth = max(columnWidth, size.width)")
        lines.append("            }")
        lines.append("        }")
        lines.append("        totalHeight = max(totalHeight, columnHeight)")
        lines.append("        maxWidth += columnWidth")
        lines.append("        return CGSize(width: maxWidth, height: totalHeight)")
    lines.append("    }\n")
    lines.append("    public func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) {")
    if is_horizontal:
        lines.append("        var x: CGFloat = bounds.minX")
        lines.append("        var y: CGFloat = bounds.minY")
        lines.append("        var rowHeight: CGFloat = 0")
        lines.append("        for subview in subviews {")
        lines.append("            let size = subview.sizeThatFits(proposal)")
        lines.append("            if x + size.width > bounds.maxX {")
        lines.append("                x = bounds.minX")
        lines.append("                y += rowHeight + spacing")
        lines.append("                rowHeight = 0")
        lines.append("            }")
        lines.append("            subview.place(at: CGPoint(x: x, y: y), proposal: ProposedViewSize(size))")
        lines.append("            x += size.width + spacing")
        lines.append("            rowHeight = max(rowHeight, size.height)")
        lines.append("        }")
    else:
        lines.append("        var x: CGFloat = bounds.minX")
        lines.append("        var y: CGFloat = bounds.minY")
        lines.append("        var columnWidth: CGFloat = 0")
        lines.append("        for subview in subviews {")
        lines.append("            let size = subview.sizeThatFits(proposal)")
        lines.append("            if y + size.height > bounds.maxY {")
        lines.append("                y = bounds.minY")
        lines.append("                x += columnWidth + spacing")
        lines.append("                columnWidth = 0")
        lines.append("            }")
        lines.append("            subview.place(at: CGPoint(x: x, y: y), proposal: ProposedViewSize(size))")
        lines.append("            y += size.height + spacing")
        lines.append("            columnWidth = max(columnWidth, size.width)")
        lines.append("        }")
    lines.append("    }\n}")
    # Extension for convenience
    lines.append("\nextension Layout where Self == {} {{".format(name))
    lines.append("    static func {}(spacing: CGFloat = {}) -> Self {{".format(name[0].lower() + name[1:], spacing))
    lines.append(f"        {name}(spacing: spacing)")
    lines.append("    }\n}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate a custom SwiftUI layout.")
    parser.add_argument("name", help="Name of the layout struct")
    parser.add_argument("--orientation", choices=["horizontal", "vertical"], default="horizontal", help="Flow orientation")
    parser.add_argument("--spacing", type=float, default=8.0, help="Spacing between views")
    parser.add_argument("--output", default=".", help="Output directory")
    args = parser.parse_args()

    content = generate_layout(args.name, args.orientation, args.spacing)
    filename = os.path.join(args.output, f"{args.name}.swift")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated {filename}")


if __name__ == '__main__':
    main()