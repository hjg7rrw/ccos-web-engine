# CCOS WebGL2 Capability Laboratory — Environment & Reproduction Playbook v0.1.3

**Owner:** Andrew Rosa / CCOS Studio. **Status:** verified in Debian 13 environment; cross-host portability remains to be tested. **Evidence labels:** OBSERVED, DOCUMENTED, INFERRED, UNTESTED.

## Objective

Independently verify the ability to compile/link WebGL2 GLSL shaders and **draw and read real pixels**, then run the original CCOS 4,800-point WebGL2 application under a software renderer. Keep all failure paths and environment differences visible.

## Tested environment — OBSERVED

- Debian GNU/Linux 13 (trixie), Linux container; physical `/dev/dri` not available in earlier inspection.
- Chromium 144.0.7559.96; Python 3.13.5; Python Playwright 1.57.0; Node 22.16.0.
- Graphics backend A: Chromium ANGLE + SwiftShader, Vulkan software renderer.
- Graphics backend B: Chromium ANGLE + Mesa llvmpipe, software OpenGL renderer.
- Xvfb `xvfb-run -a` creates an ephemeral 1440×900, 24-bit virtual X11 screen.
- Offscreen software EGL initialized in earlier investigation; this did **not alone** establish browser access.
- Shader probe must check `getContext('webgl2')`, program compile/link, `drawArrays`, center `readPixels`, GL error status, not just strings.

## Fast path (pre-existing sandbox already has these tools)

```bash
cd CCOS_WebGL2_Lab_v0.1.3
./ops/run_all_linux.sh
```

This runs Node math tests; Python generator test; 5-mode graphics matrix; and real app integration at 1366×768 and 390×844. Results written to `qa-webgl2/history/capability_matrix.json` and `qa-webgl2/webgl2_qa.json`, with screenshots under `qa-webgl2/`.

## Preparing a compatible Ubuntu / Debian machine (requires explicit local admin permission)

```bash
sudo apt-get update
sudo apt-get install -y chromium xvfb xauth libegl1 libgl1-mesa-dri python3 python3-venv nodejs npm
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-webgl2.txt
./ops/run_all_linux.sh
```

No install action was required or executed as part of our validated test; the listed commands are **installation instructions, not test results**. Distribution package names vary by release. Ubuntu's Chromium packaging may use Snap; if system Chromium is missing, install Playwright's bundled browser using `python -m playwright install chromium` and specify the browser binary where applicable. No GPU access is assumed.

## All graphics modes

```bash
# No display. In this *current* environment these unexpectedly passed:
env -u DISPLAY -u EGL_PLATFORM -u LIBGL_ALWAYS_SOFTWARE -u MESA_LOADER_DRIVER_OVERRIDE \
 python3 ops/webgl2_probe.py --modes headless-default,headless-swiftshader \
 --output qa-webgl2/history/baseline_no_display.json

# Full matrix with a virtual X display and both software rendering paths:
./ops/run_matrix_linux.sh

# Integration-level page rendering and UI/particle tests:
./run_webgl2_qa.sh
```

`ops/webgl2_probe.py` returns success for one or more supported modes if `--require-one` is set; it logs each pass/failure even when the overall command succeeds. Inspect each individual probe, not just the command's exit code.

## What commands and settings do

| Mechanism | Purpose | Caveat |
|---|---|---|
| `xvfb-run -a` | Private virtual X11 server, temporary display | Requires Xvfb/xauth, no hardware GPU implied |
| `--use-gl=angle --use-angle=swiftshader` | Force ANGLE with SwiftShader software graphics | Version-specific flags; some Chrome builds may differ |
| `--use-gl=angle --use-angle=gl` | ANGLE uses Mesa/llvmpipe software OpenGL with environment variables | Mesa packages/driver versions matter |
| `--enable-webgl --ignore-gpu-blocklist` | Allow WebGL and relax platform GPU screening | Diagnostic use only, never a guarantee |
| `--enable-unsafe-swiftshader` | Allow fallback software GL even when browser blocks it by policy | Security implications: only trusted offline content |
| `LIBGL_ALWAYS_SOFTWARE=1` | Request Mesa software renderer | Does not force ANGLE SwiftShader |
| `MESA_LOADER_DRIVER_OVERRIDE=llvmpipe` | Request Mesa llvmpipe software driver | Driver-specific; not universal |
| `EGL_PLATFORM=x11` | Select Mesa EGL X11 platform | Need a working X server |
| `page.set_content` | Bypasses browser navigation restriction for trusted local first-party HTML | Does **not** test ES module imports or normal HTTP navigation |
| `preserveDrawingBuffer:true` | Keeps offscreen WebGL probe pixels available to read | Diagnostic probe only; application rendering may normally clear buffer |

## Browser sandbox and trust boundary

Earlier Playwright/Chromium in this environment could not enable Chromium's standard sandbox and navigation is constrained by managed policy. The tests intentionally load **only internally generated HTML or audited CCOS-local files** and make no remote requests. The testing flags are not safe justification for visiting untrusted pages. This is a QA lab, not a public web browser or internet-exposed service.

Do not expose an unauthenticated HTTP control service, credentials, arbitrary code execution endpoints or proxy within this environment. If the code changes to load external assets, inspect rights and trust posture first.

## Windows (UNTESTED here)

Use `ops/Run-WebGL2Probe.ps1` in a PowerShell window with Python/Playwright and Chromium installed. Windows does not use Xvfb. It may allow normal hardware WebGL2 or ANGLE SwiftShader depending on graphics driver and browser policy. The PS script is a convenience path, not verified Windows equivalence.

## Troubleshooting decision tree

1. **Python import fails:** install Playwright into the **same interpreter** running the script.
2. **Chrome launch fails:** find Chromium binary or use bundled Playwright chromium, check sandbox restrictions and installed shared libraries.
3. **Headed browser launch fails:** set up Xvfb on Linux, verify `$DISPLAY` inside runner.
4. **`getContext('webgl2')` is null:** test explicit SwiftShader, then Mesa. Record browser GPU blocklist diagnostics; do not claim a renderer pass.
5. **Context exists but shader fails:** capture compile/link log, version, shader source ID and renderer string.
6. **Shader passes but pixel color is wrong:** verify framebuffer timing, viewport, target coordinates, context attributes and `gl.getError`; ensure pixels are read before default framebuffer discard.
7. **Lab passes but CCOS app fails:** isolate application shaders, resize/viewport, state transition, JS runtime errors and context loss.
8. **Application passes but `http://localhost` is blocked:** treat as separate *network/navigation policy* failure; `page.set_content` is not proof of HTTP loading.
9. **Performance low:** do not equate SwiftShader frame rate to physical hardware. Decrease DPR/point count and test real hardware before optimization claims.

## Acceptance hierarchy

P0: Runner starts and returns structured diagnostics, including failures. P1: genuine WebGL2 shader render/readback verified. P2: CCOS app draws visible 4,800-point field and GL errors = 0. P3: interaction, layout and JS console checks. P4: actual asset/ES module loading via HTTP (OPEN). P5: native GPU/device/browser performance (OPEN). P6: integration in public deployment (OPEN).
