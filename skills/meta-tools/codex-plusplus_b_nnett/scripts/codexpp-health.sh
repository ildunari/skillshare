#!/usr/bin/env bash
set -euo pipefail

APP="${CODEXPP_APP:-/Applications/Coding/Codex (Beta).app}"
ROOT="${CODEXPP_ROOT:-$HOME/Library/Application Support/codex-plusplus}"
REPO="${CODEXPP_REPO:-$HOME/LocalDev/codex-plusplus}"

echo "== Codex++ health =="
echo "app:  $APP"
echo "root: $ROOT"
echo "repo: $REPO"
echo

if command -v codexplusplus >/dev/null 2>&1; then
  codexplusplus status || true
  echo
  codexplusplus doctor || true
else
  echo "codexplusplus CLI not found on PATH"
fi

echo
echo "== Repo =="
if [ -d "$REPO/.git" ]; then
  git -C "$REPO" status --short --branch
  git -C "$REPO" log -1 --oneline --decorate
else
  echo "repo missing"
fi

echo
echo "== Watcher =="
launchctl list 2>/dev/null | grep -i codexplusplus || echo "no launchd codexplusplus entry found"

echo
echo "== Logs =="
if [ -d "$ROOT/log" ]; then
  find "$ROOT/log" -maxdepth 1 -type f -print
else
  echo "log dir missing"
fi
