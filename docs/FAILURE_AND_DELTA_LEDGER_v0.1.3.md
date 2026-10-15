# WebGL2 Experiment, Pain Point & Delta Ledger — CCOS v0.1.3

**Lineage:** CCOS Web Engine v0.1 → v0.1.1 responsive patch → v0.1.2 software-renderer breakthrough → v0.1.3 comprehensive capability matrix and reproducibility package. No prior release is overwritten. Entries below distinguish **historical observation** from **fresh test** and from **hypothesis**.

## Phase-by-phase evidence

| ID | Evidence | Original behavior / pain point | Root-cause status | Intervention | Result / exact boundary |
|---|---|---|---|---|---|
| F-001 | HISTORICAL | Chromium headless lacked WebGL1 and WebGL2 context in early probes | Suspected browser flags/display/managed environment, not conclusively isolated | Tried SwiftShader/ANGLE and EGL options in headless process | Early attempts failed. No blanket permanent headless prohibition is justified. |
| F-002 | HISTORICAL | Browser navigation to local web server blocked while HTTP 200 worked | Managed browser navigation policy | Used `page.set_content` from trusted local HTML + CSS + first-party JS compiled in controlled order | Visual/UI QA available, but normal HTTP/ES module loading still untested. |
| F-003 | HISTORICAL | At 390px, the word `DIMENSION.` overflowed the viewport | Responsive typography | Changed mobile h2 to `min(13vw,3.3rem)` in v0.1.1 | Five desktop/tablet/mobile width tests passed; original release preserved. |
| F-004 | HISTORICAL | HTML fallback loaded but particles could not be visually verified | No active WebGL2 context in that run | Installed no new hardware; instead used headed Chromium in ephemeral Xvfb + ANGLE SwiftShader | v0.1.2 GPU shaders and points actually rendered on desktop/mobile. |
| F-005 | HISTORICAL | Initial 3D pixel check falsely reported blank framebuffer | Default WebGL drawing buffer cleared/discarded between frames | Sampled pixels in requestAnimationFrame near actual draw; separate new probe uses preserveDrawingBuffer | v0.1.2 pixel validation passed; this is a test design fix, not shader fix. |
| F-006 | FRESH 2026-10-14/15 | User asked to generalize a single working launch into durable capability | Old instructions assumed headed Xvfb always needed | Independent 5-mode shader triangle + framebuffer matrix | `headless-default` PASS; `headless-swiftshader` PASS; `headed-default` FAIL; `headed-swiftshader` PASS; `headed-mesa` PASS under Xvfb. |
| F-007 | FRESH 2026-10-14/15 | Earlier account said headless still blocked | Browser mode flags and runtime environment not held constant across attempts | Re-ran headless defaults without DISPLAY/EGL/Mesa overrides | Both headless modes PASS in present environment; original blanket claim SUPERSEDED. |
| F-008 | FRESH 2026-10-14/15 | Rendering claims need regression controls | A working triangle alone does not prove full application | Original app QA + JS math + scaffold tests | All four Node checks + Python generator check + desktop/mobile original-app test PASS. |
| F-009 | KNOWN LIMIT | Software frame times not equal physical GPU timings | Software rasterizer is CPU-bound | Record software backend/vendor explicitly | Approx. 21–23 FPS desktop and 56–58 FPS mobile in these runs. Hardware comparisons not supported. |
| F-010 | OPEN | Navigation policy prevents normal direct browser app loading | Managed browser access restriction | Keep first-party inline QA path; propose separate trusted browser/runner later | Normal HTTP + ES module route remains UNVERIFIED. |
| F-011 | OPEN | CI/platform portability unspecified | Host packages/browser flags/browser policy vary | Linux and PowerShell scripts with dependency and runtime logs | Linux current host verified; Windows and cloud CI untested. |

## Delta register

| Delta | Change class | Evidence | Status |
|---|---|---|---|
| WGL-001 | RETAIN | WebGL2 shader compile/link + real framebuffer draw required to claim renderer capability | HOUSE CONTROL |
| WGL-002 | MODIFY | Renderer discovery: probe **headless and headed** separately | TEST SUPPORTED |
| WGL-003 | SUPERSEDE | Claim `headless browser still blocked` as universally true | OBSERVABLY FALSE in current session |
| WGL-004 | RETAIN | Xvfb + ANGLE/SwiftShader works without a physical GPU | RE-VERIFIED |
| WGL-005 | AUGMENT | Explicit Mesa/llvmpipe backend alternative | RE-VERIFIED |
| WGL-006 | AUGMENT | Per-mode JSON capability matrix and failure records | IMPLEMENTED + TESTED |
| WGL-007 | AUGMENT | Self-contained local shader/triangle fixture (independent app control) | IMPLEMENTED + TESTED via Playwright probe |
| WGL-008 | AUGMENT | One-command test runner and dependency/runbook docs | IMPLEMENTED + TESTED on this Linux host |
| WGL-009 | RETAIN | Original CCOS art/code untouched in active tests except version-specific copies | PROTECTED |
| WGL-010 | PROPOSED | Portable CI automation and hardware GPU tests | NOT PROMOTED |

## Strongest supported inference

The earlier failure was **environmental/configuration dependent**, not an inherent inability of WebGL2 to run without a GPU. Current observations prove selected Chromium software renderers work in this container, including headless operation. They **do not identify a single unique root cause** for all earlier headless failures because test flags and host state were not fully controlled then. This uncertainty remains open.

## Red-team assumptions
- Real rendering might be mistaken for simulated pixels. Mitigation: original shader sources, actual `gl.drawArrays`, GL pixel readback, and screenshots.
- Software WebGL may silently use a different backend. Mitigation: capture `UNMASKED_RENDERER_WEBGL`, version and capabilities for every run.
- A command may succeed if only one of five modes passes. Mitigation: inspect per-mode outcome; `--require-one` is a minimal functionality gate, not a universal pass.
- A good framebuffer sample can hide bad content layout. Mitigation: separate responsive/browser fallback suites and screenshot QA.
- A single host passing can encourage platform overclaims. Mitigation: explicit Windows/macOS/physical GPU/CI UNTESTED tags.
- Source package could depend on accidental network availability. Mitigation: zero network in core project, stable local source and auditable package footprint.
- Git storage could overwrite unrelated Jarvis/memory files. Mitigation: isolated GitHub branch and controlled file namespace; no merge without review.

## Useful learnings for downstream CCOS systems
1. Test **capability** independently from **application**, then layer integration tests above it.
2. Revisit past blockers when host versions, flags or display conditions change.
3. Keep actual failures in the acceptance record, not just successful runs.
4. A fallback only counts after direct testing; no hypothetical green status.
5. Log environment, state, mode, source version and outcome so later failures can be diagnosed without retraining the agent.
6. Visual verification requires actual rendered output and controls; test framework success is not enough by itself.

## Additional fresh negative control — F-012 / WGL-011

After the initial five-mode and no-display successes, later no-display headless Chromium probes returned null WebGL2 contexts. That failure was recorded as `qa-webgl2/history/reprobe_after_fixture_failure.json`; a separate HTML fixture failed the same way. Re-running with ephemeral Xvfb restored explicit SwiftShader and Mesa software rendering and the CCOS application. **MODIFY**: headless possible ≠ headless reliable. Root cause still open; see `docs/INTERMITTENT_HEADLESS_DELTA_v0.1.3.md`.
