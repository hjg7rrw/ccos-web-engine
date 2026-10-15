# Addendum — Intermittent Headless WebGL2 Availability (F-012)

**Fresh observation, October 14–15, 2026.** The same Debian/Chromium/Playwright container initially produced a passing WebGL2 shader+pixel test in headless mode both with and without Xvfb.

Later, after additional browser testing, the independent headless modes **both returned null WebGL2 contexts** without a display. These failures were captured in the local release's `qa-webgl2/history/reprobe_after_fixture_failure.json`.

A retry under Xvfb passed all four expected software configurations (two headless modes on Xvfb plus headed SwiftShader and headed Mesa); headed default returned null as previously observed. The actual 4,800-particle app also passed at both tested viewports.

The separate HTML diagnostic fixture failed headlessly without display but passed **headed on Xvfb + ANGLE SwiftShader**, including shader compilation, an actual drawn triangle, center pixel `[41,186,117,255]`, and GL error 0.

## Delta WGL-011: MODIFY reliability guidance

The claim 'headless sometimes works' is supported; the claim 'headless works reliably here' is **not** supported. For a repeatable test in this environment, choose ephemeral Xvfb and explicitly select SwiftShader or Mesa. Run the no-display headless probe as exploratory, not as the sole acceptance gate.

The unique cause of intermittent headless failure remains **UNKNOWN**; browser process state, policy, resource initialization and host graphics infrastructure are candidate explanations, not verified root causes. Do not delete or reclassify the failure as a success just because a later retry passed.

## Controls to add next

1. Repeat both paths over many fresh browser processes, persisting per-run outcomes.
2. Compare Chromium GPU log/flags, EGL selections and process exit conditions.
3. Make a fresh QA environment required for each controlled test batch where practical.
4. Treat application and graphics capability as separate gates.
5. Keep untrusted pages away from the browser profile when software-GL safety overrides are present.

**Source data in full local release:** `qa-webgl2/history/reprobe_after_fixture_failure.json`, `qa-webgl2/history/baseline_no_display.json`, `qa-webgl2/history/capability_matrix.json`, and the successful fixture screenshot.
