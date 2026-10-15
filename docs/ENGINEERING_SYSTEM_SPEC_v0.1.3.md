# CCOS WebGL2 Engine & Diagnostic System — Architecture / Skill Contract v0.1.3

## Functional architecture

```text
SOURCE+CANON --> Scene/particle data --> Browser JS application --> WebGL2 state+shaders
                                                          |                |
                                              UI+scroll+interactions       v
                                                     |            Draw/animation frame
                                                     |                |
                                                     +----> QA integration screenshot+GL readings

ENVIRONMENT --> Browser launcher --> WebGL2 capability probe (separate standalone GLSL fixture)
                  |                    |
                  |                    +--> Per-mode JSON successes AND failures
                  +--> Xvfb headless/headed software renderer selection

LEDGER --> Failing mode/reproducer/root-cause hypothesis --> Minimal patch --> Retest --> Versioned delta
```

## Original v0.1.2 renderer logic

- `src/math.js`: deterministic procedural samplers for 3 shapes and 4×4 camera projection matrices.
- `src/engine.js`: WebGL2 point shaders, data buffers, point morph and browser render loop, WebGL context loss and adaptive DPR.
- `src/main.js`: scroll position and page/shape controls drive the renderer.
- `src/styles.css`: responsive HUD and accessible text/control fallback.
- `src/data.js`: modular world descriptions.
- `tests/webgl2_software_qa.py`: first-party source assembled in deterministic module order for a local policy-constrained browser; integration-level pixel/interaction QA.
- `ops/webgl2_probe.py`: independent 128px real shader draw and pixel validation; runs five browser/backends.

## Test hierarchy / acceptance gates

| Gate | Evidence required | Authority |
|---|---|---|
| C0 - Availability | chromium, Playwright and display dependencies callable | Capability log |
| C1 - GL | `getContext('webgl2')` non-null and OpenGL ES 3.0 version | Live API reading |
| C2 - Shader | compile+link two GLSL 3.00 ES shader stages | Test fixture result |
| C3 - Draw | `drawArrays` triangle + center framebuffer RGBA + GL zero error | GPU/CPU backend pixel sample |
| C4 - Studio pipeline | CCOS particle renderer 4,800 points; desktop+mobile screenshots | Integration QA |
| C5 - Interaction | controlled shape changes, selected state, diagnostic display, JS no errors | Browser QA |
| C6 - Loading | HTTP/ES module import/navigation path tested | OPEN; don't infer |
| C7 - Performance | Repeatable physical hardware metrics | OPEN; don't infer |

## Skill interface

**Name:** CCOS_WEBGL2_LAB_OPERATOR v0.1.3. **Activation:** test or debug any browser graphics stack or interactive WebGL2 production. **Input:** trusted project directory, intended renderer modes, platform. **Output:** run configuration, capability matrix, app QA result, successful and failed cases, observed bottlenecks, next test and delta decision. **No silent promotion.**

**Control loop:** BOOT environment → ISOLATE browser capability → BENCH independent shader → VERIFY actual app → CLASSIFY failure → PATCH smallest causal layer → RETEST → NONREGRESSION → DOCUMENT new and old results → PROMOTE only after repeat evidence.

## Non-portable assumptions

This lab's configured flags, installed browser and Python package version are platform-specific. GPU safety policies vary. The browser may disallow actual local HTTP navigation. A simulated 390×844 viewport is not a real mobile browser or GPU. No paid service or Higgsfield connector is used.

## Continuous improvements and responsible expansion

Next tests: run on an independent Linux container; test actual HTTP module loading in a permitted browser; disable SwiftShader and measure genuine GPU hardware; introduce browser/engine crash recovery test; track GL context loss/restoration; verify power/thermal constraints for mobile; only then establish a production deployment standard.
