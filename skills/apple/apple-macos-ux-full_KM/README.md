# apple-macos-ux-full

A comprehensive skill for building native macOS apps with AppKit + SwiftUI.

## Quick Start

1) Generate a skeleton:
```
python scripts/scaffold_macos_app.py --name MyApp --out scaffold/MyApp --menubar yes
```

2) Create a menu from spec:
```
python scripts/menu_generator.py --spec templates/menu.yaml --swiftui-out scaffold/MyApp/Sources/AppCommands.swift
```

3) Create a toolbar:
```
python scripts/toolbar_generator.py --spec templates/toolbar.json --out scaffold/MyApp/Sources/ToolbarController.swift
```

4) Add status bar:
```
python scripts/statusbar_generator.py --mode swiftui --out scaffold/MyApp/Sources/StatusBarScene.swift
```

5) Add a window manager:
```
python scripts/window_manager_generator.py --out scaffold/MyApp/Sources/WindowManager.swift --roles Main,Inspector,Library
```

Open the folder in Xcode, set signing, and run.
