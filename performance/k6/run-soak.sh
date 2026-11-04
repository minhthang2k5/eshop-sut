#!/usr/bin/env bash
set -euo pipefail
TEST_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
command -v k6 >/dev/null
command -v python3 >/dev/null
mkdir -p "$TEST_DIR/output"
RUN_DIR="$(mktemp -d "$TEST_DIR/output/soak-$(date +%Y%m%d-%H%M%S)-XXXXXX")"
printf 'Soak output: %s\n' "$RUN_DIR"

# Find the most recent telemetry file belonging to a live backend.
SOURCE=""
if [[ "${TELEMETRY:-1}" != 0 ]]; then
  SOURCE="${TELEMETRY_FILE:-}"
  if [[ -z "$SOURCE" ]]; then
    for FILE in "${TELEMETRY_DIR:-$TEST_DIR/output/telemetry}"/server-*.jsonl; do
      NAME="${FILE##*/}"
      if [[ "$NAME" =~ -([0-9]+)-[0-9]+\.jsonl$ ]] && kill -0 "${BASH_REMATCH[1]}" 2>/dev/null; then
        if [[ -z "$SOURCE" || "$FILE" -nt "$SOURCE" ]]; then SOURCE="$FILE"; fi
      fi
    done
  fi
  if [[ ! -f "$SOURCE" ]]; then
    printf 'Không tìm thấy file CPU/RAM của backend; vẫn chạy k6.\n'
    SOURCE=""
  fi
fi
OFFSET=0
if [[ -n "$SOURCE" ]]; then OFFSET=$(wc -c < "$SOURCE"); fi
BEFORE_START=$(date +%s%3N)
K6_START=""
K6_END=""
K6_PID=""
LOGGER_PID=""
INTERRUPTED=false

interrupt() {
  INTERRUPTED=true
  if [[ -n "$K6_PID" ]]; then kill -"$1" "$K6_PID" 2>/dev/null || true; fi
}
finish() {
  RESULT=$?
  trap - EXIT
  END=$(date +%s%3N)
  {
    printf '{"before_start_ms":%s,"after_end_ms":%s,"interrupted":%s' "$BEFORE_START" "$END" "$INTERRUPTED"
    if [[ -n "$K6_START" ]]; then printf ',"k6_start_ms":%s' "$K6_START"; fi
    if [[ -n "$K6_END" ]]; then printf ',"k6_end_ms":%s' "$K6_END"; fi
    printf '}\n'
  } > "$RUN_DIR/measurement-timeline.json"
  # Persist scenario clock/profile directly; never infer them from directory names.
  python3 - "$RUN_DIR" <<'PYTIMELINE'
import json, pathlib, sys
run = pathlib.Path(sys.argv[1])
p = run / 'measurement-timeline.json'
timeline = json.loads(p.read_text())
log = run / 'k6.log'
for line in log.read_text().splitlines() if log.exists() else []:
    if 'SOAK_TIMELINE ' not in line:
        continue
    try:
        marker, _ = json.JSONDecoder().raw_decode(line.replace('\\"', '"').split('SOAK_TIMELINE ', 1)[1])
        timeline.update(scenario_start_ms=marker['start_ms'], profile=marker['profile'])
        break
    except (ValueError, KeyError):
        continue
p.write_text(json.dumps(timeline) + '\n')
PYTIMELINE
  if [[ -n "$SOURCE" ]]; then
    tail -c "+$((OFFSET + 1))" "$SOURCE" > "$RUN_DIR/node-cpu-ram.jsonl"
  fi
  printf 'Kết quả: %s\n' "$RUN_DIR"
  exit "$RESULT"
}
trap finish EXIT
trap 'interrupt INT' INT
trap 'interrupt TERM' TERM

# 1. Before soak: collect idle CPU/RAM for 30 seconds.
if [[ -n "$SOURCE" ]]; then
  printf 'Thu CPU/RAM trước tải: 30s...\n'
  sleep 30 || true
fi
if [[ "$INTERRUPTED" == true ]]; then exit 130; fi

# 2. Run soak.js. Keep k6's exit code, including threshold failure (99).
K6_START=$(date +%s%3N)
exec 3> >(tee "$RUN_DIR/k6.log")
LOGGER_PID=$!
K6_WEB_DASHBOARD=true K6_WEB_DASHBOARD_OPEN=false K6_WEB_DASHBOARD_PORT=0 \
K6_WEB_DASHBOARD_EXPORT="$RUN_DIR/soak_report.html" \
k6 run --out "json=$RUN_DIR/metrics.json" \
  --summary-export="$RUN_DIR/summary.json" \
  "$TEST_DIR/soak.js" >&3 2>&1 &
K6_PID=$!
set +e
wait "$K6_PID"
K6_RESULT=$?
if [[ "$INTERRUPTED" == true ]]; then wait "$K6_PID"; K6_RESULT=$?; fi
set -e
K6_PID=""
K6_END=$(date +%s%3N)
exec 3>&-
wait "$LOGGER_PID" || true

# 3. After soak: keep the backend running and collect 60 more seconds.
if [[ -n "$SOURCE" && "$INTERRUPTED" == false ]]; then
  printf 'Thu CPU/RAM sau tải: 60s; giữ backend đang chạy...\n'
  sleep 60 || true
fi
if [[ "$INTERRUPTED" == true && "$K6_RESULT" == 0 ]]; then exit 130; fi
exit "$K6_RESULT"
