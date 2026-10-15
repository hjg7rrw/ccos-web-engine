# CCOS WebGL2 Laboratory: Test Evidence & Provenance

**OBSERVED (current run):** Headless Chromium with or without explicit SwiftShader successfully compiled/link GLSL and drew readable WebGL2 pixels in the tested environment. Headed Chrome under Xvfb without backend flags returned a null WebGL2 context. Explicit ANGLE SwiftShader and Mesa llvmpipe both passed. The full CCOS application passed at 1366x768 and 390x844 with 4,800 points, controls, and no observed JS errors.

**HISTORICAL:** First headless attempts returned null contexts; earlier v0.1.2 lab achieved WebGL2 only through headed Chromium + Xvfb. Previous temporary framebuffer readback failed until sampling was moved to the render frame. Mobile heading overflow was fixed in v0.1.1. Previous results remain legitimate observations of earlier configurations; they do not establish universal impossibility.

**INFERRED:** Browser flags, renderer/backend selection and managed environment conditions likely affected earlier attempts. They were not individually controlled enough to identify a unique root cause.

**UNVERIFIED:** Chromium HTTP navigation policy bypass or functioning ES module loads via normal URL, physical hardware GPU performance, Windows/macOS portability, long-term reliability and external deployment.

**Source policy:** Original CCOS authored shaders and project code are distinct from Igloo's proprietary effects. The reusable diagnostic is independently authored and should not fetch or copy third-party assets.

**Security limit:** --enable-unsafe-swiftshader and restricted sandbox configurations must remain in an isolated QA profile with trusted local content, never repurposed for arbitrary browsing.

**Primary evidence files:** local release `CCOS_WebGL2_Lab_v0.1.3/qa-webgl2/history/capability_matrix.json`, `baseline_no_display.json`, `qa-webgl2/webgl2_qa.json`, and test screenshots. This branch carries a summarized JSON registry and source-level reproduction logic; complete binary screenshots remain in the local archived release.
