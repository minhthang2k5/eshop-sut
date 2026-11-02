#!/usr/bin/env bash
set -euo pipefail
TEST_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
command -v k6 >/dev/null
command -v python3 >/dev/null
mkdir -p "$TEST_DIR/output"
RUN_DIR="$(mktemp -d "$TEST_DIR/output/stress-$(date +%Y%m%d-%H%M%S)-XXXXXX")"
exec python3 "$TEST_DIR/telemetry/run_stress.py" "$RUN_DIR"
