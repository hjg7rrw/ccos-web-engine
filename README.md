# CCOS Web Engine — Independent WebGL2 Studio Lab

**Owner:** Andrew Rosa / CCOS Studio  
**Status:** Technical prototype / not production-approved

This is the dedicated repository for the CCOS Web Engine, separate from Jarvis. The WebGL2 capability laboratory documents Chromium software rendering using ANGLE SwiftShader, Mesa llvmpipe and Xvfb, with both successful and failed tests preserved.

## Transfer status

The repository now contains the **complete runnable original website engine** (`index.html`, `src/*`), its basic deterministic tests and generator, and the previously audited 12-file laboratory under `lab/v0.1.3/`. Remote inventory verifies **32 source files** at this stage. The complete v0.1.4 historical release also contains many additional documents, QA assets, and binary screenshots that have **not yet been mirrored**. GitHub's connected text-file writing interface cannot directly import the local ZIP or binary assets; that portion requires a separate authorized bulk upload route.

## Rights and QA limits

All rights reserved / source **UNLICENSED** unless explicitly relicensed. Igloo Inc. supplied technical inspiration, not proprietary source or media. Software-rendering flags like `--enable-unsafe-swiftshader` are for trusted first-party local tests only. Physical GPU performance, full HTTP module loading, Windows parity, and deployment are not verified.

See the lab documentation for operating scripts, failure logs, run matrices and known limitations. No Jarvis production files should be changed to use this independent repository.

**Current visibility: PUBLIC**. Source is unlicensed/all rights reserved. This public upload was requested by the repository owner. Do not commit credentials, private records or unreviewed third-party IP.
