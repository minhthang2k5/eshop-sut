#!/usr/bin/env bash
# Run from any directory; keep each run's artifacts together and preserve k6's exit code.
set -euo pipefail
TEST_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$TEST_DIR/output"
RUN_DIR="$(mktemp -d "$TEST_DIR/output/smoke-$(date +%Y%m%d-%H%M%S)-XXXXXX")"
printf 'Smoke output: %s\n' "$RUN_DIR"
k6 run --out "json=$RUN_DIR/metrics.json" \
  --summary-export="$RUN_DIR/summary.json" \
  "$TEST_DIR/smoke.js" 2>&1 | tee "$RUN_DIR/k6.log"
