#!/usr/bin/env python3
"""
toolbar_generator.py
Generate NSToolbar delegate & configuration from a JSON/YAML spec.

Spec (JSON/YAML):
```
{
  "identifier": "MainToolbar",
  "unified": true,
  "centered": "com.example.search",
  "allowed": [
    {
      "id": "com.example.new",
      "label": "New",
      "image": "plus",
      "action": "newDocument:",
      "style": "prominent",        // optional: "prominent" or "plain" for Liquid Glass
      "tint": "systemBlue"          // optional: NSColor static name for glass tint
    },
    {
      "id": "com.example.search",
      "label": "Search",
      "image": "magnifyingglass",
      "selectable": true,
      "style": "plain"
    }
  ],
  "default": ["com.example.new", "flexibleSpace", "com.example.search"]
}
```

The optional `style` and `tint` fields allow you to opt toolbar items into
macOS 26 Liquid Glass styling.  When `style` is `prominent`, the generated
code calls `item.style = .prominent` (otherwise `.plain`).  When `tint` is
specified, `item.backgroundTintColor` is set using a static property on
`NSColor` (e.g. `systemBlue`, `systemRed`).  These values are ignored on
macOS versions prior to 26.

Usage:
  python toolbar_generator.py --spec templates/toolbar.json --out ToolbarController.swift
"""
import os, argparse, json
from pathlib import Path

def load_spec(path: Path):
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml # type: ignore
            return yaml.safe_load(text)
        except Exception:
            raise SystemExit("YAML parsing requires PyYAML; use JSON or install pyyaml.")
    return json.loads(text)

def gen_toolbar(spec):
    ident = spec.get("identifier", "MainToolbar")
    unified = spec.get("unified", True)
    centered = spec.get("centered")
    allowed = spec.get("allowed", [])
    default = spec.get("default", [])

    code = []
    code.append("import AppKit")
    code.append("")
    code.append("final class ToolbarController: NSObject, NSToolbarDelegate {")
    code.append(f"    let toolbar = NSToolbar(identifier: \"{ident}\")")
    code.append("    override init() {")
    code.append("        super.init()")
    code.append("        toolbar.delegate = self")
    if unified:
        code.append("        if #available(macOS 11.0, *) {")
        code.append("            toolbar.allowsUserCustomization = true")
        code.append("        }")
    code.append("    }")
    code.append("")
    code.append("    func attach(to window: NSWindow) {")
    code.append("        window.toolbar = toolbar")
    code.append("        if #available(macOS 11.0, *) {")
    code.append("            window.toolbarStyle = .unified")
    if centered:
        code.append(f"            window.toolbar?.centeredItemIdentifier = NSToolbarItem.Identifier(\"{centered}\")")
    code.append("        }")
    code.append("    }")
    code.append("")
    # Allowed item identifiers
    code.append("    func toolbarAllowedItemIdentifiers(_ toolbar: NSToolbar) -> [NSToolbarItem.Identifier] {")
    items = [f"NSToolbarItem.Identifier(\"{a['id']}\")" for a in allowed]
    items += [".flexibleSpace", ".space", ".separator"]
    code.append(f"        return [{', '.join(items)}]")
    code.append("    }")
    code.append("")
    # Default items
    code.append("    func toolbarDefaultItemIdentifiers(_ toolbar: NSToolbar) -> [NSToolbarItem.Identifier] {")
    def_items = []
    for d in default:
        if d in ("flexibleSpace","space","separator"):
            mapping = { "flexibleSpace": ".flexibleSpace", "space": ".space", "separator": ".separator" }
            def_items.append(mapping[d])
        else:
            def_items.append(f"NSToolbarItem.Identifier(\"{d}\")")
    code.append(f"        return [{', '.join(def_items)}]")
    code.append("    }")
    code.append("")
    # Item creation
    code.append("    func toolbar(_ toolbar: NSToolbar, itemForItemIdentifier itemIdentifier: NSToolbarItem.Identifier, willBeInsertedIntoToolbar flag: Bool) -> NSToolbarItem? {")
    code.append("        switch itemIdentifier.rawValue {")
    for a in allowed:
        sel = a.get("action", "noop:")
        label = a.get("label", a["id"])
        image = a.get("image")
        style = a.get("style")
        tint = a.get("tint")
        code.append(f"        case \"{a['id']}\":")
        code.append(f"            let item = NSToolbarItem(itemIdentifier: itemIdentifier)")
        code.append(f"            item.label = \"{label}\"")
        if image:
            code.append(f"            item.image = NSImage(systemSymbolName: \"{image}\", accessibilityDescription: \"{label}\")")
        code.append(f"            item.target = nil")
        code.append(f"            item.action = Selector(\"{sel}\")")
        # Apply Liquid Glass style and tint when present
        if style:
            if style == "prominent":
                code.append("            if #available(macOS 26.0, *) { item.style = .prominent }")
            elif style == "plain":
                code.append("            if #available(macOS 26.0, *) { item.style = .plain }")
        if tint:
            code.append(f"            if #available(macOS 26.0, *) {{ item.backgroundTintColor = .{tint} }}")
        code.append("            return item")
    code.append("        default: return nil")
    code.append("        }")
    code.append("    }")
    code.append("}")
    return "\n".join(code)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", default="ToolbarController.swift")
    args = ap.parse_args()

    spec = load_spec(Path(args.spec))
    code = gen_toolbar(spec)
    Path(args.out).write_text(code, encoding='utf-8')
    print(f"Wrote toolbar to {args.out}")

if __name__ == '__main__':
    main()
