# CCOS WebGL2 Environment Playbook v0.1.3

**Observed host:** Debian GNU/Linux 13; Chromium 144.0.7559.96; Python 3.13.5; Playwright 1.57.0; Node 22.16.0. Software renderers: ANGLE SwiftShader, Mesa llvmpipe. Physical GPU not required.

**Fast start:** `./ops/run_matrix_linux.sh` on a compatible Linux machine with Chromium, Python Playwright, xvfb-run/Xvfb/xauth installed. `python3 -m pip install playwright==1.57.0` may be used in a managed virtualenv. For a new host, installing Chromium/Xvfb may need administrator privileges and distro-specific package names.

**No-display baseline:** `env -u DISPLAY -u EGL_PLATFORM python3 ops/webgl2_probe.py --modes headless-default,headless-swiftshader --output qa/no_display.json`.

**What is really checked:** non-null WebGL2 context, shader compile/link, GLSL 300 ES triangle, framebuffer RGBA sample, zero GL error, per-mode output. The lab continues to log failed cases even when one mode succeeds.

**Key configurations:**

| Condition | Mechanism | Pain point / boundary |
|---|---|---|
| Headed browser in no-display Linux | `xvfb-run -a` | A visible X server is required |
| Force SwiftShader | `--use-gl=angle --use-angle=swiftshader` | Software GL, not a GPU performance estimate |
| Force Mesa | `--use-gl=angle --use-angle=gl` + `MESA_LOADER_DRIVER_OVERRIDE=llvmpipe` | Depends on Mesa packages |
| Permit software WebGL | `--enable-unsafe-swiftshader --enable-webgl --ignore-gpu-blocklist` | Only trusted local content; not safe browsing advice |
| No display Chromium | `headless=True` | Worked in the **current** run; earlier probes reported failure |
| Browser page loading | `page.set_content` | Does not prove normal HTTP navigation/ES module imports |
| Pixel sampling | Preserve WebGL drawing buffer or read promptly in render frame | Buffer may clear between frames |

**Troubleshooting sequence:** dependency import → executable/browser launch → X display → WebGL2 context → GLSL compilation/link → draw/GL errors → RGBA readback → original app interaction → HTTP loading → hardware benchmarking. Don't skip layers or call unsupported features verified.

**Security:** unsafe software WebGL flags and relaxed Chromium process sandbox, when applicable, are acceptable only for trusted local first-party content inside a contained QA environment. Never use this profile for untrusted public browsing. Never expose the runner as a public service.

**Known open gates:** real HTTP/ES-module loading, mobile hardware tests, physical-GPU performance, Windows/macOS compatibility, public deployment. These are not fulfilled by software rendering.

**Maintenance:** lock source version using readable version IDs, record all failed modes, change minimum causal layer, rerun prior successful tests. Never discard the failure ledger.
