# CCOS Web Engine — Verified software WebGL2 QA (v0.1.2)

**Date:** 2026-10-14/15 (environment UTC). **Owner:** Andrew Rosa / CCOS Studio.

## Problem and root cause

The previous headless browser context could not initialize WebGL1 or WebGL2. Debian 13 Chromium (144.0.7559.96) was running without physical `/dev/dri` and the default display variable pointed at no accessible X server. The system Mesa EGL surfaceless backend could initialize, but Chromium's headless GPU process failed.

## Tested fix

Launch Chromium **headed** inside a new, ephemeral Xvfb display. Pass `--use-gl=angle --use-angle=swiftshader --enable-webgl --enable-unsafe-swiftshader --ignore-gpu-blocklist` and use `EGL_PLATFORM=x11`, `LIBGL_ALWAYS_SOFTWARE=1`. The alternate `--use-angle=gl` path also initialized using Mesa llvmpipe. Software rendering means no physical GPU is required.

## Direct capability evidence
- `WebGL 2.0 (OpenGL ES 3.0 Chromium)` reported by `gl.VERSION`.
- `ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver)` from the WebGL debug renderer info extension.
- Mesa alternative: `ANGLE (Mesa, llvmpipe (LLVM 19.1.7 256 bits), OpenGL 4.5)`.
- Actual CCOS shader and particle rendering verified in screenshot captures (not 2D mockups). `gl.getError() == 0`, 11 distinct colors in sampled WebGL framebuffer pixels, and renderer state `WEBGL2 ONLINE / 4,800 LIVE PARTICLES`.
- Desktop and mobile interaction clicks work: Particle Engine => shape `HELIX`, diagnostics => `WebGL2`.
- JavaScript page errors: none during these tests.
- Independent regressions: 4 Node tests + 1 Python generator test passed.

## Test images and source evidence
- `qa-webgl2/webgl2_1366x768_initial.png`
- `qa-webgl2/webgl2_1366x768_interactive.png`
- `qa-webgl2/webgl2_390x844_initial.png`
- `qa-webgl2/webgl2_390x844_interactive.png`
- `qa-webgl2/webgl2_qa.json`

## Known boundaries
1. Browser is running **software** SwiftShader, not a physical GPU. The displayed FPS values are not representative of desktop/mobile consumer hardware.
2. Chromium managed browser policy prohibits website navigation. The QA uses `page.set_content` with local first-party JS modules joined in source order. This tests the actual WebGL2 rendering and UI behavior but not the original HTTP/ES-module resource loading flow.
3. In this container Chromium's own process sandbox cannot be enabled. Only trusted local assets are loaded, and remote navigation is prohibited. This is not a safe general-purpose web browsing configuration.
4. The Xvfb process and Chromium process are launched on demand; this environment is ephemeral and not a permanent public live preview or production host.
5. No external asset-rights or original Igloo implementation claims follow from this test.

## Reproduction
```bash
./run_webgl2_qa.sh
node --test tests/*.test.mjs
python3 -m unittest discover -s tests -p 'test_*.py' -v
```
The wrapper exits nonzero if the source fails graphics, geometry, interaction or page-error assertions.
