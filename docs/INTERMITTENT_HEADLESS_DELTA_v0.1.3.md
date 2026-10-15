# F-012 / WGL-011 — Intermittent Headless GL Context in the Same Container

**Evidence:** In the same session, independent headless probes without Xvfb initially returned WebGL2/SwiftShader PASS, then later BOTH returned null contexts under similar flags (`qa-webgl2/history/reprobe_after_fixture_failure.json`). This is a newly observed negative control, not a failed application build. Running a temporary Xvfb session restored the tested backends; `headed-default` still failed as expected, while explicit SwiftShader and Mesa passed.

The standalone trusted HTML fixture also failed in a headless no-display attempt, then passed when loaded in Chromium headed on Xvfb with ANGLE SwiftShader. Its framebuffer sample was `[41, 186, 117, 255]` with GL error 0, proving a real triangle was drawn on that configuration (`qa-webgl2/history/diagnostic_fixture_headed_xvfb.png`).

**Corrected claim:** Headless software rendering is POSSIBLE but NOT CONFIRMED RELIABLE in this test host; initial headless successes must not be extrapolated to robust unattended use. The precise reason for intermittent headless context failure is UNKNOWN, not conclusively a Chromium regression or a package issue.

**House rule candidate:** For controlled CI-like tests here, use a fresh ephemeral Xvfb session + explicitly selected ANGLE SwiftShader (or Mesa alternative), and re-run the capability probe when browser state or runtime changes. Document unsuccessful no-display attempts rather than silently retrying until green.

**Next experiment:** repeated independent processes, count success/failure by mode; compare browser GPU logs/runtime settings while holding versions fixed, and test another host. Keep the old v0.1.2 renderer proof intact.
