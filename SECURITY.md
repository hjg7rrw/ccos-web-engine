# CCOS WebGL2 Security Boundaries

- Do not commit keys, tokens, personal credentials, `.env` files, or browser profiles.
- Use `--enable-unsafe-swiftshader` and relaxed GPU flags only for trusted local first-party pages in an isolated QA process. Never use that browser for arbitrary websites.
- Prefer local-only HTTP bindings and ephemeral Xvfb sessions.
- Log all failed WebGL contexts, shader errors and framebuffer readback issues.
- Distinguish software rendering from physical GPU and smartphone performance.
- Preserve negative controls and lineage without promoting hypotheses to verified facts.
