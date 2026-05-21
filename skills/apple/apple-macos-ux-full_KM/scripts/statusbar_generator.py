#!/usr/bin/env python3
"""
statusbar_generator.py
Generate macOS status bar app templates for AppKit (NSStatusItem) and SwiftUI (MenuBarExtra).

Usage:
  python statusbar_generator.py --mode appkit --out StatusBarController.swift
  python statusbar_generator.py --mode swiftui --out StatusBarScene.swift

On macOS 26 and later, the SwiftUI template applies Liquid Glass to the
popover content by calling `.glassEffect(.regular, in: RoundedRectangle(cornerRadius: 12))` on the
outer `VStack`.  The AppKit template remains unchanged; you can add
`NSGlassEffectView` manually if you need a glass popover.
"""
import os, argparse, textwrap
from pathlib import Path

APPKIT = """import AppKit

final class StatusBarController: NSObject {{
    private var statusItem: NSStatusItem!
    private let menu = NSMenu()

    override init() {{
        super.init()
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
        if let button = statusItem.button {{
            button.image = NSImage(systemSymbolName: "bolt.horizontal", accessibilityDescription: "Utility")
            button.action = #selector(toggle(_:))
            button.target = self
        }}
        buildMenu()
    }}

    private func buildMenu() {{
        let openItem = NSMenuItem(title: "Open Window", action: #selector(openWindow(_:)), keyEquivalent: "o")
        openItem.keyEquivalentModifierMask = [.command]
        openItem.target = self
        menu.addItem(openItem)

        menu.addItem(NSMenuItem.separator())
        let quitItem = NSMenuItem(title: "Quit", action: #selector(quit(_:)), keyEquivalent: "q")
        quitItem.keyEquivalentModifierMask = [.command]
        quitItem.target = self
        menu.addItem(quitItem)
    }}

    @objc private func toggle(_ sender: Any?) {{
        statusItem.menu = menu
        statusItem.popUpMenu(menu)
        statusItem.menu = nil
    }}

    @objc private func openWindow(_ sender: Any?) {{
        NSApp.activate(ignoringOtherApps: true)
        // You can forward to your window controller; example:
        if let appDelegate = NSApp.delegate as? AppDelegate {{
            let wc = MainWindowController()
            wc.show()
        }}
    }}

    @objc private func quit(_ sender: Any?) {{
        NSApp.terminate(sender)
    }}
}}
"""

SWIFTUI = """import SwiftUI

struct StatusContent: View {{
    @State private var value = 0
    var body: some View {{
        VStack(alignment: .leading) {{
            Text("Quick Utility").font(.headline)
            HStack {{
                Text("Value: \\(value)")
                Spacer()
                Button("Add") {{ value += 1 }}
            }}
            Divider()
            Button("Open Main Window") {{
                NSApp.activate(ignoringOtherApps: true)
            }}
            Button("Quit") {{ NSApp.terminate(nil) }}
        }}
        .padding(12)
        .frame(width: 240)
        // Apply Liquid Glass on macOS 26 and later; ignored on earlier systems
        .glassEffect(.regular, in: RoundedRectangle(cornerRadius: 12))
    }}
}}

struct StatusBarScene: Scene {{
    var body: some Scene {{
        MenuBarExtra("Utility") {{
            StatusContent()
        }}
    }}
}}
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["appkit","swiftui"], required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    code = APPKIT if args.mode == "appkit" else SWIFTUI
    Path(args.out).write_text(code, encoding="utf-8")
    print(f"Wrote status bar template to {args.out}")

if __name__ == "__main__":
    main()
