# CCOS Web Engine — controlled validation report

**Run ID:** CWE-RUN-2026-10-14-01  
**Version:** v0.1 candidate  
**Scope:** local source, script, public-source and partial browser QA.  
**Date:** 2026-10-14

## Verified, actually executed

- Node executable present; scripts parsed with `node --check`.
- Node native unit suite: **4/4 pass** (bounded interpolation, deterministic 3D geometry, invalid input handling, matrix finite/dimensions).
- Python scaffold generator suite: **1/1 pass**. Generator creates an independent site and refuses to overwrite existing output.
- Python scripts compile without syntax errors.
- HTTP server on localhost responded **200 OK**, serving the main website markup.
- Public-site audit against own local server reported HTTP **200**, title, metadata, stylesheet, one module script, zero image assets and seven hyperlinks.
- Public `www.igloo.inc` and Awwwards page requests were blocked/unavailable from this code container. Separate authenticated research tools fetched the Awwwards developer case study; therefore production techniques are documented from that public source rather than inferred from missing HTML.
- GitHub connector examined linked repository names and root directories in read-only mode. No writes, deployments, new repositories or external user account changes performed.

## Not verified — honest blockers

- Full runtime WebGL2 rendering: local Chromium's graphical environment failed to initialize a usable GTK/EGL context; `Playwright` browser launch failed. Therefore no successful screenshot or browser-interaction test is claimed.
- GPU frame rate, mobile hardware frame rate, shader compile in a production browser, actual context recovery and remote hosting.
- Accessibility compliance with assistive technology and accessibility test tools.
- Exact Igloo source implementation or its production performance.
- Live run of the independent GitHub metadata scanner from this code container (outbound DNS for npm and some HTTP requests failed); public repositories were separately inspected via connected GitHub tools.

## QA gate verdict

**Candidate / controlled internal study. NOT production-approved.** Browser, device and accessibility QA must pass before publication. The project contains a Playwright smoke harness to run on a normal local workstation with browser support.

## Highest-value next test

On a Windows workstation with Chrome/Edge installed: run the Python server, open the site, use three controls, inspect Chrome DevTools Console for WebGL errors, test a mobile viewport, and run `python3 tests/browser_smoke.py http://localhost:8080` after installing Playwright and its browser only if desired. Save results under the next numbered run ID and resolve any reproducible failures.

**Historical note:** Newer v0.1.2/v0.1.3 tests later established software WebGL2; this v0.1 report retains the older failed configuration.
