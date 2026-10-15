# CCOS Web Engine — Independent WebGL2 Studio Lab

**Owner:** Andrew Rosa / CCOS Studio  
**Status:** Technical prototype / not production-approved

This is the dedicated repository for the CCOS Web Engine, separate from Jarvis. The WebGL2 capability laboratory documents Chromium software rendering using ANGLE SwiftShader, Mesa llvmpipe and Xvfb, with both successful and failed tests preserved.

## Transfer status

The first GitHub transfer contains the already-audited WebGL2 diagnostic files from the isolated Jarvis development branch at `CCOS/webgl2-lab/v0.1.3/`. The complete v0.1.4 graphics-engine archive (including browser screenshots and additional source) is held separately, and **is not yet fully mirrored to this repository**.

## Rights and QA limits

All rights reserved / source **UNLICENSED** unless explicitly relicensed. Igloo Inc. supplied technical inspiration, not proprietary source or media. Software-rendering flags like `--enable-unsafe-swiftshader` are for trusted first-party local tests only. Physical GPU performance, full HTTP module loading, Windows parity, and deployment are not verified.

See the lab documentation for operating scripts, failure logs, run matrices and known limitations. No Jarvis production files should be changed to use this independent repository.