#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  forge-sage-watch.sh [--cwd PATH] [--interval SECONDS] [--tail LINES] "PROMPT"

Launch `forge-agent research` and print periodic heartbeat updates while it runs.
The script reports only observable signals:
  - elapsed time
  - process state / cpu / memory
  - whether output changed
  - the latest emitted output lines

It does not attempt to infer semantic progress.
EOF
}

CWD=""
INTERVAL=30
TAIL_LINES=20

while [[ $# -gt 0 ]]; do
  case "$1" in
    --cwd)
      CWD="${2:-}"
      shift 2
      ;;
    --interval)
      INTERVAL="${2:-}"
      shift 2
      ;;
    --tail)
      TAIL_LINES="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    -*)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      break
      ;;
  esac
done

if [[ $# -lt 1 ]]; then
  usage >&2
  exit 2
fi

PROMPT="$1"
LOG_FILE="$(mktemp -t forge-sage-watch.XXXXXX.log)"
START_TS="$(date +%s)"
LAST_SIZE=0

CMD=(forge-agent research)
if [[ -n "$CWD" ]]; then
  CMD+=(--cwd "$CWD")
fi
CMD+=("$PROMPT")

echo "[forge-sage-watch] launching: ${CMD[*]}"
echo "[forge-sage-watch] log: $LOG_FILE"

"${CMD[@]}" >"$LOG_FILE" 2>&1 &
PID=$!

report_status() {
  local now elapsed size ps_line
  now="$(date +%s)"
  elapsed="$(( now - START_TS ))"
  size="$(wc -c <"$LOG_FILE" | tr -d ' ')"
  ps_line="$(ps -p "$PID" -o pid=,etime=,stat=,%cpu=,%mem=,command= 2>/dev/null || true)"

  echo "[forge-sage-watch] elapsed=${elapsed}s pid=${PID}"
  if [[ -n "$ps_line" ]]; then
    echo "[forge-sage-watch] process: $ps_line"
  else
    echo "[forge-sage-watch] process: exited"
  fi

  if [[ "$size" -gt "$LAST_SIZE" ]]; then
    echo "[forge-sage-watch] output grew: ${LAST_SIZE} -> ${size} bytes"
    echo "[forge-sage-watch] recent output:"
    tail -n "$TAIL_LINES" "$LOG_FILE"
  else
    echo "[forge-sage-watch] no new output yet"
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

echo "[forge-sage-watch] completed with exit=$STATUS"
FINAL_SIZE="$(wc -c <"$LOG_FILE" | tr -d ' ')"
if [[ "$FINAL_SIZE" -le 20000 ]]; then
  echo "[forge-sage-watch] final output:"
  cat "$LOG_FILE"
else
  echo "[forge-sage-watch] final output too large to print in full; tail follows"
  tail -n 80 "$LOG_FILE"
fi
echo "[forge-sage-watch] full log saved at: $LOG_FILE"

exit "$STATUS"
