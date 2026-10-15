# CCOS WebGL2 Migration Security Gate — Delta v0.1.4

**Date:** October 15, 2026  
**Classification:** TEST RESULT + SOURCE-CONSTRAINT + AUGMENTED security control  
**Change status:** MODIFY (publisher only); RETAIN (engine v0.1.3 and prior learning)

## Repository state verified by connected GitHub API
- Destination: `hjg7rrw/ccos-web-engine` — exists, accessible, write permission exposed.
- **Visibility: PUBLIC**, empty repository at time of verification. A previous plan specified PRIVATE.
- This release is **NOT uploaded**. Publishing private project files to a public repository would break the stated repository contract.
- GitHub application tools exposed repository reads/writes but no repository-visibility action. An alternate app's available actions did not include changing repository visibility.

## New safeguards
1. Publisher defaults to a dry-run, with no remote access.
2. `--execute` requires a complete history bundle.
3. It requires the authenticated GitHub CLI to positively identify `PRIVATE` visibility.
4. It rechecks privacy immediately before uploading.
5. It stops if `main` already exists remotely (non-overwrite).
6. It restores the full Git history from a release bundle instead of making a disconnected new initial commit.
7. No Jarvis repository code is modified.
8. No credentials are embedded or printed.
9. Five negative-control regression tests verify public/missing-auth/refused paths.

## Current round of independently rerun tests
- JS geometry/projection tests: 4 PASS.
- Python site scaffolding regression: PASS.
- Python publisher negative controls: 5 PASS.
- WebGL2 browser capability on Xvfb: headless-default PASS, headless SwiftShader PASS, headed-default FAIL (null WebGL2 context), headed SwiftShader PASS, headed Mesa llvmpipe PASS.
- App Chromium WebGL2 integration: 1366x768 PASS and 390x844 PASS; 4,800 live particles; interactive controls and GL pixels verified.
- Software frame rates in this particular run were ~10 FPS (desktop) and ~29 FPS (mobile viewport). Earlier measurements were higher; these are not physical GPU benchmarks.

## Gaps, authorizations, responsibilities
- **USER (required):** In GitHub repository Settings → General → Danger Zone, switch visibility to PRIVATE. No terminal required.
- **AI (after GitHub reports PRIVATE):** Upload complete history/source using an authorized channel, read back the remote file inventory and compare with this manifest.
- **BOTH (later):** Real-device test, regular HTTP/module loading, deployment choice, and production approval.

No unauthorized public upload has occurred. The current stopping condition is account administration, not source readiness.

**HISTORICAL NOTICE:** This document records an earlier PRIVATE-only publication decision. The user later explicitly instructed the assistant to upload to the then-PUBLIC repository. It is archived for lineage, not current upload authorization.
