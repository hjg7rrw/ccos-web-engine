#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
for cmd in xvfb-run chromium python3; do
  command -v "$cmd" >/dev/null || { echo "Missing executable: $cmd"; exit 2; }
done
python3 -c 'from playwright.sync_api import sync_playwright' || { echo 'Python Playwright required for test runner'; exit 2; }
export LIBGL_ALWAYS_SOFTWARE=1
export EGL_PLATFORM=x11
export MESA_LOADER_DRIVER_OVERRIDE=llvmpipe
xvfb-run -a -s '-screen 0 1440x900x24 -nolisten tcp' python3 tests/webgl2_software_qa.py
