# CCOS_WEBGL2_OPERATOR v0.1.3

**Trigger:** Diagnose WebGL2/Chromium/software GPU availability or rerun our 3D website.

1. Inspect environment and prior failure/delta ledger, then identify whether the target is capability, application, resource loading or performance.
2. Run headless no-display probe and persist JSON.
3. If Linux Xvfb exists, run the five-mode matrix to try default, SwiftShader and Mesa, log failures too.
4. Require actual GLSL ES 3.00 compile/link/draw/readPixels; no simulated canvas evidence.
5. Run CCOS browser app integration and verify pixels, particle count, shape selection, UI, GL errors and browser errors.
6. Classify failures: dependency/process/display/context/shader/draw/state/navigation/policy/performance.
7. Change only smallest responsible variable; retest successes as non-regression.
8. Update ledger with source version, mode, outcome, root-cause certainty, unverified boundaries, next actions.
9. Keep software rendering confined to trusted local sources if unsafe flags are used. No source/asset piracy or unrelated repo edits.
10. Separate user / AI / collaboration responsibilities and report completion state.

**Acceptance:** the application is NOT production-approved until normal resource loading, real-device hardware tests and deployment requirements also pass.
