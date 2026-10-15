# CCOS WebGL2 Capability Laboratory v0.1.3

**Owner:** Andrew Rosa / CCOS Studio  
**Date:** 2026-10-14/15  
**Status:** Reproduced locally using Chromium software rendering. Safe isolated review branch; unrelated Jarvis source and the default branch are unchanged.

## Mission
Record every observed WebGL2 capability path and failed attempt, the browser launch logic, shader rendering and pixel validation, the downstream CCOS application acceptance gates, the environment assumptions, security boundaries, and all meaningful learning deltas. Igloo Inc. is a technical reference only; no proprietary assets or code are included.

## Verified environment
Debian GNU/Linux 13, Chromium 144.0.7559.96, Playwright 1.57.0, Python 3.13.5, Node 22.16.0. No physical GPU needed for the successful software rendering tests.

## Actual current backend matrix
| Browser mode | Result | Renderer |
|---|---|---|
| Headless, no X display | PASS | ANGLE / SwiftShader |
| Headless, explicit ANGLE SwiftShader | PASS | ANGLE / SwiftShader |
| Headed Chromium on Xvfb (no graphics overrides) | **FAIL** | WebGL2 context null |
| Headed Xvfb, ANGLE SwiftShader | PASS | ANGLE / SwiftShader |
| Headed Xvfb, ANGLE Mesa GL | PASS | Mesa / llvmpipe |

Tests use a real GLSL ES 3.00 vertex+fragment pair, compile and link the shaders, issue a draw call and read pixels from the WebGL framebuffer. A non-null API context is not sufficient for a PASS.

Earlier experiments reported that headless browser graphics were unavailable. Re-testing with isolated modes demonstrated headless software rendering works in the **current** environment. The universal headless blocker claim has been superseded, not silently erased.

## Application-level verification (v0.1.2 source, re-run for v0.1.3)
- Node.js math/geometry: 4/4 passed.
- Python new-site generator: 1/1 passed.
- Browser render integration: 1366x768 and 390x844 passed.
- On-screen WebGL2/4,800 particles, 11 sampled framebuffer colors, zero GL errors, shape controls and diagnostics passed.
- Approximate container software FPS: desktop 21-23 and mobile-size viewport 56-58; not physical-GPU benchmarks.
- Browser policy prevents navigation to the real HTTP server. Original CSS/JS is inlined for the browser QA; ES module loading over HTTP remains unverified.

## Files in this GitHub branch
- `ops/webgl2_probe.py`: independent browser/shader/pixel test; outputs JSON for each mode, success and failure.
- `ops/run_matrix_linux.sh`: temporary Xvfb display with SwiftShader/Mesa paths.
- `ops/Run-WebGL2Probe.ps1`: Windows-oriented unverified probe.
- `docs/FAILURE_DELTA_LEDGER.md`: observation history, failure modes, interventions and delta controls.
- `docs/ENVIRONMENT_PLAYBOOK.md`: reproducibility and security boundaries.
- `qa/observed_matrix.json`: source of the current capability records.
- `skills/CCOS_WEBGL2_OPERATOR.md`: reusable debugging and reporting procedure.

## Linux quick run
```bash
# Requires system Chromium, xvfb-run, Xvfb, Python 3, and the Playwright Python package
python3 -m pip install playwright==1.57.0
bash ops/run_matrix_linux.sh
```

Manual install may need OS package manager permissions; no installation commands are executed automatically by these files. Windows script is supplied for later validation; it is not claimed tested.

## Explicitly NOT verified
Normal HTTP/ES module loading in this managed browser, physical GPU speed, real mobile hardware, Windows and macOS parity, safe operation with arbitrary internet pages, or a publicly deployed host. The locally packaged v0.1.3 archive contains the complete older original CCOS interactive demo, source, image captures and all test scripts. This branch preserves the diagnostics and run logic in readable Git files, isolated from the Jarvis runtime.

## Controls
Only trusted self-authored/local HTML under the unsafe SwiftShader fallback. No secrets, no hidden API requests, no unsolicited dependency installs, no modifications to production Jarvis, no merge without explicit review. Git internal object identifiers are Git transport details, not project lineage. Studio lineage is maintained by explicit human-readable version IDs and delta records.

## Attribution
Original independent CCOS research/programming: Andrew Rosa / CCOS Studio. Technical background reference: [abeto's Igloo case study](https://www.awwwards.com/igloo-inc-case-study.html). All third-party licenses must be verified before source reuse.

## GitHub file permissions

Files created through the connected GitHub contents interface may not retain executable file mode. On Linux, invoke checked-in shell scripts with `bash ops/run_matrix_linux.sh` instead of relying on `./ops/run_matrix_linux.sh` until executable file permissions are explicitly set in Git.

## Later regression finding: intermittent headless availability

A separate no-display headless retest returned null contexts after earlier successful tests, while the Xvfb+ANGLE/SwiftShader and Mesa paths continued to pass. Headless is therefore **possible but not established reliable** in this host. See `docs/INTERMITTENT_HEADLESS_DELTA.md`. Always retain failure results; prefer the explicitly selected headed Xvfb software path for reproducible integration QA.
