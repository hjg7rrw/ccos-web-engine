#!/usr/bin/env bash
# Controlled Linux test: each browser mode is measured and logged, including failures.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v xvfb-run >/dev/null || { echo 'Missing Xvfb/xvfb-run'; exit 2; }
python3 -c 'import playwright.sync_api' || { echo 'Missing Python Playwright'; exit 2; }
export EGL_PLATFORM=x11
export LIBGL_ALWAYS_SOFTWARE=1
export MESA_LOADER_DRIVER_OVERRIDE=llvmpipe
xvfb-run -a -s '-screen 0 1440x900x24 -nolisten tcp' \
  python3 ops/webgl2_probe.py \
  --modes headless-default,headless-swiftshader,headed-default,headed-swiftshader,headed-mesa \
  --output qa/observed_matrix.json --require-one
