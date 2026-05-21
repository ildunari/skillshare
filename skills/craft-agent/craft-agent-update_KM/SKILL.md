---
name: "Craft Agent Update & Repatch"
description: |
  Update Craft Agents Electron app to the latest version and re-apply local patches
  (window size, multi_tool_use.parallel fix). Handles quit, backup, install, patch,
  re-sign, and relaunch. Use when the user says "update craft agent" or "repatch".
targets: [Craft-MyWorkspace, Craft-Brown]
alwaysAllow: ["Bash", "Read", "Write", "Edit"]
---

# Craft Agent Update & Repatch

Automates the full update cycle for the Craft Agents Electron app at `/Applications/AI/Craft Agents.app/`.

## When to Use

- After a new version is downloaded by the auto-updater (check `~/Library/Caches/@craft-agentelectron-updater/pending/`)
- When the user says "update craft agent", "repatch", or "re-apply patches"
- After manually downloading a new version

## Background

Craft Agents is an Electron app. We apply two local patches to the compiled JS bundles:

1. **Window size patch** (`main.cjs`): Reduce `minWidth`/`minHeight` to 300 so the app can be resized very small
2. **multi_tool_use.parallel patch** (`interceptor.cjs`): Decompose GPT-5.x's hallucinated `multi_tool_use.parallel` tool wrapper into individual tool calls

Modifying files in the `.app` bundle breaks the code signature, which blocks the auto-updater. After patching, we re-sign with ad-hoc signature to restore `app.isPackaged = true`.

## Procedure

### 1. Check for updates

```bash
# Check current version
cat "/Applications/AI/Craft Agents.app/Contents/Resources/app/package.json" | python3 -c "import sys,json; print(json.load(sys.stdin)['version'])"

# Check pending update
ls -la ~/Library/Caches/@craft-agentelectron-updater/pending/
cat ~/Library/Caches/@craft-agentelectron-updater/pending/update-info.json 2>/dev/null
```

If no pending update exists, check if the user has a DMG in Downloads.

### 2. Run the update script

The script handles the full flow: extract → quit app → backup → install → patch → re-sign → verify → relaunch.

