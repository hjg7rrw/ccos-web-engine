# Fresh Run Evidence — CCOS v0.1.3

Source: machine-readable JSON files in `qa-webgl2/`. No source values interpolated or assumed.

OS: Linux-6.18.44-x86_64-with-glibc2.41
Chromium: Chromium 144.0.7559.96 built on Debian GNU/Linux 13 (trixie)
Playwright: 1.57.0

## Xvfb multi-mode probe

| Mode | Result | Renderer |
|---|---|---|
| headless-default | PASS | ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver) |
| headless-swiftshader | PASS | ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver) |
| headed-default | FAIL | getContext(webgl2) returned null |
| headed-swiftshader | PASS | ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver) |
| headed-mesa | PASS | ANGLE (Mesa, llvmpipe (LLVM 19.1.7 256 bits), OpenGL 4.5) |

## No-display control

| Mode | Result | Renderer |
|---|---|---|
| headless-default | PASS | ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver) |
| headless-swiftshader | PASS | ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver) |

## CCOS original-app integration

| Viewport | WebGL2 | GL error | Distinct framebuffer sample colors | Interaction | Reported software FPS |
|---|---|---|---|---|---|
| 1366x768 | True | 0 | 11 | True | 21 |
| 390x844 | True | 0 | 11 | True | 56 |

**Caution:** Renderer strings and WebGL2 drawing were observed in the container; physical device tests, remote browsing and full production hosting have not been performed. A previous experiment reported headless failure under different parameters; the historical report remains in the older version, and the new test supersedes any universal no-headless claim.
