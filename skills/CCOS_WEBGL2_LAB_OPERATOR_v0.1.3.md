# CCOS_WEBGL2_LAB_OPERATOR v0.1.3 — Reusable Agent Skill

**Purpose:** obtain evidence of WebGL2 execution across no-display/headed/browser/software backend configurations. Never conflate capability availability, rendering correctness, application function, resource loading or performance.

**Required inventory:** OS/runtime, browser binary+version, Playwright version, display state, renderer selection, content trust, project source revision, QA result location.

**Procedure:**
1. Read `docs/ENVIRONMENT_PLAYBOOK_v0.1.3.md` and `docs/FAILURE_AND_DELTA_LEDGER_v0.1.3.md`.
2. Run `python3 ops/webgl2_probe.py --modes headless-default,headless-swiftshader` for a no-display baseline.
3. When a virtual display is available, run `./ops/run_matrix_linux.sh`. Capture **every** outcome, including failure.
4. Run independent shader/program/triangle/readPixels assertions. A WebGL2 API object alone is not success.
5. Run original engine integration `./run_webgl2_qa.sh`, verify screenshots, real draw pixels, shape interaction, browser errors and responsive layout.
6. Locate smallest causal failure layer: environment, WebGL context, GLSL compile, scene logic, application UI, resource loading, browser policy, performance, cross-device.
7. Modify only responsible layer; retain previous version and previous successful tests.
8. Record source version, date, active constraints, test mode, outcome, root-cause evidence, unexpected side effects and next test.
9. Report with evidence labels: OBSERVED, INFERRED, UNVERIFIED; update RETAIN/MODIFY/SUPERSEDE/DEPRECATE ledger.

**Negative controls:** headless success must not be described as headed success; virtual mobile viewport is not mobile hardware; SwiftShader isn't a physical GPU benchmark; canvas pixel tests do not verify actual network/ES-module loading; browser sandbox overrides are suitable only for trusted local files; an unsuccessful attempt is a learning artifact, not discarded noise.

**Stop gates:** no permission for untrusted browsing with unsafe flags; no copied proprietary asset; no modifications to unrelated repository default branch; preserve reproducibility over hero claims.

**Responsibility:** AI runs controlled tools and documents results; user approves public deployment, hardware access and merging; both select future acceptance targets.
