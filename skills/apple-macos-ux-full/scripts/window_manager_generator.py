#!/usr/bin/env python3
"""
window_manager_generator.py
Generate multi-window architecture code with restoration and autosave.

This generator creates a singleton `WindowManager` that manages a set of
`NSWindowController` instances keyed by role.  On macOS 26 and later,
you can choose to create window controllers that embed Liquid Glass
surfaces (see `glass_window_generator.py`).  The window manager itself
remains agnostic of materials.

Usage:
  python window_manager_generator.py --out WindowManager.swift --roles Main,Inspector,Library
"""
import os, argparse
from pathlib import Path

TEMPLATE = """import AppKit
import SwiftUI

final class WindowManager: NSObject {{
    static let shared = WindowManager()
    private var controllers: [String: NSWindowController] = [:]

    func show(role: String, make: () -> NSWindowController) {{
        if let wc = controllers[role] {{
            wc.showWindow(nil)
            wc.window?.makeKeyAndOrderFront(nil)
            return
        }}
        let wc = make()
        controllers[role] = wc
        wc.window?.isRestorable = true
        wc.window?.setFrameAutosaveName(role + "Window")
        wc.showWindow(nil)
    }}

    func close(role: String) {{
        controllers[role]?.close()
        controllers.remove(role)
    }}

    func restoreWindows() {{
        // Called at launch to restore known roles
        for (role, wc) in controllers {{
            wc.window?.isRestorable = true
            wc.window?.setFrameAutosaveName(role + "Window")
        }}
    }}
}}
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="WindowManager.swift")
    ap.add_argument("--roles", default="Main,Inspector")
    args = ap.parse_args()

    roles = [r.strip() for r in args.roles.split(",") if r.strip()]
    code = TEMPLATE
    Path(args.out).write_text(code, encoding='utf-8')
    print(f"Wrote WindowManager to {args.out} with roles: {roles}")

if __name__ == '__main__':
    main()
