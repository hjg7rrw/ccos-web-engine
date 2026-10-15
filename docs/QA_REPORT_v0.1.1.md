# CCOS Web Engine v0.1.1 — Local Execution and Quality Assurance

Date: 2026-10-14
Status: **Conditional PASS for static serving, automated checks and browser fallback; WebGL2 rendering UNVERIFIED.**

## Verified in the execution container
- Source ZIP extracted and content inspected.
- `node --test tests/*.test.mjs`: 4 JavaScript math/geometry tests passed.
- `python3 -m unittest discover -s tests -p 'test_*.py' -v`: 1 website-scaffold test passed.
- Python files compiled successfully.
- Python static HTTP server bound on 127.0.0.1, port 8765; returned HTTP 200 for index.
- Browser Chromium could launch, but network navigation to 127.0.0.1 was rejected with `ERR_BLOCKED_BY_ADMINISTRATOR`. This is an environment navigation restriction, not a failure of the static HTTP server.
- Browser `set_content` loaded the original first-party page HTML, CSS and scripts combined in-memory, and exercised five viewport sizes: 1366×768, 768×1024, 390×844, 375×812, 320×700.
- All five injected fallback/interaction tests passed: one main h1, three scenes, no horizontal overflow, particle preset button reflected `aria-pressed=true`, diagnostics appeared on click, and zero page JavaScript exceptions.
- Browser `getContext('webgl2')` returned false, and renderer correctly displayed `CSS FALLBACK / WEBGL2 UNAVAILABLE`. This **does not validate the GPU animation or shader effects**.

## Regression fix: mobile typography
Observed original v0.1 on 390px viewport: last heading `DIMENSION.` extends beyond right viewport edge (right bound 415px). Adjusted media-rule h2 font sizing to `min(13vw,3.3rem)`. Repeated tests show no overflow at 320, 375 or 390px. Original v0.1 remains preserved separately.

## Pending gates
1. Real browser navigation to the locally served site (restricted by this container's browser policy).
2. Hardware or software WebGL2 shader compile/render, particle-morph visual inspection and continuous FPS observation.
3. Touch-device behavior, actual GPU/device performance, reduced-motion and cross-browser QA.
4. Deployment to a user-approved public or staging destination.

## Screenshots
`qa_preview_desktop.png` and `qa_preview_mobile.png` are genuine headless Chromium fallback layout captures, **not evidence of GPU-rendered 3D**.

No existing GitHub repositories were modified in this run.
