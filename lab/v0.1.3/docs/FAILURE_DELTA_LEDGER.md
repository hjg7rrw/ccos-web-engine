# WebGL2 Failure & Delta Ledger — CCOS v0.1.3

Version trajectory: v0.1 original procedural WebGL2 demo → v0.1.1 responsive fix → v0.1.2 SwiftShader+Xvfb render proof → v0.1.3 general capability matrix and reusable operator.

| ID | Classification | Symptom | Intervention | Outcome |
|---|---|---|---|---|
| F-001 | HISTORICAL | First headless probes returned no WebGL1/2 | Tried multiple Chromium flags/renderers | Failed in that configuration; cause incompletely isolated |
| F-002 | HISTORICAL | HTTP 200 but browser policy rejects localhost navigation | Use trusted local `page.set_content` | Browser UI/render QA works; ES-module/HTTP loading unverified |
| F-003 | HISTORICAL | Mobile `DIMENSION.` heading overflows 390px | `font-size:min(13vw,3.3rem)` | Five responsive viewports passed |
| F-004 | HISTORICAL | CSS fallback okay; 3D not testable | Xvfb headed Chromium ANGLE/SwiftShader | 4,800 WebGL2 points visibly render |
| F-005 | HISTORICAL | False negative from blank pixel samples | Sample in render cycle; use preserved buffer in standalone probe | Real pixel test passed |
| F-006 | FRESH | Headed default graphics on Xvfb returns null context | Select ANGLE/SwiftShader or Mesa llvmpipe explicitly | Both alternate software backends pass |
| F-007 | FRESH | Old claim 'headless always blocked' conflicts with fresh test | No-display headless retry | Current headless default and headless SwiftShader pass; old universal claim superseded |
| F-008 | FRESH | Environment success alone not app correctness | Independent real app QA desktop+mobile | Both pass; 4 Node math tests and Python scaffold pass |
| F-009 | LIMIT | Software FPS varies with viewport | Report renderer and scope | Container FPS is not a physical hardware comparison |
| F-010 | OPEN | Normal HTTP module path not run in constrained browser | Future permitted browser environment | Unverified |
| F-011 | OPEN | Windows/other Linux distributions may differ | Port runner and repeat tests | Not promoted |

## Governance deltas
- **RETAIN:** real GLSL 300 ES draw + framebuffer read, GL error and renderer info as capability gates.
- **MODIFY:** evaluate headless and headed paths separately; don't infer one from the other.
- **SUPERSEDE:** globally categorical 'headless graphics blocked' claim.
- **RETAIN:** Xvfb + SwiftShader works without physical GPU; renderer/backends recorded.
- **AUGMENT:** Mesa llvmpipe alternate; per-mode JSON failures; security and provenance.
- **PROPOSED, NOT PROMOTED:** CI, physical GPU matrix, HTTP loading, cross-device performance.

## Strongest supported interpretation
The initial failure was contingent on conditions and/or invocation details rather than WebGL2 intrinsically requiring a GPU or Xvfb. A unique root cause for the very first headless failures cannot be deduced from the available uncontrolled runs.

## Red-team checks
Passing Python launch is not GL success; GL version is not a successful draw; triangle pixel proof is not app proof; WebGL screen capture is not HTTP loading proof; viewport simulation is not a phone GPU; success on one host is not broad portability; unsafe SwiftShader flags are not appropriate for arbitrary websites.

A failed mode is preserved as evidence, not automatically patched away. Each adaptation must state TEST RESULT vs INFERENCE, its exact version and scope.
