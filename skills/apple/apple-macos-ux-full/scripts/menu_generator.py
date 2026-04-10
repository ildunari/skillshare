#!/usr/bin/env python3
"""
menu_generator.py
Generate Swift menu structures (SwiftUI Commands or AppKit NSMenu) from JSON/YAML.

Examples:
  python menu_generator.py --spec templates/menu.json --swiftui-out AppCommands.swift
  python menu_generator.py --spec templates/menu.yaml --appkit-out MainMenu.swift --mode appkit

Spec format (JSON/YAML):
{
  "mode": "swiftui|appkit",
  "menus": [
    { "title": "File", "items": [
        {"label": "New Window", "action": "newWindow:", "key": "n", "modifiers": ["command"]},
        {"separator": true},
        {"label": "Close Window", "action": "performClose:", "key": "w", "modifiers": ["command"]}
    ]}
  ]
}
"""
import os, argparse, json, re
from pathlib import Path

def parse_minimal_yaml(text: str):
    # Minimal, indentation-based YAML parser for simple dict/list specs used by templates.
    # Supports keys, strings, numbers, booleans, null, and lists of dicts.
    lines = [l.rstrip() for l in text.splitlines() if l.strip() and not l.strip().startswith("#")]
    idx = 0

    def parse_block(indent=0):
        nonlocal idx
        obj = {}
        lst = None
        while idx < len(lines):
            line = lines[idx]
            cur_indent = len(line) - len(line.lstrip())
            if cur_indent < indent:
                break
            if cur_indent > indent:
                # parse nested block for previous key
                if lst is not None and isinstance(obj, dict) and "__lastkey__" in obj:
                    key = obj.pop("__lastkey__")
                    obj[key] = parse_block(cur_indent)
                else:
                    # attach nested block to last added list item if any
                    if isinstance(lst, list) and len(lst)>0 and isinstance(lst[-1], dict):
                        nested = parse_block(cur_indent)
                        lst[-1].update(nested if isinstance(nested, dict) else {"value": nested})
                continue

            # at same indent
            s = line.strip()
            if s.startswith("- "):
                if lst is None:
                    lst = []
                val = s[2:]
                if ":" in val:
                    key, v = [p.strip() for p in val.split(":", 1)]
                    item = {key: parse_scalar(v)}
                else:
                    item = parse_scalar(val)
                lst.append(item if isinstance(item, dict) else {"value": item})
                idx += 1
            else:
                if ":" in s:
                    key, v = [p.strip() for p in s.split(":", 1)]
                    if v == "":
                        # nested to follow
                        obj["__lastkey__"] = key
                        idx += 1
                    else:
                        obj[key] = parse_scalar(v)
                        idx += 1
                else:
                    idx += 1
        if lst is not None and obj:
            # merge dict with list as "items" when appropriate
            obj["items"] = lst
            return obj
        return lst if lst is not None else obj

    def parse_scalar(v: str):
        if v in ("null", "Null", "NULL", "~"): return None
        if v in ("true", "True", "TRUE"): return True
        if v in ("false", "False", "FALSE"): return False
        if re.match(r"^-?\d+$", v): return int(v)
        if re.match(r"^-?\d+\.\d+$", v): return float(v)
        return v.strip('"\'')
    return parse_block(0)

def load_spec(path: Path):
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml # type: ignore
            return yaml.safe_load(text)
        except Exception:
            return parse_minimal_yaml(text)
    return json.loads(text)

def swift_mods(mods):
    mapping = {
        "command": ".command",
        "option": ".option",
        "shift": ".shift",
        "control": ".control"
    }
    return "[" + ", ".join(mapping[m.lower()] for m in mods) + "]" if mods else "[]"

def gen_swiftui_commands(spec):
    parts = [
        "import SwiftUI",
        "",
        "struct AppCommands: Commands {",
        "    var body: some Commands {",
    ]
    for menu in spec.get("menus", []):
        parts.append(f'        CommandMenu("{menu["title"]}") {{')
        for it in menu.get("items", []):
            if it.get("separator"):
                parts.append("            Divider()")
                continue
            label = it["label"]
            action = it.get("action", "")
            key = it.get("key")
            mods = swift_mods(it.get("modifiers", []))
            if key:
                parts.append(f'            Button("{label}") {{ NSApp.sendAction(Selector(("{action}")), to: nil, from: nil) }}'
                             f'.keyboardShortcut("{key}", modifiers: {mods})')
            else:
                parts.append(f'            Button("{label}") {{ NSApp.sendAction(Selector(("{action}")), to: nil, from: nil) }}')
        parts.append("        }")
    parts += ["    }", "}", ""]
    return "\n".join(parts)

def gen_appkit_menu(spec):
    out = [
        "import AppKit",
        "",
        "final class MainMenuBuilder {",
        "    static func build() -> NSMenu {",
        "        let mainMenu = NSMenu(title: \"MainMenu\")",
        "        NSApp.mainMenu = mainMenu",
        "        ",
    ]
    for menu in spec.get("menus", []):
        title = menu["title"]
        out += [
            f'        let {title.lower()}Menu = NSMenu(title: "{title}")',
            f'        let {title.lower()}Item = NSMenuItem(title: "{title}", action: nil, keyEquivalent: "")',
            f'        mainMenu.addItem({title.lower()}Item)',
            f'        mainMenu.setSubmenu({title.lower()}Menu, for: {title.lower()}Item)',
        ]
        for it in menu.get("items", []):
            if it.get("separator"):
                out.append(f'        {title.lower()}Menu.addItem(NSMenuItem.separator())')
                continue
            label = it["label"]
            action = it.get("action", "noop:")
            key = it.get("key", "")
            mods = it.get("modifiers", [])
            out.append(f'        do {{')
            out.append(f'            let item = NSMenuItem(title: "{label}", action: Selector(("{action}")), keyEquivalent: "{key}")')
            if mods:
                mask_exprs = []
                for m in mods:
                    mm = m.lower()
                    if mm == "command": mask_exprs.append(".command")
                    elif mm == "option": mask_exprs.append(".option")
                    elif mm == "shift": mask_exprs.append(".shift")
                    elif mm == "control": mask_exprs.append(".control")
                out.append(f'            item.keyEquivalentModifierMask = NSEvent.ModifierFlags([{", ".join(mask_exprs)}])')
            out.append(f'            item.target = nil')
            out.append(f'            {title.lower()}Menu.addItem(item)')
            out.append(f'        }}')
    out += [
        "        return mainMenu",
        "    }",
        "}",
        ""
    ]
    return "\n".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True, help="Path to menu JSON/YAML spec")
    ap.add_argument("--swiftui-out", help="Output Swift file for SwiftUI Commands")
    ap.add_argument("--appkit-out", help="Output Swift file for AppKit NSMenu builder")
    ap.add_argument("--mode", choices=["swiftui","appkit"], help="Override mode from spec")
    args = ap.parse_args()

    spec = load_spec(Path(args.spec))
    mode = args.mode or spec.get("mode", "swiftui")
    if mode == "swiftui":
        code = gen_swiftui_commands(spec)
        out = args.swiftui_out or "AppCommands.swift"
        Path(out).write_text(code, encoding="utf-8")
        print(f"Wrote SwiftUI Commands to {out}")
    else:
        code = gen_appkit_menu(spec)
        out = args.appkit_out or "MainMenu.swift"
        Path(out).write_text(code, encoding="utf-8")
        print(f"Wrote AppKit menu builder to {out}")

if __name__ == "__main__":
    main()
