#!/usr/bin/env bash
# Run from any directory; keep each run's artifacts together and preserve k6's exit code.
set -euo pipefail
TEST_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$TEST_DIR/output"
RUN_DIR="$(mktemp -d "$TEST_DIR/output/baseline-$(date +%Y%m%d-%H%M%S)-XXXXXX")"
printf 'Baseline output: %s\n' "$RUN_DIR"
K6_WEB_DASHBOARD=true \
K6_WEB_DASHBOARD_OPEN=false \
K6_WEB_DASHBOARD_PORT=0 \
K6_WEB_DASHBOARD_EXPORT="$RUN_DIR/baseline_report.html" \
k6 run --out "json=$RUN_DIR/metrics.json" \
  --summary-export="$RUN_DIR/summary.json" \
  "$TEST_DIR/baseline.js" 2>&1 | tee "$RUN_DIR/k6.log"
