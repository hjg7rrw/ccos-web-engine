#!/usr/bin/env bash
# Master quality gate. All output remains in qa-webgl2/history and stdout.
set -euo pipefail
cd "$(dirname "$0")/.."
printf '\n[CCOS QA] Node geometry/matrix tests\n'
node --test tests/*.test.mjs
printf '\n[CCOS QA] Python website generator tests\n'
python3 -m unittest discover -s tests -p 'test_*.py' -v
printf '\n[CCOS QA] WebGL2 backend capability matrix\n'
bash lab/v0.1.3/ops/run_matrix_linux.sh
printf '\n[CCOS QA] Browser app integration (SwiftShader + Xvfb)\n'
bash run_webgl2_qa.sh
printf '\n[CCOS QA] COMPLETE: all required checks passed\n'
