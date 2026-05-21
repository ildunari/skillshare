#!/usr/bin/env python3
"""
glass_window_generator.py

Generate a simple AppKit window controller that uses Liquid Glass surfaces.

This helper script reduces the boilerplate required to set up a window with
`NSGlassEffectView` for its content area and optionally configures a
unified toolbar.  The generated Swift code targets macOS 26 and later and
illustrates the recommended patterns for Liquid Glass on macOS.

Example spec (command line flags):

```
python glass_window_generator.py --out MyGlassWindow.swift \
    --title "Inspector" --width 500 --height 300 --controller InspectorWindowController
```

This writes a Swift file defining `InspectorWindowController`, which
allocates an NSWindow, sets a unified toolbar style, and embeds an
`NSGlassEffectView` as the root view.  You can modify the generated
StackView contents to suit your application.
"""
import argparse
from pathlib import Path

TEMPLATE = '''import AppKit

@available(macOS 26.0, *)
final class {controller_name}: NSWindowController {{
    override init(window: NSWindow?) {{
        let wnd = NSWindow(contentRect: NSRect(x: 0, y: 0, width: {width}, height: {height}),
                           styleMask: [.titled, .closable, .resizable],
                           backing: .buffered,
                           defer: false)
        wnd.title = "{title}"
        wnd.toolbarStyle = .unified
        super.init(window: wnd)
        setup()
    }}

    required init?(coder: NSCoder) {{
        fatalError("init(coder:) has not been implemented")
    }}

    private func setup() {{
        guard let window = self.window else {{ return }}
        // Create glass surface
        let glass = NSGlassEffectView()
        glass.cornerRadius = 14
        glass.tintColor = .controlAccentColor
        // Empty stack for your custom content
        let stack = NSStackView()
        stack.orientation = .vertical
        stack.spacing = 12
        // TODO: add your controls to 'stack'
        glass.contentView = stack
        window.contentView = glass
    }}
}}
'''

def main():
    parser = argparse.ArgumentParser(description="Generate a Liquid Glass window controller")
    parser.add_argument('--out', required=True, help='Destination Swift file')
    parser.add_argument('--title', default='Glass Window', help='Window title')
    parser.add_argument('--width', type=int, default=600, help='Window width')
    parser.add_argument('--height', type=int, default=400, help='Window height')
    parser.add_argument('--controller', default='GlassWindowController', help='Controller class name')
    args = parser.parse_args()

    code = TEMPLATE.format(controller_name=args.controller, title=args.title, width=args.width, height=args.height)
    Path(args.out).write_text(code, encoding='utf-8')
    print(f"Wrote glass window code to {args.out}")

if __name__ == '__main__':
    main()