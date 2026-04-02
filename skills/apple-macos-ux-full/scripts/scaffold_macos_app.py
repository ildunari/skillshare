#!/usr/bin/env python3
"""
scaffold_macos_app.py
Generate a complete hybrid AppKit+SwiftUI skeleton with production defaults.

Usage:
  python scaffold_macos_app.py --name MyApp --out ./MyApp --bundle com.example.myapp --swiftui yes --statusbar no

What you get:
  - App.swift (SwiftUI entry) + AppDelegate (NSApplicationDelegate)
  - Unified toolbar-ready window controller with transparent titlebar
  - SwiftUI NavigationSplitView content + AppKit bridges (NSHostingController)
  - Commands (menus) and Settings scene
  - Optional MenuBarExtra and NSStatusItem-based status bar stub
"""
import os, argparse, textwrap, json
from pathlib import Path

APP_SWIFT = """import SwiftUI
import AppKit

@main
struct {APP_NAME}App: App {{
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate

    var body: some Scene {{
        WindowGroup("{APP_NAME}") {{
            RootView()
        }}
        .windowStyle(.automatic)
        .defaultSize(width: 1000, height: 700)
        .windowToolbarStyle(.unified)
        .commands {{ AppCommands() }}

        Settings {{
            SettingsView()
        }}
        {MENUBAR_SCENE}
    }}
}}
"""

APP_DELEGATE = """import AppKit
import SwiftUI

final class AppDelegate: NSObject, NSApplicationDelegate {{
    func applicationDidFinishLaunching(_ notification: Notification) {{
        // Opt-out of automatic window tabbing unless explicitly desired.
        NSWindow.allowsAutomaticWindowTabbing = false
    }}
}}
"""

ROOT_VIEW = """import SwiftUI

struct RootView: View {{
    @State private var selection: SidebarItem? = .inbox

    var body: some View {{
        NavigationSplitView {{
            SidebarView(selection: $selection)
        }} detail: {{
            DetailContainer(selection: selection)
        }}
        .navigationSplitViewStyle(.balanced)
    }}
}}

enum SidebarItem: Hashable {{
    case inbox, today, starred
}}

struct SidebarView: View {{
    @Binding var selection: SidebarItem?
    var body: some View {{
        List(selection: $selection) {{
            Section("Library") {{
                Label("Inbox", systemImage: "tray").tag(SidebarItem.inbox)
                Label("Today", systemImage: "sun.max").tag(SidebarItem.today)
                Label("Starred", systemImage: "star").tag(SidebarItem.starred)
            }}
        }}
        .listStyle(.sidebar)
    }}
}}

struct DetailContainer: View {{
    let selection: SidebarItem?
    var body: some View {{
        Group {{
            switch selection {{
            case .inbox: Text("Inbox")
            case .today: Text("Today")
            case .starred: Text("Starred")
            case .none: Text("Select an item")
            }}
        }}
        .padding()
    }}
}}
"""

SETTINGS_VIEW = """import SwiftUI

struct SettingsView: View {{
    @AppStorage("launchAtLogin") private var launchAtLogin = false
    @AppStorage("showBadges") private var showBadges = true

    var body: some View {{
        Form {{
            Toggle("Launch at Login", isOn: $launchAtLogin)
            Toggle("Show Badges", isOn: $showBadges)
        }}
        .padding(20)
        .frame(minWidth: 420, idealWidth: 520)
    }}
}}
"""

COMMANDS = """import SwiftUI

struct AppCommands: Commands {
    @Environment(\.openSettings) private var openSettings

    var body: some Commands {
        CommandGroup(replacing: .appSettings) {
            Button("Settings…") { openSettings() }
                .keyboardShortcut(",", modifiers: .command)
        }
        CommandMenu("Navigate") {
            Button("Show Sidebar") { /* toggle logic */ }
                .keyboardShortcut("s", modifiers: [.command, .option])
        }
    }
}
"""

STATUSBAR_SWIFTUI = """import SwiftUI

struct StatusUI: View {{
    @State private var counter = 0
    var body: some View {{
        VStack(alignment: .leading, spacing: 8) {{
            Text("Status Utility")
                .font(.headline)
            HStack {{
                Text("Count: \\(counter)")
                Spacer()
                Button("Increment") {{ counter += 1 }}
            }}
            Divider()
            Button("Quit") {{ NSApp.terminate(nil) }}
        }}
        .padding(12)
        .frame(width: 260)
    }}
}}
"""

MENUBAR_EXTRA = """
        MenuBarExtra("\\U0001F5D4 Status") {
            StatusUI()
        }
"""

APPKIT_WINDOW = """import Cocoa
import SwiftUI

final class MainWindowController: NSWindowController, NSWindowDelegate {{
    convenience init() {{
        let contentView = NSHostingView(rootView: RootView())
        let window = NSWindow(contentRect: NSRect(x: 0, y: 0, width: 1000, height: 700),
                              styleMask: [.titled, .resizable, .closable, .miniaturizable],
                              backing: .buffered,
                              defer: false)
        window.center()
        window.titleVisibility = .hidden
        window.titlebarAppearsTransparent = true
        window.isReleasedWhenClosed = false
        window.toolbar = NSToolbar(identifier: "MainToolbar")
        window.toolbarStyle = .unified
        window.contentView = contentView
        self.init(window: window)
        window.delegate = self
        window.setFrameAutosaveName("MainWindow")
    }}

    func show() {{
        window?.makeKeyAndOrderFront(nil)
    }}
}}
"""

def materialize(out_dir: Path, name: str, include_swiftui_menubar: bool):
    src = out_dir / "Sources"
    os.makedirs(src, exist_ok=True)

    w = lambda p, c: (p.write_text(c, encoding="utf-8"))

    w(src / "App.swift", APP_SWIFT.format(APP_NAME=name, MENUBAR_SCENE=(MENUBAR_EXTRA if include_swiftui_menubar else "")))
    w(src / "AppDelegate.swift", APP_DELEGATE)
    w(src / "RootView.swift", ROOT_VIEW)
    w(src / "SettingsView.swift", SETTINGS_VIEW)
    w(src / "AppCommands.swift", COMMANDS)
    w(src / "StatusUI.swift", STATUSBAR_SWIFTUI)
    w(src / "MainWindowController.swift", APPKIT_WINDOW)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True, help="App display name and title")
    ap.add_argument("--bundle", default="com.example.app", help="Bundle identifier (informational)")
    ap.add_argument("--out", required=True, help="Output folder to generate sources")
    ap.add_argument("--menubar", choices=["yes","no"], default="no", help="Include SwiftUI MenuBarExtra scene")
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    materialize(out_dir, args.name, include_swiftui_menubar=(args.menubar == "yes"))

    readme = f"""# {args.name}

This folder contains a hybrid AppKit + SwiftUI skeleton generated by scaffold_macos_app.py.
- Entry: `App.swift` with Scenes (WindowGroup, Settings{", MenuBarExtra" if args.menubar=="yes" else ""})
- AppKit window: `MainWindowController.swift` with unified toolbar & transparent titlebar
- Commands: `AppCommands.swift`
- Settings: `SettingsView.swift`
"""
    (Path(args.out) / "README.md").write_text(readme, encoding="utf-8")
    print(f"Scaffold created in: {out_dir}")

if __name__ == "__main__":
    main()
