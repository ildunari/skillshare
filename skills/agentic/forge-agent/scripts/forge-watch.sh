#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  forge-watch.sh <subcommand> [subcommand args...]

Examples:
  forge-watch.sh research --cwd /path/to/repo "trace the bug"
  forge-watch.sh review "review the latest change"
  forge-watch.sh check "validate this repo"

This wrapper launches `forge-agent <subcommand> ...` and prints periodic
heartbeat updates based on observable signals:
  - elapsed time
  - process state / cpu / memory
  - whether output changed
  - the latest emitted output lines

It does not attempt to infer semantic progress.

Environment variables:
  FORGE_WATCH_INTERVAL  Poll interval in seconds (default: 30)
  FORGE_WATCH_TAIL      Tail line count when output changes (default: 20)
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ $# -lt 2 ]]; then
  usage >&2
  exit 2
fi

SUBCOMMAND="$1"
shift

INTERVAL="${FORGE_WATCH_INTERVAL:-30}"
TAIL_LINES="${FORGE_WATCH_TAIL:-20}"
LOG_FILE="$(mktemp -t forge-watch.XXXXXX.log)"
START_TS="$(date +%s)"
LAST_SIZE=0

CMD=(forge-agent "$SUBCOMMAND" "$@")

echo "[forge-watch] launching: ${CMD[*]}"
echo "[forge-watch] log: $LOG_FILE"

"${CMD[@]}" >"$LOG_FILE" 2>&1 &
PID=$!

report_status() {
  local now elapsed size ps_line
  now="$(date +%s)"
  elapsed="$(( now - START_TS ))"
  size="$(wc -c <"$LOG_FILE" | tr -d ' ')"
  ps_line="$(ps -p "$PID" -o pid=,etime=,stat=,%cpu=,%mem=,command= 2>/dev/null || true)"

  echo "[forge-watch] elapsed=${elapsed}s pid=${PID}"
  if [[ -n "$ps_line" ]]; then
    echo "[forge-watch] process: $ps_line"
  else
    echo "[forge-watch] process: exited"
  fi

  if [[ "$size" -gt "$LAST_SIZE" ]]; then
    echo "[forge-watch] output grew: ${LAST_SIZE} -> ${size} bytes"
    echo "[forge-watch] recent output:"
    tail -n "$TAIL_LINES" "$LOG_FILE"
  else
    echo "[forge-watch] no new output yet"
  fi

  LAST_SIZE="$size"
}

while kill -0 "$PID" 2>/dev/null; do
  sleep "$INTERVAL"
  report_status
done

if wait "$PID"; then
  STATUS=0
else
  STATUS=$?
fi

echo "[forge-watch] completed with exit=$STATUS"
FINAL_SIZE="$(wc -c <"$LOG_FILE" | tr -d ' ')"
if [[ "$FINAL_SIZE" -le 20000 ]]; then
  echo "[forge-watch] final output:"
  cat "$LOG_FILE"
else
  echo "[forge-watch] final output too large to print in full; tail follows"
  tail -n 80 "$LOG_FILE"
fi
echo "[forge-watch] full log saved at: $LOG_FILE"

exit "$STATUS"
