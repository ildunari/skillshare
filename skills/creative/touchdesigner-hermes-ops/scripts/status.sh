#!/usr/bin/env bash
set -euo pipefail

echo "Console user: $(stat -f '%Su' /dev/console 2>/dev/null || echo unknown)"
if brew list --cask touchdesigner >/dev/null 2>&1; then
  brew info --cask touchdesigner | sed -n '1,8p'
else
  echo "TouchDesigner: not installed"
fi

if [[ -f "$HOME/Downloads/twozero.tox" ]]; then
  ls -lh "$HOME/Downloads/twozero.tox"
else
  echo "twozero.tox: missing"
fi

echo
printf 'Default Hermes MCP: '
hermes mcp list 2>/dev/null | grep -q twozero_td && echo configured || echo missing
printf 'GPT Hermes MCP: '
HERMES_PROFILE=gpt hermes mcp list 2>/dev/null | grep -q twozero_td && echo configured || echo missing

printf 'twozero port 40404: '
if nc -z 127.0.0.1 40404 >/dev/null 2>&1; then
  echo READY
else
  echo NOT_READY
fi
