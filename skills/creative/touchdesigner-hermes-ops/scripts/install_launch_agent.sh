#!/usr/bin/env bash
set -euo pipefail

LABEL="com.kosta.touchdesigner.twozero"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"
APP="/Applications/TouchDesigner.app"
LOG_DIR="$HOME/Library/Logs"

mkdir -p "$HOME/Library/LaunchAgents" "$LOG_DIR"

if [[ ! -d "$APP" ]]; then
  echo "TouchDesigner.app not found at $APP" >&2
  echo "Install with: brew install --cask touchdesigner" >&2
  exit 1
fi

cat > "$PLIST" <<'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.kosta.touchdesigner.twozero</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/open</string>
    <string>-a</string>
    <string>/Applications/TouchDesigner.app</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>StandardOutPath</key>
  <string>/Users/Kosta/Library/Logs/com.kosta.touchdesigner.twozero.out.log</string>
  <key>StandardErrorPath</key>
  <string>/Users/Kosta/Library/Logs/com.kosta.touchdesigner.twozero.err.log</string>
</dict>
</plist>
PLIST

console_user=$(stat -f '%Su' /dev/console 2>/dev/null || true)
current_user=$(id -un)

echo "Wrote $PLIST"

if [[ "$console_user" == "$current_user" ]]; then
  launchctl bootout "gui/$(id -u)" "$PLIST" 2>/dev/null || true
  launchctl bootstrap "gui/$(id -u)" "$PLIST"
  launchctl enable "gui/$(id -u)/$LABEL"
  echo "Loaded $LABEL for current GUI session."
else
  echo "Not loading now: console user is '$console_user', current user is '$current_user'."
  echo "It will be ready to load when $current_user owns the GUI session."
fi