```bash
#!/bin/bash
set -euo pipefail

APP="/Applications/AI/Craft Agents.app"
ZIP="$HOME/Library/Caches/@craft-agentelectron-updater/pending/Craft-Agents-arm64.zip"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP="/Applications/AI/Craft Agents.app.backup-${STAMP}"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

echo "== Craft Agents update =="

# Extract update
if [ ! -f "$ZIP" ]; then
  echo "No pending update ZIP found at $ZIP"
  echo "Check ~/Downloads/ for a DMG or trigger update check in the app"
  exit 1
fi
unzip -qq "$ZIP" -d "$TMPDIR"

FRESH_APP="$TMPDIR/Craft Agents.app"
if [ ! -d "$FRESH_APP" ]; then
  echo "Fresh app bundle missing after extraction"
  exit 1
fi

# Quit app
echo "== requesting app quit =="
osascript -e 'tell application "Craft Agents" to quit' 2>/dev/null || true
for i in $(seq 1 60); do
  pgrep -f '/Applications/AI/Craft Agents.app/Contents/MacOS/Craft Agents' >/dev/null 2>&1 || break
  sleep 1
done
if pgrep -f '/Applications/AI/Craft Agents.app/Contents/MacOS/Craft Agents' >/dev/null 2>&1; then
  pkill -TERM -f '/Applications/AI/Craft Agents.app/Contents/MacOS/Craft Agents' || true
  sleep 3
fi
if pgrep -f '/Applications/AI/Craft Agents.app/Contents/MacOS/Craft Agents' >/dev/null 2>&1; then
  pkill -KILL -f '/Applications/AI/Craft Agents.app/Contents/MacOS/Craft Agents' || true
  sleep 2
fi

# Backup and install
echo "== backing up current app =="
[ -d "$APP" ] && mv "$APP" "$BACKUP"
echo "== installing fresh app =="
cp -R "$FRESH_APP" "$APP"

# Apply patches
MAIN="$APP/Contents/Resources/app/dist/main.cjs"
INTERCEPTOR="$APP/Contents/Resources/app/dist/interceptor.cjs"

echo "== applying patches =="
python3 - <<'PY'
from pathlib import Path

main = Path('/Applications/AI/Craft Agents.app/Contents/Resources/app/dist/main.cjs')
interceptor = Path('/Applications/AI/Craft Agents.app/Contents/Resources/app/dist/interceptor.cjs')

# --- Window size patch ---
m = main.read_text()
count_700 = m.count('minWidth: 700,')
count_800 = m.count('minWidth: 800,')
if count_700 < 1 or count_800 < 1:
    raise SystemExit(f'Window anchors not found (700={count_700}, 800={count_800}) — check if upstream changed')
m = m.replace('minWidth: 700,', 'minWidth: 300,', 1)
m = m.replace('minWidth: 800,', 'minWidth: 300,', 1)
main.write_text(m)
print('Window size patch applied')

# --- multi_tool_use.parallel patch ---
i = interceptor.read_text()
anchor = '        const parsed = JSON.parse(tc.arguments);\n'
if 'Decompose hallucinated multi_tool_use.parallel wrapper from GPT models' in i:
    print('Parallel patch already present (skipped)')
else:
    if anchor not in i:
        raise SystemExit('Interceptor anchor not found — check if upstream changed')
    patch = anchor + (
        '        // Decompose hallucinated multi_tool_use.parallel wrapper from GPT models\n'
        '        if (tc.name === "multi_tool_use.parallel" && Array.isArray(parsed.tool_uses)) {\n'
        '          debugLog(`[OpenAI SSE] Decomposed multi_tool_use.parallel into ${parsed.tool_uses.length} individual tool calls`);\n'
        '          parsed.tool_uses.forEach((sub, idx) => {\n'
        '            const subId = `${tc.id}_parallel_${idx}`;\n'
        '            const subName = sub.recipient_name || sub.name;\n'
        '            const subParams = sub.parameters || {};\n'
        '            delete subParams._intent;\n'
        '            delete subParams._displayName;\n'
        '            emitSseLine(JSON.stringify({\n'
        '              choices: [{ index: tc.choiceIndex, delta: {\n'
        '                tool_calls: [{ index: idx, id: subId, type: "function", function: { name: subName, arguments: "" } }]\n'
        '              }}]\n'
        '            }), controller);\n'
        '            emitSseLine(JSON.stringify({\n'
        '              choices: [{ index: tc.choiceIndex, delta: {\n'
        '                tool_calls: [{ index: idx, function: { arguments: JSON.stringify(subParams) } }]\n'
        '              }}]\n'
        '            }), controller);\n'
        '          });\n'
        '          continue;\n'
        '        }\n'
    )
    i = i.replace(anchor, patch, 1)
    interceptor.write_text(i)
    print('Parallel tool patch applied')
PY

# Re-sign (once, after all patches)
echo "== re-signing app =="
codesign --force --deep --sign - "$APP"

# Verify
echo "== verifying patches =="
grep -c 'minWidth: 300,' "$MAIN"
grep -c 'Decompose hallucinated multi_tool_use.parallel' "$INTERCEPTOR"

echo "== verifying signature =="
codesign --verify --deep --strict --verbose=2 "$APP"

# Relaunch
echo "== relaunching =="
open -a "$APP"

echo "== done =="
echo "Backup at: $BACKUP"
```

### 3. Post-update cleanup

Delete old backups (they're ~200MB+ each):

```bash
# List backups
ls -la /Applications/AI/ | grep backup

# Remove old ones (keep only the latest if desired)
rm -rf "/Applications/AI/Craft Agents.app.backup-YYYYMMDD-HHMMSS"
```

### 4. Clear updater cache (optional)

```bash
rm -rf "$HOME/Library/Application Support/Craft Agents/Code Cache"
rm -rf "$HOME/Library/Application Support/Craft Agents/Cache"
```

## Patch Details

### Window Size Patch

**File:** `main.cjs`
**What:** `minWidth: 700` → `300` (session window), `minWidth: 800` → `300` (main window)
**Why:** User wants very narrow layouts (down to 300px)
**Find with:** `grep -n "minWidth:" main.cjs`

### multi_tool_use.parallel Patch

**File:** `interceptor.cjs`
**What:** Intercepts the hallucinated `multi_tool_use.parallel` tool call from GPT-5.x and decomposes it into individual tool calls
**Why:** GPT models sometimes emit a fake wrapper tool instead of using OpenAI's native parallel tool calls. Without this patch, Pi SDK throws "tool not found"
**Anchor:** `const parsed = JSON.parse(tc.arguments);` inside `flushTrackedCalls()`

### Signature & Auto-Updater

- Modifying `.app` bundle files breaks the sealed code signature
- Broken signature → Electron thinks it's dev mode → auto-updater skips
- Ad-hoc re-sign (`codesign --force --deep --sign -`) restores `app.isPackaged = true`
- Always re-sign **once** after **all** patches are applied
- Updater cache: `~/Library/Caches/@craft-agentelectron-updater/`

## When Patches Become Unnecessary

- **Window size**: Remove when upstream adds a configurable minWidth or reduces it
- **multi_tool_use.parallel**: Remove when the Craft Agents team adds native handling in `interceptor.ts`
- Check release notes before patching — if a fix landed upstream, skip that patch
